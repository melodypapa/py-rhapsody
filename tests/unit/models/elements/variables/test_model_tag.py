"""Tests for rhapsody_cli.models.elements.variables.RPTag."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.variables.model_variables import RPTag, RPVariable
from tests.unit.models.fakes import make_fake_element


def test_tag_is_a_variable() -> None:
    fake = make_fake_element("Tag", getName="MyTag")
    tag = RPTag(fake)

    assert isinstance(tag, RPVariable)
    assert tag.get_name() == "MyTag"


def test_tag_is_registered_for_meta_class_tag() -> None:
    fake = make_fake_element("Tag", getName="MyTag")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPTag)
