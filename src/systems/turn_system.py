from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ecs.system import System
from components.is_player_character_tag import IsPlayerCharacterTag
from components.ai_component import AIComponent
from actions.input_event_handler import GameInputEventHandler

if TYPE_CHECKING:
    from systems.action_system import ActionSystem
    from systems.tcod_event_dispatch_system import EventDispatchSystem
    from ecs.entity import Entity
    from ecs.world import World
    from actions.action import Action


class TurnSystem(System):
    """Handles tcod event loop and performing actions on acting entities."""
    def __init__(
            self,
            world: World,
            action_system: ActionSystem,
            event_handler: GameInputEventHandler,
            event_dispatcher: EventDispatchSystem
    ):
        self.world = world
        self.action_system = action_system
        self.event_handler = event_handler
        self.event_dispatcher = event_dispatcher

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        # TODO: This service is at risk at beign an infinite loop, this method
        # needs to consume an action (or wait for input and then consume the
        # action). <RM, 2025-05-4>
        if not self.action_system.has_ready_actor():
            return

        acting_entity = self.action_system.get_ready_actor()

        # Handle player character action.
        if acting_entity.get_component(IsPlayerCharacterTag):
            # Wait for player input.
            for tcod_event in self.event_dispatcher.get_events():
                action = self.event_handler.dispatch(tcod_event)

                if action:
                    self.action_system.pop_ready_actor()
                    action.perform()
                    break

        # Handle entity AI action.
        else:
            action = self.get_ai_action(acting_entity)

            if action:
                action.perform()

            # Consume the action, otherwise the program loops.
            self.action_system.pop_ready_actor()

    def get_ai_action(self, entity: Entity) -> Action | None:
        ai_component: Optional[AIComponent] = entity.get_component(AIComponent)

        if ai_component:
            return ai_component.get_action(
                world=self.world, acting_entity=entity)

        else:
            return None
