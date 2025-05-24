from math import sin, cos

import tcod
import numpy as np

from ecs.world import World
from components.map_component import MapComponent
from utils.ecs_helpers import get_blocking_entities_at_position
from .direction_enum import Direction


def calculate_destination(
        starting_x: int, starting_y: int, speed: int, direction: Direction
) -> tuple[int, int]:
    """Compute final position of a moving entity using speed and direction."""
    dx = round(speed * cos(direction.radians))
    dy = round(speed * sin(direction.radians))

    return (starting_x + dx, starting_y + dy)


def is_move_valid(
        world: World, x: int, y: int, direction, speed: int,
        map_component: MapComponent
) -> bool:
    arrival_x, arrival_y = calculate_destination(x, y, speed, direction)

    graph = tcod.path.CustomGraph(
        shape=(map_component.width, map_component.height), order="F"
    )
    graph.add_edges(
        edge_map=direction.edge_map,
        cost=map_component.tiles["walkable"].astype(int)
    )
    pathfinder = tcod.path.Pathfinder(graph)
    pathfinder.add_root((x, y))
    pathfinder.resolve()

    max_distance = np.iinfo(pathfinder.distance.dtype).max
    distance = pathfinder.distance[arrival_x][arrival_y]
    blocking_entities = get_blocking_entities_at_position(
        world, arrival_x, arrival_y
    )

    return distance != max_distance and not blocking_entities
