from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OsuPy import OsuPy


class Render:
    def __init__(self, parent: "OsuPy") -> None:
        self.parent = parent
