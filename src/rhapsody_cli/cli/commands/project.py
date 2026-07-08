"""Project-related CLI commands using argparse architecture."""

from __future__ import annotations

import sys

from rhapsody_cli.cli.abstract_command import AbstractCommand
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import RhapsodyConnectionError


class OpenProjectCommand(AbstractCommand):
    """Command: Open a Rhapsody project file."""

    def execute(self, project_path: str) -> None:  # type: ignore[override]
        """Execute the open command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            ctx.open_project(project_path)
            print(f"Opened project: {project_path}")
        except RhapsodyConnectionError as e:
            print(f"Connection error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class ListProjectsCommand(AbstractCommand):
    """Command: List open projects."""

    def execute(self) -> None:  # type: ignore[override]
        """Execute the list command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            assert ctx.app is not None
            projects = ctx.app.getProjects()

            if not projects or len(projects) == 0:
                print("No open projects")
                return

            rows = []
            for proj in projects:
                rows.append([proj.getName(), proj.getFilename()])

            output = OutputFormatter.table(["Name", "Path"], rows)
            print(output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class CloseProjectCommand(AbstractCommand):
    """Command: Close active project."""

    def execute(self) -> None:  # type: ignore[override]
        """Execute the close command."""
        try:
            ctx = RhapsodyContext()
            if ctx.project is None:
                print("No active project")
                return
            ctx.close_project()
            print("Project closed")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class NewProjectCommand(AbstractCommand):
    """Command: Create a new empty Rhapsody project."""

    def execute(self, project_location: str, project_name: str) -> None:  # type: ignore[override]
        """Execute the new command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            ctx.create_project(project_location, project_name)
            print(f"Created project: {project_name} at {project_location}")
        except RhapsodyConnectionError as e:
            print(f"Connection error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
