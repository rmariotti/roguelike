from typing_extensions import override

from .action import Action


class EscapeAction(Action):
    @override
    def perform(self) -> None:
        raise SystemExit()
