import gym
from OsuEnv import OsuEnv

gym.register("OsuEnv-v0", OsuEnv)

if __name__ == "__main__":
    print("Starting...")
    env = gym.make("OsuEnv-v0")
    print(env.observation_space.shape)
    env.reset()
    for _ in range(300):
        observation, reward, terminated, truncated, info = env.step(
            env.action_space.sample()
        )

        if terminated:
            print("Terminated")
            env.reset()
    env.close()
