from typing import TYPE_CHECKING
import gymnasium
from pygame import Vector2

if TYPE_CHECKING:
    from osupy.env import OsuPyEnv


class MoverReward(gymnasium.RewardWrapper):
    def __init__(self, env):
        self.env: "OsuPyEnv" = env  # type: ignore
        super().__init__(env)

    def reward(self, reward):
        mover_reward = 0
        if len(self.env.osu.upcoming_notes) == 0:
            return 2
        next_note = Vector2(
            self.env.osu.upcoming_notes[0].get_virtual_x() / self.env.osu.width,
            self.env.osu.upcoming_notes[0].get_virtual_y() / self.env.osu.height,
        )
        mouse = Vector2(
            self.env.osu.mouse.x / self.env.osu.width,
            self.env.osu.mouse.y / self.env.osu.height,
        )
        distance = next_note.distance_to(mouse)

        if distance < 0.1:
            mover_reward = 10
        elif distance < 0.2:
            mover_reward = 5
        elif distance < 0.4:
            mover_reward = 1
        elif distance < 0.5:
            mover_reward = 0
        elif distance < 0.7:
            mover_reward = -1
        else:
            mover_reward = -5

        return mover_reward
