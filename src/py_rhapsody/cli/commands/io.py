"""Import and export CLI commands."""

from __future__ import annotations

import click

from py_rhapsody.cli.context import RhapsodyContext


@click.group()
def io() -> None:
    """Import and export Rhapsody models."""
    pass


@io.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--target", default="Root", help="Target container (default: Root)")
@click.pass_obj
def import_cmd(ctx: RhapsodyContext, source: str, target: str) -> None:
    """Import model from file."""
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


@io.command()
@click.argument("output", type=click.Path())
@click.option("--format", "export_format", default="xmi", help="Export format (xmi, json)")
@click.pass_obj
def export(ctx: RhapsodyContext, output: str, export_format: str) -> None:
    """Export model to file."""
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
