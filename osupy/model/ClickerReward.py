from typing import SupportsFloat
import gymnasium as gym

from osupy.Note import Note
from osupy.env import OsuPyEnv


class ClickerReward(gym.RewardWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.env: OsuPyEnv = env  # type: ignore

    def reward(self, reward: SupportsFloat) -> float:
        try:
            next_note: Note = self.env.get_info()["upcoming_notes"][0]
            curve = self.env.get_info()["curve"]
            hold = self.env.get_info()["click"]
            if hold:
                if curve:
                    if (
                        self.env.osu.game_time >= curve.time - 200
                        and self.env.osu.game_time < curve.end_time
                    ):
                        return 1
                if abs(next_note.time - self.env.osu.game_time) < 50:
                    return 10
                if abs(next_note.time - self.env.osu.game_time) < 100:
                    return 5
                if abs(next_note.time - self.env.osu.game_time) < 200:
                    return 1
                return -0.1

            if next_note.time - self.env.osu.game_time > 200:
                return -0.1

            return 0
        except Exception:
            print("IndexError", self.env.get_info()["upcoming_notes"])
            return 0
