from typing import List, Tuple

import numpy as np # type: ignore
import tcod

from ecs.component import Component
from ecs.entity import Entity
from components.map_component import MapComponent
from components.position_component import PositionComponent
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction


class AI(Component):
    def get_path_to(
            self,
            map_component: MapComponent,
            moving_entity: Entity,
            blocking_entities: List[Entity],
            destination_x: int,
            destination_y: int
    ) -> List[Tuple[int, int]]:
        """
        Get a path from the current position of the moving entity to the given
        destination.

        If there is no valid path returns an empty list.

        :param map_component: The map component for the game world.
        :param moving_entity: The entity seeking a path (owns this AI component).
        :param blocking_entities: A list of entities that block movement.
        :param destination_x: The x coordinate of the target position.
        :param destination_y: The y coordinate of the target position.
        """
        
        # Copy the walkable array.
        cost = np.array(map_component.tiles["walkable"], dtype=np.int8)

        for entity in blocking_entities:
            blocking_entity_position_component = entity.get_component(
                PositionComponent
            )

            # Add to the cost of a blocked position.
            # A lower number means more enemies will crowd behind each other in
            # hallways. A higher number means enemies will take longer paths in
            # order to surround the player.
            cost[(
                blocking_entity_position_component.x,
                blocking_entity_position_component.y
            )] += 10

        # Create a graph from the cost array and pass that graph to a new
        # pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        moving_entity_position_component = moving_entity.get_component(
            PositionComponent
        )

        # Add the current position of the entity as a root node to the 
        # pathfinder.
        pathfinder.add_root((
            moving_entity_position_component.x,
            moving_entity_position_component.y
        ))

        # Compute the path to the destination and remove the starting node.
        path: List[List[int]] = pathfinder.path_to(
            (destination_x, destination_y)
        )[1:].tolist()

        # Convert the list of nodes into a list of coordinates.
        return [(node[0], node[1]) for node in path]
    

class HostileEnemyAI(AI):
    def __init__(self):
        super().__init__()
        self.cached_path: List[Tuple[int, int]] = []

    def move_towards_player_and_attack(
            self,
            map_component: MapComponent,
            acting_entity: Entity,
            player_entity: Entity
    ) -> None:
        player_entity_position_component = player_entity.get_component(
            PositionComponent
        )
        moving_entity_position_component = acting_entity.get_component(
            PositionComponent
        )

        dx = player_entity_position_component.x - moving_entity_position_component.x
        dy = player_entity_position_component.y - moving_entity_position_component.y

        distance = max(abs(dx), abs(dy)) # Chebyshev distance.

        if map_component.visible[moving_entity_position_component.x, moving_entity_position_component.y]:
            if distance <= 1:
                return MeleeAction(acting_entity, dx, dy)
            
            self.cached_path = self.get_path_to(
                player_entity_position_component.x,
                player_entity_position_component.y
            )

        if self.cached_path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                acting_entity,
                dest_x - moving_entity_position_component.x,
                dest_y - moving_entity_position_component.y
            ).perform()
        
        return WaitAction()
