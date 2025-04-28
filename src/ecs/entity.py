from typing import Optional, Type
from .component import Component


class Entity:
    """A generic object to represent players, enemies, items, etc."""
    def __init__(self, *components: Component):
        self.components = list(components)

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """Returns entity's component of given type."""
        # TODO: Index components so that accessing them does not
        # require linear search.
        for component in self.components:
            if isinstance(component, component_type):
                return component

        return None

    def consume_component(self, component_type: Type[Component]) -> None:

