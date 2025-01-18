from enum import Enum

from ecs import Entity
from components import (
    PositionComponent,
    DirectionComponent,
    SpeedComponent,
    RenderingComponent,
    IsBlockingTag
)
from colors import Palette
from utils import Direction


class MonsterType(Enum):
    LARVA=0
    CREEPER=1
    ADULT=2
    BREEDER=3
    QUEEN=4


def generate_monster(
        monster_type: MonsterType,
        position: tuple[int, int] = (0, 0),
        direction: Direction = Direction.NORTH
) -> Entity:
    """Builds a monster entity given a type."""

    # TODO: Replace this function with a proper Factory that uses blueprints
    # from raw data. <RM, 2025-01-17>
    if monster_type == MonsterType.LARVA:
        return Entity(
            PositionComponent(*position),
            RenderingComponent("l", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.CREEPER:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0), DirectionComponent(direction),
            RenderingComponent("c", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.ADULT:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0), DirectionComponent(direction),
            RenderingComponent("A", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.BREEDER:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0), DirectionComponent(direction),
            RenderingComponent("B", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.QUEEN:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0), DirectionComponent(direction),
            RenderingComponent("Q", Palette.CYAN_BRIGHT.value),
            IsBlockingTag()
        )
    else:
        raise ValueError
    