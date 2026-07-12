"""Wraps ``com.telelogic.rhapsody.core.IRPRelation``."""

from typing import Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPRelation(RPUnit):
    """Wraps ``IRPRelation``: the base interface for relationships between
    classifiers (such as associations, and the instance links derived from
    them).
    """

    # IRPRelation method parity checklist:
    # [x] addQualifier              [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getAssociationClass       [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getInverse                [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getIsNavigable            [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getIsSymmetric            [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getMultiplicity           [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getObjectAsObjectType     [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getOfClass                [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getOtherClass             [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getQualifier              [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getQualifiers             [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getQualifierType          [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getRelationLabel          [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getRelationLinkName       [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getRelationRoleName       [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getRelationType           [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getVisibility             [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] isTypelessObject          [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] makeUnidirect             [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] removeQualifier           [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setInverse                [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setIsNavigable            [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setMultiplicity           [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setOfClass                [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setOtherClass             [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setQualifier              [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setQualifierType          [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setRelationLabel          [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setRelationLinkName       [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setRelationRoleName       [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setRelationType           [x] impl  [x] docstring  [x] test   (already implemented)
    # No deprecated methods in IRPRelation. All 31 methods at full parity.

    def addQualifier(self, p_val: RPModelElement) -> None:
        """Adds a qualifier to the association.

        Args:
            p_val: The model element to add as a qualifier.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::addQualifier(com.telelogic.rhapsody.core.IRPModelElement pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addQualifier(p_val._com))

    def getAssociationClass(self) -> Any:
        """Returns the association class linked to this relation, if any.

        Returns:
            The wrapped ``IRPAssociationClass``, or an empty wrapper if none exists.

        Raises:
            RhapsodyRuntimeException: if the association class cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getAssociationClass()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getAssociationClass", "associationClass"))

    def getInverse(self) -> "RPRelation":
        """Gets the inverse relation for this (bidirectional) relation.

        Returns:
            The wrapped ``IRPRelation`` representing the inverse direction.

        Raises:
            RhapsodyRuntimeException: if the inverse relation cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getInverse()
        """
        return cast(RPRelation, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInverse", "inverse")))

    def getIsNavigable(self) -> bool:
        """Checks whether the relation is navigable.

        Returns:
            ``True`` if the relation is navigable, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getIsNavigable()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsNavigable", "isNavigable"))

    def getIsSymmetric(self) -> bool:
        """Checks whether the relation is symmetric.

        Returns:
            ``True`` if the relation is symmetric, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getIsSymmetric()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsSymmetric", "isSymmetric"))

    def getMultiplicity(self) -> str:
        """Gets the multiplicity of the relation.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).

        Raises:
            RhapsodyRuntimeException: if the multiplicity cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getMultiplicity()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def getObjectAsObjectType(self) -> Any:
        """Gets the object's class, treated as the object's type.

        Returns:
            The wrapped ``IRPClass``.

        Raises:
            RhapsodyRuntimeException: if the object type cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getObjectAsObjectType()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getObjectAsObjectType", "objectAsObjectType"))

    def getOfClass(self) -> Any:
        """Gets the classifier that owns this relation.

        Returns:
            The wrapped ``IRPClassifier``.

        Raises:
            RhapsodyRuntimeException: if the owner classifier cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getOfClass()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOfClass", "ofClass"))

    def getOtherClass(self) -> Any:
        """Gets the class that this class is related to via this relation.

        Returns:
            The wrapped ``IRPClassifier`` on the other end of the relation.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getOtherClass()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOtherClass", "otherClass"))

    def getQualifier(self) -> str:
        """Gets the qualifier text for the association.

        Returns:
            The qualifier string.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifier()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getQualifier", "qualifier"))

    def getQualifiers(self) -> RPCollection:
        """Gets the collection of qualifier model elements for the association.

        Returns:
            An ``RPCollection`` of qualifier model elements.

        Raises:
            RhapsodyRuntimeException: if the qualifiers cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifiers()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getQualifiers", "qualifiers"))

    def getQualifierType(self) -> Any:
        """For associations that use qualifiers, returns the type of the qualifier.

        Returns:
            The wrapped ``IRPClassifier`` used as the qualifier's type.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getQualifierType()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getQualifierType", "qualifierType"))

    def getRelationLabel(self) -> str:
        """Gets the label of the relation.

        Returns:
            The relation label string.

        Raises:
            RhapsodyRuntimeException: if the relation label cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationLabel()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLabel", "relationLabel"))

    def getRelationLinkName(self) -> str:
        """Gets the link name of the relation.

        Returns:
            The relation link name string.

        Raises:
            RhapsodyRuntimeException: if the relation link name cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationLinkName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLinkName", "relationLinkName"))

    def getRelationRoleName(self) -> str:
        """Gets the role name of the relation.

        Returns:
            The relation role name string.

        Raises:
            RhapsodyRuntimeException: if the relation role name cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationRoleName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationRoleName", "relationRoleName"))

    def getRelationType(self) -> str:
        """Gets the type of the relation.

        Returns:
            The relation type string (e.g. ``"Association"``).

        Raises:
            RhapsodyRuntimeException: if the relation type cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getRelationType()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationType", "relationType"))

    def getVisibility(self) -> str:
        """Gets the visibility of the relation.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).

        Raises:
            RhapsodyRuntimeException: if the visibility cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::getVisibility()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def isTypelessObject(self) -> bool:
        """Checks whether the object at the other end of the relation has no type.

        Returns:
            ``True`` if the related object is typeless, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the typeless state cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::isTypelessObject()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isTypelessObject", "typelessObject"))

    def makeUnidirect(self) -> None:
        """Makes the relation unidirectional.

        Raises:
            RhapsodyRuntimeException: if the relation cannot be made unidirectional.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::makeUnidirect()
        """
        AbstractRPModelElement.call_com(lambda: self._com.makeUnidirect())

    def removeQualifier(self, p_val: RPModelElement) -> None:
        """Removes a qualifier from the association.

        Args:
            p_val: The model element to remove from the qualifiers.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be removed.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::removeQualifier(com.telelogic.rhapsody.core.IRPModelElement pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeQualifier(p_val._com))

    def setInverse(self, role_name: str, link_type: str) -> None:
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

    def setIsNavigable(self, is_navigable: bool) -> None:
        """Sets whether the relation is navigable.

        Args:
            is_navigable: ``True`` to make the relation navigable, ``False`` otherwise.

        Raises:
            RhapsodyRuntimeException: if the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setIsNavigable(int isNavigable)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsNavigable", "isNavigable", 1 if is_navigable else 0)

    def setMultiplicity(self, multiplicity: str) -> None:
        """Sets the multiplicity of the relation.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).

        Raises:
            RhapsodyRuntimeException: if the multiplicity cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setMultiplicity(java.lang.String multiplicity)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def setOfClass(self, of_class: RPClassifier) -> None:
        """Sets the classifier that owns this relation.

        Args:
            of_class: The classifier to set as the owner of this relation.

        Raises:
            RhapsodyRuntimeException: if the owner classifier cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setOfClass(com.telelogic.rhapsody.core.IRPClassifier ofClass)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOfClass", "ofClass", of_class._com)

    def setOtherClass(self, other_class: RPClassifier) -> None:
        """Sets the class that this class is related to via this relation.

        Args:
            other_class: The classifier to set on the other end of the relation.

        Raises:
            RhapsodyRuntimeException: if the other class cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setOtherClass(com.telelogic.rhapsody.core.IRPClassifier otherClass)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOtherClass", "otherClass", other_class._com)

    def setQualifier(self, qualifier: str) -> None:
        """Sets the qualifier text for the association.

        Args:
            qualifier: The qualifier string to set.

        Raises:
            RhapsodyRuntimeException: if the qualifier cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setQualifier(java.lang.String qualifier)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifier", "qualifier", qualifier)

    def setQualifierType(self, p_val: RPModelElement) -> None:
        """Sets the type to use for the qualifier for the association.

        Args:
            p_val: The classifier to use as the qualifier's type.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setQualifierType(com.telelogic.rhapsody.core.IRPClassifier pVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifierType", "qualifierType", p_val._com)

    def setRelationLabel(self, relation_label: str) -> None:
        """Sets the label of the relation.

        Args:
            relation_label: The label string to set.

        Raises:
            RhapsodyRuntimeException: if the relation label cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationLabel(java.lang.String relationLabel)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLabel", "relationLabel", relation_label)

    def setRelationLinkName(self, relation_link_name: str) -> None:
        """Sets the link name of the relation.

        Args:
            relation_link_name: The link name string to set.

        Raises:
            RhapsodyRuntimeException: if the relation link name cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationLinkName(java.lang.String relationLinkName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLinkName", "relationLinkName", relation_link_name)

    def setRelationRoleName(self, relation_role_name: str) -> None:
        """Sets the role name of the relation.

        Args:
            relation_role_name: The role name string to set.

        Raises:
            RhapsodyRuntimeException: if the relation role name cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationRoleName(java.lang.String relationRoleName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationRoleName", "relationRoleName", relation_role_name)

    def setRelationType(self, relation_type: str) -> None:
        """Sets the type of the relation.

        Args:
            relation_type: The relation type string to set (e.g. ``"Association"``).

        Raises:
            RhapsodyRuntimeException: if the relation type cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPRelation::setRelationType(java.lang.String relationType)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationType", "relationType", relation_type)
