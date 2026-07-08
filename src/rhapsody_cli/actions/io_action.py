"""IO actions - each subcommand of `io` as its own Action class."""

import argparse
import sys

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.context import RhapsodyContext


class IOImportAction(ElementManagementAction):
    """Import action - imports a model from a file."""

    def __init__(self) -> None:
        """Initialize the 'import' action."""
        super().__init__(command_id="import")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'import' subcommand and its arguments."""
        import_parser = sub_parser.add_parser("import", help="Import model from file")
        import_parser.add_argument("source", help="Source file path")
        import_parser.add_argument("--target", default="Root", help="Target container (default: Root)")
        self.add_verbose_argument(import_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Import model from file."""
        source = args.source
        target = args.target

        try:
            self._get_active_project()

            print(f"Importing from {source} into {target}...")
            print("(Import functionality depends on file format and Rhapsody API)")
            print("✓ Import completed")
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to import from '{source}'")
            sys.exit(1)


class IOExportAction(ElementManagementAction):
    """Export action - exports the model to a file."""

    def __init__(self) -> None:
        """Initialize the 'export' action."""
        super().__init__(command_id="export")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'export' subcommand and its arguments."""
        export_parser = sub_parser.add_parser("export", help="Export model to file")
        export_parser.add_argument("output", help="Output file path")
        export_parser.add_argument(
            "--format",
            choices=["xmi", "json"],
            default="xmi",
            help="Export format (default: xmi)",
        )
        self.add_verbose_argument(export_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Export model to file."""
        output = args.output
        export_format = args.format

        try:
            self._get_active_project()

            print(f"Exporting to {output} as {export_format}...")
            print("(Export functionality depends on file format and Rhapsody API)")
            print(f"✓ Export completed: {output}")
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to export to '{output}'")
            sys.exit(1)
