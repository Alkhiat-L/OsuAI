import gymnasium as gym
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    CheckpointCallback,
    EvalCallback,
    ProgressBarCallback,
)

from osupy.model import ClickerAction, ClickerObservation, ClickerReward


if __name__ == "__main__":
    env = gym.make("osupy/OsuPyEnv-v0", model="click")
    env = ClickerObservation(env)
    env = ClickerAction(env)
    env = ClickerReward(env)  # type: ignore
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    model = PPO(policy="MlpPolicy", env=wrapped_env, verbose=1, n_steps=4096)

    callbacks = []

    eval_env = gym.wrappers.FlattenObservation(  # type: ignore
        ClickerReward(
            ClickerAction(  # type: ignore
                ClickerObservation(gym.make("osupy/OsuPyEnv-v0", model="click"))
            )
        )
    )  # type: ignore

    callbacks.append(
        CheckpointCallback(
            save_freq=10000,
            save_path="./clicker-logs",
            name_prefix="osupy-ppo-clicker",
        )
    )

    callbacks.append(
        EvalCallback(
            eval_env=eval_env,
            n_eval_episodes=5,
            eval_freq=10000,
            deterministic=True,
            verbose=1,
            best_model_save_path="./clicker-logs",
        )
    )

    callbacks.append(ProgressBarCallback())

    model.learn(total_timesteps=500000, callback=callbacks)
