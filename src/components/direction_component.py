from ecs import Component
from utils import Direction


class DirectionComponent(Component):
    """A container object with data about direction of an entity."""
    def __init__(self, direction: Direction):
        self.direction = direction

