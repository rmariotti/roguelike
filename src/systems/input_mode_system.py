from __future__ import annotations

from typing_extensions import override
from typing import TYPE_CHECKING

from ecs.system import System
from components.input_mode_component import InputModeComponent
from inputs.input_action_mapper import InputActionMapper

if TYPE_CHECKING:
    from ecs.world import World
    from inputs.input_event_handler import InputEventHandler


class InputModeSystem(System):
    def __init__(
            self,
            world: World,
            input_action_mapper: InputActionMapper,
            game_input_event_handler: InputEventHandler,
            ui_input_event_handler: InputEventHandler
    ):
        self.world = world
        self.input_action_mapper = input_action_mapper
        self.game_input_event_handler = game_input_event_handler
        self.ui_input_event_handler = ui_input_event_handler

    @override
    def start(self):
        pass

    @override
    def stop(self):
        pass

    @override
    def update(self):
        input_mode_components = [
            e.get_component(InputModeComponent)

            for e in self.world.get_entities_with_components(
                InputModeComponent
            )
        ]

        for input_mode_component in input_mode_components:
            input_mode_component: InputModeComponent

            if (
                input_mode_component.input_mode ==
                input_mode_component.previous_input_mode
            ):
                return

            # Load current input mode.
            game_actions_mappings = self.input_action_mapper.get_game_actions(
                input_mode_component.input_mode
            )

            ui_actions_mappings = self.input_action_mapper.get_ui_actions(
                input_mode_component.input_mode
            )

            if game_actions_mappings is not None:
                self.game_input_event_handler.key_action_map = (
                    game_actions_mappings
                )

            if ui_actions_mappings is not None:
                self.ui_input_event_handler.key_action_map = (
                    ui_actions_mappings
                )

            input_mode_component.previous_input_mode = (
                input_mode_component.input_mode
            )
