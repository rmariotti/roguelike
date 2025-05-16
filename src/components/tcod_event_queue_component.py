from tcod import event

from ecs.component import Component


class TCODEventQueueComponent(Component):
    event_queue: list[event.Event] = []
