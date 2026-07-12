"""Interactions model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
from rhapsody_cli.models.elements.containment.model_collaboration import RPCollaboration

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
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
    # [ ] getBaseEvent                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getSuperEvent                [ ] impl  [ ] docstring  [ ] test
    # [ ] setBaseEvent                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setSuperEvent                [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPInterfaceItem methods (covered by RPInterfaceItem checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPEvent methods.

    def getBaseEvent(self) -> "RPEvent":
        """Returns the base event of this event.

        Returns:
            The base event, or ``None`` if not set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPEvent::getBaseEvent()
        """
        raise NotImplementedError

    def getSuperEvent(self) -> "RPEvent":
        """Returns the super event of this event.

        Returns:
            The super event, or ``None`` if not set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPEvent::getSuperEvent()
        """
        raise NotImplementedError

    def setBaseEvent(self, base_event: "RPEvent") -> None:
        """Sets the base event of this event.

        Args:
            base_event: The base event to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPEvent::setBaseEvent(com.telelogic.rhapsody.core.IRPEvent baseEvent)
        """
        raise NotImplementedError

    def setSuperEvent(self, super_event: "RPEvent") -> None:
        """Sets the super event of this event.

        Args:
            super_event: The super event to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPEvent::setSuperEvent(com.telelogic.rhapsody.core.IRPEvent superEvent)
        """
        raise NotImplementedError


class RPEventReception(RPInterfaceItem):
    """Wraps ``IRPEventReception``."""

    # IRPEventReception method parity checklist:
    # [ ] getEvent                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setEvent                     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPInterfaceItem methods (covered by RPInterfaceItem checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPEventReception methods.

    def getEvent(self) -> "RPEvent":
        """Returns the event associated with this event reception.

        Returns:
            The associated event.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPEventReception::getEvent()
        """
        raise NotImplementedError

    def setEvent(self, p_val: "RPEvent") -> None:
        """Sets the event associated with this event reception.

        Args:
            p_val: The event to associate with this reception.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPEventReception::setEvent(com.telelogic.rhapsody.core.IRPEvent pVal)
        """
        raise NotImplementedError


class RPExecutionOccurrence(RPModelElement):
    """Wraps ``IRPExecutionOccurrence``."""

    # IRPExecutionOccurrence method parity checklist:
    # [ ] getMessage                   [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPExecutionOccurrence methods.

    def getMessage(self) -> "RPMessage":
        """Returns the message associated with this execution occurrence.

        Returns:
            The associated message.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPExecutionOccurrence::getMessage()
        """
        raise NotImplementedError


class RPGuard(RPModelElement):
    """Wraps ``IRPGuard``."""

    # IRPGuard method parity checklist:
    # [ ] getBody                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setBody                      [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPGuard methods.

    def getBody(self) -> str:
        """Returns the body of this guard.

        Returns:
            The guard body text.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPGuard::getBody()
        """
        raise NotImplementedError

    def setBody(self, body: str) -> None:
        """Sets the body of this guard.

        Args:
            body: The guard body text to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPGuard::setBody(java.lang.String body)
        """
        raise NotImplementedError


class RPInteractionOccurrence(RPModelElement):
    """Wraps ``IRPInteractionOccurrence``."""

    # IRPInteractionOccurrence method parity checklist:
    # [ ] getMessagePoints             [ ] impl  [ ] docstring  [ ] test
    # [ ] getReferenceSequenceDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] setReferenceSequenceDiagram  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOccurrence methods.

    def getMessagePoints(self) -> "RPCollection":
        """Returns the message points of this interaction occurrence.

        Returns:
            A collection of message points.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOccurrence::getMessagePoints()
        """
        raise NotImplementedError

    def getReferenceSequenceDiagram(self) -> "RPSequenceDiagram":
        """Returns the reference sequence diagram of this interaction occurrence.

        Returns:
            The referenced sequence diagram.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOccurrence::getReferenceSequenceDiagram()
        """
        raise NotImplementedError

    def setReferenceSequenceDiagram(self, reference_sequence_diagram: "RPSequenceDiagram") -> None:
        """Sets the reference sequence diagram of this interaction occurrence.

        Args:
            reference_sequence_diagram: The sequence diagram to reference.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOccurrence::setReferenceSequenceDiagram(com.telelogic.rhapsody.core.IRPSequenceDiagram referenceSequenceDiagram)
        """
        raise NotImplementedError


class RPInteractionOperand(RPCollaboration):
    """Wraps ``IRPInteractionOperand``: represents interaction operands in Rhapsody models."""

    # IRPInteractionOperand method parity checklist:
    # [ ] getContainedMessages         [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionConstraint     [ ] impl  [ ] docstring  [ ] test
    # [ ] setInteractionConstraint     [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPCollaboration methods (covered by RPCollaboration checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOperand methods.

    def getContainedMessages(self) -> "RPCollection":
        """Returns a collection of all the messages contained in this interaction operand.

        Returns:
            A collection of messages contained in this interaction operand.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperand::getContainedMessages()
        """
        raise NotImplementedError

    def getInteractionConstraint(self) -> str:
        """Returns the constraint (guard condition) defined for this interaction operand.

        Returns:
            The constraint (guard condition) defined for this interaction operand.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperand::getInteractionConstraint()
        """
        raise NotImplementedError

    def setInteractionConstraint(self, interaction_constraint: str) -> None:
        """Sets the constraint (guard condition) for this interaction operand.

        Args:
            interaction_constraint: The constraint (guard condition) to use, for example, "x = 5".

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperand::setInteractionConstraint(java.lang.String interactionConstraint)
        """
        raise NotImplementedError


class RPInteractionOperator(RPModelElement):
    """Wraps ``IRPInteractionOperator``."""

    # IRPInteractionOperator method parity checklist:
    # [ ] getInteractionOperands       [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionType           [ ] impl  [ ] docstring  [ ] test
    # [ ] setInteractionType           [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPInteractionOperator methods.

    def getInteractionOperands(self) -> "RPCollection":
        """Returns the interaction operands of this interaction operator.

        Returns:
            A collection of interaction operands.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperator::getInteractionOperands()
        """
        raise NotImplementedError

    def getInteractionType(self) -> str:
        """Returns the interaction type of this interaction operator.

        Returns:
            The interaction type.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperator::getInteractionType()
        """
        raise NotImplementedError

    def setInteractionType(self, interaction_type: str) -> None:
        """Sets the interaction type of this interaction operator.

        Args:
            interaction_type: The interaction type to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInteractionOperator::setInteractionType(java.lang.String interactionType)
        """
        raise NotImplementedError


class RPMessage(RPModelElement):
    """Wraps ``IRPMessage``."""

    # IRPMessage method parity checklist:
    # [ ] addSourceExecutionOccurrence [ ] impl  [ ] docstring  [ ] test
    # [ ] addTargetExecutionOccurrence [ ] impl  [ ] docstring  [ ] test
    # [ ] getActualParameterList       [ ] impl  [ ] docstring  [ ] test
    # [ ] getCommunicationConnection   [ ] impl  [ ] docstring  [ ] test
    # [ ] getCondition                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getDurationConstraint        [ ] impl  [ ] docstring  [ ] test
    # [ ] getDurationObservation       [ ] impl  [ ] docstring  [ ] test
    # [ ] getFlowPort                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFormalInterfaceItem       [ ] impl  [ ] docstring  [ ] test
    # [ ] getFormalType                [ ] impl  [ ] docstring  [ ] test
    # [ ] getInvariant                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getMessageType               [ ] impl  [ ] docstring  [ ] test
    # [ ] getPort                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getReturnValue               [ ] impl  [ ] docstring  [ ] test
    # [ ] getSequenceNumber            [ ] impl  [ ] docstring  [ ] test
    # [ ] getSignature                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getSource                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getSourceExecutionOccurrence [ ] impl  [ ] docstring  [ ] test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getTargetExecutionOccurrence [ ] impl  [ ] docstring  [ ] test
    # [ ] getTimeConstraint            [ ] impl  [ ] docstring  [ ] test
    # [ ] getTimeObservation           [ ] impl  [ ] docstring  [ ] test
    # [ ] getTimerValue                [ ] impl  [ ] docstring  [ ] test
    # [ ] reroute                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setActualParameterList       [ ] impl  [ ] docstring  [ ] test
    # [ ] setDurationConstraint        [ ] impl  [ ] docstring  [ ] test
    # [ ] setDurationObservation       [ ] impl  [ ] docstring  [ ] test
    # [ ] setFlowPort                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setFormalInterfaceItem       [ ] impl  [ ] docstring  [ ] test
    # [ ] setFormalType                [ ] impl  [ ] docstring  [ ] test
    # [ ] setInvariant                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setPort                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setReturnValue               [ ] impl  [ ] docstring  [ ] test
    # [ ] setTimeConstraint            [ ] impl  [ ] docstring  [ ] test
    # [ ] setTimeObservation           [ ] impl  [ ] docstring  [ ] test
    # [ ] setTimerValue                [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPMessage methods.

    def addSourceExecutionOccurrence(self) -> "RPExecutionOccurrence":
        """Adds a source execution occurrence to this message.

        Returns:
            The newly created source execution occurrence.

        Raises:
            RhapsodyRuntimeException: If the execution occurrence cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::addSourceExecutionOccurrence()
        """
        raise NotImplementedError

    def addTargetExecutionOccurrence(self) -> "RPExecutionOccurrence":
        """Adds a target execution occurrence to this message.

        Returns:
            The newly created target execution occurrence.

        Raises:
            RhapsodyRuntimeException: If the execution occurrence cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::addTargetExecutionOccurrence()
        """
        raise NotImplementedError

    def getActualParameterList(self) -> "RPCollection":
        """Returns the actual parameter list of this message.

        Returns:
            A collection of actual parameters.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getActualParameterList()
        """
        raise NotImplementedError

    def getCommunicationConnection(self) -> "RPAssociationRole":
        """Returns the communication connection of this message.

        Returns:
            The association role representing the communication connection.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getCommunicationConnection()
        """
        raise NotImplementedError

    def getCondition(self) -> str:
        """Returns the condition of this message.

        Returns:
            The condition text.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getCondition()
        """
        raise NotImplementedError

    def getDurationConstraint(self) -> str:
        """Gets the text of the Duration Constraint.

        Returns:
            The text of the Duration Constraint.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getDurationConstraint()
        """
        raise NotImplementedError

    def getDurationObservation(self) -> str:
        """Gets the text of the Duration Observation.

        Returns:
            The text of the Duration Observation.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getDurationObservation()
        """
        raise NotImplementedError

    def getFlowPort(self) -> "RPSysMLPort":
        """Returns the flow port of this message.

        Returns:
            The SysML flow port.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getFlowPort()
        """
        raise NotImplementedError

    def getFormalInterfaceItem(self) -> "RPInterfaceItem":
        """Returns the formal interface item of this message.

        Returns:
            The formal interface item (e.g. operation or event).

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getFormalInterfaceItem()
        """
        raise NotImplementedError

    def getFormalType(self) -> "RPModelElement":
        """Returns the model element associated with an action block, condition
        mark, timeout, or canceled timeout, in a sequence diagram.

        Returns:
            The model element associated with this sequence diagram element.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getFormalType()
        """
        raise NotImplementedError

    def getInvariant(self) -> str:
        """Gets the text of the Invariant field for the state invariant.

        Returns:
            The text of the Invariant field.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getInvariant()
        """
        raise NotImplementedError

    def getMessageType(self) -> str:
        """Returns the message type of this message.

        Returns:
            The message type.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getMessageType()
        """
        raise NotImplementedError

    def getPort(self) -> "RPPort":
        """Returns the port of this message.

        Returns:
            The port associated with this message.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getPort()
        """
        raise NotImplementedError

    def getReturnValue(self) -> str:
        """Returns the return value of this message.

        Returns:
            The return value text.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getReturnValue()
        """
        raise NotImplementedError

    def getSequenceNumber(self) -> str:
        """Returns the sequence number of this message.

        Returns:
            The sequence number.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getSequenceNumber()
        """
        raise NotImplementedError

    def getSignature(self) -> str:
        """Returns the signature of this message.

        Returns:
            The message signature.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getSignature()
        """
        raise NotImplementedError

    def getSource(self) -> "RPClassifierRole":
        """Returns the source classifier role of this message.

        Returns:
            The source classifier role.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getSource()
        """
        raise NotImplementedError

    def getSourceExecutionOccurrence(self) -> "RPExecutionOccurrence":
        """Returns the source execution occurrence of this message.

        Returns:
            The source execution occurrence.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getSourceExecutionOccurrence()
        """
        raise NotImplementedError

    def getTarget(self) -> "RPClassifierRole":
        """Returns the target classifier role of this message.

        Returns:
            The target classifier role.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getTarget()
        """
        raise NotImplementedError

    def getTargetExecutionOccurrence(self) -> "RPExecutionOccurrence":
        """Returns the target execution occurrence of this message.

        Returns:
            The target execution occurrence.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getTargetExecutionOccurrence()
        """
        raise NotImplementedError

    def getTimeConstraint(self) -> str:
        """Gets the text for the Time Constraint that was applied to this state
        variant.

        Returns:
            The text for the Time Constraint.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getTimeConstraint()
        """
        raise NotImplementedError

    def getTimeObservation(self) -> str:
        """Gets the text of the Time Observation.

        Returns:
            The text of the Time Observation.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getTimeObservation()
        """
        raise NotImplementedError

    def getTimerValue(self) -> str:
        """Returns the timer value of this message.

        Returns:
            The timer value.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::getTimerValue()
        """
        raise NotImplementedError

    def reroute(self) -> None:
        """Reroutes this message.

        Raises:
            RhapsodyRuntimeException: If the message cannot be rerouted.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::reroute()
        """
        raise NotImplementedError

    def setActualParameterList(self, p_val: "RPCollection") -> None:
        """Sets the actual parameter list of this message.

        Args:
            p_val: A collection of actual parameters.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setActualParameterList(com.telelogic.rhapsody.core.IRPCollection pVal)
        """
        raise NotImplementedError

    def setDurationConstraint(self, duration_constraint: str) -> None:
        """Modifies the text of this Duration Constraint.

        Args:
            duration_constraint: The text to use for the Duration Constraint.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setDurationConstraint(java.lang.String durationConstraint)
        """
        raise NotImplementedError

    def setDurationObservation(self, duration_observation: str) -> None:
        """Modifies the text of this Duration Observation.

        Args:
            duration_observation: The text to use for the Duration Observation.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setDurationObservation(java.lang.String durationObservation)
        """
        raise NotImplementedError

    def setFlowPort(self, flow_port: "RPSysMLPort") -> None:
        """Sets the flow port of this message.

        Args:
            flow_port: The SysML flow port to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setFlowPort(com.telelogic.rhapsody.core.IRPSysMLPort flowPort)
        """
        raise NotImplementedError

    def setFormalInterfaceItem(self, new_val: "RPInterfaceItem") -> None:
        """Sets the realization of a message.

        Args:
            new_val: The operation or other interface item to use for the
                realization of the message.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setFormalInterfaceItem(com.telelogic.rhapsody.core.IRPInterfaceItem newVal)
        """
        raise NotImplementedError

    def setFormalType(self, formal_type: "RPModelElement") -> None:
        """Specifies the model element that should be associated with an action
        block, condition mark, timeout, or canceled timeout, in a sequence
        diagram.

        Args:
            formal_type: The model element to associate with this sequence
                diagram element.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setFormalType(com.telelogic.rhapsody.core.IRPModelElement formalType)
        """
        raise NotImplementedError

    def setInvariant(self, invariant: str) -> None:
        """Modifies the text of the Invariant field for the state invariant.

        Args:
            invariant: The text to use for the Invariant field.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setInvariant(java.lang.String invariant)
        """
        raise NotImplementedError

    def setPort(self, port: "RPPort") -> None:
        """Sets the port of this message.

        Args:
            port: The port to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setPort(com.telelogic.rhapsody.core.IRPPort port)
        """
        raise NotImplementedError

    def setReturnValue(self, return_value: str) -> None:
        """Sets the return value of this message.

        Args:
            return_value: The return value text to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setReturnValue(java.lang.String returnValue)
        """
        raise NotImplementedError

    def setTimeConstraint(self, time_constraint: str) -> None:
        """Modifies the text of this Time Constraint.

        Args:
            time_constraint: The text to use for this Time Constraint.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setTimeConstraint(java.lang.String timeConstraint)
        """
        raise NotImplementedError

    def setTimeObservation(self, time_observation: str) -> None:
        """Modifies the text of this Time Observation.

        Args:
            time_observation: The text to use for the Time Observation.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setTimeObservation(java.lang.String timeObservation)
        """
        raise NotImplementedError

    def setTimerValue(self, timer_value: str) -> None:
        """Sets the timer value of this message.

        Args:
            timer_value: The timer value to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPMessage::setTimerValue(java.lang.String timerValue)
        """
        raise NotImplementedError


class RPTransition(RPModelElement):
    """Wraps ``IRPTransition``: represents transitions in a statechart."""

    # IRPTransition method parity checklist:
    # [ ] getInheritsFrom              [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsOverridden              [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsAction                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsGuard                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsLabel                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsSource                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsStatechart             [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsTarget                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsTrigger                [ ] impl  [ ] docstring  [ ] test
    # [ ] getOfState                   [ ] impl  [ ] docstring  [ ] test
    # [ ] isDefaultTransition          [ ] impl  [ ] docstring  [ ] test
    # [ ] isStaticReaction             [ ] impl  [ ] docstring  [ ] test
    # [ ] itsCompoundSource            [ ] impl  [ ] docstring  [ ] test
    # [ ] overrideInheritance          [ ] impl  [ ] docstring  [ ] test
    # [ ] resetLabelInheritance        [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsAction                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsGuard                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsLabel                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsSource                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsStatechart             [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsTarget                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsTrigger                [ ] impl  [ ] docstring  [ ] test
    # [ ] unoverrideInheritance        [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPTransition methods.

    def getInheritsFrom(self) -> "RPTransition":
        """For transitions inherited from a base statechart, returns the base
        transition from which this transition is derived.

        Returns:
            The base transition from which this transition is derived.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getInheritsFrom()
        """
        raise NotImplementedError

    def getIsOverridden(self) -> int:
        """Checks whether the transition is a new transition added to the
        derived statechart, or a transition inherited from the base statechart.

        Returns:
            1 if the transition is new in the derived statechart, 0 if
            inherited from the base statechart.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getIsOverridden()
        """
        raise NotImplementedError

    def getItsAction(self) -> "RPAction":
        """Returns the action that was set for the transition.

        Returns:
            The action for the transition.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsAction()
        """
        raise NotImplementedError

    def getItsGuard(self) -> "RPGuard":
        """Returns the guard that was set for the transition.

        Returns:
            The guard for the transition.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsGuard()
        """
        raise NotImplementedError

    def getItsLabel(self) -> str:
        """Returns the trigger, guard, and action for the transition as a single
        string, as it appears in the transition label in the statechart.

        For example, ``IgnitionEvent[gear == 0]/runStarter()``.

        Returns:
            A string consisting of the trigger, guard, and action.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsLabel()
        """
        raise NotImplementedError

    def getItsSource(self) -> "RPStateVertex":
        """Returns the state that is the source of the transition.

        Returns:
            The source state vertex.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsSource()
        """
        raise NotImplementedError

    def getItsStatechart(self) -> "RPStatechart":
        """Returns the statechart that the transition belongs to.

        Returns:
            The owning statechart.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsStatechart()
        """
        raise NotImplementedError

    def getItsTarget(self) -> "RPStateVertex":
        """Returns the state that is the target of the transition.

        Returns:
            The target state vertex.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsTarget()
        """
        raise NotImplementedError

    def getItsTrigger(self) -> "RPTrigger":
        """Returns the trigger that was set for the transition.

        Returns:
            The trigger for the transition.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getItsTrigger()
        """
        raise NotImplementedError

    def getOfState(self) -> "RPState":
        """For default transitions, returns the state where the transition
        originates. If called on a non-default transition, returns null.

        Returns:
            The state where the transition originates (for default transitions).

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::getOfState()
        """
        raise NotImplementedError

    def isDefaultTransition(self) -> int:
        """Checks whether this is the default transition of the statechart.

        Returns:
            1 if the transition is the default transition, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::isDefaultTransition()
        """
        raise NotImplementedError

    def isStaticReaction(self) -> int:
        """Checks whether the transition is an internal transition in a state.

        Returns:
            1 if the transition is an internal transition, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::isStaticReaction()
        """
        raise NotImplementedError

    def itsCompoundSource(self) -> "RPCollection":
        """Returns the compound source of this transition.

        Returns:
            A collection of source state vertices.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::itsCompoundSource()
        """
        raise NotImplementedError

    def overrideInheritance(self) -> None:
        """Overrides inheritance for this transition.

        For internal use only.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::overrideInheritance()
        """
        raise NotImplementedError

    def resetLabelInheritance(self) -> "RPTransition":
        """Restores inheritance from the base statechart for the three components
        that make up the transition label: trigger, guard, and action.

        Returns:
            The transition on which the method was called.

        Raises:
            RhapsodyRuntimeException: If the inheritance cannot be reset.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::resetLabelInheritance()
        """
        raise NotImplementedError

    def setItsAction(self, action: str) -> "RPAction":
        """Sets the action for the transition.

        Args:
            action: The action to use for the transition, for example,
                "runStarter()".

        Returns:
            The action that was created.

        Raises:
            RhapsodyRuntimeException: If the action cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsAction(java.lang.String action)
        """
        raise NotImplementedError

    def setItsGuard(self, guard: str) -> "RPGuard":
        """Sets the guard for the transition.

        Args:
            guard: The guard to use for the transition, for example,
                "gear == 0".

        Returns:
            The guard that was created.

        Raises:
            RhapsodyRuntimeException: If the guard cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsGuard(java.lang.String guard)
        """
        raise NotImplementedError

    def setItsLabel(self, trigger: str, guard: str, action: str) -> None:
        """Sets the trigger, guard, and action for the transition.

        Args:
            trigger: The trigger to use for the transition — can be an event or
                triggered operation. If the string does not match an existing
                event or triggered operation, a new event with that name is
                created.
            guard: The guard to use for the transition, for example,
                "gear == 0".
            action: The action to use for the transition, for example,
                "runStarter()".

        Raises:
            RhapsodyRuntimeException: If the label cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsLabel(java.lang.String trigger, java.lang.String guard, java.lang.String action)
        """
        raise NotImplementedError

    def setItsSource(self, its_source: "RPStateVertex") -> None:
        """Sets the source of the transition.

        This method can only be used before ``createGraphics`` is called. Once
        the graphics have been created, the source cannot be changed.

        Args:
            its_source: The state that should be used as the source of the
                transition.

        Raises:
            RhapsodyRuntimeException: If the source cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsSource(com.telelogic.rhapsody.core.IRPStateVertex itsSource)
        """
        raise NotImplementedError

    def setItsStatechart(self, its_statechart: "RPStatechart") -> None:
        """Sets the statechart that the transition belongs to.

        For internal use only.

        Args:
            its_statechart: The statechart to set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsStatechart(com.telelogic.rhapsody.core.IRPStatechart itsStatechart)
        """
        raise NotImplementedError

    def setItsTarget(self, its_target: "RPStateVertex") -> None:
        """Sets the target of the transition.

        This method can only be used before ``createGraphics`` is called. Once
        the graphics have been created, the target cannot be changed.

        Args:
            its_target: The state that should be used as the target of the
                transition.

        Raises:
            RhapsodyRuntimeException: If the target cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsTarget(com.telelogic.rhapsody.core.IRPStateVertex itsTarget)
        """
        raise NotImplementedError

    def setItsTrigger(self, trigger: str) -> "RPTrigger":
        """Sets the trigger for the transition.

        Args:
            trigger: The trigger to use for the transition — can be an event or
                triggered operation. If the string does not match an existing
                event or triggered operation, a new event with that name is
                created.

        Returns:
            The trigger that was created.

        Raises:
            RhapsodyRuntimeException: If the trigger cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::setItsTrigger(java.lang.String trigger)
        """
        raise NotImplementedError

    def unoverrideInheritance(self) -> None:
        """Reverses the effect of overriding inheritance for this transition.

        For internal use only.

        Reference:
            com.telelogic.rhapsody.core.IRPTransition::unoverrideInheritance()
        """
        raise NotImplementedError


class RPTrigger(RPModelElement):
    """Wraps ``IRPTrigger``: represents the trigger of a transition in a statechart."""

    # IRPTrigger method parity checklist:
    # [ ] getBody                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsOperation              [ ] impl  [ ] docstring  [ ] test
    # [ ] isOperation                  [ ] impl  [ ] docstring  [ ] test
    # [ ] isTimeout                    [ ] impl  [ ] docstring  [ ] test
    # [ ] setBody                      [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPTrigger methods.

    def getBody(self) -> str:
        """Returns the body of this trigger.

        Returns:
            The trigger body text.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTrigger::getBody()
        """
        raise NotImplementedError

    def getItsOperation(self) -> "RPInterfaceItem":
        """Returns the operation associated with this trigger.

        Returns:
            The associated interface item (operation or event).

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTrigger::getItsOperation()
        """
        raise NotImplementedError

    def isOperation(self) -> int:
        """Checks whether this trigger is an operation trigger.

        Returns:
            1 if the trigger is an operation trigger, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTrigger::isOperation()
        """
        raise NotImplementedError

    def isTimeout(self) -> int:
        """Checks whether this trigger is a timeout trigger.

        Returns:
            1 if the trigger is a timeout trigger, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the property cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPTrigger::isTimeout()
        """
        raise NotImplementedError

    def setBody(self, body: str) -> None:
        """Sets the body of this trigger.

        Args:
            body: The trigger body text to set.

        Raises:
            RhapsodyRuntimeException: If the property cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPTrigger::setBody(java.lang.String body)
        """
        raise NotImplementedError


class RPDestructionEvent(RPMessage):
    """Wraps ``IRPDestructionEvent``: represents destruction events in sequence diagrams."""

    # IRPDestructionEvent method parity checklist:
    # [inherited] IRPMessage methods (covered by RPMessage checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPDestructionEvent methods.

    pass
