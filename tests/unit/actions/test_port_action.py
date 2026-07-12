"""Tests for port actions."""

from typing import Any, Tuple
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractPortAction:
    """Test AbstractPortAction base class.

    SWR_PORT_00006: Path and Name Validation
    SWR_PORT_00009: Error Handling and Logging
    SWR_PORT_00010: GUID Lookup Support
    """

    def test_resolve_classifier_success(self) -> None:
        """Test successful classifier resolution."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_classifier = MagicMock()
        mock_classifier.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_classifier,
            ):
                result = action._resolve_classifier("Sensors/TemperatureSensor")
                assert result == mock_classifier

    def test_resolve_port_success(self) -> None:
        """Test successful port resolution by iterating getPorts() and matching name."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_classifier = MagicMock()

        # Create mock ports
        port1 = MagicMock()
        port1.getName.return_value = "inputPort"
        port2 = MagicMock()
        port2.getName.return_value = "outputPort"
        mock_classifier.getPorts.return_value = [port1, port2]

        result = action._resolve_port(mock_classifier, "outputPort")
        assert result == port2

    def test_resolve_port_not_found(self) -> None:
        """Test that missing port raises CliExecutionError."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_classifier = MagicMock()

        # Create mock ports without matching name
        port1 = MagicMock()
        port1.getName.return_value = "inputPort"
        mock_classifier.getPorts.return_value = [port1]

        with pytest.raises(CliExecutionError) as exc_info:
            action._resolve_port(mock_classifier, "missingPort")

        assert "Port 'missingPort' not found" in str(exc_info.value)

    def test_resolve_port_by_guid_success(self) -> None:
        """Test successful port lookup by GUID."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_port = MagicMock()
        mock_port.getMetaClass.return_value = "Port"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_port

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            result = action._resolve_port_by_guid("12345678-1234-1234-1234-123456789abc")
            assert result == mock_port
            mock_project.findElementByGUID.assert_called_once_with("12345678-1234-1234-1234-123456789abc")

    def test_resolve_port_by_guid_not_found(self) -> None:
        """Test GUID lookup fails when element is None."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = None

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_port_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "No element found with GUID" in str(exc_info.value)

    def test_resolve_port_by_guid_wrong_type(self) -> None:
        """Test GUID lookup fails for non-Port element."""
        from rhapsody_cli.actions.port_action import AbstractPortAction

        action = AbstractPortAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        mock_project = MagicMock()
        mock_project.findElementByGUID.return_value = mock_class

        with patch.object(ElementManagementAction, "_get_active_project", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_port_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "does not resolve to a Port" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)


class TestPortCreateAction:
    """Test PortCreateAction.

    SWR_PORT_00001: Port Create Command
    SWR_PORT_00007: External JSON File Support
    SWR_PORT_00011: PortContract Resolution
    SWR_PORT_00012: IsBehavioral and IsReversed Support
    SWR_PORT_00013: Bulk Creation Support
    """

    def _make_action_with_classifier(self) -> Tuple[Any, Any]:
        """Helper: build action and mock parent classifier."""
        from rhapsody_cli.actions.port_action import PortCreateAction

        action = PortCreateAction()
        mock_classifier = MagicMock()
        return action, mock_classifier

    def test_create_single_port_inline_json(self) -> None:
        """UTS_PORT_00001: Test creating single port with inline JSON."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_port = MagicMock()
        mock_classifier.addPort.return_value = mock_port

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"clientPort","description":"Client interface"}'

            action.execute(args)

            mock_classifier.addPort.assert_called_once_with("clientPort")
            mock_port.setDescription.assert_called_once_with("Client interface")

    def test_create_bulk_ports_from_file(self, tmp_path: Any) -> None:
        """UTS_PORT_00002: Test creating multiple ports from JSON file."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_port = MagicMock()
        mock_classifier.addPort.return_value = mock_port

        json_file = tmp_path / "ports.json"
        json_file.write_text('[{"name":"inputPort"},{"name":"outputPort"}]', encoding="utf-8")

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_classifier.addPort.call_count == 2

    def test_create_with_boolean_flags(self) -> None:
        """UTS_PORT_00003: Test isBehavioral/isReversed set via setIsX(0/1)."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_port = MagicMock()
        mock_classifier.addPort.return_value = mock_port

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"clientPort","isBehavioral":1,"isReversed":0}'

            action.execute(args)

            mock_port.setIsBehavioral.assert_called_once_with(1)
            mock_port.setIsReversed.assert_called_once_with(0)

    def test_create_with_port_contract(self) -> None:
        """UTS_PORT_00004: Test portContract resolved via findNestedClassifierRecursive."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_port = MagicMock()
        mock_classifier.addPort.return_value = mock_port
        mock_owner = MagicMock()
        mock_contract = MagicMock()
        mock_classifier.getOwner.return_value = mock_owner
        mock_owner.findNestedClassifierRecursive.return_value = mock_contract

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"clientPort","portContract":"IClient"}'

            action.execute(args)

            mock_classifier.getOwner.assert_called_once()
            mock_owner.findNestedClassifierRecursive.assert_called_once_with("IClient")
            mock_port.setPortContract.assert_called_once_with(mock_contract)

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_PORT_00005: Test unknown attributes skipped with warning."""
        action, mock_classifier = self._make_action_with_classifier()
        mock_port = MagicMock()
        mock_classifier.addPort.return_value = mock_port

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"name":"clientPort","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self) -> None:
        """UTS_PORT_00006: Test missing name raises CliExecutionError."""
        action, mock_classifier = self._make_action_with_classifier()

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.input = None
            args.attributes = '{"description":"No name"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "'name' is required" in str(exc_info.value)


