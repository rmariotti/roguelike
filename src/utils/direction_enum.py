from enum import Enum
from math import pi


class Direction(Enum):
    """Cardinal and intercardinal directions map to integers."""
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj.__value__ = value
        return obj

    def __init__(self, id_: int, radians: float, edge_map: list):
        self.id_ = id_
        self.radians = radians
        self.edge_map = edge_map

    @classmethod
    def from_movement_delta(cls, delta_x: int, delta_y: int):
        # TODO: Extend this to support non unitary movement. <RM, 2025-05-04>
        if delta_x == 0 and delta_y > 0:
            return Direction.SOUTH
        elif delta_x == 0 and delta_y < 0:
            return Direction.NORTH
        elif delta_x > 0 and delta_y == 0:
            return Direction.EAST
        elif delta_x > 0 and delta_y > 0:
            return Direction.SOUTH_EAST
        elif delta_x > 0 and delta_y < 0:
            return Direction.NORTH_EAST
        elif delta_x < 0 and delta_y == 0:
            return Direction.WEST
        elif delta_x < 0 and delta_y > 0:
            return Direction.SOUTH_WEST
        elif delta_x < 0 and delta_y < 0:
            return Direction.NORTH_WEST
        else:
            raise ValueError("Unable to parse direction.")

    # Cardinal directions.
    NORTH = 0, float(3/2*pi),[
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
    ]
    EAST = 1, float(0), [
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 0],
    ]
    SOUTH = 2, float(pi/2), [
            [0, 0, 0],
            [0, 0, 0],
            [0, 1, 0],
    ]
    WEST = 3, float(pi), [
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
    ]

    # Intercardinal directions.
    NORTH_EAST = 4, float(7/4*pi), [
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
    ]
    SOUTH_EAST = 5, float(1/4*pi), [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1],
    ]
    SOUTH_WEST = 6, float(3/4*pi), [
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
    ]
    NORTH_WEST = 7, float(5/4*pi), [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
    ]

    # Secondary intercardinal directions.
    NORTH_NORTH_EAST = 8, float(15/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    EAST_NORTH_EAST = 9, float(1/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    EAST_SOUTH_EAST = 10, float(3/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    SOUTH_SOUTH_EAST = 11, float(5/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    SOUTH_SOUTH_WEST = 12, float(7/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    WEST_SOUTH_WEST = 13, float(9/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    WEST_NORTH_WEST = 14, float(11/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]
    NORTH_NORTH_WEST = 15, float(13/8*pi), [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
    ]

