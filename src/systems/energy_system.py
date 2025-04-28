from ecs.entity_manager import EntityManager
from components.can_act_tag import CanActTag
from components.actor_component import ActorComponent


class EnergySystem:
    """Handles actors energy upkeep."""
    def __init__(self):
        self.entity_manager: EntityManager

    def update(self) -> None:
        # Check if some actor is waiting to act.
        actors_waiting = self.entity_manager.get_entities_with_components(
                CanActTag)

        if actors_waiting.lenght != 0:
            return
        
        # Get all actors.
        actors = self.entity_manager.get_entities_with_components(
                ActorComponent)

        for actor in actors:
            actor.energy += actor.upkeep
