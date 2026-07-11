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
            mock_project.findElementByGUID.assert_called_once_with("12345678-1234-1234-1234-123456789abc")

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
        json_file.write_text('[{"name":"TempSensor"},{"name":"PressureSensor"}]', encoding="utf-8")

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


class TestClassDeleteAction:
    """Test ClassDeleteAction.

    UTS_CLS_00011: Delete class by path
    UTS_CLS_00012: Delete class by GUID
    UTS_CLS_00013: Delete handles COM error
    UTS_CLS_00014: Delete requires path or guid
    """

    def test_delete_class_by_path_success(self) -> None:
        """UTS_CLS_00011: Test successful class deletion by path."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/OldClass"
            args.guid = None

            action.execute(args)

            mock_class.deleteFromProject.assert_called_once()

    def test_delete_class_by_guid_success(self) -> None:
        """UTS_CLS_00012: Test successful class deletion by GUID."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"

            action.execute(args)

            mock_class.deleteFromProject.assert_called_once()

    def test_delete_class_handles_com_error(self) -> None:
        """UTS_CLS_00013: Test error handling during deletion."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"
        mock_class.deleteFromProject.side_effect = Exception("COM error")

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/OldClass"
            args.guid = None

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "COM error" in str(exc_info.value)

    def test_delete_requires_path_or_guid(self) -> None:
        """UTS_CLS_00014: Test that exactly one of path/guid is required."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        args = MagicMock()
        args.path = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid must be specified" in str(exc_info.value)

    def test_delete_rejects_both_path_and_guid(self) -> None:
        """Test that specifying both path and guid is rejected."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        args = MagicMock()
        args.path = "Sensors/X"
        args.guid = "12345678-1234-1234-1234-123456789abc"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Only one of --path or --guid" in str(exc_info.value)


class TestClassViewAction:
    """Test ClassViewAction.

    UTS_CLS_00015: View table output
    UTS_CLS_00016: View JSON output to file
    UTS_CLS_00017: View CSV output
    UTS_CLS_00018: View by GUID
    UTS_CLS_00019: View requires path or guid
    UTS_CLS_00020: View normalizes IsAbstract to int in JSON
    """

    def _make_mock_class(self) -> MagicMock:
        """Helper: build a fully-populated mock class."""
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"
        mock_class.getName.return_value = "TemperatureSensor"
        mock_class.getGUID.return_value = "12345678-1234-1234-1234-123456789abc"
        mock_class.getDescription.return_value = "Temperature sensor"
        mock_class.getIsAbstract.return_value = True  # bool
        mock_class.getIsActive.return_value = 1
        mock_class.getIsFinal.return_value = 0
        mock_class.getIsComposite.return_value = 0
        mock_class.getIsReactive.return_value = 0
        mock_class.getFullPathName.return_value = "Sensors/TemperatureSensor"

        op1 = MagicMock()
        op1.getName.return_value = "readValue"
        op2 = MagicMock()
        op2.getName.return_value = "setThreshold"
        mock_class.getOperations.return_value = [op1, op2]

        attr1 = MagicMock()
        attr1.getName.return_value = "threshold"
        attr2 = MagicMock()
        attr2.getName.return_value = "unit"
        mock_class.getAttributes.return_value = [attr1, attr2]

        return mock_class

    def test_view_table_output(self, capsys) -> None:
        """UTS_CLS_00015: Test table format output."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out
            assert "Property" in captured.out
            assert "readValue, setThreshold" in captured.out

    def test_view_json_output_to_file(self, tmp_path) -> None:
        """UTS_CLS_00016: Test JSON output to file with int-normalized IsAbstract."""
        import json as json_module

        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            output_file = tmp_path / "class.json"
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "json"
            args.output = str(output_file)

            action.execute(args)

            data = json_module.loads(output_file.read_text())
            assert data["name"] == "TemperatureSensor"
            assert data["guid"] == "12345678-1234-1234-1234-123456789abc"
            assert data["isAbstract"] == 1  # bool True normalized to int
            assert data["isActive"] == 1
            assert data["isFinal"] == 0
            assert data["operations"] == ["readValue", "setThreshold"]
            assert data["attributes"] == ["threshold", "unit"]

    def test_view_csv_output(self, capsys) -> None:
        """UTS_CLS_00017: Test CSV format output."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "csv"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            lines = captured.out.strip().split("\n")
            assert len(lines) == 2
            assert "Name,GUID" in lines[0]
            assert "TemperatureSensor" in lines[1]

    def test_view_by_guid(self, capsys) -> None:
        """UTS_CLS_00018: Test viewing class by GUID."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out

    def test_view_requires_path_or_guid(self) -> None:
        """UTS_CLS_00019: Test that exactly one of path/guid is required."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        args = MagicMock()
        args.path = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid must be specified" in str(exc_info.value)


class TestClassListAction:
    """Test ClassListAction.

    UTS_CLS_00021: List classes in package
    UTS_CLS_00022: List empty package
    UTS_CLS_00023: List JSON output
    """

    def test_list_classes(self, capsys) -> None:
        """UTS_CLS_00021: Test listing classes in a package."""
        from rhapsody_cli.actions.class_action import ClassListAction

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        cls1 = MagicMock()
        cls1.getName.return_value = "TemperatureSensor"
        cls2 = MagicMock()
        cls2.getName.return_value = "PressureSensor"
        mock_package.getClasses.return_value = [cls1, cls2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out
            assert "PressureSensor" in captured.out

    def test_list_empty_package(self, capsys) -> None:
        """UTS_CLS_00022: Test listing empty package."""
        from rhapsody_cli.actions.class_action import ClassListAction

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.getClasses.return_value = []

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "EmptyPackage"
            args.format = "table"
            args.output = None

            action.execute(args)

            capsys.readouterr()  # Should produce empty table (no data)

    def test_list_json_output(self, capsys) -> None:
        """UTS_CLS_00023: Test JSON output format."""
        import json as json_module

        from rhapsody_cli.actions.class_action import ClassListAction

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        cls1 = MagicMock()
        cls1.getName.return_value = "TemperatureSensor"
        cls2 = MagicMock()
        cls2.getName.return_value = "PressureSensor"
        mock_package.getClasses.return_value = [cls1, cls2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "json"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            data = json_module.loads(captured.out)
            assert data == ["TemperatureSensor", "PressureSensor"]


class TestClassLinkAction:
    """Test ClassLinkAction.

    UTS_CLS_00024: Add generalization by name
    UTS_CLS_00025: Remove generalization by name
    UTS_CLS_00026: Link requires add or remove
    UTS_CLS_00027: Link target not found raises error
    UTS_CLS_00028: Link by GUID
    """

    def test_add_generalization_by_path(self) -> None:
        """UTS_CLS_00024: Test adding generalization by name."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.add = "BaseSensor"
            args.remove = None
            args.type = "generalization"

            action.execute(args)

            mock_source.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_source.addGeneralization.assert_called_once_with(mock_target)

    def test_remove_generalization_by_path(self) -> None:
        """UTS_CLS_00025: Test removing generalization by name."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.add = None
            args.remove = "BaseSensor"
            args.type = "generalization"

            action.execute(args)

            mock_source.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_source.deleteGeneralization.assert_called_once_with(mock_target)

    def test_link_requires_add_or_remove(self) -> None:
        """UTS_CLS_00026: Test that exactly one of add/remove is required."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        args = MagicMock()
        args.path = "Sensors/X"
        args.guid = None
        args.add = None
        args.remove = None
        args.type = "generalization"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --add or --remove must be specified" in str(exc_info.value)

    def test_link_target_not_found_raises_error(self) -> None:
        """UTS_CLS_00027: Test that missing target raises error."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_source.findNestedClassifierRecursive.return_value = None

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            args = MagicMock()
            args.path = "Sensors/X"
            args.guid = None
            args.add = "NonExistent"
            args.remove = None
            args.type = "generalization"

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "Class 'NonExistent' not found" in str(exc_info.value)

    def test_link_by_guid(self) -> None:
        """UTS_CLS_00028: Test linking class by GUID."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.add = "BaseSensor"
            args.remove = None
            args.type = "generalization"

            action.execute(args)

            mock_source.addGeneralization.assert_called_once_with(mock_target)


