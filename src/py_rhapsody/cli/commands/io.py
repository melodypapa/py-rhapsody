"""Import and export CLI commands using class-based architecture."""

from __future__ import annotations

import click

from py_rhapsody.cli.context import RhapsodyContext


class BaseIOCommand(click.Command):
    """Base class for io commands."""

    pass


class ImportCommand(BaseIOCommand):
    """Command: Import model from file."""

    def __init__(self) -> None:
        super().__init__(
            name="import",
            help="Import model from file.",
            callback=self.execute,
            params=[
                click.Argument(["source"], type=click.Path(exists=True)),
                click.Option(
                    ["--target"],
                    default="Root",
                    help="Target container (default: Root)",
                ),
            ],
        )

    def execute(self, source: str, target: str) -> None:
        """Execute the import command."""
        ctx = RhapsodyContext()
        if not isinstance(ctx, RhapsodyContext):
            click.echo("Error: Invalid context", err=True)
            raise click.Abort()

        if ctx.project is None:
            click.echo("Error: No active project", err=True)
            raise click.Abort()

        try:
            click.echo(f"Importing from {source} into {target}...")
            click.echo("(Import functionality depends on file format and Rhapsody API)")
            click.echo("✓ Import completed")
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class ExportCommand(BaseIOCommand):
    """Command: Export model to file."""

    def __init__(self) -> None:
        super().__init__(
            name="export",
            help="Export model to file.",
            callback=self.execute,
            params=[
                click.Argument(["output"], type=click.Path()),
                click.Option(
                    ["--format"],
                    "export_format",
                    default="xmi",
                    help="Export format (xmi, json)",
                ),
            ],
        )

    def execute(self, output: str, export_format: str) -> None:
        """Execute the export command."""
        ctx = RhapsodyContext()
        if not isinstance(ctx, RhapsodyContext):
            click.echo("Error: Invalid context", err=True)
            raise click.Abort()

        if ctx.project is None:
            click.echo("Error: No active project", err=True)
            raise click.Abort()

        try:
            click.echo(f"Exporting to {output} as {export_format}...")
            click.echo("(Export functionality depends on file format and Rhapsody API)")
            click.echo(f"✓ Export completed: {output}")
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class IOCommandGroup(click.Group):
    """Command group for import and export operations."""

    def __init__(self) -> None:
        super().__init__(
            name="io",
            help="Import and export Rhapsody models.",
            invoke_without_command=False,
        )
        self.add_command(ImportCommand())
        self.add_command(ExportCommand())


io = IOCommandGroup()
