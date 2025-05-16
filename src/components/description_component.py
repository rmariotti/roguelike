from ecs.component import Component


class DescriptionComponent(Component):
    def __init__(self, name: str = "entity", description: str = "an entity"):
        self.name = name
        self.description = description
