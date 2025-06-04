from ecs.system import System
from ecs.world import World
from components.actor_component import ActorComponent
from components.scheduler_component import SchedulerComponent
from utils.ecs_helpers import get_default_component


class EnergySystem(System):
    """Handles actors energy upkeep and the ready to act queue."""
    def __init__(self, world: World):
        self.world = world

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        scheduler: SchedulerComponent = get_default_component(
            world=self.world,
            component_type=SchedulerComponent
        )

        # Check if a character is acting.
        # TODO: Use a proper lock to avoid actor's upkeep beign executed
        # while awaiting for someone to act. <RM, 2025-05-03>
        if (
            scheduler.queue
        ):
            return

        # Get all actors.
        actors = self.world.get_entities_with_components(ActorComponent)

        for actor in actors:
            actor_component: ActorComponent = actor.get_component(
                ActorComponent
            )
            actor_component.energy += actor_component.upkeep

            if actor_component.energy >= actor_component.treshold:
                # Reset energy after gaining a turn.
                actor_component.energy = 0
                scheduler.queue.append(actor)
