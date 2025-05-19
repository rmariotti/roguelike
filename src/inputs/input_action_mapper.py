from typing import Dict

import tcod.event

from inputs.input_modes import InputModes
from actions.action import Action


BindingsDict = Dict[InputModes, Dict[tcod.event.KeySym, Action]]


class InputActionMapper:
    def __init__(self):
        self._game_bindings: BindingsDict = {}
        self._ui_bindings: BindingsDict = {}

    def initialize_mode(self, mode: InputModes):
        self._game_bindings[mode] = {}
        self._ui_bindings[mode] = {}

    def _register(
            self,
            bindings: Dict,
            mode: InputModes,
            key: tcod.event.KeySym,
            action: Action
    ):
        bindings.setdefault(mode, {})[key] = action

    def register_game(
            self,
            mode: InputModes,
            key: tcod.event.KeySym,
            action: Action
    ):
        self._register(self._game_bindings, mode, key, action)

    def register_ui(
            self,
            mode: InputModes,
            key: tcod.event.KeySym,
            action: Action
    ):
        self._register(self._ui_bindings, mode, key, action)

    def get_game_actions(
            self,
            mode: InputModes
    ) -> Dict[tcod.event.KeySym, Action] | None:
        return self._game_bindings.get(mode)

    def get_ui_actions(
            self,
            mode: InputModes
    ) -> Dict[tcod.event.KeySym, Action] | None:
        return self._ui_bindings.get(mode)
