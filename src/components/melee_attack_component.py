from ecs.component import Component


class MeleeAttackComponent(Component):
    def __init__(self, damage: int = 3, description: str = "{0} attacks {1}."):
        self.damage = damage
        self.description = description 
