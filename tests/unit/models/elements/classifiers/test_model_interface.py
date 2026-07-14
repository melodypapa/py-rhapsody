"""Tests for rhapsody_cli.models.elements.classifiers.model_interface.RPInterface."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPInterface
from tests.unit.models.fakes import make_fake_element


def test_interface_is_model_element() -> None:
    fake = make_fake_element("Interface", getName="IFoo")
    iface = RPInterface(fake)
    assert isinstance(iface, RPModelElement)
    assert iface.get_name() == "IFoo"


def test_interface_is_registered() -> None:
    fake = make_fake_element("Interface", getName="IFoo")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPInterface)
