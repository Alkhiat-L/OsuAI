import gymnasium as gym
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    EvalCallback,
    CheckpointCallback,
    ProgressBarCallback,
)

from osupy.model import ClickerAction, ClickerObservation, ClickerReward


def env_creator(_) -> OsuPyEnv:
    env: OsuPyEnv = gym.make("osupy/OsuPyEnv-v0")  # type: ignore
    env.reset()
    return env


if __name__ == "__main__":
    env = gym.make("osupy/OsuPyEnv-v0")
    env = ClickerObservation(env)
    env = ClickerAction(env)
    env = ClickerReward(env)
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    model = PPO(policy="MlpPolicy", env=wrapped_env, verbose=1)

    callbacks = []

    eval_env = gym.wrappers.FlattenObservation(gym.make("osupy/OsuPyEnv-v0"))  # type: ignore

    callbacks.append(
        CheckpointCallback(
            save_freq=10000,
            save_path="./clicker-logs/",
            name_prefix="osupy-ppo-clicker",
        )
    )

    callbacks.append(
        EvalCallback(
            eval_env,
            best_model_save_path="./clicker-logs/",
            log_path="./clicker-logs/",
            eval_freq=5000,
            n_eval_episodes=20,
            deterministic=True,
        )
    )

    callbacks.append(ProgressBarCallback())

    model.learn(total_timesteps=100000, callback=callbacks)