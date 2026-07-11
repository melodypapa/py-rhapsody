"""Abstract base class for all CLI command groups."""

import argparse
import logging
from typing import Dict, List, Optional

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class AbstractCommand:
    """Base class for all CLI command groups.

    Subclasses provide their own set of AbstractAction instances via
    get_actions(). Each action registers its own subparser/arguments and
    owns its own execution logic - the command group itself only owns
    top-level parsing and dispatch to the selected action.
    """

    def __init__(self, command: str, args: List[str]) -> None:
        """Initialize the command group and parse its subcommand arguments.

        Args:
            command: Name of the command group (e.g. "element", "io", "project")
            args: Raw command-line arguments after the command group name
        """
        self._args = args
        self._subcommand: Optional[str] = None
        self._parsed_args: Optional[argparse.Namespace] = None

        parser = argparse.ArgumentParser(
            prog=f"rhapsody-cli {command}",
            description=f"Manage {command}s",
            add_help=True,
        )

        actions = self.get_actions()
        self._sub_commands: Dict[str, AbstractAction] = {action.command_id: action for action in actions}

        sub_parsers = parser.add_subparsers(dest="subcommand", help=f"{command.capitalize()} operations")
        for action in actions:
            action.init_arguments(sub_parsers)

        try:
            self._parsed_args = parser.parse_args(args)
            self._subcommand = self._parsed_args.subcommand
        except SystemExit:
            # argparse calls sys.exit on error, we want to propagate that
            raise

        if not self._subcommand:
            parser.print_help()
            raise CliExecutionError(f"Missing subcommand for '{command}'", exit_code=2)

    def get_actions(self) -> List[AbstractAction]:
        """Return the list of actions (subcommands) for this command group.

        Subclasses must override this to register their own actions.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.get_actions() must be implemented")

    def execute(self, output_format: str = "table") -> None:
        """Dispatch execution to the action matching the parsed subcommand.

        Args:
            output_format: The output format ("table", "json", "csv") to set
                on the dispatched action before executing it.
        """
        action = self._sub_commands.get(self._subcommand) if self._subcommand else None
        if action is None or self._parsed_args is None:
            logger.error("Unknown subcommand '%s'", self._subcommand)
            raise CliExecutionError(f"Unknown subcommand '{self._subcommand}'", exit_code=2)
        if hasattr(action, "output_format"):
            action.output_format = output_format
        action.execute(self._parsed_args)

    def usage(self, error: str = "") -> None:
        """Raise a CliExecutionError with a usage message.

        Args:
            error: Optional error message to include before the usage text.
        """
        message = f"{error}\n" if error else ""
        message += f"Usage: rhapsody-cli {self._command_name()} [options]"
        logger.error(message)
        raise CliExecutionError(message, exit_code=2)

    def _command_name(self) -> str:
        """Get the command name (lowercase class name)."""
        return self.__class__.__name__.replace("Command", "").lower()
