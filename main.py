import gymnasium as gym
import ray
from OsuEnv import action_space, observation_space, OsuEnv as OsuEnv

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


def env_creator(_):
    env = gym.make("OsuEnv:OsuAi/OsuEnv-v0")
    env.reset()
    return env


if __name__ == "__main__":
    env = gym.make("OsuEnv:OsuAi/OsuEnv-v0")

    model = PPO("MlpPolicy", env, verbose=1)
    i = 0
    try:
        model.load("ppo")
    except FileNotFoundError:
        pass
    while True:
        model.learn(total_timesteps=1000)
        i+=1
        print(i)

        model.save("ppo")

        print('Model saved!')
        if i >= 10:
            model.save(f"ppo-backup-{i}")




