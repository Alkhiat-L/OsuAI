"""
Versão antiga do projeto, que foi feita para funcionar gravando a tela do jogo original,
essa versão não está mais sendo atualizada. A versão atualizada do projeto está na pasta
'osupy'.
"""

import time

import cv2
import dxcam
import keyboard
import mss
import mss.base
import numpy as np
import torch
import torchvision
from PIL import Image
from screeninfo import get_monitors


SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height


def restart():
    keyboard.press("r")
    time.sleep(1)
    keyboard.release("r")


def screenshot(
    camera: mss.base.MSSBase, size: tuple[int, int] = (256, 256), original: bool = False
) -> np.ndarray:
    frame = camera.shot()

    if original:
        return frame
    im: np.ndarray = cv2.resize(frame, dsize=size)
    im = im.flatten()

    return im


if __name__ == "__main__":
    print(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    camera: dxcam.DXCamera = dxcam.create(
        device_idx=0,
        region=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        output_color="GRAY",
    )

    camera.start()
    while 5:
        time.sleep(3)
        im = screenshot(
            camera,
            (
                160 * 2,
                90 * 2,
            ),
            original=True,
        )
        Image.fromarray(cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)).show()
        reset = cv2.imread("imgs/reset.png", cv2.IMREAD_GRAYSCALE)
        Image.fromarray(cv2.cvtColor(reset, cv2.COLOR_GRAY2RGB)).show()

        if reset is None:
            raise FileNotFoundError("The 'reset.png' file could not be found or read.")
        if reset.shape[0] > im.shape[0] or reset.shape[1] > im.shape[1]:
            raise ValueError(
                "The template image (reset.png) is larger than the screenshot. Please use a smaller template."
            )
        # Perform template matching

        res = cv2.matchTemplate(im, reset, cv2.TM_SQDIFF_NORMED)

        # Find the best match

        min_val, _, _, _ = cv2.minMaxLoc(res)

        # Define a threshold for matching (you may need to adjust this)

        threshold = 0.1

        # Check if the best match is below the threshold (lower is better for TM_SQDIFF_NORMED)

        has_lost = min_val < threshold

        print(f"Min val: {min_val}, has_lost: {has_lost}")
    camera.stop()
