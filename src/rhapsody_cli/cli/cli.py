"""Main CLI entry point using argparse."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Optional

from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.logging_config import CliLoggingConfigurator

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="rhapsody-cli",
        description="Rhapsody model CLI tool for browsing and managing models.",
        add_help=True,
    )

    parser.add_argument(
        "--output",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Element command group
    element_parser = subparsers.add_parser("element", help="Manage model elements")
    element_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable DEBUG-level logging",
    )

    element_subparsers = element_parser.add_subparsers(
        dest="element_subcommand",
        help="Element operations",
    )

    # element add
    add_parser = element_subparsers.add_parser("add", help="Add a new element")
    add_parser.add_argument("--type", required=True, help="Element type (class, actor, etc)")
    add_parser.add_argument("--name", required=True, help="Element name")

    # element view
    view_parser = element_subparsers.add_parser("view", help="View element details")
    view_parser.add_argument("--path", required=True, help="Element path (e.g., Root::MyClass)")

    # element query
    query_parser = element_subparsers.add_parser("query", help="Query elements in active project")
    query_parser.add_argument("pattern", nargs="?", default=None, help="Search pattern (optional)")

    # element delete
    delete_parser = element_subparsers.add_parser("delete", help="Delete an element")
    delete_parser.add_argument("path", help="Element path to delete")

    # IO command group
    io_parser = subparsers.add_parser("io", help="Import and export operations")
    io_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable DEBUG-level logging",
    )

    io_subparsers = io_parser.add_subparsers(dest="io_subcommand", help="IO operations")

    # io import
    import_parser = io_subparsers.add_parser("import", help="Import model from file")
    import_parser.add_argument("source", help="Source file path")
    import_parser.add_argument("--target", default="Root", help="Target container (default: Root)")

    # io export
    export_parser = io_subparsers.add_parser("export", help="Export model to file")
    export_parser.add_argument("output", help="Output file path")
    export_parser.add_argument(
        "--format",
        choices=["xmi", "json"],
        default="xmi",
        help="Export format (default: xmi)",
    )

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Configure logging
    verbose = getattr(args, "verbose", False)
    CliLoggingConfigurator(verbose=verbose).configure()

    # Set up global context
    ctx = RhapsodyContext()
    ctx.output_format = args.output

    try:
        # Import commands here to avoid circular imports
        from rhapsody_cli.cli.commands.element import (
            AddElementCommand,
            DeleteElementCommand,
            QueryElementCommand,
            ViewElementCommand,
        )
        from rhapsody_cli.cli.commands.io import ExportCommand, ImportCommand

        # Dispatch to element commands
        if args.command == "element":
            if args.element_subcommand == "add":
                cmd = AddElementCommand(args=[])
                cmd.execute(element_type=args.type, name=args.name)
            elif args.element_subcommand == "view":
                cmd = ViewElementCommand(args=[])
                cmd.execute(path=args.path)
            elif args.element_subcommand == "query":
                cmd = QueryElementCommand(args=[])
                cmd.execute(pattern=args.pattern)
            elif args.element_subcommand == "delete":
                cmd = DeleteElementCommand(args=[])
                cmd.execute(path=args.path)
            else:
                parser.print_help()
                sys.exit(2)

        # Dispatch to IO commands
        elif args.command == "io":
            if args.io_subcommand == "import":
                cmd = ImportCommand(args=[])
                cmd.execute(source=args.source, target=args.target)
            elif args.io_subcommand == "export":
                cmd = ExportCommand(args=[])
                cmd.execute(output=args.output, export_format=args.format)
            else:
                parser.print_help()
                sys.exit(2)

    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)
    except SystemExit:
        raise
    except Exception as e:
        logger.error("Command failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
