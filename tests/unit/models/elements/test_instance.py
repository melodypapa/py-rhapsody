"""Tests for rhapsody_cli.elements.instance.RPInstance."""

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.relations import RPInstance, RPRelation
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_instance_is_a_relation() -> None:
    fake = make_fake_element("Instance", getName="driver1")
    instance = RPInstance(fake)

    assert isinstance(instance, RPRelation)
    assert instance.getName() == "driver1"


def test_instance_get_all_nested_elements_returns_collection() -> None:
    fake = make_fake_element("Instance")
    nested = make_fake_element("Attribute", getName="speed")
    fake.getAllNestedElements.return_value = make_fake_collection([nested])
    instance = RPInstance(fake)

    nested_elements = instance.getAllNestedElements()

    assert len(nested_elements) == 1
    assert nested_elements[0].getName() == "speed"


def test_instance_get_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance", getAttributeValue="42")
    instance = RPInstance(fake)

    assert instance.getAttributeValue("speed") == "42"

    fake.getAttributeValue.assert_called_once_with("speed")


def test_instance_set_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.setAttributeValue("speed", "88")

    fake.setAttributeValue.assert_called_once_with("speed", "88")


def test_instance_get_in_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn1")
    fake.getInLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.getInLinks()

    assert len(links) == 1
    assert links[0].getName() == "conn1"


def test_instance_get_out_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn2")
    fake.getOutLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.getOutLinks()

    assert len(links) == 1
    assert links[0].getName() == "conn2"


def test_instance_is_registered_for_meta_class_instance() -> None:
    fake = make_fake_element("Instance", getName="driver1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPInstance)
