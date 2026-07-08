"""Tests for CLI components."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import RhapsodyConnectionError


@pytest.fixture(autouse=True)
def _reset_logger() -> Iterator[None]:
    """Reset the rhapsody_cli logger before and after each test."""
    logger = logging.getLogger("rhapsody_cli")
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)
    yield
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)


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


def test_context_get_active_project_attaches_and_returns_active_project() -> None:
    """Test get_active_project() attaches to Rhapsody and returns activeProject()."""
    ctx = RhapsodyContext()
    fake_app = MagicMock(name="FakeApplication")
    fake_project = MagicMock(name="FakeProject")
    fake_app.activeProject.return_value = fake_project

    def fake_connect(method: str = "attach") -> MagicMock:
        ctx.app = fake_app
        return fake_app

    with patch.object(ctx, "connect", side_effect=fake_connect) as mock_connect:
        result = ctx.get_active_project()

    mock_connect.assert_called_once_with("attach")
    fake_app.activeProject.assert_called_once_with()
    assert result is fake_project
    assert ctx.project is fake_project


def test_context_get_active_project_propagates_connection_error() -> None:
    """Test get_active_project() lets RhapsodyConnectionError from connect() propagate."""
    ctx = RhapsodyContext()
    with patch.object(ctx, "connect", side_effect=RhapsodyConnectionError("no running instance")):
        with pytest.raises(RhapsodyConnectionError):
            ctx.get_active_project()
