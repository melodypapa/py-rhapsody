"""Tests for rhapsody_cli.models.elements.containment.RPModule."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.containment import RPModule
from rhapsody_cli.models.elements.relations import RPInstance
from tests.unit.models.fakes import make_fake_element


def test_module_is_an_instance() -> None:
    fake = make_fake_element("Module", getName="Module1")
    module = RPModule(fake)

    assert isinstance(module, RPInstance)
    assert module.get_name() == "Module1"


def test_module_is_registered_for_meta_class_module() -> None:
    fake = make_fake_element("Module", getName="Module1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPModule)
