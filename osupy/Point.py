from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def get_virtual_x(self) -> int:
        return self.x + 80

    def get_virtual_y(self) -> int:
        return self.y + 80

    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y

    @staticmethod
    def from_string(string: str) -> "Point":
        x = int(string.split(":")[0])
        y = int(string.split(":")[1])
        return Point(x, y)
