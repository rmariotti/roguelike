from __future__ import annotations

from abc import ABC
from typing import Optional, Tuple, Iterable, TYPE_CHECKING
from typing_extensions import override

from utils.movement_helpers import calculate_destination
from utils.ecs_helpers import get_blocking_entities_at_position
from components.position_component import PositionComponent
from components.speed_component import SpeedComponent

if TYPE_CHECKING:
    from ecs.entity import Entity
    from ecs.world import World
    from utils.direction_enum import Direction


class Action(ABC):
    """
    Represents an action triggered by user input or AI to alter game state.

    The action is forst validated and then perfomed within the game world.

    Args:
        entity: The entity performing the action.
        world: The game context in which the action takes place.
    """
    def __init__(self, entity: Entity, world: World) -> None:
        self.entity = entity
        self.world = world

    def validate(self) -> bool:
        """Asserts that the action is valid and can be performed."""
        raise NotImplementedError()

    def perform(self) -> None:
        """
        Creates an intent component in the entity performing an action.

        Intent components are then resolved by the relevant system to perform
        the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    """
    An action that includes a direction, tipically used for movement.

    Extends the base Action class by specifying a direction in which the
    action is intended to occur.

    Args:
        entity: The entity performing the action.
        world: The game context in wich the action is performed.
        direction: The direction in which the action is aimed.
    """
    def __init__(self, entity: Entity, world: World, direction: Direction):
        super().__init__(entity, world)

        self.direction = direction

    @property
    def destination_xy(self) -> Tuple[int, int]:
        """Returns this actions destination coordinates."""
        position_component = self.entity.get_component(PositionComponent)
        speed_component = self.entity.get_component(SpeedComponent)

        destination_x, destination_y = calculate_destination(
            position_component.x,
            position_component.y,
            speed_component.walking_speed,
            self.direction
        )

        return (destination_x, destination_y)

    @property
    def blocking_entities(self) -> Optional[Iterable[Entity]]:
        """Return the blocking entity at this actions direction."""
        return get_blocking_entities_at_position(
            self.world,
            *self.destination_xy
        )

    @override
    def perform(self) -> None:
        raise NotImplementedError()


class ItemAction(Action):
    """
    An item-based action, optionally directed at a specific position.

    Extends the base Action class by specifying an item to be used and, if
    needed, a target position in the game world.

    Args:
        world: The game context in which the action is performed.
        entity: The entity performing the action.
        item: The item being used in the action.
        target_position: The target location affected by the item,
            or None if the action does not involve a specific position.
    """
    def __init__(
            self,
            world: World,
            entity: Entity,
            item: Entity,
            target_position: tuple(int, int) | None
    ):
        super().__init__(entity=entity, world=world)
        self.item = item

        if not target_position:
            position_component: PositionComponent | None = (
                entity.get_component(PositionComponent)
            )

            target_position = position_component.x, position_component.y

        self.target_position = target_position

    @property
    def target_entity(self) -> Entity | None:
        """Return the entity at this action destination"""
        return get_blocking_entities_at_position(
            world=self.world,
            *self.target_position
        )
