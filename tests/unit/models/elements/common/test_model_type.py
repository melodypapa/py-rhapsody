"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPType."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.common import RPType
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPType:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Type", getName="T1")
        t = RPType(fake)
        assert isinstance(t, RPModelElement)
        assert t.get_name() == "T1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Type", getName="T1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPType)

    def test_add_enumeration_literal_delegates_and_wraps(self) -> None:
        # Pattern E

        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.addEnumerationLiteral.return_value = lit
        t = RPType(fake)
        wrapped = t.add_enumeration_literal("RED")
        assert wrapped.get_name() == "RED"
        fake.addEnumerationLiteral.assert_called_once_with("RED")

    def test_delete_enumeration_literal_delegates(self) -> None:
        # Pattern F
        from rhapsody_cli.models.elements.common import RPEnumerationLiteral

        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.deleteEnumerationLiteral.return_value = None
        t = RPType(fake)
        t.delete_enumeration_literal(RPEnumerationLiteral(lit))
        fake.deleteEnumerationLiteral.assert_called_once_with(lit)

    def test_get_declaration_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Type", getDeclaration="int x")
        t = RPType(fake)
        assert t.get_declaration() == "int x"
        fake.getDeclaration.assert_called_once_with()

    def test_get_enumeration_literals_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.getEnumerationLiterals.return_value = make_fake_collection([lit])
        t = RPType(fake)
        result = t.get_enumeration_literals()
        assert isinstance(result, RPCollection)
        fake.getEnumerationLiterals.assert_called_once_with()

    def test_get_is_predefined_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsPredefined=True)
        t = RPType(fake)
        assert t.get_is_predefined() == 1

    def test_get_is_typedef_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsTypedef=True)
        t = RPType(fake)
        assert t.get_is_typedef() == 1

    def test_get_is_typedef_constant_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsTypedefConstant=True)
        t = RPType(fake)
        assert t.get_is_typedef_constant() == 1

    def test_get_is_typedef_ordered_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsTypedefOrdered=True)
        t = RPType(fake)
        assert t.get_is_typedef_ordered() == 1

    def test_get_is_typedef_reference_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsTypedefReference=True)
        t = RPType(fake)
        assert t.get_is_typedef_reference() == 1

    def test_get_kind_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Type", getKind="Enumeration")
        t = RPType(fake)
        assert t.get_kind() == "Enumeration"

    def test_get_typedef_base_type_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("Type")
        base = make_fake_element("Class", getName="Base")
        fake.getTypedefBaseType.return_value = base
        t = RPType(fake)
        wrapped = t.get_typedef_base_type()
        assert wrapped.get_name() == "Base"
        fake.getTypedefBaseType.assert_called_once_with()

    def test_get_typedef_multiplicity_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Type", getTypedefMultiplicity="0..1")
        t = RPType(fake)
        assert t.get_typedef_multiplicity() == "0..1"

    def test_is_array_returns_int(self) -> None:
        # Pattern G — representative for all 16 is_* checks
        fake = make_fake_element("Type", isArray=True)
        t = RPType(fake)
        assert t.is_array() == 1

    def test_is_enum_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isEnum=True)
        t = RPType(fake)
        assert t.is_enum() == 1

    def test_is_equal_to_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isEqualTo=True)
        t = RPType(fake)
        assert t.is_equal_to() == 1

    def test_is_implicit_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isImplicit=True)
        t = RPType(fake)
        assert t.is_implicit() == 1

    def test_is_kind_enumeration_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindEnumeration=True)
        t = RPType(fake)
        assert t.is_kind_enumeration() == 1

    def test_is_kind_language_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindLanguage=True)
        t = RPType(fake)
        assert t.is_kind_language() == 1

    def test_is_kind_struct_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindStruct=True)
        t = RPType(fake)
        assert t.is_kind_struct() == 1

    def test_is_kind_typedef_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindTypedef=True)
        t = RPType(fake)
        assert t.is_kind_typedef() == 1

    def test_is_kind_union_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindUnion=True)
        t = RPType(fake)
        assert t.is_kind_union() == 1

    def test_is_pointer_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isPointer=True)
        t = RPType(fake)
        assert t.is_pointer() == 1

    def test_is_pointer_to_pointer_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isPointerToPointer=True)
        t = RPType(fake)
        assert t.is_pointer_to_pointer() == 1

    def test_is_reference_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isReference=True)
        t = RPType(fake)
        assert t.is_reference() == 1

    def test_is_reference_to_pointer_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isReferenceToPointer=True)
        t = RPType(fake)
        assert t.is_reference_to_pointer() == 1

    def test_is_struct_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isStruct=True)
        t = RPType(fake)
        assert t.is_struct() == 1

    def test_is_template_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isTemplate=True)
        t = RPType(fake)
        assert t.is_template() == 1

    def test_is_union_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isUnion=True)
        t = RPType(fake)
        assert t.is_union() == 1

    def test_set_kind_delegates(self) -> None:
        # Pattern D — representative for set_* str-arg setters
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_kind("Enumeration")
        fake.setKind.assert_called_once_with("Enumeration")

    def test_set_declaration_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_declaration("int x")
        fake.setDeclaration.assert_called_once_with("int x")

    def test_set_is_typedef_constant_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_is_typedef_constant(1)
        fake.setIsTypedefConstant.assert_called_once_with(1)

    def test_set_is_typedef_ordered_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_is_typedef_ordered(1)
        fake.setIsTypedefOrdered.assert_called_once_with(1)

    def test_set_is_typedef_reference_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_is_typedef_reference(1)
        fake.setIsTypedefReference.assert_called_once_with(1)

    def test_set_typedef_base_type_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier

        fake = make_fake_element("Type")
        base = make_fake_element("Class", getName="Base")
        t = RPType(fake)
        t.set_typedef_base_type(RPClassifier(base))
        fake.setTypedefBaseType.assert_called_once_with(base)

    def test_set_typedef_multiplicity_delegates(self) -> None:
        # Pattern D — str-arg setter
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_typedef_multiplicity("0..1")
        fake.setTypedefMultiplicity.assert_called_once_with("0..1")
