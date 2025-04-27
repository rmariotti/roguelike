from enum import Enum

from ecs.entity import Entity
from components.position_component import PositionComponent
from components.direction_component import DirectionComponent
from components.speed_component import SpeedComponent
from components.rendering_component import RenderingComponent
from components.is_blocking_tag import IsBlockingTag
from components.ai_component import HostileEnemyAI
from components.fighter_component import FighterComponent
from colors.palette import Palette
from utils.direction_enum import Direction


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
            SpeedComponent(0, 1), DirectionComponent(direction),
            RenderingComponent("c", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.ADULT:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0, 1), DirectionComponent(direction),
            RenderingComponent("A", Palette.ORANGE_BRIGHT.value),
            FighterComponent(hp=30, defense=2, power=5),
            HostileEnemyAI(),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.BREEDER:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0, 1), DirectionComponent(direction),
            RenderingComponent("B", Palette.ORANGE_BRIGHT.value),
            IsBlockingTag()
        )
    elif monster_type == MonsterType.QUEEN:
        return Entity(
            PositionComponent(*position),
            SpeedComponent(0, 1), DirectionComponent(direction),
            RenderingComponent("Q", Palette.CYAN_BRIGHT.value),
            IsBlockingTag()
        )
    else:
        raise ValueError
    
