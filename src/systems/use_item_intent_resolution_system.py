from __future__ import annotations

from typing_extensions import override
from typing import Iterable

from ecs.system import System
from ecs.world import World
from ecs.entity import Entity
from components.queue_component import QueueComponent
from components.consumable_component import ConsumableComponent
from components.use_item_intent import UseItemIntent
from events.apply_effect_event import ApplyEffectEvent


class UseItemIntentResolutionSystem(System):
    """System that converts item usage intents to apply effect events."""
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
        # Get apply effect events queue.
        event_queues: Iterable[QueueComponent[ApplyEffectEvent]] = (
            e.get_component(QueueComponent)
            for e in self.world.get_entities_with_generic_components(
                {QueueComponent: ApplyEffectEvent},
                QueueComponent
            )
        )

        # Get entities with use item intents.
        use_item_entities: list[Entity] = (
            self.world.get_entities_with_components(
                UseItemIntent
            )
        )
        use_item_components: list[UseItemIntent] = [
           e.get_component(UseItemIntent) for e in use_item_entities
        ]

        entity_component_zip = zip(use_item_entities, use_item_components)

        for event_queue in event_queues:
            event_queue: QueueComponent[ApplyEffectEvent]

            for intent_entity, intent_component in entity_component_zip:
                intent_component: UseItemIntent

                # Build the apply effect event.
                item = intent_component.item
                consumable_component: ConsumableComponent | None = item.get_component(ConsumableComponent)

                if not consumable_component:
                    continue

                target = intent_component.target or intent_entity

                event = ApplyEffectEvent(
                    effect = consumable_component.effect,
                    user=intent_entity,
                    target=target,
                    params=consumable_component.params,
                    item=item
                )
                # Add the event to the queue.
                event_queue.queue.append(event)
                # Remove use item intent from entity.
                intent_entity.components.remove(intent_component)
