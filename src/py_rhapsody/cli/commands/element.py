"""Element-related CLI commands."""

from __future__ import annotations

import click

from py_rhapsody.cli.context import RhapsodyContext
from py_rhapsody.cli.formatters import OutputFormatter


@click.group()
def element() -> None:
    """Manage model elements."""
    pass


@element.command()
@click.option("--type", "element_type", required=True, help="Element type (class, actor, etc)")
@click.option("--name", required=True, help="Element name")
@click.pass_obj
def add(ctx: RhapsodyContext, element_type: str, name: str) -> None:
    """Add a new element to the project."""
    if ctx.project is None:
        click.echo("Error: No active project. Use 'project open' first.", err=True)
        raise click.Abort()

    try:
        root = ctx.project.getRoot()  # type: ignore[attr-defined]
        if element_type.lower() == "class":
            root.createClass(name)
        elif element_type.lower() == "actor":
            root.createActor(name)
        elif element_type.lower() == "package":
            root.createPackage(name)
        else:
            click.echo(f"Error: Unknown element type '{element_type}'", err=True)
            raise click.Abort()

        click.echo(f"Created {element_type}: {name}")
    except click.Abort:
        raise
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


@element.command()
@click.option("--path", required=True, help="Element path (e.g., Root::MyClass)")
@click.pass_obj
def view(ctx: RhapsodyContext, path: str) -> None:
    """View element details."""
    if ctx.project is None:
        click.echo("Error: No active project", err=True)
        raise click.Abort()

    try:
        data = {
            "path": path,
            "type": "unknown",
            "properties": {"status": "read-only for demo"},
        }

        if ctx.output_format == "json":
            output = OutputFormatter.json_format(data)
        else:
            rows = [["path", path], ["type", "unknown"]]
            output = OutputFormatter.table(["Property", "Value"], rows)

        click.echo(output)
    except click.Abort:
        raise
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


@element.command()
@click.option("--filter", default=None, help="Filter by type or name")
@click.pass_obj
def query(ctx: RhapsodyContext, filter: str) -> None:
    """Query elements in active project."""
    if ctx.project is None:
        click.echo("Error: No active project", err=True)
        raise click.Abort()

    try:
        root = ctx.project.getRoot()  # type: ignore[attr-defined]
        elements = root.getNestedElements()

        if ctx.output_format == "json":
            data = {
                "elements": [
                    {"name": elem.getName(), "type": elem.getMetaClass()} for elem in elements
                ]
            }
            output = OutputFormatter.json_format(data)
        else:
            rows = [[elem.getName(), elem.getMetaClass()] for elem in elements]
            output = OutputFormatter.table(["Name", "Type"], rows)

        click.echo(output)
    except click.Abort:
        raise
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
