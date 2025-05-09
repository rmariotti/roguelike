from collections import deque
from typing import Optional

from ecs.system import System
from ecs.entity import Entity
from ecs.world import World
from components.actor_component import ActorComponent


class ActionSystem(System):
    """Handles actors energy upkeep and the ready to act queue."""
    def __init__(self, world: World):
        self.world = world
        self.ready_queue = deque()

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        # Check if a character is acting.
        # TODO: Use a proper lock to avoid actor's upkeep beign executed
        # while awaiting for someone to act. <RM, 2025-05-03>
        if (
            self.ready_queue
        ):
            return

        # Get all actors.
        actors = self.world.get_entities_with_components(
            ActorComponent)

        for actor in actors:
            actor_component: ActorComponent = actor.get_component(
                ActorComponent)
            actor_component.energy += actor_component.upkeep

            if actor_component.energy >= actor_component.treshold:
                # Reset energy after gaining a turn.
                actor_component.energy = 0
                self.ready_queue.append(actor)

    def has_ready_actor(self) -> bool:
        return len(self.ready_queue) > 0

    def pop_ready_actor(self) -> Optional[Entity]:
        if self.ready_queue:
            return self.ready_queue.popleft()
        else:
            return None

    def get_ready_actor(self) -> Optional[Entity]:
        if self.ready_queue:
            return self.ready_queue[0]
        else:
            return None
