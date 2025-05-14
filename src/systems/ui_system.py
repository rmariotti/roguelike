from __future__ import annotations

from typing_extensions import override
from typing import TYPE_CHECKING

from ecs.system import System
from components.is_player_character_tag import IsPlayerCharacterTag
from components.health_component import HealthComponent
from components.ui_label_component import UILabelComponent
from components.ui_bar_component import UIBarComponent
from components.needs_player_health_tag import NeedsPlayerHealthTag

if TYPE_CHECKING:
    from ecs.world import World


class UISystem(System):
    def __init__(self, world: World):
        super().__init__()
        self.world = world

    @override
    def start(self):
        return super().start()

    @override
    def stop(self):
        return super().stop()

    @override
    def update(self):
        super().update()

        self.update_player_health()

    def update_player_health(self):
        player_entities = self.world.get_entities_with_components(
            IsPlayerCharacterTag, HealthComponent)

        for entity in player_entities:
            health_component: HealthComponent = (
                entity.get_component(HealthComponent)
            )

            player_health_ui_label_entities = (
                self.world.get_entities_with_components(
                    UILabelComponent, NeedsPlayerHealthTag
                )
            )

            player_health_ui_labels = map(
                lambda e: e.get_component(UILabelComponent),
                player_health_ui_label_entities
            )

            for label in player_health_ui_labels:
                label: UILabelComponent
                label.text = label.template.format(
                    health_component.hp, health_component.max_hp
                )

            player_health_ui_bars_entities = (
                self.world.get_entities_with_components(
                    UIBarComponent, NeedsPlayerHealthTag
                )
            )

            player_health_ui_bars = map(
                lambda e: e.get_component(UIBarComponent),
                player_health_ui_bars_entities
            )

            for bar in player_health_ui_bars:
                bar: UIBarComponent
                bar.fill_width = int(
                    float(health_component.hp) / health_component.max_hp * bar.width
                )
