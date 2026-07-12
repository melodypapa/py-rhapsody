"""Wraps ``com.telelogic.rhapsody.core.IRPOperation``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPOperation(RPInterfaceItem):
    """Wraps ``IRPOperation``: represents an operation or method in a classifier."""

    # IRPOperation method parity checklist:
    # [x] create_auto_flow_chart  [x] impl  [x] docstring  [x] test
    # [ ] deleteArgument  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteFlowchart  [ ] impl  [ ] docstring  [ ] test
    # [x] get_body  [x] impl  [x] docstring  [x] test
    # [ ] getFlowchart  [ ] impl  [ ] docstring  [ ] test
    # [ ] getImplementationSignature  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInitializer  [ ] impl  [ ] docstring  [ ] test
    # [x] get_is_abstract  [x] impl  [x] docstring  [x] test
    # [ ] getIsCgDerived  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsConst  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsCtor  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsDtor  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsFinal  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsInline  [ ] impl  [ ] docstring  [ ] test
    # [x] get_is_static  [x] impl  [x] docstring  [x] test
    # [ ] getIsTrigger  [ ] impl  [ ] docstring  [ ] test
    # [x] get_is_virtual  [x] impl  [x] docstring  [x] test
    # [x] get_return_type_declaration  [x] impl  [x] docstring  [x] test
    # [x] get_returns  [x] impl  [x] docstring  [x] test
    # [ ] getVisibility  [ ] impl  [ ] docstring  [ ] test
    # [ ] setBody  [ ] impl  [ ] docstring  [ ] test
    # [ ] setFlowchart  [ ] impl  [ ] docstring  [ ] test
    # [ ] setInitializer  [ ] impl  [ ] docstring  [ ] test
    # [x] set_is_abstract  [x] impl  [x] docstring  [ ] test
    # [ ] setIsConst  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsFinal  [ ] impl  [ ] docstring  [ ] test
    # [x] set_is_static  [x] impl  [x] docstring  [ ] test
    # [x] set_is_virtual  [x] impl  [x] docstring  [ ] test
    # [x] set_return_type_declaration  [x] impl  [x] docstring  [x] test
    # [x] set_returns  [x] impl  [x] docstring  [x] test
    # [ ] setVisibility  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedDiagramsOnServer  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPInterfaceItem / IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPInterfaceItem / RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPOperation methods.

    def get_body(self) -> str:
        """Returns the body/implementation of the operation.

        Returns:
            The operation's body code as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getBody()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def get_is_abstract(self) -> bool:
        """Checks whether this operation is abstract.

        Returns:
            ``True`` if the operation is abstract, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsAbstract()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsAbstract", "isAbstract"))

    def set_is_abstract(self, is_abstract: int) -> None:
        """Sets whether this operation is abstract.

        Args:
            is_abstract: ``1`` to mark the operation as abstract, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setIsAbstract(boolean isAbstract)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsAbstract(is_abstract))

    def get_is_static(self) -> bool:
        """Checks whether this operation is static.

        Returns:
            ``True`` if the operation is static, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsStatic()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsStatic", "isStatic"))

    def set_is_static(self, is_static: int) -> None:
        """Sets whether this operation is static.

        Args:
            is_static: ``1`` to mark the operation as static, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setIsStatic(boolean isStatic)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsStatic(is_static))

    def get_is_virtual(self) -> bool:
        """Checks whether this operation is virtual (for C++ or C# classes).

        Returns:
            ``True`` if the operation is virtual, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsVirtual()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsVirtual", "isVirtual"))

    def set_is_virtual(self, is_virtual: int) -> None:
        """Sets whether this operation is virtual (for C++ or C# classes).

        Args:
            is_virtual: ``1`` to mark the operation as virtual, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setIsVirtual(boolean isVirtual)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsVirtual(is_virtual))

    def get_returns(self) -> "RPClassifier":
        """Returns the type specification for the operation's return value.

        Returns:
            The wrapped return type element.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getReturns()
        """
        return cast("RPClassifier", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getReturns", "returns")))

    def get_return_type_declaration(self) -> str:
        """Returns the on-the-fly return type declaration for the operation.

        Returns:
            The return type declaration as a string (e.g. ``"int"``).

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getReturnTypeDeclaration()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getReturnTypeDeclaration", "returnTypeDeclaration"))

    def create_auto_flow_chart(self) -> None:
        """Automatically generates a flowchart for the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::createAutoFlowChart()
        """
        AbstractRPModelElement.call_com(lambda: self._com.createAutoFlowChart())

    def set_returns(self, returns: "RPClassifier") -> None:
        """Sets the return type of the operation to an existing classifier.

        Args:
            returns: The wrapped ``IRPClassifier`` to use as the return type.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setReturns(com.telelogic.rhapsody.core.IRPClassifier returns)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setReturns", "returns", returns._com)

    def set_return_type_declaration(self, new_val: str) -> None:
        """Specifies an on-the-fly return type declaration for the operation.

        Args:
            new_val: The on-the-fly type declaration (e.g. ``"int"``), reusing
                a matching existing type if found.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setReturnTypeDeclaration(java.lang.String newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setReturnTypeDeclaration", "returnTypeDeclaration", new_val)


AbstractRPModelElement.register_wrapper("Operation", RPOperation)
