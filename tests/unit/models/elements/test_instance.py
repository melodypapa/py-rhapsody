"""Tests for rhapsody_cli.elements.instance.RPInstance."""

from rhapsody_cli.models.core import RPCollection, wrap
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


def test_instance_add_relation_to_the_whole_wraps_result() -> None:
    fake = make_fake_element("Instance")
    relation = make_fake_element("Relation", getName="whole")
    fake.addRelationToTheWhole.return_value = relation
    instance = RPInstance(fake)

    result = instance.addRelationToTheWhole("whole")

    fake.addRelationToTheWhole.assert_called_once_with("whole")
    assert result.getName() == "whole"


def test_instance_get_instantiated_by_wraps_result() -> None:
    fake = make_fake_element("Instance")
    op = make_fake_element("Operation", getName="create")
    fake.getInstantiatedBy.return_value = op
    instance = RPInstance(fake)

    result = instance.getInstantiatedBy()

    fake.getInstantiatedBy.assert_called_once_with()
    assert result.getName() == "create"


def test_instance_get_list_of_initializer_arguments_returns_collection() -> None:
    fake = make_fake_element("Instance")
    arg = make_fake_element("Argument", getName="x")
    fake.getListOfInitializerArguments.return_value = make_fake_collection([arg])
    instance = RPInstance(fake)

    result = instance.getListOfInitializerArguments()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].getName() == "x"


def test_instance_set_explicit_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.setExplicit()

    fake.setExplicit.assert_called_once_with()


def test_instance_set_implicit_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.setImplicit()

    fake.setImplicit.assert_called_once_with()


def test_instance_set_initializer_argument_value_delegates_to_com() -> None:
    fake = make_fake_element("Instance")
    instance = RPInstance(fake)

    instance.setInitializerArgumentValue("x", "42")

    fake.setInitializerArgumentValue.assert_called_once_with("x", "42")


def test_instance_set_instantiated_by_unwraps_arg() -> None:
    fake = make_fake_element("Instance")
    op = make_fake_element("Operation", getName="create")
    instance = RPInstance(fake)

    instance.setInstantiatedBy(wrap(op))

    fake.setInstantiatedBy.assert_called_once_with(op)


def test_instance_update_contained_diagrams_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Instance", updateContainedDiagramsOnServer=2)
    instance = RPInstance(fake)

    assert instance.updateContainedDiagramsOnServer(1) == 2

    fake.updateContainedDiagramsOnServer.assert_called_once_with(1)
