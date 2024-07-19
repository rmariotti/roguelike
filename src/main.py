#!/usr/bin/env python3
from typing import Iterable

import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from ecs import Entity, EntityManager
from components import PositionComponent, SpeedComponent, DirectionComponent, RenderingComponent, MapComponent
from systems import MovementSystem, RenderingSystem


def main() -> None:
    """
    Application entry point.
    """
    # TODO: Load screen size from configuration file.
    screen_width, screen_height = (80, 50)
    map_width, map_height = (80, 45)

    tileset = tcod.tileset.load_tilesheet(
            # TODO: Hardcoded sting here.
            "../assets/fonts/dejavu10x10_gs_tc.png",
            32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = EventHandler()

    # Initialize player character, motionless at the center ofthe screen. 
    player_character_entity = Entity(
            PositionComponent(int(screen_width / 2), int(screen_height / 2)),
            SpeedComponent(0), DirectionComponent(0),
            RenderingComponent("@", (255, 255, 0)))
    npc = Entity(
            PositionComponent(int(screen_width / 3), int(screen_height / 3)),
            RenderingComponent("X", (255, 255, 255)))

    # Initialize game map.
    game_map = Entity(MapComponent(map_width, map_height))

    # Initialize ECS world.
    entity_manager = EntityManager([player_character_entity, npc, game_map])
    # Initialize systems.
    systems = []

    movement_system = MovementSystem(entity_manager)
    systems.append(movement_system)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Demo",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")

        # Initialize rendering systems.
        rendering_system = RenderingSystem(entity_manager, root_console, context)
        systems.append(rendering_system)

        while True:
            for event in tcod.event.wait():
                # TODO: Move event handling from here, maybe in a system?
                action = event_handler.dispatch(event)

                if action is None:
                    update_systems(systems) 

                if isinstance(action, MovementAction):
                    player_character_entity.get_component(SpeedComponent).speed = 1
                    update_systems(systems)
                    player_character_entity.get_component(SpeedComponent).speed = 0 
 
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


# TODO: Remove this function and build proper ECS world support.
def update_systems(systems: Iterable):
    """
    Helper function to update all systems in ECS world.
    """
    for system in systems:
        system.update()


if __name__ == "__main__":
    main()

