from ecs.component import Component


class ActorComponent(Component):
    """
    Component for acting entities.

    Every game loop the energy of an actor is increased of the upkeep value, 
    if it reaches the treshold value, the actor gains an action and 
    the energy is reset.
    """
    def __init__(self, energy=0, upkeep=1, treshold=10):
        super().__init__()

        self.energy = energy
        self.upkeep = upkeep
        self.treshold = treshold
