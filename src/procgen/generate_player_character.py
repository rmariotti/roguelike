from ecs.entity import Entity
from components.description_component import DescriptionComponent
from components.actor_component import ActorComponent
from components.position_component import PositionComponent
from components.is_player_character_tag import IsPlayerCharacterTag
from components.is_blocking_tag import IsBlockingTag
from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from components.rendering_component import RenderingComponent
from components.melee_attack_component import MeleeAttackComponent
from components.health_component import HealthComponent
from colors.palette import Palette
from utils.direction_enum import Direction


def generate_player_character(position: tuple[int, int] = (0, 0)):
    return Entity(
        ActorComponent(),
        DescriptionComponent(name="ripley", description="The player character"),
        PositionComponent(position[0], position[1]),
        IsPlayerCharacterTag(),
        IsBlockingTag(),
        SpeedComponent(0, 1), DirectionComponent(Direction.NORTH),
        RenderingComponent("@", Palette.ORANGE_BRIGHT.value),
        MeleeAttackComponent(damage=3),
        HealthComponent(hp=30)
    )
