from ecs import Component


class PositionComponent(Component):
    """
    A container object with data about an entity that has a position.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

