from typing import Type, TypeVar, Generic, Any
from ecs.component import Component

TComponent = TypeVar('TComponent', bound=Component)

_tag_cache = {}


def create_is_default_tag(component_type: Type[TComponent]) -> Type[Any]:
    if component_type in _tag_cache:
        return _tag_cache[component_type]

    class IsDefaultTag(Generic[TComponent]):
        def __init__(self):
            self.component_type: Type[TComponent] = component_type

    _tag_cache[component_type] = IsDefaultTag
    return IsDefaultTag


def DefaultTag(component_type: Type[TComponent]) -> Type[Any]:
    """
    `create_is_default_tag` wrapper to allow DefaultTag(ComponentType) syntax.
    """
    tag_class = create_is_default_tag(component_type)
    return tag_class()
