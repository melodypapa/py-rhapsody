"""Element command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.element_action import (
    ElementAddAction,
    ElementDeleteAction,
    ElementQueryAction,
    ElementViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ElementCommand(AbstractCommand):
    """Element command group - handles element subcommands (add, view, query, delete)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize ElementCommand and parse element subcommands.

        Args:
            args: Arguments after 'element' command
                (e.g., ['add', '--type', 'class', '--name', 'MyClass'])
        """
        super().__init__("element", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the element subcommand actions."""
        return [
            ElementAddAction(),
            ElementViewAction(),
            ElementQueryAction(),
            ElementDeleteAction(),
        ]
