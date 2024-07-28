import sys
from typing import Any
import gymnasium as gym
import pygame
from osupy.env import ActType, ObsType, OsuPyEnv as OsuPyEnv

from stable_baselines3 import A2C, PPO


def env_creator(_) -> gym.Env[Any, Any]:
    env: gym.Env[Any, Any] = gym.make("osupy/OsuPyEnv-v0")
    env.reset()
    return env


if __name__ == "__main__":
    env: gym.Env[ObsType, ActType] = gym.make("osupy/OsuPyEnv-v0", render_mode="human")
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    model = PPO(policy="MlpPolicy", env=wrapped_env, verbose=1)
    i = 0
    try:
        model.load("logs/best_model.zip")
    except FileNotFoundError:
        pass
    while True:
        obs: Any
        info: dict[str, Any]
        obs, info = wrapped_env.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            action, _ = model.predict(obs)
            obs, rewards, done, _, info = wrapped_env.step(action)
            i += 1
            if i % 100 == 0:
                print(f"Episode {i} reward: {rewards}")
