"""Tests for AbstractCommand base class."""

from __future__ import annotations

import pytest

from rhapsody_cli.cli.abstract_command import AbstractCommand


class ConcreteCommand(AbstractCommand):
    """Concrete implementation of AbstractCommand for testing."""

    def execute(self) -> None:  # type: ignore[override]
        """Minimal execute implementation."""
        pass


class TestAbstractCommand:
    """Test AbstractCommand base class."""

    def test_execute_not_implemented(self) -> None:
        """Test that execute() raises NotImplementedError on base class."""
        cmd = AbstractCommand(args=[])
        with pytest.raises(NotImplementedError):
            cmd.execute()

    def test_parse_args_simple(self) -> None:
        """Test basic argument storage."""
        cmd = ConcreteCommand(args=["--name", "test", "value"])
        assert cmd._args == ["--name", "test", "value"]

    def test_command_name(self) -> None:
        """Test command name derivation from class name."""
        cmd = ConcreteCommand(args=[])
        assert cmd._command_name() == "concrete"
