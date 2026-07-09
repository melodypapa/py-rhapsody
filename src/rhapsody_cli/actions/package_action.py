"""Package-related CLI actions.

SWR_PKG_0005: Path Validation
SWR_PKG_0010: Error Handling and Logging
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, List

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class AbstractPackageAction(ElementManagementAction):
    """Base class for package actions with common path validation.

    SWR_PKG_0005: Path Validation
    SWR_PKG_0010: Error Handling and Logging
    """

    def _resolve_and_validate_package(self, path: str) -> Any:
        """Resolve path and validate it's a Package element.

        Args:
            path: Package path to resolve.

        Returns:
            Package COM object.

        Raises:
            CliExecutionError: If path not found or not a Package.
        """
        root = self._get_active_root()
        container = self._resolve_container_or_element(
            root, path, resolve_element=False, operation=f"resolve package path '{path}'"
        )

        meta_class = container.getMetaClass()
        if meta_class != "Package":
            raise CliExecutionError(
                f"Path '{path}' does not resolve to a Package (found {meta_class})"
            )

        return container
