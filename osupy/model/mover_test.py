import sys
import time
import gymnasium as gym

from gymnasium.wrappers.record_video import RecordVideo
import pygame
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import TD3
from stable_baselines3.common.env_util import make_vec_env

from osupy.model import MoverAction, MoverObservation, MoverReward

if __name__ == "__main__":

    def make_env():
        env = OsuPyEnv(render_mode="rgb_array", model="move")
        env = MoverObservation(env)
        env = MoverAction(env)
        env = MoverReward(env)
        env = RecordVideo(env, "mover-logs/video.mp4")
        return env

    env = make_vec_env(make_env, n_envs=1)

    model = TD3(policy="MultiInputPolicy", env=env, verbose=1, device="cuda").load(
        "mover-logs/best_model.zip", env=env
    )

    model.learn(total_timesteps=10000, reset_num_timesteps=False)

    obs = env.reset()
    done = False
    i = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        action, _ = model.predict(obs)  # type: ignore
        start_time = time.time()
        rewards = 0
        obs, reward, done, _ = env.step(action)
        while (time.time() - start_time) < (1000 / 10000):
            env.render()
        i += 1
        print(f"Step {i} reward: {rewards}")

        if done:
            print("Episode finished after {} timesteps".format(i))
            break
