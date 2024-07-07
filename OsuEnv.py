import time

import cv2
import dxcam
import environment
import gym
import gym.spaces
import numpy as np
import psutil
import pyautogui as ag


class OsuEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        self.screen_width = 1366
        self.screen_height = 768

        self.camera: dxcam.DXCamera = dxcam.create(
            device_idx=0,
            region=(0, 0, self.screen_width, self.screen_height),
            output_color="GRAY",
        )
        self.camera.start()

        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(90 * 2, 160 * 2),
            dtype=np.uint8,
        )

        self.action_space = gym.spaces.Tuple(
            (
                gym.spaces.Box(low=0, high=self.screen_width, shape=(1,)),
                gym.spaces.Box(low=0, high=self.screen_height, shape=(1,)),
                gym.spaces.Discrete(2),
            )
        )

        self.current_score = 0

    def _get_obs(self) -> np.ndarray:
        shot = environment.screenshot(
            self.camera,
            (
                160 * 2,
                90 * 2,
            ),
        )
        obs_shape = self.observation_space.shape

        try:
            assert obs_shape
            assert shot.shape[0] == obs_shape[0]
        except AssertionError:
            print(f"Observation shape: {shot.shape}")
            print(f"Expected shape: {obs_shape}")
            raise AssertionError("Observation shape does not match expected shape.")

        return shot

    def _ensure_osu_is_running(self):
        osu_process = None
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == "osu!.exe":
                osu_process = process
                break

        if osu_process is None:
            raise RuntimeError(
                "Osu! is not running. Please start Osu! before running the environment."
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
        im = environment.screenshot(
            self.camera,
            (
                160 * 2,
                90 * 2,
            ),
            original=True,
        )
        reset = cv2.imread("imgs/reset.png", cv2.IMREAD_GRAYSCALE)

        if reset is None:
            raise FileNotFoundError("The 'reset.png' file could not be found or read.")

        if reset.shape[0] > im.shape[0] or reset.shape[1] > im.shape[1]:
            raise ValueError(
                "The template image (reset.png) is larger than the screenshot. Please use a smaller template."
            )

        res = cv2.matchTemplate(im, reset, cv2.TM_SQDIFF_NORMED)

        min_val, _, _, _ = cv2.minMaxLoc(res)
        threshold = 0.2
        has_lost = False
        if min_val < threshold:
            has_lost = True

        return {"has_lost": has_lost}

    def _get_action(self, action) -> dict:
        return {"x": action[0], "y": action[1], "click": action[2]}

    def _calculate_reward(self):
        return 0

    def step(self, action):
        action = self._get_action(action)
        x, y = action["x"], action["y"]
        ag.moveTo(x, y, 0.16, tween=lambda x: x**2)
        if action["click"] == 1:
            ag.mouseDown()
        elif action["click"] == 0:
            ag.mouseUp()

        observation = self._get_obs()
        info = self._get_info()

        terminated = info["has_lost"]
        if terminated:
            print("Game over!")
        reward = self._calculate_reward()

        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):  # type: ignore
        super().reset(seed=seed, options=options)

        print("Resetting...")
        self._ensure_osu_is_running()
        time.sleep(1)  # Give some time for the window to settle

        ag.keyDown("'")
        time.sleep(0.5)
        ag.keyUp("'")

        observation = self._get_obs()
        info = self._get_info()

        print(observation.shape)

        return observation, info

    def render(self):
        # The game is already rendering on the screen, so we don't need to do anything here
        pass

    def close(self):
        if self.camera:
            self.camera.stop()


if __name__ == "__main__":
    gym.register("OsuEnv-v0", OsuEnv)

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
