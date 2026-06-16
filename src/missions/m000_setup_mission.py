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

        ])
