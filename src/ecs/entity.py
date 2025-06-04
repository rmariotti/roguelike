from typing import Optional, Type, Iterable
from .component import Component


class Entity:
    """A generic object to represent players, enemies, items, etc."""
    def __init__(self, *components: Component):
        self.components = list(components)

    def get_component(
            self, component_type: Type[Component]
    ) -> Optional[Component]:
        """Returns entity's component of given type."""
        components = self.get_components(component_type)

        if components:
            return components[0]

        return None

    def get_components(
        self, component_type: Type[Component]
    ) -> Iterable[Component]:
        """Returns all the components of given type."""
        components: list[Component] = []

        # TODO: Index components so that accessing them does not
        # require linear search.
        for component in self.components:
            if isinstance(component, component_type):
                components.append(component)

        return components

    def consume_component(self, component_type: Type[Component]) -> None:
        """Removes ther first component of the given type from entity."""
        for component in self.components:
            if isinstance(component, component_type):
                self.components.remove(component)
                return None
