from typing import Any, Optional, SupportsFloat
import gymnasium as gym

from osupy.Note import Note
from osupy.env import OsuPyEnv


class ClickerReward(gym.RewardWrapper[Any, Any]):
    def __init__(self, env: OsuPyEnv):
        super().__init__(env)
        self.env: OsuPyEnv = env

    def reward(self, reward: SupportsFloat) -> float:
        try:
            next_note: Note = self.env.get_info()["upcoming_notes"][0]
            curve: Optional[Note] = self.env.get_info()["curve"]
            hold: bool = self.env.get_info()["click"]
            time_diff = abs(next_note.time - self.env.osu.game_time)
            if curve:
                if hold:
                    return 1.0
                return -1.0
            if next_note.time - self.env.osu.game_time < -200:
                return -1.0
            if time_diff > 200:
                if hold:
                    return -1.0
                else:
                    return 0
            if not hold:
                return -1.0
            if time_diff < 50:
                return 10.0
            if time_diff < 100:
                return 5.0
            if time_diff < 200:
                return 1.5
            return 0

        except Exception:
            print("IndexError", self.env.get_info()["upcoming_notes"])
            return 0
