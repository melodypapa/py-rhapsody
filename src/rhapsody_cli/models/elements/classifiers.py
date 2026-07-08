"""Classifier-family wrappers: mirrors IRPClassifier and its Java subtypes
(IRPClass, IRPActor, IRPUseCase, IRPOperation, IRPStatechart) from
com.telelogic.rhapsody.core.
"""

from typing import Any

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``: the base class for all classifiable elements."""

    def addAttribute(self, name: str) -> Any:
        """Adds a new attribute to the classifier.

        Args:
            name: The name of the new attribute.

        Returns:
            The wrapped ``IRPAttribute`` created.
        """
        return wrap(call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> Any:
        """Adds a new operation to the classifier.

        Args:
            name: The name of the new operation.

        Returns:
            The wrapped ``IRPOperation`` created.
        """
        return wrap(call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        """Returns all attributes defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getAttributes()))

    def getOperations(self) -> RPCollection:
        """Returns all operations defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPOperation`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getOperations()))

    def addGeneralization(self, base_classifier: "RPClassifier") -> None:
        """Adds a generalization relationship from this classifier to another.

        Args:
            base_classifier: The base classifier to generalize from.
        """
        call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> Any:
        """Adds a statechart behavior to this classifier.

        Returns:
            The wrapped ``IRPStatechart`` created.
        """
        return wrap(call_com(lambda: self._com.addStatechart()))


class RPClass(RPClassifier):
    """Wraps ``IRPClass``: represents a class in the model."""

    def addSuperclass(self, super_class: "RPClass") -> None:
        """Adds a superclass to this class.

        Args:
            super_class: The class to inherit from.
        """
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        """Adds a constructor operation to this class.

        Args:
            arguments_data: The argument specification for the constructor.

        Returns:
            The wrapped ``IRPOperation`` for the new constructor.
        """
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        """Adds a destructor operation to this class.

        Returns:
            The wrapped ``IRPOperation`` for the new destructor.
        """
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        """Checks whether this class is abstract.

        Returns:
            ``True`` if the class is abstract, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> Any:
        """Adds a nested class to this class.

        Args:
            name: The name of the new nested class.

        Returns:
            The wrapped ``IRPClass`` created.
        """
        return wrap(call_com(lambda: self._com.addClass(name)))


