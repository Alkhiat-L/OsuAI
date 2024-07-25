import re
from dataclasses import dataclass
from typing import Any, Dict, List

from osupy.Note import Note
from osupy.NoteType import NoteType
from osupy.Point import Point


@dataclass
class TimingPoint:
    time: int
    beat_length: float


@dataclass
class Beatmap:
    title: str
    artist: str
    creator: str
    version: str
    hp_drain_rate: float
    circle_size: float
    overall_difficulty: float
    approach_rate: float
    slider_multiplier: float
    slider_tick_rate: float
    audio_filename: str
    timing_points: dict[int, TimingPoint]
    notes: List[Note]

    def __post_init__(self) -> None:
        for note in self.notes:
            note.beatmap = self
            if note.time not in self.timing_points.keys():
                self.timing_points.update({note.time: TimingPoint(note.time, -100)})
            note.__post_init__()


def parse_timing_points(timing_points_section: str) -> Dict[int, TimingPoint]:
    timing_points = dict()
    for line in timing_points_section.strip().split("\n"):
        parts = line.split(",")
        time = int(parts[0])
        beat_length = float(parts[1])
        timing_points.update({time: TimingPoint(time, beat_length)})
    return timing_points


def parse_beatmap(file_path: str) -> Beatmap:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    sections = re.split(r"^\[([^\]]+)\]\n", content, flags=re.MULTILINE)[1:]
    sections = dict(zip(sections[::2], sections[1::2]))

    metadata = parse_section(sections["Metadata"])
    difficulty = parse_section(sections["Difficulty"])
    hit_objects = parse_hit_objects(sections["HitObjects"])
    general = parse_section(sections["General"])
    timing_points = parse_timing_points(sections["TimingPoints"])

    return Beatmap(
        title=metadata["Title"],
        artist=metadata["Artist"],
        creator=metadata["Creator"],
        version=metadata["Version"],
        hp_drain_rate=float(difficulty["HPDrainRate"]),
        circle_size=float(difficulty["CircleSize"]),
        overall_difficulty=float(difficulty["OverallDifficulty"]),
        approach_rate=float(difficulty["ApproachRate"]),
        slider_multiplier=float(difficulty["SliderMultiplier"]),
        slider_tick_rate=float(difficulty["SliderTickRate"]),
        notes=hit_objects,
        audio_filename=general["AudioFilename"],
        timing_points=timing_points,
    )


def parse_section(section: str) -> Dict[str, Any]:
    return dict(re.findall(r"^([^:]+):\s*(.+)$", section, re.MULTILINE))


def parse_hit_objects(hit_objects_section: str) -> List[Note]:
    notes = []
    for line in hit_objects_section.strip().split("\n"):
        parts = line.split(",")
        x, y, time, type_flags = map(int, parts[:4])
        note_type = Note.get_type(type_flags)  # Extract the base note type
        length = None
        if note_type == NoteType.SLIDER:
            curve_type, *curve_points_str = parts[5].split("|")
            curve_points = [Point.from_string(p) for p in curve_points_str]
            length = float(parts[7])
        else:
            curve_type, curve_points = "", []
        notes.append(
            Note(
                x=x,
                y=y,
                time=time,
                type_f=note_type,
                hit_sound=int(parts[4]),
                length=length,
                curve_type=curve_type,
                curve_points=curve_points,
            )
        )
    return notes
