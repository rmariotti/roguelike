from ecs.component import Component
from utils.direction_enum import Direction


class DirectionComponent(Component):
    """A container object with data about direction of an entity."""
    def __init__(self, direction: Direction):
        super().__init__()

        self.direction = direction
