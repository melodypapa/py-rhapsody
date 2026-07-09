"""Wraps ``com.telelogic.rhapsody.core.IRPInterfaceItem``."""

from typing import Any

from rhapsody_cli.models.core import RPCollection, call_com, wrap
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


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
