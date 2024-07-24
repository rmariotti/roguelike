from typing_extensions import override
from abc import ABC

from ecs import Entity
from components import SpeedComponent, DirectionComponent 
from utils import Direction


class Action(ABC):
    def perform(self, entity: Entity) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    @override
    def perform(self, entity: Entity) -> None:
        raise SystemExit()


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
