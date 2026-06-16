from raccoon import *


class TestMission(Mission):
    def sequence(self) -> Sequential:
        # DEBUG: full motion-PID tune (distance, lateral, heading).
        # Autonomous (step_confirm=False); persists the best-found gains to
        # raccoon.project.yml. Each axis drives forward ~1 m, returns to start,
        # repeated across the Hooke-Jeeves trials (turn: rotate, then back).
        return seq([
            wait_for_button(),
            drive_forward(50),
            wait_for_button(),
            turn_right(90)
        ])
