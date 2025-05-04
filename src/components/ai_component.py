from __future__ import annotations

from typing import Optional, List, Tuple, TYPE_CHECKING
from typing_extensions import override
from abc import abstractmethod

import numpy as np # type: ignore
import tcod

from ecs.component import Component
from ecs.entity import Entity
from ecs.world import World
from components.map_component import MapComponent
from components.position_component import PositionComponent
from components.is_player_character_tag import IsPlayerCharacterTag
from components.is_blocking_tag import IsBlockingTag
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from utils.direction_enum import Direction

if TYPE_CHECKING:
    from actions.action import Action


class AIComponent(Component):
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

    @abstractmethod
    def get_action(
            self,
            world: World,
            acting_entity: Entity
    ) -> Action | None:
        raise NotImplementedError()
    

class HostileEnemyAIComponent(AIComponent):
    def __init__(self):
        super().__init__()
        self.cached_path: List[Tuple[int, int]] = []

    def move_towards_player_and_attack(
            self,
            world: World,
            map_component: MapComponent,
            acting_entity: Entity,
            player_entity: Entity
    ) -> Action:
        player_entity_position_component = player_entity.get_component(
            PositionComponent
        )
        moving_entity_position_component = acting_entity.get_component(
            PositionComponent
        )

        dx = player_entity_position_component.x - moving_entity_position_component.x
        dy = player_entity_position_component.y - moving_entity_position_component.y

        distance = max(abs(dx), abs(dy)) # Chebyshev distance.

        print("Distance: {0}".format(distance))

        if map_component.visible[moving_entity_position_component.x, moving_entity_position_component.y]:
            if distance <= 1:
                return MeleeAction(
                    world=world,
                    entity=acting_entity,
                    direction=Direction.from_movement_delta(dx, dy)
                )
            
            self.cached_path = self.get_path_to(
                blocking_entities=world.get_entities_with_components(IsBlockingTag),
                map_component=map_component,
                moving_entity=acting_entity,
                destination_x=player_entity_position_component.x,
                destination_y=player_entity_position_component.y
            )

            print("Path: {0}".format(self.cached_path))

        if self.cached_path:
            dest_x, dest_y = self.cached_path.pop(0)

            print("Destination: {0}, {1}".format(dest_x, dest_y))

            direction: Direction = Direction.from_movement_delta(
                dest_x - moving_entity_position_component.x,
                dest_y - moving_entity_position_component.y
            )

            print("Direction: {0}".format(direction))

            return MovementAction(
                world=world,
                entity=acting_entity,
                direction=direction
            )
        
        return WaitAction(world=world, entity=acting_entity)

    @override
    def get_action(
            self,
            world: World,
            acting_entity: Entity
    ) -> Optional[Action]:
        map_entities = world.get_entities_with_components(MapComponent)
        player_enties = world.get_entities_with_components(IsPlayerCharacterTag)

        if map_entities and player_enties:
            map_component: MapComponent = map_entities[0].get_component(MapComponent)
            player_entity: Entity = player_enties[0]

            return self.move_towards_player_and_attack(
                world=world,
                map_component=map_component,
                acting_entity=acting_entity,
                player_entity=player_entity
            )
        else:
            return None
