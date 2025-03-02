"""
Mouse events.


How it works
------------

The renderer has a 2 dimensional grid of mouse event handlers.
(`prompt_toolkit.layout.MouseHandlers`.) When the layout is rendered, the
`Window` class will make sure that this grid will also be filled with
callbacks. For vt100 terminals, mouse events are received through stdin, just
like any other key press. There is a handler among the key bindings that
catches these events and forwards them to such a mouse event handler. It passes
through the `Window` class where the coordinates are translated from absolute
coordinates to coordinates relative to the user control, and there
`UIControl.mouse_handler` is called.
"""
from __future__ import annotations
from enum import Enum
from .data_structures import Point
__all__ = ['MouseEventType', 'MouseButton', 'MouseModifier', 'MouseEvent']

class MouseEventType(Enum):
    MOUSE_UP = 'MOUSE_UP'
    MOUSE_DOWN = 'MOUSE_DOWN'
    SCROLL_UP = 'SCROLL_UP'
    SCROLL_DOWN = 'SCROLL_DOWN'
    MOUSE_MOVE = 'MOUSE_MOVE'

class MouseButton(Enum):
    LEFT = 'LEFT'
    MIDDLE = 'MIDDLE'
    RIGHT = 'RIGHT'
    NONE = 'NONE'
    UNKNOWN = 'UNKNOWN'

class MouseModifier(Enum):
    SHIFT = 'SHIFT'
    ALT = 'ALT'
    CONTROL = 'CONTROL'

class MouseEvent:
    """
    Mouse event, sent to `UIControl.mouse_handler`.

    :param position: `Point` instance.
    :param event_type: `MouseEventType`.
    """

    def __init__(self, position: Point, event_type: MouseEventType, button: MouseButton, modifiers: frozenset[MouseModifier]) -> None:
        self.position = position
        self.event_type = event_type
        self.button = button
        self.modifiers = modifiers

    def __repr__(self) -> str:
        return 'MouseEvent({!r},{!r},{!r},{!r})'.format(self.position, self.event_type, self.button, self.modifiers)