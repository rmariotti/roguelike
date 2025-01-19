from typing_extensions import override

from ecs import EntityManager, Entity
from components import SpeedComponent, DirectionComponent, PositionComponent
from utils import calculate_destination, get_blocking_entities_at_position

from .action import ActionWithDirection


class MeleeAction(ActionWithDirection):
    @override
    def perform(self, world: EntityManager, entity: Entity):
        print("Performing melee action.")
        position_component = entity.get_component(PositionComponent)
        speed_component = entity.get_component(SpeedComponent)
        direction_component = entity.get_component(DirectionComponent)


        dest_x, dest_y = calculate_destination(
            position_component.x,
            position_component.y,
            speed_component.walking_speed,
            self.direction
        )

        targets = get_blocking_entities_at_position(world, dest_x, dest_y)

        if not targets:
            return

        print(f"You kick someone, much to its annoyance!")