from typing_extensions import override

from tcod.context import Context

from ecs.system import System
from ecs.world import World
from inputs.input_event_handler import UIInputEventHandler
from components.is_player_character_tag import IsPlayerCharacterTag
from components.tcod_event_queue_component import TCODEventQueueComponent
from utils.ecs_helpers import get_default_component


class UIInputSystem(System):
    def __init__(
            self, world: World, event_handler: UIInputEventHandler,
            context: Context
    ):
        self.world: World = world
        self.event_handler: UIInputEventHandler = event_handler
        self.context: Context = context

    @override
    def start(self):
        return super().start()

    @override
    def stop(self):
        return super().stop()

    @override
    def update(self):
        tcod_event_queue: TCODEventQueueComponent = get_default_component(
            world=self.world,
            component_type=TCODEventQueueComponent
        )

        player_entity = self.world.get_entities_with_components(
            IsPlayerCharacterTag
        )

        if player_entity:
            for tcod_event in tcod_event_queue.event_queue:
                self.context.convert_event(tcod_event)
                action = self.event_handler.dispatch(tcod_event)

                if action:
                    action.perform()
                    break
