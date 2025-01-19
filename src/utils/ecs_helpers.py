from typing import Optional, Iterable

from ecs import Entity, EntityManager
from components import PositionComponent, IsBlockingTag


def get_blocking_entities_at_position(
        world: EntityManager, x: int, y: int
) -> Optional[Iterable[Entity]]:
    blocking_entities = world.get_entities_with_components(
        PositionComponent, IsBlockingTag
    )
    
    blocking_entities_at_position = [
        entity
        for entity in blocking_entities
        if (
            (position := entity.get_component(PositionComponent)) and
            (position.x, position.y) == (x, y)
        )
    ]

    return (
        blocking_entities_at_position
        if blocking_entities_at_position
        else None
    )
