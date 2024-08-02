from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, Tuple

from osupy.NoteType import NoteType

from osupy.Point import Point

if TYPE_CHECKING:
    from osupy.beatmap import Beatmap


@dataclass
class Note:
    x: int
    y: int
    time: int
    type_f: NoteType
    hit_sound: int = 0
    duration: Optional[float] = None
    curve_type: str = ""
    combo_number: int = 1
    curve_points: list["Point"] = field(default_factory=lambda: [])
    slides: int = 1
    length: Optional[float] = None
    beatmap: Optional["Beatmap"] = None
    hit: bool = False

    @property
    def end_time(self) -> float:
        if self.duration is None:
            return 0
        return self.time + self.duration

    def __post_init__(self) -> None:
        if self.beatmap is None:
            return
        if self.length is None:
            return
        self.duration = (
            abs(
                (self.length / (self.beatmap.slider_multiplier * 100 * 2))
                * self.beatmap.timing_points[self.time].beat_length
            )
            * 10
        )

    @staticmethod
    def get_type(type_f: int) -> NoteType:
        circle = 0b00000001
        slider = 0b00000010
        combo = 0b00000100
        spinner = 0b00001000
        if type_f & circle:
            return NoteType.CIRCLE
        if type_f & slider:
            return NoteType.SLIDER
        if type_f & combo:
            return NoteType.COMBO
        if type_f & spinner:
            return NoteType.SPINNER
        return NoteType.CIRCLE

    def get_virtual_x(self) -> int:
        return self.x + 150

    def get_virtual_y(self) -> int:
        return self.y + 150

    def get_virtual_position(self) -> Tuple[int, int]:
        return (self.get_virtual_x(), self.get_virtual_y())

    @staticmethod
    def from_string(string: str) -> "Note":
        args = string.split(",")
        curve_points = [Point.from_string(i) for i in args[5].split("|")[1:]]
        return Note(
            int(args[0]),
            int(args[1]),
            int(args[2]),
            Note.get_type(int(args[3])),
            curve_type=args[5].split("|")[0],
            curve_points=curve_points,
            length=float(args[7]),
        )

    def mark_hit(self) -> None:
        self.hit = True
