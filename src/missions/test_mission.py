from raccoon import *

from src.steps.velocity_plot import PlotDriveVelocity, PlotTurnVelocity


class TestMission(Mission):
    def sequence(self) -> Sequential:
        # Educational PID demo: each move records commanded vs. measured
        # velocity and saves a matplotlib plot to /tmp/velocity_plots.
        # PlotDriveVelocity / PlotTurnVelocity are instrumented drop-in
        # replacements for drive_forward / turn_right.
        return seq([
            wait_for_button(),
            PlotDriveVelocity(50),
            wait_for_button(),
            PlotTurnVelocity(90, direction="right")
        ])
