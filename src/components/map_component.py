import numpy as np # type: ignore

from ecs import Component
import tile_types


class MapComponent(Component):
    """A container object with data about a map of tiles."""
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height),
                             fill_value=tile_types.floor, order="F")
