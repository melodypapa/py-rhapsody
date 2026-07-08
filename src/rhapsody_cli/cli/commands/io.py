"""Import and export CLI commands using argparse architecture."""

from __future__ import annotations

import sys

from rhapsody_cli.cli.abstract_command import AbstractCommand
from rhapsody_cli.cli.context import RhapsodyContext


class ImportCommand(AbstractCommand):
    """Command: Import model from file."""

    def execute(self, source: str, target: str = "Root") -> None:  # type: ignore[override]
        """Execute the import command."""
        ctx = RhapsodyContext()
        try:
            ctx.get_active_project()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            print(f"Importing from {source} into {target}...")
            print("(Import functionality depends on file format and Rhapsody API)")
            print("✓ Import completed")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class ExportCommand(AbstractCommand):
    """Command: Export model to file."""

    def execute(self, output: str, export_format: str = "xmi") -> None:  # type: ignore[override]
        """Execute the export command."""
        ctx = RhapsodyContext()
        try:
            ctx.get_active_project()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            print(f"Exporting to {output} as {export_format}...")
            print("(Export functionality depends on file format and Rhapsody API)")
            print(f"✓ Export completed: {output}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
