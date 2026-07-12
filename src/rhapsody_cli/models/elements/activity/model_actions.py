"""Actions model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.model_interactions import RPMessage
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState
from rhapsody_cli.models.elements.values.model_values import RPValueSpecification

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
    from rhapsody_cli.models.elements.model_interactions import RPEvent
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPAcceptEventAction(RPState):
    """Wraps ``IRPAcceptEventAction``: represents Accept Event Action elements in a statechart or activity diagram."""

    # IRPAcceptEventAction method parity checklist:
    # [ ] getEvent                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setEvent                     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPState methods (covered by RPState checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # No deprecated IRPAcceptEventAction methods.

    def get_event(self) -> "RPEvent":
        """Returns the event that the action waits for.

        Returns:
            The event that the action waits for.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptEventAction::getEvent()
        """
        raise NotImplementedError

    def set_event(self, event: "RPEvent") -> None:
        """Specifies the event that the action should wait for.

        Args:
            event: The event that the action should wait for.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptEventAction::setEvent(com.telelogic.rhapsody.core.IRPEvent event)
        """
        raise NotImplementedError


class RPAcceptTimeEvent(RPState):
    """Wraps ``IRPAcceptTimeEvent``: represents Accept Time Event elements in activity diagrams and statecharts."""

    # IRPAcceptTimeEvent method parity checklist:
    # [ ] getDurationTime              [ ] impl  [ ] docstring  [ ] test
    # [ ] setDurationTime              [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPState methods (covered by RPState checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # No deprecated IRPAcceptTimeEvent methods.

    def get_duration_time(self) -> str:
        """Returns the duration that was specified for this element.

        Returns:
            The duration that was specified for this element.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptTimeEvent::getDurationTime()
        """
        raise NotImplementedError

    def set_duration_time(self, duration_time: str) -> None:
        """Specifies the duration that should be used for this element.

        Args:
            duration_time: The duration that should be used for this element.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptTimeEvent::setDurationTime(java.lang.String durationTime)
        """
        raise NotImplementedError


class RPAction(RPModelElement):
    """Wraps ``IRPAction``: represents the action defined for a transition in a statechart."""

    # IRPAction method parity checklist:
    # [ ] getBody                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setBody                      [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPAction methods.

    def get_body(self) -> str:
        """Gets the code defined as the action for the transition.

        Returns:
            The code defined as the action for the transition.

        Reference:
            com.telelogic.rhapsody.core.IRPAction::getBody()
        """
        raise NotImplementedError

    def set_body(self, body: str) -> None:
        """Specifies the code that serves as the action for the transition.

        Args:
            body: The code that should be used as the action for the transition.

        Reference:
            com.telelogic.rhapsody.core.IRPAction::setBody(java.lang.String body)
        """
        raise NotImplementedError


class RPActionBlock(RPMessage):
    """Wraps ``IRPActionBlock``: represents action blocks in sequence diagrams."""

    # IRPActionBlock method parity checklist:
    # [inherited] IRPMessage methods (covered by RPMessage checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPActionBlock methods.

    pass


class RPCallOperation(RPState):
    """Wraps ``IRPCallOperation``: represents call operation elements in activity diagrams."""

    # IRPCallOperation method parity checklist:
    # [ ] getOperation                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] test
    # [ ] setOperation                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setTarget                    [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPState methods (covered by RPState checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # No deprecated IRPCallOperation methods.

    def get_operation(self) -> "RPInterfaceItem":
        """Returns the operation specified for this call operation element.

        Returns:
            The operation specified for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::getOperation()
        """
        raise NotImplementedError

    def get_target(self) -> "RPRelation":
        """Returns the target specified for this call operation element.

        Returns:
            The target specified for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::getTarget()
        """
        raise NotImplementedError

    def set_operation(self, operation: "RPInterfaceItem") -> None:
        """Specifies the operation to use for this call operation element.

        Args:
            operation: The operation to use for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::setOperation(com.telelogic.rhapsody.core.IRPInterfaceItem operation)
        """
        raise NotImplementedError

    def set_target(self, target: "RPRelation") -> None:
        """Specifies the target to use for this call operation element.

        Args:
            target: The target to use for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::setTarget(com.telelogic.rhapsody.core.IRPRelation target)
        """
        raise NotImplementedError


class RPContextSpecification(RPValueSpecification):
    """Wraps ``IRPContextSpecification``: represents the exact context of an object in a hierarchy.

    Uses a collection of strings for the full path to the element and a collection
    of indices to disambiguate when multiplicity is greater than one.
    """

    # IRPContextSpecification method parity checklist:
    # [ ] getMultiplicities            [ ] impl  [ ] docstring  [ ] test
    # [ ] getValue                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setMultiplicities            [ ] impl  [ ] docstring  [ ] test
    # [ ] setValue                     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPValueSpecification methods (covered by RPValueSpecification checklist)
    # No deprecated IRPContextSpecification methods.

    def get_multiplicities(self) -> "RPCollection":
        """Returns the collection of relevant indices for each of the model elements in the "value" collection.

        Returns:
            A ``RPCollection`` of indices (integers provided as strings) for the
            model elements in the "value" collection.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::getMultiplicities()
        """
        raise NotImplementedError

    def get_value(self) -> "RPCollection":
        """Returns the collection of strings that represents the model elements constituting the full path to the element.

        Returns:
            A ``RPCollection`` of strings representing the full path to the element.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::getValue()
        """
        raise NotImplementedError

    def set_multiplicities(self, multiplicities: "RPCollection") -> None:
        """Specifies the collection of indices to use for the model elements in the "value" collection.

        Args:
            multiplicities: A ``RPCollection`` of indices (integers provided as
                strings) for the model elements in the "value" collection.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::setMultiplicities(com.telelogic.rhapsody.core.IRPCollection multiplicities)
        """
        raise NotImplementedError

    def set_value(self, value: "RPCollection") -> None:
        """Specifies the collection of strings that represents the model elements constituting the full path to the element.

        Args:
            value: A ``RPCollection`` of strings representing the full path to the
                element.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::setValue(com.telelogic.rhapsody.core.IRPCollection value)
        """
        raise NotImplementedError


class RPSendAction(RPAction):
    """Wraps ``IRPSendAction``: represents Send Action elements in an activity or statechart."""

    # IRPSendAction method parity checklist:
    # [ ] addArgumentValue             [ ] impl  [ ] docstring  [ ] test
    # [ ] getArgVals                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getEvent                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getInvokedOperation          [ ] impl  [ ] docstring  [ ] test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] test
    # [ ] setEvent                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setInvokedOperation          [ ] impl  [ ] docstring  [ ] test
    # [ ] setTarget                    [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPAction methods (covered by RPAction checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPSendAction methods.

    def add_argument_value(self, value: str, position: int) -> None:
        """Provides an argument value for an argument of the event associated with the Send Action element.

        Args:
            value: The value to use for the argument, expressed as a string.
            position: The position of the argument in the argument list (starts at 1).

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::addArgumentValue(java.lang.String value, int position)
        """
        raise NotImplementedError

    def get_arg_vals(self) -> "RPCollection":
        """Returns a collection of the argument values set for the event associated with the Send Action element.

        Returns:
            A ``RPCollection`` of strings representing the argument values that
            were set for the event.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getArgVals()
        """
        raise NotImplementedError

    def get_event(self) -> "RPEvent":
        """Gets the event sent by the Send Action element.

        Returns:
            The event sent by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getEvent()
        """
        raise NotImplementedError

    def get_invoked_operation(self) -> "RPInterfaceItem":
        """Returns the interface item element that is invoked by the Send Action element.

        Returns:
            The ``IRPInterfaceItem`` element that is invoked by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getInvokedOperation()
        """
        raise NotImplementedError

    def get_target(self) -> "RPModelElement":
        """Gets the event target of the Send Action element.

        Returns:
            The target of the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getTarget()
        """
        raise NotImplementedError

    def set_event(self, event: "RPEvent") -> None:
        """Specifies the event sent by the Send Action element.

        Args:
            event: The event that should be sent by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setEvent(com.telelogic.rhapsody.core.IRPEvent event)
        """
        raise NotImplementedError

    def set_invoked_operation(self, invoked_operation: "RPInterfaceItem") -> None:
        """Sets the invoked operation property.

        Args:
            invoked_operation: The invoked operation to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setInvokedOperation(com.telelogic.rhapsody.core.IRPInterfaceItem invokedOperation)
        """
        raise NotImplementedError

    def set_target(self, target: "RPModelElement") -> None:
        """Sets the specified model element to be the target of the Send Action element.

        Args:
            target: The model element that should be used as the target of the Send
                Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setTarget(com.telelogic.rhapsody.core.IRPModelElement target)
        """
        raise NotImplementedError
