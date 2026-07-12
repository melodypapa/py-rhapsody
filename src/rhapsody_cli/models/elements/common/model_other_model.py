"""Other Model model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.relations.model_instance import RPInstance

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.common.model_misc import RPEnumerationLiteral
    from rhapsody_cli.models.elements.containment.model_package import RPPackage
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
    from rhapsody_cli.models.elements.graphics.model_graphics import RPLink
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


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

    def getFormalClassifier(self) -> "RPClassifier":
        """Returns the classifier (for example, class or actor) that the lifeline realizes.

        Returns:
            The classifier that the lifeline realizes.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalClassifier()
        """
        raise NotImplementedError

    def getFormalInstance(self) -> "RPInstance":
        """Returns the object that is realized by the lifeline, for cases where a lifeline represents an object and not just a classifier.

        Returns:
            The object that is realized by the lifeline, or null if the lifeline does not realize an object.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getFormalInstance()
        """
        raise NotImplementedError

    def getReferencedSequenceDiagram(self) -> "RPSequenceDiagram":
        """Returns the sequence diagram referenced by the lifeline.

        Returns:
            The sequence diagram referenced by the lifeline, or null if there is no referenced diagram.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencedSequenceDiagram()
        """
        raise NotImplementedError

    def getReferencingClassifierRolesRecursively(self) -> "RPCollection":
        """Returns a collection of all the lifelines in referenced sequence diagrams, recursively including all lifelines in the decomposition hierarchy.

        Returns:
            A collection of all the lifelines in referenced sequence diagrams.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPClassifierRole::getReferencingClassifierRolesRecursively()
        """
        raise NotImplementedError

    def getRoleType(self) -> str:
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

    def setFormalClassifier(self, formal_classifier: "RPClassifier") -> None:
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

    def setFormalInstance(self, formal_instance: "RPInstance") -> None:
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

    def setReferencedSequenceDiagram(self, referenced_sequence_diagram: "RPSequenceDiagram") -> None:
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

    def addLink(self, from_part: "RPInstance", to_part: "RPInstance", assoc: "RPRelation", to_port: "RPSysMLPort", new_owner: "RPPackage") -> "RPLink":
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
        raise NotImplementedError

    def getIsReversed(self) -> int:
        """Checks whether the flowport was specified as conjugated.

        Returns:
            1 if the flowport was specified as conjugated, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getIsReversed()
        """
        raise NotImplementedError

    def getPortDirection(self) -> str:
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

    def getType(self) -> "RPClassifier":
        """Returns the type that was specified for the flowport.

        Returns:
            The type that was specified for the flowport.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPSysMLPort::getType()
        """
        raise NotImplementedError

    def setIsReversed(self, is_reversed: int) -> None:
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

    def setPortDirection(self, port_direction: str) -> None:
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

    def setType(self, type_: "RPClassifier") -> None:
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

    def addEnumerationLiteral(self, name: str) -> "RPEnumerationLiteral":
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

    def deleteEnumerationLiteral(self, literal: "RPEnumerationLiteral") -> None:
        """Deletes the specified enumeration literal from this type.

        Args:
            literal: The enumeration literal to delete.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::deleteEnumerationLiteral(com.telelogic.rhapsody.core.IRPEnumerationLiteral literal)
        """
        raise NotImplementedError

    def getDeclaration(self) -> str:
        """Returns the declaration of the type.

        Returns:
            The declaration of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getDeclaration()
        """
        raise NotImplementedError

    def getEnumerationLiterals(self) -> "RPCollection":
        """Returns the enumeration literals of the type.

        Returns:
            A collection of the type's enumeration literals.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getEnumerationLiterals()
        """
        raise NotImplementedError

    def getIsPredefined(self) -> int:
        """Returns whether the type is predefined.

        Returns:
            1 if the type is predefined, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsPredefined()
        """
        raise NotImplementedError

    def getIsTypedef(self) -> int:
        """Returns whether the type is a typedef.

        Returns:
            1 if the type is a typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedef()
        """
        raise NotImplementedError

    def getIsTypedefConstant(self) -> int:
        """Returns whether the typedef is a constant.

        Returns:
            1 if the typedef is a constant, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefConstant()
        """
        raise NotImplementedError

    def getIsTypedefOrdered(self) -> int:
        """Returns whether the typedef is ordered.

        Returns:
            1 if the typedef is ordered, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefOrdered()
        """
        raise NotImplementedError

    def getIsTypedefReference(self) -> int:
        """Returns whether the typedef is a reference.

        Returns:
            1 if the typedef is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getIsTypedefReference()
        """
        raise NotImplementedError

    def getKind(self) -> str:
        """Returns the kind of the type.

        Returns:
            The kind of the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getKind()
        """
        raise NotImplementedError

    def getTypedefBaseType(self) -> "RPClassifier":
        """Returns the base type of the typedef.

        Returns:
            The base type of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefBaseType()
        """
        raise NotImplementedError

    def getTypedefMultiplicity(self) -> str:
        """Returns the multiplicity of the typedef.

        Returns:
            The multiplicity of the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::getTypedefMultiplicity()
        """
        raise NotImplementedError

    def isArray(self) -> int:
        """Checks whether the type is an array.

        Returns:
            1 if the type is an array, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isArray()
        """
        raise NotImplementedError

    def isEnum(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually an enum.

        Returns:
            1 if the type is an enum, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEnum()
        """
        raise NotImplementedError

    def isEqualTo(self) -> int:
        """Checks whether the type is an equal-to type.

        Returns:
            1 if the type is an equal-to type, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isEqualTo()
        """
        raise NotImplementedError

    def isImplicit(self) -> int:
        """Checks whether the type is implicit.

        Returns:
            1 if the type is implicit, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isImplicit()
        """
        raise NotImplementedError

    def isKindEnumeration(self) -> int:
        """Checks whether the kind of the type is Enumeration.

        Returns:
            1 if the kind of the type is Enumeration, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindEnumeration()
        """
        raise NotImplementedError

    def isKindLanguage(self) -> int:
        """Checks whether the kind of the type was set to Language.

        Returns:
            1 if the kind of the type is Language, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindLanguage()
        """
        raise NotImplementedError

    def isKindStruct(self) -> int:
        """Checks whether the kind of the type is Structure.

        Returns:
            1 if the kind of the type is Structure, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindStruct()
        """
        raise NotImplementedError

    def isKindTypedef(self) -> int:
        """Checks whether the kind of the type is Typedef.

        Returns:
            1 if the kind of the type is Typedef, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindTypedef()
        """
        raise NotImplementedError

    def isKindUnion(self) -> int:
        """Checks whether the kind of the type is Union.

        Returns:
            1 if the kind of the type is Union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isKindUnion()
        """
        raise NotImplementedError

    def isPointer(self) -> int:
        """Checks whether the type is a pointer.

        Returns:
            1 if the type is a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointer()
        """
        raise NotImplementedError

    def isPointerToPointer(self) -> int:
        """Checks whether the type is a pointer to a pointer.

        Returns:
            1 if the type is a pointer to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isPointerToPointer()
        """
        raise NotImplementedError

    def isReference(self) -> int:
        """Checks whether the type is a reference.

        Returns:
            1 if the type is a reference, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReference()
        """
        raise NotImplementedError

    def isReferenceToPointer(self) -> int:
        """Checks whether the type is a reference to a pointer.

        Returns:
            1 if the type is a reference to a pointer, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isReferenceToPointer()
        """
        raise NotImplementedError

    def isStruct(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a struct.

        Returns:
            1 if the type is a struct, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isStruct()
        """
        raise NotImplementedError

    def isTemplate(self) -> int:
        """Checks whether the type is a template.

        Returns:
            1 if the type is a template, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isTemplate()
        """
        raise NotImplementedError

    def isUnion(self) -> int:
        """For types whose kind was set to Language, parses the declaration to see if the type is actually a union.

        Returns:
            1 if the type is a union, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::isUnion()
        """
        raise NotImplementedError

    def setDeclaration(self, declaration: str) -> None:
        """Sets the declaration of the type.

        Args:
            declaration: The declaration to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setDeclaration(java.lang.String declaration)
        """
        raise NotImplementedError

    def setIsTypedefConstant(self, is_typedef_constant: int) -> None:
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

    def setIsTypedefOrdered(self, is_typedef_ordered: int) -> None:
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

    def setIsTypedefReference(self, is_typedef_reference: int) -> None:
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

    def setKind(self, kind: str) -> None:
        """Sets the kind of the type.

        Args:
            kind: The kind to set for the type.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setKind(java.lang.String kind)
        """
        raise NotImplementedError

    def setTypedefBaseType(self, typedef_base_type: "RPClassifier") -> None:
        """Sets the base type of the typedef.

        Args:
            typedef_base_type: The base type to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefBaseType(com.telelogic.rhapsody.core.IRPClassifier typedefBaseType)
        """
        raise NotImplementedError

    def setTypedefMultiplicity(self, typedef_multiplicity: str) -> None:
        """Sets the multiplicity of the typedef.

        Args:
            typedef_multiplicity: The multiplicity to set for the typedef.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPType::setTypedefMultiplicity(java.lang.String typedefMultiplicity)
        """
        raise NotImplementedError
