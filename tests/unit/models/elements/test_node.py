"""Tests for rhapsody_cli.models.elements.containment.RPNode."""

from rhapsody_cli.models.core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPNode
from tests.unit.models.fakes import make_fake_element


def test_node_is_a_unit() -> None:
    fake = make_fake_element("Node", getName="Node1")
    node = RPNode(fake)

    assert isinstance(node, RPUnit)
    assert node.getName() == "Node1"


def test_node_is_registered_for_meta_class_node() -> None:
    fake = make_fake_element("Node", getName="Node1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPNode)
