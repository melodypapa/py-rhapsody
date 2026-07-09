"""Tests for rhapsody_cli.models.elements.relations.RPGeneralization."""

from rhapsody_cli.models._core import RPModelElement, wrap
from rhapsody_cli.models.elements.relations import RPGeneralization
from tests.unit.models.fakes import make_fake_element


def test_generalization_is_a_model_element() -> None:
    fake = make_fake_element("Generalization")
    gen = RPGeneralization(fake)

    assert isinstance(gen, RPModelElement)


def test_generalization_is_registered_for_meta_class_generalization() -> None:
    fake = make_fake_element("Generalization")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPGeneralization)
