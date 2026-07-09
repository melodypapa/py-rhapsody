"""Tests for rhapsody_cli.models.elements.containment.RPCollaboration."""

from rhapsody_cli.models.core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPCollaboration
from tests.unit.models.fakes import make_fake_element


def test_collaboration_is_a_unit() -> None:
    fake = make_fake_element("Collaboration", getName="Collab1")
    collab = RPCollaboration(fake)

    assert isinstance(collab, RPUnit)
    assert collab.getName() == "Collab1"


def test_collaboration_is_registered_for_meta_class_collaboration() -> None:
    fake = make_fake_element("Collaboration", getName="Collab1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPCollaboration)
