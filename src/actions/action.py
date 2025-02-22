from __future__ import annotations

from abc import ABC
from typing import Optional, Tuple, Iterable, TYPE_CHECKING
from typing_extensions import override

from utils import calculate_destination, get_blocking_entities_at_position
from components import (
    PositionComponent, DirectionComponent, SpeedComponent
)

if TYPE_CHECKING:
    from ecs import Entity, EntityManager
    from utils import Direction


class Action(ABC):
    def __init__(self, entity: Entity, world: EntityManager) -> None:
        super().__init__()
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
    def __init__(self, entity: Entity, world: EntityManager, direction: Direction):
        super().__init__(entity, world)

        self.direction = direction

    @property
    def destination_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        direction_component = self.entity.get_component(DirectionComponent)
        position_component = self.entity.get_component(PositionComponent)
        speed_component = self.entity.get_component(SpeedComponent)

        destination_x, destination_y = calculate_destination(
            position_component.x,
            position_component.y,
            speed_component.walking_speed,
            direction_component.direction
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
