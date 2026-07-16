"""Wraps ``com.telelogic.rhapsody.core.IRPOperation``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPActivityDiagram


class RPOperation(RPInterfaceItem):
    """Wraps ``IRPOperation``: represents an operation or method in a classifier."""

    # IRPOperation method parity checklist:
    # [x] create_auto_flow_chart  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_argument  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_flowchart  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_body  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] get_flowchart  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_implementation_signature  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_initializer  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_is_abstract  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] get_is_cg_derived  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_is_const  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_is_ctor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_is_dtor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_is_final  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_is_inline  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_is_static  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] get_is_trigger  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_is_virtual  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_return_type_declaration  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_returns  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_visibility  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_body  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_flowchart  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_initializer  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] set_is_abstract  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] set_is_const  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_is_final  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] set_is_static  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_virtual  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_return_type_declaration  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_returns  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] set_visibility  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] update_contained_diagrams_on_server  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_interface_item / irp_classifier / irp_unit / irp_model_element methods (covered by rp_interface_item / rp_classifier / rp_unit / rp_model_element checklists)
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
        AbstractRPModelElement._set_method_or_property(self._com, "setIsAbstract", "isAbstract", is_abstract)

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
        AbstractRPModelElement._set_method_or_property(self._com, "setIsStatic", "isStatic", is_static)

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
        AbstractRPModelElement._set_method_or_property(self._com, "setIsVirtual", "isVirtual", is_virtual)

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

    def delete_argument(self, argument: RPModelElement) -> None:
        """Deletes the specified argument from the operation.

        Args:
            argument: The wrapped argument to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::deleteArgument(com.telelogic.rhapsody.core.IRPArgument argument)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteArgument(argument._com))

    def delete_flowchart(self) -> None:
        """Deletes the flowchart associated with the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::deleteFlowchart()
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFlowchart())

    def get_flowchart(self) -> "RPActivityDiagram":
        """Returns the flowchart associated with the operation.

        Returns:
            The wrapped activity diagram representing the flowchart.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getFlowchart()
        """
        return cast("RPActivityDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getFlowchart", "flowchart")))

    def get_implementation_signature(self) -> str:
        """Returns the implementation signature of the operation.

        Returns:
            The implementation signature as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getImplementationSignature()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getImplementationSignature", "implementationSignature"))

    def get_initializer(self) -> str:
        """Returns the initializer for the operation.

        Returns:
            The initializer as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getInitializer()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getInitializer", "initializer"))

    def get_is_cg_derived(self) -> int:
        """Checks whether the operation's code is derived from code generation.

        Returns:
            ``1`` if the operation is code-generated derived, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsCgDerived()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsCgDerived", "isCgDerived"))

    def get_is_const(self) -> int:
        """Checks whether the operation is const (C++).

        Returns:
            ``1`` if the operation is const, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsConst()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsConst", "isConst"))

    def get_is_ctor(self) -> int:
        """Checks whether the operation is a constructor.

        Returns:
            ``1`` if the operation is a constructor, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsCtor()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsCtor", "isCtor"))

    def get_is_dtor(self) -> int:
        """Checks whether the operation is a destructor.

        Returns:
            ``1`` if the operation is a destructor, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsDtor()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsDtor", "isDtor"))

    def get_is_final(self) -> int:
        """Checks whether the operation is final.

        Returns:
            ``1`` if the operation is final, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsFinal()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsFinal", "isFinal"))

    def get_is_inline(self) -> int:
        """Checks whether the operation is inline.

        Returns:
            ``1`` if the operation is inline, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsInline()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsInline", "isInline"))

    def get_is_trigger(self) -> int:
        """Checks whether the operation is used as a trigger.

        Returns:
            ``1`` if the operation is a trigger, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getIsTrigger()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsTrigger", "isTrigger"))

    def get_visibility(self) -> int:
        """Returns the visibility of the operation.

        The visibility values correspond to:
        - 0: Private
        - 1: Protected
        - 2: Public
        - 3: Package

        Returns:
            The visibility as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::getVisibility()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def set_body(self, body: str) -> None:
        """Sets the body/implementation of the operation.

        Args:
            body: The body code to set.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setBody(java.lang.String body)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)

    def set_flowchart(self, flowchart: RPModelElement) -> None:
        """Sets the flowchart associated with the operation.

        Args:
            flowchart: The wrapped activity diagram to set as the flowchart.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setFlowchart(com.telelogic.rhapsody.core.IRPActivityDiagram flowchart)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setFlowchart", "flowchart", flowchart._com)

    def set_initializer(self, initializer: str) -> None:
        """Sets the initializer for the operation.

        Args:
            initializer: The initializer string to set.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setInitializer(java.lang.String initializer)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setInitializer", "initializer", initializer)

    def set_is_const(self, is_const: int) -> None:
        """Sets whether the operation is const (C++).

        Args:
            is_const: ``1`` to mark the operation as const, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setIsConst(int isConst)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsConst(is_const))

    def set_is_final(self, is_final: int) -> None:
        """Sets whether the operation is final.

        Args:
            is_final: ``1`` to mark the operation as final, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setIsFinal(int isFinal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsFinal(is_final))

    def set_visibility(self, visibility: int) -> None:
        """Sets the visibility of the operation.

        The visibility values correspond to:
        - 0: Private
        - 1: Protected
        - 2: Public
        - 3: Package

        Args:
            visibility: The visibility value to set.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::setVisibility(int visibility)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setVisibility(visibility))

    def update_contained_diagrams_on_server(self) -> None:
        """Updates the contained diagrams on the server.

        This method is relevant when working with Design Manager.

        Reference:
            com.telelogic.rhapsody.core.IRPOperation::updateContainedDiagramsOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer())


AbstractRPModelElement.register_wrapper("Operation", RPOperation)
