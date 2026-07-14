"""Wraps ``com.telelogic.rhapsody.core.IRPRelation``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_association_class import RPAssociationClass
    from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPRelation(RPUnit):
    """Wraps ``IRPRelation``: the base interface for relationships between
    classifiers (such as associations, and the instance links derived from
    them).
    """

    # IRPRelation method parity checklist:
    # [x] add_qualifier              [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_association_class       [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_inverse                [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_is_navigable            [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_is_symmetric            [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_multiplicity           [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_object_as_object_type     [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_of_class                [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_other_class             [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_qualifier              [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_qualifiers             [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_qualifier_type          [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_relation_label          [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_relation_link_name       [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_relation_role_name       [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_relation_type           [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_visibility             [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] is_typeless_object          [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] make_unidirect             [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] remove_qualifier           [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_inverse                [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_is_navigable            [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_multiplicity           [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_of_class                [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_other_class             [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_qualifier              [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_qualifier_type          [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_relation_label          [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_relation_link_name       [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_relation_role_name       [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_relation_type           [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # No deprecated methods in IRPRelation. All 31 methods at full parity.

    def add_qualifier(self, p_val: RPModelElement) -> None:
        """Adds a qualifier to the association.

        Args:
            p_val: The model element to add as a qualifier.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::addQualifier(com.telelogic.rhapsody.core.IRPModelElement pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addQualifier(p_val._com))

    def get_association_class(self) -> "RPAssociationClass":
        """Returns the association class linked to this relation, if any.

        Returns:
            The wrapped ``IRPAssociationClass``, or an empty wrapper if none exists.

        Raises:
            RhapsodyRuntimeException: if the association class cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getAssociationClass()
        """
        return cast("RPAssociationClass", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getAssociationClass", "associationClass")))

    def get_inverse(self) -> "RPRelation":
        """Gets the inverse relation for this (bidirectional) relation.

        Returns:
            The wrapped ``IRPRelation`` representing the inverse direction.

        Raises:
            RhapsodyRuntimeException: if the inverse relation cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getInverse()
        """
        return cast(RPRelation, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInverse", "inverse")))

    def get_is_navigable(self) -> bool:
        """Checks whether the relation is navigable.

        Returns:
            ``True`` if the relation is navigable, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getIsNavigable()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsNavigable", "isNavigable"))

    def get_is_symmetric(self) -> bool:
        """Checks whether the relation is symmetric.

        Returns:
            ``True`` if the relation is symmetric, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getIsSymmetric()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsSymmetric", "isSymmetric"))

    def get_multiplicity(self) -> str:
        """Gets the multiplicity of the relation.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).

        Raises:
            RhapsodyRuntimeException: if the multiplicity cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getMultiplicity()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def get_object_as_object_type(self) -> "RPClass":
        """Gets the object's class, treated as the object's type.

        Returns:
            The wrapped ``IRPClass``.

        Raises:
            RhapsodyRuntimeException: if the object type cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getObjectAsObjectType()
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getObjectAsObjectType", "objectAsObjectType")))

    def get_of_class(self) -> "RPClassifier":
        """Gets the classifier that owns this relation.

        Returns:
            The wrapped ``IRPClassifier``.

        Raises:
            RhapsodyRuntimeException: if the owner classifier cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getOfClass()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOfClass", "ofClass")))

    def get_other_class(self) -> "RPClassifier":
        """Gets the class that this class is related to via this relation.

        Returns:
            The wrapped ``IRPClassifier`` on the other end of the relation.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getOtherClass()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOtherClass", "otherClass")))

    def get_qualifier(self) -> str:
        """Gets the qualifier text for the association.

        Returns:
            The qualifier string.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifier()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getQualifier", "qualifier"))

    def get_qualifiers(self) -> RPCollection:
        """Gets the collection of qualifier model elements for the association.

        Returns:
            An ``RPCollection`` of qualifier model elements.

        Raises:
            RhapsodyRuntimeException: if the qualifiers cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getQualifiers", "qualifiers"))

    def get_qualifier_type(self) -> "RPClassifier":
        """For associations that use qualifiers, returns the type of the qualifier.

        Returns:
            The wrapped ``IRPClassifier`` used as the qualifier's type.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifierType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getQualifierType", "qualifierType")))

    def get_relation_label(self) -> str:
        """Gets the label of the relation.

        Returns:
            The relation label string.

        Raises:
            RhapsodyRuntimeException: if the relation label cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationLabel()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLabel", "relationLabel"))

    def get_relation_link_name(self) -> str:
        """Gets the link name of the relation.

        Returns:
            The relation link name string.

        Raises:
            RhapsodyRuntimeException: if the relation link name cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationLinkName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLinkName", "relationLinkName"))

    def get_relation_role_name(self) -> str:
        """Gets the role name of the relation.

        Returns:
            The relation role name string.

        Raises:
            RhapsodyRuntimeException: if the relation role name cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationRoleName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationRoleName", "relationRoleName"))

    def get_relation_type(self) -> str:
        """Gets the type of the relation.

        Returns:
            The relation type string (e.g. ``"Association"``).

        Raises:
            RhapsodyRuntimeException: if the relation type cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationType()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationType", "relationType"))

    def get_visibility(self) -> str:
        """Gets the visibility of the relation.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).

        Raises:
            RhapsodyRuntimeException: if the visibility cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getVisibility()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def is_typeless_object(self) -> bool:
        """Checks whether the object at the other end of the relation has no type.

        Returns:
            ``True`` if the related object is typeless, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the typeless state cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::isTypelessObject()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isTypelessObject", "typelessObject"))

    def make_unidirect(self) -> None:
        """Makes the relation unidirectional.

        Raises:
            RhapsodyRuntimeException: if the relation cannot be made unidirectional.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::makeUnidirect()
        """
        AbstractRPModelElement.call_com(lambda: self._com.makeUnidirect())

    def remove_qualifier(self, p_val: RPModelElement) -> None:
        """Removes a qualifier from the association.

        Args:
            p_val: The model element to remove from the qualifiers.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::removeQualifier(com.telelogic.rhapsody.core.IRPModelElement pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeQualifier(p_val._com))

    def set_inverse(self, role_name: str, link_type: str) -> None:
        """Sets the inverse role name and link type for the relation.

        Args:
            role_name: The role name to use for the inverse relation.
            link_type: The link type to use for the inverse relation.

        Raises:
            RhapsodyRuntimeException: if the inverse relation cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setInverse(java.lang.String roleName, java.lang.String linkType)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setInverse(role_name, link_type))

    def set_is_navigable(self, is_navigable: bool) -> None:
        """Sets whether the relation is navigable.

        Args:
            is_navigable: ``True`` to make the relation navigable, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setIsNavigable(int isNavigable)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsNavigable", "isNavigable", 1 if is_navigable else 0)

    def set_multiplicity(self, multiplicity: str) -> None:
        """Sets the multiplicity of the relation.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).

        Raises:
            RhapsodyRuntimeException: if the multiplicity cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setMultiplicity(java.lang.String multiplicity)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def set_of_class(self, of_class: RPClassifier) -> None:
        """Sets the classifier that owns this relation.

        Args:
            of_class: The classifier to set as the owner of this relation.

        Raises:
            RhapsodyRuntimeException: if the owner classifier cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setOfClass(com.telelogic.rhapsody.core.IRPClassifier ofClass)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOfClass", "ofClass", of_class._com)

    def set_other_class(self, other_class: RPClassifier) -> None:
        """Sets the class that this class is related to via this relation.

        Args:
            other_class: The classifier to set on the other end of the relation.

        Raises:
            RhapsodyRuntimeException: if the other class cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setOtherClass(com.telelogic.rhapsody.core.IRPClassifier otherClass)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOtherClass", "otherClass", other_class._com)

    def set_qualifier(self, qualifier: str) -> None:
        """Sets the qualifier text for the association.

        Args:
            qualifier: The qualifier string to set.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setQualifier(java.lang.String qualifier)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifier", "qualifier", qualifier)

    def set_qualifier_type(self, p_val: RPModelElement) -> None:
        """Sets the type to use for the qualifier for the association.

        Args:
            p_val: The classifier to use as the qualifier's type.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setQualifierType(com.telelogic.rhapsody.core.IRPClassifier pVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifierType", "qualifierType", p_val._com)

    def set_relation_label(self, relation_label: str) -> None:
        """Sets the label of the relation.

        Args:
            relation_label: The label string to set.

        Raises:
            RhapsodyRuntimeException: if the relation label cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationLabel(java.lang.String relationLabel)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLabel", "relationLabel", relation_label)

    def set_relation_link_name(self, relation_link_name: str) -> None:
        """Sets the link name of the relation.

        Args:
            relation_link_name: The link name string to set.

        Raises:
            RhapsodyRuntimeException: if the relation link name cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationLinkName(java.lang.String relationLinkName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLinkName", "relationLinkName", relation_link_name)

    def set_relation_role_name(self, relation_role_name: str) -> None:
        """Sets the role name of the relation.

        Args:
            relation_role_name: The role name string to set.

        Raises:
            RhapsodyRuntimeException: if the relation role name cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationRoleName(java.lang.String relationRoleName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationRoleName", "relationRoleName", relation_role_name)

    def set_relation_type(self, relation_type: str) -> None:
        """Sets the type of the relation.

        Args:
            relation_type: The relation type string to set (e.g. ``"Association"``).

        Raises:
            RhapsodyRuntimeException: if the relation type cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationType(java.lang.String relationType)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationType", "relationType", relation_type)


AbstractRPModelElement.register_wrapper("Relation", RPRelation)
