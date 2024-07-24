from ecs import Component


class SpeedComponent(Component):
    """A container object with data about a entity that has a speed."""
    def __init__(self, speed: int):
        self.speed = speed
