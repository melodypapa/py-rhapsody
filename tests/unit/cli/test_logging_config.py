"""Tests for CliLoggingConfigurator."""

import logging
from pathlib import Path

import pytest

from rhapsody_cli.cli.logging_config import CliLoggingConfigurator


def _reset_logger() -> logging.Logger:
    """Return the rhapsody_cli logger with handlers cleared for a clean test."""
    logger = logging.getLogger("rhapsody_cli")
    logger.handlers.clear()
    return logger


class TestCliLoggingConfigurator:
    """Tests for CliLoggingConfigurator."""

    def test_default_level_is_info(self) -> None:
        """Test: verbose=False sets logger level to INFO."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()
        assert logger.level == logging.INFO

    def test_verbose_level_is_debug(self) -> None:
        """Test: verbose=True sets logger level to DEBUG."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=True).configure()
        assert logger.level == logging.DEBUG

    def test_configure_adds_stream_and_file_handlers(self) -> None:
        """Test: configure() attaches exactly one StreamHandler and one FileHandler."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()

        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)]
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

        assert len(stream_handlers) == 1
        assert len(file_handlers) == 1

    def test_configure_is_idempotent(self) -> None:
        """Test: calling configure() twice does not duplicate handlers."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()
        CliLoggingConfigurator(verbose=False).configure()

        assert len(logger.handlers) == 2

    def test_file_handler_targets_expected_log_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test: FileHandler writes to rhapsody-cli.log in the current working directory."""
        monkeypatch.chdir(tmp_path)
        logger = _reset_logger()

        CliLoggingConfigurator(verbose=False).configure()
        logger.info("hello world")

        for handler in logger.handlers:
            handler.flush()

        log_file = tmp_path / "rhapsody-cli.log"
        assert log_file.exists()
        assert "hello world" in log_file.read_text()
