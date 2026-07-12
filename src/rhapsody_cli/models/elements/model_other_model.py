"""Other Model model-element wrappers (auto-generated stubs)."""

from typing import Any

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.relations.model_instance import RPInstance


class RPClassifierRole(RPModelElement):
    """Wraps ``IRPClassifierRole``: represents lifelines in sequence diagrams and "objects" (lifelines) in communication diagrams."""

    # IRPClassifierRole method parity checklist:
    # [ ] getFormalClassifier          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFormalInstance            [ ] impl  [ ] docstring  [ ] test
    # [ ] getReferencedSequenceDiagram [ ] impl  [ ] docstring  [ ] test
    # [ ] getReferencingClassifierRolesRecursively [ ] impl  [ ] docstring  [ ] test
    # [ ] getRoleType                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setFormalClassifier          [ ] impl  [ ] docstring  [ ] test
    # [ ] setFormalInstance            [ ] impl  [ ] docstring  [ ] test
    # [ ] setReferencedSequenceDiagram [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPClassifierRole methods.

    def get_formal_classifier(self) -> Any:
        """Returns the classifier (for example, class or actor) that the lifeline realizes.

        Returns:
            The classifier that the lifeline realizes.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalClassifier()
        """
        raise NotImplementedError

    def get_formal_instance(self) -> Any:
        """Returns the object that is realized by the lifeline, for cases where a lifeline represents an object and not just a classifier.

        Returns:
            The object that is realized by the lifeline, or null if the lifeline does not realize an object.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalInstance()
        """
        raise NotImplementedError

    def get_referenced_sequence_diagram(self) -> Any:
        """Returns the sequence diagram referenced by the lifeline.

        Returns:
            The sequence diagram referenced by the lifeline, or null if there is no referenced diagram.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencedSequenceDiagram()
        """
        raise NotImplementedError

    def get_referencing_classifier_roles_recursively(self) -> "RPCollection":
        """Returns a collection of all the lifelines in referenced sequence diagrams, recursively including all lifelines in the decomposition hierarchy.

        Returns:
            A collection of all the lifelines in referenced sequence diagrams.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencingClassifierRolesRecursively()
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError


class RPSysMLPort(RPInstance):
    """Wraps ``IRPSysMLPort``: represents flowport elements in Rhapsody models."""

    # IRPSysMLPort method parity checklist:
    # [ ] addLink                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsReversed                [ ] impl  [ ] docstring  [ ] test
    # [ ] getPortDirection             [ ] impl  [ ] docstring  [ ] test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsReversed                [ ] impl  [ ] docstring  [ ] test
    # [ ] setPortDirection             [ ] impl  [ ] docstring  [ ] test
    # [ ] setType                      [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPInstance methods (covered by RPInstance checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPRelation methods (covered by RPRelation checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPSysMLPort methods.

    def add_link(self, from_part: "RPInstance", to_part: "RPInstance", assoc: "RPRelation", to_port: "RPSysMLPort", new_owner: "RPPackage") -> Any:
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
            com.telelogic.rhapsody.core.IRPSysMLPort::addLink(com.telelogic.rhapsody.core.IRPInstance fromPart, com.telelogic.rhapsody.core.IRPInstance toPart, com.telelogic.rhapsody.core.IRPRelation assoc, com.telelogic.rhapsody.core.IRPSysMLPort toPort, com.telelogic.rhapsody.core.IRPPackage newOwner)
        """
        raise NotImplementedError

    def get_is_reversed(self) -> int:
        """Checks whether the flowport was specified as conjugated.

        Returns:
            1 if the flowport was specified as conjugated, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getIsReversed()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_type(self) -> Any:
        """Returns the type that was specified for the flowport.

        Returns:
            The type that was specified for the flowport.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getType()
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def set_type(self, type_: "RPClassifier") -> None:
        """Sets the type for the flowport.

        Args:
            type_: The type to use for the flowport.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::setType(com.telelogic.rhapsody.core.IRPClassifier type)
        """
        raise NotImplementedError


