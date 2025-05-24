from messages.message_categories import MessageCategory
from .ui_colors import UIColors


class MessagePresentation:
    @staticmethod
    def get_message_color_by_category(
        message_category: MessageCategory
    ) -> tuple[int, int, int]:
        return {
            MessageCategory.INFO: UIColors.TEXT,
            MessageCategory.WARNING: UIColors.WARNING,
            MessageCategory.SUCCESS: UIColors.SUCCESS,
            MessageCategory.SYSTEM: UIColors.WARNING,
            MessageCategory.IMPOSSIBLE: UIColors.IMPOSSIBLE
        }.get(message_category, UIColors.TEXT)
