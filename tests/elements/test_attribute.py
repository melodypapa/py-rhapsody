"""Tests for rhapsody_cli.elements.attribute.RPAttribute."""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.attribute import RPAttribute
from tests.fakes import make_fake_element


def test_attribute_is_a_unit() -> None:
    fake = make_fake_element("Attribute", getName="count")
    attribute = RPAttribute(fake)

    assert isinstance(attribute, RPUnit)
    assert attribute.getName() == "count"


def test_attribute_get_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getMultiplicity="1")
    attribute = RPAttribute(fake)

    assert attribute.getMultiplicity() == "1"


def test_attribute_set_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setMultiplicity("0..*")

    fake.setMultiplicity.assert_called_once_with("0..*")


def test_attribute_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getIsStatic=0)
    attribute = RPAttribute(fake)

    assert attribute.getIsStatic() is False


def test_attribute_set_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setIsStatic(True)

    fake.setIsStatic.assert_called_once_with(1)


def test_attribute_get_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getVisibility="private")
    attribute = RPAttribute(fake)

    assert attribute.getVisibility() == "private"


def test_attribute_set_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setVisibility("public")

    fake.setVisibility.assert_called_once_with("public")


def test_attribute_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getDefaultValue="0")
    attribute = RPAttribute(fake)

    assert attribute.getDefaultValue() == "0"


def test_attribute_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setDefaultValue("42")

    fake.setDefaultValue.assert_called_once_with("42")


def test_attribute_is_registered_for_meta_class_attribute() -> None:
    fake = make_fake_element("Attribute", getName="count")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPAttribute)
