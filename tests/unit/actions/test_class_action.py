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


class TestClassCreateAction:
    """Test ClassCreateAction.

    UTS_CLS_00001: Create single class with inline JSON
    UTS_CLS_00002: Create multiple classes from JSON file
    UTS_CLS_00003: Create with stereotypes
    UTS_CLS_00004: Create with tags
    UTS_CLS_00005: Create with boolean flags
    UTS_CLS_00006: Create with operations
    UTS_CLS_00007: Create with attributes
    UTS_CLS_00008: Create with superclasses
    UTS_CLS_00009: Create skips unknown attributes
    UTS_CLS_00010: Create fails without name
    """

    def _make_action_with_parent(self) -> tuple:
        """Helper: build action and mock parent package."""
        from rhapsody_cli.actions.class_action import ClassCreateAction

        action = ClassCreateAction()
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        return action, mock_parent

    def test_create_single_class_inline_json(self) -> None:
        """UTS_CLS_00001: Test creating single class with inline JSON."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TemperatureSensor","description":"Temp sensor"}'

            action.execute(args)

            mock_parent.addClass.assert_called_once_with("TemperatureSensor")
            mock_class.setDescription.assert_called_once_with("Temp sensor")

    def test_create_bulk_classes_from_file(self, tmp_path) -> None:
        """UTS_CLS_00002: Test creating multiple classes from JSON file."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        json_file = tmp_path / "classes.json"
        json_file.write_text(
            '[{"name":"TempSensor"},{"name":"PressureSensor"}]', encoding="utf-8"
        )

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_parent.addClass.call_count == 2

    def test_create_with_stereotypes(self) -> None:
        """UTS_CLS_00003: Test stereotypes applied via addStereotype(name, 'Class')."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","stereotypes":["active","boundary"]}'

            action.execute(args)

            assert mock_class.addStereotype.call_count == 2
            mock_class.addStereotype.assert_any_call("active", "Class")
            mock_class.addStereotype.assert_any_call("boundary", "Class")

    def test_create_with_tags(self) -> None:
        """UTS_CLS_00004: Test tags set via setPropertyValue."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","tags":{"status":"active","level":"3"}}'

            action.execute(args)

            assert mock_class.setPropertyValue.call_count == 2
            mock_class.setPropertyValue.assert_any_call("status", "active")
            mock_class.setPropertyValue.assert_any_call("level", "3")

    def test_create_with_boolean_flags(self) -> None:
        """UTS_CLS_00005: Test isAbstract/isFinal/isActive set via setIsX(1/0)."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","isAbstract":true,"isFinal":false,"isActive":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setIsFinal.assert_called_once_with(0)
            mock_class.setIsActive.assert_called_once_with(1)

    def test_create_with_operations(self) -> None:
        """UTS_CLS_00006: Test operations added via addOperation."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","operations":["readValue","setThreshold"]}'

            action.execute(args)

            assert mock_class.addOperation.call_count == 2
            mock_class.addOperation.assert_any_call("readValue")
            mock_class.addOperation.assert_any_call("setThreshold")

    def test_create_with_attributes_list(self) -> None:
        """UTS_CLS_00007: Test attributes added via addAttribute."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","attributes":["threshold","unit"]}'

            action.execute(args)

            assert mock_class.addAttribute.call_count == 2
            mock_class.addAttribute.assert_any_call("threshold")
            mock_class.addAttribute.assert_any_call("unit")

    def test_create_with_superclasses(self) -> None:
        """UTS_CLS_00008: Test superclasses resolved via findNestedClassifierRecursive."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class
        mock_base = MagicMock()
        mock_parent.findNestedClassifierRecursive.return_value = mock_base

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","superclasses":["BaseSensor"]}'

            action.execute(args)

            mock_parent.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_class.addGeneralization.assert_called_once_with(mock_base)

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_CLS_00009: Test unknown attributes skipped with warning."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self) -> None:
        """UTS_CLS_00010: Test missing name raises CliExecutionError."""
        action, mock_parent = self._make_action_with_parent()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"description":"No name"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "'name' is required" in str(exc_info.value)