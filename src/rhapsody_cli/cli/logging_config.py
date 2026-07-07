"""Class-based logging configuration for the rhapsody_cli CLI."""

from __future__ import annotations

import logging

_LOGGER_NAME = "rhapsody_cli"


class CliLoggingConfigurator:
    """Configures console + file logging for the rhapsody_cli package logger."""

    LOG_FILE_NAME = "rhapsody-cli.log"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    def __init__(self, verbose: bool = False) -> None:
        """Store the desired verbosity for the next configure() call."""
        self.verbose = verbose

    def configure(self) -> None:
        """Apply console + file logging configuration to the rhapsody_cli logger."""
        logger = logging.getLogger(_LOGGER_NAME)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(self.LOG_FORMAT)
        logger.addHandler(self._build_stream_handler(formatter))
        logger.addHandler(self._build_file_handler(formatter))

    def _build_stream_handler(self, formatter: logging.Formatter) -> logging.StreamHandler:
        """Build the stderr console handler."""
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _build_file_handler(self, formatter: logging.Formatter) -> logging.FileHandler:
        """Build the append-mode file handler writing to LOG_FILE_NAME."""
        handler = logging.FileHandler(self.LOG_FILE_NAME, mode="a")
        handler.setFormatter(formatter)
        return handler
