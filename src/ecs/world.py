from typing import Type

from .entity import Entity
from .component import Component


class World:
    """Collection of entities."""
    def __init__(self, entities: list[Entity] = []):
        self.entities = entities

    def get_entities_with_components(
            self, *components_types: Type[Component]) -> list[Entity]:
        """Get entities that contains all the specified components."""
        entities_with_components = []
        has_required_components = True
        has_required_component = False

        # TODO: This nested loop is inefficient, some kind of indexing
        # for components should be used.
        for entity in self.entities:
            has_required_components = True

            # Check if the entity at least one component matching the 
            # required component for each required component.
            for required_component_type in components_types:
                has_required_component = False

                # Check if one of the components in entity is of the 
                # required component type.
                for component in entity.components:
                    has_required_component = (has_required_component or
                                              isinstance(
                                                  component,
                                                  required_component_type))
                
                has_required_components = (has_required_components and
                                           has_required_component)

            if (has_required_components):
                entities_with_components.append(entity)
            else:
                continue

        return entities_with_components
