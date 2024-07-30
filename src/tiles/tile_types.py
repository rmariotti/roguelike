import numpy as np # type: ignore

from colors import Palette


# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
        [
            ("ch", np.int32), # Unicode codepoint.
            ("fg", "3B"), # 3 unsigned bytes, for RGB colors.
            ("bg", "3B"),
        ])

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
        [
            ("walkable", np.bool), # True if this tile can be walked over.
            ("transparent", np.bool), # True if this tile doesn't block FOV.
            ("dark", graphic_dt), # Graphics for when this tile is not in FOV.
            ("light", graphic_dt) # Graphics for when the tile is in FOV.
        ])


def new_tile(
        *, # Enforce the use of keywords, so params order doesn't matter.
        walkable: int,
        transparent: int,
        dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
        light: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types."""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles.
SHROUD = np.array(
        (ord(" "), Palette.WHITE_BRIGHT.value, Palette.BLACK.value),
        dtype=graphic_dt
)

floor = new_tile(
        walkable=True,
        transparent=True,
        dark=(ord("."), Palette.BROWN_BRIGHT.value, Palette.BLACK.value),
        light=(ord("."), Palette.WHITE.value, Palette.BLACK.value),
)
bound_wall = new_tile(
        walkable=False,
        transparent=False,
        dark=(ord("#"), Palette.CYAN.value, Palette.PURPLE.value),
        light=(ord("#"), Palette.CYAN_BRIGHT.value, Palette.PURPLE.value),
)
