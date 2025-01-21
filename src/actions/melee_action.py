from typing_extensions import override

from .action import ActionWithDirection


class MeleeAction(ActionWithDirection):
    @override
    def perform(self):
        targets = self.blocking_entities

        if not targets:
            return

        for target in targets:
            print(f"You kick {target.name}, much to its annoyance!")