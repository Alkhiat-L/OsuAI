import gymnasium as gym
from osupy.env import OsuPyEnv as OsuPyEnv

from stable_baselines3 import PPO

def env_creator(_):
    env = gym.make('osupy/OsuPyEnv-v0')
    env.reset()
    return env

if __name__ == '__main__':
    env = gym.make('osupy/OsuPyEnv-v0', render_mode='human')
    wrapped_env = gym.wrappers.FlattenObservation(env)  # type: ignore
    clipped = gym.wrappers.ClipAction(wrapped_env)  # type: ignore
    model = PPO(policy='MlpPolicy', env=clipped, verbose=1)
    i = 0
    try:
        model.load('osupy-ppo')
    except FileNotFoundError:
        pass
    while True:
        obs, info = clipped.reset()
        done = False
        while not done:
            action, _ = model.predict(obs)
            obs, rewards, done, _, info = clipped.step(action)
            i += 1
            if i % 100 == 0:
                print(f'Episode {i} reward: {rewards}')