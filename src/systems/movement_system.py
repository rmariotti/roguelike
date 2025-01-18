from math import sin, cos
import numpy as np
from typing import Optional, Iterable

import tcod

from ecs import EntityManager
from components import (
    PositionComponent,
    SpeedComponent,
    DirectionComponent,
    MapComponent,
    IsBlockingTag
)

from ecs import Entity


class MovementSystem:
    """An object containing entity movement logic."""
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager
    
    def update(self) -> None:
        map_entities = self.entity_manager.get_entities_with_components(
                MapComponent)

        moveable_entities = self.entity_manager.get_entities_with_components(
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

                    # Calculate position delta using speed and direction.
                    dx = round(speed_component.speed * 
                               cos(direction_component.direction.radians))
                    dy = round(speed_component.speed *
                               sin(direction_component.direction.radians))

                    # Check that the point of arrival is reachable.
                    arrival_x, arrival_y = (position_component.x + dx,
                                            position_component.y + dy)
                    
                    if (
                        pathfinder.distance[arrival_x][arrival_y] != np.iinfo(pathfinder.distance.dtype).max and
                        self.get_blocking_entities_at_position(arrival_x, arrival_y) is None
                    ): 
                        # Update entity position.
                        position_component.x += dx
                        position_component.y += dy

                    # Stop the entity after movement.
                    speed_component.speed = 0

    def get_blocking_entities_at_position(
            self, x: int, y: int
    ) -> Optional[Iterable[Entity]]:
        blocking_entities = self.entity_manager.get_entities_with_components(
            PositionComponent, IsBlockingTag
        )
        
        blocking_entities_at_position = [
            entity
            for entity in blocking_entities
            if (
                (position := entity.get_component(PositionComponent)) and
                (position.x, position.y) == (x, y)
            )
        ]

        return (
            blocking_entities_at_position
            if blocking_entities_at_position
            else None
        )
