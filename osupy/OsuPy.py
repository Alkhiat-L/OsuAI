import sys
import time
from dataclasses import dataclass, field
from enum import Enum

import pygame

from osupy.effect import Effect, SplashEffect

from .render import Renderer


class NoteType(Enum):
    CIRCLE = 0
    SLIDER = 1
    COMBO = 2
    SPINNER = 3
    COMBO_1 = 4
    COMBO_2 = 5
    COMBO_3 = 6
    HOLD = 7


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y

    @staticmethod
    def from_string(string: str) -> "Point":
        x = int(string.split(":")[0])
        y = int(string.split(":")[1])
        return Point(x, y)


@dataclass
class Note:
    x: int
    y: int
    time: int
    type_f: NoteType
    hit_sound: int = 0
    curve_type: str = ""
    curve_points: list[Point] = field(default_factory=lambda: [])

    @staticmethod
    def from_string(string: str) -> "Note":
        args = string.split(",")
        curve_points = [Point.from_string(i) for i in args[5].split("|")[1:]]
        return Note(
            int(args[0]),
            int(args[1]),
            int(args[2]),
            NoteType(int(args[3])),
            curve_type=args[5].split("|")[0],
            curve_points=curve_points,
        )


class States(Enum):
    IDLE = 0
    TRAIN = 1
    HUMAN = 2


@dataclass
class ActionSpace:
    x: int
    y: int
    click: bool

    def mouse_pos(self) -> tuple[int, int]:
        return (self.x, self.y)


def _to_miliseconds(nanosecs: int) -> int:
    return nanosecs // 1000000


class OsuPy:
    def __init__(
        self,
    ) -> None:
        self.renderer = Renderer(self)
        self.notes = []
        self.score = 0
        self.accuracy = 0
        self.hp = 200
        self.time = 0
        self.last_time = 0
        self.state: States = States.IDLE
        self.mouse: tuple[int, int] = (0, 0)
        self.effects: list[Effect] = []
        self.delta = 0

    def step(self, action: "ActionSpace") -> None:
        self.mouse = action.mouse_pos()

        if action.click:
            self.effects.append(SplashEffect(self.mouse))
        for effect in self.effects:
            effect.step(self.delta)
            if effect.queue_delete:
                del effect
        if self.state == States.HUMAN:
            self.render()
        if self.state == States.TRAIN:
            self.time += 1
            self.delta = 1

    def render(self) -> None:
        self.renderer.render()
        now = _to_miliseconds(time.time_ns())
        self.time += now - self.last_time
        self.delta = now - self.last_time
        self.last_time = now

    def reset(self) -> None:
        self.notes = []
        self.score = 0
        self.accuracy = 0
        self.hp = 200
        self.time = 0
        self.last_time = 0
        self.state: States = States.IDLE


if __name__ == "__main__":
    print("Starting...")
    osu = OsuPy()
    osu.reset()
    osu.state = States.HUMAN

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pressed_keys = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        osu.step(ActionSpace(mouse[0], mouse[1], pressed_keys[0]))
