"""Abstract base class for all CLI command groups."""

from __future__ import annotations

import argparse
import sys

from rhapsody_cli.actions.abstract_action import AbstractAction


class AbstractCommand:
    """Base class for all CLI command groups.

    Subclasses provide their own set of AbstractAction instances via
    get_actions(). Each action registers its own subparser/arguments and
    owns its own execution logic - the command group itself only owns
    top-level parsing and dispatch to the selected action.
    """

    def __init__(self, command: str, args: list[str]) -> None:
        """Initialize the command group and parse its subcommand arguments.

        Args:
            command: Name of the command group (e.g. "element", "io", "project")
            args: Raw command-line arguments after the command group name
        """
        self._args = args
        self._subcommand: str | None = None
        self._parsed_args: argparse.Namespace | None = None

        parser = argparse.ArgumentParser(
            prog=f"rhapsody-cli {command}",
            description=f"Manage {command}s",
            add_help=True,
        )

        actions = self.get_actions()
        self._sub_commands: dict[str, AbstractAction] = {action.command_id: action for action in actions}

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
            sys.exit(2)

    def get_actions(self) -> list[AbstractAction]:
        """Return the list of actions (subcommands) for this command group.

        Subclasses must override this to register their own actions.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.get_actions() must be implemented")

    def execute(self, **kwargs: object) -> None:
        """Dispatch execution to the action matching the parsed subcommand."""
        action = self._sub_commands.get(self._subcommand) if self._subcommand else None
        if action is None or self._parsed_args is None:
            print(f"Error: Unknown subcommand '{self._subcommand}'", file=sys.stderr)
            sys.exit(2)
        action.execute(self._parsed_args)

    def usage(self, error: str = "") -> None:
        """Print usage message and exit.

        Args:
            error: Optional error message to display before usage
        """
        if error:
            print(error)
        print(f"\nUsage: rhapsody-cli {self._command_name()} [options]")
        sys.exit(2)

    def _command_name(self) -> str:
        """Get the command name (lowercase class name)."""
        return self.__class__.__name__.replace("Command", "").lower()
