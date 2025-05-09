import numpy as np # type: ignore

from ecs.component import Component
from tiles.tile_types import bound_wall


class MapComponent(Component):
    """A container object with data about a map of tiles."""
    def __init__(self, width: int, height: int):
        super().__init__()

        self.width, self.height = width, height
        self.tiles = np.full((width, height),
                             fill_value=bound_wall, order="F")
        # Tiles that the player can currently see. 
        self.visible = np.full((width, height),
                               fill_value=False, order="F")
        # Tiles that the player has seen before.
        self.explored = np.full((width, height), fill_value=False, order="F")
