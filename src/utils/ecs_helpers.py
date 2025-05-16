from typing import Optional, Iterable, Type

from ecs.entity import Entity
from ecs.world import World
from ecs.component import Component
from components.position_component import PositionComponent
from components.is_blocking_tag import IsBlockingTag
from components.is_default_tag import create_is_default_tag


def get_blocking_entities_at_position(
        world: World, x: int, y: int
) -> Iterable[Entity]:
    blocking_entities = world.get_entities_with_components(
        PositionComponent, IsBlockingTag
    )

    blocking_entities_at_position = [
        entity for entity in blocking_entities if (
            (position := entity.get_component(PositionComponent)) and
            (position.x, position.y) == (x, y)
        )
    ]

    return blocking_entities_at_position or []


def get_default_component(
        world: World, component_type: Type[Component]
) -> Optional[Component]:
    tag_type = create_is_default_tag(component_type)
    entities_with_component = world.get_entities_with_components(
        component_type, tag_type
    )

    if entities_with_component:
        return entities_with_component[0].get_component(component_type)

    return None
