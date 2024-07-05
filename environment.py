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

def screenshot(camera):
    frame = camera.get_latest_frame()

    im = cv2.resize(frame, dsize=(96, 96))

    tensor = torch.unsqueeze(torchvision.transforms.ToTensor()(im), 0)

    tensor = tensor.to(device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    return tensor

def step(action, camera):
    x, y = action.x, action.y
    x0, y0 = mouse.get_position()
    mouse.drag(x0, y0, x, y)
    if action.click == 1:
        mouse.click()
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
