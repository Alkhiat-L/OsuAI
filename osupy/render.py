from typing import Optional, TYPE_CHECKING

import pygame
import pygame.locals

from osupy.NoteType import NoteType


if TYPE_CHECKING:
    from OsuPy import OsuPy
DEBUG = 0


class Renderer:
    def __init__(self, parent: "OsuPy") -> None:
        self.parent = parent
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface: Optional[pygame.Surface] = None
        self.width = 640
        self.height = 480
        self.font = pygame.font.Font(None, 36)

    def render(self) -> None:
        if self.surface is None:
            self.surface = pygame.display.set_mode((self.width, self.height))
        # Background

        self.surface.fill((25, 25, 35))

        # Draw grid

        self.draw_grid()

        # Draw notes

        self.draw_notes()

        # Draw effects

        for effect in self.parent.effects:
            effect.draw(self.surface)
        # Draw cursor

        pygame.draw.circle(self.surface, (200, 200, 200), self.parent.mouse, 5)

        # Draw UI elements

        self.draw_ui()

        pygame.display.update()
        self.clock.tick(60)

    def draw_grid(self) -> None:
        if not self.surface:
            return
        for x in range(0, self.width, 40):
            pygame.draw.line(self.surface, (50, 50, 60), (x, 0), (x, self.height))
        for y in range(0, self.height, 40):
            pygame.draw.line(self.surface, (50, 50, 60), (0, y), (self.width, y))

    def draw_notes(self) -> None:
        if not self.surface:
            return
        current_time = self.parent.game_time
        approach_rate = self.parent.beatmap.approach_rate if self.parent.beatmap else 9
        approach_duration = 1200 - (approach_rate * 100)  # AR9 = 450ms, AR10 = 350ms

        for note in self.parent.upcoming_notes:
            time_diff = note.time - current_time
            if 0 <= time_diff <= approach_duration:
                progress = 1 - (time_diff / approach_duration)
                size = int(54 + (1 - progress) * 54)
                alpha = int(255 * progress)

                circle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(
                    circle_surface,
                    (255, 68, 68, alpha),
                    (size // 2, size // 2),
                    size // 2,
                )
                pygame.draw.circle(
                    circle_surface,
                    (255, 255, 255, alpha),
                    (size // 2, size // 2),
                    size // 2 - 2,
                    2,
                )

                self.surface.blit(
                    circle_surface, (note.x - size // 2, note.y - size // 2)
                )

                if progress > 0.8:
                    pygame.draw.circle(
                        self.surface, (255, 255, 255), (note.x, note.y), 27
                    )
                # Draw number for combo

                combo_num = self.font.render(
                    str(note.combo_number), True, (255, 255, 255)
                )
                self.surface.blit(
                    combo_num,
                    (
                        note.x - combo_num.get_width() // 2,
                        note.y - combo_num.get_height() // 2,
                    ),
                )

                # Draw slider path if it's a slider

                if note.type_f == NoteType.SLIDER:
                    points = [(note.x, note.y)] + [
                        (p.x, p.y) for p in note.curve_points
                    ]
                    pygame.draw.lines(
                        self.surface, (255, 255, 255, alpha), False, points, 2
                    )

    def draw_ui(self) -> None:
        if not self.surface:
            return
        score_text = self.font.render(
            f"Score: {self.parent.score}", True, (255, 255, 255)
        )
        accuracy_text = self.font.render(
            f"Accuracy: {self.parent.accuracy:.2f}%", True, (255, 255, 255)
        )
        hp_text = self.font.render(f"HP: {self.parent.hp}", True, (255, 255, 255))

        self.surface.blit(score_text, (10, 10))
        self.surface.blit(accuracy_text, (10, 50))
        self.surface.blit(hp_text, (10, 90))

        if DEBUG:
            self.debug_ui()

    def debug_ui(self) -> None:
        if not self.surface:
            return
        if not self.parent.beatmap:
            return
        self.surface.blit(
            self.font.render(
                f"upcoming notes: {len(self.parent.upcoming_notes)}",
                True,
                (255, 255, 255),
            ),
            (10, 130),
        )
        self.surface.blit(
            self.font.render(
                f"time: {self.parent.game_time:.2f}",
                True,
                (255, 255, 255),
            ),
            (10, 150),
        )
