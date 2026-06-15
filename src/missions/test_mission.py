from raccoon import *


class TestMission(Mission):
    def sequence(self) -> Sequential:
        # DEBUG: motion-PID drive-pattern validation.
        # Runs ONLY the motion phase, no button confirms (step_confirm=False),
        # no persistence (don't overwrite tuned gains while validating the
        # forward/back drive pattern). Start with the distance axis.
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
                motion_axes=["distance"],
                step_confirm=False,
                persist=False,
            ),
        ])
