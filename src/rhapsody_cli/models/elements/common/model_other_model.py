"""Other Model model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.relations.model_instance import RPInstance

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.common.model_misc import RPEnumerationLiteral
    from rhapsody_cli.models.elements.containment.model_package import RPPackage
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
    from rhapsody_cli.models.elements.graphics.model_graphics import RPLink
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPClassifierRole(RPModelElement):
    """Wraps ``IRPClassifierRole``: represents lifelines in sequence diagrams and "objects" (lifelines) in communication diagrams."""

    # IRPClassifierRole method parity checklist:
    # [ ] getFormalClassifier          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFormalInstance            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getReferencedSequenceDiagram [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getReferencingClassifierRolesRecursively [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRoleType                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFormalClassifier          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFormalInstance            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setReferencedSequenceDiagram [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPClassifierRole methods.

    def get_formal_classifier(self) -> "RPClassifier":
        """Returns the classifier (for example, class or actor) that the lifeline realizes.

        Returns:
            The classifier that the lifeline realizes.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalClassifier()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFormalClassifier())))

    def get_formal_instance(self) -> "RPInstance":
        """Returns the object that is realized by the lifeline, for cases where a lifeline represents an object and not just a classifier.

        Returns:
            The object that is realized by the lifeline, or null if the lifeline does not realize an object.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalInstance()
        """
        return cast("RPInstance", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFormalInstance())))

    def get_referenced_sequence_diagram(self) -> "RPSequenceDiagram":
        """Returns the sequence diagram referenced by the lifeline.

        Returns:
            The sequence diagram referenced by the lifeline, or null if there is no referenced diagram.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencedSequenceDiagram()
        """
        return cast("RPSequenceDiagram", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getReferencedSequenceDiagram())))

    def get_referencing_classifier_roles_recursively(self) -> "RPCollection":
        """Returns a collection of all the lifelines in referenced sequence diagrams, recursively including all lifelines in the decomposition hierarchy.

        Returns:
            A collection of all the lifelines in referenced sequence diagrams.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencingClassifierRolesRecursively()
        """
        return RPCollection(self.call_com(lambda: self._com.getReferencingClassifierRolesRecursively()))

    def get_role_type(self) -> str:
        """Returns a string representing the type of the classifier role.

        For example, ``CLASS`` for elements of type IRPClass and ``ACTOR`` for
        elements of type IRPActor. For objects, the string returned is ``CLASS``.

        Returns:
            A string representing the type of the classifier role.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getRoleType()
        """
        return str(self._get_method_or_property(self._com, "getRoleType", "roleType"))

    def set_formal_classifier(self, formal_classifier: "RPClassifier") -> None:
        """Sets the specified element as the classifier realized by the lifeline.

        Args:
            formal_classifier: The model element that should be used as the
                classifier realized by the lifeline.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::setFormalClassifier(com.telelogic.rhapsody.core.IRPClassifier formalClassifier)
        """
        self.call_com(lambda: self._com.setFormalClassifier(formal_classifier._com))

    def set_formal_instance(self, formal_instance: "RPInstance") -> None:
        """Sets the specified element as the object realized by the lifeline.

        Args:
            formal_instance: The model element that should be used as the object
                realized by the lifeline.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::setFormalInstance(com.telelogic.rhapsody.core.IRPInstance formalInstance)
        """
        self.call_com(lambda: self._com.setFormalInstance(formal_instance._com))

    def set_referenced_sequence_diagram(self, referenced_sequence_diagram: "RPSequenceDiagram") -> None:
        """Sets the specified diagram to be the sequence diagram referenced by the lifeline.

        Args:
            referenced_sequence_diagram: The diagram that should be used as the
                sequence diagram referenced by the lifeline.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::setReferencedSequenceDiagram(com.telelogic.rhapsody.core.IRPSequenceDiagram referencedSequenceDiagram)
        """
        self.call_com(lambda: self._com.setReferencedSequenceDiagram(referenced_sequence_diagram._com))


