from abc import ABC

from ecs import Entity


class Action(ABC):
    def perform(self, entity: Entity) -> None:
        raise NotImplementedError()