class TestPortDeleteAction:
    """Test PortDeleteAction.

    SWR_PORT_00002: Port Delete Command
    SWR_PORT_00010: GUID Lookup Support
    """

    def test_delete_port_by_path_and_name(self) -> None:
        """UTS_PORT_00007: Test successful port deletion by path + name using deleteFromProject."""
        from rhapsody_cli.actions.port_action import PortDeleteAction

        action = PortDeleteAction()
        mock_classifier = MagicMock()
        mock_port = MagicMock()

        # Setup getPorts to return the mock port
        mock_port.getName.return_value = "clientPort"
        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None

            action.execute(args)

            mock_port.deleteFromProject.assert_called_once()

    def test_delete_port_by_guid(self) -> None:
        """UTS_PORT_00008: Test successful port deletion by GUID."""
        from rhapsody_cli.actions.port_action import PortDeleteAction

        action = PortDeleteAction()
        mock_port = MagicMock()
        mock_port.getMetaClass.return_value = "Port"

        with patch.object(action, "_resolve_port_by_guid", return_value=mock_port):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"

            action.execute(args)

            mock_port.deleteFromProject.assert_called_once()

    def test_delete_port_guid_wrong_type(self) -> None:
        """UTS_PORT_00009: Test that wrong type via --guid raises error."""
        from rhapsody_cli.actions.port_action import PortDeleteAction

        action = PortDeleteAction()
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

            assert "does not resolve to a Port" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)

    def test_delete_requires_path_name_or_guid(self) -> None:
        """UTS_PORT_00010: Test that either --path + --name or --guid is required."""
        from rhapsody_cli.actions.port_action import PortDeleteAction

        action = PortDeleteAction()
        args = MagicMock()
        args.path = None
        args.name = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path + --name or --guid must be specified" in str(exc_info.value)


class TestPortViewAction:
    """Test PortViewAction.

    SWR_PORT_00003: Port View Command
    SWR_PORT_00008: Multi-Format Output
    SWR_PORT_00010: GUID Lookup Support
    """

    def _make_mock_port(self) -> MagicMock:
        """Helper: build a fully-populated mock port with 8 fields."""
        mock_port = MagicMock()
        mock_port.getMetaClass.return_value = "Port"
        mock_port.getName.return_value = "clientPort"
        mock_port.getGUID.return_value = "12345678-1234-1234-1234-123456789abc"
        mock_port.getDescription.return_value = "Client interface port"
        mock_port.getIsBehavioral.return_value = 1
        mock_port.getIsReversed.return_value = 0
        mock_port.getFullPathName.return_value = "Sensors/TemperatureSensor/clientPort"

        mock_contract = MagicMock()
        mock_contract.getName.return_value = "IClient"
        mock_port.getPortContract.return_value = mock_contract

        return mock_port

    def test_view_table_output(self, capsys: Any) -> None:
        """UTS_PORT_00011: Test table format output with 8 fields."""
        from rhapsody_cli.actions.port_action import PortViewAction

        action = PortViewAction()
        mock_port = self._make_mock_port()
        mock_classifier = MagicMock()

        mock_port.getName.return_value = "clientPort"
        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "clientPort" in captured.out
            assert "Property" in captured.out
            assert "IClient" in captured.out

    def test_view_json_output_to_file(self, tmp_path: Any) -> None:
        """UTS_PORT_00012: Test JSON output to file with 8 keys."""
        import json as json_module

        from rhapsody_cli.actions.port_action import PortViewAction

        action = PortViewAction()
        mock_port = self._make_mock_port()
        mock_classifier = MagicMock()

        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            output_file = tmp_path / "port.json"
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.format = "json"
            args.output = str(output_file)

            action.execute(args)

            data = json_module.loads(output_file.read_text())
            assert data["name"] == "clientPort"
            assert data["guid"] == "12345678-1234-1234-1234-123456789abc"
            assert data["isBehavioral"] == 1
            assert data["isReversed"] == 0
            assert data["portContract"] == "IClient"
            assert data["description"] == "Client interface port"
            assert data["metaClass"] == "Port"
            assert data["fullPath"] == "Sensors/TemperatureSensor/clientPort"

    def test_view_csv_output(self, capsys: Any) -> None:
        """UTS_PORT_00013: Test CSV format output with 8 columns."""
        from rhapsody_cli.actions.port_action import PortViewAction

        action = PortViewAction()
        mock_port = self._make_mock_port()
        mock_classifier = MagicMock()

        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.format = "csv"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            lines = captured.out.strip().split("\n")
            assert len(lines) == 2
            assert "Name,GUID" in lines[0]
            assert "clientPort" in lines[1]

    def test_view_by_guid(self, capsys: Any) -> None:
        """UTS_PORT_00014: Test viewing port by GUID."""
        from rhapsody_cli.actions.port_action import PortViewAction

        action = PortViewAction()
        mock_port = self._make_mock_port()

        with patch.object(action, "_resolve_port_by_guid", return_value=mock_port):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "clientPort" in captured.out


