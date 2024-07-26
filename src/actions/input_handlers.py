from typing import Optional
from typing_extensions import override

import tcod.event

from .escape_action import EscapeAction
from .movement_action import MovementAction
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
            action = MovementAction(direction=Direction.NORTH, speed=1)
        elif key == tcod.event.KeySym.DOWN:
            action = MovementAction(direction=Direction.SOUTH, speed=1)
        elif key == tcod.event.KeySym.LEFT:
            action = MovementAction(direction=Direction.WEST, speed=1)
        elif key == tcod.event.KeySym.RIGHT:
            action = MovementAction(direction=Direction.EAST, speed=1)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
