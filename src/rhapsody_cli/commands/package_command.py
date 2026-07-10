"""Package command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.package_action import (
    PackageCreateAction,
    PackageDeleteAction,
    PackageListAction,
    PackageUpdateAction,
    PackageViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class PackageCommand(AbstractCommand):
    """Package command group - handles package subcommands (create, delete, view, list)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize PackageCommand and parse package subcommands.

        Args:
            args: Arguments after 'package' command
                (e.g., ['create', '--path', 'Sensors', '{"name":"Temp"}'])
        """
        super().__init__("package", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the package subcommand actions."""
        return [
            PackageCreateAction(),
            PackageDeleteAction(),
            PackageViewAction(),
            PackageListAction(),
            PackageUpdateAction(),
        ]
