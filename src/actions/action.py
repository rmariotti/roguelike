from __future__ import annotations

from abc import ABC
from typing import Optional, Tuple, Iterable, TYPE_CHECKING
from typing_extensions import override

from utils.math_helpers import calculate_destination
from utils.ecs_helpers import get_blocking_entities_at_position
from components.position_component import PositionComponent
from components.speed_component import SpeedComponent

if TYPE_CHECKING:
    from ecs.entity import Entity
    from ecs.world import World
    from utils.direction_enum import Direction


class Action(ABC):
    def __init__(self, entity: Entity, world: World) -> None:
        self.entity = entity
        self.world = world

    def perform(self) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        `self.world` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, world: World, entity: Entity, direction: Direction):
        super().__init__(entity, world)

        self.direction = direction

    @property
    def destination_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
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
        """Return the blocking entity at this actions destination."""
        return get_blocking_entities_at_position(
            self.world,
            *self.destination_xy
        )

    @override
    def perform(self) -> None:
        raise NotImplementedError()
