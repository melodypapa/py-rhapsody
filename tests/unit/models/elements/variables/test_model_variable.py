"""Tests for rhapsody_cli.models.elements.variables.RPVariable."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.variables.model_variables import RPVariable
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_variable_is_a_unit() -> None:
    fake = make_fake_element("Variable", getName="count")
    variable = RPVariable(fake)

    assert isinstance(variable, RPUnit)
    assert variable.get_name() == "count"


def test_variable_add_element_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    new_value = make_fake_element("Class", getName="Extra")
    element = make_fake_element("Class", getName="Extra")
    fake.addElementDefaultValue.return_value = new_value
    variable = RPVariable(fake)

    result = variable.add_element_default_value(AbstractRPModelElement.wrap(element))

    fake.addElementDefaultValue.assert_called_once_with(element)
    assert result.get_name() == "Extra"


def test_variable_add_string_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    literal = make_fake_element("LiteralSpecification", getName="42")
    fake.addStringDefaultValue.return_value = literal
    variable = RPVariable(fake)

    result = variable.add_string_default_value("42")

    fake.addStringDefaultValue.assert_called_once_with("42")
    assert result.get_name() == "42"


def test_variable_get_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDeclaration="int*")
    variable = RPVariable(fake)

    assert variable.get_declaration() == "int*"


def test_variable_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDefaultValue="0")
    variable = RPVariable(fake)

    assert variable.get_default_value() == "0"


def test_variable_get_type_wraps_result() -> None:
    fake = make_fake_element("Variable")
    type_com = make_fake_element("Class", getName="int")
    fake.getType.return_value = type_com
    variable = RPVariable(fake)

    result = variable.get_type()

    fake.getType.assert_called_once_with()
    assert result.get_name() == "int"


def test_variable_get_value_specifications_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Spec")
    fake = make_fake_element("Variable")
    fake.getValueSpecifications.return_value = make_fake_collection([inner])
    variable = RPVariable(fake)

    result = variable.get_value_specifications()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_variable_set_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.set_declaration("int*")

    fake.setDeclaration.assert_called_once_with("int*")


def test_variable_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.set_default_value("42")

    fake.setDefaultValue.assert_called_once_with("42")


def test_variable_set_type_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    type_fake = make_fake_element("Class", getName="int")
    variable = RPVariable(fake)

    variable.set_type(RPClassifier(type_fake))

    fake.setType.assert_called_once_with(type_fake)


def test_variable_set_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.set_type_declaration("int*")

    fake.setTypeDeclaration.assert_called_once_with("int*")


# =============================================================================
# RPAttribute tests
# =============================================================================


def test_attribute_get_is_constant_returns_int() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsConstant=1)
    attr = RPAttribute(fake)
    assert attr.get_is_constant() == 1
    fake.getIsConstant.assert_called_once_with()


def test_attribute_get_is_constant_returns_zero() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsConstant=0)
    attr = RPAttribute(fake)
    assert attr.get_is_constant() == 0
    fake.getIsConstant.assert_called_once_with()


def test_attribute_get_is_ordered_returns_int() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsOrdered=1)
    attr = RPAttribute(fake)
    assert attr.get_is_ordered() == 1
    fake.getIsOrdered.assert_called_once_with()


def test_attribute_get_is_ordered_returns_zero() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsOrdered=0)
    attr = RPAttribute(fake)
    assert attr.get_is_ordered() == 0
    fake.getIsOrdered.assert_called_once_with()


def test_attribute_get_is_reference_returns_int() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsReference=1)
    attr = RPAttribute(fake)
    assert attr.get_is_reference() == 1
    fake.getIsReference.assert_called_once_with()


def test_attribute_get_is_reference_returns_zero() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute", getIsReference=0)
    attr = RPAttribute(fake)
    assert attr.get_is_reference() == 0
    fake.getIsReference.assert_called_once_with()


def test_attribute_set_is_constant_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_constant(True)

    fake.setIsConstant.assert_called_once_with(1)


def test_attribute_set_is_constant_false_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_constant(False)

    fake.setIsConstant.assert_called_once_with(0)


def test_attribute_set_is_ordered_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_ordered(True)

    fake.setIsOrdered.assert_called_once_with(1)


def test_attribute_set_is_ordered_false_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_ordered(False)

    fake.setIsOrdered.assert_called_once_with(0)


def test_attribute_set_is_reference_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_reference(True)

    fake.setIsReference.assert_called_once_with(1)


def test_attribute_set_is_reference_false_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPAttribute

    fake = make_fake_element("Attribute")
    attr = RPAttribute(fake)

    attr.set_is_reference(False)

    fake.setIsReference.assert_called_once_with(0)


# =============================================================================
# RPTag tests
# =============================================================================


def test_tag_get_base_wraps_result() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    base_com = make_fake_element("Class", getName="BaseClass")
    fake = make_fake_element("Tag")
    fake.getBase.return_value = base_com
    tag = RPTag(fake)

    result = tag.get_base()

    fake.getBase.assert_called_once_with()
    assert result.get_name() == "BaseClass"


def test_tag_get_from_profile_returns_profile() -> None:
    from rhapsody_cli.models.elements.containment.model_profile import RPProfile
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake_profile = make_fake_element("Profile", getName="MyProfile")
    fake = make_fake_element("Tag", getFromProfile=fake_profile)
    tag = RPTag(fake)

    result = tag.get_from_profile()
    assert isinstance(result, RPProfile)
    assert result.get_name() == "MyProfile"
    fake.getFromProfile.assert_called_once_with()


def test_tag_get_multiplicity_returns_str() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag", getMultiplicity="0..*")
    tag = RPTag(fake)

    assert tag.get_multiplicity() == "0..*"
    fake.getMultiplicity.assert_called_once_with()


def test_tag_get_tag_meta_class_returns_str() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag", getTagMetaClass="Stereotype")
    tag = RPTag(fake)

    assert tag.get_tag_meta_class() == "Stereotype"
    fake.getTagMetaClass.assert_called_once_with()


def test_tag_get_value_returns_str() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag", getValue="some_value")
    tag = RPTag(fake)

    assert tag.get_value() == "some_value"
    fake.getValue.assert_called_once_with()


def test_tag_set_multiplicity_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag")
    tag = RPTag(fake)

    tag.set_multiplicity("1..*")

    fake.setMultiplicity.assert_called_once_with("1..*")


def test_tag_set_tag_meta_class_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag")
    tag = RPTag(fake)

    tag.set_tag_meta_class("NewStereotype")

    fake.setTagMetaClass.assert_called_once_with("NewStereotype")


def test_tag_set_value_delegates_to_com() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag")
    tag = RPTag(fake)

    tag.set_value("new_value")

    fake.setValue.assert_called_once_with("new_value")
