from collections import deque
from typing import TypeVar, Generic, Deque

from ecs.component import Component
from ecs.generic_component import GenericComponent


T = TypeVar('T')


class QueueComponent(Generic[T], GenericComponent, Component):
    """
    Generic component that holds a queue of data of type T.

    Args:
        item_type: Type of items in the queue, for runtime access.

    Attributes:
        queue: A queue of object of the same type in FIFO order.
    """
    def __init__(self, item_type: type):
        super().__init__(item_type)  # Pass item type to GenericComponent.
        self.queue: Deque[T] = deque()
