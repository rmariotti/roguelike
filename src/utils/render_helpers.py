from __future__ import annotations

from typing import TYPE_CHECKING, Reversible
import textwrap

from colors.message_presentation import MessagePresentation

if TYPE_CHECKING:
    from tcod import Console
    from messages.message import Message
    from components.message_log_component import MessageLogComponent
    from components.ui_message_log_component import UIMessageLogComponent


def render_message_log_component(
        console: Console,
        message_log_component: MessageLogComponent,
        ui_message_log_component: UIMessageLogComponent
) -> None:
    render_message_log(
        console=console,
        x=ui_message_log_component.position[0],
        y=ui_message_log_component.position[1],
        width=ui_message_log_component.width,
        height=ui_message_log_component.height,
        messages=message_log_component.message_log.messages
    )

def render_message_log(
    console: Console,
    x: int,
    y: int,
    width: int,
    height: int,
    messages: Reversible[Message]
) -> None:
    """
    Render the messages provided.

    The `messages` are rendered statrting at the last message and working
    backwards.
    """
    y_offset = height - 1

    for message in reversed(messages):
        for line in reversed(textwrap.wrap(message.full_text, width)):
            console.print(
                x=x,
                y=y + y_offset,
                string=line,
                fg=MessagePresentation.get_message_color_by_category(
                    message_category=message.message_category
                )
            )

            y_offset -= 1
            if y_offset < 0:
                return  # No more space to print messages.
