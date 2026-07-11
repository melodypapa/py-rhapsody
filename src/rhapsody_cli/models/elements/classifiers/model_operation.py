"""Wraps ``com.telelogic.rhapsody.core.IRPOperation``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem


class RPOperation(RPInterfaceItem):
    """Wraps ``IRPOperation``: represents an operation or method in a classifier."""

    def getBody(self) -> str:
        """Returns the body/implementation of the operation.

        Returns:
            The operation's body code as a string.
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def getIsAbstract(self) -> bool:
        """Checks whether this operation is abstract.

        Returns:
            ``True`` if the operation is abstract, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsAbstract", "isAbstract"))

    def getIsStatic(self) -> bool:
        """Checks whether this operation is static.

        Returns:
            ``True`` if the operation is static, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsStatic", "isStatic"))

    def getIsVirtual(self) -> bool:
        """Checks whether this operation is virtual.

        Returns:
            ``True`` if the operation is virtual, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsVirtual", "isVirtual"))

    def getReturns(self) -> Any:
        """Returns the type specification for the operation's return value.

        Returns:
            The wrapped return type element.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getReturns", "returns"))

    def getReturnTypeDeclaration(self) -> str:
        """Returns the on-the-fly return type declaration for the operation.

        Returns:
            The return type declaration as a string (e.g. ``"int"``).
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getReturnTypeDeclaration", "returnTypeDeclaration"))

    def createAutoFlowChart(self) -> None:
        """Automatically generates a flowchart for the operation."""
        AbstractRPModelElement.call_com(lambda: self._com.createAutoFlowChart())

    def setReturns(self, returns: Any) -> None:
        """Sets the return type of the operation to an existing classifier.

        Args:
            returns: The wrapped ``IRPClassifier`` to use as the return type.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setReturns", "returns", returns._com)

    def setReturnTypeDeclaration(self, new_val: str) -> None:
        """Specifies an on-the-fly return type declaration for the operation.

        Args:
            new_val: The on-the-fly type declaration (e.g. ``"int"``), reusing
                a matching existing type if found.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setReturnTypeDeclaration", "returnTypeDeclaration", new_val)


AbstractRPModelElement.register_wrapper("Operation", RPOperation)
