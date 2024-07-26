from typing_extensions import override

from .action import Action
from ecs import Entity


class EscapeAction(Action):
    @override
    def perform(self, entity: Entity) -> None:
        raise SystemExit()
