#!/usr/bin/env python3
from typing import Iterable

import tcod

from actions import EventHandler
from ecs import Entity, EntityManager
from components import (
    PositionComponent, SpeedComponent, DirectionComponent,
    RenderingComponent, IsPlayerCharacterTag)
from systems import MovementSystem, RenderingSystem, EventSystem, FovSystem
from utils import Direction
from procgen import generate_level


def main() -> None:
    """Application entry point."""
    # TODO: Load screen size from configuration file.
    screen_width, screen_height = map_width, map_height = (80, 50)
    room_max_size, room_min_size, max_rooms = (10, 6, 30)

    tileset = tcod.tileset.load_tilesheet(
            # TODO: Hardcoded sting here.
            "../assets/fonts/dejavu10x10_gs_tc.png",
            32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = EventHandler()

    # Initialize player character, motionless at the center ofthe screen. 
    player_character_entity = Entity(
            PositionComponent(int(screen_width / 2), int(screen_height / 2)),
            IsPlayerCharacterTag(),
            SpeedComponent(0), DirectionComponent(Direction.NORTH),
            RenderingComponent("@", (255, 255, 0)))
    npc = Entity(
            PositionComponent(int(screen_width / 3), int(screen_height / 3)),
            RenderingComponent("X", (255, 255, 255)))

    # Initialize game map.
    game_map = Entity(generate_level(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height
    ))

    # Initialize ECS world.
    entity_manager = EntityManager([player_character_entity, npc, game_map])
    # Initialize systems.
    systems = []

    event_system = EventSystem(entity_manager, event_handler)
    systems.append(event_system)

    movement_system = MovementSystem(entity_manager)
    systems.append(movement_system)

    fov_system = FovSystem(entity_manager)
    systems.append(fov_system)

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
            update_systems(systems) 

# TODO: Remove this function and build proper ECS world support.
def update_systems(systems: Iterable):
    """Helper function to update all systems in ECS world."""
    for system in systems:
        system.update()


if __name__ == "__main__":
    main()
