"""
Filters that accept a `Application` as argument.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, cast
from prompt_toolkit.application.current import get_app
from prompt_toolkit.cache import memoized
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.selection import SelectionType
from .base import Condition, Filter
if TYPE_CHECKING:
    from prompt_toolkit.layout.layout import FocusableElement
__all__ = ['has_arg', 'has_completions', 'completion_is_selected', 'has_focus', 'buffer_has_focus', 'has_selection', 'has_suggestion', 'has_validation_error', 'is_done', 'is_read_only', 'is_multiline', 'renderer_height_is_known', 'in_editing_mode', 'in_paste_mode', 'vi_mode', 'vi_navigation_mode', 'vi_insert_mode', 'vi_insert_multiple_mode', 'vi_replace_mode', 'vi_selection_mode', 'vi_waiting_for_text_object_mode', 'vi_digraph_mode', 'vi_recording_macro', 'emacs_mode', 'emacs_insert_mode', 'emacs_selection_mode', 'shift_selection_mode', 'is_searching', 'control_is_searchable', 'vi_search_direction_reversed']

def has_focus(value: FocusableElement) -> Condition:
    """
    Enable when this buffer has the focus.
    """
    @Condition
    def has_focus() -> bool:
        return get_app().layout.current_control == value
    return has_focus

@Condition
def buffer_has_focus() -> bool:
    """
    Enabled when the currently focused control is a `BufferControl`.
    """
    from prompt_toolkit.layout.controls import BufferControl
    return isinstance(get_app().layout.current_control, BufferControl)

@Condition
def has_selection() -> bool:
    """
    Enable when the current buffer has a selection.
    """
    return bool(get_app().current_buffer.selection_state)

@Condition
def has_suggestion() -> bool:
    """
    Enable when the current buffer has a suggestion.
    """
    return bool(get_app().current_buffer.suggestion)

@Condition
def has_completions() -> bool:
    """
    Enable when the current buffer has completions.
    """
    return bool(get_app().current_buffer.complete_state)

@Condition
def completion_is_selected() -> bool:
    """
    True when the user selected a completion.
    """
    complete_state = get_app().current_buffer.complete_state
    return bool(complete_state and complete_state.current_completion)

@Condition
def is_read_only() -> bool:
    """
    True when the current buffer is read only.
    """
    return get_app().current_buffer.read_only()

@Condition
def is_multiline() -> bool:
    """
    True when the current buffer has been marked as multiline.
    """
    return get_app().current_buffer.multiline

@Condition
def has_validation_error() -> bool:
    """Current buffer has validation error."""
    return bool(get_app().current_buffer.validation_error)

@Condition
def has_arg() -> bool:
    """Enable when the input processor has an 'arg'."""
    return get_app().key_processor.arg is not None

@Condition
def is_done() -> bool:
    """
    True when the CLI is returning, aborting or exiting.
    """
    return get_app().is_done

@Condition
def renderer_height_is_known() -> bool:
    """
    Only True when the renderer knows it's real height.

    (On VT100 terminals, we have to wait for a CPR response, before we can be
    sure of the available height between the cursor position and the bottom of
    the terminal. And usually it's nicer to wait with drawing bottom toolbars
    until we receive the height, in order to avoid flickering -- first drawing
    somewhere in the middle, and then again at the bottom.)
    """
    return get_app().renderer.height_is_known

@Condition
def in_paste_mode() -> bool:
    """When we are pasting text from the clipboard."""
    return get_app().paste_mode

def in_editing_mode(editing_mode: EditingMode) -> Filter:
    """
    Check whether a given editing mode is active. (Vi or Emacs.)
    """
    @Condition
    def in_editing_mode_filter() -> bool:
        return get_app().editing_mode == editing_mode
    return in_editing_mode_filter

@Condition
def vi_navigation_mode() -> bool:
    """
    Active when the set for Vi navigation key bindings are active.
    """
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.input_mode == 'navigation'

@Condition
def vi_recording_macro() -> bool:
    """When recording a Vi macro."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.recording_register is not None

@Condition
def emacs_mode() -> bool:
    """When the Emacs bindings are active."""
    return get_app().editing_mode == EditingMode.EMACS

@Condition
def emacs_insert_mode() -> bool:
    """When Emacs is in insert mode."""
    app = get_app()
    return app.editing_mode == EditingMode.EMACS and not bool(app.current_buffer.selection_state)

@Condition
def emacs_selection_mode() -> bool:
    """When Emacs has a selection."""
    app = get_app()
    return app.editing_mode == EditingMode.EMACS and bool(app.current_buffer.selection_state)

@Condition
def vi_mode() -> bool:
    """When the Vi bindings are active."""
    return get_app().editing_mode == EditingMode.VI

# Create an alias for vi_mode to avoid circular imports
vi_mode = vi_mode

@Condition
def vi_insert_mode() -> bool:
    """When Vi is in insert mode."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.input_mode == 'insert'

@Condition
def vi_insert_multiple_mode() -> bool:
    """When Vi is in insert mode, entering multiple characters."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.input_mode == 'insert_multiple'

@Condition
def vi_replace_mode() -> bool:
    """When Vi is in replace mode."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.input_mode == 'replace'

@Condition
def vi_selection_mode() -> bool:
    """When Vi has a selection."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.operator_func is not None

@Condition
def vi_waiting_for_text_object_mode() -> bool:
    """When Vi is waiting for a text object."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.waiting_for_text_object

@Condition
def vi_digraph_mode() -> bool:
    """When Vi is in digraph mode."""
    app = get_app()
    return app.editing_mode == EditingMode.VI and app.vi_state.waiting_for_digraph

@Condition
def is_searching() -> bool:
    """When we are searching."""
    return get_app().current_search_state is not None

@Condition
def control_is_searchable() -> bool:
    """When the current UIControl is searchable."""
    from prompt_toolkit.layout.controls import BufferControl, SearchBufferControl
    control = get_app().layout.current_control
    return isinstance(control, (BufferControl, SearchBufferControl))

@Condition
def vi_search_direction_reversed() -> bool:
    """When the '/' and '?' key bindings for Vi-style searching have been reversed."""
    return get_app().reverse_vi_search_direction()

@Condition
def shift_selection_mode() -> bool:
    """When shift has been pressed while selecting text."""
    app = get_app()
    return bool(app.current_buffer.selection_state and app.current_buffer.selection_state.type == SelectionType.CHARACTERS)