from typing_extensions import override

from ecs import Entity, EntityManager
from components import SpeedComponent, DirectionComponent, PositionComponent
from utils import (
    Direction,
    get_blocking_entities_at_position,
    calculate_destination
)

from .action import ActionWithDirection


class MovementAction(ActionWithDirection):
    def __init__(self, direction: Direction):
        super().__init__(direction)

        self.direction = direction

    @override
    def perform(self, world: EntityManager, entity: Entity) -> None:
        print("Performing movement action.")
        position_component = entity.get_component(PositionComponent)
        speed_component = entity.get_component(SpeedComponent)
        direction_component = entity.get_component(DirectionComponent)

        # Check that the entity is trying to reach a free tile.
        dest_x, dest_y = calculate_destination(
            position_component.x,
            position_component.y,
            speed_component.walking_speed,
            self.direction
        )

        if get_blocking_entities_at_position(world, dest_x, dest_y):
            return

        speed_component.speed = speed_component.walking_speed
        direction_component.direction = self.direction
