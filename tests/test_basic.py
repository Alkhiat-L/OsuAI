from typing import Literal
import osupy.NoteType

import osupy.Point
import pytest

from .context import OsuPy


@pytest.fixture
def note_str():
    return "200,175,2226,2,0,L|-8:233,3,200"


def test_works():
    assert 1 == 1


def test_load_a_note(note_str: Literal["200,175,2226,2,0,L|-8:233,3,200"]):
    note = OsuPy.Note.from_string(note_str)

    assert type(note) is OsuPy.Note


def test_load_note_position(note_str: Literal["200,175,2226,2,0,L|-8:233,3,200"]):
    note = OsuPy.Note.from_string(note_str)

    assert note.x == 200
    assert note.y == 175


def test_load_note_time(note_str: Literal["200,175,2226,2,0,L|-8:233,3,200"]):
    note = OsuPy.Note.from_string(note_str)

    assert note.time == 2226


def test_load_note_curve_points(note_str: Literal["200,175,2226,2,0,L|-8:233,3,200"]):
    note = OsuPy.Note.from_string(note_str)

    assert osupy.Point.Point(-8, 233) in note.curve_points


def test_load_type(note_str: Literal["200,175,2226,2,0,L|-8:233,3,200"]):
    note = OsuPy.Note.from_string(note_str)

    assert note.type_f == osupy.NoteType.NoteType.SLIDER


def test_load_note_with_multiple_points():
    note_str = (
        "114,65,6093,6,0,P|174:37|286:108,1,199.999980926514,8|8,0:0|0:0,0:0:0:0:"
    )
    note = OsuPy.Note.from_string(note_str)

    assert osupy.Point.Point(174, 37) in note.curve_points
    assert osupy.Point.Point(286, 108) in note.curve_points
