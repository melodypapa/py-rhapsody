"""Actions model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, Optional, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.interactions.model_interactions import RPMessage
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState
from rhapsody_cli.models.elements.values.model_values import RPValueSpecification

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
    from rhapsody_cli.models.elements.interactions.model_interactions import RPEvent
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPAcceptEventAction(RPState):
    """Wraps ``IRPAcceptEventAction``: represents Accept Event Action elements in a statechart or activity diagram."""

    # IRPAcceptEventAction method parity checklist:
    # [x] get_event                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_event                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_state methods (covered by rp_state checklist)
    # [inherited] irp_state_vertex methods (covered by rp_state_vertex checklist)
    # No deprecated IRPAcceptEventAction methods.

    def get_event(self) -> "RPEvent":
        """Returns the event that the action waits for.

        Returns:
            The event that the action waits for.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptEventAction::getEvent()
        """
        return cast("RPEvent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getEvent", "event")))

    def set_event(self, event: "RPEvent") -> None:
        """Specifies the event that the action should wait for.

        Args:
            event: The event that the action should wait for.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptEventAction::setEvent(com.telelogic.rhapsody.core.IRPEvent event)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setEvent", "event", event._com)


class RPAcceptTimeEvent(RPState):
    """Wraps ``IRPAcceptTimeEvent``: represents Accept Time Event elements in activity diagrams and statecharts."""

    # IRPAcceptTimeEvent method parity checklist:
    # [x] get_duration_time              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_duration_time              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_state methods (covered by rp_state checklist)
    # [inherited] irp_state_vertex methods (covered by rp_state_vertex checklist)
    # No deprecated IRPAcceptTimeEvent methods.

    def get_duration_time(self) -> str:
        """Returns the duration that was specified for this element.

        Returns:
            The duration that was specified for this element.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptTimeEvent::getDurationTime()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDurationTime", "durationTime"))

    def set_duration_time(self, duration_time: str) -> None:
        """Specifies the duration that should be used for this element.

        Args:
            duration_time: The duration that should be used for this element.

        Reference:
            com.telelogic.rhapsody.core.IRPAcceptTimeEvent::setDurationTime(java.lang.String durationTime)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDurationTime", "durationTime", duration_time)


class RPAction(RPModelElement):
    """Wraps ``IRPAction``: represents the action defined for a transition in a statechart."""

    # IRPAction method parity checklist:
    # [x] get_body                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_body                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPAction methods.

    def get_body(self) -> str:
        """Gets the code defined as the action for the transition.

        Returns:
            The code defined as the action for the transition.

        Reference:
            com.telelogic.rhapsody.core.IRPAction::getBody()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def set_body(self, body: str) -> None:
        """Specifies the code that serves as the action for the transition.

        Args:
            body: The code that should be used as the action for the transition.

        Reference:
            com.telelogic.rhapsody.core.IRPAction::setBody(java.lang.String body)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)


class RPActionBlock(RPMessage):
    """Wraps ``IRPActionBlock``: represents action blocks in sequence diagrams."""

    # IRPActionBlock method parity checklist:
    # [inherited] irp_message methods (covered by rp_message checklist)
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPActionBlock methods.

    pass


