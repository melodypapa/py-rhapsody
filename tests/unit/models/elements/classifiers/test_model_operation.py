"""Tests for rhapsody_cli.elements.operation.RPOperation."""

from unittest.mock import MagicMock

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers import RPInterfaceItem, RPOperation
from tests.unit.models.fakes import make_fake_element


def test_operation_is_an_interface_item() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPInterfaceItem)
    assert operation.get_name() == "doIt"


def test_operation_get_body_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getBody="return 0;")
    operation = RPOperation(fake)

    assert operation.get_body() == "return 0;"


def test_operation_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsAbstract=1)
    operation = RPOperation(fake)

    assert operation.get_is_abstract() is True


def test_operation_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsStatic=0)
    operation = RPOperation(fake)

    assert operation.get_is_static() is False


def test_operation_get_is_virtual_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsVirtual=1)
    operation = RPOperation(fake)

    assert operation.get_is_virtual() is True


def test_operation_set_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.set_is_abstract(1)

    fake.setIsAbstract.assert_called_once_with(1)


def test_operation_set_is_abstract_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["isAbstract"])
    operation = RPOperation(fake)

    operation.set_is_abstract(1)

    assert fake.isAbstract == 1


def test_operation_set_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.set_is_static(1)

    fake.setIsStatic.assert_called_once_with(1)


def test_operation_set_is_static_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["isStatic"])
    operation = RPOperation(fake)

    operation.set_is_static(1)

    assert fake.isStatic == 1


def test_operation_set_is_virtual_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.set_is_virtual(1)

    fake.setIsVirtual.assert_called_once_with(1)


def test_operation_set_is_virtual_falls_back_to_property_when_method_missing() -> None:
    fake = MagicMock(spec=["isVirtual"])
    operation = RPOperation(fake)

    operation.set_is_virtual(1)

    assert fake.isVirtual == 1


def test_operation_get_returns_wraps_result() -> None:
    fake = make_fake_element("Operation")
    return_type = make_fake_element("Class", getName="int")
    fake.getReturns.return_value = return_type
    operation = RPOperation(fake)

    result = operation.get_returns()

    fake.getReturns.assert_called_once_with()
    assert result.get_name() == "int"


def test_operation_get_return_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getReturnTypeDeclaration="int")
    operation = RPOperation(fake)

    assert operation.get_return_type_declaration() == "int"


def test_operation_set_returns_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)
    return_type = RPOperation(make_fake_element("Class", getName="int"))

    operation.set_returns(return_type)

    fake.setReturns.assert_called_once_with(return_type._com)


def test_operation_set_return_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.set_return_type_declaration("int")

    fake.setReturnTypeDeclaration.assert_called_once_with("int")


def test_operation_create_auto_flow_chart_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.create_auto_flow_chart()

    fake.createAutoFlowChart.assert_called_once_with()


def test_operation_is_registered_for_meta_class_operation() -> None:
    fake = make_fake_element("Operation", getName="doIt")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPOperation)
