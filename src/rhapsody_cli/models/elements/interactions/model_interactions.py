"""Interactions model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
from rhapsody_cli.models.elements.containment.model_collaboration import RPCollaboration

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.activity.model_actions import RPAction
    from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
    from rhapsody_cli.models.elements.common.model_other_model import (
        RPClassifierRole,
        RPSysMLPort,
    )
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPSequenceDiagram
    from rhapsody_cli.models.elements.relations.model_association_role import (
        RPAssociationRole,
    )
    from rhapsody_cli.models.elements.relations.model_port import RPPort
    from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState, RPStateVertex


class RPEvent(RPInterfaceItem):
    """Wraps ``IRPEvent``: represents events in Rhapsody models."""

    # IRPEvent method parity checklist:
    # [x] getBaseEvent                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getSuperEvent                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setBaseEvent                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setSuperEvent                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPInterfaceItem methods (covered by RPInterfaceItem checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPEvent methods.

    def get_base_event(self) -> "RPEvent":
        return cast("RPEvent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getBaseEvent", "baseEvent")))

    def get_super_event(self) -> "RPEvent":
        return cast("RPEvent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getSuperEvent", "superEvent")))

    def set_base_event(self, base_event: "RPEvent") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setBaseEvent", "baseEvent", base_event._com)

    def set_super_event(self, super_event: "RPEvent") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setSuperEvent", "superEvent", super_event._com)


class RPEventReception(RPInterfaceItem):
    """Wraps ``IRPEventReception``."""

    # IRPEventReception method parity checklist:
    # [x] getEvent                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setEvent                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPInterfaceItem methods (covered by RPInterfaceItem checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPEventReception methods.

    def get_event(self) -> "RPEvent":
        return cast("RPEvent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getEvent", "event")))

    def set_event(self, p_val: "RPEvent") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setEvent", "event", p_val._com)


class RPExecutionOccurrence(RPModelElement):
    """Wraps ``IRPExecutionOccurrence``."""

    # IRPExecutionOccurrence method parity checklist:
    # [x] getMessage                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPExecutionOccurrence methods.

    def get_message(self) -> "RPMessage":
        return cast("RPMessage", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getMessage", "message")))


class RPGuard(RPModelElement):
    """Wraps ``IRPGuard``."""

    # IRPGuard method parity checklist:
    # [x] getBody                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setBody                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPGuard methods.

    def get_body(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def set_body(self, body: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)


class RPInteractionOccurrence(RPModelElement):
    """Wraps ``IRPInteractionOccurrence``."""

    # IRPInteractionOccurrence method parity checklist:
    # [x] getMessagePoints             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getReferenceSequenceDiagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setReferenceSequenceDiagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOccurrence methods.

    def get_message_points(self) -> "RPCollection":
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getMessagePoints", "messagePoints"))

    def get_reference_sequence_diagram(self) -> "RPSequenceDiagram":
        return cast("RPSequenceDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getReferenceSequenceDiagram", "referenceSequenceDiagram")))

    def set_reference_sequence_diagram(self, reference_sequence_diagram: "RPSequenceDiagram") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setReferenceSequenceDiagram", "referenceSequenceDiagram", reference_sequence_diagram._com)


class RPInteractionOperand(RPCollaboration):
    """Wraps ``IRPInteractionOperand``: represents interaction operands in Rhapsody models."""

    # IRPInteractionOperand method parity checklist:
    # [x] getContainedMessages         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getInteractionConstraint     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setInteractionConstraint     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPCollaboration methods (covered by RPCollaboration checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOperand methods.

    def get_contained_messages(self) -> "RPCollection":
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getContainedMessages", "containedMessages"))

    def get_interaction_constraint(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getInteractionConstraint", "interactionConstraint"))

    def set_interaction_constraint(self, interaction_constraint: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setInteractionConstraint", "interactionConstraint", interaction_constraint)


class RPInteractionOperator(RPModelElement):
    """Wraps ``IRPInteractionOperator``."""

    # IRPInteractionOperator method parity checklist:
    # [x] getInteractionOperands       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getInteractionType           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setInteractionType           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOperator methods.

    def get_interaction_operands(self) -> "RPCollection":
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInteractionOperands", "interactionOperands"))

    def get_interaction_type(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getInteractionType", "interactionType"))

    def set_interaction_type(self, interaction_type: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setInteractionType", "interactionType", interaction_type)


class RPMessage(RPModelElement):
    """Wraps ``IRPMessage``."""

    # IRPMessage method parity checklist:
    # [x] addSourceExecutionOccurrence [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] addTargetExecutionOccurrence [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getActualParameterList       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getCommunicationConnection   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getCondition                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getDurationConstraint        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getDurationObservation       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getFlowPort                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getFormalInterfaceItem       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getFormalType                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getInvariant                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getMessageType               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getPort                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getReturnValue               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getSequenceNumber            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getSignature                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getSource                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getSourceExecutionOccurrence [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTarget                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTargetExecutionOccurrence [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTimeConstraint            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTimeObservation           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getTimerValue                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] reroute                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setActualParameterList       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setDurationConstraint        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setDurationObservation       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setFlowPort                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setFormalInterfaceItem       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setFormalType                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setInvariant                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setPort                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setReturnValue               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setTimeConstraint            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setTimeObservation           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setTimerValue                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPMessage methods.

    def add_source_execution_occurrence(self) -> "RPExecutionOccurrence":
        return cast("RPExecutionOccurrence", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addSourceExecutionOccurrence())))

    def add_target_execution_occurrence(self) -> "RPExecutionOccurrence":
        return cast("RPExecutionOccurrence", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTargetExecutionOccurrence())))

    def get_actual_parameter_list(self) -> "RPCollection":
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActualParameterList", "actualParameterList"))

    def get_communication_connection(self) -> "RPAssociationRole":
        return cast("RPAssociationRole", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getCommunicationConnection", "communicationConnection")))

    def get_condition(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getCondition", "condition"))

    def get_duration_constraint(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDurationConstraint", "durationConstraint"))

    def get_duration_observation(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDurationObservation", "durationObservation"))

    def get_flow_port(self) -> "RPSysMLPort":
        return cast("RPSysMLPort", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getFlowPort", "flowPort")))

    def get_formal_interface_item(self) -> "RPInterfaceItem":
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getFormalInterfaceItem", "formalInterfaceItem")))

    def get_formal_type(self) -> "RPModelElement":
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getFormalType", "formalType"))

    def get_invariant(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getInvariant", "invariant"))

    def get_message_type(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMessageType", "messageType"))

    def get_port(self) -> "RPPort":
        return cast("RPPort", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getPort", "port")))

    def get_return_value(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getReturnValue", "returnValue"))

    def get_sequence_number(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSequenceNumber", "sequenceNumber"))

    def get_signature(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getSignature", "signature"))

    def get_source(self) -> "RPClassifierRole":
        return cast("RPClassifierRole", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getSource", "source")))

    def get_source_execution_occurrence(self) -> "RPExecutionOccurrence":
        return cast("RPExecutionOccurrence", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getSourceExecutionOccurrence", "sourceExecutionOccurrence")))

    def get_target(self) -> "RPClassifierRole":
        return cast("RPClassifierRole", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTarget", "target")))

    def get_target_execution_occurrence(self) -> "RPExecutionOccurrence":
        return cast("RPExecutionOccurrence", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTargetExecutionOccurrence", "targetExecutionOccurrence")))

    def get_time_constraint(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getTimeConstraint", "timeConstraint"))

    def get_time_observation(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getTimeObservation", "timeObservation"))

    def get_timer_value(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getTimerValue", "timerValue"))

    def reroute(self) -> None:
        AbstractRPModelElement.call_com(lambda: self._com.reroute())

    def set_actual_parameter_list(self, p_val: "RPCollection") -> None:
        AbstractRPModelElement.call_com(lambda: self._com.setActualParameterList(p_val._com))

    def set_duration_constraint(self, duration_constraint: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setDurationConstraint", "durationConstraint", duration_constraint)

    def set_duration_observation(self, duration_observation: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setDurationObservation", "durationObservation", duration_observation)

    def set_flow_port(self, flow_port: "RPSysMLPort") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setFlowPort", "flowPort", flow_port._com)

    def set_formal_interface_item(self, new_val: "RPInterfaceItem") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setFormalInterfaceItem", "formalInterfaceItem", new_val._com)

    def set_formal_type(self, formal_type: "RPModelElement") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setFormalType", "formalType", formal_type._com)

    def set_invariant(self, invariant: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setInvariant", "invariant", invariant)

    def set_port(self, port: "RPPort") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setPort", "port", port._com)

    def set_return_value(self, return_value: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setReturnValue", "returnValue", return_value)

    def set_time_constraint(self, time_constraint: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setTimeConstraint", "timeConstraint", time_constraint)

    def set_time_observation(self, time_observation: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setTimeObservation", "timeObservation", time_observation)

    def set_timer_value(self, timer_value: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setTimerValue", "timerValue", timer_value)


class RPTransition(RPModelElement):
    """Wraps ``IRPTransition``: represents transitions in a statechart."""

    # IRPTransition method parity checklist:
    # [x] getInheritsFrom              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getIsOverridden              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsAction                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsGuard                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsLabel                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsSource                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsStatechart             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsTarget                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsTrigger                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getOfState                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] isDefaultTransition          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] isStaticReaction             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] itsCompoundSource            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] overrideInheritance          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] resetLabelInheritance        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsAction                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsGuard                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsLabel                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsSource                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsStatechart             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsTarget                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setItsTrigger                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] unoverrideInheritance        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPTransition methods.

    def get_inherits_from(self) -> "RPTransition":
        return cast("RPTransition", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInheritsFrom", "inheritsFrom")))

    def get_is_overridden(self) -> int:
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsOverridden", "isOverridden"))

    def get_its_action(self) -> "RPAction":
        return cast("RPAction", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsAction", "itsAction")))

    def get_its_guard(self) -> "RPGuard":
        return cast("RPGuard", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsGuard", "itsGuard")))

    def get_its_label(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getItsLabel", "itsLabel"))

    def get_its_source(self) -> "RPStateVertex":
        return cast("RPStateVertex", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsSource", "itsSource")))

    def get_its_statechart(self) -> "RPStatechart":
        return cast("RPStatechart", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsStatechart", "itsStatechart")))

    def get_its_target(self) -> "RPStateVertex":
        return cast("RPStateVertex", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsTarget", "itsTarget")))

    def get_its_trigger(self) -> "RPTrigger":
        return cast("RPTrigger", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsTrigger", "itsTrigger")))

    def get_of_state(self) -> "RPState":
        return cast("RPState", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOfState", "ofState")))

    def is_default_transition(self) -> int:
        return int(AbstractRPModelElement.call_com(lambda: self._com.isDefaultTransition()))

    def is_static_reaction(self) -> int:
        return int(AbstractRPModelElement.call_com(lambda: self._com.isStaticReaction()))

    def its_compound_source(self) -> "RPCollection":
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.itsCompoundSource()))

    def override_inheritance(self) -> None:
        AbstractRPModelElement.call_com(lambda: self._com.overrideInheritance())

    def reset_label_inheritance(self) -> "RPTransition":
        return cast("RPTransition", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.resetLabelInheritance())))

    def set_its_action(self, action: str) -> "RPAction":
        return cast("RPAction", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setItsAction(action))))

    def set_its_guard(self, guard: str) -> "RPGuard":
        return cast("RPGuard", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setItsGuard(guard))))

    def set_its_label(self, trigger: str, guard: str, action: str) -> None:
        AbstractRPModelElement.call_com(lambda: self._com.setItsLabel(trigger, guard, action))

    def set_its_source(self, its_source: "RPStateVertex") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setItsSource", "itsSource", its_source._com)

    def set_its_statechart(self, its_statechart: "RPStatechart") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setItsStatechart", "itsStatechart", its_statechart._com)

    def set_its_target(self, its_target: "RPStateVertex") -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setItsTarget", "itsTarget", its_target._com)

    def set_its_trigger(self, trigger: str) -> "RPTrigger":
        return cast("RPTrigger", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setItsTrigger(trigger))))

    def unoverride_inheritance(self) -> None:
        AbstractRPModelElement.call_com(lambda: self._com.unoverrideInheritance())


class RPTrigger(RPModelElement):
    """Wraps ``IRPTrigger``: represents the trigger of a transition in a statechart."""

    # IRPTrigger method parity checklist:
    # [x] getBody                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getItsOperation              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] isOperation                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] isTimeout                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setBody                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPTrigger methods.

    def get_body(self) -> str:
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getBody", "body"))

    def get_its_operation(self) -> "RPInterfaceItem":
        return cast("RPInterfaceItem", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getItsOperation", "itsOperation")))

    def is_operation(self) -> int:
        return int(AbstractRPModelElement.call_com(lambda: self._com.isOperation()))

    def is_timeout(self) -> int:
        return int(AbstractRPModelElement.call_com(lambda: self._com.isTimeout()))

    def set_body(self, body: str) -> None:
        AbstractRPModelElement._set_method_or_property(self._com, "setBody", "body", body)


class RPDestructionEvent(RPMessage):
    """Wraps ``IRPDestructionEvent``: represents destruction events in sequence diagrams."""

    # IRPDestructionEvent method parity checklist:
    # [inherited] IRPMessage methods (covered by RPMessage checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPDestructionEvent methods.

    pass


AbstractRPModelElement.register_wrapper("Message", RPMessage)
AbstractRPModelElement.register_wrapper("Event", RPEvent)
AbstractRPModelElement.register_wrapper("Transition", RPTransition)
AbstractRPModelElement.register_wrapper("Trigger", RPTrigger)
AbstractRPModelElement.register_wrapper("Guard", RPGuard)
AbstractRPModelElement.register_wrapper("DestructionEvent", RPDestructionEvent)
AbstractRPModelElement.register_wrapper("ExecutionOccurrence", RPExecutionOccurrence)
AbstractRPModelElement.register_wrapper("EventReception", RPEventReception)
AbstractRPModelElement.register_wrapper("InteractionOccurrence", RPInteractionOccurrence)
AbstractRPModelElement.register_wrapper("InteractionOperand", RPInteractionOperand)
AbstractRPModelElement.register_wrapper("InteractionOperator", RPInteractionOperator)
