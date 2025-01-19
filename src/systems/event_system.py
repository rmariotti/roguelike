from tcod import event

from ecs import EntityManager
from components import IsPlayerCharacterTag

from actions import EventHandler


class EventSystem:
    """System handling tcod events performing actions."""
    def __init__(self, entity_manager: EntityManager,
                 event_handler: EventHandler):
        self.entity_manager = entity_manager
        self.event_handler = event_handler

    def update(self) -> None:
        player_character_entities = self.entity_manager \
                .get_entities_with_components(IsPlayerCharacterTag)

        for tcod_event in event.wait():
            action = self.event_handler.dispatch(tcod_event)

            if action is None:
                continue

            for player_character_entity in player_character_entities:
                action.perform(self.entity_manager, player_character_entity)
