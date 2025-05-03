import numpy as np

from tcod.context import Context
from tcod.console import Console

from ecs.entity_manager import EntityManager
from ecs.system import System
from components.position_component import PositionComponent
from components.rendering_component import RenderingComponent
from components.map_component import MapComponent
from tiles.tile_types import SHROUD


class RenderingSystem(System):
    """System handling rendering of entities."""
    def __init__(self, entity_manager: EntityManager, console: Console,
                 context: Context):
        self.entity_manager = entity_manager
        self.console = console
        self.context = context
    
    def update(self) -> None:
        self.render_maps()
        self.render_characters()

    def render_characters(self) -> None:
        renderable_entities = self.entity_manager.get_entities_with_components(
                PositionComponent, RenderingComponent)
        map_entities = self.entity_manager.get_entities_with_components(
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
                        position_component.x, position_component.y]:
                    self.console.print(
                            position_component.x,
                            position_component.y,
                            rendering_component.char, 
                            fg=rendering_component.color
                    )

        self.context.present(self.console)
        self.console.clear()

    def render_maps(self) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the 
        "light" colors.
        If it isn't, but it's in the "explored" array, then draw it 
        with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        renderable_entities = self.entity_manager.get_entities_with_components(
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

