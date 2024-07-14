from dataclasses import dataclass, field
from enum import Enum

from .render import Render


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


class OsuPy:
    def __init__(self) -> None:
        self.render = Render(self)
        self.notes = []
        self.score = 0
        self.accuracy = 0
        self.hp = 200
        self.time = 0

    def step(self) -> None:
        self.time += 1
