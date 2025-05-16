from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from typing_extensions import override

import tcod.event

from actions.escape_action import EscapeAction
from actions.bump_action import BumpAction
from actions.wait_action import WaitAction
from actions.action import Action
from components.is_player_character_tag import IsPlayerCharacterTag
from components.map_component import MapComponent
from components.ui_mouse_location_component import UIMouseLocationComponent
from utils.direction_enum import Direction
from utils.ecs_helpers import get_default_component

if TYPE_CHECKING:
    from ecs.world import World
    from ecs.entity import Entity


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


class InputEventHandler(tcod.event.EventDispatch[Action]):
    """Handles input events and maps key presses to actions in the game."""
    def __init__(self, world: World):
        self.world = world
        self.player = self._get_player()
        # tcod key event to action mapping.
        self.key_action_map = {}

    def _get_player(self) -> Entity:
        player_entities = self.world.get_entities_with_components(
            IsPlayerCharacterTag)
        if player_entities:
            return player_entities[0]
        else:
            raise ValueError("Player entity not found.")

    def _get_map_component(self) -> MapComponent:
        map_entities = self.world.get_entities_with_components(
            MapComponent
        )

        if map_entities:
            map_component = map_entities[0].get_component(MapComponent)

        if map_component:
            return map_component

        raise ValueError("Map component not found.")

    def _get_mouse_component(self) -> UIMouseLocationComponent:
        mouse_component = get_default_component(
            world=self.world,
            component_type=UIMouseLocationComponent
        )

        if not mouse_component:
            raise ValueError("Mouse component not found.")

        return mouse_component

    @override
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    @override
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        return self.key_action_map.get(event.sym, None)

    @override
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        # Check that the mouse is hovering on map and update mouse location.
        map_component = self._get_map_component()

        if (
            event.tile.x < map_component.width and
            event.tile.y < map_component.height
        ):
            self._get_mouse_component().position = (event.tile.x, event.tile.y)


class GameInputEventHandler(InputEventHandler):
    """Handles input events and maps keys to actions with in game effects."""
    def __init__(self, world: World):
        super().__init__(world)

        for key, direction in MOVE_KEYS.items():
            self.key_action_map[key] = BumpAction(
                entity=self.player, world=self.world, direction=direction
            )

        for key in WAIT_KEYS:
            self.key_action_map[key] = WaitAction(
                entity=self.player, world=self.world
            )


class UIInputEventHandler(InputEventHandler):
    """Handles inputs and maps keys to actions with effects on game ui."""
    def __init__(self, world: World):
        super().__init__(world)

        self.key_action_map[tcod.event.KeySym.ESCAPE] = EscapeAction(
            entity=self.player, world=self.world
        )
