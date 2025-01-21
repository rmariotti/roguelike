from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from typing_extensions import override

import tcod.event

from .escape_action import EscapeAction
from .bump_action import BumpAction
from .action import Action
from components import IsPlayerCharacterTag
from utils import Direction

if TYPE_CHECKING:
    from ecs import EntityManager, Entity


class EventHandler(tcod.event.EventDispatch[Action]):
    """Handles input events and maps key presses to actions in the game."""
    def __init__(self, world: EntityManager):
        self.world = world
        self.player = self._get_player()

        # tcod key event to action mapping.
        self.key_action_map = {
            tcod.event.KeySym.UP: BumpAction(
                self.player, self.world, direction=Direction.NORTH),
            tcod.event.KeySym.DOWN: BumpAction(
                self.player, self.world, direction=Direction.SOUTH),
            tcod.event.KeySym.LEFT: BumpAction(
                self.player, self.world, direction=Direction.WEST),
            tcod.event.KeySym.RIGHT: BumpAction(
                self.player, self.world, direction=Direction.EAST),
            tcod.event.KeySym.ESCAPE: EscapeAction(self.player, self.world),
        }

    def _get_player(self) -> Entity:
        player_entities = self.world.get_entities_with_components(
            IsPlayerCharacterTag)
        if player_entities:
            return player_entities[0]
        else:
            raise ValueError("Player entity not found.")

    @override
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    @override
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # Usa la mappa per trovare l'azione in base al tasto
        return self.key_action_map.get(event.sym, None)
