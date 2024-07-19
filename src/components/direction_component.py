from ecs import Component


class DirectionComponent(Component):
    """
    A container object with data about direction of an entity.
    """
    def __init__(self, direction: int):
        self.direction = direction

