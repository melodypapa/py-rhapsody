"""Tests for rhapsody_cli.models.elements.classifiers.RPInterfaceItem."""

from rhapsody_cli.models.core import RPCollection
from rhapsody_cli.models.elements.classifiers import RPClassifier, RPInterfaceItem
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_interface_item_is_a_classifier() -> None:
    fake = make_fake_element("InterfaceItem", getName="doIt")
    item = RPInterfaceItem(fake)

    assert isinstance(item, RPClassifier)
    assert item.getName() == "doIt"


def test_interface_item_add_argument_wraps_result() -> None:
    fake = make_fake_element("InterfaceItem")
    argument = make_fake_element("Argument", getName="x")
    fake.addArgument.return_value = argument
    item = RPInterfaceItem(fake)

    result = item.addArgument("x")

    fake.addArgument.assert_called_once_with("x")
    assert result.getName() == "x"


def test_interface_item_add_argument_before_position_wraps_result() -> None:
    fake = make_fake_element("InterfaceItem")
    argument = make_fake_element("Argument", getName="y")
    fake.addArgumentBeforePosition.return_value = argument
    item = RPInterfaceItem(fake)

    result = item.addArgumentBeforePosition("y", 1)

    fake.addArgumentBeforePosition.assert_called_once_with("y", 1)
    assert result.getName() == "y"


def test_interface_item_get_arguments_returns_collection() -> None:
    inner = make_fake_element("Argument", getName="x")
    fake = make_fake_element("InterfaceItem")
    fake.getArguments.return_value = make_fake_collection([inner])
    item = RPInterfaceItem(fake)

    result = item.getArguments()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_interface_item_get_signature_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignature="void doIt(int x)")
    item = RPInterfaceItem(fake)

    assert item.getSignature() == "void doIt(int x)"


def test_interface_item_get_signature_no_arg_names_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignatureNoArgNames="void doIt(int)")
    item = RPInterfaceItem(fake)

    assert item.getSignatureNoArgNames() == "void doIt(int)"


def test_interface_item_get_signature_no_arg_types_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignatureNoArgTypes="void doIt(x)")
    item = RPInterfaceItem(fake)

    assert item.getSignatureNoArgTypes() == "void doIt(x)"


def test_interface_item_match_on_signature_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", matchOnSignature=1)
    other = make_fake_element("InterfaceItem")
    item = RPInterfaceItem(fake)

    result = item.matchOnSignature(RPInterfaceItem(other))

    fake.matchOnSignature.assert_called_once_with(other)
    assert result is True
