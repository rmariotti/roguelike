from __future__ import annotations

from typing import TYPE_CHECKING
from collections import deque

from ecs.component import Component

if TYPE_CHECKING:
    from typing import Deque
    from ecs.entity import Entity


class SchedulerComponent(Component):
    ready_queue: Deque[Entity] = deque()
