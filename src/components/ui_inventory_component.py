from ecs.component import Component


class UIInventoryComponent(Component):
    def __init__(self, panel_title: str | None):
        self.panel_title: str = panel_title or "<missing title>"
        self.cursor: None | int = None
