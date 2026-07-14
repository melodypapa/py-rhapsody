"""Variable-family wrappers: mirrors IRPVariable and IRPAttribute from
com.telelogic.rhapsody.core.
"""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    RPCollection,
    RPModelElement,
    RPUnit,
)
from rhapsody_cli.models.elements.classifiers import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.values.model_values import (
        RPInstanceValue,
        RPLiteralSpecification,
    )


class RPVariable(RPUnit):
    """Wraps ``IRPVariable``: the base interface for typed elements (such as
    attributes and parameters) that carry a type and default value.
    """

    # IRPVariable method parity checklist:
    # [x] add_element_default_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_string_default_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_declaration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_default_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_type  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_value_specifications  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_declaration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_default_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_type  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_type_declaration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPVariable methods.

    def add_element_default_value(self, new_default_val: RPModelElement) -> "RPInstanceValue":
        """For tags with multiplicity greater than 1, adds a model element as an additional value.

        Args:
            new_default_val: The model element to add as an additional default value.

        Returns:
            The wrapped ``IRPInstanceValue`` created for the new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::addElementDefaultValue(com.telelogic.rhapsody.core.IRPModelElement newDefaultVal)
        """
        return cast("RPInstanceValue", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addElementDefaultValue(new_default_val._com))))

    def add_string_default_value(self, new_default_val: str) -> "RPLiteralSpecification":
        """For tags with multiplicity greater than 1, adds a string as an additional value.

        Args:
            new_default_val: The string to add as an additional default value.

        Returns:
            The wrapped ``IRPLiteralSpecification`` created for the new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::addStringDefaultValue(java.lang.String newDefaultVal)
        """
        return cast("RPLiteralSpecification", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStringDefaultValue(new_default_val))))

    def get_declaration(self) -> str:
        """Returns the type declaration if an on-the-fly type was used for the element.

        Returns:
            The on-the-fly type declaration, or an existing type's info if one was used.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getDeclaration()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDeclaration", "declaration"))

    def get_default_value(self) -> str:
        """Returns the default value that was set for the variable.

        Returns:
            The default value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getDefaultValue()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDefaultValue", "defaultValue"))

    def get_type(self) -> "RPClassifier":
        """Returns the type of the variable.

        Returns:
            The wrapped ``IRPClassifier`` that is the type of the variable.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getType", "type")))

    def get_value_specifications(self) -> RPCollection:
        """Returns the initial values declared for elements with multiplicity greater than one.

        Returns:
            An ``RPCollection`` of the declared initial value specifications.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::getValueSpecifications()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getValueSpecifications", "valueSpecifications"))

    def set_declaration(self, declaration: str) -> None:
        """Specifies an on-the-fly declaration for the type of the element.

        Args:
            declaration: The on-the-fly type declaration to use instead of an existing type.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setDeclaration(java.lang.String declaration)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDeclaration", "declaration", declaration)

    def set_default_value(self, default_value: str) -> None:
        """Sets a new default value for the variable.

        Args:
            default_value: The new default value.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setDefaultValue(java.lang.String defaultValue)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDefaultValue", "defaultValue", default_value)

    def set_type(self, type_: RPClassifier) -> None:
        """Sets the type of the variable.

        Args:
            type_: The classifier to use as the variable's type.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setType", "type", type_._com)

    def set_type_declaration(self, new_val: str) -> None:
        """Specifies an on-the-fly type declaration, reusing a matching existing type if found.

        Args:
            new_val: The on-the-fly type declaration.

        Reference:
            com.telelogic.rhapsody.core.IRPVariable::setTypeDeclaration(java.lang.String newVal)
        """
        # TODO: Under Rhapsody2.Application.1 the 'typeDeclaration' property is not settable (or the
        # 'setTypeDeclaration' method is absent), so this silently no-ops. Persist the type declaration
        # via the metatype property system in a future Rhapsody build.
        AbstractRPModelElement._set_method_or_property(self._com, "setTypeDeclaration", "typeDeclaration", new_val)


AbstractRPModelElement.register_wrapper("Variable", RPVariable)


class RPAttribute(RPVariable):
    """Wraps ``IRPAttribute``: represents an attribute in a classifier."""

    # IRPAttribute method parity checklist:
    # [x] getIsConstant  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getIsOrdered  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getIsReference  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_static  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_multiplicity  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_visibility  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setIsConstant  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setIsOrdered  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setIsReference  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_is_static  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_multiplicity  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_visibility  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPAttribute methods.

    def get_is_constant(self) -> int:
        """Checks whether the attribute is defined as constant.

        Returns:
            ``1`` if the attribute is constant, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getIsConstant()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsConstant", "isConstant"))

    def get_is_ordered(self) -> int:
        """Checks whether the attribute is ordered.

        Returns:
            ``1`` if the attribute is ordered, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getIsOrdered()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsOrdered", "isOrdered"))

    def get_is_reference(self) -> int:
        """Checks whether the attribute is a reference.

        Returns:
            ``1`` if the attribute is a reference, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getIsReference()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsReference", "isReference"))

    def set_is_constant(self, is_constant: bool) -> None:
        """Specifies whether the attribute should be defined as constant.

        Args:
            is_constant: ``True`` to mark the attribute constant, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setIsConstant(int isConstant)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsConstant", "isConstant", 1 if is_constant else 0)

    def set_is_ordered(self, is_ordered: bool) -> None:
        """Specifies whether the attribute should be ordered.

        Args:
            is_ordered: ``True`` to mark the attribute ordered, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setIsOrdered(int isOrdered)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsOrdered", "isOrdered", 1 if is_ordered else 0)

    def set_is_reference(self, is_reference: bool) -> None:
        """Specifies whether the attribute should be a reference.

        Args:
            is_reference: ``True`` to mark the attribute as a reference, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setIsReference(int isReference)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsReference", "isReference", 1 if is_reference else 0)

    def get_multiplicity(self) -> str:
        """Gets the multiplicity specified for the attribute.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getMultiplicity()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def set_multiplicity(self, multiplicity: str) -> None:
        """Specifies the multiplicity for the attribute.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setMultiplicity(java.lang.String multiplicity)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def get_is_static(self) -> bool:
        """Checks whether the attribute was defined as static.

        Returns:
            ``True`` if the attribute is static, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getIsStatic()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsStatic", "isStatic"))

    def set_is_static(self, is_static: bool) -> None:
        """Specifies whether an attribute should be defined as static.

        Args:
            is_static: ``True`` to mark the attribute static, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::setIsStatic(int isStatic)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsStatic", "isStatic", 1 if is_static else 0)

    def get_visibility(self) -> str:
        """Gets the visibility specified for the attribute.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).

        Reference:
            com.telelogic.rhapsody.core.IRPAttribute::getVisibility()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def set_visibility(self, visibility: str) -> None:
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
    # [x] getBase  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getFromProfile  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getMultiplicity  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTagMetaClass  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getValue  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setMultiplicity  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_tag_context_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test   (inherited from RPModelElement)
    # [x] setTagMetaClass  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setValue  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPTag methods.

    def get_base(self) -> RPModelElement:
        """Returns the base element for the tag.

        Returns:
            The wrapped ``IRPModelElement`` that is the base of the tag.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::getBase()
        """
        return cast(RPModelElement, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getBase", "base")))

    def get_from_profile(self) -> str:
        """Returns the profile from which the tag originates.

        Returns:
            The profile name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::getFromProfile()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getFromProfile", "fromProfile"))

    def get_multiplicity(self) -> str:
        """Gets the multiplicity specified for the tag.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPTag::getMultiplicity()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicity", "multiplicity"))

    def get_tag_meta_class(self) -> str:
        """Returns the meta class of the tag.

        Returns:
            The meta class name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::getTagMetaClass()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getTagMetaClass", "tagMetaClass"))

    def get_value(self) -> str:
        """Returns the value of the tag.

        Returns:
            The tag value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::getValue()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getValue", "value"))

    def set_multiplicity(self, multiplicity: str) -> None:
        """Specifies the multiplicity for the tag.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).

        Reference:
            com.telelogic.rhapsody.core.IRPTag::setMultiplicity(java.lang.String multiplicity)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMultiplicity", "multiplicity", multiplicity)

    def set_tag_meta_class(self, tag_meta_class: str) -> None:
        """Sets the meta class of the tag.

        Args:
            tag_meta_class: The meta class name to set.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::setTagMetaClass(java.lang.String tagMetaClass)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setTagMetaClass", "tagMetaClass", tag_meta_class)

    def set_value(self, value: str) -> None:
        """Sets the value of the tag.

        Args:
            value: The value to set for the tag.

        Reference:
            com.telelogic.rhapsody.core.IRPTag::setValue(java.lang.String value)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setValue", "value", value)


AbstractRPModelElement.register_wrapper("Tag", RPTag)


class RPArgument(RPVariable):
    """Wraps ``IRPArgument``: an argument/parameter of an operation."""

    # IRPArgument method parity checklist:
    # [x] get_argument_direction  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_argument_direction  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPVariable / IRPUnit / IRPModelElement methods (covered by RPVariable / RPUnit / RPModelElement checklists)
    # No deprecated IRPArgument methods.

    def get_argument_direction(self) -> str:
        """Returns the direction of the argument (e.g. ``"in"``, ``"out"``, ``"inout"``).

        Returns:
            The argument direction as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPArgument::getArgumentDirection()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getArgumentDirection", "argumentDirection"))

    def set_argument_direction(self, argument_direction: str) -> None:
        """Sets the direction of the argument.

        Args:
            argument_direction: The direction to set (e.g. ``"in"``, ``"out"``, ``"inout"``).

        Reference:
            com.telelogic.rhapsody.core.IRPArgument::setArgumentDirection(java.lang.String argumentDirection)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setArgumentDirection", "argumentDirection", argument_direction)


AbstractRPModelElement.register_wrapper("Argument", RPArgument)
