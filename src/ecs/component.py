from abc import ABC


class Component(ABC):
    """
    Abstaract base class for components.

    A component is a data container for entities and should have no
    logic.
    """
    def __init__(self):
        pass
