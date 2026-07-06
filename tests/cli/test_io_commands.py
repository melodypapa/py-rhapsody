"""Tests for io command classes."""

from __future__ import annotations

from py_rhapsody.cli.commands.io import IOCommandGroup


class TestIOCommandGroup:
    """Tests for IOCommandGroup."""

    def test_io_group_has_import_command(self) -> None:
        """Test: IOCommandGroup includes import_cmd command."""
        group = IOCommandGroup()
        assert "import" in group.commands
        assert group.commands["import"].name == "import"

    def test_io_group_has_export_command(self) -> None:
        """Test: IOCommandGroup includes export command."""
        group = IOCommandGroup()
        assert "export" in group.commands
        assert group.commands["export"].name == "export"

    def test_io_group_name_is_io(self) -> None:
        """Test: IOCommandGroup name is 'io'."""
        group = IOCommandGroup()
        assert group.name == "io"

    def test_io_group_has_help(self) -> None:
        """Test: IOCommandGroup has help text."""
        group = IOCommandGroup()
        assert group.help is not None
        assert "import" in group.help.lower() or "export" in group.help.lower()


class TestImportCommand:
    """Tests for ImportCommand."""

    def test_import_command_name_is_import(self) -> None:
        """Test: import command name is 'import'."""
        group = IOCommandGroup()
        import_cmd = group.commands["import"]
        assert import_cmd.name == "import"

    def test_import_command_has_help(self) -> None:
        """Test: import command has help text."""
        group = IOCommandGroup()
        import_cmd = group.commands["import"]
        assert import_cmd.help is not None
        assert "import" in import_cmd.help.lower()


class TestExportCommand:
    """Tests for ExportCommand."""

    def test_export_command_name_is_export(self) -> None:
        """Test: export command name is 'export'."""
        group = IOCommandGroup()
        export_cmd = group.commands["export"]
        assert export_cmd.name == "export"

    def test_export_command_has_help(self) -> None:
        """Test: export command has help text."""
        group = IOCommandGroup()
        export_cmd = group.commands["export"]
        assert export_cmd.help is not None
        assert "export" in export_cmd.help.lower()
