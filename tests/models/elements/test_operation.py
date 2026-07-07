"""Tests for rhapsody_cli.elements.operation.RPOperation."""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.operation import RPOperation
from tests.models.fakes import make_fake_element


def test_operation_is_a_unit() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPUnit)
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


def test_operation_create_auto_flow_chart_delegates_to_com() -> None:
    fake = make_fake_element("Operation")
    operation = RPOperation(fake)

    operation.createAutoFlowChart()

    fake.createAutoFlowChart.assert_called_once_with()


def test_operation_is_registered_for_meta_class_operation() -> None:
    fake = make_fake_element("Operation", getName="doIt")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPOperation)
