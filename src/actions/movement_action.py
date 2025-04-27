from typing_extensions import override

from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from utils.ecs_helpers import get_blocking_entities_at_position

from .action import ActionWithDirection


class MovementAction(ActionWithDirection):
    @override
    def perform(self) -> None:
        speed_component = self.entity.get_component(SpeedComponent)
        direction_component = self.entity.get_component(DirectionComponent)

        # Check that the entity is trying to reach a free tile.
        if get_blocking_entities_at_position(self.world, *self.destination_xy):
            return

        speed_component.speed = speed_component.walking_speed
        direction_component.direction = self.direction
