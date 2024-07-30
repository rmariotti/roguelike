from ecs import Entity
from components import (
        PositionComponent,
        DirectionComponent,
        SpeedComponent,
        RenderingComponent
)


class Adult:
    def __init__(self):
        self.reference = Entity(
                PositionComponent(0, 0),
                DirectionComponent(),
                SpeedComponent(0),
                RenderingComponent(
                    "A",



    def spawn(self) -> Entity:
        return 
