"""Wraps ``com.telelogic.rhapsody.core.IRPInterfaceItem``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.variables.model_variables import RPArgument


class RPInterfaceItem(RPClassifier):
    """Wraps ``IRPInterfaceItem``: the base interface for operation-like
    elements that carry an argument list and signature (e.g. operations,
    triggers).
    """

    # IRPInterfaceItem method parity checklist:
    # [x] addArgument  [x] impl  [x] docstring  [x] test
    # [x] addArgumentBeforePosition  [x] impl  [x] docstring  [x] test
    # [x] getArguments  [x] impl  [x] docstring  [x] test
    # [x] getSignature  [x] impl  [x] docstring  [x] test
    # [x] getSignatureNoArgNames  [x] impl  [x] docstring  [x] test
    # [x] getSignatureNoArgTypes  [x] impl  [x] docstring  [x] test
    # [x] matchOnSignature  [x] impl  [x] docstring  [x] test
    # [inherited] IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPInterfaceItem methods.

    def addArgument(self, new_val: str) -> "RPArgument":
        """Adds a new argument to the end of the argument list.

        Only the name is taken from the supplied string; the argument's type
        defaults to ``int``. To change the type, use the returned
        ``IRPArgument`` object's type setter.

        Args:
            new_val: The name to use for the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::addArgument(java.lang.String newVal)
        """
        return cast("RPArgument", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addArgument(new_val))))

    def addArgumentBeforePosition(self, new_val: str, pos: int) -> "RPArgument":
        """Adds a new argument at the specified position in the argument list.

        As with :meth:`addArgument`, only the name is taken from the supplied
        string and the argument's type defaults to ``int``; change the type via
        the returned ``IRPArgument`` object's type setter.

        Args:
            new_val: The name to use for the new argument.
            pos: The 1-based position at which to insert the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::addArgumentBeforePosition(java.lang.String newVal, int pos)
        """
        return cast("RPArgument", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addArgumentBeforePosition(new_val, pos))))

    def getArguments(self) -> RPCollection:
        """Returns all the arguments for the operation.

        Returns:
            An ``RPCollection`` of ``IRPArgument`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::getArguments()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getArguments", "arguments"))

    def getSignature(self) -> str:
        """Returns the signature of the operation.

        Returns:
            The full signature string, including argument names and types.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::getSignature()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSignature", "signature"))

    def getSignatureNoArgNames(self) -> str:
        """Returns the signature of the operation without the argument names.

        Returns:
            The signature string with argument types but no argument names.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::getSignatureNoArgNames()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSignatureNoArgNames", "signatureNoArgNames"))

    def getSignatureNoArgTypes(self) -> str:
        """Returns the signature of the operation without the argument types.

        Returns:
            The signature string with argument names but no argument types.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::getSignatureNoArgTypes()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSignatureNoArgTypes", "signatureNoArgTypes"))

    def matchOnSignature(self, item: "RPInterfaceItem") -> bool:
        """Compares the signature of this operation with another operation's signature.

        This is useful when moving an operation from one class to another,
        because Rhapsody raises an exception if an operation with an identical
        signature already exists in the target class.

        Args:
            item: The other interface item to compare signatures with.

        Returns:
            ``True`` if the signatures match, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPInterfaceItem::matchOnSignature(com.telelogic.rhapsody.core.IRPInterfaceItem Item)
        """
        return bool(AbstractRPModelElement.call_com(lambda: self._com.matchOnSignature(item._com)))
