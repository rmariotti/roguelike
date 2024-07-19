from ecs import EntityManager
from components import PositionComponent, RenderingComponent, MapComponent

from tcod.context import Context
from tcod.console import Console


class RenderingSystem:
    """
    System handling rendering of entities with rendering and position components.
    """
    def __init__(self, entity_manager: EntityManager, console: Console, context: Context):
        self.entity_manager = entity_manager
        self.console = console
        self.context = context
    
    def update(self) -> None:
        self.render_maps()
        self.render_characters()

    def render_characters(self) -> None:
        renderable_entities = self.entity_manager.get_entities_with_components(
                PositionComponent, RenderingComponent)

        for entity in renderable_entities:
            position_component = entity.get_component(PositionComponent)
            rendering_component = entity.get_component(RenderingComponent)

            self.console.print(position_component.x, position_component.y,
                          rendering_component.char, 
                          fg=rendering_component.color)

        self.context.present(self.console)
        self.console.clear()

    def render_maps(self) -> None:
        renderable_entities = self.entity_manager.get_entities_with_components(
                MapComponent)

        for entity in renderable_entities:
            map_component = entity.get_component(MapComponent)

            self.console.rgb[0:map_component.width, 0:map_component.height] = map_component.tiles["dark"]

