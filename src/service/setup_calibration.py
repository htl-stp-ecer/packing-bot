from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from raccoon.hal import OdometrySource

if TYPE_CHECKING:
    from raccoon.robot.api import GenericRobot


class CalibrationAxis(Enum):
    FORWARD = "forward"
    LATERAL = "lateral"


@dataclass(frozen=True)
class _PoseSnapshot:
    x: float
    y: float
    heading: float

    @classmethod
    def from_pose(cls, pose) -> "_PoseSnapshot":
        return cls(
            x=float(pose.position[0]),
            y=float(pose.position[1]),
            heading=float(pose.heading),
        )

    def project(self, pose) -> tuple[float, float, float]:
        dx = float(pose.position[0]) - self.x
        dy = float(pose.position[1]) - self.y
        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)
        forward = dx * cos_h + dy * sin_h
        lateral = -dx * sin_h + dy * cos_h
        straight = math.hypot(dx, dy)
        return forward, lateral, straight


@dataclass(frozen=True)
class DriveCalibrationSample:
    axis: CalibrationAxis
    odom_distance_m: float
    ground_truth_distance_m: float
    source: str

    @property
    def scale(self) -> float:
        if abs(self.odom_distance_m) < 1e-9:
            return 1.0
        return self.ground_truth_distance_m / self.odom_distance_m


@dataclass
class IrCalibrationSet:
    sensor_ports: set[int] = field(default_factory=set)
    samples_by_port: dict[int, list[float]] = field(default_factory=dict)

    def add(self, port: int, samples: list[float]) -> None:
        self.sensor_ports.add(port)
        self.samples_by_port.setdefault(port, []).extend(float(v) for v in samples)

    def has_minimum_samples(self, min_samples: int) -> bool:
        return bool(self.sensor_ports) and all(
            len(self.samples_by_port.get(port, [])) >= min_samples
            for port in self.sensor_ports
        )


class SetupCalibrationSession:
    """Accumulates setup-time calibration evidence and applies a final trim."""

    def __init__(self, robot: "GenericRobot") -> None:
        self._robot = robot
        self._board_probe_done = False
        self._previous_preferred_source = None
        self._board_available = False
        self._gate_completed = False
        self._required_axes: set[CalibrationAxis] = set()
        self._required_ir_sets: set[str] = set()
        self._drive_samples: dict[CalibrationAxis, list[DriveCalibrationSample]] = {
            CalibrationAxis.FORWARD: [],
            CalibrationAxis.LATERAL: [],
        }
        self._ir_sets: dict[str, IrCalibrationSet] = {}

    @property
    def board_available(self) -> bool:
        return self._board_available

    @property
    def gate_completed(self) -> bool:
        return self._gate_completed

    def mark_pending(self) -> None:
        self._gate_completed = False

    def require_axis(self, axis: CalibrationAxis) -> None:
        self._required_axes.add(axis)
        self.mark_pending()

    def require_ir_set(self, set_name: str) -> None:
        self._required_ir_sets.add(set_name)
        self._ir_sets.setdefault(set_name, IrCalibrationSet())
        self.mark_pending()

    def axes_to_finalize(self, requested: list[CalibrationAxis] | None) -> list[CalibrationAxis]:
        axes = requested if requested else sorted(self._required_axes, key=lambda a: a.value)
        return list(axes)

    def ir_sets_to_finalize(self, requested: list[str] | None) -> list[str]:
        sets = requested if requested else sorted(self._required_ir_sets)
        return list(sets)

    def add_drive_sample(self, sample: DriveCalibrationSample) -> None:
        self._drive_samples[sample.axis].append(sample)
        self.mark_pending()

    def get_drive_samples(self, axis: CalibrationAxis) -> list[DriveCalibrationSample]:
        return list(self._drive_samples[axis])

    def add_ir_samples(
        self,
        set_name: str,
        sensor_ports: list[int],
        samples_by_port: dict[int, list[float]],
    ) -> None:
        bucket = self._ir_sets.setdefault(set_name, IrCalibrationSet())
        for port in sensor_ports:
            bucket.add(port, samples_by_port.get(port, []))
        self._required_ir_sets.add(set_name)
        self.mark_pending()

    def get_ir_set(self, set_name: str) -> IrCalibrationSet:
        return self._ir_sets.setdefault(set_name, IrCalibrationSet())

    def finish_gate(self) -> None:
        self._gate_completed = True

    def median_axis_scale(self, axis: CalibrationAxis) -> float:
        samples = self._drive_samples[axis]
        if not samples:
            return 1.0
        scales = sorted(sample.scale for sample in samples)
        mid = len(scales) // 2
        if len(scales) % 2 == 1:
            return float(scales[mid])
        return float((scales[mid - 1] + scales[mid]) / 2.0)

    def ensure_board_probe(self, robot: "GenericRobot", log_step) -> None:
        if self._board_probe_done:
            return
        self._previous_preferred_source = robot.odometry.get_preferred_source()
        robot.odometry.set_preferred_source(OdometrySource.CALIBRATION_BOARD)
        active = robot.odometry.get_active_source()
        self._board_available = active == OdometrySource.CALIBRATION_BOARD
        self._board_probe_done = True
        if self._board_available:
            log_step.info("Setup calibration: calibration board active")
        else:
            log_step.warn(
                "Setup calibration: calibration board unavailable; collect_drive will ask for manual distance"
            )

    def restore_odometry_source(self, robot: "GenericRobot", log_step) -> None:
        if self._previous_preferred_source is None:
            return
        robot.odometry.set_preferred_source(self._previous_preferred_source)
        active = robot.odometry.get_active_source()
        log_step.info(f"Setup calibration: odometry source restored to {active.name}")

    @staticmethod
    def capture_internal_snapshot(robot: "GenericRobot") -> _PoseSnapshot:
        return _PoseSnapshot.from_pose(robot.odometry.get_internal_pose())

    @staticmethod
    def capture_active_snapshot(robot: "GenericRobot") -> _PoseSnapshot:
        return _PoseSnapshot.from_pose(robot.odometry.get_pose())

    @staticmethod
    def axis_distance_m(start: _PoseSnapshot, end_pose, axis: CalibrationAxis) -> float:
        forward, lateral, _ = start.project(end_pose)
        return forward if axis == CalibrationAxis.FORWARD else lateral
