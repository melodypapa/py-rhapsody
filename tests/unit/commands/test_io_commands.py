"""Tests for io actions and the IOCommand dispatcher."""

import argparse
from unittest.mock import patch

import pytest

from rhapsody_cli.actions.io_action import IOExportAction, IOImportAction
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.commands.io_command import IOCommand
from rhapsody_cli.exceptions import RhapsodyConnectionError


class TestIOCommandDispatch:
    """Tests for the IOCommand group dispatcher."""

    def test_import_subcommand_dispatches(self) -> None:
        """Test: 'import' subcommand is parsed correctly."""
        cmd = IOCommand(["import", "source.xmi"])
        assert cmd._subcommand == "import"

    def test_export_subcommand_dispatches(self) -> None:
        """Test: 'export' subcommand is parsed correctly."""
        cmd = IOCommand(["export", "output.xmi"])
        assert cmd._subcommand == "export"

    def test_missing_subcommand_exits(self) -> None:
        """Test: no subcommand causes SystemExit."""
        with pytest.raises(SystemExit):
            IOCommand([])


class TestIOImportAction:
    """Tests for IOImportAction."""

    def test_import_action_exits_on_connection_error(self) -> None:
        """Test: import action exits when no Rhapsody is running."""
        action = IOImportAction()
        args = argparse.Namespace(source="source.xmi", target="Root", verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1


class TestIOExportAction:
    """Tests for IOExportAction."""

    def test_export_action_exits_on_connection_error(self) -> None:
        """Test: export action exits when no Rhapsody is running."""
        action = IOExportAction()
        args = argparse.Namespace(output="output.xmi", format="xmi", verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1
