import math
from typing import Optional


def perfect_circle(
    vertices: list[tuple[int, int]], numPoints: Optional[int] = None
) -> list[tuple[int, int]]:
    if numPoints is None:
        numPoints = 30
    if numPoints < 2 or len(vertices) != 3:
        raise ValueError("Invalid number of vertices")
    result = []

    b0x = vertices[0][0]
    b0y = vertices[0][1]
    b1x = vertices[1][0]
    b1y = vertices[1][1]
    b2x = vertices[2][0]
    b2y = vertices[2][1]

    centerX = (b0x + b1x + b2x) / 3
    centerY = (b0y + b1y + b2y) / 3

    radius = math.sqrt((b0x - b2x) ** 2 + (b0y - b2y) ** 2) / 2

    initial_angle = math.atan2(b1y - b0y, b1x - b0x)
    result.append(
        (
            int(centerX + math.cos(initial_angle) * radius),
            int(centerY + math.sin(initial_angle) * radius),
        )
    )

    for i in range(numPoints // 2):
        angle = initial_angle + (i * 2 * math.pi / numPoints)
        x = centerX + math.cos(angle) * radius
        y = centerY + math.sin(angle) * radius
        result.append((int(x), int(y)))
    return result
