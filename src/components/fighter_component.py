from ecs import Component


class FighterComponent(Component):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        # Ensure hp is in the interval between 0 and max_hp.
        self._hp = max(0, min(value, self.max_hp))
