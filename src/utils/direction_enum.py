from enum import Enum
from math import pi


class Direction(Enum):
    """Cardinal and intercardinal directions map to integers."""
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj.__value__ = value
        return obj

    def __init__(self, id_: int, radians: float):
        self.id_ = id_
        self.radians = radians

    # Cardinal directions.
    NORTH = 0, float(3/2*pi)
    EAST = 1, float(0)
    SOUTH = 2, float(pi/2)
    WEST = 3, float(pi)

    # Intercardinal directions.
    NORTH_EAST = 4, float(7/4*pi)
    SOUTH_EAST = 5, float(1/4*pi)
    SOUTH_WEST = 6, float(3/4*pi)
    NORTH_WEST = 7, float(5/4*pi)

    # Secondary intercardinal directions.
    NORTH_NORTH_EAST = 8, float(15/8*pi)
    EAST_NORTH_EAST = 9, float(1/8*pi)
    EAST_SOUTH_EAST = 10, float(3/8*pi)
    SOUTH_SOUTH_EAST = 11, float(5/8*pi)
    SOUTH_SOUTH_WEST = 12, float(7/8*pi)
    WEST_SOUTH_WEST = 13, float(9/8*pi)
    WEST_NORTH_WEST = 14, float(11/8*pi)
    NORTH_NORTH_WEST = 15, float(13/8*pi)
