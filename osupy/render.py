from typing import Optional, TYPE_CHECKING

import pygame
import pygame.locals

if TYPE_CHECKING:
    from OsuPy import OsuPy


class Renderer:
    def __init__(self, parent: "OsuPy") -> None:
        self.parent = parent
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface: Optional[pygame.Surface] = None

    def render(self) -> None:
        if self.surface is None:
            self.surface = pygame.display.set_mode((640, 480))
        self.surface.fill((55, 55, 200))

        pygame.draw.circle(self.surface, (200, 200, 200), self.parent.mouse, 5)

        for effect in self.parent.effects:
            effect.draw(self.surface)
        pygame.display.update()
        self.clock.tick(60)
