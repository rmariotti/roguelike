from ecs.component import Component


class PositionComponent(Component):
    """A container object with data about an entity that has a position."""
    def __init__(self, x: int, y: int):
        super().__init__()

        self.x = x
        self.y = y
