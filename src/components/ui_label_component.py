from ecs.component import Component
from colors.ui_colors import UIColors


class UILabelComponent(Component):
    def __init__(
            self,
            template: str,
            position: tuple[int, int],
            text_color: tuple[int, int, int] = UIColors.TEXT
    ):
        self.position = position
        self.text_color = text_color

        self.template = template
        self.text = ""
