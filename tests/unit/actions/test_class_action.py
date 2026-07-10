"""Tests for class actions."""

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.class_action import AbstractClassAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractClassAction:
    """Test AbstractClassAction base class.

    SWR_CLS_00005: Path Validation
    SWR_CLS_00010: Error Handling and Logging
    SWR_CLS_00013: GUID Lookup Support
    """

    def test_resolve_and_validate_package_success_package(self) -> None:
        """Test successful package resolution for create/list."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_package,
            ):
                result = action._resolve_and_validate_package("Sensors")
                assert result == mock_package

    def test_resolve_and_validate_package_success_project(self) -> None:
        """Test project root accepted as package parent (RPProject inherits addClass)."""
        action = AbstractClassAction()
        mock_project = MagicMock()
        mock_project.getMetaClass.return_value = "Project"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_project,
            ):
                result = action._resolve_and_validate_package("")
                assert result == mock_project

    def test_resolve_and_validate_package_not_package(self) -> None:
        """Test validation fails for non-package element."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_class,
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_package("Sensors/MyClass")

                assert "does not resolve to a Package or Project" in str(exc_info.value)
                assert "found Class" in str(exc_info.value)

    def test_resolve_and_validate_class_success(self) -> None:
        """Test successful class resolution for delete/view/link."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_class,
            ):
                result = action._resolve_and_validate_class("Sensors/TemperatureSensor")
                assert result == mock_class

    def test_resolve_and_validate_class_not_class(self) -> None:
        """Test validation fails for non-class element."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_package,
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_class("Sensors")

                assert "does not resolve to a Class" in str(exc_info.value)
                assert "found Package" in str(exc_info.value)

    def test_resolve_class_by_guid_success(self) -> None:
        """Test successful class lookup by GUID."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_class

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            result = action._resolve_class_by_guid("12345678-1234-1234-1234-123456789abc")
            assert result == mock_class
            mock_project.findElementByGUID.assert_called_once_with(
                "12345678-1234-1234-1234-123456789abc"
            )

    def test_resolve_class_by_guid_not_class(self) -> None:
        """Test GUID lookup fails for non-class element."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_package

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_class_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "does not resolve to a Class" in str(exc_info.value)
            assert "found Package" in str(exc_info.value)