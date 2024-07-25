from abc import ABC, abstractmethod


class System(ABC):
    """
    Abstract base class for systems.

    A system contains the logic to update components in entities and
    have no data.
    """
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def stop(self):
        pass
