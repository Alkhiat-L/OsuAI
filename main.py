import gymnasium as gym
import ray
from OsuEnv import OsuEnv as OsuEnv
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms import ppo

def env_creator(_):
    env = gym.make("OsuEnv:OsuAi/OsuEnv-v0")
    return env

tune.register_env("OsuAi/OsuEnv-v0", env_creator=env_creator)

if __name__ == "__main__":
    algo = (
        PPOConfig().training(gamma=0.9, lr=0.01)
        .env_runners(num_env_runners=1)
        .resources(num_gpus=0)
        .environment(env="OsuAi/OsuEnv-v0")
        .build()
    )
    algo.observation_space = env_creator('').observation_space  # type: ignore
    algo.action_space = env_creator('').action_space  # type: ignore

    for i in range(10):
        result = algo.train()
        print((result))