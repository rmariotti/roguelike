from typing_extensions import TYPE_CHECKING

from ecs.component import Component

if TYPE_CHECKING:
    from ecs.entity import Entity


class InventoryComponent(Component):
    """An entity with this component can pickup, drop and carry items."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: list[Entity] = []
