"""Tests for rhapsody_cli.models.elements.classifiers.RPAssociationClass."""

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.classifiers import RPAssociationClass, RPClass
from tests.unit.models.fakes import make_fake_element


def test_association_class_is_a_class() -> None:
    fake = make_fake_element("AssociationClass", getName="MyAssoc")
    ac = RPAssociationClass(fake)

    assert isinstance(ac, RPClass)
    assert ac.getName() == "MyAssoc"


def test_association_class_is_registered_for_meta_class_association_class() -> None:
    fake = make_fake_element("AssociationClass", getName="MyAssoc")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPAssociationClass)
