from __future__ import annotations

from typing import TYPE_CHECKING
from functools import partial

import tcod.event

from actions.escape_action import EscapeAction
from actions.bump_action import BumpAction
from actions.wait_action import WaitAction
from actions.message_log_history_actions import (
    OpenMessageLogHistory, CloseMessageLogHistory,
    MessageLogHistoryGoEnd, MessageLogHistoryGoHome,
    MessageLogHistoryMove
)
from actions.pickup_action import PickupAction
from actions.inventory_actions import OpenInventory, CloseInventory
from utils.direction_enum import Direction
from inputs.input_modes import InputModes

if TYPE_CHECKING:
    from ecs.world import World
    from ecs.entity import Entity
    from inputs.input_action_mapper import InputActionMapper


MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: Direction.NORTH,
    tcod.event.KeySym.DOWN: Direction.SOUTH,
    tcod.event.KeySym.LEFT: Direction.WEST,
    tcod.event.KeySym.RIGHT: Direction.EAST,
    tcod.event.KeySym.HOME: Direction.NORTH_WEST,
    tcod.event.KeySym.END: Direction.SOUTH_WEST,
    tcod.event.KeySym.PAGEUP: Direction.NORTH_EAST,
    tcod.event.KeySym.PAGEDOWN: Direction.SOUTH_EAST,
    # Numpad keys.
    tcod.event.KeySym.KP_1: Direction.SOUTH_WEST,
    tcod.event.KeySym.KP_2: Direction.SOUTH,
    tcod.event.KeySym.KP_3: Direction.SOUTH_EAST,
    tcod.event.KeySym.KP_4: Direction.WEST,
    tcod.event.KeySym.KP_6: Direction.EAST,
    tcod.event.KeySym.KP_7: Direction.NORTH_WEST,
    tcod.event.KeySym.KP_8: Direction.NORTH,
    tcod.event.KeySym.KP_9: Direction.NORTH_EAST,
    # Vi keys.
    tcod.event.KeySym.h: Direction.WEST,
    tcod.event.KeySym.j: Direction.SOUTH,
    tcod.event.KeySym.k: Direction.NORTH,
    tcod.event.KeySym.l: Direction.EAST,
    tcod.event.KeySym.y: Direction.NORTH_WEST,
    tcod.event.KeySym.u: Direction.NORTH_EAST,
    tcod.event.KeySym.b: Direction.SOUTH_WEST,
    tcod.event.KeySym.n: Direction.SOUTH_EAST
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR
}

CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -10,
    tcod.event.KeySym.PAGEDOWN: 10,
}


def setup_input_bindings(
        mapper: InputActionMapper,
        world: World,
        player: Entity
):
    """
    Registers all input bindings for different input modes.
    """
    # Initialize input modes.
    for input_mode in InputModes:
        mapper.initialize_mode(input_mode)

    # === DEFAULT MODE ===
    # Movement keys → BumpAction.
    for key, direction in MOVE_KEYS.items():
        mapper.register_game(
            InputModes.DEFAULT,
            key,
            partial(BumpAction, entity=player, world=world, direction=direction)
        )

    # Wait keys → WaitAction.
    for key in WAIT_KEYS:
        mapper.register_game(
            InputModes.DEFAULT,
            key,
            partial(WaitAction, entity=player, world=world)
        )

    # Open message log view.
    mapper.register_ui(
        InputModes.DEFAULT,
        tcod.event.KeySym.v,
        partial(OpenMessageLogHistory, entity=player, world=world)
    )

    # ESC → Exit the game or cancel.
    mapper.register_ui(
        InputModes.DEFAULT,
        tcod.event.KeySym.ESCAPE,
        partial(EscapeAction, entity=player, world=world)
    )

    # 'g' key → Pickup item action.
    mapper.register_game(
        InputModes.DEFAULT,
        tcod.event.KeySym.g,
        partial(PickupAction, entity=player, world=world)
    )

    # === LOG_VIEW MODE ===
    # Close log view.
    for key in (tcod.event.KeySym.x, tcod.event.KeySym.ESCAPE):
        mapper.register_ui(
            InputModes.LOG_VIEW,
            key,
            partial(CloseMessageLogHistory, entity=player, world=world)
        )

    # Scroll to start/end of log.
    mapper.register_ui(
        InputModes.LOG_VIEW,
        tcod.event.KeySym.HOME,
        partial(MessageLogHistoryGoHome, entity=player, world=world)
    )

    mapper.register_ui(
        InputModes.LOG_VIEW,
        tcod.event.KeySym.END,
        partial(MessageLogHistoryGoEnd, entity=player, world=world)
    )

    # Scroll message log cursor up/down.
    for key, adjust in CURSOR_Y_KEYS.items():
        mapper.register_ui(
            InputModes.LOG_VIEW,
            key,
            partial(MessageLogHistoryMove, entity=player, world=world, adjust=adjust)
        )

    # === INVENTORY MODE ===
    mapper.register_ui(
        InputModes.DEFAULT,
        tcod.event.KeySym.i,
        partial(OpenInventory, entity=player, world=world)
    )
