"""Relation-family wrappers: mirrors IRPRelation and IRPInstance from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any, cast

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)
from rhapsody_cli.models.elements.classifiers import RPClassifier


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
        call_com(lambda: self._com.addQualifier(p_val._com))

    def getAssociationClass(self) -> Any:
        """Returns the association class linked to this relation, if any.

        Returns:
            The wrapped ``IRPAssociationClass``, or an empty wrapper if none exists.
        """
        return wrap(call_com(lambda: self._com.getAssociationClass()))

    def getInverse(self) -> RPRelation:
        """Gets the inverse relation for this (bidirectional) relation.

        Returns:
            The wrapped ``IRPRelation`` representing the inverse direction.
        """
        return cast(RPRelation, wrap(call_com(lambda: self._com.getInverse())))

    def getIsNavigable(self) -> bool:
        """Checks whether the relation is navigable.

        Returns:
            ``True`` if the relation is navigable, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsNavigable()))

    def getIsSymmetric(self) -> bool:
        """Checks whether the relation is symmetric.

        Returns:
            ``True`` if the relation is symmetric, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsSymmetric()))

    def getMultiplicity(self) -> str:
        """Gets the multiplicity of the relation.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).
        """
        return call_com(lambda: str(self._com.getMultiplicity()))

    def getObjectAsObjectType(self) -> Any:
        """Gets the object's class, treated as the object's type.

        Returns:
            The wrapped ``IRPClass``.
        """
        return wrap(call_com(lambda: self._com.getObjectAsObjectType()))

    def getOfClass(self) -> Any:
        """Gets the classifier that owns this relation.

        Returns:
            The wrapped ``IRPClassifier``.
        """
        return wrap(call_com(lambda: self._com.getOfClass()))

    def getOtherClass(self) -> Any:
        """Gets the class that this class is related to via this relation.

        Returns:
            The wrapped ``IRPClassifier`` on the other end of the relation.
        """
        return wrap(call_com(lambda: self._com.getOtherClass()))

    def getQualifier(self) -> str:
        """Gets the qualifier text for the association.

        Returns:
            The qualifier string.
        """
        return call_com(lambda: str(self._com.getQualifier()))

    def getQualifiers(self) -> RPCollection:
        """Gets the collection of qualifier model elements for the association.

        Returns:
            An ``RPCollection`` of qualifier model elements.
        """
        return RPCollection(call_com(lambda: self._com.getQualifiers()))

    def getQualifierType(self) -> Any:
        """For associations that use qualifiers, returns the type of the qualifier.

        Returns:
            The wrapped ``IRPClassifier`` used as the qualifier's type.
        """
        return wrap(call_com(lambda: self._com.getQualifierType()))

    def getRelationLabel(self) -> str:
        """Gets the label of the relation.

        Returns:
            The relation label string.
        """
        return call_com(lambda: str(self._com.getRelationLabel()))

    def getRelationLinkName(self) -> str:
        """Gets the link name of the relation.

        Returns:
            The relation link name string.
        """
        return call_com(lambda: str(self._com.getRelationLinkName()))

    def getRelationRoleName(self) -> str:
        """Gets the role name of the relation.

        Returns:
            The relation role name string.
        """
        return call_com(lambda: str(self._com.getRelationRoleName()))

    def getRelationType(self) -> str:
        """Gets the type of the relation.

        Returns:
            The relation type string (e.g. ``"Association"``).
        """
        return call_com(lambda: str(self._com.getRelationType()))

    def getVisibility(self) -> str:
        """Gets the visibility of the relation.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).
        """
        return call_com(lambda: str(self._com.getVisibility()))

    def isTypelessObject(self) -> bool:
        """Checks whether the object at the other end of the relation has no type.

        Returns:
            ``True`` if the related object is typeless, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.isTypelessObject()))

    def makeUnidirect(self) -> None:
        """Makes the relation unidirectional."""
        call_com(lambda: self._com.makeUnidirect())

    def removeQualifier(self, p_val: RPModelElement) -> None:
        """Removes a qualifier from the association.

        Args:
            p_val: The model element to remove from the qualifiers.
        """
        call_com(lambda: self._com.removeQualifier(p_val._com))

    def setInverse(self, role_name: str, link_type: str) -> None:
        """Sets the inverse role name and link type for the relation.

        Args:
            role_name: The role name to use for the inverse relation.
            link_type: The link type to use for the inverse relation.
        """
        call_com(lambda: self._com.setInverse(role_name, link_type))

    def setIsNavigable(self, is_navigable: bool) -> None:
        """Sets whether the relation is navigable.

        Args:
            is_navigable: ``True`` to make the relation navigable, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsNavigable(1 if is_navigable else 0))

    def setMultiplicity(self, multiplicity: str) -> None:
        """Sets the multiplicity of the relation.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).
        """
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def setOfClass(self, of_class: RPClassifier) -> None:
        """Sets the classifier that owns this relation.

        Args:
            of_class: The classifier to set as the owner of this relation.
        """
        call_com(lambda: self._com.setOfClass(of_class._com))

    def setOtherClass(self, other_class: RPClassifier) -> None:
        """Sets the class that this class is related to via this relation.

        Args:
            other_class: The classifier to set on the other end of the relation.
        """
        call_com(lambda: self._com.setOtherClass(other_class._com))

    def setQualifier(self, qualifier: str) -> None:
        """Sets the qualifier text for the association.

        Args:
            qualifier: The qualifier string to set.
        """
        call_com(lambda: self._com.setQualifier(qualifier))

    def setQualifierType(self, p_val: RPModelElement) -> None:
        """Sets the type to use for the qualifier for the association.

        Args:
            p_val: The classifier to use as the qualifier's type.
        """
        call_com(lambda: self._com.setQualifierType(p_val._com))

    def setRelationLabel(self, relation_label: str) -> None:
        """Sets the label of the relation.

        Args:
            relation_label: The label string to set.
        """
        call_com(lambda: self._com.setRelationLabel(relation_label))

    def setRelationLinkName(self, relation_link_name: str) -> None:
        """Sets the link name of the relation.

        Args:
            relation_link_name: The link name string to set.
        """
        call_com(lambda: self._com.setRelationLinkName(relation_link_name))

    def setRelationRoleName(self, relation_role_name: str) -> None:
        """Sets the role name of the relation.

        Args:
            relation_role_name: The role name string to set.
        """
        call_com(lambda: self._com.setRelationRoleName(relation_role_name))

    def setRelationType(self, relation_type: str) -> None:
        """Sets the type of the relation.

        Args:
            relation_type: The relation type string to set (e.g. ``"Association"``).
        """
        call_com(lambda: self._com.setRelationType(relation_type))


class RPInstance(RPRelation):
    """Wraps ``IRPInstance``."""

    def getAllNestedElements(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
