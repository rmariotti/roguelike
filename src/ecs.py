from typing import List, Type, Optional
from abc import ABC, abstractmethod


class Component(ABC):
    """
    Abstaract base class for components.

    A component is a data container for entities and should have no 
    logic.
    """
    def __init__(self):
        pass


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, *components: Component):
        self.components = list(components)

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """
        Returns entity's component of given type.
        """
        # TODO: Index components so that accessing them does not
        # require linear search.
        for component in self.components:
            if isinstance(component, component_type):
                return component

        return None
        


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


class EntityManager:
    """
    Collection of entities.
    """
    def __init__(self, entities: List[Entity] = []):
        self.entities = entities

    def get_entities_with_components(
            self, *components_types: Type[Component]) -> List[Entity]:
        """
        Get entities that contains all the specified components.
        """
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

        return entities_with_components

