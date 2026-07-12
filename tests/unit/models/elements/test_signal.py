"""Tests for rhapsody_cli.models.elements.classifiers.model_signal.RPSignal."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPSignal
from tests.unit.models.fakes import make_fake_element


def test_signal_is_model_element() -> None:
    fake = make_fake_element("Signal", getName="Sig1")
    sig = RPSignal(fake)
    assert isinstance(sig, RPModelElement)
    assert sig.get_name() == "Sig1"


def test_signal_is_registered() -> None:
    fake = make_fake_element("Signal", getName="Sig1")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPSignal)
