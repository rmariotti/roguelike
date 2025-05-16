from typing import Tuple

from ecs.component import Component
from utils.render_priorities import RenderPriority


class RenderingComponent(Component):
    """A container object with data about a renderable entity."""
    def __init__(
            self, char: str, color: Tuple[int, int, int],
            render_priority: RenderPriority = RenderPriority.CORPSE
    ):
        self.char = char
        self.color = color
        self.render_priority = render_priority
