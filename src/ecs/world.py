from typing import Type, Iterable

from .entity import Entity
from .component import Component
from .generic_component import GenericComponent


class World:
    """Collection of entities."""
    def __init__(self, entities: list[Entity] = []):
        self.entities = entities

    def get_entities_with_components(
            self, *components_types: Type[Component]
    ) -> list[Entity]:
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
                    has_required_component = (
                        has_required_component or
                        isinstance(
                            component, required_component_type
                        )
                    )

                has_required_components = (
                    has_required_components and has_required_component
                )

            if (has_required_components):
                entities_with_components.append(entity)
            else:
                continue

        return entities_with_components

    def get_entities_with_generic_components(
            self,
            generic_components_types: dict[Type[GenericComponent], Type],
            *component_types: Type[Component]
    ) -> list[Entity]:
        """
        Retrieve all entities that:
          - Contain all the specified component types, and
          - For each specified GenericComponent type, have a component
            instance whose `generic_type` matches the expected type.

        Args:
            generic_components_types: A mapping of generic component base types
            to their expected generic type.
            *component_types: Additional component types the entity must have.

        Returns:
            A list of entities satisfying both conditions.
        """
        entities_with_components = self.get_entities_with_components(component_types)
        matching_entities: list[Entity] = []

        for entity in entities_with_components:
            if all(
                any(
                    isinstance(component, generic_type) and
                    getattr(component, "generic_type", None) == expected_type
                    for component in entity.components
                )
                for generic_type, expected_type in generic_components_types.items()
            ):
                matching_entities.append(entity)

        return matching_entities

    def get_components(
            self, component_type: Type[Component]
    ) -> Iterable[Component]:
        """Get all the components of a given type in ECS world."""
        return [
            e.get_component(component_type)

            for e in self.get_entities_with_components(component_type)
        ]

    def has_components(
        self, entity: Entity, *component_types: Type[Component]
    ) -> bool:
        """Return true if the entity contains a component of the given type."""
        entities_with_components = self.get_entities_with_components(
            *component_types
        )

        return entity in entities_with_components
