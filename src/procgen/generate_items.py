from ecs.entity import Entity
from components.rendering_component import RenderingComponent
from components.position_component import PositionComponent
from components.is_pickable_tag import IsPickableTag
from components.consumable_component import ConsumableComponent
from components.description_component import DescriptionComponent
from colors.palette import Palette


def generate_medikit(
        position: tuple[int, int] = (0, 0)
) -> Entity:
    return Entity(
        DescriptionComponent(
            name="medikit",
            description="Allows to recover a small amount of health"
        ),
        RenderingComponent("!", Palette.RED_BRIGHT),
        PositionComponent(position[0], position[1]),
        IsPickableTag(),
        ConsumableComponent('heal', {'amount': 6})
    )
