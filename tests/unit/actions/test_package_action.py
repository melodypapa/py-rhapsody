"""Tests for package actions.

UTS_PKG_00019: Path validation fails for non-existent path
UTS_PKG_00020: Path validation fails for non-package element
"""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.package_action import AbstractPackageAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractPackageAction:
    """Test AbstractPackageAction base class.

    SWR_PKG_0005: Path Validation
    SWR_PKG_0010: Error Handling and Logging
    """

    def test_resolve_and_validate_package_success(self) -> None:
        """UTS_PKG_00019: Test successful package resolution."""
        action = AbstractPackageAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_package,
            ):
                result = action._resolve_and_validate_package("Sensors")
                assert result == mock_package

    def test_resolve_and_validate_package_not_package(self) -> None:
        """UTS_PKG_00020: Test validation fails for non-package element."""
        action = AbstractPackageAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_class,
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_package("Sensors/MyClass")

                assert "does not resolve to a Package" in str(exc_info.value)
                assert "found Class" in str(exc_info.value)

    def test_resolve_and_validate_package_path_not_found(self) -> None:
        """UTS_PKG_00019: Test path not found raises CliExecutionError."""
        from rhapsody_cli.cli.path_resolver import PathResolverError

        action = AbstractPackageAction()

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                side_effect=PathResolverError("Could not navigate to 'Invalid'"),
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_package("Invalid")

                assert "Could not navigate" in str(exc_info.value)
