from typing import Any
import gymnasium as gym
from gymnasium.spaces import Box, Discrete

import numpy as np


class ClickerObservation(gym.wrappers.ObservationWrapper):  # type: ignore
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
        return {
            "game_time": observation["game_time"],
            "next_note_time": observation["upcoming_note"][0]["time"],
            "next_note_end_time": observation["upcoming_note"][0]["end_time"],
        }
