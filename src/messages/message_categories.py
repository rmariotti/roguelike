from enum import Enum, auto


class MessageCategory(Enum):
    INFO = auto()
    WARNING = auto()
    SUCCESS = auto()
    SYSTEM = auto()
