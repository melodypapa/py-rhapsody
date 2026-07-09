"""Tests for rhapsody_cli.models.elements.relations.RPDependency."""

from rhapsody_cli.models.core import RPModelElement, wrap
from rhapsody_cli.models.elements.relations import RPDependency
from tests.unit.models.fakes import make_fake_element


def test_dependency_is_a_model_element() -> None:
    fake = make_fake_element("Dependency")
    dep = RPDependency(fake)

    assert isinstance(dep, RPModelElement)


def test_dependency_is_registered_for_meta_class_dependency() -> None:
    fake = make_fake_element("Dependency")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPDependency)
