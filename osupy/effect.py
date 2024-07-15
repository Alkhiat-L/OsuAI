from abc import abstractmethod
from dataclasses import dataclass

import pygame

from pygame import Surface


@dataclass
class Effect:
    queue_delete = False
    time = 0

    @abstractmethod
    def step(self, delta) -> None:
        if self.time < 0:
            self.queue_delete = True

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        pass


@dataclass
class SplashEffect(Effect):
    position: tuple[int, int]
    duration: int = 1000

    def __post_init__(self):
        self.time = self.duration

    def step(self, delta: int) -> None:
        super().step(delta)
        self.time -= delta

    def draw(self, surface: Surface) -> None:
        try:
            pygame.draw.circle(
                surface,
                (60, 60, 230, max(min(60 * (self.time // self.duration), 255), 0)),
                self.position,
                min(5 * (self.duration // self.time), 100),
            )
        except Exception:
            pass
