import numpy as np

import tcod

from ecs.system import System
from ecs.world import World
from components.position_component import PositionComponent
from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from components.map_component import MapComponent
from utils.ecs_helpers import get_blocking_entities_at_position
from utils.math_helpers import calculate_destination


class MovementSystem(System):
    """An object containing entity movement logic."""
    def __init__(self, world: World):
        self.world = world

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()
    
    def update(self) -> None:
        map_entities = self.world.get_entities_with_components(
                MapComponent)

        moveable_entities = self.world.get_entities_with_components(
                PositionComponent, SpeedComponent, DirectionComponent)

        for map_entity in map_entities:
            # Get the active map component, to check if the moving entities
            # are moving towards blocked tiles.
            map_component: MapComponent = map_entity.get_component(MapComponent)

            for entity in moveable_entities:
                # Retrieve relevant components.
                speed_component = entity.get_component(SpeedComponent)

                # Check that speed is non-zero.
                if speed_component.speed != 0:
                    direction_component = entity.get_component(
                            DirectionComponent)
                    position_component = entity.get_component(
                            PositionComponent)

                    # Setup tcod pathfinding.
                    graph = tcod.path.CustomGraph(
                            shape=(map_component.width, map_component.height),
                            order="F"
                    )
                    graph.add_edges(
                            edge_map=direction_component.direction.edge_map,
                            cost=map_component.tiles["walkable"].astype(int)
                    )
                    pathfinder = tcod.path.Pathfinder(graph)
                    pathfinder.add_root(
                            (position_component.x, position_component.y))
                    pathfinder.resolve()

                    # Check that the point of arrival is reachable.
                    arrival_x, arrival_y = calculate_destination(
                        position_component.x,
                        position_component.y,
                        speed_component.walking_speed,
                        direction_component.direction
                    )
                    
                    if (
                        pathfinder.distance[arrival_x][arrival_y] != np.iinfo(pathfinder.distance.dtype).max and
                        get_blocking_entities_at_position(self.world, arrival_x, arrival_y) is None
                    ): 
                        # Update entity position.
                        position_component.x = arrival_x
                        position_component.y = arrival_y

                    # Stop the entity after movement.
                    speed_component.speed = 0
