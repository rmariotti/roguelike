from __future__ import annotations

from typing import TYPE_CHECKING

from tcod import event

from components.is_player_character_tag import IsPlayerCharacterTag
from actions.event_handler import EventHandler

if TYPE_CHECKING:
    from ecs.entity_manager import EntityManager


class EventSystem:
    """System handling tcod events by performing actions."""
    def __init__(
            self, entity_manager: EntityManager, event_handler: EventHandler
    ):
        self.entity_manager = entity_manager
        self.event_handler = event_handler

    def update(self) -> None:
        player_character_entities = (
            self.entity_manager.get_entities_with_components(IsPlayerCharacterTag)
        )

        for tcod_event in event.wait():
            action = self.event_handler.dispatch(tcod_event)

            if action is not None:
                for player_character_entity in player_character_entities:
                    action.perform()
