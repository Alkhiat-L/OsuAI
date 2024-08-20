import os
import gymnasium as gym
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import (
    CheckpointCallback,
    EvalCallback,
    ProgressBarCallback,
)

from gymnasium.wrappers.record_episode_statistics import RecordEpisodeStatistics

from osupy.model import MoverAction, MoverObservation, MoverReward


if __name__ == "__main__":
    env = gym.make("osupy/OsuPyEnv-v0", model="move")
    env = MoverObservation(env)
    env = MoverAction(env)
    env = MoverReward(env)
    wrapped_env = RecordEpisodeStatistics(env)
    model = PPO(policy="MultiInputPolicy", env=wrapped_env, verbose=1, n_steps=2048)

    callbacks = []

    eval_env = RecordEpisodeStatistics(
        MoverReward(
            MoverAction(  # type: ignore
                MoverObservation(gym.make("osupy/OsuPyEnv-v0", model="move"))
            )
        )
    )  # type: ignore

    callbacks.append(
        CheckpointCallback(
            save_freq=20000,
            save_path="./mover-logs",
            name_prefix="osupy-ppo-mover",
        )
    )

    callbacks.append(
        EvalCallback(
            eval_env=eval_env,
            n_eval_episodes=5,
            eval_freq=50000,
            deterministic=True,
            verbose=1,
            best_model_save_path=os.path.join(os.getcwd(), "mover-logs"),
        )
    )

    callbacks.append(ProgressBarCallback())

    model.learn(total_timesteps=500000, callback=callbacks)
