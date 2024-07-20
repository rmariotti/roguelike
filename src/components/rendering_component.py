from typing import Tuple
from ecs import Component


class RenderingComponent(Component):
    """A container object with data about a renderable entity."""
    def __init__(self, char: str, color: Tuple[int, int, int]):
        self.char = char
        self.color = color

