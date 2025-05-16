from __future__ import annotations

from typing import TYPE_CHECKING

import events.game_events

if TYPE_CHECKING:
    from ecs.world import World
    from events.event import Event
    from actions.action import Action


class GameEventHandler():
    def __init__(self, world: World):
        self.world = world

        self.event_action_map = {
            events.game_events.GameStart: None
        }

    def dispatch(self, event: Event) -> Action:
        return
