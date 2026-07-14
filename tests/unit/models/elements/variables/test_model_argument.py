"""Tests for rhapsody_cli.models.elements.variables.model_variables.RPArgument."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.variables.model_variables import RPArgument, RPVariable
from tests.unit.models.fakes import make_fake_element


def test_argument_is_a_variable() -> None:
    fake = make_fake_element("Argument", getName="id")
    argument = RPArgument(fake)

    assert isinstance(argument, RPVariable)
    assert argument.get_name() == "id"


def test_argument_get_argument_direction_delegates_to_com() -> None:
    fake = make_fake_element("Argument", getArgumentDirection="in")
    argument = RPArgument(fake)

    assert argument.get_argument_direction() == "in"


def test_argument_set_argument_direction_delegates_to_com() -> None:
    fake = make_fake_element("Argument")
    argument = RPArgument(fake)

    argument.set_argument_direction("out")

    fake.setArgumentDirection.assert_called_once_with("out")


def test_argument_is_registered_for_meta_class_argument() -> None:
    fake = make_fake_element("Argument", getName="id")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPArgument)
