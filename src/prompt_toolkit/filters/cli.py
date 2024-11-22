"""
For backwards-compatibility. keep this file.
(Many people are going to have key bindings that rely on this file.)
"""
from __future__ import annotations
from .app import (
    has_validation_error, has_arg, is_done, renderer_height_is_known,
    vi_navigation_mode, in_paste_mode, emacs_mode, emacs_insert_mode,
    vi_mode, is_searching, control_is_searchable, emacs_selection_mode,
    vi_digraph_mode, vi_waiting_for_text_object_mode, vi_selection_mode,
    vi_replace_mode, vi_insert_multiple_mode, vi_insert_mode, has_selection,
    has_completions, is_read_only, is_multiline, has_focus, in_editing_mode
)
__all__ = ['HasArg', 'HasCompletions', 'HasFocus', 'HasSelection', 'HasValidationError', 'IsDone', 'IsReadOnly', 'IsMultiline', 'RendererHeightIsKnown', 'InEditingMode', 'InPasteMode', 'ViMode', 'ViNavigationMode', 'ViInsertMode', 'ViInsertMultipleMode', 'ViReplaceMode', 'ViSelectionMode', 'ViWaitingForTextObjectMode', 'ViDigraphMode', 'EmacsMode', 'EmacsInsertMode', 'EmacsSelectionMode', 'IsSearching', 'HasSearch', 'ControlIsSearchable']
HasValidationError = lambda: has_validation_error
HasArg = lambda: has_arg
IsDone = lambda: is_done
RendererHeightIsKnown = lambda: renderer_height_is_known
ViNavigationMode = lambda: vi_navigation_mode
InPasteMode = lambda: in_paste_mode
EmacsMode = lambda: emacs_mode
EmacsInsertMode = lambda: emacs_insert_mode
ViMode = lambda: vi_mode
IsSearching = lambda: is_searching
HasSearch = lambda: is_searching
ControlIsSearchable = lambda: control_is_searchable
EmacsSelectionMode = lambda: emacs_selection_mode
ViDigraphMode = lambda: vi_digraph_mode
ViWaitingForTextObjectMode = lambda: vi_waiting_for_text_object_mode
ViSelectionMode = lambda: vi_selection_mode
ViReplaceMode = lambda: vi_replace_mode
ViInsertMultipleMode = lambda: vi_insert_multiple_mode
ViInsertMode = lambda: vi_insert_mode
HasSelection = lambda: has_selection
HasCompletions = lambda: has_completions
IsReadOnly = lambda: is_read_only
IsMultiline = lambda: is_multiline
HasFocus = has_focus
InEditingMode = in_editing_mode