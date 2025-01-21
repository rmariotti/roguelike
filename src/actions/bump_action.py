from typing_extensions import override

from .action import ActionWithDirection
from .melee_action import MeleeAction
from .movement_action import MovementAction


class BumpAction(ActionWithDirection):
    @override
    def perform(self) -> None:
        if self.blocking_entities:
            return MeleeAction(
                entity=self.entity, world=self.world, direction=self.direction
            ).perform()

        else:
            return MovementAction(
                entity=self.entity, world=self.world, direction=self.direction
            ).perform()
