"""
Versão antiga do projeto, que foi feita para funcionar gravando a tela do jogo original,
essa versão não está mais sendo atualizada. A versão atualizada do projeto está na pasta
'osupy'.
"""

import json
import time
from urllib import request

import cv2
import gymnasium as gym
import numpy as np
import psutil
import pyautogui as ag
import screeninfo
from environment import SCREEN_HEIGHT, SCREEN_WIDTH
from mss import mss
from tokens import *

DEBUG = False

observation_space = gym.spaces.flatten_space(
    gym.spaces.Box(
        low=0,
        high=255,
        shape=(
            160 * 2,
            90 * 2,
        ),
        dtype=np.uint8,
    )
)

# Calculate the number of bits needed for x and y coordinates

x_bits = int(np.ceil(np.log2(SCREEN_WIDTH)))
y_bits = int(np.ceil(np.log2(SCREEN_HEIGHT)))
total_bits = x_bits + y_bits + 1  # +1 for mouse click

action_space = gym.spaces.Box(low=0, high=1, shape=(total_bits,), dtype=np.float32)


class OsuEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        print("Starting camera...")
        self.sct = mss()

        self.observation_space = observation_space
        self.action_space = action_space

        ag.PAUSE = 0

        self.current_hp = 200
        self.current_acc = 100
        self.current_combo = 0
        self.current_miss = 0

        self.last_step_time = time.time()

    def _get_obs(self) -> np.ndarray:
        sct_img = np.array(self.sct.grab(self.sct.monitors[1]))

        im: np.ndarray = cv2.resize(
            cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY),
            dsize=(
                160 * 2,
                90 * 2,
            ),
        ).flatten()

        obs_shape = self.observation_space.shape

        try:
            assert obs_shape
            assert im.shape[0] == obs_shape[0]
        except AssertionError:
            print(f"Observation shape: {im.shape}")
            print(f"Expected shape: {obs_shape}")
            raise AssertionError("Observation shape does not match expected shape.")
        return im

    def _ensure_osu_is_running(self):
        osu_process = None
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "osu!.exe":
                osu_process = process
                break
        stream_companion_process = None
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "osu!StreamCompanion.exe":
                stream_companion_process = process
                break
        if osu_process is None:
            raise RuntimeError(
                "Osu! is not running. Please start Osu! before running the environment."
            )
        if stream_companion_process is None:
            raise RuntimeError(
                "Stream Companion is not running. Please start Stream Companion before running the environment."
            )
        osu_img = "imgs/osu.png"
        try:
            point = ag.locateCenterOnScreen(osu_img, minSearchTime=0.1, confidence=0.7)

            if point:
                ag.moveTo(point[0], point[1], 0.1)
                ag.click()
                time.sleep(0.5)
        except Exception:
            print("Already in game")

    def _verify_game_state(self):
        # Implement logic to check if Osu is in the correct state
        # This could involve analyzing the screenshot to detect specific UI elements

        pass

    def _get_info(self) -> dict:
        data: dict = json.loads(request.urlopen("http://localhost:20727/json").read())

        has_lost = data["playerHp"] <= 0
        hp = data["playerHp"]
        acc = data["acc"]
        combo = data["combo"]
        miss = data["miss"]

        if DEBUG:
            print(f"HP: {hp}")
        return {
            "has_lost": has_lost,
            "hp": hp,
            "acc": acc,
            "combo": combo,
            "miss": miss,
        }

    def _binary_to_decimal(self, binary_array):
        return int("".join(map(str, binary_array)), 2)

    def _get_action(self, action) -> dict:
        # Convert float action to binary
        binary_action = (action > 0.5).astype(int)

        # Convert binary action to x, y coordinates and click
        x_coord = self._binary_to_decimal(binary_action[:x_bits])
        y_coord = self._binary_to_decimal(binary_action[x_bits : x_bits + y_bits])
        mouse_click = binary_action[-1]

        # Ensure coordinates are within screen bounds
        x_coord = min(x_coord, self.screen_width - 1)
        y_coord = min(y_coord, self.screen_height - 1)

        return {"x": x_coord, "y": y_coord, "click": bool(mouse_click)}

    def _calculate_reward(self, info):
        reward = 0
        reward += (info["hp"] - self.current_hp) * 0.5  # 0 - 200
        reward += (info["acc"] - self.current_acc) * 2  # 0 - 100
        reward += (info["combo"] - self.current_combo) * 10  # 0 - ~200
        reward -= (info["miss"] - self.current_miss) * 5  # 0 - ~100

        if DEBUG:
            print(f"Reward: {reward}")
            print(f"HP reward: {(info['hp'] - self.current_hp) * 0.5}")
            print(f"Acc reward: {(info['acc'] - self.current_acc) * 0.5}")
            print(f"Combo reward: {(info['combo'] - self.current_combo) * 0.5}")
            print(f"Miss reward: {(info['miss'] - self.current_miss) * 0.5}")
        self.current_hp = info["hp"]
        self.current_acc = info["acc"]
        self.current_combo = info["combo"]
        self.current_miss = info["miss"]

        return reward

    def step(self, action):
        action = self._get_action(action)
        x, y = action["x"], action["y"]
        if x >= self.screen_width - 1 and y >= self.screen_height - 1:
            x -= 10
            y -= 10
        if x <= 1 and y <= 1:
            x += 10
            y += 10
        if x >= self.screen_width - 1 and y <= 1:
            x -= 10
            y += 10
        if x <= 1 and y >= self.screen_height - 1:
            x += 10
            y -= 10
        ag.moveTo(x, y, 0, tween=lambda x: x**2)
        if action["click"]:
            ag.mouseDown()
        else:
            ag.mouseUp()
        time_now = time.time()
        if self.last_step_time + ((1 / 60) / 6) > time_now:
            time.sleep(self.last_step_time + ((1 / 60) / 6) - time_now)
        self.last_step_time = time.time()

        observation = self._get_obs()
        info = self._get_info()

        terminated = info["has_lost"]
        if terminated:
            print("Game over!")
        reward = self._calculate_reward(info)

        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):  # type: ignore
        super().reset(seed=seed, options=options)

        print("Resetting...")
        self._ensure_osu_is_running()
        time.sleep(1)  # Give some time for the window to settle
        # if get_status() == 'Playing':
        #     if get_hp() == 0:
        #         print("Playing")
        #         while get_status() == 'Playing':
        #             print("Esc")
        #             ag.keyDown('Esc')
        #             time.sleep(0.1)
        #             ag.keyUp('Esc')
        #             time.sleep(1)
        #     else:
        ag.keyDown('"')
        time.sleep(0.5)
        ag.keyUp('"')
        # if (get_status()) == 'Listening':
        #     print('Listening')
        #     ag.keyDown('F2')
        #     time.sleep(0.1)
        #     ag.keyUp('F2')
        #     time.sleep(0.5)
        #     ag.keyDown('Enter')
        #     time.sleep(0.1)
        #     ag.keyUp('Enter')
        #     time.sleep(1)

        observation = self._get_obs()
        info = self._get_info()

        self.last_step_time = time.time()
        self.current_hp = 200
        self.current_acc = 100
        self.current_combo = 0
        self.current_miss = 0

        return observation, info

    def render(self):
        # The game is already rendering on the screen, so we don't need to do anything here

        pass

    def close(self):
        if self.sct:
            self.sct.close()


gym.register("OsuAi/OsuEnv-v0", "OsuEnv:OsuEnv")

if __name__ == "__main__":
    print("Starting...")
    env = gym.make("OsuAi/OsuEnv-v0")
    env.reset()
    for _ in range(300):
        observation, reward, terminated, truncated, info = env.step(
            env.action_space.sample()
        )

        if terminated:
            print("Terminated")
            env.reset()
    env.close()
