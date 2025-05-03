from __future__ import annotations

from typing import TYPE_CHECKING

from tcod import event

from ecs.system import System
from components.is_player_character_tag import IsPlayerCharacterTag
from actions.event_handler import EventHandler

if TYPE_CHECKING:
    from systems.action_system import ActionSystem
    from ecs.entity import Entity


class TurnSystem(System):
    """Handles tcod event loop and performing actions on acting entities."""
    def __init__(
            self, action_system: ActionSystem, event_handler: EventHandler
    ):
        self.action_system = action_system
        self.event_handler = event_handler

    def update(self) -> None:
        if not self.action_system.has_ready_actor():
            return
        
        acting_entity = self.action_system.pop_ready_actor()

        # Handle player character action.
        if acting_entity.get_component(IsPlayerCharacterTag):
            # Wait for player input.
            for tcod_event in event.wait():
                action = self.event_handler.dispatch(tcod_event)

                if action is not None:
                    action.perform()
                    break

        # Handle entity AI action.
        else:
            action = self.get_ai_action(acting_entity)
            if action:
                action.perfrom(acting_entity)

    def get_ai_action(self, entity: Entity):
        # TODO: Get AI action from entity.
        pass