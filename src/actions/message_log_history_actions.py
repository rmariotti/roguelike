from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

from .action import Action
from components.input_mode_component import InputModeComponent
from components.ui_message_log_history_component import (
    UIMessageLogHistoryComponent
)
from utils.ecs_helpers import get_default_component
from inputs.input_modes import InputModes

if TYPE_CHECKING:
    from ecs.entity import Entity
    from ecs.world import World


class OpenMessageLogHistory(Action):
    @override
    def perform(self):
        # Get default input mode component.
        input_mode_component = get_default_component(
            world=self.world,
            component_type=InputModeComponent
        )

        # Get message history log components.
        ui_message_log_history_components = [
            e.get_component(UIMessageLogHistoryComponent)

            for e in self.world.get_entities_with_components(
                UIMessageLogHistoryComponent
            )
        ]

        # Set log view input mode and show message history.
        if input_mode_component and ui_message_log_history_components:
            input_mode_component: InputModeComponent

            input_mode_component.input_mode = InputModes.LOG_VIEW

            for component in ui_message_log_history_components:
                component: UIMessageLogHistoryComponent

                component.is_shown = True


class CloseMessageLogHistory(Action):
    @override
    def perform(self):
        # Get default input mode component.
        input_mode_component = get_default_component(
            world=self.world,
            component_type=InputModeComponent
        )

        # Get message history log components.
        ui_message_log_history_components = [
            e.get_component(UIMessageLogHistoryComponent)

            for e in self.world.get_entities_with_components(
                UIMessageLogHistoryComponent
            )
        ]

        # Go back to default input mode.
        if input_mode_component and ui_message_log_history_components:
            input_mode_component: InputModeComponent

            input_mode_component.input_mode = InputModes.DEFAULT

            for component in ui_message_log_history_components:
                component: UIMessageLogHistoryComponent

                component.is_shown = False


class MessageLogHistoryMove(Action):
    def __init__(self, entity: Entity, world: World, adjust: int):
        super().__init__(entity, world)
        self.adjust = adjust

    @override
    def perform(self):
        # Get the cursor of each message log.
        ui_message_log_history_components = [
            e.get_component(UIMessageLogHistoryComponent)

            for e in self.world.get_entities_with_components(
                UIMessageLogHistoryComponent
            )
        ]

        for component in ui_message_log_history_components:
            component: UIMessageLogHistoryComponent

            if self.adjust < 0 and component.cursor == 0:
                # Only move from the top to the bottom when on the edge.
                component.cursor = component.length - 1
            elif self.adjust > 0 and component.cursor == component.length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the
                # history log.
                upper_bound = min(
                    component.cursor + self.adjust,
                    component.length - 1)

                component.cursor = max(0, upper_bound)


class MessageLogHistoryGoHome(Action):
    @override
    def perform(self):
        # Get the cursor of each message log.
        ui_message_log_history_components = [
            e.get_component(UIMessageLogHistoryComponent)

            for e in self.world.get_entities_with_components(
                UIMessageLogHistoryComponent
            )
        ]

        for component in ui_message_log_history_components:
            component: UIMessageLogHistoryComponent

            component.cursor = 0  # Move directly to the top message.


class MessageLogHistoryGoEnd(Action):
    @override
    def perform(self):
        # Get the cursor of each message log.
        ui_message_log_history_components = [
            e.get_component(UIMessageLogHistoryComponent)

            for e in self.world.get_entities_with_components(
                UIMessageLogHistoryComponent
            )
        ]

        for component in ui_message_log_history_components:
            component: UIMessageLogHistoryComponent

            component.cursor = component.length - 1
