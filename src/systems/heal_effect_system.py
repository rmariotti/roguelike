from __future__ import annotations

from typing_extensions import override
from typing import Iterable

from ecs.system import System
from ecs.world import World
from components.queue_component import QueueComponent
from components.health_component import HealthComponent
from components.can_heal_tag import CanHealTag
from events.apply_effect_event import ApplyEffectEvent


class HealEffectSystem(System):
    """System that processes heal effect events from the apply effect queue."""
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
        """Applies healing effects for all the queued heal events."""
        event_queues: Iterable[QueueComponent[ApplyEffectEvent]] = (
            e.get_component(QueueComponent)
            for e in self.world.get_entities_with_generic_components(
                {QueueComponent: ApplyEffectEvent},
                QueueComponent
            )
        )

        for event_queue in event_queues:
            event_queue: QueueComponent[ApplyEffectEvent]

            for event in list(event_queue.queue):
                event: ApplyEffectEvent

                # TODO: Use a constant file or an enum <29-5-2025, RM>.
                if event.effect != "heal":
                    continue

                # Get target health component and check for can heal
                # component.
                target_health: HealthComponent | None = (
                    event.target.get_component(HealthComponent)
                )
                target_can_heal: CanHealTag | None = (
                    self.world.has_components(event.target, CanHealTag)
                )

                if not (target_health and target_can_heal):
                    continue

                heal_amount = event.params.get("amount", 0)
                target_health.hp = target_health.hp + heal_amount

            # All events processed, clear the queue.
            event_queue.queue.clear()
