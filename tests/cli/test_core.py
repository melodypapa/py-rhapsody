"""Tests for CLI components."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.cli.main import cli


def test_cli_help() -> None:
    """Test main CLI help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Rhapsody model CLI tool" in result.output
    assert "Commands:" in result.output


def test_cli_output_format_option() -> None:
    """Test output format option."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--output", "json", "--help"])
    assert result.exit_code == 0


def test_project_help() -> None:
    """Test project command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["project", "--help"])
    assert result.exit_code == 0
    assert "Manage Rhapsody projects" in result.output
    assert "open" in result.output
    assert "list" in result.output


def test_element_help() -> None:
    """Test element command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["element", "--help"])
    assert result.exit_code == 0
    assert "Manage model elements" in result.output


def test_io_help() -> None:
    """Test io command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["io", "--help"])
    assert result.exit_code == 0
    assert "Import and export" in result.output


def test_formatter_table() -> None:
    """Test table formatter."""
    headers = ["Name", "Value"]
    rows = [["test1", "value1"], ["test2", "value2"]]
    output = OutputFormatter.table(headers, rows)
    assert "Name" in output
    assert "test1" in output
    assert "test2" in output


def test_formatter_json() -> None:
    """Test JSON formatter."""
    data = {"key": "value", "number": 42}
    output = OutputFormatter.json_format(data)
    assert '"key"' in output
    assert "value" in output


def test_formatter_csv() -> None:
    """Test CSV formatter."""
    headers = ["Name", "Type"]
    rows = [["MyClass", "Class"], ["MyPackage", "Package"]]
    output = OutputFormatter.csv_format(headers, rows)
    assert "Name,Type" in output or "Name, Type" in output
    assert "MyClass" in output


def test_context_initialization() -> None:
    """Test context initialization."""
    ctx = RhapsodyContext()
    assert ctx.app is None
    assert ctx.project is None
    assert ctx.output_format == "table"


def test_context_output_format() -> None:
    """Test context output format."""
    ctx = RhapsodyContext()
    ctx.output_format = "json"
    assert ctx.output_format == "json"


def test_context_create_project_connects_and_stores_project() -> None:
    """Test create_project connects, delegates to app, and stores result."""
    ctx = RhapsodyContext()
    fake_app = MagicMock(name="FakeApplication")
    fake_project = MagicMock(name="FakeProject")
    fake_app.createNewProject.return_value = fake_project
    ctx.app = fake_app

    result = ctx.create_project("C:/models", "NewProject")

    fake_app.createNewProject.assert_called_once_with("C:/models", "NewProject")
    assert result is fake_project
    assert ctx.project is fake_project


def test_context_create_project_connects_when_not_connected() -> None:
    """Test create_project calls connect() when no app is set yet."""
    ctx = RhapsodyContext()
    fake_app = MagicMock(name="FakeApplication")
    fake_project = MagicMock(name="FakeProject")
    fake_app.createNewProject.return_value = fake_project

    def fake_connect(method: str = "attach") -> MagicMock:
        ctx.app = fake_app
        return fake_app

    with patch.object(ctx, "connect", side_effect=fake_connect) as mock_connect:
        result = ctx.create_project("C:/models", "NewProject")

    mock_connect.assert_called_once()
    assert result is fake_project
    assert ctx.project is fake_project
