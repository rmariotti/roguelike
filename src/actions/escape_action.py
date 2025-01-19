from typing_extensions import override

from .action import Action
from ecs import Entity, EntityManager


class EscapeAction(Action):
    @override
    def perform(self, world: EntityManager, entity: Entity) -> None:
        raise SystemExit()
