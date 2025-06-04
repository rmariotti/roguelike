from ecs.entity import Entity
from components.queue_component import QueueComponent


class SchedulerComponent(QueueComponent[Entity]):
    def __init__(self):
        super().__init__(Entity)
