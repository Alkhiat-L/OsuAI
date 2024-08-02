import gymnasium as gym

from osupy.Note import Note
from osupy.env import OsuPyEnv


class ClickerReward(gym.wrappers.RewardWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.env: OsuPyEnv = env  # type: ignore

    def reward(self, reward: float) -> float:
        next_note: Note = self.env._get_info()["upcoming_notes"][0]
        hold = self.env._get_info()["click"][0]
        if hold:
            if next_note.end_time > 0:
                if (
                    self.env.osu.game_time >= next_note.time - 200
                    and self.env.osu.game_time < next_note.end_time
                ):
                    return 1
            if abs(next_note.time - self.env.osu.game_time) < 50:
                return 10
            if abs(next_note.time - self.env.osu.game_time) < 100:
                return 5
            if abs(next_note.time - self.env.osu.game_time) < 200:
                return 1
            return -1

        if next_note.time - self.env.osu.game_time > 200:
            return -1

        return 0
