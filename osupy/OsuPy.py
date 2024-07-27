from collections import OrderedDict
import math
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Tuple

from matplotlib.pylab import f
import numpy as np
import pygame

import osupy.effect as e

from osupy.beatmap import Beatmap, parse_beatmap

from osupy.bezier_curve import bezier_curve
from osupy.linear import linear

from osupy.Note import Note

from osupy.NoteType import NoteType
from osupy.perfect_circle import perfect_circle

from osupy.render import Renderer


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

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


@dataclass
class ObservationSpace:
    game_time: float
    mouse_pos: Tuple[int, int]
    upcoming_notes: List[Note]
    curve: Optional[Note]
    hp: int
    score: int
    accuracy: float

    def _upcoming_notes(self) -> tuple[OrderedDict, ...]:
        return tuple(
            [
                OrderedDict(
                    {
                        "time": np.array([note.time], dtype=np.float32),
                        "type": note.type_f.value,
                        "x": np.array([note.get_virtual_x()], dtype=np.float32),
                        "y": np.array([note.get_virtual_y()], dtype=np.float32),
                    }
                )
                for note in self.upcoming_notes[:5]
            ]
        )

    def _curve(self):
        if self.curve is None:
            return [0] * 8
        curve = [point.get_virtual_x() for point in self.curve.curve_points] + [
            point.get_virtual_y() for point in self.curve.curve_points
        ]
        if len(curve) <= 8:
            for _ in range(8 - len(curve)):
                curve.append(0)
        return np.array(curve, dtype=np.float32)

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            {
                "game_time": np.array([self.game_time], dtype=np.float32),
                "x": np.array([int(self.mouse_pos[0])], dtype=np.float32),
                "y": np.array([int(self.mouse_pos[1])], dtype=np.float32),
                "upcoming_notes": self._upcoming_notes(),
                "curve": self._curve(),
            }
        )


@dataclass
class Info:
    hp: float
    score: int
    accuracy: float

    def as_dict(self) -> OrderedDict:
        return OrderedDict(
            {
                "hp": self.hp,
                "score": self.score,
                "accuracy": self.accuracy,
            }
        )


