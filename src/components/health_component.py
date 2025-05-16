from ecs.component import Component


class HealthComponent(Component):
    def __init__(self, hp: int = 1):
        self.max_hp = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        """Current hit points of the entity."""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """
        Sets current hit points.

        Ensures that the value is clamped between 0 and max_hp.
        """
        self._hp = max(0, min(value, self.max_hp))
