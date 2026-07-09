"""Tests for rhapsody_cli.models.elements.containment.RPComponent."""

from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPComponent
from tests.unit.models.fakes import make_fake_element


def test_component_is_a_unit() -> None:
    fake = make_fake_element("Component", getName="Comp1")
    component = RPComponent(fake)

    assert isinstance(component, RPUnit)
    assert component.getName() == "Comp1"


def test_component_is_registered_for_meta_class_component() -> None:
    fake = make_fake_element("Component", getName="Comp1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPComponent)
