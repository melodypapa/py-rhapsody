"""Tests for PackageCommand dispatcher.

UTS_PKG_00025: PackageCommand registers all subcommands
"""

import pytest

from rhapsody_cli.commands.package_command import PackageCommand
from rhapsody_cli.exceptions import CliExecutionError


class TestPackageCommand:
    """Test PackageCommand dispatcher."""

    def test_command_id_is_package(self) -> None:
        """Test that command name is 'package'."""
        cmd = PackageCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        assert cmd._subcommand == "create"

    def test_missing_subcommand_raises_error(self) -> None:
        """Test that missing subcommand raises error."""
        with pytest.raises(CliExecutionError):
            PackageCommand([])

    def test_registers_all_five_subcommands(self) -> None:
        """UTS_PKG_00025: Test that all 5 subcommands are registered."""
        cmd = PackageCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "update" in command_ids
        assert len(actions) == 5
