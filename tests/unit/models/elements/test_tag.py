"""Tests for rhapsody_cli.models.elements.variables.RPTag."""

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.variables import RPTag, RPVariable
from tests.unit.models.fakes import make_fake_element


def test_tag_is_a_variable() -> None:
    fake = make_fake_element("Tag", getName="MyTag")
    tag = RPTag(fake)

    assert isinstance(tag, RPVariable)
    assert tag.getName() == "MyTag"


def test_tag_is_registered_for_meta_class_tag() -> None:
    fake = make_fake_element("Tag", getName="MyTag")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPTag)
