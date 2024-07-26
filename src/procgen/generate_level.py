from typing import Iterator
import random

import tcod

from components import MapComponent
from tiles import floor

from .layouts.rectangular_room import RectangularRoom


def generate_level(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int
) -> MapComponent:
    level_map = MapComponent(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, level_map.width - room_width - 1)
        y = random.randint(0, level_map.height - room_height - 1)

        # "RectangulaRoom" class makes rectangles easier to work with.
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms to see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        level_map.tiles[new_room.inner] = floor

        if len(rooms) != 0: # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                level_map.tiles[x, y] = floor

        # Finally append the new room to the list.
        rooms.append(new_room)

    return level_map

def tunnel_between(
    start: tuple[int, int], end: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5: # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically then
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
