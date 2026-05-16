from raccoon import *


class TestMission(Mission):
    def sequence(self) -> Sequential:
        return seq([
            # Phase 5 — Static Friction (motors spin low PWM until moving)
            # Safe ohne Fahrfläche: each motor braked while other is tested
            auto_tune_static_friction(persist=False),

            # Phase 6 — Vel LPF (only runs if BEMF is available)
            auto_tune_vel_lpf(persist=False),
        ])
