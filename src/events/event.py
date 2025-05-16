from abc import ABC


class Event(ABC):
    """
    Abstract base class for events.

    This class represents a generic event within the program. 
    Events are used to signal that something has occurred and 
    can be propagated to and handled by event handlers.

    Subclasses should define specific types of events and 
    include any relevant data associated with the event.
    """
    def __init__(self):
        pass
