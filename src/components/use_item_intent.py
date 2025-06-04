from ecs.component import Component
from ecs.entity import Entity


class UseItemIntent(Component):
    """
    Component representing the intent to use an item.

    Attributes:
        item: The entity of the item to be used.
        target: Optional target entity, default to self if None.
    """
    def __init__(self, item: Entity, target: Entity | None = None):
        self.item = item
        self.target = target
