"""Tests for rhapsody_cli.models.elements.relations.RPRelation."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.relations import RPRelation
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_relation_is_a_unit() -> None:
    fake = make_fake_element("Relation", getName="assoc1")
    relation = RPRelation(fake)

    assert isinstance(relation, RPUnit)
    assert relation.get_name() == "assoc1"


def test_relation_add_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    qualifier = make_fake_element("Class", getName="Key")
    relation = RPRelation(fake)

    relation.add_qualifier(AbstractRPModelElement.wrap(qualifier))

    fake.addQualifier.assert_called_once_with(qualifier)


def test_relation_get_association_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    assoc_class = make_fake_element("AssociationClass", getName="LinkClass")
    fake.getAssociationClass.return_value = assoc_class
    relation = RPRelation(fake)

    result = relation.get_association_class()

    fake.getAssociationClass.assert_called_once_with()
    assert result.get_name() == "LinkClass"


def test_relation_get_inverse_wraps_result() -> None:
    fake = make_fake_element("Relation")
    inverse = make_fake_element("Relation", getName="inverseAssoc")
    fake.getInverse.return_value = inverse
    relation = RPRelation(fake)

    result = relation.get_inverse()

    fake.getInverse.assert_called_once_with()
    assert result.get_name() == "inverseAssoc"


def test_relation_get_is_navigable_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getIsNavigable=1)
    relation = RPRelation(fake)

    assert relation.get_is_navigable() is True


def test_relation_get_is_symmetric_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getIsSymmetric=0)
    relation = RPRelation(fake)

    assert relation.get_is_symmetric() is False


def test_relation_get_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getMultiplicity="0..*")
    relation = RPRelation(fake)

    assert relation.get_multiplicity() == "0..*"


def test_relation_get_object_as_object_type_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Widget")
    fake.getObjectAsObjectType.return_value = klass
    relation = RPRelation(fake)

    result = relation.get_object_as_object_type()

    fake.getObjectAsObjectType.assert_called_once_with()
    assert result.get_name() == "Widget"


def test_relation_get_of_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Widget")
    fake.getOfClass.return_value = klass
    relation = RPRelation(fake)

    result = relation.get_of_class()

    fake.getOfClass.assert_called_once_with()
    assert result.get_name() == "Widget"


def test_relation_get_other_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Other")
    fake.getOtherClass.return_value = klass
    relation = RPRelation(fake)

    result = relation.get_other_class()

    fake.getOtherClass.assert_called_once_with()
    assert result.get_name() == "Other"


def test_relation_get_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getQualifier="key")
    relation = RPRelation(fake)

    assert relation.get_qualifier() == "key"


def test_relation_get_qualifiers_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Key")
    fake = make_fake_element("Relation")
    fake.getQualifiers.return_value = make_fake_collection([inner])
    relation = RPRelation(fake)

    result = relation.get_qualifiers()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_relation_get_qualifier_type_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="KeyType")
    fake.getQualifierType.return_value = klass
    relation = RPRelation(fake)

    result = relation.get_qualifier_type()

    fake.getQualifierType.assert_called_once_with()
    assert result.get_name() == "KeyType"


def test_relation_get_relation_label_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationLabel="owns")
    relation = RPRelation(fake)

    assert relation.get_relation_label() == "owns"


def test_relation_get_relation_link_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationLinkName="Ownership")
    relation = RPRelation(fake)

    assert relation.get_relation_link_name() == "Ownership"


def test_relation_get_relation_role_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationRoleName="owner")
    relation = RPRelation(fake)

    assert relation.get_relation_role_name() == "owner"


def test_relation_get_relation_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationType="Association")
    relation = RPRelation(fake)

    assert relation.get_relation_type() == "Association"


def test_relation_get_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getVisibility="public")
    relation = RPRelation(fake)

    assert relation.get_visibility() == "public"


def test_relation_is_typeless_object_delegates_to_com() -> None:
    fake = make_fake_element("Relation", isTypelessObject=1)
    relation = RPRelation(fake)

    assert relation.is_typeless_object() is True


def test_relation_make_unidirect_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.make_unidirect()

    fake.makeUnidirect.assert_called_once_with()


def test_relation_remove_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    qualifier = make_fake_element("Class", getName="Key")
    relation = RPRelation(fake)

    relation.remove_qualifier(AbstractRPModelElement.wrap(qualifier))

    fake.removeQualifier.assert_called_once_with(qualifier)


def test_relation_set_inverse_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_inverse("owner", "Association")

    fake.setInverse.assert_called_once_with("owner", "Association")


def test_relation_set_is_navigable_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_is_navigable(True)

    fake.setIsNavigable.assert_called_once_with(1)


def test_relation_set_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_multiplicity("0..*")

    fake.setMultiplicity.assert_called_once_with("0..*")


def test_relation_set_of_class_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="Widget")
    relation = RPRelation(fake)

    relation.set_of_class(RPClassifier(klass_fake))

    fake.setOfClass.assert_called_once_with(klass_fake)


def test_relation_set_other_class_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="Other")
    relation = RPRelation(fake)

    relation.set_other_class(RPClassifier(klass_fake))

    fake.setOtherClass.assert_called_once_with(klass_fake)


def test_relation_set_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_qualifier("key")

    fake.setQualifier.assert_called_once_with("key")


def test_relation_set_qualifier_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="KeyType")
    relation = RPRelation(fake)

    relation.set_qualifier_type(AbstractRPModelElement.wrap(klass_fake))

    fake.setQualifierType.assert_called_once_with(klass_fake)


def test_relation_set_relation_label_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_relation_label("owns")

    fake.setRelationLabel.assert_called_once_with("owns")


def test_relation_set_relation_link_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_relation_link_name("Ownership")

    fake.setRelationLinkName.assert_called_once_with("Ownership")


def test_relation_set_relation_role_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_relation_role_name("owner")

    fake.setRelationRoleName.assert_called_once_with("owner")


def test_relation_set_relation_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.set_relation_type("Association")

    fake.setRelationType.assert_called_once_with("Association")
