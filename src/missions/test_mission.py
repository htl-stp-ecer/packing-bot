from raccoon import *


class TestMission(Mission):
    def sequence(self) -> Sequential:
        # DEBUG: full motion-PID tune (distance, lateral, heading).
        # Autonomous (step_confirm=False); persists the best-found gains to
        # raccoon.project.yml. Each axis drives forward ~1 m, returns to start,
        # repeated across the Hooke-Jeeves trials (turn: rotate, then back).
        return seq([
            # auto_tune(
            #     tune_bemf_velocity=True,
            #     tune_vel_lpf=True,
            #     tune_static_friction=True,
            #     tune_firmware_pid=True,
            #     tune_encoder_cal=True,
            #     tune_characterize=True,
            #     tune_velocity=True,
            #     tune_motion=False,
            #     tune_tolerances=False,
            #     motion_axes=["distance", "lateral", "heading"],
            #     step_confirm=True,
            #     persist=True,
            # ),
            drive_forward(30),
            wait_for_button(),
            turn_right(90)
        ])
