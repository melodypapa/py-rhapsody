"""Tests for AbstractCommand base class."""

import argparse
from typing import List, Optional

import pytest

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.commands.abstract_command import AbstractCommand
from rhapsody_cli.exceptions import CliExecutionError


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
        """Test that missing subcommand raises CliExecutionError during construction."""
        action = FakeAction()
        with pytest.raises(CliExecutionError):
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


class FakeContextAwareAction(AbstractAction):
    """Fake action that mimics RhapsodyContextAction's output_format attribute."""

    def __init__(self) -> None:
        super().__init__(command_id="run")
        self.output_format: str = "table"
        self.executed = False

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'run' subcommand."""
        sub_parser.add_parser("run", help="Run the fake action")

    def execute(self, args: argparse.Namespace) -> None:
        """Record that execute was called."""
        self.executed = True


class ConcreteContextAwareCommand(AbstractCommand):
    """Concrete AbstractCommand wrapping a context-aware fake action."""

    def __init__(self, args: List[str], action: AbstractAction) -> None:
        self._action = action
        super().__init__("concrete", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the single fake action."""
        return [self._action]


class TestAbstractCommandOutputFormat:
    """Test that execute() threads output_format into the dispatched action."""

    def test_execute_sets_output_format_on_action(self) -> None:
        """execute(output_format=...) should set it on the action before calling execute()."""
        action = FakeContextAwareAction()
        cmd = ConcreteContextAwareCommand(["run"], action)

        cmd.execute(output_format="json")

        assert action.output_format == "json"
        assert action.executed is True

    def test_execute_defaults_output_format_to_table(self) -> None:
        """execute() with no output_format kwarg should leave the action's default untouched."""
        action = FakeContextAwareAction()
        cmd = ConcreteContextAwareCommand(["run"], action)

        cmd.execute()

        assert action.output_format == "table"
