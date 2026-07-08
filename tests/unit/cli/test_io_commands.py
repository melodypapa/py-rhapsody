"""Tests for io command classes."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from rhapsody_cli.cli.commands.io import ExportCommand, ImportCommand
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.exceptions import RhapsodyConnectionError


class TestImportCommand:
    """Tests for ImportCommand."""

    def test_import_command_execute_signature(self) -> None:
        """Test: ImportCommand has execute method."""
        cmd = ImportCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_import_command_exits_on_connection_error(self) -> None:
        """Test: import command exits when no Rhapsody is running."""
        cmd = ImportCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(source="/tmp/model.xmi", target="Root")
            assert exc_info.value.code == 1


class TestExportCommand:
    """Tests for ExportCommand."""

    def test_export_command_execute_signature(self) -> None:
        """Test: ExportCommand has execute method."""
        cmd = ExportCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_export_command_exits_on_connection_error(self) -> None:
        """Test: export command exits when no Rhapsody is running."""
        cmd = ExportCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(output="/tmp/model.xmi", export_format="xmi")
            assert exc_info.value.code == 1
