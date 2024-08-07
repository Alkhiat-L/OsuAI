from typing import Any
import gymnasium as gym
from gymnasium.spaces import Discrete


class ClickerObservation(gym.ObservationWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.observation_space = gym.spaces.Dict(
            {
                "time_to_next_note": Discrete(4),
                "curve_remaining": Discrete(2),
            }
        )

    def observation(self, observation: dict[str, Any]) -> dict[str, Any]:
        try:
            # 0 = <50ms, 1 = <100ms, 2 = <200ms, 3 = >200ms
            time_to_next_note_ms = (
                observation["upcoming_notes"][0]["time"] - observation["game_time"]
            )
            time_to_next_note = 0
            if time_to_next_note_ms > 200:
                time_to_next_note = 3
            elif time_to_next_note_ms > 100:
                time_to_next_note = 2
            elif time_to_next_note_ms > 50:
                time_to_next_note = 1
            else:
                time_to_next_note = 0

            # 0 = no curve, 1 = curve
            curve_remaining = 0
            if (
                observation["upcoming_notes"][0]["next_note_end_time"]
                - observation["game_time"]
            ) > 0:
                curve_remaining = 1

            return {
                "time_to_next_note": time_to_next_note,
                "curve_remaining": curve_remaining,
            }
        except Exception:
            return {
                "time_to_next_note": 0,
                "curve_remaining": 0,
            }
