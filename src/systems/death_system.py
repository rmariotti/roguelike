from ecs.system import System
from ecs.world import World
from components.health_component import HealthComponent
from components.actor_component import ActorComponent
from components.description_component import DescriptionComponent
from components.rendering_component import RenderingComponent
from components.is_blocking_tag import IsBlockingTag
from components.message_log_component import MessageLogComponent
from utils.render_priority_enum import RenderPriority
from utils.ecs_helpers import get_default_component


class DeathSystem(System):
    def __init__(self, world: World):
        self.world = world

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self):
        super().update()

        living_entities = self.world.get_entities_with_components(
            HealthComponent)

        for entity in living_entities:
            health_component: HealthComponent | None = (
                entity.get_component(HealthComponent))
            rendering_component: RenderingComponent | None = (
                entity.get_component(RenderingComponent))
            description_component: DescriptionComponent | None = (
                entity.get_component(DescriptionComponent))

            if health_component.hp <= 0:
                message_log_component: MessageLogComponent = (
                        get_default_component(
                            world=self.world,
                            component_type=MessageLogComponent
                        )
                    )
                if description_component and message_log_component:
                    message_log_component.message_log.add_message(
                        text="{} is dead".format(description_component.name)
                    )
                # Prevent the entity from acting again and render a corpse.
                entity.consume_component(ActorComponent)
                entity.consume_component(HealthComponent)
                entity.consume_component(IsBlockingTag)

                if rendering_component:
                    # TODO: Remove hardcoded character for corpses.
                    # <RM, 07-05-2025>
                    rendering_component.char = "%"
                    rendering_component.render_priority = RenderPriority.CORPSE
