from ecs.system import System
from ecs.world import World
from components.position_component import PositionComponent
from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from components.map_component import MapComponent
from utils.movement_helpers import is_move_valid, calculate_destination


class MovementSystem(System):
    """An object containing entity movement logic."""
    def __init__(self, world: World):
        self.world = world

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        map_entities = self.world.get_entities_with_components(
            MapComponent)

        moveable_entities = self.world.get_entities_with_components(
            PositionComponent, SpeedComponent, DirectionComponent)

        for map_entity in map_entities:
            # Get the active map component, to check if the moving entities
            # are moving towards blocked tiles.
            map_component: MapComponent = map_entity.get_component(
                MapComponent)

            for entity in moveable_entities:
                # Retrieve relevant components.
                speed_component = entity.get_component(SpeedComponent)

                # Check that speed is non-zero.
                if speed_component.speed != 0:
                    direction_component = entity.get_component(
                        DirectionComponent)
                    position_component = entity.get_component(
                        PositionComponent)

                    if (
                        is_move_valid(
                            world=self.world,
                            x=position_component.x, y=position_component.y,
                            direction=direction_component.direction,
                            speed=speed_component.walking_speed,
                            map_component=map_component
                        )
                    ):
                        # Update entity position.
                        position_component.x, position_component.y = (
                            calculate_destination(
                                position_component.x, position_component.y,
                                speed_component.walking_speed,
                                direction_component.direction
                            )
                        )

                    # Stop the entity after movement.
                    speed_component.speed = 0
