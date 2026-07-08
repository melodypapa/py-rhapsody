"""Project command group - dispatches to per-subcommand Action classes."""

from __future__ import annotations

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.project_action import (
    ProjectCloseAction,
    ProjectListAction,
    ProjectNewAction,
    ProjectOpenAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ProjectCommand(AbstractCommand):
    """Project command group - handles project subcommands (open, list, close, new)."""

    def __init__(self, args: list[str]) -> None:
        """Initialize ProjectCommand and parse project subcommands.

        Args:
            args: Arguments after 'project' command
                (e.g., ['open', 'MyProject.rpy'])
        """
        super().__init__("project", args)

    def get_actions(self) -> list[AbstractAction]:
        """Return the project subcommand actions."""
        return [
            ProjectOpenAction(),
            ProjectListAction(),
            ProjectCloseAction(),
            ProjectNewAction(),
        ]
