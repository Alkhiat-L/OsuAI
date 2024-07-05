import dxcam
import keyboard
import mouse
import torch
import torchvision
import win32gui
import cv2
from tokens import *
import time
import numpy as np

C300REWARD = 30
C100REWARD = 10
C500REWARD = 50
MISSESREWARD = -100
MOUSEMOVE = 50


def check_apps() -> int:
    tabs = []
    tabs.append(win32gui.FindWindow(None, "StreamCompanion (x64)"))
    if len(tabs) == 0:
        return 0
    tabs.append(win32gui.FindWindow(None, "osu!"))
    if len(tabs) == 1:
        return -1
    if len(tabs) == 2:
        return 1


def restart():
    keyboard.press('r')
    time.sleep(1)
    keyboard.release('r')


def calculate_gaes(self, rew, val, gamma=0.99, decay=0.97):
    next_val = np.concatenate([val[1:], [0]])
    deltas = [rew + gamma * next_val - val for rew, val, next_val in zip(rew, val, next_val)]

    gaes = [deltas[-1]]
    for i in reversed(range(len(deltas) - 1)):
        gaes.append(deltas[i] + decay * gamma * gaes[-1])

    ## normalizing the advantages

    mean = np.mean(gaes[::-1])
    std_dev = np.std(gaes[::-1])

    normalized_gaes = [(gae - mean) / std_dev + 1e-8 for gae in (gaes[::-1])]

    return np.array(normalized_gaes)


def screenshot(camera):
    frame = camera.get_latest_frame()

    im = cv2.resize(frame, dsize=(96, 96))

    tensor = torch.unsqueeze(torchvision.transforms.ToTensor()(im), 0)

    tensor = tensor.to(device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    return tensor

def step(action, camera):
    x, y = mouse.get_position()
    match action:
        case 0:
            keyboard.press_and_release('z')
        case 1:
            mouse.move(x + MOUSEMOVE, y)
        case 2:
            mouse.move(x - MOUSEMOVE, y)
        case 3:
            mouse.move(x, y + MOUSEMOVE)
        case 4:
            mouse.move(x, y - MOUSEMOVE)
        case 5:
            mouse.move(x + MOUSEMOVE, y + MOUSEMOVE)
        case 6:
            mouse.move(x - MOUSEMOVE, y + MOUSEMOVE)
        case 7:
            mouse.move(x - MOUSEMOVE, y - MOUSEMOVE)
        case 8:
            mouse.move(x + MOUSEMOVE, y - MOUSEMOVE)
    screen = screenshot(camera)
    if get_status() == 32 or get_hp() == 0:
        finished = True
    else:
        finished = False
    try:
        c300, c100, c50, misses = get_300(), get_100(), get_50(), get_misses()
    except Exception:
        c300, c100, c50, misses = 0, 0, 0, 0
        print(Exception)
    reward = c300 * C300REWARD + c100 * C100REWARD + c50 * C500REWARD + misses * MISSESREWARD
    return screen, reward, finished
