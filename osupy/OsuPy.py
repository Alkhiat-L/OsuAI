import math
import os
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import pygame

import osupy.effect as e

from osupy.beatmap import Beatmap, parse_beatmap

from osupy.Note import Note

from osupy.NoteType import NoteType

from .render import Renderer


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


class OsuPy:
    def __init__(
        self,
    ) -> None:
        self.renderer = Renderer(self)
        self.beatmap: Optional[Beatmap] = None
        self.notes = []
        self.upcoming_notes = []
        self.effects: List[e.Effect] = []
        self.score = 0
        self.accuracy = 0
        self.hp = 200
        self.game_time = 0  # Time since the start of the beatmap
        self.last_update_time = 0  # Last time the game state was updated
        self.state: States = States.IDLE
        self.mouse: tuple[int, int] = (0, 0)
        self.delta: float = 0
        self.hold = False
        self.curve_to_follow: Optional[Note] = None

        # Initialize Pygame mixer for audio

        pygame.mixer.init()
        self.audio: Optional[pygame.mixer.Sound] = None
        self.audio_start_time = 0

    def start_game(self) -> None:
        self.state = States.HUMAN
        self.last_update_time = time.time()
        self.audio_start_time = time.time()
        if self.audio:
            self.audio.set_volume(0.05)
            self.audio.play()

    def stop_game(self) -> None:
        if self.audio:
            self.audio.stop()
        self.state = States.IDLE

    def load_beatmap(self, file_path: str) -> None:
        self.beatmap = parse_beatmap(file_path)
        self.notes = self.beatmap.notes

        # Load audio file

        audio_path = os.path.join(
            os.path.dirname(file_path), self.beatmap.audio_filename
        )
        if os.path.exists(audio_path):
            self.audio = pygame.mixer.Sound(audio_path)
        else:
            print(f"Warning: Audio file not found at {audio_path}")
        self.reset()

    def step(self, action: "ActionSpace") -> None:
        self.mouse = action.mouse_pos()

        if action.click and not self.hold:
            self.effects.append(e.SplashEffect(position=self.mouse))
            self.effects.append(e.ParticleEffect(position=self.mouse))
            self.check_hit()
            self.hold = True
        if self.hold:
            self.check_curve()
        if not action.click and self.hold:
            self.hold = False
            self.curve_to_follow = None
        self.effects = [effect for effect in self.effects if not effect.is_finished()]
        for effect in self.effects:
            effect.step(self.delta)
        self.upcoming_notes = [
            note for note in self.upcoming_notes if note.time > self.game_time - 200
        ]

        if self.hp <= 0:
            self.stop_game()
        if len(self.upcoming_notes) == 0:
            self.stop_game()
        if self.state == States.HUMAN:
            self.render()
        if self.state == States.TRAIN:
            self.game_time += 1
            self.delta = 1

    def check_hit(self) -> None:
        hit_window = 50  # ms
        for note in self.upcoming_notes:
            distance = math.sqrt(
                (note.x - self.mouse[0]) ** 2 + (note.y - self.mouse[1]) ** 2
            )
            error = abs(note.time - self.game_time)
            if error <= hit_window and distance <= 50:
                self.hit_note(note)
                return
            if error <= hit_window * 2 and distance <= 50:
                self.hit_note(note, 100)
                return
            if error <= hit_window * 3 and distance <= 50:
                self.hit_note(note, 50)
                return
        self.miss()

    def check_curve(self) -> None:
        if self.curve_to_follow is None:
            return
        for note in self.upcoming_notes:
            pass

    def hit_note(self, note: Note, score: int = 300) -> None:
        self.score += score
        self.accuracy = (
            self.accuracy * (len(self.notes) - len(self.upcoming_notes)) + 100
        ) / (len(self.notes) - len(self.upcoming_notes) + 1)
        self.hp = min(200, self.hp + 20)
        self.upcoming_notes.remove(note)

        self.effects.append(e.ScorePopup(position=(note.x, note.y), score=score))

        if note.type_f == NoteType.SLIDER:
            self.effects.append(
                e.SliderEffect(
                    note=note,
                )
            )
            self.curve_to_follow = note

    def miss(self) -> None:
        self.accuracy = (
            self.accuracy * (len(self.notes) - len(self.upcoming_notes))
        ) / (len(self.notes) - len(self.upcoming_notes) + 1)
        self.hp = max(0, self.hp - 10)

    def render(self) -> None:
        self.renderer.render()
        current_time = time.time()
        self.delta = (
            current_time - self.last_update_time
        ) * 1000  # Convert to milliseconds
        self.game_time += self.delta
        self.last_update_time = current_time

    def reset(self) -> None:
        self.upcoming_notes = self.notes.copy()
        self.game_time = 0
        self.last_update_time = time.time()
        self.score = 0
        self.accuracy = 0
        self.hp = 200
        self.last_time = 0
        self.state: States = States.IDLE
        self.effects.clear()

        self.audio_start_time = 0


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
        osu.step(ActionSpace(mouse[0], mouse[1], pressed_keys[0]))
        if osu.state == States.IDLE:
            osu.reset()
            osu.start_game()
