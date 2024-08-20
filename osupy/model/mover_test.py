import sys
import time
import gymnasium as gym
import pygame
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO

from osupy.model import MoverAction, MoverObservation, MoverReward

if __name__ == "__main__":
    env = gym.make("osupy/OsuPyEnv-v0", render_mode="human", model="move")
    env = MoverObservation(env)
    env = MoverAction(env)
    env = MoverReward(env)  # type: ignore
    print(env.observation_space)
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    print(wrapped_env.observation_space)
    model = PPO(policy="MlpPolicy", env=wrapped_env, verbose=1, n_steps=4096)  # type: ignore

    model = model.load("mover-logs/best_model.zip")

    obs, info = wrapped_env.reset()
    done = False
    i = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        action, _ = model.predict(obs)
        start_time = time.time()
        rewards = 0
        obs, rewards, done, _, info = wrapped_env.step(action)
        while (time.time() - start_time) < (1000 / 10000):
            wrapped_env.render()
        i += 1
        print(f"Step {i} reward: {rewards}")

        if done:
            print("Episode finished after {} timesteps".format(i))
            break
