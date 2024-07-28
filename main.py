"""
Versão antiga do projeto, que foi feita para funcionar gravando a tela do jogo original,
essa versão não está mais sendo atualizada. A versão atualizada do projeto está na pasta
'osupy'.
"""

import gymnasium as gym
from OsuEnv import OsuEnv as OsuEnv

from stable_baselines3 import PPO


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
        i += 1
        print(i)

        model.save("ppo")

        print("Model saved!")
        if i >= 10:
            model.save(f"ppo-backup-{i}")
