from abc import ABC


class Component(ABC):
    """
    Abstract base class for components.

    A component is a data container for entities and should have no
    logic.
    """
    def __init__(self):
        super().__init__()
