from raccoon import *


class TestMission(Mission):
    def sequence(self) -> Sequential:
        # DEBUG: full motion-PID tune (distance, lateral, heading).
        # Autonomous (step_confirm=False); persists the best-found gains to
        # raccoon.project.yml. Each axis drives forward ~1 m, returns to start,
        # repeated across the Hooke-Jeeves trials (turn: rotate, then back).
        return seq([
            # auto_tune(
            #     tune_bemf_velocity=False,
            #     tune_vel_lpf=False,
            #     tune_static_friction=False,
            #     tune_firmware_pid=False,
            #     tune_encoder_cal=False,
            #     tune_characterize=False,
            #     tune_velocity=False,
            #     tune_motion=True,
            #     tune_tolerances=False,
            #     motion_axes=["distance", "lateral", "heading"],
            #     step_confirm=False,
            #     persist=True,
            # ),
        ])
