"""Variable-family wrappers: mirrors IRPVariable and IRPAttribute from
com.telelogic.rhapsody.core.
"""

from typing import Any

from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    RPCollection,
    RPModelElement,
    RPUnit,
)
from rhapsody_cli.models.elements.classifiers import RPClassifier


class RPVariable(RPUnit):
    """Wraps ``IRPVariable``: the base interface for typed elements (such as
    attributes and parameters) that carry a type and default value.
    """

    # IRPVariable method parity checklist:
    # [x] addElementDefaultValue  [x] impl  [x] docstring  [x] test
    # [x] addStringDefaultValue  [x] impl  [x] docstring  [x] test
    # [x] getDeclaration  [x] impl  [x] docstring  [x] test
    # [x] getDefaultValue  [x] impl  [x] docstring  [x] test
    # [x] getType  [x] impl  [x] docstring  [x] test
    # [x] getValueSpecifications  [x] impl  [x] docstring  [x] test
    # [x] setDeclaration  [x] impl  [x] docstring  [x] test
    # [x] setDefaultValue  [x] impl  [x] docstring  [x] test
    # [x] setType  [x] impl  [x] docstring  [x] test
    # [x] setTypeDeclaration  [x] impl  [x] docstring  [x] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPVariable methods.

    def addElementDefaultValue(self, new_default_val: RPModelElement) -> Any:
        """For tags with multiplicity greater than 1, adds a model element as an additional value.

        Args:
            new_default_val: The model element to add as an additional default value.

        Returns:
            The wrapped ``IRPInstanceValue`` created for the new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::addElementDefaultValue(com.telelogic.rhapsody.core.IRPModelElement newDefaultVal)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addElementDefaultValue(new_default_val._com)))

    def addStringDefaultValue(self, new_default_val: str) -> Any:
        """For tags with multiplicity greater than 1, adds a string as an additional value.

        Args:
            new_default_val: The string to add as an additional default value.

        Returns:
            The wrapped ``IRPLiteralSpecification`` created for the new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::addStringDefaultValue(java.lang.String newDefaultVal)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStringDefaultValue(new_default_val)))

    def getDeclaration(self) -> str:
        """Returns the type declaration if an on-the-fly type was used for the element.

        Returns:
            The on-the-fly type declaration, or an existing type's info if one was used.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getDeclaration()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDeclaration", "declaration"))

    def getDefaultValue(self) -> str:
        """Returns the default value that was set for the variable.

        Returns:
            The default value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getDefaultValue()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDefaultValue", "defaultValue"))

    def getType(self) -> Any:
        """Returns the type of the variable.

        Returns:
            The wrapped ``IRPClassifier`` that is the type of the variable.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getType()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getType", "type"))

    def getValueSpecifications(self) -> RPCollection:
        """Returns the initial values declared for elements with multiplicity greater than one.

        Returns:
            An ``RPCollection`` of the declared initial value specifications.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getValueSpecifications()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getValueSpecifications", "valueSpecifications"))

    def setDeclaration(self, declaration: str) -> None:
        """Specifies an on-the-fly declaration for the type of the element.

        Args:
            declaration: The on-the-fly type declaration to use instead of an existing type.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setDeclaration(java.lang.String declaration)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDeclaration", "declaration", declaration)

    def setDefaultValue(self, default_value: str) -> None:
        """Sets a new default value for the variable.

        Args:
            default_value: The new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setDefaultValue(java.lang.String defaultValue)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDefaultValue", "defaultValue", default_value)

    def setType(self, type_: RPClassifier) -> None:
        """Sets the type of the variable.

        Args:
            type_: The classifier to use as the variable's type.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setType", "type", type_._com)

    def setTypeDeclaration(self, new_val: str) -> None:
        """Specifies an on-the-fly type declaration, reusing a matching existing type if found.

        Args:
            new_val: The on-the-fly type declaration.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setTypeDeclaration(java.lang.String newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setTypeDeclaration", "typeDeclaration", new_val)


class RPAttribute(RPVariable):
    """Wraps ``IRPAttribute``: represents an attribute in a classifier."""

    # IRPAttribute method parity checklist:
    # [ ] getIsConstant  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsOrdered  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsReference  [ ] impl  [ ] docstring  [ ] test
    # [x] getIsStatic  [x] impl  [x] docstring  [x] test
    # [x] getMultiplicity  [x] impl  [x] docstring  [x] test
    # [x] getVisibility  [x] impl  [x] docstring  [x] test
    # [ ] setIsConstant  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsOrdered  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsReference  [ ] impl  [ ] docstring  [ ] test
    # [x] setIsStatic  [x] impl  [x] docstring  [x] test
    # [x] setMultiplicity  [x] impl  [x] docstring  [x] test
    # [x] setVisibility  [x] impl  [x] docstring  [x] test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPAttribute methods.

    def getMultiplicity(self) -> str:
        """Gets the multiplicity specified for the attribute.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getMultiplicity()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def setMultiplicity(self, multiplicity: str) -> None:
        """Specifies the multiplicity for the attribute.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setMultiplicity(java.lang.String multiplicity)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def getIsStatic(self) -> bool:
        """Checks whether the attribute was defined as static.

        Returns:
            ``True`` if the attribute is static, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getIsStatic()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsStatic", "isStatic"))

    def setIsStatic(self, is_static: bool) -> None:
        """Specifies whether an attribute should be defined as static.

        Args:
            is_static: ``True`` to mark the attribute static, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setIsStatic(int isStatic)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsStatic", "isStatic", 1 if is_static else 0)

    def getVisibility(self) -> str:
        """Gets the visibility specified for the attribute.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getVisibility()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def setVisibility(self, visibility: str) -> None:
        """Specifies the visibility of the attribute.

        Args:
            visibility: The visibility string to set (e.g. ``"public"``, ``"private"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setVisibility(java.lang.String visibility)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setVisibility", "visibility", visibility)


AbstractRPModelElement.register_wrapper("Attribute", RPAttribute)


class RPTag(RPVariable):
    """Wraps ``IRPTag``: a tag that extends ``IRPVariable``."""

    # IRPTag method parity checklist:
    # [ ] getBase  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromProfile  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMultiplicity  [ ] impl  [ ] docstring  [ ] test
    # [ ] getTagMetaClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] getValue  [ ] impl  [ ] docstring  [ ] test
    # [ ] setMultiplicity  [ ] impl  [ ] docstring  [ ] test
    # [x] setTagContextValue  [x] impl  [x] docstring  [x] test   (inherited from RPModelElement)
    # [ ] setTagMetaClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] setValue  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPTag methods.

    pass


AbstractRPModelElement.register_wrapper("Tag", RPTag)


class RPArgument(RPVariable):
    """Wraps ``IRPArgument``: an argument/parameter of an operation."""

    # IRPArgument method parity checklist:
    # [x] getArgumentDirection  [x] impl  [x] docstring  [x] test
    # [x] setArgumentDirection  [x] impl  [x] docstring  [x] test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPArgument methods.

    def getArgumentDirection(self) -> str:
        """Returns the direction of the argument (e.g. ``"in"``, ``"out"``, ``"inout"``).

        Returns:
            The argument direction as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPArgument::getArgumentDirection()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getArgumentDirection", "argumentDirection"))

    def setArgumentDirection(self, argument_direction: str) -> None:
        """Sets the direction of the argument.

        Args:
            argument_direction: The direction to set (e.g. ``"in"``, ``"out"``, ``"inout"``).

        Reference:
            com.telelogic.rhapsody.core.IRPArgument::setArgumentDirection(java.lang.String argumentDirection)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setArgumentDirection", "argumentDirection", argument_direction)


AbstractRPModelElement.register_wrapper("Argument", RPArgument)
