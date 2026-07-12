"""Tests for rhapsody_cli.elements.instance.RPInstance."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.relations import RPInstance, RPRelation
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_instance_is_a_relation() -> None:
    fake = make_fake_element("Instance", getName="driver1")
    instance = RPInstance(fake)

    assert isinstance(instance, RPRelation)
    assert instance.get_name() == "driver1"


def test_instance_get_all_nested_elements_returns_collection() -> None:
    fake = make_fake_element("Instance")
    nested = make_fake_element("Attribute", getName="speed")
    fake.getAllNestedElements.return_value = make_fake_collection([nested])
    instance = RPInstance(fake)

    nested_elements = instance.get_all_nested_elements()

    assert len(nested_elements) == 1
    assert nested_elements[0].get_name() == "speed"


def test_instance_get_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance", getAttributeValue="42")
    instance = RPInstance(fake)

    assert instance.get_attribute_value("speed") == "42"

    fake.getAttributeValue.assert_called_once_with("speed")


def test_instance_set_attribute_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.set_attribute_value("speed", "88")

    fake.setAttributeValue.assert_called_once_with("speed", "88")


def test_instance_get_in_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn1")
    fake.getInLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.get_in_links()

    assert len(links) == 1
    assert links[0].get_name() == "conn1"


def test_instance_get_out_links_returns_collection() -> None:
    fake = make_fake_element("Instance")
    link = make_fake_element("Link", getName="conn2")
    fake.getOutLinks.return_value = make_fake_collection([link])
    instance = RPInstance(fake)

    links = instance.get_out_links()

    assert len(links) == 1
    assert links[0].get_name() == "conn2"


def test_instance_is_registered_for_meta_class_instance() -> None:
    fake = make_fake_element("Instance", getName="driver1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPInstance)


def test_instance_add_relation_to_the_whole_wraps_result() -> None:
    fake = make_fake_element("Instance")
    relation = make_fake_element("Relation", getName="whole")
    fake.addRelationToTheWhole.return_value = relation
    instance = RPInstance(fake)

    result = instance.add_relation_to_the_whole("whole")

    fake.addRelationToTheWhole.assert_called_once_with("whole")
    assert result.get_name() == "whole"


def test_instance_get_instantiated_by_wraps_result() -> None:
    fake = make_fake_element("Instance")
    op = make_fake_element("Operation", getName="create")
    fake.getInstantiatedBy.return_value = op
    instance = RPInstance(fake)

    result = instance.get_instantiated_by()

    fake.getInstantiatedBy.assert_called_once_with()
    assert result.get_name() == "create"


def test_instance_get_list_of_initializer_arguments_returns_collection() -> None:
    fake = make_fake_element("Instance")
    arg = make_fake_element("Argument", getName="x")
    fake.getListOfInitializerArguments.return_value = make_fake_collection([arg])
    instance = RPInstance(fake)

    result = instance.get_list_of_initializer_arguments()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "x"


def test_instance_set_explicit_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.set_explicit()

    fake.setExplicit.assert_called_once_with()


def test_instance_set_implicit_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.set_implicit()

    fake.setImplicit.assert_called_once_with()


def test_instance_set_initializer_argument_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.set_initializer_argument_value("x", "42")

    fake.setInitializerArgumentValue.assert_called_once_with("x", "42")


def test_instance_set_instantiated_by_unwraps_arg() -> None:
    fake = make_fake_element("Instance")
    op = make_fake_element("Operation", getName="create")
    instance = RPInstance(fake)

    instance.set_instantiated_by(AbstractRPModelElement.wrap(op))

    fake.setInstantiatedBy.assert_called_once_with(op)


def test_instance_update_contained_diagrams_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Instance", updateContainedDiagramsOnServer=2)
    instance = RPInstance(fake)

    assert instance.update_contained_diagrams_on_server(1) == 2

    fake.updateContainedDiagramsOnServer.assert_called_once_with(1)
