"""Wraps ``com.telelogic.rhapsody.core.IRPRelation``."""

from typing import Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

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


class RPRelation(RPUnit):
    """Wraps ``IRPRelation``: the base interface for relationships between
    classifiers (such as associations, and the instance links derived from
    them).
    """

    def addQualifier(self, p_val: RPModelElement) -> None:
        """Adds a qualifier to the association.

        Args:
            p_val: The model element to add as a qualifier.
        """
        AbstractRPModelElement.call_com(lambda: self._com.addQualifier(p_val._com))

    def getAssociationClass(self) -> Any:
        """Returns the association class linked to this relation, if any.

        Returns:
            The wrapped ``IRPAssociationClass``, or an empty wrapper if none exists.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getAssociationClass", "associationClass"))

    def getInverse(self) -> "RPRelation":
        """Gets the inverse relation for this (bidirectional) relation.

        Returns:
            The wrapped ``IRPRelation`` representing the inverse direction.
        """
        return cast(RPRelation, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInverse", "inverse")))

    def getIsNavigable(self) -> bool:
        """Checks whether the relation is navigable.

        Returns:
            ``True`` if the relation is navigable, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsNavigable", "isNavigable"))

    def getIsSymmetric(self) -> bool:
        """Checks whether the relation is symmetric.

        Returns:
            ``True`` if the relation is symmetric, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsSymmetric", "isSymmetric"))

    def getMultiplicity(self) -> str:
        """Gets the multiplicity of the relation.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def getObjectAsObjectType(self) -> Any:
        """Gets the object's class, treated as the object's type.

        Returns:
            The wrapped ``IRPClass``.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getObjectAsObjectType", "objectAsObjectType"))

    def getOfClass(self) -> Any:
        """Gets the classifier that owns this relation.

        Returns:
            The wrapped ``IRPClassifier``.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOfClass", "ofClass"))

    def getOtherClass(self) -> Any:
        """Gets the class that this class is related to via this relation.

        Returns:
            The wrapped ``IRPClassifier`` on the other end of the relation.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOtherClass", "otherClass"))

    def getQualifier(self) -> str:
        """Gets the qualifier text for the association.

        Returns:
            The qualifier string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getQualifier", "qualifier"))

    def getQualifiers(self) -> RPCollection:
        """Gets the collection of qualifier model elements for the association.

        Returns:
            An ``RPCollection`` of qualifier model elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getQualifiers", "qualifiers"))

    def getQualifierType(self) -> Any:
        """For associations that use qualifiers, returns the type of the qualifier.

        Returns:
            The wrapped ``IRPClassifier`` used as the qualifier's type.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getQualifierType", "qualifierType"))

    def getRelationLabel(self) -> str:
        """Gets the label of the relation.

        Returns:
            The relation label string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLabel", "relationLabel"))

    def getRelationLinkName(self) -> str:
        """Gets the link name of the relation.

        Returns:
            The relation link name string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationLinkName", "relationLinkName"))

    def getRelationRoleName(self) -> str:
        """Gets the role name of the relation.

        Returns:
            The relation role name string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationRoleName", "relationRoleName"))

    def getRelationType(self) -> str:
        """Gets the type of the relation.

        Returns:
            The relation type string (e.g. ``"Association"``).
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRelationType", "relationType"))

    def getVisibility(self) -> str:
        """Gets the visibility of the relation.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def isTypelessObject(self) -> bool:
        """Checks whether the object at the other end of the relation has no type.

        Returns:
            ``True`` if the related object is typeless, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isTypelessObject", "typelessObject"))

    def makeUnidirect(self) -> None:
        """Makes the relation unidirectional."""
        AbstractRPModelElement.call_com(lambda: self._com.makeUnidirect())

    def removeQualifier(self, p_val: RPModelElement) -> None:
        """Removes a qualifier from the association.

        Args:
            p_val: The model element to remove from the qualifiers.
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeQualifier(p_val._com))

    def setInverse(self, role_name: str, link_type: str) -> None:
        """Sets the inverse role name and link type for the relation.

        Args:
            role_name: The role name to use for the inverse relation.
            link_type: The link type to use for the inverse relation.
        """
        AbstractRPModelElement.call_com(lambda: self._com.setInverse(role_name, link_type))

    def setIsNavigable(self, is_navigable: bool) -> None:
        """Sets whether the relation is navigable.

        Args:
            is_navigable: ``True`` to make the relation navigable, ``False`` otherwise.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsNavigable", "isNavigable", 1 if is_navigable else 0)

    def setMultiplicity(self, multiplicity: str) -> None:
        """Sets the multiplicity of the relation.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def setOfClass(self, of_class: RPClassifier) -> None:
        """Sets the classifier that owns this relation.

        Args:
            of_class: The classifier to set as the owner of this relation.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOfClass", "ofClass", of_class._com)

    def setOtherClass(self, other_class: RPClassifier) -> None:
        """Sets the class that this class is related to via this relation.

        Args:
            other_class: The classifier to set on the other end of the relation.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOtherClass", "otherClass", other_class._com)

    def setQualifier(self, qualifier: str) -> None:
        """Sets the qualifier text for the association.

        Args:
            qualifier: The qualifier string to set.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifier", "qualifier", qualifier)

    def setQualifierType(self, p_val: RPModelElement) -> None:
        """Sets the type to use for the qualifier for the association.

        Args:
            p_val: The classifier to use as the qualifier's type.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setQualifierType", "qualifierType", p_val._com)

    def setRelationLabel(self, relation_label: str) -> None:
        """Sets the label of the relation.

        Args:
            relation_label: The label string to set.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLabel", "relationLabel", relation_label)

    def setRelationLinkName(self, relation_link_name: str) -> None:
        """Sets the link name of the relation.

        Args:
            relation_link_name: The link name string to set.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationLinkName", "relationLinkName", relation_link_name)

    def setRelationRoleName(self, relation_role_name: str) -> None:
        """Sets the role name of the relation.

        Args:
            relation_role_name: The role name string to set.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationRoleName", "relationRoleName", relation_role_name)

    def setRelationType(self, relation_type: str) -> None:
        """Sets the type of the relation.

        Args:
            relation_type: The relation type string to set (e.g. ``"Association"``).
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRelationType", "relationType", relation_type)
