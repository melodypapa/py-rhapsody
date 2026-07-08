"""Abstract base class for all CLI commands."""

from __future__ import annotations

import sys


class AbstractCommand:
    """Base class for all CLI commands."""

    def __init__(self, args: list[str]) -> None:
        """Initialize command with raw arguments.

        Args:
            args: Raw command-line arguments (excluding command name itself)
        """
        self._args = args

    def execute(self, **kwargs: object) -> None:
        """Execute the command. Must be overridden by subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__}.execute() must be implemented")

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
