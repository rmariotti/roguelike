from typing_extensions import override

from actions import Action
from ecs import Entity
from components import SpeedComponent, DirectionComponent
from utils import Direction


class MovementAction(Action):
    def __init__(self, direction: Direction, speed: int):
        super().__init__()

        self.direction = direction
        self.speed = speed

    @override
    def perform(self, entity: Entity) -> None:
        speed_component = entity.get_component(SpeedComponent)
        direction_component = entity.get_component(DirectionComponent)

        speed_component.speed = self.speed
        direction_component.direction = self.direction
