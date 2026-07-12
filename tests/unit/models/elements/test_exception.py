"""Tests for rhapsody_cli.models.elements.classifiers.model_exception.RPException."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPException
from tests.unit.models.fakes import make_fake_element


def test_exception_is_model_element() -> None:
    fake = make_fake_element("Exception", getName="Exc1")
    exc = RPException(fake)
    assert isinstance(exc, RPModelElement)
    assert exc.get_name() == "Exc1"


def test_exception_is_registered() -> None:
    fake = make_fake_element("Exception", getName="Exc1")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPException)
