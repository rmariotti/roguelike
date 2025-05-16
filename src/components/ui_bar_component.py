from ecs.component import Component


class UIBarComponent(Component):
    def __init__(
            self, position: tuple[int, int], width: int,
            height: int, characters: int,
            background_color: tuple[int, int, int],
            fill_color: tuple[int, int, int]
    ):
        self.position: tuple[int, int] = position
        self.width: int = width
        self.height: int = height
        self.characters: int = characters
        self.background_color: tuple[int, int, int] = background_color
        self.fill_color: tuple[int, int, int] = fill_color

        self.fill_width: int = 0
