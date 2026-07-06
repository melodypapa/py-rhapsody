"""Project-related CLI commands."""

from __future__ import annotations

import click

from py_rhapsody.cli.context import RhapsodyContext
from py_rhapsody.cli.formatters import OutputFormatter
from py_rhapsody.exceptions import RhapsodyConnectionError


@click.group()
def project() -> None:
    """Manage Rhapsody projects."""
    pass


@project.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.pass_obj
def open(ctx: RhapsodyContext, project_path: str) -> None:
    """Open a Rhapsody project file."""
    try:
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


@project.command()
@click.pass_obj
def list(ctx: RhapsodyContext) -> None:
    """List open projects."""
    try:
        ctx.connect("attach")
        assert ctx.app is not None  # For mypy type narrowing
        projects = ctx.app.getProjects()

        if not projects or len(projects) == 0:
            click.echo("No open projects")
            return

        rows = []
        for proj in projects:
            rows.append([proj.getName(), proj.getPath()])

        output = OutputFormatter.table(["Name", "Path"], rows)
        click.echo(output)
    except click.Abort:
        raise
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


@project.command()
@click.pass_obj
def close(ctx: RhapsodyContext) -> None:
    """Close active project."""
    try:
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
