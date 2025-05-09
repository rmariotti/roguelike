from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

from ecs.system import System
from ecs.world import World
from actions.input_event_handler import UIInputEventHandler
from components.is_player_character_tag import IsPlayerCharacterTag

if TYPE_CHECKING:
    from systems.tcod_event_dispatch_system import EventDispatchSystem


class UiInputSystem(System):
    def __init__(
            self, world: World, event_handler: UIInputEventHandler,
            event_dispatcher: EventDispatchSystem
    ):
        super().__init__()
        self.world: World = world
        self.event_handler: UIInputEventHandler = event_handler
        self.event_dispatcher: EventDispatchSystem = event_dispatcher

    @override
    def start(self):
        return super().start()

    @override
    def stop(self):
        return super().stop()

    @override
    def update(self):
        super().update()

        player_entity = self.world.get_entities_with_components(
            IsPlayerCharacterTag
        )

        if player_entity:
            for tcod_event in self.event_dispatcher.get_events():
                action = self.event_handler.dispatch(tcod_event)

                if action:
                    action.perform()
                    break
