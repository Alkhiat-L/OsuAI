from typing import Any, Optional, override, SupportsFloat

import gymnasium as gym
import numpy as np

from osupy.OsuPy import ActionSpace, OsuPy, States


class OsuPyEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode=None):
        self.osu = OsuPy()
        self.observation_space = gym.spaces.Dict(
            {
                "game_time": gym.spaces.Box(low=0, high=240000, shape=(1,)),
                "x": gym.spaces.Box(low=0, high=800, shape=(1,)),
                "y": gym.spaces.Box(low=0, high=600, shape=(1,)),
                "upcoming_notes": gym.spaces.Tuple(
                    [
                        gym.spaces.Dict(
                            {
                                "x": gym.spaces.Box(low=0, high=800, shape=(1,)),
                                "y": gym.spaces.Box(low=0, high=600, shape=(1,)),
                                "time": gym.spaces.Box(low=0, high=240000, shape=(1,)),
                                "type": gym.spaces.Discrete(4),
                            }
                        )
                        for _ in range(5)
                    ]
                ),
                "curve": gym.spaces.Box(low=0, high=2, shape=(8,), dtype=np.float32),
            }
        )
        self._action_space = gym.spaces.Dict(
            {
                "x": gym.spaces.Box(low=0, high=2, shape=(1,), dtype=np.float32),
                "y": gym.spaces.Box(low=0, high=2, shape=(1,), dtype=np.float32),
                "click": gym.spaces.Box(low=0, high=2, shape=(1,), dtype=np.float32),
            }
        )

        self.action_space = gym.spaces.flatten_space(self._action_space)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        if self.render_mode == "human":
            self.osu.state = States.HUMAN

        pass

    def _parse_action(self, action: dict[str, Any]) -> ActionSpace:
        action = gym.spaces.unflatten(self._action_space, action)  # type: ignore

        return ActionSpace(action["x"] * 400, action["y"] * 300, action["click"] >= 1)

    @override
    def step(self, action) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        observation, reward, done, info = self.osu.step(self._parse_action(action))  # type: ignore
        self.render()
        print(observation)
        return observation, reward, done, False, info

    @override
    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> tuple[Any, dict[str, Any]]:
        super().reset(seed=seed)
        self.osu.load_beatmap("beatmap.osu")
        self.osu.reset()
        if self.render_mode == "human":
            self.osu.state = States.HUMAN
        assert self.observation_space.contains(self.osu.get_observation())

        return self.osu.get_observation(), {}

    def render(self):
        if self.render_mode == "human":
            self.osu.render()

    def close(self):
        self.osu.stop_game()


gym.register("osupy/OsuPyEnv-v0", "osupy:OsuPyEnv")

if __name__ == "__main__":
    print("Starting...")
    env = gym.make("osupy/OsuPyEnv-v0", render_mode="human")
    obs = env.reset()
    for _ in range(300):
        observation, reward, terminated, truncated, info = env.step(
            env.action_space.sample()
        )
        if terminated:
            print("Terminated")
            env.reset()
    env.close()
