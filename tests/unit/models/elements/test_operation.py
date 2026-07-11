"""Tests for rhapsody_cli.elements.operation.RPOperation."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers import RPInterfaceItem, RPOperation
from tests.unit.models.fakes import make_fake_element


def test_operation_is_an_interface_item() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPInterfaceItem)
    assert operation.getName() == "doIt"


def test_operation_get_body_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getBody="return 0;")
    operation = RPOperation(fake)

    assert operation.getBody() == "return 0;"


def test_operation_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsAbstract=1)
    operation = RPOperation(fake)

    assert operation.getIsAbstract() is True


def test_operation_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsStatic=0)
    operation = RPOperation(fake)

    assert operation.getIsStatic() is False


def test_operation_get_is_virtual_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getIsVirtual=1)
    operation = RPOperation(fake)

    assert operation.getIsVirtual() is True


def test_operation_get_returns_wraps_result() -> None:
    fake = make_fake_element("Operation")
    return_type = make_fake_element("Class", getName="int")
    fake.getReturns.return_value = return_type
    operation = RPOperation(fake)

    result = operation.getReturns()

    fake.getReturns.assert_called_once_with()
    assert result.getName() == "int"


def test_operation_get_return_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Operation", getReturnTypeDeclaration="int")
    operation = RPOperation(fake)

    assert operation.getReturnTypeDeclaration() == "int"


def test_operation_set_returns_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)
    return_type = RPOperation(make_fake_element("Class", getName="int"))

    operation.setReturns(return_type)

    fake.setReturns.assert_called_once_with(return_type._com)


def test_operation_set_return_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.setReturnTypeDeclaration("int")

    fake.setReturnTypeDeclaration.assert_called_once_with("int")


def test_operation_create_auto_flow_chart_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.createAutoFlowChart()

    fake.createAutoFlowChart.assert_called_once_with()


def test_operation_is_registered_for_meta_class_operation() -> None:
    fake = make_fake_element("Operation", getName="doIt")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPOperation)
