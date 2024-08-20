import gymnasium
import numpy as np


class MoverAction(gymnasium.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.env = env

        self.action_space = gymnasium.spaces.Box(
            low=-1, high=1, shape=(2,), dtype=np.float32
        )

    def action(self, action):
        return {"click": 0, "x": action[0], "y": action[1]}
