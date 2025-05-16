from ecs.component import Component


class UIMessageLogComponent(Component):
    def __init__(
            self, position: tuple[int, int], width: int, height: int,
    ):
        self.position: tuple[int, int] = position
        self.width: int = width
        self.height: int = height
