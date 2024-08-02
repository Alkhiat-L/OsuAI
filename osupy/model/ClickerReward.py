import gymnasium as gym

from osupy.Note import Note
from osupy.env import OsuPyEnv


class ClickerReward(gym.wrappers.RewardWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.env: OsuPyEnv = env  # type: ignore

    def reward(self, reward: float) -> float:
        next_note: Note = self.env._get_info()["upcoming_notes"][0]
        if next_note.time - self.env.osu.game_time > 1000:
            return -100
        return reward
