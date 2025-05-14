from enum import Enum


class Palette(tuple[int, int, int], Enum):
    """
    Game color palette (urbex-16 by Rustocat).

    Source: https://lospec.com/palette-list/urbex-16
    """
    BLACK = (22, 7, 18)
    RED = (122, 19, 56)
    GREEN = (93, 118, 67)
    ORANGE = (169, 49, 48)
    BROWN = (38, 32, 29)
    PURPLE = (89, 48, 132)
    CYAN = (56, 112, 190)
    WHITE = (143, 147, 134)

    BLACK_BRIGHT = (82, 83, 76)
    RED_BRIGHT = (145, 118, 146)
    GREEN_BRIGHT = (145, 164, 112)
    ORANGE_BRIGHT = (224, 164, 110)
    BROWN_BRIGHT = (77, 83, 58)
    PURPLE_BRIGHT = (131, 70, 100)
    CYAN_BRIGHT = (87, 159, 180)
    WHITE_BRIGHT = (203, 209, 190)

    GREY = (82, 83, 76)
    PINK_GREY = (145, 118, 146)
    MOSS_GREEN = (145, 164, 112)
    PEACH = (224, 164, 110)
    OLIVE = (77, 83, 58)
    DUSTY_PURPLE = (131, 70, 100)