class OsuPy:
    def __init__(
        self,
    ) -> None:
        self.renderer = Renderer(self)
        self.beatmap: Optional[Beatmap] = None
        self.notes = []
        self.upcoming_notes: List[Note] = []
        self.effects: List[e.Effect] = []
        self.score = 0
        self.last_score = 0
        self.accuracy = 1
        self.last_accuracy = 1
        self.hp = 200
        self.last_hp = 200
        self.notes_len = 0
        self.notes_hit = 0
        self.game_time = 0  # Time since the start of the beatmap
        self.last_update_time = 0  # Last time the game state was updated
        self.state: States = States.IDLE
        self.mouse: tuple[int, int] = (0, 0)
        self.delta: float = 0
        self.hold = False
        self.hit_window = 300  # ms
        self.curve_to_follow: Optional[Note] = None
        # pygame.mixer.init()
        # self.audio: Optional[pygame.mixer.Sound] = None
        # self.audio_start_time = 0

    def start_game(self) -> None:
        self.state = States.HUMAN
        self.last_update_time = time.time()
        # self.audio_start_time = time.time()
        # if self.audio:
        #     self.audio.set_volume(0.05)
        #     self.audio.play()

    def stop_game(self) -> None:
        # if self.audio:
        #     self.audio.stop()
        self.state = States.IDLE

    def load_beatmap(self, file_path: str) -> None:
        self.beatmap = parse_beatmap(file_path)
        self.notes = self.beatmap.notes
        # audio_path = os.path.join(
        #     os.path.dirname(file_path), self.beatmap.audio_filename
        # )
        # if os.path.exists(audio_path):
        #     self.audio = pygame.mixer.Sound(audio_path)
        # else:
        #     print(f"Warning: Audio file not found at {audio_path}")
        self.reset()

    def step(self, action: ActionSpace) -> Tuple[dict[str, Any], float, bool, dict]:
        action = ActionSpace(action["x"], action["y"], action["click"])
        self.mouse = (int(action.x), int(action.y))

        if action.click and not self.hold:
            self.effects.append(e.SplashEffect(position=self.mouse))
            self.effects.append(e.ParticleEffect(position=self.mouse))
            self.check_hit()
            self.hold = True
        self.check_misses()
        self.check_curve()
        self.accuracy = max(5, self.notes_hit) / max(5, self.notes_len) * 100
        if not action.click and self.hold:
            self.hold = False
        self.effects = [effect for effect in self.effects if not effect.is_finished()]
        for effect in self.effects:
            effect.step(self.delta)
        self.upcoming_notes = [
            note
            for note in self.upcoming_notes
            if note.time > self.game_time - self.hit_window
        ]

        done = False
        if self.hp <= 0 or len(self.upcoming_notes) == 0:
            self.stop_game()
            done = True

        observation = self.get_observation()
        reward = self.get_reward()

        self.last_accuracy = self.accuracy
        self.last_score = self.score
        self.last_hp = self.hp

        return observation, reward, done, {}

    def check_hit(self) -> None:
        for note in self.upcoming_notes:
            distance = math.sqrt(
                (note.get_virtual_x() - self.mouse[0]) ** 2
                + (note.get_virtual_y() - self.mouse[1]) ** 2
            )
            error = abs(note.time - self.game_time)
            if error <= self.hit_window and distance <= 54:
                self.hit_note(note)
                return
            if error <= self.hit_window * 2 and distance <= 70:
                self.hit_note(note, 100)
                return
            if error <= self.hit_window * 3 and distance <= 90:
                self.hit_note(note, 50)
                return
        self.miss()

    def check_misses(self) -> None:
        if len(self.upcoming_notes) <= 0:
            return
        for note in self.upcoming_notes:
            error = note.time - self.game_time
            if error <= self.hit_window / 2:
                self.miss()
                self.upcoming_notes.remove(note)
                return

    def check_curve(self) -> None:
        if self.curve_to_follow is None:
            return
        if self.curve_to_follow.type_f == NoteType.SLIDER:
            if self.curve_to_follow.duration is None:
                return
            progress = min(
                1,
                max(0, self.game_time - self.curve_to_follow.time)
                / (self.curve_to_follow.duration),
            )
            current_point = self.calculate_curve_point(self.curve_to_follow, progress)

            distance = math.sqrt(
                (current_point[0] - self.mouse[0]) ** 2
                + (current_point[1] - self.mouse[1]) ** 2
            )
            score = 0
            if distance >= 80 or not self.hold:
                self.curve_to_follow = None
            if progress >= 0.5 and progress < 0.7:
                score = 50
            if progress >= 0.7 and progress < 0.9:
                score = 100
            if progress >= 0.9:
                score = 300
                self.curve_to_follow = None

            if self.curve_to_follow is None:
                self.effects.append(
                    e.ScorePopup(
                        position=(
                            current_point[0],
                            current_point[1],
                        ),
                        score=score,
                    )
                )
                self.score += score

                if score >= 50:
                    self.notes_hit += 1

    def calculate_curve_point(self, note: Note, progress: float) -> Tuple[int, int]:
        points = [(note.get_virtual_x(), note.get_virtual_y())] + [
            (p.get_virtual_x(), p.get_virtual_y()) for p in note.curve_points
        ]
        if note.curve_type == "B":
            points = bezier_curve(points, 50)
        if note.curve_type == "P":
            points = perfect_circle(points, 100)
            points.reverse()
        if note.curve_type == "L":
            points = linear(points, 50)
        if len(points) <= int(len(points) * progress) + 1:
            return (note.get_virtual_x(), note.get_virtual_y())
        return points[int(len(points) * progress)]

    def hit_note(self, note: Note, score: int = 300) -> None:
        self.notes_len += 1
        if not note.type_f == NoteType.SLIDER:
            self.score += score
            if score == 50:
                self.notes_hit += 1

            self.hp = min(200, self.hp + 20)
            self.upcoming_notes.remove(note)

            self.effects.append(
                e.ScorePopup(
                    position=(note.get_virtual_x(), note.get_virtual_y()), score=score
                )
            )

        if note.type_f == NoteType.SLIDER:
            self.effects.append(
                e.SliderEffect(
                    note=note,
                    duration=int(note.duration or 1000),
                )
            )
            self.curve_to_follow = note

    def miss(self) -> None:
        self.accuracy = self.notes_hit / self.notes_len
        self.hp = max(0, self.hp - 10)
        self.notes_len += 1

    def get_observation(self) -> OrderedDict:
        return ObservationSpace(
            game_time=self.game_time,
            mouse_pos=self.mouse,
            upcoming_notes=[note for note in self.upcoming_notes[:5]],
            hp=self.hp,
            curve=self.curve_to_follow,
            score=self.score,
            accuracy=self.accuracy,
        ).as_dict()

    def _distance_from_next_note(self) -> float:
        if len(self.upcoming_notes) == 0:
            return 0
        return math.sqrt(
            (self.upcoming_notes[0].get_virtual_x() - self.mouse[0]) ** 2
            + (self.upcoming_notes[0].get_virtual_y() - self.mouse[1]) ** 2
        )

    def get_reward(self) -> float:
        return (
            ((self.score - self.last_score) * 500)
            + (self.accuracy - self.last_accuracy) * 10
            + (self.hp - self.last_hp) / 10
            - ((self._distance_from_next_note() - 100) / 100)
        )

    def render(self) -> None:
        if self.state == States.HUMAN:
            self.renderer.render()
            current_time = time.time()
            self.delta = (
                current_time - self.last_update_time
            ) * 1000  # Convert to milliseconds
            self.game_time += self.delta
            self.last_update_time = current_time
        if self.state == States.TRAIN:
            self.game_time += 1
            self.delta = 1

    def reset(self) -> dict[str, Any]:
        self.upcoming_notes = self.notes.copy()
        self.game_time = 0
        self.last_update_time = time.time()
        self.score = 0
        self.last_score = 0
        self.accuracy = 1
        self.last_accuracy = 1
        self.hp = 200
        self.last_hp = 200
        self.last_time = 0
        self.state: States = States.IDLE
        self.effects.clear()
        self.notes_len = 0
        self.notes_hit = 0

        self.audio_start_time = 0

        return self.get_observation()


if __name__ == "__main__":
    print("Starting...")
    osu = OsuPy()
    osu.load_beatmap("beatmap.osu")
    osu.start_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pressed_keys = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        observation, reward, done, _ = osu.step(
            ActionSpace(mouse[0], mouse[1], pressed_keys[0])
        )
        osu.render()
        if done:
            osu.reset()
            osu.start_game()
