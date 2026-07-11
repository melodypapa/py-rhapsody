"""Tests for CLI components."""

import logging
from typing import Iterator

import pytest

from rhapsody_cli.cli.formatters import OutputFormatter


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
