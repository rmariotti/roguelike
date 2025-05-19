from ecs.component import Component
from inputs.input_modes import InputModes


class InputModeComponent(Component):
    """
    Keeps track of the active input mode.

    The `inputs.input_event_handler.InputEventHandler` uses the default
    `InputModeComponent` to activate and deactivate input sets.
    """
    def __init__(self, input_mode: InputModes = InputModes.DEFAULT):
        self.input_mode = input_mode
