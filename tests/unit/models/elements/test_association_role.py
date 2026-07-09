"""Tests for rhapsody_cli.models.elements.relations.RPAssociationRole."""

from rhapsody_cli.models.core import wrap
from rhapsody_cli.models.elements.relations import RPAssociationRole, RPInstance
from tests.unit.models.fakes import make_fake_element


def test_association_role_is_an_instance() -> None:
    fake = make_fake_element("AssociationRole")
    role = RPAssociationRole(fake)

    assert isinstance(role, RPInstance)


def test_association_role_is_registered_for_meta_class_association_role() -> None:
    fake = make_fake_element("AssociationRole")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPAssociationRole)
