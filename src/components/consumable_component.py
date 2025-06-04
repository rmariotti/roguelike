from ecs.component import Component


class ConsumableComponent(Component):
    """
    Component that marks an entity as a consumable item.

    Attributes:
        effect: Type of effect.
        params: Effect parameters.
    """
    def __init__(self, effect: str, params: dict):
        self.effect = effect
        self.params = params
