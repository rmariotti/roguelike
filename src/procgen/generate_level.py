from typing import Iterator
import random

import tcod

from ecs import EntityManager
from components import MapComponent
from tiles import floor
from components import PositionComponent

from .generate_monster import generate_monster, MonsterType
from .layouts.rectangular_room import RectangularRoom


def generate_level(
        world: EntityManager,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int
) -> MapComponent:
    """Builds a game level of interconnected rectangular rooms."""
    level_map = MapComponent(map_width, map_height)

    rooms: list[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, level_map.width - room_width - 1)
        y = random.randint(0, level_map.height - room_height - 1)

        # RectangulaRoom class makes rectangles easier to work with.
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms to see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        level_map.tiles[new_room.inner] = floor

        place_entities(world, new_room, 2)

        if len(rooms) != 0: # All rooms after the first.
            # Dig out a corridor between this room and the previous one.
            for x, y in corridor_between(rooms[-1].center, new_room.center, 2):
                level_map.tiles[x, y] = floor

        # Finally append the new room to the list.
        rooms.append(new_room)

    return level_map


def corridor_between(
        start: tuple[int, int], end: tuple[int, int], width: int
) -> Iterator[tuple[int, int]]:
    """Return an L-shaped corridor between two points."""
    x1, y1 = start
    x2, y2 = end

    start_to_corner_enlarge_direction: tuple[int, int] = (0, 0)
    corner_to_end_enlarge_direction: tuple[int, int] = (0, 0)

    if random.random() < 0.5: # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1

        # Calculate in what direction the corridor can grow in width.
        if x1 > x2:
            corner_to_end_enlarge_direction = (1, 0)
        else:
            corner_to_end_enlarge_direction = (-1, 0)
        if y1 > y2:
            start_to_corner_enlarge_direction = (0, 1)
        else:
            start_to_corner_enlarge_direction = (0, -1)
    else:
        # Move vertically, then horizzontally.
        corner_x, corner_y = x1, y2

        # Calculate in what direction the corridor can grow in width.
        if x1 > x2:
            start_to_corner_enlarge_direction = (-1, 0)
        else:
            start_to_corner_enlarge_direction = (1, 0)
        if y1 > y2:
            corner_to_end_enlarge_direction = (0, -1)
        else:
            corner_to_end_enlarge_direction = (0, 1)

    # Generate the coordinates for this tunnel.
    # Fist line: from start to corner.
    for x, y in enlarge_corridor(
            tcod.los.bresenham((x1, y1), (corner_x, corner_y)),
            start_to_corner_enlarge_direction, width):
        yield x, y

    # Second line: from conrner to end.
    for x, y in enlarge_corridor(
            tcod.los.bresenham((corner_x, corner_y), (x2, y2)),
            corner_to_end_enlarge_direction, width):
        yield x, y


def enlarge_corridor(
        line: Iterator[tuple[int, int]], direction: tuple[int, int], width: int
) -> Iterator[tuple[int, int]]:
    """Increase corridor width."""
    for width_step in range(width):
        for x, y in line.tolist():
            yield x + width_step*direction[0], y + width_step*direction[1]


def place_entities(
        world: EntityManager, room: RectangularRoom, maximum_enemies: int,
) -> None:
    number_of_enemies = random.randint(0, maximum_enemies)

    for i in range(number_of_enemies):
        # Generate a random point inside the room to spawn the enemy.
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        # TODO: Remove highly inefficent code.
        is_tile_free = not any(
            entity.get_component(PositionComponent).x == x and 
            entity.get_component(PositionComponent).y == y 
            for entity in world.get_entities_with_components(PositionComponent)
        )

        if is_tile_free:
            # Enemy spawn table.
            if random.random() < 0.8:
                world.entities.append(
                    generate_monster(MonsterType.LARVA, position=(x, y)))
            else:
                world.entities.append(
                    generate_monster(MonsterType.ADULT, position=(x, y)))
