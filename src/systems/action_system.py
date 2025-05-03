from collections import deque
from typing import Optional, TYPE_CHECKING

from ecs.system import System
from ecs.entity_manager import EntityManager
from components.actor_component import ActorComponent

if TYPE_CHECKING:
    from ecs.entity import Entity


class ActionSystem(System):
    """Handles actors energy upkeep and the ready to act queue."""
    def __init__(self):
        self.entity_manager: EntityManager
        self.ready_queue = deque()

    def update(self) -> None:
        # Get all actors.
        actors = self.entity_manager.get_entities_with_components(
            ActorComponent)

        for actor in actors:
            actor_component: ActorComponent = actor.get_component(ActorComponent)
            actor_component.energy += actor.upkeep

            if actor_component.energy >= actor_component.treshold:
                actor_component.energy = 0 # Reset energy after gaining a turn.
                self.ready_queue.append(actor)

    def has_ready_actor(self) -> bool:
        return len(self.ready_queue) > 0
    
    def pop_ready_actor(self) -> Optional[Entity]:
        if self.ready_queue:
            return self.ready_queue.popleft()
        else:
            return None