class TestClassUpdateAction:
    """Test ClassUpdateAction.

    UTS_CLS_00030: Update class via path
    UTS_CLS_00031: Update class via GUID with type validation
    UTS_CLS_00032: Update GUID wrong type raises error
    UTS_CLS_00033: Partial update only modifies provided fields
    UTS_CLS_00034: Boolean flags converted to int (1/0)
    UTS_CLS_00035: Unknown fields skipped with warning
    UTS_CLS_00036: Update from JSON file
    UTS_CLS_00037: Update requires path or guid
    """

    def test_update_class_with_path(self) -> None:
        """UTS_CLS_00030: Test updating class via --path."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated description"}'

            action.execute(args)

            mock_class.setDescription.assert_called_once_with("Updated description")

    def test_update_class_with_guid(self) -> None:
        """UTS_CLS_00031: Test updating class via --guid with type validation."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "{ABC-123}"
            args.input = None
            args.attributes = '{"description":"Updated"}'

            action.execute(args)

            mock_class.setDescription.assert_called_once_with("Updated")

    def test_update_class_guid_wrong_type(self) -> None:
        """UTS_CLS_00032: Test --guid resolving to non-Class raises error."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_project = MagicMock()
        mock_element = MagicMock()
        mock_element.getMetaClass.return_value = "Package"
        mock_project.findElementByGUID.return_value = mock_element

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            args = MagicMock()
            args.path = None
            args.guid = "{ABC-123}"
            args.input = None
            args.attributes = '{"description":"x"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "does not resolve to a Class" in str(exc_info.value)
            assert "found Package" in str(exc_info.value)

    def test_update_class_partial_update(self) -> None:
        """UTS_CLS_00033: Test partial update - only isAbstract field applied."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/MyClass"
            args.guid = None
            args.input = None
            args.attributes = '{"isAbstract":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setDescription.assert_not_called()
            mock_class.setName.assert_not_called()

    def test_update_class_boolean_flags(self) -> None:
        """UTS_CLS_00034: Test isAbstract/isFinal/isActive converted to int (1/0)."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/MyClass"
            args.guid = None
            args.input = None
            args.attributes = '{"isAbstract":true,"isFinal":false,"isActive":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setIsFinal.assert_called_once_with(0)
            mock_class.setIsActive.assert_called_once_with(1)

    def test_update_class_skips_unknown_fields(self) -> None:
        """UTS_CLS_00035: Test unknown field triggers warning, known field still applied."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/MyClass"
            args.guid = None
            args.input = None
            args.attributes = '{"unknown_field":"value","description":"real desc"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)
                mock_class.setDescription.assert_called_once_with("real desc")

    def test_update_class_from_file(self, tmp_path) -> None:
        """UTS_CLS_00036: Test loading JSON from --input file."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        json_file = tmp_path / "update.json"
        json_file.write_text('{"description":"From file"}')

        action = ClassUpdateAction()
        mock_class = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/MyClass"
            args.guid = None
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            mock_class.setDescription.assert_called_once_with("From file")

    def test_update_class_requires_path_or_guid(self) -> None:
        """UTS_CLS_00037: Test that neither --path nor --guid raises error."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()

        args = MagicMock()
        args.path = None
        args.guid = None
        args.input = None
        args.attributes = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid is required" in str(exc_info.value)
