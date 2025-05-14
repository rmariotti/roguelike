import numpy as np

from tcod.context import Context
from tcod.console import Console

from ecs.world import World
from ecs.system import System
from components.position_component import PositionComponent
from components.rendering_component import RenderingComponent
from components.map_component import MapComponent
from components.ui_label_component import UILabelComponent
from components.ui_bar_component import UIBarComponent
from tiles.tile_types import SHROUD


class RenderingSystem(System):
    """System handling rendering of entities."""
    def __init__(
            self, world: World, console: Console, context: Context
    ):
        super().__init__()

        self.world = world
        self.console = console
        self.context = context

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        self.render_maps()
        self.render_characters()
        self.render_ui()
        self.context.present(self.console)
        self.console.clear()

    def render_characters(self) -> None:
        renderable_entities = sorted(
            self.world.get_entities_with_components(
                PositionComponent, RenderingComponent
            ),
            key=lambda x: x.get_component(
                RenderingComponent).render_priority.value
        )

        map_entities = self.world.get_entities_with_components(
            MapComponent)

        for entity in renderable_entities:
            position_component: PositionComponent = entity.get_component(
                PositionComponent)
            rendering_component: RenderingComponent = entity.get_component(
                RenderingComponent)

            for map_entity in map_entities:
                map_component: MapComponent = map_entity.get_component(
                    MapComponent)

                # Only print entities that are in FOV.
                if map_component.visible[
                    position_component.x,
                    position_component.y
                ]:
                    self.console.print(
                        position_component.x,
                        position_component.y,
                        rendering_component.char,
                        fg=rendering_component.color
                    )

    def render_maps(self) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the
        "light" colors.
        If it isn't, but it's in the "explored" array, then draw it
        with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        renderable_entities = self.world.get_entities_with_components(
            MapComponent)

        for entity in renderable_entities:
            map_component: MapComponent = entity.get_component(MapComponent)

            self.console.rgb[0:map_component.width, 0:map_component.height] = (
                    np.select(
                        condlist=[
                            map_component.visible,
                            map_component.explored,
                        ],
                        choicelist=[
                            map_component.tiles["light"],
                            map_component.tiles["dark"],
                        ],
                        default=SHROUD
                    )
            )

    def render_ui(self) -> None:
        ui_bar_entities = self.world.get_entities_with_components(
            UIBarComponent
        )

        for ui_bar_entity in ui_bar_entities:
            ui_bar_component: UIBarComponent = (
                ui_bar_entity.get_component(UIBarComponent)
            )

            if ui_bar_component:
                # Draw unfilled part of the bar.
                self.console.draw_rect(
                    x=ui_bar_component.position[0],
                    y=ui_bar_component.position[1],
                    width=ui_bar_component.width,
                    height=ui_bar_component.height,
                    ch=ui_bar_component.characters,
                    bg=ui_bar_component.background_color
                )

                # Draw filled part of the bar.
                if ui_bar_component.fill_width > 0:
                    self.console.draw_rect(
                        x=ui_bar_component.position[0],
                        y=ui_bar_component.position[1],
                        width=ui_bar_component.fill_width,
                        height=ui_bar_component.height,
                        ch=ui_bar_component.characters,
                        bg=ui_bar_component.fill_color
                    )

        ui_label_entities = self.world.get_entities_with_components(
            UILabelComponent
        )

        for ui_label_entity in ui_label_entities:
            ui_label_component: UILabelComponent = (
                ui_label_entity.get_component(UILabelComponent)
            )

            if ui_label_component:
                self.console.print(
                    x=ui_label_component.position[0],
                    y=ui_label_component.position[1],
                    string=ui_label_component.text
                )