class RPType(RPClassifier):
    """Wraps ``IRPType``."""

    # IRPType method parity checklist:
    # [ ] addEnumerationLiteral        [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteEnumerationLiteral     [ ] impl  [ ] docstring  [ ] test
    # [ ] getDeclaration               [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnumerationLiterals       [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsPredefined              [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsTypedef                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsTypedefConstant         [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsTypedefOrdered          [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsTypedefReference        [ ] impl  [ ] docstring  [ ] test
    # [ ] getKind                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getTypedefBaseType           [ ] impl  [ ] docstring  [ ] test
    # [ ] getTypedefMultiplicity       [ ] impl  [ ] docstring  [ ] test
    # [ ] isArray                      [ ] impl  [ ] docstring  [ ] test
    # [ ] isEnum                       [ ] impl  [ ] docstring  [ ] test
    # [ ] isEqualTo                    [ ] impl  [ ] docstring  [ ] test
    # [ ] isImplicit                   [ ] impl  [ ] docstring  [ ] test
    # [ ] isKindEnumeration            [ ] impl  [ ] docstring  [ ] test
    # [ ] isKindLanguage               [ ] impl  [ ] docstring  [ ] test
    # [ ] isKindStruct                 [ ] impl  [ ] docstring  [ ] test
    # [ ] isKindTypedef                [ ] impl  [ ] docstring  [ ] test
    # [ ] isKindUnion                  [ ] impl  [ ] docstring  [ ] test
    # [ ] isPointer                    [ ] impl  [ ] docstring  [ ] test
    # [ ] isPointerToPointer           [ ] impl  [ ] docstring  [ ] test
    # [ ] isReference                  [ ] impl  [ ] docstring  [ ] test
    # [ ] isReferenceToPointer         [ ] impl  [ ] docstring  [ ] test
    # [ ] isStruct                     [ ] impl  [ ] docstring  [ ] test
    # [ ] isTemplate                   [ ] impl  [ ] docstring  [ ] test
    # [ ] isUnion                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setDeclaration               [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsTypedefConstant         [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsTypedefOrdered          [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsTypedefReference        [ ] impl  [ ] docstring  [ ] test
    # [ ] setKind                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setTypedefBaseType           [ ] impl  [ ] docstring  [ ] test
    # [ ] setTypedefMultiplicity       [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPType methods.

    def add_enumeration_literal(self, name: str) -> Any:
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
        raise NotImplementedError

    def delete_enumeration_literal(self, literal: "RPEnumerationLiteral") -> None:
        """Deletes the specified enumeration literal from this type.

        Args:
            literal: The enumeration literal to delete.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::deleteEnumerationLiteral(com.telelogic.rhapsody.core.IRPEnumerationLiteral literal)
        """
        raise NotImplementedError

    def get_declaration(self) -> str:
        """Returns the declaration of the type.

        Returns:
            The declaration of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getDeclaration()
        """
        raise NotImplementedError

    def get_enumeration_literals(self) -> "RPCollection":
        """Returns the enumeration literals of the type.

        Returns:
            A collection of the type's enumeration literals.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getEnumerationLiterals()
        """
        raise NotImplementedError

    def get_is_predefined(self) -> int:
        """Returns whether the type is predefined.

        Returns:
            1 if the type is predefined, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsPredefined()
        """
        raise NotImplementedError

    def get_is_typedef(self) -> int:
        """Returns whether the type is a typedef.

        Returns:
            1 if the type is a typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedef()
        """
        raise NotImplementedError

    def get_is_typedef_constant(self) -> int:
        """Returns whether the typedef is a constant.

        Returns:
            1 if the typedef is a constant, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefConstant()
        """
        raise NotImplementedError

    def get_is_typedef_ordered(self) -> int:
        """Returns whether the typedef is ordered.

        Returns:
            1 if the typedef is ordered, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefOrdered()
        """
        raise NotImplementedError

    def get_is_typedef_reference(self) -> int:
        """Returns whether the typedef is a reference.

        Returns:
            1 if the typedef is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefReference()
        """
        raise NotImplementedError

    def get_kind(self) -> str:
        """Returns the kind of the type.

        Returns:
            The kind of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getKind()
        """
        raise NotImplementedError

    def get_typedef_base_type(self) -> Any:
        """Returns the base type of the typedef.

        Returns:
            The base type of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefBaseType()
        """
        raise NotImplementedError

    def get_typedef_multiplicity(self) -> str:
        """Returns the multiplicity of the typedef.

        Returns:
            The multiplicity of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefMultiplicity()
        """
        raise NotImplementedError

    def is_array(self) -> int:
        """Checks whether the type is an array.

        Returns:
            1 if the type is an array, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isArray()
        """
        raise NotImplementedError

    def is_enum(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually an enum.

        Returns:
            1 if the type is an enum, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEnum()
        """
        raise NotImplementedError

    def is_equal_to(self) -> int:
        """Checks whether the type is an equal-to type.

        Returns:
            1 if the type is an equal-to type, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEqualTo()
        """
        raise NotImplementedError

    def is_implicit(self) -> int:
        """Checks whether the type is implicit.

        Returns:
            1 if the type is implicit, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isImplicit()
        """
        raise NotImplementedError

    def is_kind_enumeration(self) -> int:
        """Checks whether the kind of the type is Enumeration.

        Returns:
            1 if the kind of the type is Enumeration, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindEnumeration()
        """
        raise NotImplementedError

    def is_kind_language(self) -> int:
        """Checks whether the kind of the type was set to Language.

        Returns:
            1 if the kind of the type is Language, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindLanguage()
        """
        raise NotImplementedError

    def is_kind_struct(self) -> int:
        """Checks whether the kind of the type is Structure.

        Returns:
            1 if the kind of the type is Structure, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindStruct()
        """
        raise NotImplementedError

    def is_kind_typedef(self) -> int:
        """Checks whether the kind of the type is Typedef.

        Returns:
            1 if the kind of the type is Typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindTypedef()
        """
        raise NotImplementedError

    def is_kind_union(self) -> int:
        """Checks whether the kind of the type is Union.

        Returns:
            1 if the kind of the type is Union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindUnion()
        """
        raise NotImplementedError

    def is_pointer(self) -> int:
        """Checks whether the type is a pointer.

        Returns:
            1 if the type is a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointer()
        """
        raise NotImplementedError

    def is_pointer_to_pointer(self) -> int:
        """Checks whether the type is a pointer to a pointer.

        Returns:
            1 if the type is a pointer to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointerToPointer()
        """
        raise NotImplementedError

    def is_reference(self) -> int:
        """Checks whether the type is a reference.

        Returns:
            1 if the type is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReference()
        """
        raise NotImplementedError

    def is_reference_to_pointer(self) -> int:
        """Checks whether the type is a reference to a pointer.

        Returns:
            1 if the type is a reference to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReferenceToPointer()
        """
        raise NotImplementedError

    def is_struct(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a struct.

        Returns:
            1 if the type is a struct, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isStruct()
        """
        raise NotImplementedError

    def is_template(self) -> int:
        """Checks whether the type is a template.

        Returns:
            1 if the type is a template, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isTemplate()
        """
        raise NotImplementedError

    def is_union(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a union.

        Returns:
            1 if the type is a union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isUnion()
        """
        raise NotImplementedError

    def set_declaration(self, declaration: str) -> None:
        """Sets the declaration of the type.

        Args:
            declaration: The declaration to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setDeclaration(java.lang.String declaration)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def set_kind(self, kind: str) -> None:
        """Sets the kind of the type.

        Args:
            kind: The kind to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setKind(java.lang.String kind)
        """
        raise NotImplementedError

    def set_typedef_base_type(self, typedef_base_type: "RPClassifier") -> None:
        """Sets the base type of the typedef.

        Args:
            typedef_base_type: The base type to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefBaseType(com.telelogic.rhapsody.core.IRPClassifier typedefBaseType)
        """
        raise NotImplementedError

    def set_typedef_multiplicity(self, typedef_multiplicity: str) -> None:
        """Sets the multiplicity of the typedef.

        Args:
            typedef_multiplicity: The multiplicity to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefMultiplicity(java.lang.String typedefMultiplicity)
        """
        raise NotImplementedError
