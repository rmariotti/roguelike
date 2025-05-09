from typing_extensions import override

from .action import ActionWithDirection
from components.melee_attack_component import MeleeAttackComponent
from components.health_component import HealthComponent
from components.description_component import DescriptionComponent


class MeleeAction(ActionWithDirection):
    @override
    def perform(self):
        actor_melee_attack_component: MeleeAttackComponent | None = (
            self.entity.get_component(MeleeAttackComponent)
        )

        actor_description_component: DescriptionComponent | None = (
            self.entity.get_component(DescriptionComponent)
        )

        if not (self.blocking_entities and actor_melee_attack_component):
            return

        for target in self.blocking_entities:
            target_health_component: HealthComponent | None = (
                target.get_component(HealthComponent)
            )

            target_description_component: DescriptionComponent | None = (
                target.get_component(DescriptionComponent)
            )

            if target_health_component:
                target_health_component.hp -= (
                    actor_melee_attack_component.damage
                )

            if target_description_component and actor_description_component:
                print(
                    actor_melee_attack_component.description.format(
                        actor_description_component.name,
                        target_description_component.name
                    ))
            else:
                print("Something takes damage!")
