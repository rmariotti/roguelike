import numpy as np

from tcod.context import Context
from tcod.console import Console

from ecs.world import World
from ecs.system import System
from components.position_component import PositionComponent
from components.rendering_component import RenderingComponent
from components.description_component import DescriptionComponent
from components.map_component import MapComponent
from components.ui_label_component import UILabelComponent
from components.ui_bar_component import UIBarComponent
from components.message_log_component import MessageLogComponent
from components.ui_message_log_component import UIMessageLogComponent
from components.ui_mouse_location_component import UIMouseLocationComponent
from components.ui_names_at_mouse_location_tag import UINamesAtMouseLocationTag
from tiles.tile_types import SHROUD
from utils.ecs_helpers import (
    get_default_component,
    get_blocking_entities_at_position
)
from utils.render_helpers import render_message_log_component


class RenderSystem(System):
    """System handling rendering of entities."""
    def __init__(
            self, world: World, console: Console, context: Context
    ):
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
        self.render_names_at_mouse_location()

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
        # Render ui bars.
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

        # Render ui labels.
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

        # Render ui message logs.
        self.render_message_logs()

    def render_message_logs(self) -> None:
        """
        Render message logs.
        The messages are rendered starting at the last message and
        working backwards.
        """
        ui_message_log_entities = self.world.get_entities_with_components(
            UIMessageLogComponent,
            MessageLogComponent
        )

        for ui_message_log_entity in ui_message_log_entities:
            message_log_component: MessageLogComponent = (
                ui_message_log_entity.get_component(MessageLogComponent)
            )
            ui_message_log_component: UIMessageLogComponent = (
                ui_message_log_entity.get_component(UIMessageLogComponent)
            )

            if ui_message_log_component:
                render_message_log_component(
                    console=self.console,
                    message_log_component=message_log_component,
                    ui_message_log_component=ui_message_log_component
                )

    def render_names_at_mouse_location(self) -> None:
        """
        Render the names of the entities under mouse cursor.
        """
        names_at_mouse_location_tag = get_default_component(
            world=self.world,
            component_type=UINamesAtMouseLocationTag
        )
        mouse_location_component = get_default_component(
            world=self.world,
            component_type=UIMouseLocationComponent
        )

        if names_at_mouse_location_tag and mouse_location_component:
            mouse_location_component: UIMouseLocationComponent
            entities_at_location = get_blocking_entities_at_position(
                world=self.world,
                x=mouse_location_component.position[0],
                y=mouse_location_component.position[1]
            )

            for entity in entities_at_location:
                # TODO: Check entity visibility before rendering names.
                description_component = entity.get_component(
                    component_type=DescriptionComponent
                )
                position_component = entity.get_component(
                    component_type=PositionComponent
                )

                if description_component and position_component:
                    description_component: DescriptionComponent
                    position_component: PositionComponent

                    self.console.print(
                        x=position_component.x,
                        y=position_component.y,
                        string=description_component.name
                    )
