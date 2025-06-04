from __future__ import annotations

from typing import override, Iterable

import tcod

from ecs.system import System
from ecs.world import World
from ecs.entity import Entity
from components.ui_inventory_component import UIInventoryComponent
from components.inventory_component import InventoryComponent
from components.position_component import PositionComponent
from components.is_player_character_tag import IsPlayerCharacterTag
from components.description_component import DescriptionComponent
from colors.ui_colors import UIColors


class UIInventoryRenderSystem(System):
    """
    Renders the inventory in tcod ui.

    The position of the window will adapt to where the player character is
    located, so the player can always see where his character is.
    """
    def __init__(
            self, world: World, root_console: tcod.console.Console,
            context: tcod.context.Context
    ):
        self.world: World = world
        self.root_console: tcod.console.Console = root_console
        self.inventory_console : tcod.console.Console | None = None
        self.contex: tcod.context.Context = context

    @override
    def start(self):
        pass

    @override
    def stop(self):
        pass

    @override
    def update(self):
        # Get ui inventory components.
        ui_inventories: Iterable[UIInventoryComponent] = (
            self.world.get_components(
               UIInventoryComponent
            )
        )

        for ui_inventory in ui_inventories:
            player_character_with_inventory = (
                (
                    e,
                    e.get_component(InventoryComponent),
                    e.get_component(PositionComponent)
                )

                for e in self.world.get_entities_with_components(
                    IsPlayerCharacterTag,
                    InventoryComponent,
                    PositionComponent
                )
            )

            for entity, inventory, position in player_character_with_inventory:
                entity: Entity
                inventory: InventoryComponent
                position: PositionComponent

                number_of_items_in_inventory = len(inventory.items)

                height = number_of_items_in_inventory + 2
                width = len(ui_inventory.panel_title) + 4

                if height <= 3:
                    height = 3

                # TODO: Replace this absolute values with something
                # calculated on the size of the screen. <RM, 03-06-2025>
                if position.x <= 30:
                    x = 40
                else:
                    x = 0

                y = 0

                self.root_console.draw_frame(
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    title=ui_inventory.panel_title,
                    clear=True,
                    fg=UIColors.TEXT,
                    bg=UIColors.BACKGROUND
                )

                if number_of_items_in_inventory > 0:
                    for i, item in enumerate(inventory.items):
                        item_key = chr(ord("a") + i)

                        item_description_component = item.get_component(
                            DescriptionComponent
                        )

                        item_name = getattr(item_description_component, "name", None) or "unnamed item"

                        self.root_console.print(
                            x + 1, y + i + 1, f"{item_key} - {item_name}"
                        )
                else:
                    self.root_console.print(x + 1, y + 1, "empty")
