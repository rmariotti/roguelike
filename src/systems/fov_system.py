from tcod.map import compute_fov

from ecs.system import System
from ecs.entity_manager import EntityManager
from components.position_component import PositionComponent
from components.map_component import MapComponent
from components.is_player_character_tag import IsPlayerCharacterTag 


class FovSystem(System):
    """An object containing player field of view logic."""
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    
    def update(self) -> None:
        """Recompute the visible area based on the player's point of view."""
        fov_entities = self.entity_manager.get_entities_with_components(
                PositionComponent, IsPlayerCharacterTag)
        map_entities = self.entity_manager.get_entities_with_components(
                MapComponent)

        for fov_entity in fov_entities:
            position_component: PositionComponent = fov_entity.get_component(
                    PositionComponent)

            for map_entity in map_entities:
                map_component: MapComponent = map_entity.get_component(
                        MapComponent)

                map_component.visible[:] = compute_fov(
                        map_component.tiles["transparent"],
                        (position_component.x, position_component.y),
                        # TODO: Hardcoded radius value.
                        radius=8,
                )
                # If a tile is "visible" it should be added to "explored".
                map_component.explored |= map_component.visible

