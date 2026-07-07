"""Project-related CLI commands using class-based architecture."""

from __future__ import annotations

import click

from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import RhapsodyConnectionError


class BaseProjectCommand(click.Command):
    """Base class for project commands."""

    pass


class OpenProjectCommand(BaseProjectCommand):
    """Command: Open a Rhapsody project file."""

    def __init__(self) -> None:
        super().__init__(
            name="open",
            help="Open a Rhapsody project file.",
            callback=self.execute,
            params=[
                click.Argument(["project_path"], type=click.Path(exists=True)),
            ],
        )

    def execute(self, project_path: str) -> None:
        """Execute the open command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            ctx.open_project(project_path)
            click.echo(f"Opened project: {project_path}")
        except click.Abort:
            raise
        except RhapsodyConnectionError as e:
            click.echo(f"Connection error: {e}", err=True)
            raise click.Abort() from e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class ListProjectsCommand(BaseProjectCommand):
    """Command: List open projects."""

    def __init__(self) -> None:
        super().__init__(
            name="list",
            help="List open projects.",
            callback=self.execute,
            params=[],
        )

    def execute(self) -> None:
        """Execute the list command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            assert ctx.app is not None
            projects = ctx.app.getProjects()

            if not projects or len(projects) == 0:
                click.echo("No open projects")
                return

            rows = []
            for proj in projects:
                rows.append([proj.getName(), proj.getFilename()])

            output = OutputFormatter.table(["Name", "Path"], rows)
            click.echo(output)
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class CloseProjectCommand(BaseProjectCommand):
    """Command: Close active project."""

    def __init__(self) -> None:
        super().__init__(
            name="close",
            help="Close active project.",
            callback=self.execute,
            params=[],
        )

    def execute(self) -> None:
        """Execute the close command."""
        try:
            ctx = RhapsodyContext()
            if ctx.project is None:
                click.echo("No active project")
                return
            ctx.close_project()
            click.echo("Project closed")
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class NewProjectCommand(BaseProjectCommand):
    """Command: Create a new empty Rhapsody project."""

    def __init__(self) -> None:
        super().__init__(
            name="new",
            help="Create a new empty Rhapsody project.",
            callback=self.execute,
            params=[
                click.Argument(["project_location"], type=click.Path()),
                click.Argument(["project_name"]),
            ],
        )

    def execute(self, project_location: str, project_name: str) -> None:
        """Execute the new command."""
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            ctx.create_project(project_location, project_name)
            click.echo(f"Created project: {project_name} at {project_location}")
        except click.Abort:
            raise
        except RhapsodyConnectionError as e:
            click.echo(f"Connection error: {e}", err=True)
            raise click.Abort() from e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class ProjectCommandGroup(click.Group):
    """Command group for project operations."""

    def __init__(self) -> None:
        super().__init__(
            name="project",
            help="Manage Rhapsody projects.",
            invoke_without_command=False,
        )
        self.add_command(OpenProjectCommand())
        self.add_command(ListProjectsCommand())
        self.add_command(CloseProjectCommand())
        self.add_command(NewProjectCommand())


project = ProjectCommandGroup()
