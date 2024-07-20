from ecs import EntityManager
from components import PositionComponent, SpeedComponent, DirectionComponent
from math import sin, cos


class MovementSystem:
    """An object containing entity movement logic."""
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager

    
    def update(self) -> None:
        moveable_entities = self.entity_manager.get_entities_with_components(
                PositionComponent, SpeedComponent, DirectionComponent)

        for entity in moveable_entities:
            # Retrieve relevant components.
            speed_component = entity.get_component(SpeedComponent)
            direction_component = entity.get_component(DirectionComponent)
            position_component = entity.get_component(PositionComponent)

            # Calculate position delta using speed and direction.
            # TODO: Remove placeholder values.
            dx = round(speed_component.speed * cos(direction_component.direction.radians))
            dy = round(speed_component.speed * sin(direction_component.direction.radians))

            # Update entity position.
            position_component.x += dx
            position_component.y += dy

