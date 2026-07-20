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

    def test_registers_all_seven_subcommands(self) -> None:
        """UTS_PKG_00025: Test that all 7 subcommands are registered (5 original + export + import)."""
        cmd = PackageCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "update" in command_ids
        assert "export" in command_ids
        assert "import" in command_ids
        assert len(actions) == 7


class TestPackageCommandExportImportRegistration:
    """Tests that PackageCommand registers export/import subcommands.

    UTS_XCH_00091: PackageCommand registers export/import subcommands
    """

    def test_get_actions_includes_export_action(self) -> None:
        """PackageCommand.get_actions() must include a PackageExportAction instance."""
        cmd = PackageCommand(["export", "--path", "Sensors", "--file", "out.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "export" in command_ids

    def test_get_actions_includes_import_action(self) -> None:
        """PackageCommand.get_actions() must include a PackageImportAction instance."""
        cmd = PackageCommand(["import", "--path", "Sensors", "--file", "in.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "import" in command_ids
