from typing import Any
import gymnasium as gym
from gymnasium.spaces import Box

import numpy as np


class ClickerObservation(gym.ObservationWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.observation_space = gym.spaces.Dict(
            {
                "game_time": Box(low=0, high=np.inf, shape=(1,)),
                "next_note_time": Box(low=0, high=np.inf, shape=(1,)),
                "next_note_end_time": Box(low=0, high=np.inf, shape=(1,)),
            }
        )

    def observation(self, observation: dict[str, Any]) -> dict[str, Any]:
        try:
            return {
                "game_time": observation["game_time"],
                "next_note_time": observation["upcoming_notes"][0]["time"],
                "next_note_end_time": observation["upcoming_notes"][0]["end_time"],
            }
        except Exception:
            print("IndexError", observation["upcoming_notes"][0])
            return {
                "game_time": observation["game_time"],
                "next_note_time": 0,
                "next_note_end_time": 0,
            }
