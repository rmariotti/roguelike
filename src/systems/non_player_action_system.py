from typing import TYPE_CHECKING

from components.is_player_character_tag import IsPlayerCharacterTag
from components.can_act_tag import CanActTag

if TYPE_CHECKING:
    from ecs.entity_manager import EntityManager

class NonPlayerActionSystem:
    def __init__(
            self, entity_manager: EntityManager
    ):
        self.entity_manager = entity_manager

    def update(self) -> None:
        acting_player_character = (
            self.entity_manager.get_entities_with_components(
                IsPlayerCharacterTag, CanActTag
            )

