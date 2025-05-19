from enum import Enum, auto


class InputModes(Enum):
    """States for the input event handler."""
    DEFAULT = auto()
    LOG_VIEW = auto()
