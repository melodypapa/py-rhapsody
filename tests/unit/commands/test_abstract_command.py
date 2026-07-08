"""Tests for AbstractCommand base class."""

import argparse
from typing import List, Optional

import pytest

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.commands.abstract_command import AbstractCommand


class FakeAction(AbstractAction):
    """Fake action for testing dispatch."""

    def __init__(self) -> None:
        super().__init__(command_id="run")
        self.executed_with: Optional[argparse.Namespace] = None

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'run' subcommand and its arguments."""
        run_parser = sub_parser.add_parser("run", help="Run the fake action")
        run_parser.add_argument("--name", default="test")

    def execute(self, args: argparse.Namespace) -> None:
        """Record the parsed args it was called with."""
        self.executed_with = args


class ConcreteCommand(AbstractCommand):
    """Concrete implementation of AbstractCommand for testing."""

    def __init__(self, args: List[str], action: AbstractAction) -> None:
        self._action = action
        super().__init__("concrete", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the single fake action."""
        return [self._action]


class TestAbstractCommand:
    """Test AbstractCommand base class."""

    def test_get_actions_not_implemented(self) -> None:
        """Test that get_actions() raises NotImplementedError on base class."""
        with pytest.raises(NotImplementedError):
            AbstractCommand("abstract", ["subcommand"])

    def test_no_subcommand_exits(self) -> None:
        """Test that missing subcommand causes SystemExit during construction."""
        action = FakeAction()
        with pytest.raises(SystemExit):
            ConcreteCommand([], action)

    def test_execute_dispatches_to_action(self) -> None:
        """Test that execute() dispatches to the matching action."""
        action = FakeAction()
        cmd = ConcreteCommand(["run", "--name", "hello"], action)
        cmd.execute()
        assert action.executed_with is not None
        assert action.executed_with.name == "hello"

    def test_command_name(self) -> None:
        """Test command name derivation from class name."""
        action = FakeAction()
        cmd = ConcreteCommand(["run"], action)
        assert cmd._command_name() == "concrete"
