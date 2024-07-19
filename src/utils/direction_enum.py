from enum import Enum


class Direction(Enum):
    """
    Cardinal and intercardinal directions map to integers.
    """
    # Cardinal directions.
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Intercardinal directions.
    NORTH_EAST = 4
    SOUTH_EAST = 5
    SOUTH_WEST = 6
    NORTH_WEST = 7

    # Secondary intercardinal directions.
    NORTH_NORTH_EAST = 8
    EAST_NORTH_EAST = 9
    EAST_SOUTH_EAST = 10
    SOUTH_SOUTH_EAST = 11
    SOUTH_SOUTH_WEST = 12
    WEST_SOUTH_WEST = 13
    WEST_NORTH_WEST = 14
    NORTH_NORTH_WEST = 15
