#!/usr/bin/env python3
from typing import Iterable

import tcod

from actions.input_event_handler import InputEventHandler
from ecs.entity import Entity
from ecs.world import World
from components.position_component import PositionComponent 
from components.speed_component import SpeedComponent
from components.direction_component import DirectionComponent
from components.rendering_component import RenderingComponent
from components.is_player_character_tag import IsPlayerCharacterTag
from components.actor_component import ActorComponent
from systems.movement_system import MovementSystem
from systems.rendering_system import RenderingSystem
from systems.fov_system import FovSystem
from systems.turn_system import TurnSystem
from systems.action_system import ActionSystem
from utils.direction_enum import Direction
from procgen.generate_level import generate_level
from colors.palette import Palette


def main() -> None:
    """Application entry point."""
    # TODO: Load screen size from configuration file.
    screen_width, screen_height = map_width, map_height = (80, 50)
    room_max_size, room_min_size, max_rooms = (10, 4, 4)

    tileset = tcod.tileset.load_tilesheet(
        # TODO: Hardcoded sting here.
        "assets/fonts/dejavu10x10_gs_tc.png",
        32, 8, tcod.tileset.CHARMAP_TCOD)

    # Initialize ECS world.
    world = World()
    # Initialize systems.
    systems = []

    # Initialize player character, motionless at the center ofthe screen. 
    player_character_entity = Entity(
        ActorComponent(),
        PositionComponent(int(screen_width / 2), int(screen_height / 2)),
        IsPlayerCharacterTag(),
        SpeedComponent(0, 1), DirectionComponent(Direction.NORTH),
        RenderingComponent("@", Palette.ORANGE_BRIGHT.value))
    

    # Initialize game map.
    game_map = Entity(generate_level(
        world=world,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height
    ))

    # Populate systems and world.
    world.entities.extend([player_character_entity, game_map])

    # Initialize the tcod event handler.
    input_event_handler = InputEventHandler(world=world)

    action_system = ActionSystem(world)
    turn_system = TurnSystem(world, action_system, input_event_handler)
    systems.extend((action_system, turn_system))

    movement_system = MovementSystem(world)
    systems.append(movement_system)

    fov_system = FovSystem(world)
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
        rendering_system = RenderingSystem(world, root_console, context)
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
