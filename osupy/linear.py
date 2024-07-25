def linear(points: list[tuple[int, int]], length: int) -> list[tuple[int, int]]:
    if len(points) < 2:
        return points
    result = []
    for i in range(len(points) - 1):
        result.append((points[i][0], points[i][1]))
        for j in range(1, length):
            result.append(
                (
                    points[i][0] + (points[i + 1][0] - points[i][0]) * j / length,
                    points[i][1] + (points[i + 1][1] - points[i][1]) * j / length,
                )
            )
    result.append(points[-1])
    return result
