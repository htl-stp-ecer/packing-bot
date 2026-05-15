from raccoon import *

from src.hardware.defs import Defs
from src.steps.et_scan_align import EtScanAlign


class M000SetupMission(SetupMission):
    def sequence(self) -> Sequential:
        setup_time = 120
        return seq([
            # pause_setup_timer(),
            # fully_disable_servos(),
            # wait_for_button("move servos into starting position"),
            # start_setup_timer(),  # countdown begins here, full duration
            # parallel(
            #     Defs.pom_grab.start(),
            #     Defs.shild.down(),
            #     Defs.shild_graber.closed(),
            # ),
            #
            # parallel(
            #     Defs.pom_arm.start(100),
            # ),
            #
            # Defs.shild.up(),
            #
            #
            # #auto_tune(
            # #    vel_axes=["vy"],
            # #    tune_motion=False,
            # #    characterize_axes=["lateral"]
            # #),
            loop_for(
                calibrate(distance_cm=100,
                          # calibration_sets=["default", "upper"],
                          ),
                5
            ),
            #
            # fully_disable_servos(),
        ])
