from enum import Enum

from .palette import Palette


class UIColors(Enum):
    """Semantic tokens built from color palette."""
    TEXT = Palette.WHITE
    BACKGROUND = Palette.BLACK
    HIGHLIGHT = Palette.ORANGE
    SELECTION = Palette.CYAN

    HEALTH_BAR_TEXT = Palette.RED_BRIGHT
    HEALTH_BAR_FILL = Palette.RED
    HEALTH_BAR_EMPTY = Palette.ORANGE_BRIGHT
