"""Tests for package actions.

UTS_PKG_00019: Path validation fails for non-existent path
UTS_PKG_00020: Path validation fails for non-package element
"""

import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.package_action import (
    AbstractPackageAction,
    PackageCreateAction,
)
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


class TestPackageCreateAction:
    """Test PackageCreateAction.

    UTS_PKG_00001: Create single package with inline JSON
    UTS_PKG_00002: Create multiple packages from JSON file
    UTS_PKG_00003: Create with stereotypes
    UTS_PKG_00004: Create with tags
    UTS_PKG_00006: Create skips unknown attributes
    UTS_PKG_00007: Create fails without name
    """

    def test_create_single_package_inline_json(self) -> None:
        """UTS_PKG_00001: Test creating single package with inline JSON."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","description":"Temperature sensors"}'

            action.execute(args)

            mock_parent.addNestedPackage.assert_called_once_with("TempSensors")
            mock_package.setDescription.assert_called_once_with("Temperature sensors")

    def test_create_bulk_packages_from_file(self, tmp_path: Any) -> None:
        """UTS_PKG_00002: Test creating multiple packages from JSON file."""
        json_file = tmp_path / "packages.json"
        json_file.write_text(
            '[{"name":"TempSensors","description":"Temperature"},'
            '{"name":"PressureSensors","description":"Pressure"}]'
        )

        action = PackageCreateAction()
        mock_parent = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_parent.addNestedPackage.call_count == 2

    def test_create_with_stereotypes(self) -> None:
        """UTS_PKG_00003: Test creating package with stereotypes."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = (
                '{"name":"TempSensors","stereotypes":["auto_generated"]}'
            )

            action.execute(args)

            mock_package.addStereotype.assert_called_once_with("auto_generated", "Package")

    def test_create_with_tags(self) -> None:
        """UTS_PKG_00004: Test creating package with tags."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","tags":{"status":"active"}}'

            action.execute(args)

            mock_package.setPropertyValue.assert_called_once_with("status", "active")

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_PKG_00006: Test that unknown attributes are skipped with warning."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self) -> None:
        """UTS_PKG_00007: Test that missing name raises error."""
        action = PackageCreateAction()
        mock_parent = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"description":"No name"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "'name' is required" in str(exc_info.value)

    def test_create_from_invalid_json_raises_error(self) -> None:
        """UTS_PKG_00009: Test that invalid JSON raises error."""
        action = PackageCreateAction()

        args = MagicMock()
        args.path = "Sensors"
        args.input = None
        args.attributes = "{invalid json"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Invalid JSON" in str(exc_info.value)

    def test_create_from_missing_file_raises_error(self) -> None:
        """UTS_PKG_00010: Test that missing file raises error."""
        action = PackageCreateAction()

        args = MagicMock()
        args.path = "Sensors"
        args.input = None
        args.attributes = "nonexistent_file.json"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "File not found" in str(exc_info.value)
