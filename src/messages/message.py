from .message_categories import MessageCategory


class Message:
    def __init__(
            self, text: str,
            message_category: MessageCategory
    ):
        self.plain_text = text
        self.message_category = message_category
        self.count = 1

    @property
    def full_text(self) -> str:
        """
        Returns the message with the count at the end of it.
        """
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"

        return self.plain_text
