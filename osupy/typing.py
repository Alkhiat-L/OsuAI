from typing import Tuple, TypedDict

import numpy as np
import numpy.typing as npt


class NoteType(TypedDict):
    x: float
    y: float
    time: float
    type: int


class ObservationType(TypedDict):
    game_time: np.int32
    x: np.float32
    y: np.float32
    upcoming_notes: Tuple[NoteType, NoteType, NoteType, NoteType, NoteType]
    curve: npt.NDArray[np.float32]


class ActionType(TypedDict):
    x: npt.NDArray[np.float32]
    y: npt.NDArray[np.float32]
    click: npt.NDArray[np.float32]
