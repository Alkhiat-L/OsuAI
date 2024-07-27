from typing import Any, Optional, override, SupportsFloat

import gymnasium as gym

from osupy.OsuPy import OsuPy


class OsuPyEnv(gym.Env):
    def __init__(self):
        self.osu = OsuPy()
        pass

    @override
    def step(self, action) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        observation, reward, done, info = self.osu.step(action)
        return observation, reward, done, False, info

    @override
    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> tuple[Any, dict[str, Any]]:
        super().reset(seed=seed)
        self.osu.load_beatmap("beatmap.osu")
        self.osu.reset()
        self.osu.start_game()

        return self.osu.get_observation(), {}

    def render(self):
        if self.render_mode == "human":
            self.osu.render()

    def close(self):
        self.osu.stop_game()


gym.register("osupy/OsuPyEnv-v0", "osupy:OsuPyEnv")

if __name__ == "__main__":
    print("Starting...")
    env = gym.make("osupy/OsuPyEnv-v0")
    env.reset()
    for _ in range(300):
        observation, reward, terminated, truncated, info = env.step(
            env.action_space.sample()
        )

        if terminated:
            print("Terminated")
            env.reset()
    env.close()