class RPSysMLPort(RPInstance):
    """Wraps ``IRPSysMLPort``: represents flowport elements in Rhapsody models."""

    # IRPSysMLPort method parity checklist:
    # [ ] addLink                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsReversed                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPortDirection             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIsReversed                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setPortDirection             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setType                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPInstance methods (covered by RPInstance checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPRelation methods (covered by RPRelation checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPSysMLPort methods.

    def add_link(self, from_part: "RPInstance", to_part: "RPInstance", assoc: "RPRelation", to_port: "RPSysMLPort", new_owner: "RPPackage") -> "RPLink":
        """Creates a link between flowports on two parts.

        Args:
            from_part: The "from" part for the link.
            to_part: The "to" part for the link.
            assoc: Use ``None`` for this argument (it is not relevant for links
                between flowports).
            to_port: The "to" port for the link.
            new_owner: The package that should be the owner of the link created.

        Returns:
            The link that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::addLink(
                com.telelogic.rhapsody.core.IRPInstance fromPart,
                com.telelogic.rhapsody.core.IRPInstance toPart,
                com.telelogic.rhapsody.core.IRPRelation assoc,
                com.telelogic.rhapsody.core.IRPSysMLPort toPort,
                com.telelogic.rhapsody.core.IRPPackage newOwner)
        """
        return cast("RPLink", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addLink(from_part._com, to_part._com, assoc._com, to_port._com, new_owner._com))))

    def get_is_reversed(self) -> int:
        """Checks whether the flowport was specified as conjugated.

        Returns:
            1 if the flowport was specified as conjugated, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getIsReversed()
        """
        return int(self.call_com(lambda: self._com.getIsReversed()))

    def get_port_direction(self) -> str:
        """Returns the direction that was specified for the flowport.

        Returns:
            The direction that was specified for the flowport — one of ``"In"``,
            ``"Out"``, or ``"InOut"``.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getPortDirection()
        """
        return str(self._get_method_or_property(self._com, "getPortDirection", "portDirection"))

    def get_type(self) -> "RPClassifier":
        """Returns the type that was specified for the flowport.

        Returns:
            The type that was specified for the flowport.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getType())))

    def set_is_reversed(self, is_reversed: int) -> None:
        """Specifies whether the flowport should be conjugated.

        Args:
            is_reversed: Use 1 to specify that the flowport should be conjugated,
                0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::setIsReversed(int isReversed)
        """
        self._set_method_or_property(self._com, "setIsReversed", "isReversed", is_reversed)

    def set_port_direction(self, port_direction: str) -> None:
        """Sets the direction of the flowport.

        Args:
            port_direction: The direction to use for the flowport. The valid values
                are ``"In"``, ``"Out"``, and ``"InOut"``.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::setPortDirection(java.lang.String portDirection)
        """
        self._set_method_or_property(self._com, "setPortDirection", "portDirection", port_direction)

    def set_type(self, type_: "RPClassifier") -> None:
        """Sets the type for the flowport.

        Args:
            type_: The type to use for the flowport.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        self.call_com(lambda: self._com.setType(type_._com))


