#!/usr/bin/env python3
from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import tcod

from ecs.entity import Entity
from ecs.world import World

from ecs.system import System
from systems.action_execution_system import ActionExecutionSystem
from systems.death_system import DeathSystem
from systems.energy_system import EnergySystem
from systems.fov_system import FovSystem
from systems.movement_system import MovementSystem
from systems.ui_message_log_history_render_system import (
    UIMessageLogHistoryRenderSystem
)
from systems.render_manager_system import RenderManagerSystem
from systems.render_system import RenderSystem
from systems.tcod_event_polling_system import TCODEventPollingSystem
from systems.ui_input_system import UIInputSystem
from systems.ui_system import UISystem
from systems.input_mode_system import InputModeSystem

from components.is_default_tag import DefaultTag
from components.message_log_component import MessageLogComponent
from components.needs_player_health_tag import NeedsPlayerHealthTag
from components.scheduler_component import SchedulerComponent
from components.tcod_event_queue_component import TCODEventQueueComponent
from components.ui_bar_component import UIBarComponent
from components.ui_label_component import UILabelComponent
from components.ui_message_log_component import UIMessageLogComponent
from components.ui_message_log_history_component import (
    UIMessageLogHistoryComponent
)
from components.input_mode_component import InputModeComponent
from components.ui_mouse_location_component import UIMouseLocationComponent
from components.ui_names_at_mouse_location_tag import UINamesAtMouseLocationTag

from inputs.input_event_handler import (
    GameInputEventHandler,
    UIInputEventHandler,
    InputEventHandler
)
from inputs.input_action_mapper import InputActionMapper
from inputs.setup_input_bindings import setup_input_bindings

from messages.message_log import MessageLog
from procgen.generate_level import generate_level
from procgen.generate_player_character import generate_player_character
from colors.ui_colors import UIColors

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.context import Context


def main() -> None:
    """Application entry point."""
    screen_width, screen_height = map_width, map_height = (80, 50)
    room_max_size, room_min_size, max_rooms = (10, 4, 4)

    tileset = tcod.tileset.load_tilesheet(
        "assets/fonts/dejavu10x10_gs_tc.png",
        32, 8, tcod.tileset.CHARMAP_TCOD
    )

    world = World()

    # Core game entities
    player_character_entity = generate_player_character(
        (screen_width // 2, screen_height // 2)
    )
    game_map = Entity(generate_level(
        world=world,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height
    ))
    action_scheduler = Entity(
        DefaultTag(SchedulerComponent),
        SchedulerComponent()
    )
    tcod_event_queue = Entity(
        DefaultTag(TCODEventQueueComponent),
        TCODEventQueueComponent()
    )
    input_modes = Entity(
        InputModeComponent(),
        DefaultTag(InputModeComponent)
    )

    # Add core entities to the world
    world.entities.extend([
        player_character_entity,
        game_map,
        action_scheduler,
        tcod_event_queue,
        input_modes
    ])

    ui_input_event_handler = UIInputEventHandler(world=world)
    game_input_event_handler = GameInputEventHandler(world=world)
    input_action_mapper = InputActionMapper()

    setup_input_bindings(
        mapper=input_action_mapper,
        world=world,
        player=player_character_entity
    )

    systems = systems_initialize(
        world=world,
        game_input_event_handler=game_input_event_handler
    )

    # UI Entities
    mouse = Entity(
        DefaultTag(UIMouseLocationComponent),
        DefaultTag(UINamesAtMouseLocationTag),
        UIMouseLocationComponent(),
        UINamesAtMouseLocationTag()
    )
    world.entities.append(mouse)

    player_health_label = Entity(
        UILabelComponent(
            template="HP: {0}/{1}",
            position=(1, 47),
            text_color=UIColors.TEXT
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
            background_color=UIColors.HEALTH_BAR_EMPTY,
            fill_color=UIColors.HEALTH_BAR_FILL
        ),
        NeedsPlayerHealthTag()
    )
    world.entities.append(player_health_bar)

    message_log = MessageLog()
    message_log_entity = Entity(
        DefaultTag(MessageLogComponent),
        MessageLogComponent(message_log=message_log),
        UIMessageLogComponent(position=(21, 45), width=40, height=5),
        DefaultTag(UIMessageLogHistoryComponent),
        UIMessageLogHistoryComponent()
    )
    world.entities.append(message_log_entity)

    message_log.add_message("Hello world!")

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Roguelike Demo",
        vsync=True,
    ) as context:
        console = tcod.console.Console(screen_width, screen_height, order="F")
        tcod_systems = tcod_systems_initialize(
            world=world, context=context, console=console,
            game_input_event_handler=game_input_event_handler,
            ui_input_event_handler=ui_input_event_handler,
            input_action_mapper=input_action_mapper
        )
        systems.extend(tcod_systems)

        while True:
            systems_update(systems)


def systems_initialize(
        world: World, game_input_event_handler: InputEventHandler
) -> list[System]:
    """Initialize core game systems."""
    systems: list[System] = []

    systems.extend([
        EnergySystem(world),
        ActionExecutionSystem(world, game_input_event_handler),
        MovementSystem(world),
        DeathSystem(world),
        FovSystem(world),
        UISystem(world),
    ])

    return systems


def tcod_systems_initialize(
        world: World, context: Context, console: Console,
        ui_input_event_handler: InputEventHandler,
        game_input_event_handler: InputEventHandler,
        input_action_mapper: InputActionMapper,
) -> list[System]:
    """Initialize TCOD-specific systems."""
    systems: list[System] = []

    systems.extend([
        TCODEventPollingSystem(world),
        UIInputSystem(
            world, event_handler=ui_input_event_handler, context=context
        ),
        InputModeSystem(
            world=world,
            input_action_mapper=input_action_mapper,
            game_input_event_handler=game_input_event_handler,
            ui_input_event_handler=ui_input_event_handler
        ),
        RenderSystem(world, console, context),
        UIMessageLogHistoryRenderSystem(
            world=world,
            root_console=console,
            context=context
        ),
        RenderManagerSystem(console=console, context=context)
    ])

    return systems


def systems_update(systems: Iterable[System]) -> None:
    """Call update() on all systems."""
    for system in systems:
        system.update()


if __name__ == "__main__":
    main()
