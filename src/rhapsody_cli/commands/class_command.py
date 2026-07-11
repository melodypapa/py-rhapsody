"""Class command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.class_action import (
    ClassCreateAction,
    ClassDeleteAction,
    ClassLinkAction,
    ClassListAction,
    ClassUpdateAction,
    ClassViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ClassCommand(AbstractCommand):
    """Class command group - handles class subcommands (create, delete, view, list, link, update)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize ClassCommand and parse class subcommands.

        Args:
            args: Arguments after 'class' command
                (e.g., ['create', '--path', 'Sensors', '{"name":"Temp"}'])
        """
        super().__init__("class", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the class subcommand actions."""
        return [
            ClassCreateAction(),
            ClassDeleteAction(),
            ClassViewAction(),
            ClassListAction(),
            ClassLinkAction(),
            ClassUpdateAction(),
        ]
