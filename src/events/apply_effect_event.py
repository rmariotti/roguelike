from ecs.entity import Entity
from .event import Event


class ApplyEffectEvent(Event):
    """
    Data structure representing a resolved effect to be applied.

    Attributes:
        effect: Type of the effect.
        user: Entity applying the effect.
        target: Entity the effect is applied to.
        params: Parameters of the effect.
        item: Entity of the consumed item.
    """
    def __init__(
        self,
        effect: str,
        user: Entity,
        target: Entity,
        params: dict,
        item: Entity
    ):
        self.effect = effect
        self.user = user
        self.target = target
        self.params = params
        self.item = item