class RPActor(RPClassifier):
    """Wraps ``IRPActor``: represents an actor in the model."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        """Adds a new event reception to the actor.

        Args:
            name: The name of the event reception.
            event: The event model element associated with the reception.

        Returns:
            The wrapped ``IRPEventReception`` created.
        """
        return wrap(call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        """Checks whether the behavior of the actor is overridden.

        Returns:
            ``True`` if the behavior is overridden, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        """Sets whether the behavior of the actor is overridden.

        Args:
            is_overridden: ``True`` to mark the behavior as overridden, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0))


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``: represents a use case in the model."""

    def addExtensionPoint(self, entry_point: str) -> None:
        """Adds an extension point to the use case.

        Args:
            entry_point: The name of the extension point.
        """
        call_com(lambda: self._com.addExtensionPoint(entry_point))

    def getExtensionPoints(self) -> RPCollection:
        """Returns all extension points defined on the use case.

        Returns:
            An ``RPCollection`` of extension point strings.
        """
        return RPCollection(call_com(lambda: self._com.getExtensionPoints()))

    def getEntryPoints(self) -> RPCollection:
        """Returns all entry points defined on the use case.

        Returns:
            An ``RPCollection`` of entry point strings.
        """
        return RPCollection(call_com(lambda: self._com.getEntryPoints()))

    def getDescribingDiagrams(self) -> RPCollection:
        """Returns all diagrams that describe this use case.

        Returns:
            An ``RPCollection`` of ``IRPDiagram`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getDescribingDiagrams()))


class RPInterfaceItem(RPClassifier):
    """Wraps ``IRPInterfaceItem``: the base interface for operation-like
    elements that carry an argument list and signature (e.g. operations,
    triggers).
    """

    def addArgument(self, new_val: str) -> Any:
        """Adds a new argument to the end of the argument list.

        Args:
            new_val: The name (or name/type expression) of the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.
        """
        return wrap(call_com(lambda: self._com.addArgument(new_val)))

    def addArgumentBeforePosition(self, new_val: str, pos: int) -> Any:
        """Adds a new argument at the specified position in the argument list.

        Args:
            new_val: The name (or name/type expression) of the new argument.
            pos: The 1-based position at which to insert the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.
        """
        return wrap(call_com(lambda: self._com.addArgumentBeforePosition(new_val, pos)))

    def getArguments(self) -> RPCollection:
        """Returns all the arguments for the operation.

        Returns:
            An ``RPCollection`` of ``IRPArgument`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getArguments()))

    def getSignature(self) -> str:
        """Returns the signature of the operation.

        Returns:
            The full signature string, including argument names and types.
        """
        return call_com(lambda: str(self._com.getSignature()))

    def getSignatureNoArgNames(self) -> str:
        """Returns the signature of the operation without the argument names.

        Returns:
            The signature string with argument types but no argument names.
        """
        return call_com(lambda: str(self._com.getSignatureNoArgNames()))

    def getSignatureNoArgTypes(self) -> str:
        """Returns the signature of the operation without the argument types.

        Returns:
            The signature string with argument names but no argument types.
        """
        return call_com(lambda: str(self._com.getSignatureNoArgTypes()))

    def matchOnSignature(self, item: "RPInterfaceItem") -> bool:
        """Compares the signature of this operation with another operation's signature.

        Args:
            item: The other interface item to compare signatures with.

        Returns:
            ``True`` if the signatures match, ``False`` otherwise.
        """
        return bool(call_com(lambda: self._com.matchOnSignature(item._com)))


class RPOperation(RPInterfaceItem):
    """Wraps ``IRPOperation``: represents an operation or method in a classifier."""

    def getBody(self) -> str:
        """Returns the body/implementation of the operation.

        Returns:
            The operation's body code as a string.
        """
        return call_com(lambda: str(self._com.getBody()))

    def getIsAbstract(self) -> bool:
        """Checks whether this operation is abstract.

        Returns:
            ``True`` if the operation is abstract, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def getIsStatic(self) -> bool:
        """Checks whether this operation is static.

        Returns:
            ``True`` if the operation is static, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsStatic()))

    def getIsVirtual(self) -> bool:
        """Checks whether this operation is virtual.

        Returns:
            ``True`` if the operation is virtual, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsVirtual()))

    def getReturns(self) -> Any:
        """Returns the type specification for the operation's return value.

        Returns:
            The wrapped return type element.
        """
        return wrap(call_com(lambda: self._com.getReturns()))

    def createAutoFlowChart(self) -> None:
        """Automatically generates a flowchart for the operation."""
        call_com(lambda: self._com.createAutoFlowChart())


class RPStatechart(RPClass):
    """Wraps ``IRPStatechart``: represents a statechart behavior."""

    def addNewNodeByType(self, meta_type: str, x_position: int, y_position: int, width: int, height: int) -> Any:
        """Adds a new node to the statechart.

        Args:
            meta_type: The type of node to create (e.g., 'State', 'Junction').
            x_position: The X coordinate for the node.
            y_position: The Y coordinate for the node.
            width: The width of the node.
            height: The height of the node.

        Returns:
            The wrapped node element created.
        """
        return wrap(call_com(lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height)))

    def createGraphics(self) -> None:
        """Creates the graphics/diagram representation for the statechart."""
        call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        """Closes the statechart diagram."""
        call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        """Deletes a state from the statechart.

        Args:
            state: The state element to delete.
        """
        call_com(lambda: self._com.deleteState(state._com))


register_wrapper("Class", RPClass)
register_wrapper("Actor", RPActor)
register_wrapper("UseCase", RPUseCase)
register_wrapper("Operation", RPOperation)
register_wrapper("Statechart", RPStatechart)
