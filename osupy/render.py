from typing import Optional, TYPE_CHECKING

import pygame

from osupy.bezier_curve import bezier_curve

from osupy.NoteType import NoteType
from osupy.perfect_circle import perfect_circle


if TYPE_CHECKING:
    from OsuPy import OsuPy
DEBUG = 0


class Renderer:
    def __init__(self, parent: "OsuPy") -> None:
        self.parent = parent
        pygame.init()
        pygame.mouse.set_cursor(pygame.cursors.ball)
        self.clock = pygame.time.Clock()
        self.surface: Optional[pygame.Surface] = None
        self.width = 800
        self.height = 600
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
        approach_duration = 1200 - 750 * (approach_rate - 5) / 5
        fade_in = 800 - 500 * (approach_rate - 5) / 5

        for note in self.parent.upcoming_notes:
            time_diff = note.time - current_time
            if 0 <= time_diff <= approach_duration:
                progress = 1 - (time_diff / approach_duration)
                fade_in_progress = 1 - (time_diff / fade_in)
                size = int(54 + (1 - progress) * 54)
                alpha = int(255 * progress)
                fade_in_alpha = int(255 * fade_in_progress)

                circle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(
                    circle_surface,
                    (255, 68, 68, max(min(alpha, 255), 0)),
                    (size // 2, size // 2),
                    size // 2,
                )
                pygame.draw.circle(
                    circle_surface,
                    (255, 255, 255, max(min(alpha, 255), 0)),
                    (size // 2, size // 2),
                    size // 2 - 2,
                    2,
                )
                final_circle_surface = pygame.Surface((54, 54), pygame.SRCALPHA)
                pygame.draw.circle(
                    final_circle_surface,
                    (255, 68, 68, max(min(fade_in_alpha, 255), 0)),
                    (27, 27),
                    27 - 2,
                )

                self.surface.blit(
                    final_circle_surface,
                    (note.get_virtual_x() - 27, note.get_virtual_y() - 27),
                )

                self.surface.blit(
                    circle_surface,
                    (
                        note.get_virtual_x() - size // 2,
                        note.get_virtual_y() - size // 2,
                    ),
                )

                if progress > 0.8:
                    pygame.draw.circle(
                        self.surface,
                        (255, 255, 255),
                        (note.get_virtual_x(), note.get_virtual_y()),
                        27,
                    )
                # Draw number for combo

                combo_num = self.font.render(
                    str(note.combo_number), True, (255, 255, 255)
                )
                self.surface.blit(
                    combo_num,
                    (
                        note.get_virtual_x() - combo_num.get_width() // 2,
                        note.get_virtual_y() - combo_num.get_height() // 2,
                    ),
                )

                # Draw slider path if it's a slider

                if note.type_f == NoteType.SLIDER:
                    points = [(note.get_virtual_x(), note.get_virtual_y())] + [
                        (p.get_virtual_x(), p.get_virtual_y())
                        for p in note.curve_points
                    ]
                    if note.curve_type == "B":
                        points = bezier_curve(points)
                    if note.curve_type == "P":
                        points = perfect_circle(points)
                    pygame.draw.lines(
                        self.surface,
                        (255, 255, 255, max(min(alpha, 255), 0)),
                        False,
                        points,
                        2,
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
