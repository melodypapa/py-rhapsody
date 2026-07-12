"""Tests for rhapsody_cli.models.elements.classifiers.model_enumeration.RPEnumeration."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPEnumeration
from tests.unit.models.fakes import make_fake_element


def test_enumeration_is_model_element() -> None:
    fake = make_fake_element("Enumeration", getName="Color")
    enum = RPEnumeration(fake)
    assert isinstance(enum, RPModelElement)
    assert enum.get_name() == "Color"


def test_enumeration_is_registered() -> None:
    fake = make_fake_element("Enumeration", getName="Color")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPEnumeration)
