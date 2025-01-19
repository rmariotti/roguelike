from abc import ABC
from typing_extensions import override

from ecs import Entity, EntityManager
from utils import Direction


class Action(ABC):
    def perform(self, world: EntityManager, entity: Entity) -> None:
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, direction: Direction):
        super().__init__()

        self.direction = direction

    @override
    def perform(self, world: EntityManager, entity: Entity) -> None:
        raise NotImplementedError()
