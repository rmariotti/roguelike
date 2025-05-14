from .message import Message
from .message_categories import MessageCategory


class MessageLog:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add_message(
        self, text: str,
        message_category: MessageCategory = MessageCategory.INFO,
        *, stack: bool = True
    ) -> None:
        """
        Adds a message to the log.
        `text` is the message text, `message_category` determines styling.
        If `stack` is True then the message can stack with a previous message
        of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(
                Message(text=text, message_category=message_category)
            )
