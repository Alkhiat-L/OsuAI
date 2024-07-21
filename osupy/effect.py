import random
from abc import abstractmethod

import pygame


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
    def __init__(self, position: tuple[int, int], duration: int = 1000):
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
    def __init__(
        self, start: tuple[int, int], end: tuple[int, int], duration: int = 1000
    ):
        super().__init__(duration)
        self.start = start
        self.end = end

    def draw(self, surface: pygame.Surface) -> None:
        progress = 1 - (self.time / self.duration)
        x = int(self.start[0] + (self.end[0] - self.start[0]) * progress)
        y = int(self.start[1] + (self.end[1] - self.start[1]) * progress)

        pygame.draw.circle(surface, (255, 68, 68), (x, y), 15)
        pygame.draw.line(surface, (255, 68, 68), self.start, (x, y), 3)


class ParticleEffect(Effect):
    def __init__(self, position: tuple[int, int], duration: int = 1000):
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
