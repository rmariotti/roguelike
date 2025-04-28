from ecs.component import Component


class ActorComponent(Component):
    def __init__(self):
        super().__init__()
        self.energy: int
        self.upkeep: int
