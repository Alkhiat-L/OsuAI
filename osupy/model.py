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

    env_eval = gym.wrappers.FlattenObservation(  # type: ignore
        gym.make("osupy/OsuPyEnv-v0")
    )

    env_show = gym.wrappers.FlattenObservation(  # type: ignore
        gym.make("osupy/OsuPyEnv-v0", render_mode="human")
    )

    callbacks.append(
        EvalCallback(
            env_eval,
            best_model_save_path="./logs/",
            log_path="./logs/",
            eval_freq=40000,
            n_eval_episodes=30,  # Run 30 games
            deterministic=False,
            render=False,
        )
    )

    callbacks.append(
        EvalCallback(
            env_show,
            best_model_save_path="./logs/",
            log_path="./logs/",
            eval_freq=40000,
            n_eval_episodes=2,  # Run 30 games
            deterministic=False,
            render=True,
        )
    )

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
