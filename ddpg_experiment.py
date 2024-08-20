import gymnasium as gym
import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.common.callbacks import (
    ProgressBarCallback,
)
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.noise import NormalActionNoise
from gymnasium.wrappers import time_limit


# Define the environment
class MouseMovementEnv(gym.Env):
    def __init__(self):
        super(MouseMovementEnv, self).__init__()
        self.observation_space = gym.spaces.Box(
            low=0, high=1000, shape=(4,), dtype=np.float32
        )
        self.action_space = gym.spaces.Box(
            low=-1000, high=1000, shape=(2,), dtype=np.float32
        )
        self.current_pos = np.array([500, 500])
        self.target_pos = np.random.rand(2) * 1000

    def reset(self, seed=None, options=None):  # type: ignore
        self.current_pos = np.random.rand(2) * 1000
        self.target_pos = np.random.rand(2) * 1000
        return np.concatenate((self.current_pos, self.target_pos)), {}

    def step(self, action):  # type: ignore
        delta_x, delta_y = action
        previous_distance = np.linalg.norm(self.target_pos - self.current_pos)
        self.current_pos += np.array([delta_x, delta_y])
        new_distance = np.linalg.norm(self.target_pos - self.current_pos)
        reward = previous_distance - new_distance  # Reward for reducing distance
        if new_distance > previous_distance:
            reward -= 10  # Additional penalty for moving further away
        done = new_distance < 10
        return (
            np.concatenate((self.current_pos, self.target_pos)),
            reward,
            done,
            False,
            {},
        )

    def render(self, mode="human"):
        pass


# Create and wrap the environment
env = DummyVecEnv(
    [lambda: time_limit.TimeLimit(MouseMovementEnv(), max_episode_steps=100)]
)

eval_env = DummyVecEnv([lambda: MouseMovementEnv()])

# Add noise for exploration
if not (action_shape := env.action_space.shape):
    raise ValueError("env.action_space.shape is None.")
n_actions = action_shape[0]
action_noise = NormalActionNoise(
    mean=np.zeros(n_actions), sigma=0.05 * np.ones(n_actions)
)


# Instantiate the DDPG agent
model = DDPG(
    "MlpPolicy",
    env,
    action_noise=action_noise,
    verbose=1,
    train_freq=1000,
    gradient_steps=20,
)


callbacks = []

callbacks.append(ProgressBarCallback())

# Train the model
model.learn(total_timesteps=100000, callback=callbacks)

# Test the trained model
obs = env.reset()
for i in range(100):
    action, _states = model.predict(obs)  # type: ignore
    obs, rewards, done, info = env.step(action)
    if done:
        break
    print(f"Step {i+1}: Action taken: {action}, Reward: {rewards}")

# Save the model
model.save("ddpg_mouse_movement")
