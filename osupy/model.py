import gymnasium as gym
from matplotlib import pyplot as plt
import numpy as np
from sympy import true
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    EvalCallback,
    CheckpointCallback,
    ProgressBarCallback,
)


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

    callbacks = []

    callbacks.append(
        CheckpointCallback(
            save_freq=20000,
            save_path="./logs/",
            name_prefix="osupy-ppo",
        )
    )

    callbacks.append(ProgressBarCallback())

    try:
        model.load("osupy-ppo")
    except FileNotFoundError:
        pass
    while True:
        try:
            model.learn(total_timesteps=400000, callback=callbacks)
        except KeyboardInterrupt:
            break
