from typing_extensions import override
from typing import List

from tcod import event

from ecs.system import System


class EventDispatchSystem(System):
    @override
    def __init__(self):
        super().__init__()

        self.event_queue: List[event.Event] = []

    @override
    def start():
        super().start()
    
    @override
    def stop():
        super().stop()

    @override
    def update(self):
        super().update()
        self.event_queue = list(event.get())

    def get_events(self) -> List[event.Event]:
        return self.event_queue