"""Tests for rhapsody_cli.models.elements.interactions.* classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
from rhapsody_cli.models.elements.interactions import (
    RPDestructionEvent,
    RPEvent,
    RPEventReception,
    RPExecutionOccurrence,
    RPGuard,
    RPInteractionOccurrence,
    RPInteractionOperand,
    RPInteractionOperator,
    RPMessage,
    RPTransition,
    RPTrigger,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPEvent:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Event", getName="Evt1")
        evt = RPEvent(fake)
        assert isinstance(evt, RPModelElement)
        assert evt.get_name() == "Evt1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Event", getName="Evt1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPEvent)

    def test_get_base_event_wraps_result(self) -> None:
        fake = make_fake_element("Event")
        base = make_fake_element("Event", getName="Base")
        fake.getBaseEvent.return_value = base
        evt = RPEvent(fake)
        result = evt.get_base_event()
        assert result.get_name() == "Base"
        fake.getBaseEvent.assert_called_once_with()

    def test_get_super_event_wraps_result(self) -> None:
        fake = make_fake_element("Event")
        sup = make_fake_element("Event", getName="Super")
        fake.getSuperEvent.return_value = sup
        evt = RPEvent(fake)
        result = evt.get_super_event()
        assert result.get_name() == "Super"
        fake.getSuperEvent.assert_called_once_with()

    def test_set_base_event_delegates(self) -> None:
        fake = make_fake_element("Event")
        base = make_fake_element("Event", getName="Base")
        fake.setBaseEvent.return_value = None
        evt = RPEvent(fake)
        evt.set_base_event(RPEvent(base))
        fake.setBaseEvent.assert_called_once_with(base)

    def test_set_super_event_delegates(self) -> None:
        fake = make_fake_element("Event")
        sup = make_fake_element("Event", getName="Super")
        fake.setSuperEvent.return_value = None
        evt = RPEvent(fake)
        evt.set_super_event(RPEvent(sup))
        fake.setSuperEvent.assert_called_once_with(sup)


class TestRPEventReception:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("EventReception", getName="ER1")
        er = RPEventReception(fake)
        assert isinstance(er, RPModelElement)
        assert er.get_name() == "ER1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("EventReception", getName="ER1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPEventReception)

    def test_get_event_wraps_result(self) -> None:
        fake = make_fake_element("EventReception")
        evt = make_fake_element("Event", getName="Evt1")
        fake.getEvent.return_value = evt
        er = RPEventReception(fake)
        result = er.get_event()
        assert result.get_name() == "Evt1"
        fake.getEvent.assert_called_once_with()

    def test_set_event_delegates(self) -> None:
        fake = make_fake_element("EventReception")
        evt = make_fake_element("Event", getName="Evt1")
        fake.setEvent.return_value = None
        er = RPEventReception(fake)
        er.set_event(RPEvent(evt))
        fake.setEvent.assert_called_once_with(evt)


class TestRPExecutionOccurrence:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("ExecutionOccurrence", getName="EO1")
        eo = RPExecutionOccurrence(fake)
        assert isinstance(eo, RPModelElement)
        assert eo.get_name() == "EO1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("ExecutionOccurrence", getName="EO1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPExecutionOccurrence)

    def test_get_message_wraps_result(self) -> None:
        fake = make_fake_element("ExecutionOccurrence")
        msg = make_fake_element("Message", getName="Msg1")
        fake.getMessage.return_value = msg
        eo = RPExecutionOccurrence(fake)
        result = eo.get_message()
        assert result.get_name() == "Msg1"
        fake.getMessage.assert_called_once_with()


class TestRPGuard:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Guard", getName="G1")
        g = RPGuard(fake)
        assert isinstance(g, RPModelElement)
        assert g.get_name() == "G1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Guard", getName="G1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGuard)

    def test_get_body_returns_string(self) -> None:
        fake = make_fake_element("Guard", getBody="x > 0")
        g = RPGuard(fake)
        assert g.get_body() == "x > 0"
        fake.getBody.assert_called_once_with()

    def test_set_body_delegates(self) -> None:
        fake = make_fake_element("Guard")
        fake.setBody.return_value = None
        g = RPGuard(fake)
        g.set_body("x > 0")
        fake.setBody.assert_called_once_with("x > 0")


class TestRPInteractionOccurrence:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("InteractionOccurrence", getName="IO1")
        io = RPInteractionOccurrence(fake)
        assert isinstance(io, RPModelElement)
        assert io.get_name() == "IO1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("InteractionOccurrence", getName="IO1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInteractionOccurrence)

    def test_get_message_points_returns_collection(self) -> None:
        inner = make_fake_element("Class", getName="MP")
        fake = make_fake_element("InteractionOccurrence")
        fake.getMessagePoints.return_value = make_fake_collection([inner])
        io = RPInteractionOccurrence(fake)
        result = io.get_message_points()
        assert isinstance(result, RPCollection)
        fake.getMessagePoints.assert_called_once_with()

    def test_get_reference_sequence_diagram_wraps_result(self) -> None:
        fake = make_fake_element("InteractionOccurrence")
        seq = make_fake_element("SequenceDiagram", getName="SD1")
        fake.getReferenceSequenceDiagram.return_value = seq
        io = RPInteractionOccurrence(fake)
        result = io.get_reference_sequence_diagram()
        assert result.get_name() == "SD1"
        fake.getReferenceSequenceDiagram.assert_called_once_with()

    def test_set_reference_sequence_diagram_delegates(self) -> None:
        fake = make_fake_element("InteractionOccurrence")
        seq = make_fake_element("SequenceDiagram", getName="SD1")
        fake.setReferenceSequenceDiagram.return_value = None
        io = RPInteractionOccurrence(fake)
        io.set_reference_sequence_diagram(RPModelElement(seq))
        fake.setReferenceSequenceDiagram.assert_called_once_with(seq)


class TestRPInteractionOperand:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("InteractionOperand", getName="IOp1")
        iop = RPInteractionOperand(fake)
        assert isinstance(iop, RPModelElement)
        assert iop.get_name() == "IOp1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("InteractionOperand", getName="IOp1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInteractionOperand)

    def test_get_contained_messages_returns_collection(self) -> None:
        inner = make_fake_element("Message", getName="M1")
        fake = make_fake_element("InteractionOperand")
        fake.getContainedMessages.return_value = make_fake_collection([inner])
        iop = RPInteractionOperand(fake)
        result = iop.get_contained_messages()
        assert isinstance(result, RPCollection)
        fake.getContainedMessages.assert_called_once_with()

    def test_get_interaction_constraint_returns_string(self) -> None:
        fake = make_fake_element("InteractionOperand", getInteractionConstraint="x > 0")
        iop = RPInteractionOperand(fake)
        assert iop.get_interaction_constraint() == "x > 0"
        fake.getInteractionConstraint.assert_called_once_with()

    def test_set_interaction_constraint_delegates(self) -> None:
        fake = make_fake_element("InteractionOperand")
        fake.setInteractionConstraint.return_value = None
        iop = RPInteractionOperand(fake)
        iop.set_interaction_constraint("x > 0")
        fake.setInteractionConstraint.assert_called_once_with("x > 0")


class TestRPInteractionOperator:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("InteractionOperator", getName="Alt")
        iop = RPInteractionOperator(fake)
        assert isinstance(iop, RPModelElement)
        assert iop.get_name() == "Alt"

    def test_is_registered(self) -> None:
        fake = make_fake_element("InteractionOperator", getName="Alt")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInteractionOperator)

    def test_get_interaction_operands_returns_collection(self) -> None:
        inner = make_fake_element("InteractionOperand", getName="IOp1")
        fake = make_fake_element("InteractionOperator")
        fake.getInteractionOperands.return_value = make_fake_collection([inner])
        iop = RPInteractionOperator(fake)
        result = iop.get_interaction_operands()
        assert isinstance(result, RPCollection)
        fake.getInteractionOperands.assert_called_once_with()

    def test_get_interaction_type_returns_string(self) -> None:
        fake = make_fake_element("InteractionOperator", getInteractionType="alt")
        iop = RPInteractionOperator(fake)
        assert iop.get_interaction_type() == "alt"
        fake.getInteractionType.assert_called_once_with()

    def test_set_interaction_type_delegates(self) -> None:
        fake = make_fake_element("InteractionOperator")
        fake.setInteractionType.return_value = None
        iop = RPInteractionOperator(fake)
        iop.set_interaction_type("alt")
        fake.setInteractionType.assert_called_once_with("alt")


class TestRPMessage:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Message", getName="Msg1")
        msg = RPMessage(fake)
        assert isinstance(msg, RPModelElement)
        assert msg.get_name() == "Msg1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Message", getName="Msg1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPMessage)

    def test_add_source_execution_occurrence_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        eo = make_fake_element("ExecutionOccurrence", getName="EO1")
        fake.addSourceExecutionOccurrence.return_value = eo
        msg = RPMessage(fake)
        result = msg.add_source_execution_occurrence()
        assert result.get_name() == "EO1"
        fake.addSourceExecutionOccurrence.assert_called_once_with()

    def test_add_target_execution_occurrence_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        eo = make_fake_element("ExecutionOccurrence", getName="EO2")
        fake.addTargetExecutionOccurrence.return_value = eo
        msg = RPMessage(fake)
        result = msg.add_target_execution_occurrence()
        assert result.get_name() == "EO2"
        fake.addTargetExecutionOccurrence.assert_called_once_with()

    def test_get_actual_parameter_list_returns_collection(self) -> None:
        inner = make_fake_element("Class", getName="P")
        fake = make_fake_element("Message")
        fake.getActualParameterList.return_value = make_fake_collection([inner])
        msg = RPMessage(fake)
        result = msg.get_actual_parameter_list()
        assert isinstance(result, RPCollection)
        fake.getActualParameterList.assert_called_once_with()

    def test_get_communication_connection_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        conn = make_fake_element("AssociationRole", getName="conn1")
        fake.getCommunicationConnection.return_value = conn
        msg = RPMessage(fake)
        result = msg.get_communication_connection()
        assert result.get_name() == "conn1"
        fake.getCommunicationConnection.assert_called_once_with()

    def test_get_condition_returns_string(self) -> None:
        fake = make_fake_element("Message", getCondition="cond")
        msg = RPMessage(fake)
        assert msg.get_condition() == "cond"
        fake.getCondition.assert_called_once_with()

    def test_get_duration_constraint_returns_string(self) -> None:
        fake = make_fake_element("Message", getDurationConstraint="5s")
        msg = RPMessage(fake)
        assert msg.get_duration_constraint() == "5s"
        fake.getDurationConstraint.assert_called_once_with()

    def test_get_duration_observation_returns_string(self) -> None:
        fake = make_fake_element("Message", getDurationObservation="{t}")
        msg = RPMessage(fake)
        assert msg.get_duration_observation() == "{t}"
        fake.getDurationObservation.assert_called_once_with()

    def test_get_flow_port_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        fp = make_fake_element("SysMLPort", getName="fp1")
        fake.getFlowPort.return_value = fp
        msg = RPMessage(fake)
        result = msg.get_flow_port()
        assert result.get_name() == "fp1"
        fake.getFlowPort.assert_called_once_with()

    def test_get_formal_interface_item_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        op = make_fake_element("InterfaceItem", getName="op1")
        fake.getFormalInterfaceItem.return_value = op
        msg = RPMessage(fake)
        result = msg.get_formal_interface_item()
        assert result.get_name() == "op1"
        fake.getFormalInterfaceItem.assert_called_once_with()

    def test_get_formal_type_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        ft = make_fake_element("Class", getName="FT")
        fake.getFormalType.return_value = ft
        msg = RPMessage(fake)
        result = msg.get_formal_type()
        assert result.get_name() == "FT"
        fake.getFormalType.assert_called_once_with()

    def test_get_invariant_returns_string(self) -> None:
        fake = make_fake_element("Message", getInvariant="inv")
        msg = RPMessage(fake)
        assert msg.get_invariant() == "inv"
        fake.getInvariant.assert_called_once_with()

    def test_get_message_type_returns_string(self) -> None:
        fake = make_fake_element("Message", getMessageType="asynch")
        msg = RPMessage(fake)
        assert msg.get_message_type() == "asynch"
        fake.getMessageType.assert_called_once_with()

    def test_get_port_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        p = make_fake_element("Port", getName="p1")
        fake.getPort.return_value = p
        msg = RPMessage(fake)
        result = msg.get_port()
        assert result.get_name() == "p1"
        fake.getPort.assert_called_once_with()

    def test_get_return_value_returns_string(self) -> None:
        fake = make_fake_element("Message", getReturnValue="result")
        msg = RPMessage(fake)
        assert msg.get_return_value() == "result"
        fake.getReturnValue.assert_called_once_with()

    def test_get_sequence_number_returns_string(self) -> None:
        fake = make_fake_element("Message", getSequenceNumber="1")
        msg = RPMessage(fake)
        assert msg.get_sequence_number() == "1"
        fake.getSequenceNumber.assert_called_once_with()

    def test_get_signature_returns_string(self) -> None:
        fake = make_fake_element("Message", getSignature="sig")
        msg = RPMessage(fake)
        assert msg.get_signature() == "sig"
        fake.getSignature.assert_called_once_with()

    def test_get_source_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        src = make_fake_element("ClassifierRole", getName="src")
        fake.getSource.return_value = src
        msg = RPMessage(fake)
        result = msg.get_source()
        assert result.get_name() == "src"
        fake.getSource.assert_called_once_with()

    def test_get_source_execution_occurrence_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        eo = make_fake_element("ExecutionOccurrence", getName="EO1")
        fake.getSourceExecutionOccurrence.return_value = eo
        msg = RPMessage(fake)
        result = msg.get_source_execution_occurrence()
        assert result.get_name() == "EO1"
        fake.getSourceExecutionOccurrence.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        tgt = make_fake_element("ClassifierRole", getName="tgt")
        fake.getTarget.return_value = tgt
        msg = RPMessage(fake)
        result = msg.get_target()
        assert result.get_name() == "tgt"
        fake.getTarget.assert_called_once_with()

    def test_get_target_execution_occurrence_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        eo = make_fake_element("ExecutionOccurrence", getName="EO2")
        fake.getTargetExecutionOccurrence.return_value = eo
        msg = RPMessage(fake)
        result = msg.get_target_execution_occurrence()
        assert result.get_name() == "EO2"
        fake.getTargetExecutionOccurrence.assert_called_once_with()

    def test_get_time_constraint_returns_string(self) -> None:
        fake = make_fake_element("Message", getTimeConstraint="{t}")
        msg = RPMessage(fake)
        assert msg.get_time_constraint() == "{t}"
        fake.getTimeConstraint.assert_called_once_with()

    def test_get_time_observation_returns_string(self) -> None:
        fake = make_fake_element("Message", getTimeObservation="{now}")
        msg = RPMessage(fake)
        assert msg.get_time_observation() == "{now}"
        fake.getTimeObservation.assert_called_once_with()

    def test_get_timer_value_returns_string(self) -> None:
        fake = make_fake_element("Message", getTimerValue="100")
        msg = RPMessage(fake)
        assert msg.get_timer_value() == "100"
        fake.getTimerValue.assert_called_once_with()

    def test_reroute_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.reroute.return_value = None
        msg = RPMessage(fake)
        msg.reroute()
        fake.reroute.assert_called_once_with()

    def test_set_actual_parameter_list_delegates(self) -> None:
        inner = make_fake_element("Class", getName="P")
        fake = make_fake_element("Message")
        col = RPCollection(make_fake_collection([inner]))
        fake.setActualParameterList.return_value = None
        msg = RPMessage(fake)
        msg.set_actual_parameter_list(col)
        fake.setActualParameterList.assert_called_once_with(col._com)

    def test_set_duration_constraint_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setDurationConstraint.return_value = None
        msg = RPMessage(fake)
        msg.set_duration_constraint("5s")
        fake.setDurationConstraint.assert_called_once_with("5s")

    def test_set_duration_observation_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setDurationObservation.return_value = None
        msg = RPMessage(fake)
        msg.set_duration_observation("{t}")
        fake.setDurationObservation.assert_called_once_with("{t}")

    def test_set_flow_port_delegates(self) -> None:
        fake = make_fake_element("Message")
        fp = make_fake_element("SysMLPort", getName="fp1")
        fake.setFlowPort.return_value = None
        msg = RPMessage(fake)
        msg.set_flow_port(RPModelElement(fp))
        fake.setFlowPort.assert_called_once_with(fp)

    def test_set_formal_interface_item_delegates(self) -> None:
        fake = make_fake_element("Message")
        op = make_fake_element("InterfaceItem", getName="op1")
        fake.setFormalInterfaceItem.return_value = None
        msg = RPMessage(fake)
        msg.set_formal_interface_item(RPInterfaceItem(op))
        fake.setFormalInterfaceItem.assert_called_once_with(op)

    def test_set_formal_type_delegates(self) -> None:
        fake = make_fake_element("Message")
        ft = make_fake_element("Class", getName="FT")
        fake.setFormalType.return_value = None
        msg = RPMessage(fake)
        msg.set_formal_type(RPModelElement(ft))
        fake.setFormalType.assert_called_once_with(ft)

    def test_set_invariant_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setInvariant.return_value = None
        msg = RPMessage(fake)
        msg.set_invariant("inv")
        fake.setInvariant.assert_called_once_with("inv")

    def test_set_port_delegates(self) -> None:
        fake = make_fake_element("Message")
        p = make_fake_element("Port", getName="p1")
        fake.setPort.return_value = None
        msg = RPMessage(fake)
        msg.set_port(RPModelElement(p))
        fake.setPort.assert_called_once_with(p)

    def test_set_return_value_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setReturnValue.return_value = None
        msg = RPMessage(fake)
        msg.set_return_value("result")
        fake.setReturnValue.assert_called_once_with("result")

    def test_set_time_constraint_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setTimeConstraint.return_value = None
        msg = RPMessage(fake)
        msg.set_time_constraint("{t}")
        fake.setTimeConstraint.assert_called_once_with("{t}")

    def test_set_time_observation_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setTimeObservation.return_value = None
        msg = RPMessage(fake)
        msg.set_time_observation("{now}")
        fake.setTimeObservation.assert_called_once_with("{now}")

    def test_set_timer_value_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setTimerValue.return_value = None
        msg = RPMessage(fake)
        msg.set_timer_value("100")
        fake.setTimerValue.assert_called_once_with("100")


class TestRPTransition:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        t = RPTransition(fake)
        assert isinstance(t, RPModelElement)
        assert t.get_name() == "T1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTransition)

    def test_get_inherits_from_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        base = make_fake_element("Transition", getName="Base")
        fake.getInheritsFrom.return_value = base
        t = RPTransition(fake)
        result = t.get_inherits_from()
        assert result.get_name() == "Base"
        fake.getInheritsFrom.assert_called_once_with()

    def test_get_is_overridden_returns_int(self) -> None:
        fake = make_fake_element("Transition", getIsOverridden=True)
        t = RPTransition(fake)
        assert t.get_is_overridden() == 1
        fake.getIsOverridden.assert_called_once_with()

    def test_get_its_action_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        action = make_fake_element("Action", getName="doIt")
        fake.getItsAction.return_value = action
        t = RPTransition(fake)
        result = t.get_its_action()
        assert result.get_name() == "doIt"
        fake.getItsAction.assert_called_once_with()

    def test_get_its_guard_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        guard = make_fake_element("Guard", getName="G1")
        fake.getItsGuard.return_value = guard
        t = RPTransition(fake)
        result = t.get_its_guard()
        assert result.get_name() == "G1"
        fake.getItsGuard.assert_called_once_with()

    def test_get_its_label_returns_string(self) -> None:
        fake = make_fake_element("Transition", getItsLabel="e[g]/a")
        t = RPTransition(fake)
        assert t.get_its_label() == "e[g]/a"
        fake.getItsLabel.assert_called_once_with()

    def test_get_its_source_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        src = make_fake_element("StateVertex", getName="S1")
        fake.getItsSource.return_value = src
        t = RPTransition(fake)
        result = t.get_its_source()
        assert result.get_name() == "S1"
        fake.getItsSource.assert_called_once_with()

    def test_get_its_statechart_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        sc = make_fake_element("Statechart", getName="SC1")
        fake.getItsStatechart.return_value = sc
        t = RPTransition(fake)
        result = t.get_its_statechart()
        assert result.get_name() == "SC1"
        fake.getItsStatechart.assert_called_once_with()

    def test_get_its_target_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        tgt = make_fake_element("StateVertex", getName="S2")
        fake.getItsTarget.return_value = tgt
        t = RPTransition(fake)
        result = t.get_its_target()
        assert result.get_name() == "S2"
        fake.getItsTarget.assert_called_once_with()

    def test_get_its_trigger_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        trig = make_fake_element("Trigger", getName="Trg1")
        fake.getItsTrigger.return_value = trig
        t = RPTransition(fake)
        result = t.get_its_trigger()
        assert result.get_name() == "Trg1"
        fake.getItsTrigger.assert_called_once_with()

    def test_get_of_state_wraps_result(self) -> None:
        fake = make_fake_element("Transition")
        st = make_fake_element("State", getName="S1")
        fake.getOfState.return_value = st
        t = RPTransition(fake)
        result = t.get_of_state()
        assert result.get_name() == "S1"
        fake.getOfState.assert_called_once_with()

    def test_is_default_transition_returns_int(self) -> None:
        fake = make_fake_element("Transition", isDefaultTransition=True)
        t = RPTransition(fake)
        assert t.is_default_transition() == 1
        fake.isDefaultTransition.assert_called_once_with()

    def test_is_static_reaction_returns_int(self) -> None:
        fake = make_fake_element("Transition", isStaticReaction=True)
        t = RPTransition(fake)
        assert t.is_static_reaction() == 1
        fake.isStaticReaction.assert_called_once_with()

    def test_its_compound_source_returns_collection(self) -> None:
        inner = make_fake_element("StateVertex", getName="S1")
        fake = make_fake_element("Transition")
        fake.itsCompoundSource.return_value = make_fake_collection([inner])
        t = RPTransition(fake)
        result = t.its_compound_source()
        assert isinstance(result, RPCollection)
        fake.itsCompoundSource.assert_called_once_with()

    def test_override_inheritance_delegates(self) -> None:
        fake = make_fake_element("Transition")
        fake.overrideInheritance.return_value = None
        t = RPTransition(fake)
        t.override_inheritance()
        fake.overrideInheritance.assert_called_once_with()

    def test_reset_label_inheritance_wraps_result(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        fake.resetLabelInheritance.return_value = fake
        t = RPTransition(fake)
        result = t.reset_label_inheritance()
        assert result.get_name() == "T1"
        fake.resetLabelInheritance.assert_called_once_with()

    def test_set_its_action_wraps_result(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        action = make_fake_element("Action", getName="doIt")
        fake.setItsAction.return_value = action
        t = RPTransition(fake)
        result = t.set_its_action("doIt()")
        assert result.get_name() == "doIt"
        fake.setItsAction.assert_called_once_with("doIt()")

    def test_set_its_guard_wraps_result(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        guard = make_fake_element("Guard", getName="G1")
        fake.setItsGuard.return_value = guard
        t = RPTransition(fake)
        result = t.set_its_guard("x > 0")
        assert result.get_name() == "G1"
        fake.setItsGuard.assert_called_once_with("x > 0")

    def test_set_its_label_delegates(self) -> None:
        fake = make_fake_element("Transition")
        fake.setItsLabel.return_value = None
        t = RPTransition(fake)
        t.set_its_label("evt", "g", "act")
        fake.setItsLabel.assert_called_once_with("evt", "g", "act")

    def test_set_its_source_delegates(self) -> None:
        fake = make_fake_element("Transition")
        src = make_fake_element("StateVertex", getName="S1")
        fake.setItsSource.return_value = None
        t = RPTransition(fake)
        t.set_its_source(RPModelElement(src))
        fake.setItsSource.assert_called_once_with(src)

    def test_set_its_statechart_delegates(self) -> None:
        fake = make_fake_element("Transition")
        sc = make_fake_element("Statechart", getName="SC1")
        fake.setItsStatechart.return_value = None
        t = RPTransition(fake)
        t.set_its_statechart(RPModelElement(sc))
        fake.setItsStatechart.assert_called_once_with(sc)

    def test_set_its_target_delegates(self) -> None:
        fake = make_fake_element("Transition")
        tgt = make_fake_element("StateVertex", getName="S2")
        fake.setItsTarget.return_value = None
        t = RPTransition(fake)
        t.set_its_target(RPModelElement(tgt))
        fake.setItsTarget.assert_called_once_with(tgt)

    def test_set_its_trigger_wraps_result(self) -> None:
        fake = make_fake_element("Transition", getName="T1")
        trig = make_fake_element("Trigger", getName="Trg1")
        fake.setItsTrigger.return_value = trig
        t = RPTransition(fake)
        result = t.set_its_trigger("evt")
        assert result.get_name() == "Trg1"
        fake.setItsTrigger.assert_called_once_with("evt")

    def test_unoverride_inheritance_delegates(self) -> None:
        fake = make_fake_element("Transition")
        fake.unoverrideInheritance.return_value = None
        t = RPTransition(fake)
        t.unoverride_inheritance()
        fake.unoverrideInheritance.assert_called_once_with()


class TestRPTrigger:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Trigger", getName="Trg1")
        trg = RPTrigger(fake)
        assert isinstance(trg, RPModelElement)
        assert trg.get_name() == "Trg1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Trigger", getName="Trg1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTrigger)

    def test_get_body_returns_string(self) -> None:
        fake = make_fake_element("Trigger", getBody="evt")
        trg = RPTrigger(fake)
        assert trg.get_body() == "evt"
        fake.getBody.assert_called_once_with()

    def test_get_its_operation_wraps_result(self) -> None:
        fake = make_fake_element("Trigger")
        op = make_fake_element("InterfaceItem", getName="op1")
        fake.getItsOperation.return_value = op
        trg = RPTrigger(fake)
        result = trg.get_its_operation()
        assert result.get_name() == "op1"
        fake.getItsOperation.assert_called_once_with()

    def test_is_operation_returns_int(self) -> None:
        fake = make_fake_element("Trigger", isOperation=True)
        trg = RPTrigger(fake)
        assert trg.is_operation() == 1
        fake.isOperation.assert_called_once_with()

    def test_is_timeout_returns_int(self) -> None:
        fake = make_fake_element("Trigger", isTimeout=True)
        trg = RPTrigger(fake)
        assert trg.is_timeout() == 1
        fake.isTimeout.assert_called_once_with()

    def test_set_body_delegates(self) -> None:
        fake = make_fake_element("Trigger")
        fake.setBody.return_value = None
        trg = RPTrigger(fake)
        trg.set_body("evt")
        fake.setBody.assert_called_once_with("evt")


class TestRPDestructionEvent:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("DestructionEvent", getName="DE1")
        de = RPDestructionEvent(fake)
        assert isinstance(de, RPModelElement)
        assert de.get_name() == "DE1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("DestructionEvent", getName="DE1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPDestructionEvent)
