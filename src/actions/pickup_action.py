from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

from .action import Action

from components.inventory_component import InventoryComponent
from components.position_component import PositionComponent
from components.is_pickable_tag import IsPickableTag
from components.pickup_item_intent import PickupItemIntent
from exceptions.action_exceptions import ImpossibleAction
from utils.ecs_helpers import get_entities_with_components_at_position

if TYPE_CHECKING:
    from ecs.entity import Entity
    from ecs.world import World


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""
    def __init__(self, entity: Entity, world: World):
        super().__init__(entity, world)

    @override
    def perform(self) -> None:
        # Check that the entity has inventory and position components.
        has_components = self.world.has_components(
            self.entity,
            InventoryComponent,
            PositionComponent
        )

        if not has_components:
            raise ImpossibleAction(
                "The entity trying to pickup an item has no inventory "
                "or position components."
            )

        # Get entity position and check if there are items there.
        position_component: PositionComponent = self.entity.get_component(
            PositionComponent
        )

        item_entities = get_entities_with_components_at_position(
            self.world,
            (position_component.x, position_component.y),
            IsPickableTag
        )

        if not item_entities:
            raise ImpossibleAction(
                "There are no items to pickup."
            )

        # Get entity inventory and check if there is room to pickup an item.
        inventory_component: InventoryComponent = self.entity.get_component(
            InventoryComponent
        )

        if not inventory_component.capacity >= len(inventory_component.items):
            raise(
                "The inventory is full."
            )

        # Everything is valid, add intent component to entity.
        print("Pickup action intent added.")
        self.entity.components.append(
            PickupItemIntent()
        )
