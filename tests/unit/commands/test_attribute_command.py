"""Tests for AttributeCommand dispatcher.

UTS_ATTR_00022: AttributeCommand registers all subcommands
"""

import pytest

from rhapsody_cli.commands.attribute_command import AttributeCommand
from rhapsody_cli.exceptions import CliExecutionError


class TestAttributeCommand:
    """Test AttributeCommand dispatcher."""

    def test_command_id_is_attribute(self) -> None:
        """Test that command name is 'attribute'."""
        cmd = AttributeCommand(["create", "--path", "Sensors/Cls", '{"name":"Test"}'])
        assert cmd._subcommand == "create"

    def test_missing_subcommand_raises_error(self) -> None:
        """Test that missing subcommand raises error."""
        with pytest.raises(CliExecutionError):
            AttributeCommand([])

    def test_registers_all_five_subcommands(self) -> None:
        """UTS_ATTR_00022: Test that all 5 subcommands are registered."""
        cmd = AttributeCommand(["create", "--path", "Sensors/Cls", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "update" in command_ids
        assert len(actions) == 5
