from raccoon import *

from src.hardware.defs import Defs
from src.steps.et_scan_align import EtScanAlign
from src.steps.setup_calibration import CalibrationAxis, calibration_gate, collect_drive


class M000SetupMission(SetupMission):
    setup_time = 120

    async def pre_start_gate(self, robot) -> None:
        await calibration_gate().run_step(robot)
        await robot._pre_start_gate()

    def sequence(self) -> Sequential:
        return seq([
            auto_tune(
                tune_bemf_velocity=False,
                tune_vel_lpf=False,
                tune_static_friction=False,
                tune_firmware_pid=False,
                tune_encoder_cal=False,
                tune_characterize=False,
                tune_velocity=False,
                tune_motion=True,
                tune_tolerances=False,
                motion_axes=["distance", "lateral", "heading"],
                step_confirm=False,
                persist=True,
            ),
            #
            # pause_setup_timer(),
            # fully_disable_servos(),
            # wait_for_button("move servos into starting position"),
            # start_setup_timer(),
            #
            # collect_drive(
            #     drive_forward(70, heading=0, speed=0.4),
            #     axis=CalibrationAxis.FORWARD,
            # ),
            #
            # calibration_gate(
            #     require_axes=[CalibrationAxis.FORWARD],
            # ),
            #
            # # parallel(
            # #     Defs.pom_grab.start(),
            # #     Defs.shild.down(),
            # #     Defs.shild_graber.closed(),
            # # ),
            # #
            # # parallel(
            # #     Defs.pom_arm.start(100),
            # # ),
            # #
            # # Defs.shild.up(),
            # #
            # #
            # # #auto_tune(
            # # #    vel_axes=["vy"],
            # # #    tune_motion=False,
            # # #    characterize_axes=["lateral"]
            # # #),
            # # loop_for(
            # # slow_servo(Defs.pom_arm, 170, 20),
            # # slow_servo(Defs.pom_arm, 0, 20),
            # # calibrate(distance_cm=70,
            # #           ema_alpha=0.3,
            # #           # calibration_sets=["default", "upper"],
            # #           ),
            # #auto_tune(),
            # #     5
            # # ),
            # # turn_left(45),
            # #
            # # fully_disable_servos(),
            #
            # # DEBUG: no-op setup during motion-tune drive-pattern validation
            # # (was drive_forward(20) — kept out so the full ~1 m runway is free).
            # wait_for_seconds(0.1),
        ])
