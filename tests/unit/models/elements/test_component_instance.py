"""Tests for rhapsody_cli.models.elements.containment.RPComponentInstance."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.containment import RPComponentInstance
from rhapsody_cli.models.elements.relations import RPInstance
from tests.unit.models.fakes import make_fake_element


def test_component_instance_is_an_instance() -> None:
    fake = make_fake_element("ComponentInstance", getName="CompInst1")
    comp_inst = RPComponentInstance(fake)

    assert isinstance(comp_inst, RPInstance)
    assert comp_inst.get_name() == "CompInst1"


def test_component_instance_is_registered_for_meta_class_component_instance() -> None:
    fake = make_fake_element("ComponentInstance", getName="CompInst1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPComponentInstance)
