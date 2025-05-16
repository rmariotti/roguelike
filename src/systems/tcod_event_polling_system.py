from typing_extensions import override
from tcod import event

from ecs.system import System
from ecs.world import World
from components.tcod_event_queue_component import TCODEventQueueComponent
from utils.ecs_helpers import get_default_component


class TCODEventPollingSystem(System):
    @override
    def __init__(self, world: World):
        self.world = world

    @override
    def start(self):
        super().start()

    @override
    def stop(self):
        super().stop()

    @override
    def update(self):
        tcod_event_queue: TCODEventQueueComponent = get_default_component(
            world=self.world,
            component_type=TCODEventQueueComponent
        )

        tcod_event_queue.event_queue = list(event.get())