class TestPortListAction:
    """Test PortListAction.

    SWR_PORT_00004: Port List Command
    SWR_PORT_00008: Multi-Format Output
    """

    def test_list_ports(self, capsys: Any) -> None:
        """UTS_PORT_00015: Test listing ports on a classifier."""
        from rhapsody_cli.actions.port_action import PortListAction

        action = PortListAction()
        mock_classifier = MagicMock()
        port1 = MagicMock()
        port1.getName.return_value = "inputPort"
        port2 = MagicMock()
        port2.getName.return_value = "outputPort"
        mock_classifier.getPorts.return_value = [port1, port2]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "inputPort" in captured.out
            assert "outputPort" in captured.out

    def test_list_empty(self, capsys: Any) -> None:
        """UTS_PORT_00016: Test listing classifier with no ports."""
        from rhapsody_cli.actions.port_action import PortListAction

        action = PortListAction()
        mock_classifier = MagicMock()
        mock_classifier.getPorts.return_value = []

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "table"
            args.output = None

            action.execute(args)

            capsys.readouterr()  # Should produce empty table (no data)

    def test_list_json_output(self, capsys: Any) -> None:
        """UTS_PORT_00017: Test JSON output format."""
        import json as json_module

        from rhapsody_cli.actions.port_action import PortListAction

        action = PortListAction()
        mock_classifier = MagicMock()
        port1 = MagicMock()
        port1.getName.return_value = "inputPort"
        port2 = MagicMock()
        port2.getName.return_value = "outputPort"
        mock_classifier.getPorts.return_value = [port1, port2]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.format = "json"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            data = json_module.loads(captured.out)
            assert data == ["inputPort", "outputPort"]


class TestPortUpdateAction:
    """Test PortUpdateAction.

    SWR_PORT_00005: Port Update Command
    SWR_PORT_00010: GUID Lookup Support
    """

    def test_update_port_by_path_and_name(self) -> None:
        """UTS_PORT_00018: Test updating port via --path + --name."""
        from rhapsody_cli.actions.port_action import PortUpdateAction

        action = PortUpdateAction()
        mock_classifier = MagicMock()
        mock_port = MagicMock()
        mock_port.getName.return_value = "clientPort"
        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.input = None
            args.attributes = '{"isBehavioral":1}'

            action.execute(args)

            mock_port.setIsBehavioral.assert_called_once_with(1)

    def test_update_port_by_guid(self) -> None:
        """UTS_PORT_00019: Test updating port via --guid with type validation."""
        from rhapsody_cli.actions.port_action import PortUpdateAction

        action = PortUpdateAction()
        mock_port = MagicMock()
        mock_port.getMetaClass.return_value = "Port"

        with patch.object(action, "_resolve_port_by_guid", return_value=mock_port):
            args = MagicMock()
            args.path = None
            args.name = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"isReversed":1}'

            action.execute(args)

            mock_port.setIsReversed.assert_called_once_with(1)

    def test_update_partial_update(self) -> None:
        """UTS_PORT_00020: Test that partial update only modifies specified fields."""
        from rhapsody_cli.actions.port_action import PortUpdateAction

        action = PortUpdateAction()
        mock_classifier = MagicMock()
        mock_port = MagicMock()
        mock_port.getName.return_value = "clientPort"
        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.input = None
            args.attributes = '{"isBehavioral":1}'

            action.execute(args)

            mock_port.setIsBehavioral.assert_called_once_with(1)
            mock_port.setIsReversed.assert_not_called()
            mock_port.setName.assert_not_called()

    def test_update_skips_unknown_fields(self) -> None:
        """UTS_PORT_00021: Test that unknown fields are skipped with warning."""
        from rhapsody_cli.actions.port_action import PortUpdateAction

        action = PortUpdateAction()
        mock_classifier = MagicMock()
        mock_port = MagicMock()
        mock_port.getName.return_value = "clientPort"
        mock_classifier.getPorts.return_value = [mock_port]

        with patch.object(action, "_resolve_classifier", return_value=mock_classifier):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.name = "clientPort"
            args.guid = None
            args.input = None
            args.attributes = '{"isBehavioral":1,"unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_port.setIsBehavioral.assert_called_once_with(1)
                mock_warning.assert_called()
                assert "unknown_field" in str(mock_warning.call_args)
