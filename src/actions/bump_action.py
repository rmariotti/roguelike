from typing_extensions import override

from ecs import Entity, EntityManager
from components import SpeedComponent, DirectionComponent, PositionComponent
from utils import (
    get_blocking_entities_at_position,
    calculate_destination
)

from .action import ActionWithDirection
from .melee_action import MeleeAction
from .movement_action import MovementAction


class BumpAction(ActionWithDirection):
    @override
    def perform(self, world: EntityManager, entity: Entity) -> None:
        position_component = entity.get_component(PositionComponent)
        speed_component = entity.get_component(SpeedComponent)

        dest_x, dest_y = calculate_destination(
            position_component.x,
            position_component.y,
            speed_component.walking_speed,
            self.direction
        )

        if get_blocking_entities_at_position(world, dest_x, dest_y):
            return MeleeAction(self.direction).perform(
                world, entity)

        else:
            return MovementAction(self.direction).perform(
                world, entity)