class RPCallOperation(RPState):
    """Wraps ``IRPCallOperation``: represents call operation elements in activity diagrams."""

    # IRPCallOperation method parity checklist:
    # [x] get_operation                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_target                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_operation                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_target                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_state methods (covered by rp_state checklist)
    # [inherited] irp_state_vertex methods (covered by rp_state_vertex checklist)
    # No deprecated IRPCallOperation methods.

    def get_operation(self) -> "RPInterfaceItem":
        """Returns the operation specified for this call operation element.

        Returns:
            The operation specified for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::getOperation()
        """
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOperation", "operation")))

    def get_target(self) -> "RPRelation":
        """Returns the target specified for this call operation element.

        Returns:
            The target specified for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::getTarget()
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTarget", "target")))

    def set_operation(self, operation: "RPInterfaceItem") -> None:
        """Specifies the operation to use for this call operation element.

        Args:
            operation: The operation to use for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::setOperation(com.telelogic.rhapsody.core.IRPInterfaceItem operation)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOperation", "operation", operation._com)

    def set_target(self, target: "RPRelation") -> None:
        """Specifies the target to use for this call operation element.

        Args:
            target: The target to use for this call operation element.

        Reference:
            com.telelogic.rhapsody.core.IRPCallOperation::setTarget(com.telelogic.rhapsody.core.IRPRelation target)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setTarget", "target", target._com)


class RPContextSpecification(RPValueSpecification):
    """Wraps ``IRPContextSpecification``: represents the exact context of an object in a hierarchy.

    Uses a collection of strings for the full path to the element and a collection
    of indices to disambiguate when multiplicity is greater than one.
    """

    # IRPContextSpecification method parity checklist:
    # [x] get_multiplicities            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_multiplicities            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_value                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # [inherited] irp_value_specification methods (covered by rp_value_specification checklist)
    # No deprecated IRPContextSpecification methods.

    def get_multiplicities(self) -> "RPCollection":
        """Returns the collection of relevant indices for each of the model elements in the "value" collection.

        Returns:
            A ``RPCollection`` of indices (integers provided as strings) for the
            model elements in the "value" collection.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::getMultiplicities()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getMultiplicities", "multiplicities"))

    def get_value(self) -> "RPCollection":
        """Returns the collection of strings that represents the model elements constituting the full path to the element.

        Returns:
            A ``RPCollection`` of strings representing the full path to the element.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::getValue()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getValue", "value"))

    def set_multiplicities(self, multiplicities: "RPCollection") -> None:
        """Specifies the collection of indices to use for the model elements in the "value" collection.

        Args:
            multiplicities: A ``RPCollection`` of indices (integers provided as
                strings) for the model elements in the "value" collection.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::setMultiplicities(com.telelogic.rhapsody.core.IRPCollection multiplicities)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setMultiplicities(multiplicities._com))

    def set_value(self, value: "RPCollection") -> None:
        """Specifies the collection of strings that represents the model elements constituting the full path to the element.

        Args:
            value: A ``RPCollection`` of strings representing the full path to the
                element.

        Reference:
            com.telelogic.rhapsody.core.IRPContextSpecification::setValue(com.telelogic.rhapsody.core.IRPCollection value)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setValue(value._com))


class RPSendAction(RPAction):
    """Wraps ``IRPSendAction``: represents Send Action elements in an activity or statechart."""

    # IRPSendAction method parity checklist:
    # [x] add_argument_value             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_arg_vals                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_event                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_invoked_operation          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_target                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_event                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_invoked_operation          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_target                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_action methods (covered by rp_action checklist)
    # [inherited] irp_model_element methods (covered by rp_model_element checklist)
    # No deprecated IRPSendAction methods.

    def add_argument_value(self, value: str, position: int) -> None:
        """Provides an argument value for an argument of the event associated with the Send Action element.

        Args:
            value: The value to use for the argument, expressed as a string.
            position: The position of the argument in the argument list (starts at 1).

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::addArgumentValue(java.lang.String value, int position)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addArgumentValue(value, position))

    def get_arg_vals(self) -> "RPCollection":
        """Returns a collection of the argument values set for the event associated with the Send Action element.

        Returns:
            A ``RPCollection`` of strings representing the argument values that
            were set for the event.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getArgVals()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getArgVals", "argVals"))

    def get_event(self) -> "RPEvent":
        """Gets the event sent by the Send Action element.

        Returns:
            The event sent by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getEvent()
        """
        return cast("RPEvent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getEvent", "event")))

    def get_invoked_operation(self) -> "RPInterfaceItem":
        """Returns the interface item element that is invoked by the Send Action element.

        Returns:
            The ``IRPInterfaceItem`` element that is invoked by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getInvokedOperation()
        """
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInvokedOperation", "invokedOperation")))

    def get_target(self) -> Optional["RPModelElement"]:
        """Gets the event target of the Send Action element.

        Returns:
            The target of the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::getTarget()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTarget", "target"))

    def set_event(self, event: "RPEvent") -> None:
        """Specifies the event sent by the Send Action element.

        Args:
            event: The event that should be sent by the Send Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setEvent(com.telelogic.rhapsody.core.IRPEvent event)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setEvent", "event", event._com)

    def set_invoked_operation(self, invoked_operation: "RPInterfaceItem") -> None:
        """Sets the invoked operation property.

        Args:
            invoked_operation: The invoked operation to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setInvokedOperation(com.telelogic.rhapsody.core.IRPInterfaceItem invokedOperation)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setInvokedOperation", "invokedOperation", invoked_operation._com)

    def set_target(self, target: "RPModelElement") -> None:
        """Sets the specified model element to be the target of the Send Action element.

        Args:
            target: The model element that should be used as the target of the Send
                Action element.

        Reference:
            com.telelogic.rhapsody.core.IRPSendAction::setTarget(com.telelogic.rhapsody.core.IRPModelElement target)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setTarget", "target", target._com)


# Register wrappers for Rhapsody meta classes
AbstractRPModelElement.register_wrapper("AcceptEventAction", RPAcceptEventAction)
AbstractRPModelElement.register_wrapper("AcceptTimeEvent", RPAcceptTimeEvent)
AbstractRPModelElement.register_wrapper("Action", RPAction)
AbstractRPModelElement.register_wrapper("ActionBlock", RPActionBlock)
AbstractRPModelElement.register_wrapper("CallOperation", RPCallOperation)
AbstractRPModelElement.register_wrapper("ContextSpecification", RPContextSpecification)
AbstractRPModelElement.register_wrapper("SendAction", RPSendAction)
