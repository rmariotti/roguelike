from typing_extensions import override

from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from components.position_component import PositionComponent
from components.map_component import MapComponent
from exceptions.action_exceptions import ImpossibleAction
from utils.ecs_helpers import get_blocking_entities_at_position
from utils.movement_helpers import is_move_valid

from .action import ActionWithDirection


class MovementAction(ActionWithDirection):
    @override
    def perform(self) -> None:
        # Get all components needed for entity movement.
        speed_component = self.entity.get_component(SpeedComponent)
        direction_component = self.entity.get_component(DirectionComponent)
        position_component = self.entity.get_component(PositionComponent)

        # TODO: In ordere to support multiple maps, a relation between
        # position components and a map component is needed. <RM, 21-05-2025>
        map_component = next(
            iter(self.world.get_components(MapComponent)), None
        )

        # Check that the entity has all required components for movement.
        if not (
            speed_component and
            direction_component and
            position_component and
            map_component
        ):
            raise RuntimeError(
                "Entity does not have required components for movement."
            )

        # Check that the entity is trying to reach a free tile.
        if get_blocking_entities_at_position(self.world, *self.destination_xy):
            raise ImpossibleAction("The way is blocked.")

        # Check if the entity can actually move in the given direction.
        if not is_move_valid(
            world=self.world,
            x=position_component.x,
            y=position_component.y,
            direction=self.direction,
            speed=speed_component.walking_speed,
            map_component=map_component
        ):
            raise ImpossibleAction("The entity cannot move in that direction.")

        # Set entity speed and direction so the movement system ca move it.
        speed_component.speed = speed_component.walking_speed
        direction_component.direction = self.direction
