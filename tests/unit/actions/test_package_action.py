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
        mock_package.get_meta_class.return_value = "Package"

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
        mock_class.get_meta_class.return_value = "Class"

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
        mock_parent.add_nested_package.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","description":"Temperature sensors"}'

            action.execute(args)

            mock_parent.add_nested_package.assert_called_once_with("TempSensors")
            mock_package.set_description.assert_called_once_with("Temperature sensors")

    def test_create_bulk_packages_from_file(self, tmp_path: Any) -> None:
        """UTS_PKG_00002: Test creating multiple packages from JSON file."""
        json_file = tmp_path / "packages.json"
        json_file.write_text('[{"name":"TempSensors","description":"Temperature"},' '{"name":"PressureSensors","description":"Pressure"}]')

        action = PackageCreateAction()
        mock_parent = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_parent.add_nested_package.call_count == 2

    def test_create_with_stereotypes(self) -> None:
        """UTS_PKG_00003: Test creating package with stereotypes."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.add_nested_package.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","stereotypes":["auto_generated"]}'

            action.execute(args)

            mock_package.add_stereotype.assert_called_once_with("auto_generated", "Package")

    def test_create_with_tags(self) -> None:
        """UTS_PKG_00004: Test creating package with tags."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.add_nested_package.return_value = mock_package

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TempSensors","tags":{"status":"active"}}'

            action.execute(args)

            mock_package.set_property_value.assert_called_once_with("status", "active")

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_PKG_00006: Test that unknown attributes are skipped with warning."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.add_nested_package.return_value = mock_package

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

    def test_create_at_root_with_none_path(self) -> None:
        """UTS_PKG_00026: Create package at root when --path is None."""
        action = PackageCreateAction()
        mock_root = MagicMock()
        mock_package = MagicMock()
        mock_root.add_package.return_value = mock_package

        with patch.object(action, "_get_active_root", return_value=mock_root):
            args = MagicMock()
            args.path = None
            args.input = None
            args.attributes = '{"name":"TopLevel"}'

            action.execute(args)

            # Root should call addPackage, NOT addNestedPackage
            mock_root.add_package.assert_called_once_with("TopLevel")
            mock_root.add_nested_package.assert_not_called()

    def test_create_at_root_with_empty_path(self) -> None:
        """UTS_PKG_00027: Create package at root when --path is empty string."""
        action = PackageCreateAction()
        mock_root = MagicMock()
        mock_package = MagicMock()
        mock_root.add_package.return_value = mock_package

        with patch.object(action, "_get_active_root", return_value=mock_root):
            args = MagicMock()
            args.path = ""
            args.input = None
            args.attributes = '{"name":"TopLevel"}'

            action.execute(args)

            # Root should call addPackage, NOT addNestedPackage
            mock_root.add_package.assert_called_once_with("TopLevel")
            mock_root.add_nested_package.assert_not_called()

    def test_create_duplicate_at_root_raises_error(self) -> None:
        """UTS_PKG_00032: Duplicate package name rejected at project root."""
        action = PackageCreateAction()
        mock_root = MagicMock()

        # Mock getPackages() to return collection with existing package named "TopLevel"
        existing_pkg = MagicMock()
        existing_pkg.get_name.return_value = "TopLevel"
        mock_root.get_packages.return_value = [existing_pkg]

        with patch.object(action, "_get_active_root", return_value=mock_root):
            args = MagicMock()
            args.path = None
            args.input = None
            args.attributes = '{"name":"TopLevel"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "TopLevel" in str(exc_info.value)
            assert "already exists" in str(exc_info.value)
            assert "project root" in str(exc_info.value)
            # addPackage should NOT have been called
            mock_root.add_package.assert_not_called()

    def test_create_duplicate_nested_raises_error(self) -> None:
        """UTS_PKG_00033: Duplicate package name rejected in parent package."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_parent.get_name.return_value = "Sensors"

        # Mock getNestedPackages() to return collection with existing package named "Temp"
        existing_pkg = MagicMock()
        existing_pkg.get_name.return_value = "Temp"
        mock_parent.get_nested_packages.return_value = [existing_pkg]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"Temp"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "Temp" in str(exc_info.value)
            assert "already exists" in str(exc_info.value)
            assert "Sensors" in str(exc_info.value)
            # addNestedPackage should NOT have been called
            mock_parent.add_nested_package.assert_not_called()

    def test_create_non_duplicate_nested_succeeds(self) -> None:
        """UTS_PKG_00034: Non-duplicate nested package creation succeeds."""
        action = PackageCreateAction()
        mock_parent = MagicMock()
        mock_package = MagicMock()
        mock_parent.add_nested_package.return_value = mock_package

        # Mock getNestedPackages() to return empty collection (no duplicates)
        mock_parent.get_nested_packages.return_value = []

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"Humidity"}'

            action.execute(args)

            # addNestedPackage should have been called
            mock_parent.add_nested_package.assert_called_once_with("Humidity")


class TestPackageDeleteAction:
    """Test PackageDeleteAction.

    UTS_PKG_00011: Delete package successfully
    UTS_PKG_00012: Delete handles COM error
    """

    def test_delete_package_success(self) -> None:
        """UTS_PKG_00011: Test successful package deletion."""
        from rhapsody_cli.actions.package_action import PackageDeleteAction

        action = PackageDeleteAction()
        mock_package = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/OldPackage"

            action.execute(args)

            mock_package.delete_from_project.assert_called_once()

    def test_delete_package_handles_error(self) -> None:
        """UTS_PKG_00012: Test error handling during deletion."""
        from rhapsody_cli.actions.package_action import PackageDeleteAction

        action = PackageDeleteAction()
        mock_package = MagicMock()
        mock_package.delete_from_project.side_effect = Exception("COM error")

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/OldPackage"

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "COM error" in str(exc_info.value)


class TestPackageViewAction:
    """Test PackageViewAction.

    UTS_PKG_00013: View table output
    UTS_PKG_00014: View JSON output to file
    UTS_PKG_00015: View CSV output
    """

    def test_view_table_output(self, capsys: Any) -> None:
        """UTS_PKG_00013: Test table format output."""
        from rhapsody_cli.actions.package_action import PackageViewAction

        action = PackageViewAction()
        mock_package = MagicMock()
        mock_package.get_name.return_value = "TempSensors"
        mock_package.get_guid.return_value = "{12345}"
        mock_package.get_description.return_value = "Temperature sensors"
        mock_package.get_meta_class.return_value = "Package"
        mock_package.get_full_path_name.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TempSensors" in captured.out
            assert "{12345}" in captured.out

    def test_view_json_output_to_file(self, tmp_path: Any) -> None:
        """UTS_PKG_00014: Test JSON output to file."""
        from rhapsody_cli.actions.package_action import PackageViewAction

        action = PackageViewAction()
        mock_package = MagicMock()
        mock_package.get_name.return_value = "TempSensors"
        mock_package.get_guid.return_value = "{12345}"
        mock_package.get_description.return_value = "Temperature sensors"
        mock_package.get_meta_class.return_value = "Package"
        mock_package.get_full_path_name.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            output_file = tmp_path / "package.json"
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "json"
            args.output = str(output_file)

            action.execute(args)

            data = json.loads(output_file.read_text())
            assert data["name"] == "TempSensors"
            assert data["guid"] == "{12345}"

    def test_view_csv_output(self, capsys: Any) -> None:
        """UTS_PKG_00015: Test CSV format output."""
        from rhapsody_cli.actions.package_action import PackageViewAction

        action = PackageViewAction()
        mock_package = MagicMock()
        mock_package.get_name.return_value = "TempSensors"
        mock_package.get_guid.return_value = "{12345}"
        mock_package.get_description.return_value = "Temperature sensors"
        mock_package.get_meta_class.return_value = "Package"
        mock_package.get_full_path_name.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "csv"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            lines = captured.out.strip().split("\n")
            assert len(lines) == 2
            assert "Name" in lines[0]
            assert "GUID" in lines[0]
            assert "TempSensors" in lines[1]


class TestPackageListAction:
    """Test PackageListAction.

    UTS_PKG_00016: List nested packages
    UTS_PKG_00017: List empty package
    UTS_PKG_00018: List JSON output
    """

    def test_list_nested_packages(self, capsys: Any) -> None:
        """UTS_PKG_00016: Test listing nested packages."""
        from rhapsody_cli.actions.package_action import PackageListAction

        action = PackageListAction()
        mock_parent = MagicMock()
        pkg1 = MagicMock()
        pkg1.get_name.return_value = "TempSensors"
        pkg2 = MagicMock()
        pkg2.get_name.return_value = "PressureSensors"
        mock_parent.get_nested_packages.return_value = [pkg1, pkg2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TempSensors" in captured.out
            assert "PressureSensors" in captured.out

    def test_list_empty_package(self, capsys: Any) -> None:
        """UTS_PKG_00017: Test listing empty package."""
        from rhapsody_cli.actions.package_action import PackageListAction

        action = PackageListAction()
        mock_parent = MagicMock()
        mock_parent.get_nested_packages.return_value = []

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "EmptyPackage"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "no data" in captured.out

    def test_list_json_output(self, capsys: Any) -> None:
        """UTS_PKG_00018: Test JSON output format."""
        from rhapsody_cli.actions.package_action import PackageListAction

        action = PackageListAction()
        mock_parent = MagicMock()
        pkg1 = MagicMock()
        pkg1.get_name.return_value = "TempSensors"
        pkg2 = MagicMock()
        pkg2.get_name.return_value = "PressureSensors"
        mock_parent.get_nested_packages.return_value = [pkg1, pkg2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "json"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert data == ["TempSensors", "PressureSensors"]


class TestPackageUpdateAction:
    """Test PackageUpdateAction.

    UTS_PKG_00035: Update package via path
    UTS_PKG_00036: Update package via GUID with type validation
    UTS_PKG_00037: Update GUID wrong type raises error
    UTS_PKG_00038: Partial update only modifies provided fields
    UTS_PKG_00039: Unknown fields skipped with warning
    UTS_PKG_00040: Update from JSON file
    UTS_PKG_00041: Update requires path or guid
    """

    def test_update_package_with_path(self) -> None:
        """UTS_PKG_00035: Test updating package via --path."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated description"}'

            action.execute(args)

            mock_package.set_description.assert_called_once_with("Updated description")

    def test_update_package_with_guid(self) -> None:
        """UTS_PKG_00036: Test updating package via --guid with type validation."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_root = MagicMock()
        mock_package = MagicMock()
        mock_package.get_meta_class.return_value = "Package"
        mock_root.find_element_by_guid.return_value = mock_package

        with patch.object(action, "_get_active_root", return_value=mock_root):
            args = MagicMock()
            args.path = None
            args.guid = "{ABC-123}"
            args.input = None
            args.attributes = '{"description":"Updated"}'

            action.execute(args)

            mock_root.find_element_by_guid.assert_called_once_with("{ABC-123}")
            mock_package.set_description.assert_called_once_with("Updated")

    def test_update_package_guid_wrong_type(self) -> None:
        """UTS_PKG_00037: Test --guid resolving to non-Package raises error."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_root = MagicMock()
        mock_element = MagicMock()
        mock_element.get_meta_class.return_value = "Class"
        mock_root.find_element_by_guid.return_value = mock_element

        with patch.object(action, "_get_active_root", return_value=mock_root):
            args = MagicMock()
            args.path = None
            args.guid = "{ABC-123}"
            args.input = None
            args.attributes = '{"description":"x"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "does not resolve to a Package" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)

    def test_update_package_partial_update(self) -> None:
        """UTS_PKG_00038: Test partial update - only tags field applied."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.guid = None
            args.input = None
            args.attributes = '{"tags":{"status":"active"}}'

            action.execute(args)

            mock_package.set_property_value.assert_called_once_with("status", "active")
            mock_package.set_description.assert_not_called()
            mock_package.set_name.assert_not_called()

    def test_update_package_skips_unknown_fields(self) -> None:
        """UTS_PKG_00039: Test unknown field triggers warning, known field still applied."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.guid = None
            args.input = None
            args.attributes = '{"unknown_field":"value","description":"real desc"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)
                mock_package.set_description.assert_called_once_with("real desc")

    def test_update_package_from_file(self, tmp_path: Any) -> None:
        """UTS_PKG_00040: Test loading JSON from --input file."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        json_file = tmp_path / "update.json"
        json_file.write_text('{"description":"From file"}')

        action = PackageUpdateAction()
        mock_package = MagicMock()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.guid = None
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            mock_package.set_description.assert_called_once_with("From file")

    def test_update_package_requires_path_or_guid(self) -> None:
        """UTS_PKG_00041: Test that neither --path nor --guid raises error."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()

        args = MagicMock()
        args.path = None
        args.guid = None
        args.input = None
        args.attributes = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid is required" in str(exc_info.value)
