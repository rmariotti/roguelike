from __future__ import annotations

from typing import override

import tcod
import libtcodpy

from ecs.world import World
from ecs.system import System
from components.message_log_component import MessageLogComponent
from components.ui_message_log_history_component import (
    UIMessageLogHistoryComponent,
)
from utils.render_helpers import render_message_log


class UIMessageLogHistoryRenderSystem(System):
    """Renders the message log history in tcod ui."""
    def __init__(
            self, world: World, root_console: tcod.console.Console,
            context: tcod.context.Context
    ):
        self.world: World = world
        self.root_console: tcod.console.Console = root_console
        self.log_console: tcod.console.Console | None = None
        self.context: tcod.context.Context = context

    @override
    def start(self):
        pass

    @override
    def stop(self):
        pass

    @override
    def update(self):
        # Get all message history logs.
        message_log_history_entities = (
            self.world.get_entities_with_components(
                UIMessageLogHistoryComponent,
                MessageLogComponent
            )
        )

        # Get components.
        if message_log_history_entities:
            components = [
                (
                    e.get_component(UIMessageLogHistoryComponent),
                    e.get_component(MessageLogComponent)
                )
                for e in message_log_history_entities
            ]

        for ui_history_component, log_component in components:
            ui_history_component: UIMessageLogHistoryComponent
            log_component: MessageLogComponent

            if not ui_history_component.is_shown:
                return

            # Sync ui history component and log component.
            # TODO: The following lines of code should be in a
            # separate system. <RM, 17-5-2025>
            if not ui_history_component.length:
                ui_history_component.length = (
                    len(log_component.message_log.messages)
                )
                ui_history_component.cursor = (
                    ui_history_component.length - 1
                )

            # TODO: Remove hardcoded console size. <RM, 17-5-2025>
            self.log_console = tcod.console.Console(
                self.root_console.width - 6,
                self.root_console.height - 6
            )

            # Draw a frame with a custom banner title.
            self.log_console.draw_frame(
                0, 0, self.log_console.width, self.log_console.height
            )
            self.log_console.print_box(
                0, 0, self.log_console.width, 1,
                "┤Message history├", alignment=libtcodpy.CENTER
            )

            # Render the message log using the cursor parameter.
            render_message_log(
               self.log_console,
               1,
               1,
               self.log_console.width - 2,
               self.log_console.height - 2,
               log_component.message_log.messages[: ui_history_component.cursor + 1]
            )
            self.log_console.blit(self.root_console, 3, 3)