class RPType(RPClassifier):
    """Wraps ``IRPType``."""

    # IRPType method parity checklist:
    # [ ] addEnumerationLiteral        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] deleteEnumerationLiteral     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getDeclaration               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getEnumerationLiterals       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsPredefined              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsTypedef                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsTypedefConstant         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsTypedefOrdered          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsTypedefReference        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getKind                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getTypedefBaseType           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getTypedefMultiplicity       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isArray                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isEnum                       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isEqualTo                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isImplicit                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isKindEnumeration            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isKindLanguage               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isKindStruct                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isKindTypedef                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isKindUnion                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isPointer                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isPointerToPointer           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isReference                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isReferenceToPointer         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isStruct                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isTemplate                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isUnion                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setDeclaration               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIsTypedefConstant         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIsTypedefOrdered          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIsTypedefReference        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setKind                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setTypedefBaseType           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setTypedefMultiplicity       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPType methods.

    def add_enumeration_literal(self, name: str) -> "RPEnumerationLiteral":
        """Adds an enumeration literal with the specified name to this type.

        Args:
            name: The name for the new enumeration literal.

        Returns:
            The enumeration literal that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::addEnumerationLiteral(java.lang.String name)
        """
        return cast("RPEnumerationLiteral", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addEnumerationLiteral(name))))

    def delete_enumeration_literal(self, literal: "RPEnumerationLiteral") -> None:
        """Deletes the specified enumeration literal from this type.

        Args:
            literal: The enumeration literal to delete.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::deleteEnumerationLiteral(com.telelogic.rhapsody.core.IRPEnumerationLiteral literal)
        """
        self.call_com(lambda: self._com.deleteEnumerationLiteral(literal._com))

    def get_declaration(self) -> str:
        """Returns the declaration of the type.

        Returns:
            The declaration of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getDeclaration()
        """
        return str(self._get_method_or_property(self._com, "getDeclaration", "declaration"))

    def get_enumeration_literals(self) -> "RPCollection":
        """Returns the enumeration literals of the type.

        Returns:
            A collection of the type's enumeration literals.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getEnumerationLiterals()
        """
        return RPCollection(self.call_com(lambda: self._com.getEnumerationLiterals()))

    def get_is_predefined(self) -> int:
        """Returns whether the type is predefined.

        Returns:
            1 if the type is predefined, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsPredefined()
        """
        return int(self.call_com(lambda: self._com.getIsPredefined()))

    def get_is_typedef(self) -> int:
        """Returns whether the type is a typedef.

        Returns:
            1 if the type is a typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedef()
        """
        return int(self.call_com(lambda: self._com.getIsTypedef()))

    def get_is_typedef_constant(self) -> int:
        """Returns whether the typedef is a constant.

        Returns:
            1 if the typedef is a constant, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefConstant()
        """
        return int(self.call_com(lambda: self._com.getIsTypedefConstant()))

    def get_is_typedef_ordered(self) -> int:
        """Returns whether the typedef is ordered.

        Returns:
            1 if the typedef is ordered, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefOrdered()
        """
        return int(self.call_com(lambda: self._com.getIsTypedefOrdered()))

    def get_is_typedef_reference(self) -> int:
        """Returns whether the typedef is a reference.

        Returns:
            1 if the typedef is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefReference()
        """
        return int(self.call_com(lambda: self._com.getIsTypedefReference()))

    def get_kind(self) -> str:
        """Returns the kind of the type.

        Returns:
            The kind of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getKind()
        """
        return str(self._get_method_or_property(self._com, "getKind", "kind"))

    def get_typedef_base_type(self) -> "RPClassifier":
        """Returns the base type of the typedef.

        Returns:
            The base type of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefBaseType()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getTypedefBaseType())))

    def get_typedef_multiplicity(self) -> str:
        """Returns the multiplicity of the typedef.

        Returns:
            The multiplicity of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefMultiplicity()
        """
        return str(self._get_method_or_property(self._com, "getTypedefMultiplicity", "typedefMultiplicity"))

    def is_array(self) -> int:
        """Checks whether the type is an array.

        Returns:
            1 if the type is an array, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isArray()
        """
        return int(self.call_com(lambda: self._com.isArray()))

    def is_enum(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually an enum.

        Returns:
            1 if the type is an enum, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEnum()
        """
        return int(self.call_com(lambda: self._com.isEnum()))

    def is_equal_to(self) -> int:
        """Checks whether the type is an equal-to type.

        Returns:
            1 if the type is an equal-to type, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEqualTo()
        """
        return int(self.call_com(lambda: self._com.isEqualTo()))

    def is_implicit(self) -> int:
        """Checks whether the type is implicit.

        Returns:
            1 if the type is implicit, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isImplicit()
        """
        return int(self.call_com(lambda: self._com.isImplicit()))

    def is_kind_enumeration(self) -> int:
        """Checks whether the kind of the type is Enumeration.

        Returns:
            1 if the kind of the type is Enumeration, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindEnumeration()
        """
        return int(self.call_com(lambda: self._com.isKindEnumeration()))

    def is_kind_language(self) -> int:
        """Checks whether the kind of the type was set to Language.

        Returns:
            1 if the kind of the type is Language, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindLanguage()
        """
        return int(self.call_com(lambda: self._com.isKindLanguage()))

    def is_kind_struct(self) -> int:
        """Checks whether the kind of the type is Structure.

        Returns:
            1 if the kind of the type is Structure, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindStruct()
        """
        return int(self.call_com(lambda: self._com.isKindStruct()))

    def is_kind_typedef(self) -> int:
        """Checks whether the kind of the type is Typedef.

        Returns:
            1 if the kind of the type is Typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindTypedef()
        """
        return int(self.call_com(lambda: self._com.isKindTypedef()))

    def is_kind_union(self) -> int:
        """Checks whether the kind of the type is Union.

        Returns:
            1 if the kind of the type is Union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindUnion()
        """
        return int(self.call_com(lambda: self._com.isKindUnion()))

    def is_pointer(self) -> int:
        """Checks whether the type is a pointer.

        Returns:
            1 if the type is a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointer()
        """
        return int(self.call_com(lambda: self._com.isPointer()))

    def is_pointer_to_pointer(self) -> int:
        """Checks whether the type is a pointer to a pointer.

        Returns:
            1 if the type is a pointer to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointerToPointer()
        """
        return int(self.call_com(lambda: self._com.isPointerToPointer()))

    def is_reference(self) -> int:
        """Checks whether the type is a reference.

        Returns:
            1 if the type is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReference()
        """
        return int(self.call_com(lambda: self._com.isReference()))

    def is_reference_to_pointer(self) -> int:
        """Checks whether the type is a reference to a pointer.

        Returns:
            1 if the type is a reference to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReferenceToPointer()
        """
        return int(self.call_com(lambda: self._com.isReferenceToPointer()))

    def is_struct(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a struct.

        Returns:
            1 if the type is a struct, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isStruct()
        """
        return int(self.call_com(lambda: self._com.isStruct()))

    def is_template(self) -> int:
        """Checks whether the type is a template.

        Returns:
            1 if the type is a template, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isTemplate()
        """
        return int(self.call_com(lambda: self._com.isTemplate()))

    def is_union(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a union.

        Returns:
            1 if the type is a union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isUnion()
        """
        return int(self.call_com(lambda: self._com.isUnion()))

    def set_declaration(self, declaration: str) -> None:
        """Sets the declaration of the type.

        Args:
            declaration: The declaration to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setDeclaration(java.lang.String declaration)
        """
        self._set_method_or_property(self._com, "setDeclaration", "declaration", declaration)

    def set_is_typedef_constant(self, is_typedef_constant: int) -> None:
        """Sets whether the typedef is a constant.

        Args:
            is_typedef_constant: Use 1 to specify that the typedef is a constant,
                0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setIsTypedefConstant(int isTypedefConstant)
        """
        self._set_method_or_property(self._com, "setIsTypedefConstant", "isTypedefConstant", is_typedef_constant)

    def set_is_typedef_ordered(self, is_typedef_ordered: int) -> None:
        """Sets whether the typedef is ordered.

        Args:
            is_typedef_ordered: Use 1 to specify that the typedef is ordered,
                0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setIsTypedefOrdered(int isTypedefOrdered)
        """
        self._set_method_or_property(self._com, "setIsTypedefOrdered", "isTypedefOrdered", is_typedef_ordered)

    def set_is_typedef_reference(self, is_typedef_reference: int) -> None:
        """Sets whether the typedef is a reference.

        Args:
            is_typedef_reference: Use 1 to specify that the typedef is a reference,
                0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setIsTypedefReference(int isTypedefReference)
        """
        self._set_method_or_property(self._com, "setIsTypedefReference", "isTypedefReference", is_typedef_reference)

    def set_kind(self, kind: str) -> None:
        """Sets the kind of the type.

        Args:
            kind: The kind to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setKind(java.lang.String kind)
        """
        self._set_method_or_property(self._com, "setKind", "kind", kind)

    def set_typedef_base_type(self, typedef_base_type: "RPClassifier") -> None:
        """Sets the base type of the typedef.

        Args:
            typedef_base_type: The base type to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefBaseType(com.telelogic.rhapsody.core.IRPClassifier typedefBaseType)
        """
        self.call_com(lambda: self._com.setTypedefBaseType(typedef_base_type._com))

    def set_typedef_multiplicity(self, typedef_multiplicity: str) -> None:
        """Sets the multiplicity of the typedef.

        Args:
            typedef_multiplicity: The multiplicity to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefMultiplicity(java.lang.String typedefMultiplicity)
        """
        self._set_method_or_property(self._com, "setTypedefMultiplicity", "typedefMultiplicity", typedef_multiplicity)


AbstractRPModelElement.register_wrapper("ClassifierRole", RPClassifierRole)
AbstractRPModelElement.register_wrapper("SysMLPort", RPSysMLPort)
AbstractRPModelElement.register_wrapper("Type", RPType)
