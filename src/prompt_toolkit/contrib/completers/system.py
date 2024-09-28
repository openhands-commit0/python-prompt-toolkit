from __future__ import annotations
from prompt_toolkit.completion.filesystem import ExecutableCompleter, PathCompleter
from prompt_toolkit.contrib.regular_languages.compiler import compile
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
__all__ = ['SystemCompleter']

class SystemCompleter(GrammarCompleter):
    """
    Completer for system commands.
    """

    def __init__(self) -> None:
        g = compile('\n                # First we have an executable.\n                (?P<executable>[^\\s]+)\n\n                # Ignore literals in between.\n                (\n                    \\s+\n                    ("[^"]*" | \'[^\']*\' | [^\'"]+ )\n                )*\n\n                \\s+\n\n                # Filename as parameters.\n                (\n                    (?P<filename>[^\\s]+) |\n                    "(?P<double_quoted_filename>[^\\s]+)" |\n                    \'(?P<single_quoted_filename>[^\\s]+)\'\n                )\n            ', escape_funcs={'double_quoted_filename': lambda string: string.replace('"', '\\"'), 'single_quoted_filename': lambda string: string.replace("'", "\\'")}, unescape_funcs={'double_quoted_filename': lambda string: string.replace('\\"', '"'), 'single_quoted_filename': lambda string: string.replace("\\'", "'")})
        super().__init__(g, {'executable': ExecutableCompleter(), 'filename': PathCompleter(only_directories=False, expanduser=True), 'double_quoted_filename': PathCompleter(only_directories=False, expanduser=True), 'single_quoted_filename': PathCompleter(only_directories=False, expanduser=True)})