from math import sin, cos

from .direction_enum import Direction


def calculate_destination(
        starting_x: int, starting_y: int, speed: int, direction: Direction
) -> tuple[int, int]:
    """Compute final position of a moving entity using speed and direction."""
    dx = round(speed * cos(direction.radians))
    dy = round(speed * sin(direction.radians))

    return (starting_x + dx, starting_y + dy)
