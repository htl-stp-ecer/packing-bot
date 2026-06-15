from src.hardware.robot import Robot
import raccoon.foundation as logging
from raccoon.robot.api import GenericRobot

#logging.set_file_level("fused_odometry.cpp", logging.Level.trace),
#logging.set_file_level("single_line_follow.py", logging.Level.debug),
#logging.set_file_level("libstp.step.base", logging.Level.debug),


# DEBUG (motion-tune drive-pattern validation): run fully autonomously.
# Skip the light/button pre-start gate so no human interaction is needed, and
# raise the shutdown timer so the multi-trial motion tune can run to completion
# (the C++ tuner blocks in an executor thread and cannot be cancelled mid-run).
async def _skip_pre_start_gate(self) -> None:
    self.info("DEBUG: skipping pre-start gate (autonomous motion-tune run)")


GenericRobot._pre_start_gate = _skip_pre_start_gate


def main():
    robot = Robot()
    robot.shutdown_in = 900
    robot.start()


if __name__ == "__main__":
    main()
