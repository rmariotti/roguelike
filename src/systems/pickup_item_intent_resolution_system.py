from __future__ import annotations

from typing import override

from ecs.system import System
from ecs.world import World
from ecs.entity import Entity
from components.pickup_item_intent import PickupItemIntent
from components.position_component import PositionComponent
from components.inventory_component import InventoryComponent
from components.is_pickable_tag import IsPickableTag
from utils.ecs_helpers import get_entities_with_components_at_position


class PickupItemIntentResolutionSystem(System):
    """Resolves pickup item intents by updating game state accordingly."""
    def __init__(self, world: World):
        self.world = world

    @override
    def start(self):
        pass

    @override
    def stop(self):
        pass

    @override
    def update(self):
        # Get entities with pickup item intent.
        pickup_item_entities: list[Entity] = (
            self.world.get_entities_with_components(
                PickupItemIntent
            )
        )
        pickup_item_components: list[PickupItemIntent] = [
            e.get_component(PickupItemIntent) for e in pickup_item_entities
        ]

        entity_component_zip = zip(
            pickup_item_entities, pickup_item_components
        )

        for intent_entity, intent_component in entity_component_zip:
            intent_entity: Entity
            intent_component: PickupItemIntent

            position_component: PositionComponent = intent_entity.get_component(
                PositionComponent
            )
            inventory_component: InventoryComponent = intent_entity.get_component(
                InventoryComponent
            )

            item_entities = get_entities_with_components_at_position(
                self.world,
                (position_component.x, position_component.y),
                IsPickableTag
            )

            topmost_item: Entity = item_entities[0]

            inventory_component.capacity += 1
            inventory_component.items.append(topmost_item)

            # Remove the position tag from the item.
            topmost_item.consume_component(PositionComponent)
            intent_entity.consume_component(PickupItemIntent)
