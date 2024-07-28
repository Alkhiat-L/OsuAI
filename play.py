"""
Versão antiga do projeto, que foi feita para funcionar gravando a tela do jogo original,
essa versão não está mais sendo atualizada. A versão atualizada do projeto está na pasta
'osupy'.
"""

import sys

import pygame
from osupy.OsuPy import ActionSpace, OsuPy


if __name__ == "__main__":
    print("Starting...")
    osu = OsuPy()
    osu.load_beatmap("beatmap.osu")
    osu.start_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pressed_keys = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        observation, reward, done, _ = osu.step(
            ActionSpace(mouse[0], mouse[1], pressed_keys[0])
        )
        if done:
            osu.reset()
            osu.start_game()
