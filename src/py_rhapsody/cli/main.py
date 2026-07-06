"""Main CLI entry point."""

from __future__ import annotations

import click

from py_rhapsody.cli.commands.element import element as element_cmd
from py_rhapsody.cli.commands.io import io as io_cmd
from py_rhapsody.cli.commands.project import project as project_cmd
from py_rhapsody.cli.context import RhapsodyContext


@click.group()
@click.option(
    "--output",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format",
)
@click.pass_context
def cli(ctx: click.Context, output: str) -> None:
    """Rhapsody model CLI tool for browsing and managing models."""
    if ctx.obj is None:
        ctx.obj = RhapsodyContext()
    ctx.obj.output_format = output


cli.add_command(project_cmd)
cli.add_command(element_cmd)
cli.add_command(io_cmd)


if __name__ == "__main__":
    cli()
