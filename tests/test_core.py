"""Tests for py_rhapsody._core: call_com, RPModelElement, wrap()."""

from __future__ import annotations

import pytest

from py_rhapsody._core import RPModelElement, call_com
from py_rhapsody.exceptions import RhapsodyRuntimeException
from tests.fakes import make_com_error, make_fake_element


def test_call_com_returns_value_on_success() -> None:
    result = call_com(lambda: 42)

    assert result == 42


def test_call_com_translates_com_error() -> None:
    def failing() -> int:
        raise make_com_error("getName failed")

    with pytest.raises(RhapsodyRuntimeException, match="getName failed"):
        call_com(failing)


def test_call_com_does_not_translate_other_exceptions() -> None:
    def failing() -> int:
        raise ValueError("not a COM error")

    with pytest.raises(ValueError, match="not a COM error"):
        call_com(failing)


def test_model_element_get_name_delegates_to_com() -> None:
    fake = make_fake_element("Class", getName="Widget")
    element = RPModelElement(fake)

    assert element.getName() == "Widget"
    fake.getName.assert_called_once_with()


def test_model_element_set_name_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    element = RPModelElement(fake)

    element.setName("NewName")

    fake.setName.assert_called_once_with("NewName")


def test_model_element_get_meta_class_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    element = RPModelElement(fake)

    assert element.getMetaClass() == "Package"


def test_model_element_get_guid_delegates_to_com() -> None:
    fake = make_fake_element("Class", getGUID="guid-123")
    element = RPModelElement(fake)

    assert element.getGUID() == "guid-123"


def test_model_element_com_error_becomes_rhapsody_runtime_exception() -> None:
    fake = make_fake_element("Class")
    fake.getName.side_effect = make_com_error("boom")
    element = RPModelElement(fake)

    with pytest.raises(RhapsodyRuntimeException, match="boom"):
        element.getName()


def test_model_element_equality_by_underlying_com_object() -> None:
    fake = make_fake_element("Class")

    assert RPModelElement(fake) == RPModelElement(fake)
    assert RPModelElement(fake) != RPModelElement(make_fake_element("Class"))
