import gymnasium as gym
import ray
from OsuEnv import OsuEnv as OsuEnv
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig


osuEnv = OsuEnv()

ray.init()

tune.register_env("OsuAi/OsuEnv-v0", lambda _: OsuEnv())

if __name__ == "__main__":
    print("Starting...")
    config = (  # 1. Configure the algorithm,
        PPOConfig()
        .environment("OsuAi/OsuEnv-v0")
        .env_runners(num_env_runners=1)
        .framework("torch")
        .training(model={"fcnet_hiddens": [64, 64]})
        .evaluation(evaluation_num_env_runners=1)
    )

    config.observation_space = osuEnv.observation_space  # type: ignore
    config.action_space = osuEnv.action_space  # type: ignore

    algo = config.build()

    for _ in range(5):
        print(algo.train())
    algo.evaluate()
