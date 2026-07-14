"""Tests for rhapsody_cli.models.elements.containment.RPNode."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit
from rhapsody_cli.models.elements.containment import RPComponentInstance, RPNode
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_node_is_a_unit() -> None:
    fake = make_fake_element("Node", getName="Node1")
    node = RPNode(fake)

    assert isinstance(node, RPUnit)
    assert node.get_name() == "Node1"


def test_node_is_registered_for_meta_class_node() -> None:
    fake = make_fake_element("Node", getName="Node1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPNode)


# Tests for methods from Task 12


def test_node_add_component_instance_delegates_and_wraps() -> None:
    fake = make_fake_element("Node")
    inst = make_fake_element("ComponentInstance", getName="Inst1")
    fake.addComponentInstance.return_value = inst
    node = RPNode(fake)

    result = node.add_component_instance("Inst1")

    fake.addComponentInstance.assert_called_once_with("Inst1")
    assert result.get_name() == "Inst1"


def test_node_get_component_instances_returns_collection() -> None:
    fake = make_fake_element("Node")
    inst = make_fake_element("ComponentInstance", getName="Inst1")
    fake.getComponentInstances.return_value = make_fake_collection([inst])
    node = RPNode(fake)

    result = node.get_component_instances()

    fake.getComponentInstances.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_node_find_component_instance_wraps_result() -> None:
    fake = make_fake_element("Node")
    inst = make_fake_element("ComponentInstance", getName="Inst1")
    fake.findComponentInstance.return_value = inst
    node = RPNode(fake)

    result = node.find_component_instance("Inst1")

    fake.findComponentInstance.assert_called_once_with("Inst1")
    assert result is not None
    assert result.get_name() == "Inst1"


def test_node_find_component_instance_returns_none_when_not_found() -> None:
    fake = make_fake_element("Node")
    fake.findComponentInstance.return_value = None
    node = RPNode(fake)

    result = node.find_component_instance("NonExistent")

    fake.findComponentInstance.assert_called_once_with("NonExistent")
    assert result is None


def test_node_delete_component_instance_delegates() -> None:
    fake = make_fake_element("Node")
    node = RPNode(fake)
    inst_fake = make_fake_element("ComponentInstance", getName="Inst1")
    inst = RPComponentInstance(inst_fake)

    node.delete_component_instance(inst)

    fake.deleteComponentInstance.assert_called_once_with(inst_fake)


def test_node_get_cpu_type_returns_str() -> None:
    fake = make_fake_element("Node")
    fake.getCPUtype.return_value = "x86"
    node = RPNode(fake)

    result = node.get_cpu_type()

    fake.getCPUtype.assert_called_once_with()
    assert result == "x86"


def test_node_set_cpu_type_delegates() -> None:
    fake = make_fake_element("Node")
    node = RPNode(fake)

    node.set_cpu_type("ARM")

    fake.setCPUtype.assert_called_once_with("ARM")
