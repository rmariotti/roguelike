from __future__ import annotations

from typing import override

from .action import Action
from components.ui_inventory_component import UIInventoryComponent
from ecs.entity import Entity


class OpenInventory(Action):
    @override
    def perform(self):
        # Add an `Entity` with `UIInventoryComponent` to world.
        # The `UIINventoryRenderSystem` will print it on screen.
        self.world.entities.append(
            Entity(
                UIInventoryComponent(
                    panel_title="inventory"
                )
            )
        )


class CloseInventory(Action):
    @override
    def perform(self):
        ui_inventory_entities = self.world.get_entities_with_components(
            UIInventoryComponent
        )

        for e in ui_inventory_entities:
            self.world.entities.remove(e)
