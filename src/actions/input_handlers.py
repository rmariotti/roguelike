from typing import Optional
from typing_extensions import override

import tcod.event

from .escape_action import EscapeAction
from .bump_action import BumpAction
from .action import Action
from utils import Direction


class EventHandler(tcod.event.EventDispatch[Action]):
    @override
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    @override
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP:
            action = BumpAction(direction=Direction.NORTH)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(direction=Direction.SOUTH)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(direction=Direction.WEST)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(direction=Direction.EAST)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
