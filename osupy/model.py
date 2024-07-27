import gymnasium as gym
from matplotlib import pyplot as plt
import numpy as np
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO


def env_creator(_):
    env = gym.make("osupy/OsuPyEnv-v0")
    env.reset()
    return env


if __name__ == "__main__":
    env = gym.make("osupy/OsuPyEnv-v0")
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    model = PPO(policy="MlpPolicy", env=wrapped_env, verbose=1)
    i = 0
    j = 1
    try:
        model.load("osupy-ppo")
    except FileNotFoundError:
        pass
    while True:
        try:
            model.learn(total_timesteps=50000)
            i += 1
            print(i)
            model.save("osupy-ppo")
            print("Model Saved!")
            if i > j * 10:
                model.save(f"osupy-ppo-backup={j}")
                j += 1
        except KeyboardInterrupt:
            break
