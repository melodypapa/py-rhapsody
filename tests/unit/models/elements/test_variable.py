"""Tests for rhapsody_cli.models.elements.variables.RPVariable."""

from rhapsody_cli.models._core import RPCollection, RPUnit, wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.variables import RPVariable
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_variable_is_a_unit() -> None:
    fake = make_fake_element("Variable", getName="count")
    variable = RPVariable(fake)

    assert isinstance(variable, RPUnit)
    assert variable.getName() == "count"


def test_variable_add_element_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    new_value = make_fake_element("Class", getName="Extra")
    element = make_fake_element("Class", getName="Extra")
    fake.addElementDefaultValue.return_value = new_value
    variable = RPVariable(fake)

    result = variable.addElementDefaultValue(wrap(element))

    fake.addElementDefaultValue.assert_called_once_with(element)
    assert result.getName() == "Extra"


def test_variable_add_string_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    literal = make_fake_element("LiteralSpecification", getName="42")
    fake.addStringDefaultValue.return_value = literal
    variable = RPVariable(fake)

    result = variable.addStringDefaultValue("42")

    fake.addStringDefaultValue.assert_called_once_with("42")
    assert result.getName() == "42"


def test_variable_get_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDeclaration="int*")
    variable = RPVariable(fake)

    assert variable.getDeclaration() == "int*"


def test_variable_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDefaultValue="0")
    variable = RPVariable(fake)

    assert variable.getDefaultValue() == "0"


def test_variable_get_type_wraps_result() -> None:
    fake = make_fake_element("Variable")
    type_com = make_fake_element("Class", getName="int")
    fake.getType.return_value = type_com
    variable = RPVariable(fake)

    result = variable.getType()

    fake.getType.assert_called_once_with()
    assert result.getName() == "int"


def test_variable_get_value_specifications_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Spec")
    fake = make_fake_element("Variable")
    fake.getValueSpecifications.return_value = make_fake_collection([inner])
    variable = RPVariable(fake)

    result = variable.getValueSpecifications()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_variable_set_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setDeclaration("int*")

    fake.setDeclaration.assert_called_once_with("int*")


def test_variable_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setDefaultValue("42")

    fake.setDefaultValue.assert_called_once_with("42")


def test_variable_set_type_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    type_fake = make_fake_element("Class", getName="int")
    variable = RPVariable(fake)

    variable.setType(RPClassifier(type_fake))

    fake.setType.assert_called_once_with(type_fake)


def test_variable_set_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setTypeDeclaration("int*")

    fake.setTypeDeclaration.assert_called_once_with("int*")
