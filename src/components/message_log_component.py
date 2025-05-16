from __future__ import annotations

from typing import TYPE_CHECKING

from ecs.component import Component

if TYPE_CHECKING:
    from messages.message_log import MessageLog


class MessageLogComponent(Component):
    def __init__(
            self,
            message_log: MessageLog
    ):
        self.message_log: MessageLog = message_log
