from typing import Any
import gymnasium as gym
from gymnasium.spaces import Discrete


class ClickerAction(gym.ActionWrapper):  # type: ignore
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = Discrete(2)

    def action(self, action: int) -> dict[str, Any]:
        return {"click": action, "x": 0, "y": 0}
