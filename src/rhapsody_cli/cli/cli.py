"""Main CLI entry point using argparse - PanGu style architecture."""

import logging
import sys
from typing import Optional

from rhapsody_cli.cli.logging_config import CliLoggingConfigurator
from rhapsody_cli.commands.attribute_command import AttributeCommand
from rhapsody_cli.commands.class_command import ClassCommand
from rhapsody_cli.commands.operation_command import OperationCommand
from rhapsody_cli.commands.package_command import PackageCommand
from rhapsody_cli.commands.port_command import PortCommand
from rhapsody_cli.commands.project_command import ProjectCommand
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        _usage("")

    command_name = sys.argv[1]
    command_args = sys.argv[2:]

    # Check for help
    if command_name in ("-h", "--help"):
        _usage("")

    # Check for verbose flag in args and configure logging
    verbose = "-v" in command_args or "--verbose" in command_args
    CliLoggingConfigurator(verbose=verbose).configure()

    # Check for output format flag
    output_format = "table"
    if "--format" in command_args:
        idx = command_args.index("--format")
        if idx + 1 < len(command_args):
            output_format = command_args[idx + 1]

    try:
        # Dispatch to command group classes
        cmd: Optional[object] = None

        if command_name == "class":
            cmd = ClassCommand(command_args)
        elif command_name == "attribute":
            cmd = AttributeCommand(command_args)
        elif command_name == "package":
            cmd = PackageCommand(command_args)
        elif command_name == "operation":
            cmd = OperationCommand(command_args)
        elif command_name == "port":
            cmd = PortCommand(command_args)
        elif command_name == "project":
            cmd = ProjectCommand(command_args)
        else:
            _usage(f"Unknown command: {command_name}")

        # Execute the command
        if cmd and hasattr(cmd, "execute"):
            cmd.execute(output_format=output_format)

    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)
    except SystemExit:
        raise
    except CliExecutionError as e:
        # The single legitimate place sys.exit() is called for our own
        # errors: all CLI actions/commands raise CliExecutionError instead
        # of calling sys.exit() directly.
        logger.error(str(e))
        sys.exit(e.exit_code)
    except Exception as e:
        logger.error("Command failed: %s", e)
        sys.exit(1)


def _usage(error: str) -> None:
    """Print usage message and exit."""
    commands_text = "Commands:\n  attribute  Manage attributes\n  class      Manage classes\n"
    commands_text += "  operation  Manage operations\n"
    commands_text += "  package    Manage packages\n  port       Manage ports\n  project    Manage projects\n"
    options_text = "Global Options:\n  --format <format>   Output format (table, json, csv)."
    options_text += " Default: table\n  -v|--verbose        Enable debug logging\n"
    options_text += "  -h|--help          Show this help message\n"

    message = "Usage:\n  rhapsody-cli <command> [options]\n\n"
    message += commands_text + "\n" + options_text

    if error != "":
        print(f"Error: {error}\n", file=sys.stderr)
        print(message, file=sys.stderr)
    else:
        print(message)
    sys.exit(2 if error else 0)


if __name__ == "__main__":
    main()
