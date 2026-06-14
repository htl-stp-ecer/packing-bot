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
            # loop_for(
            # slow_servo(Defs.pom_arm, 170, 20),
            # slow_servo(Defs.pom_arm, 0, 20),
            # calibrate(distance_cm=70,
            #           ema_alpha=0.3,
            #           # calibration_sets=["default", "upper"],
            #           ),
            auto_tune(),
            #     5
            # ),
            # turn_left(45),
            #
            # fully_disable_servos(),

            #drive_forward(20)
        ])
