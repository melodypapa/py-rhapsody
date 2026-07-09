"""Tests for rhapsody_cli.models.elements.relations.RPHyperLink."""

from rhapsody_cli.models.core import wrap
from rhapsody_cli.models.elements.relations import RPDependency, RPHyperLink
from tests.unit.models.fakes import make_fake_element


def test_hyperlink_is_a_dependency() -> None:
    fake = make_fake_element("HyperLink")
    link = RPHyperLink(fake)

    assert isinstance(link, RPDependency)


def test_hyperlink_is_registered_for_meta_class_hyperlink() -> None:
    fake = make_fake_element("HyperLink")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPHyperLink)
