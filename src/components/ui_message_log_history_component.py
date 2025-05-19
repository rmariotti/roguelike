from ecs.component import Component


class UIMessageLogHistoryComponent(Component):
    def __init__(self, is_shown: bool = False):
        self.is_shown: bool = is_shown
        self.length: None | int = None
        self.cursor: None | int = None
