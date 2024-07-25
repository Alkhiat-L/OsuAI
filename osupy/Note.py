from dataclasses import dataclass, field

from osupy.NoteType import NoteType
from osupy.Point import Point


@dataclass
class Note:
    x: int
    y: int
    time: int
    type_f: NoteType
    hit_sound: int = 0
    curve_type: str = ""
    combo_number = 50
    curve_points: list[Point] = field(default_factory=lambda: [])

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
        )
