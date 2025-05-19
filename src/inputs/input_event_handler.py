from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from typing_extensions import override

import tcod.event

from actions.action import Action

from components.is_player_character_tag import IsPlayerCharacterTag
from components.map_component import MapComponent
from components.ui_mouse_location_component import UIMouseLocationComponent
from utils.ecs_helpers import get_default_component

if TYPE_CHECKING:
    from ecs.world import World
    from ecs.entity import Entity


class InputEventHandler(tcod.event.EventDispatch[Action]):
    """Handles input events and maps key presses to actions in the game."""
    def __init__(self, world: World):
        self.world = world
        self.player = self._get_player()
        # tcod key event to action mapping.
        self.key_action_map: dict[tcod.event.KeySym, Action] = {}

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


class UIInputEventHandler(InputEventHandler):
    """Handles inputs and maps keys to actions with effects on game ui."""
    def __init__(self, world: World):
        super().__init__(world)
