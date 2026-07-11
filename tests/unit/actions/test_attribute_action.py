"""Tests for attribute actions."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.attribute_action import AbstractAttributeAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractAttributeAction:
    """Test AbstractAttributeAction base class.

    SWR_ATTR_00006: Path and Name Validation
    SWR_ATTR_00009: Error Handling and Logging
    SWR_ATTR_00010: GUID Lookup Support
    """

    def test_resolve_classifier_success(self) -> None:
        """Test successful classifier resolution."""
        action = AbstractAttributeAction()
        mock_classifier = MagicMock()
        mock_classifier.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_classifier,
            ):
                result = action._resolve_classifier("Sensors/TemperatureSensor")
                assert result == mock_classifier

    def test_resolve_attribute_success(self) -> None:
        """Test successful attribute resolution by name within classifier."""
        action = AbstractAttributeAction()
        mock_classifier = MagicMock()
        mock_attr = MagicMock()
        mock_classifier.findAttribute.return_value = mock_attr

        result = action._resolve_attribute(mock_classifier, "threshold")
        assert result == mock_attr
        mock_classifier.findAttribute.assert_called_once_with("threshold")

    def test_resolve_attribute_not_found(self) -> None:
        """Test that missing attribute raises CliExecutionError."""
        action = AbstractAttributeAction()
        mock_classifier = MagicMock()
        mock_classifier.findAttribute.return_value = None

        with pytest.raises(CliExecutionError) as exc_info:
            action._resolve_attribute(mock_classifier, "missingAttr")

        assert "Attribute 'missingAttr' not found" in str(exc_info.value)

    def test_resolve_attribute_by_guid_success(self) -> None:
        """Test successful attribute lookup by GUID."""
        action = AbstractAttributeAction()
        mock_attr = MagicMock()
        mock_attr.getMetaClass.return_value = "Attribute"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_attr

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            result = action._resolve_attribute_by_guid("12345678-1234-1234-1234-123456789abc")
            assert result == mock_attr
            mock_project.findElementByGUID.assert_called_once_with("12345678-1234-1234-1234-123456789abc")

    def test_resolve_attribute_by_guid_not_found(self) -> None:
        """Test GUID lookup fails when element is None."""
        action = AbstractAttributeAction()
        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = None

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_attribute_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "No element found with GUID" in str(exc_info.value)

    def test_resolve_attribute_by_guid_wrong_type(self) -> None:
        """Test GUID lookup fails for non-attribute element."""
        action = AbstractAttributeAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_class

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_attribute_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "does not resolve to an Attribute" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)


class TestAttributeCreateAction:
    """Test AttributeCreateAction.

    SWR_ATTR_00001: Attribute Create Command
    SWR_ATTR_00007: External JSON File Support
    SWR_ATTR_00011: Type Resolution
    SWR_ATTR_00012: IsStatic Flag Support
    SWR_ATTR_00013: Bulk Creation Support
    """

    def _make_action_with_classifier(self) -> tuple[Any, Any]:
        """Helper: build action and mock parent classifier."""
        from rhapsody_cli.actions.attribute_action import AttributeCreateAction

        action = AttributeCreateAction()
        mock_classifier = MagicMock()
        return action, mock_classifier

    def test_create_single_attribute_inline_json(self) -> None:
        """UTS_ATTR_00001: Test creating single attribute with inline JSON."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_attr = MagicMock()
        mock_classifier.addAttribute.return_value = mock_attr

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"threshold","description":"Temperature threshold"}'

            action.execute(args)

            mock_classifier.addAttribute.assert_called_once_with("threshold")
            mock_attr.setDescription.assert_called_once_with("Temperature threshold")

    def test_create_bulk_attributes_from_file(self, tmp_path: Any) -> None:
        """UTS_ATTR_00002: Test creating multiple attributes from JSON file."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_attr = MagicMock()
        mock_classifier.addAttribute.return_value = mock_attr

        json_file = tmp_path / "attributes.json"
        json_file.write_text('[{"name":"threshold"},{"name":"sampleRate"}]', encoding="utf-8")

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_classifier.addAttribute.call_count == 2

    def test_create_with_isstatic_flag(self) -> None:
        """UTS_ATTR_00003: Test isStatic set via setIsStatic(1/0)."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_attr = MagicMock()
        mock_classifier.addAttribute.return_value = mock_attr

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"X","isStatic":true}'

            action.execute(args)

            mock_attr.setIsStatic.assert_called_once_with(1)

    def test_create_with_type_resolution(self) -> None:
        """UTS_ATTR_00004: Test type resolved via findNestedClassifierRecursive."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_attr = MagicMock()
        mock_classifier.addAttribute.return_value = mock_attr
        mock_owner = MagicMock()
        mock_type = MagicMock()
        mock_classifier.getOwner.return_value = mock_owner
        mock_owner.findNestedClassifierRecursive.return_value = mock_type

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"threshold","type":"Temperature"}'

            action.execute(args)

            mock_classifier.getOwner.assert_called_once()
            mock_owner.findNestedClassifierRecursive.assert_called_once_with("Temperature")
            mock_attr.setType.assert_called_once_with(mock_type)

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_ATTR_00005: Test unknown attributes skipped with warning."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_attr = MagicMock()
        mock_classifier.addAttribute.return_value = mock_attr

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"X","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self) -> None:
        """UTS_ATTR_00006: Test missing name raises CliExecutionError."""
        action, mock_classifier = self._make_action_with_classifier()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"description":"No name"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "'name' is required" in str(exc_info.value)


class TestAttributeDeleteAction:
    """Test AttributeDeleteAction.

    SWR_ATTR_00002: Attribute Delete Command
    SWR_ATTR_00010: GUID Lookup Support
    """

    def test_delete_attribute_by_path_and_name(self) -> None:
        """UTS_ATTR_00007: Test successful attribute deletion by path + name."""
        from rhapsody_cli.actions.attribute_action import AttributeDeleteAction

        action = AttributeDeleteAction()
        mock_classifier = MagicMock()
        mock_attr = MagicMock()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None

                action.execute(args)

                mock_classifier.deleteAttribute.assert_called_once_with(mock_attr)

    def test_delete_attribute_by_guid(self) -> None:
        """UTS_ATTR_00008: Test successful attribute deletion by GUID."""
        from rhapsody_cli.actions.attribute_action import AttributeDeleteAction

        action = AttributeDeleteAction()
        mock_attr = MagicMock()
        mock_attr.getMetaClass.return_value = "Attribute"
        mock_owner = MagicMock()
        mock_attr.getOwner.return_value = mock_owner

        with patch.object(action, "_resolve_attribute_by_guid", return_value=mock_attr):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"

            action.execute(args)

            mock_attr.getOwner.assert_called_once()
            mock_owner.deleteAttribute.assert_called_once_with(mock_attr)

    def test_delete_attribute_guid_wrong_type(self) -> None:
        """UTS_ATTR_00009: Test that wrong type via --guid raises error."""
        from rhapsody_cli.actions.attribute_action import AttributeDeleteAction

        action = AttributeDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_class

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "does not resolve to an Attribute" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)

    def test_delete_requires_path_name_or_guid(self) -> None:
        """UTS_ATTR_00010: Test that either --path + --name or --guid is required."""
        from rhapsody_cli.actions.attribute_action import AttributeDeleteAction

        action = AttributeDeleteAction()
        args = MagicMock()
        args.path = None
        args.name = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path + --name or --guid must be specified" in str(exc_info.value)


class TestAttributeViewAction:
    """Test AttributeViewAction.

    SWR_ATTR_00003: Attribute View Command
    SWR_ATTR_00008: Multi-Format Output
    SWR_ATTR_00010: GUID Lookup Support
    """

    def _make_mock_attribute(self) -> MagicMock:
        """Helper: build a fully-populated mock attribute."""
        mock_attr = MagicMock()
        mock_attr.getMetaClass.return_value = "Attribute"
        mock_attr.getName.return_value = "threshold"
        mock_attr.getGUID.return_value = "12345678-1234-1234-1234-123456789abc"
        mock_attr.getDescription.return_value = "Temperature threshold"
        mock_attr.getDefaultValue.return_value = "25.0"
        mock_attr.getMultiplicity.return_value = "1"
        mock_attr.getIsStatic.return_value = True
        mock_attr.getVisibility.return_value = "private"
        mock_attr.getDeclaration.return_value = "float threshold = 25.0;"
        mock_attr.getFullPathName.return_value = "Sensors/TemperatureSensor/threshold"

        mock_type = MagicMock()
        mock_type.getName.return_value = "Temperature"
        mock_attr.getType.return_value = mock_type

        return mock_attr

    def test_view_table_output(self, capsys: Any) -> None:
        """UTS_ATTR_00011: Test table format output."""
        from rhapsody_cli.actions.attribute_action import AttributeViewAction

        action = AttributeViewAction()
        mock_attr = self._make_mock_attribute()

        with patch.object(action, "_resolve_classifier", return_value=MagicMock()):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.format = "table"
                args.output = None

                action.execute(args)

                captured = capsys.readouterr()
                assert "threshold" in captured.out
                assert "Property" in captured.out
                assert "Temperature" in captured.out

    def test_view_json_output_to_file(self, tmp_path: Any) -> None:
        """UTS_ATTR_00012: Test JSON output to file."""
        import json as json_module

        from rhapsody_cli.actions.attribute_action import AttributeViewAction

        action = AttributeViewAction()
        mock_attr = self._make_mock_attribute()

        with patch.object(action, "_resolve_classifier", return_value=MagicMock()):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                output_file = tmp_path / "attr.json"
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.format = "json"
                args.output = str(output_file)

                action.execute(args)

                data = json_module.loads(output_file.read_text())
                assert data["name"] == "threshold"
                assert data["guid"] == "12345678-1234-1234-1234-123456789abc"
                assert data["isStatic"] == 1  # bool True normalized to int
                assert data["type"] == "Temperature"
                assert data["visibility"] == "private"
                assert data["defaultValue"] == "25.0"
                assert data["multiplicity"] == "1"
                assert data["declaration"] == "float threshold = 25.0;"
                assert data["description"] == "Temperature threshold"
                assert data["metaClass"] == "Attribute"
                assert data["fullPath"] == "Sensors/TemperatureSensor/threshold"

    def test_view_csv_output(self, capsys: Any) -> None:
        """UTS_ATTR_00013: Test CSV format output."""
        from rhapsody_cli.actions.attribute_action import AttributeViewAction

        action = AttributeViewAction()
        mock_attr = self._make_mock_attribute()

        with patch.object(action, "_resolve_classifier", return_value=MagicMock()):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.format = "csv"
                args.output = None

                action.execute(args)

                captured = capsys.readouterr()
                lines = captured.out.strip().split("\n")
                assert len(lines) == 2
                assert "Name,GUID" in lines[0]
                assert "threshold" in lines[1]

    def test_view_by_guid(self, capsys: Any) -> None:
        """UTS_ATTR_00014: Test viewing attribute by GUID."""
        from rhapsody_cli.actions.attribute_action import AttributeViewAction

        action = AttributeViewAction()
        mock_attr = self._make_mock_attribute()

        with patch.object(action, "_resolve_attribute_by_guid", return_value=mock_attr):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "threshold" in captured.out


class TestAttributeListAction:
    """Test AttributeListAction.

    SWR_ATTR_00004: Attribute List Command
    SWR_ATTR_00008: Multi-Format Output
    """

    def test_list_attributes(self, capsys: Any) -> None:
        """UTS_ATTR_00015: Test listing attributes on a classifier."""
        from rhapsody_cli.actions.attribute_action import AttributeListAction

        action = AttributeListAction()
        mock_classifier = MagicMock()
        attr1 = MagicMock()
        attr1.getName.return_value = "threshold"
        attr2 = MagicMock()
        attr2.getName.return_value = "sampleRate"
        mock_classifier.getAttributes.return_value = [attr1, attr2]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "threshold" in captured.out
            assert "sampleRate" in captured.out

    def test_list_empty(self, capsys: Any) -> None:
        """UTS_ATTR_00016: Test listing classifier with no attributes."""
        from rhapsody_cli.actions.attribute_action import AttributeListAction

        action = AttributeListAction()
        mock_classifier = MagicMock()
        mock_classifier.getAttributes.return_value = []

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "table"
            args.output = None

            action.execute(args)

            capsys.readouterr()  # Should produce empty table (no data)

    def test_list_json_output(self, capsys: Any) -> None:
        """UTS_ATTR_00017: Test JSON output format."""
        import json as json_module

        from rhapsody_cli.actions.attribute_action import AttributeListAction

        action = AttributeListAction()
        mock_classifier = MagicMock()
        attr1 = MagicMock()
        attr1.getName.return_value = "threshold"
        attr2 = MagicMock()
        attr2.getName.return_value = "sampleRate"
        mock_classifier.getAttributes.return_value = [attr1, attr2]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "json"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            data = json_module.loads(captured.out)
            assert data == ["threshold", "sampleRate"]


class TestAttributeUpdateAction:
    """Test AttributeUpdateAction.

    SWR_ATTR_00005: Attribute Update Command
    SWR_ATTR_00010: GUID Lookup Support
    """

    def test_update_attribute_by_path_and_name(self) -> None:
        """UTS_ATTR_00018: Test updating attribute via --path + --name."""
        from rhapsody_cli.actions.attribute_action import AttributeUpdateAction

        action = AttributeUpdateAction()
        mock_classifier = MagicMock()
        mock_attr = MagicMock()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.input = None
                args.attributes = '{"defaultValue":"42.0"}'

                action.execute(args)

                mock_attr.setDefaultValue.assert_called_once_with("42.0")

    def test_update_attribute_by_guid(self) -> None:
        """UTS_ATTR_00019: Test updating attribute via --guid with type validation."""
        from rhapsody_cli.actions.attribute_action import AttributeUpdateAction

        action = AttributeUpdateAction()
        mock_attr = MagicMock()
        mock_attr.getMetaClass.return_value = "Attribute"

        with patch.object(action, "_resolve_attribute_by_guid", return_value=mock_attr):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"visibility":"public"}'

            action.execute(args)

            mock_attr.setVisibility.assert_called_once_with("public")

    def test_update_partial_update(self) -> None:
        """UTS_ATTR_00020: Test that partial update only modifies specified fields."""
        from rhapsody_cli.actions.attribute_action import AttributeUpdateAction

        action = AttributeUpdateAction()
        mock_classifier = MagicMock()
        mock_attr = MagicMock()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.input = None
                args.attributes = '{"isStatic":true}'

                action.execute(args)

                mock_attr.setIsStatic.assert_called_once_with(1)
                mock_attr.setDefaultValue.assert_not_called()
                mock_attr.setName.assert_not_called()

    def test_update_skips_unknown_fields(self) -> None:
        """UTS_ATTR_00021: Test that unknown fields are skipped with warning."""
        from rhapsody_cli.actions.attribute_action import AttributeUpdateAction

        action = AttributeUpdateAction()
        mock_classifier = MagicMock()
        mock_attr = MagicMock()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            with patch.object(action, "_resolve_attribute", return_value=mock_attr):
                args = MagicMock()
                args.path = "Sensors/TemperatureSensor"
                args.name = "threshold"
                args.guid = None
                args.input = None
                args.attributes = '{"defaultValue":"new default","unknown_field":"value"}'

                with patch.object(action.logger, "warning") as mock_warning:
                    action.execute(args)

                    mock_attr.setDefaultValue.assert_called_once_with("new default")
                    mock_warning.assert_called()
                    assert "unknown_field" in str(mock_warning.call_args)
