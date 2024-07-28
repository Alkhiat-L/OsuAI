import random
from abc import abstractmethod

import pygame

from osupy.bezier_curve import bezier_curve
from osupy.linear import linear

from osupy.Note import Note
from osupy.perfect_circle import perfect_circle


class Effect:
    def __init__(self, duration: int = 1000):
        self.duration = duration
        self.time = duration

    def step(self, delta: float) -> None:
        self.time -= delta

    def is_finished(self) -> bool:
        return self.time <= 0

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass


class SplashEffect(Effect):
    def __init__(self, position: pygame.math.Vector2, duration: int = 1000):
        super().__init__(duration)
        self.position = position

    def draw(self, surface: pygame.Surface) -> None:
        progress = self.time / self.duration
        size = int(30 * (1 - progress))
        alpha = int(255 * progress)

        circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            circle_surface, (60, 60, 230, max(min(alpha, 255), 0)), (size, size), size
        )
        surface.blit(circle_surface, (self.position[0] - size, self.position[1] - size))


class ScorePopup(Effect):
    def __init__(self, position: tuple[int, int], score: int, duration: int = 1000):
        super().__init__(duration)
        self.position = position
        self.score = score
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface: pygame.Surface) -> None:
        progress = self.time / self.duration
        y_offset = int(30 * (1 - progress))
        alpha = int(255 * progress)

        text = self.font.render(
            f"+{self.score}", True, (255, 255, 255, max(min(alpha, 255), 0))
        )
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        surface.blit(
            text_surface,
            (self.position[0] - text.get_width() // 2, self.position[1] - y_offset),
        )


class SliderEffect(Effect):
    def __init__(self, note: Note, duration: int = 1000):
        super().__init__(duration)
        self.note = note
        self.curve = [(self.note.get_virtual_x(), self.note.get_virtual_y())] + [
            (p.get_virtual_x(), p.get_virtual_y()) for p in self.note.curve_points
        ]
        if self.note.curve_type == "B":
            self.curve = bezier_curve(self.curve, 50)
        if self.note.curve_type == "P":
            self.curve = perfect_circle(self.curve, 100)
            self.curve.reverse()
        if self.note.curve_type == "L":
            self.curve = linear(self.curve, 50)

    def draw(self, surface: pygame.Surface) -> None:
        progress = 1 - (self.time / self.duration)
        if len(self.curve) <= int(len(self.curve) * progress) + 1:
            return
        actual_node = self.curve[int(len(self.curve) * progress)]
        pygame.draw.circle(surface, (255, 68, 68), (actual_node[0], actual_node[1]), 15)
        pygame.draw.lines(
            surface,
            (255, 68, 68),
            False,
            self.curve[int(len(self.curve) * progress) :],
            2,
        )


class ParticleEffect(Effect):
    def __init__(self, position: pygame.math.Vector2, duration: int = 1000):
        super().__init__(duration)
        self.position = position
        self.particles = [
            (random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)
        ]

    def draw(self, surface: pygame.Surface) -> None:
        progress = self.time / self.duration

        for dx, dy in self.particles:
            x = int(self.position[0] + dx * 30 * (1 - progress))
            y = int(self.position[1] + dy * 30 * (1 - progress))
            size = int(3 * progress)
            alpha = int(255 * progress)

            pygame.draw.circle(
                surface, (255, 255, 0, max(min(alpha, 255), 0)), (x, y), size
            )
