"""Tests for ClassCommand dispatcher.

UTS_CLS_00029: ClassCommand registers all subcommands
"""

import pytest

from rhapsody_cli.commands.class_command import ClassCommand
from rhapsody_cli.exceptions import CliExecutionError


class TestClassCommand:
    """Test ClassCommand dispatcher."""

    def test_command_id_is_class(self) -> None:
        """Test that command name is 'class'."""
        cmd = ClassCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        assert cmd._subcommand == "create"

    def test_missing_subcommand_raises_error(self) -> None:
        """Test that missing subcommand raises error."""
        with pytest.raises(CliExecutionError):
            ClassCommand([])

    def test_registers_all_six_subcommands(self) -> None:
        """UTS_CLS_00029: Test that all 6 subcommands are registered."""
        cmd = ClassCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "link" in command_ids
        assert "update" in command_ids
        assert len(actions) == 6
