"""Tests for the top-level CLI dispatcher (rhapsody_cli.cli.cli)."""

from typing import List
from unittest.mock import MagicMock, patch

from rhapsody_cli.cli.cli import main


def _run_main(argv: List[str]) -> MagicMock:
    """Run main() with the given argv (excluding the program name), returning the mocked Command class."""
    with patch("sys.argv", ["rhapsody-cli"] + argv):
        with patch("rhapsody_cli.cli.cli.PackageCommand") as mock_command_cls:
            mock_instance = MagicMock()
            mock_command_cls.return_value = mock_instance
            main()
    return mock_instance


def test_format_flag_is_parsed_and_passed_to_execute() -> None:
    """--format json should result in cmd.execute(output_format='json')."""
    mock_instance = _run_main(["package", "query", "--format", "json"])

    mock_instance.execute.assert_called_once_with(output_format="json")


def test_missing_format_flag_defaults_to_table() -> None:
    """Without --format, cmd.execute(output_format='table') should be used."""
    mock_instance = _run_main(["package", "query"])

    mock_instance.execute.assert_called_once_with(output_format="table")
