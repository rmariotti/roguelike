from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ecs.system import System
from components.is_player_character_tag import IsPlayerCharacterTag
from components.ai_component import AIComponent
from components.scheduler_component import SchedulerComponent
from components.tcod_event_queue_component import TCODEventQueueComponent
from inputs.input_event_handler import GameInputEventHandler
from utils.ecs_helpers import get_default_component

if TYPE_CHECKING:
    from ecs.entity import Entity
    from ecs.world import World
    from actions.action import Action


class ActionExecutionSystem(System):
    """Handles tcod event loop and performing actions on acting entities."""
    def __init__(
            self,
            world: World,
            event_handler: GameInputEventHandler,
    ):
        self.world = world
        self.event_handler = event_handler

    def start(self):
        return super().start()

    def stop(self):
        return super().stop()

    def update(self) -> None:
        # Get actor ready queue.
        scheduler: SchedulerComponent = get_default_component(
            world=self.world,
            component_type=SchedulerComponent
        )

        # TODO: This service is at risk at beign an infinite loop, this method
        # needs to consume an action (or wait for input and then consume the
        # action). <RM, 2025-05-4>
        if not scheduler.ready_queue:
            return

        # The index-0 element always exist since `ready_queue` in not empty.
        acting_entity = scheduler.ready_queue[0]

        # Handle player character action.
        if acting_entity.get_component(IsPlayerCharacterTag):
            # Get input event queue for the current ui.
            input_event_queue: TCODEventQueueComponent = get_default_component(
                world=self.world,
                component_type=TCODEventQueueComponent
            )

            # Wait for player input.
            for input_event in input_event_queue.event_queue:
                action = self.event_handler.dispatch(input_event)

                if action:
                    scheduler.ready_queue.popleft()
                    action().perform()
                    break

        # Handle entity AI action.
        else:
            action = self._get_ai_action(acting_entity)

            if action:
                action.perform()

            # Consume the action, otherwise the program loops.
            scheduler.ready_queue.popleft()

    def _get_ai_action(self, entity: Entity) -> Action | None:
        ai_component: Optional[AIComponent] = entity.get_component(AIComponent)

        if ai_component:
            return ai_component.get_action(
                world=self.world, acting_entity=entity)

        else:
            return None
