from typing_extensions import override

from tcod.console import Console
from tcod.context import Context

from ecs.system import System


class RenderManagerSystem(System):
    """
    Presents output on the root console and clears it for the next frame.

    This system have to be updated after all the other render systems.
    """
    def __init__(self, console: Console, context: Context):
        self.console: Console = console
        self.context: Context = context

    @override
    def start(self):
        pass

    @override
    def stop(self):
        pass

    @override
    def update(self):
        self.context.present(self.console)
        self.console.clear()
