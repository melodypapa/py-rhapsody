"""Variable-family wrappers: mirrors IRPVariable and IRPAttribute from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)
from rhapsody_cli.models.elements.classifiers import RPClassifier


class RPVariable(RPUnit):
    """Wraps ``IRPVariable``: the base interface for typed elements (such as
    attributes and parameters) that carry a type and default value.
    """

    def addElementDefaultValue(self, new_default_val: RPModelElement) -> Any:
        """For tags with multiplicity greater than 1, adds a model element as an additional value.

        Args:
            new_default_val: The model element to add as an additional default value.

        Returns:
            The wrapped ``IRPInstanceValue`` created for the new default value.
        """
        return wrap(call_com(lambda: self._com.addElementDefaultValue(new_default_val._com)))

    def addStringDefaultValue(self, new_default_val: str) -> Any:
        """For tags with multiplicity greater than 1, adds a string as an additional value.

        Args:
            new_default_val: The string to add as an additional default value.

        Returns:
            The wrapped ``IRPLiteralSpecification`` created for the new default value.
        """
        return wrap(call_com(lambda: self._com.addStringDefaultValue(new_default_val)))

    def getDeclaration(self) -> str:
        """Returns the type declaration if an on-the-fly type was used for the element.

        Returns:
            The on-the-fly type declaration, or an existing type's info if one was used.
        """
        return call_com(lambda: str(self._com.getDeclaration()))

    def getDefaultValue(self) -> str:
        """Returns the default value that was set for the variable.

        Returns:
            The default value as a string.
        """
        return call_com(lambda: str(self._com.getDefaultValue()))

    def getType(self) -> Any:
        """Returns the type of the variable.

        Returns:
            The wrapped ``IRPClassifier`` that is the type of the variable.
        """
        return wrap(call_com(lambda: self._com.getType()))

    def getValueSpecifications(self) -> RPCollection:
        """Returns the initial values declared for elements with multiplicity greater than one.

        Returns:
            An ``RPCollection`` of the declared initial value specifications.
        """
        return RPCollection(call_com(lambda: self._com.getValueSpecifications()))

    def setDeclaration(self, declaration: str) -> None:
        """Specifies an on-the-fly declaration for the type of the element.

        Args:
            declaration: The on-the-fly type declaration to use instead of an existing type.
        """
        call_com(lambda: self._com.setDeclaration(declaration))

    def setDefaultValue(self, default_value: str) -> None:
        """Sets a new default value for the variable.

        Args:
            default_value: The new default value.
        """
        call_com(lambda: self._com.setDefaultValue(default_value))

    def setType(self, type_: RPClassifier) -> None:
        """Sets the type of the variable.

        Args:
            type_: The classifier to use as the variable's type.
        """
        call_com(lambda: self._com.setType(type_._com))

    def setTypeDeclaration(self, new_val: str) -> None:
        """Specifies an on-the-fly type declaration, reusing a matching existing type if found.

        Args:
            new_val: The on-the-fly type declaration.
        """
        call_com(lambda: self._com.setTypeDeclaration(new_val))


class RPAttribute(RPVariable):
    """Wraps ``IRPAttribute``: represents an attribute in a classifier."""

    def getMultiplicity(self) -> str:
        """Gets the multiplicity specified for the attribute.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).
        """
        return call_com(lambda: str(self._com.getMultiplicity()))

    def setMultiplicity(self, multiplicity: str) -> None:
        """Specifies the multiplicity for the attribute.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).
        """
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def getIsStatic(self) -> bool:
        """Checks whether the attribute was defined as static.

        Returns:
            ``True`` if the attribute is static, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsStatic()))

    def setIsStatic(self, is_static: bool) -> None:
        """Specifies whether an attribute should be defined as static.

        Args:
            is_static: ``True`` to mark the attribute static, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsStatic(1 if is_static else 0))

    def getVisibility(self) -> str:
        """Gets the visibility specified for the attribute.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).
        """
        return call_com(lambda: str(self._com.getVisibility()))

    def setVisibility(self, visibility: str) -> None:
        """Specifies the visibility of the attribute.

        Args:
            visibility: The visibility string to set (e.g. ``"public"``, ``"private"``).
        """
        call_com(lambda: self._com.setVisibility(visibility))


register_wrapper("Attribute", RPAttribute)
