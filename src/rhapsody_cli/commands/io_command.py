"""IO command group - dispatches to per-subcommand Action classes."""

from __future__ import annotations

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.io_action import IOExportAction, IOImportAction
from rhapsody_cli.commands.abstract_command import AbstractCommand


class IOCommand(AbstractCommand):
    """IO command group - handles io subcommands (import, export)."""

    def __init__(self, args: list[str]) -> None:
        """Initialize IOCommand and parse io subcommands.

        Args:
            args: Arguments after 'io' command
                (e.g., ['import', 'source.xmi', '--target', 'Root'])
        """
        super().__init__("io", args)

    def get_actions(self) -> list[AbstractAction]:
        """Return the io subcommand actions."""
        return [
            IOImportAction(),
            IOExportAction(),
        ]
