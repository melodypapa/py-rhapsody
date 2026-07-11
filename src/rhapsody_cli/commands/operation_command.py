"""Operation command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.operation_action import (
    OperationCreateAction,
    OperationDeleteAction,
    OperationListAction,
    OperationUpdateAction,
    OperationViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class OperationCommand(AbstractCommand):
    """Operation command group - handles operation subcommands (create, delete, view, list, update)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize OperationCommand and parse operation subcommands.

        Args:
            args: Arguments after 'operation' command
                (e.g., ['create', '--path', 'Sensors/Cls', '{"name":"readValue"}'])
        """
        super().__init__("operation", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the operation subcommand actions."""
        return [
            OperationCreateAction(),
            OperationDeleteAction(),
            OperationViewAction(),
            OperationListAction(),
            OperationUpdateAction(),
        ]
