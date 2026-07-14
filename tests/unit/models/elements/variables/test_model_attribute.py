"""Tests for rhapsody_cli.elements.attribute.RPAttribute."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.variables.model_variables import RPAttribute, RPVariable
from tests.unit.models.fakes import make_fake_element


def test_attribute_is_a_variable() -> None:
    fake = make_fake_element("Attribute", getName="count")
    attribute = RPAttribute(fake)

    assert isinstance(attribute, RPVariable)
    assert attribute.get_name() == "count"


def test_attribute_get_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getMultiplicity="1")
    attribute = RPAttribute(fake)

    assert attribute.get_multiplicity() == "1"


def test_attribute_set_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.set_multiplicity("0..*")

    fake.setMultiplicity.assert_called_once_with("0..*")


def test_attribute_get_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getIsStatic=0)
    attribute = RPAttribute(fake)

    assert attribute.get_is_static() is False


def test_attribute_set_is_static_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.set_is_static(True)

    fake.setIsStatic.assert_called_once_with(1)


def test_attribute_get_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getVisibility="private")
    attribute = RPAttribute(fake)

    assert attribute.get_visibility() == "private"


def test_attribute_set_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.set_visibility("public")

    fake.setVisibility.assert_called_once_with("public")


def test_attribute_is_registered_for_meta_class_attribute() -> None:
    fake = make_fake_element("Attribute", getName="count")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPAttribute)
