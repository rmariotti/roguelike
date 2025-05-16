from ecs.component import Component


class UIMouseLocationComponent(Component):
    def __init__(self, position: tuple[int, int] = (0, 0)):
        self.position: tuple[int, int] = position
