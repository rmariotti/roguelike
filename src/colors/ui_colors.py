from enum import Enum

from .palette import Palette


class UIColors(tuple[int, int, int], Enum):
    """Semantic tokens built from color palette."""
    TEXT = Palette.WHITE_BRIGHT

    BACKGROUND = Palette.BLACK
    HIGHLIGHT = Palette.ORANGE
    SELECTION = Palette.CYAN

    SUCCESS = Palette.GREEN_BRIGHT
    WARNING = Palette.ORANGE_BRIGHT
    ERROR = Palette.RED_BRIGHT
    INVALID = Palette.MOSS_GREEN
    IMPOSSIBLE = Palette.PEACH

    HEALTH_BAR_FILL = Palette.ORANGE
    HEALTH_BAR_EMPTY = Palette.ORANGE_BRIGHT
