#!/usr/bin/env python3
from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import tcod

from actions.input_event_handler import GameInputEventHandler
from actions.input_event_handler import UIInputEventHandler
from ecs.entity import Entity
from ecs.world import World
from systems.movement_system import MovementSystem
from systems.death_system import DeathSystem
from systems.rendering_system import RenderingSystem
from systems.fov_system import FovSystem
from systems.turn_system import TurnSystem
from systems.action_system import ActionSystem
from systems.ui_input_system import UiInputSystem
from systems.tcod_event_dispatch_system import EventDispatchSystem
from systems.ui_system import UISystem
from components.ui_label_component import UILabelComponent
from components.ui_bar_component import UIBarComponent
from components.needs_player_health_tag import NeedsPlayerHealthTag
from procgen.generate_level import generate_level
from procgen.generate_player_character import generate_player_character
from colors.ui_colors import UIColors

if TYPE_CHECKING:
    from ecs.system import System


def main() -> None:
    """Application entry point."""
    # TODO: Load screen size from configuration file.
    screen_width, screen_height = map_width, map_height = (80, 50)
    room_max_size, room_min_size, max_rooms = (10, 4, 4)

    tileset = tcod.tileset.load_tilesheet(
        # TODO: Hardcoded sting here.
        "assets/fonts/dejavu10x10_gs_tc.png",
        32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # Initialize ECS world.
    world = World()
    
    # Initialize player character, motionless at the center ofthe screen.
    player_character_entity = generate_player_character(
        (int(screen_width/2), int(screen_height/2))
    )

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

    # Initialize systems.
    systems = initialize_systems(world=world)


    # Build game UI.
    player_health_label = Entity(
        UILabelComponent(
            template="HP: {0}/{1}",
            position=(1, 47)
        ),
        NeedsPlayerHealthTag()
    )
    world.entities.append(player_health_label)

    player_health_bar = Entity(
        UIBarComponent(
            position=(1, 47),
            width=20,
            height=1,
            characters=1,
            background_color=UIColors.HEALTH_BAR_EMPTY.value.value,
            fill_color=UIColors.HEALTH_BAR_FILL.value.value
        ),
        NeedsPlayerHealthTag()
    )
    world.entities.append(player_health_bar)

    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=tileset,
            title="Roguelike Demo",
            vsync=True,
    ) as context:
        root_console = tcod.console.Console(
            screen_width, screen_height, order="F")

        # Initialize rendering systems.
        rendering_system = RenderingSystem(world, root_console, context)
        systems.append(rendering_system)

        while True:
            update_systems(systems)


# TODO: Remove this function and build proper ECS world support.
def update_systems(systems: Iterable) -> None:
    """Helper function to update all systems in ECS world."""
    for system in systems:
        system.update()


def initialize_systems(world: World) -> list[System]:
    """Helper function to initialize all systems in ECS world."""
    systems: list[System] = []

    # Initialize the tcod event handler.
    game_input_event_handler = GameInputEventHandler(world=world)
    ui_input_event_handler = UIInputEventHandler(world=world)

    event_dispatch_system = EventDispatchSystem()

    ui_input_system = UiInputSystem(
        world=world, event_handler=ui_input_event_handler,
        event_dispatcher=event_dispatch_system
    )
    action_system = ActionSystem(world)
    turn_system = TurnSystem(
        world=world, action_system=action_system,
        event_handler=game_input_event_handler,
        event_dispatcher=event_dispatch_system
    )

    movement_system = MovementSystem(world)
    death_system = DeathSystem(world)
    fov_system = FovSystem(world)
    ui_system = UISystem(world=world)

    systems.extend((
        event_dispatch_system, ui_input_system, action_system, turn_system,
        movement_system, death_system, fov_system, ui_system
    ))

    return systems


if __name__ == "__main__":
    main()
