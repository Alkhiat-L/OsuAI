import gymnasium as gym
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO

def env_creator(_):
    env = gym.make('osupy/OsuPyEnv-v0')
    env.reset()
    return env

if __name__ == '__main__':
    env = gym.make('osupy/OsuPyEnv-v0')
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    clipped = gym.wrappers.ClipAction(wrapped_env)  # type: ignore
    model = PPO(policy='MlpPolicy', env=clipped, verbose=1)
    i = 0
    try:
        model.load('osupy-ppo')
    except FileNotFoundError:
        pass
    while True:
        model.learn(total_timesteps=1000)
        i += 1
        print(i)
        model.save('osupy-ppo')
        print('Model Saved!')
        if i >= 10:
            model.save(f'osupy-ppo-backup={i}')