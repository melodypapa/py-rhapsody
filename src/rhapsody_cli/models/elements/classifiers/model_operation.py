"""Wraps ``com.telelogic.rhapsody.core.IRPOperation``."""

from typing import Any

from rhapsody_cli.models.core import call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem


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


register_wrapper("Operation", RPOperation)
