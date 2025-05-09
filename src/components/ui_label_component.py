from ecs.component import Component


class UILabelComponent(Component):
    def __init__(self, template: str, position: tuple[int, int]):
        super().__init__()

        self.position = position

        self.template = template
        self.text = ""
