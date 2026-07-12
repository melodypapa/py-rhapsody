"""Activity model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.activity.model_actions import (
        RPAcceptEventAction,
        RPAcceptTimeEvent,
        RPCallOperation,
    )
    from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation
    from rhapsody_cli.models.elements.common.model_other_model import RPSysMLPort
    from rhapsody_cli.models.elements.diagrams.model_diagram_types import RPActivityDiagram
    from rhapsody_cli.models.elements.graphics.model_graphics import RPPin
    from rhapsody_cli.models.elements.relations.model_instance import RPInstance
    from rhapsody_cli.models.elements.relations.model_port import RPPort


class RPFlow(RPModelElement):
    """Wraps ``IRPFlow``."""

    # IRPFlow method parity checklist:
    # [ ] addConveyed                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getConveyed                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDirection                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd1                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd1Port                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd1SysMLPort             [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2Port                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2SysMLPort             [ ] impl  [ ] docstring  [ ] test
    # [ ] removeConveyed               [ ] impl  [ ] docstring  [ ] test
    # [ ] setDirection                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd1                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd1ViaPort               [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd1ViaSysMLPort          [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd2                      [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd2ViaPort               [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd2ViaSysMLPort          [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPFlow methods.

    def add_conveyed(self, p_element: "RPModelElement") -> None:
        """Adds a conveyed element to the flow.

        Args:
            p_element: The model element to add as conveyed.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::addConveyed(com.telelogic.rhapsody.core.IRPModelElement pElement)
        """
        raise NotImplementedError

    def get_conveyed(self) -> "RPCollection":
        """Returns the conveyed elements of the flow.

        Returns:
            RPCollection: The conveyed elements of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getConveyed()
        """
        raise NotImplementedError

    def get_direction(self) -> str:
        """Returns the direction of the flow.

        Returns:
            str: The direction of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getDirection()
        """
        raise NotImplementedError

    def get_end1(self) -> "RPModelElement":
        """Returns the first end of the flow.

        Returns:
            Any: The model element at the first end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd1()
        """
        raise NotImplementedError

    def get_end1_port(self) -> "RPPort":
        """Returns the port at the first end of the flow.

        Returns:
            Any: The port at the first end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd1Port()
        """
        raise NotImplementedError

    def get_end1_sys_ml_port(self) -> "RPSysMLPort":
        """Returns the SysML port at the first end of the flow.

        Returns:
            Any: The SysML port at the first end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd1SysMLPort()
        """
        raise NotImplementedError

    def get_end2(self) -> "RPModelElement":
        """Returns the second end of the flow.

        Returns:
            Any: The model element at the second end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd2()
        """
        raise NotImplementedError

    def get_end2_port(self) -> "RPPort":
        """Returns the port at the second end of the flow.

        Returns:
            Any: The port at the second end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd2Port()
        """
        raise NotImplementedError

    def get_end2_sys_ml_port(self) -> "RPSysMLPort":
        """Returns the SysML port at the second end of the flow.

        Returns:
            Any: The SysML port at the second end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::getEnd2SysMLPort()
        """
        raise NotImplementedError

    def remove_conveyed(self, p_element: "RPModelElement") -> None:
        """Removes a conveyed element from the flow.

        Args:
            p_element: The model element to remove from the conveyed collection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::removeConveyed(com.telelogic.rhapsody.core.IRPModelElement pElement)
        """
        raise NotImplementedError

    def set_direction(self, direction: str) -> None:
        """Specifies the direction to use for the flow.

        Args:
            direction: Can be one of the following values: "toEnd1", "toEnd2",
                "bidirectional".

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setDirection(java.lang.String direction)
        """
        raise NotImplementedError

    def set_end1(self, end1: "RPModelElement") -> None:
        """Sets the first end of the flow.

        Args:
            end1: The model element to set as the first end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd1(com.telelogic.rhapsody.core.IRPModelElement end1)
        """
        raise NotImplementedError

    def set_end1_via_port(self, p_instance: "RPInstance", p_port: "RPPort") -> None:
        """Sets the first end of the flow via a port.

        Args:
            p_instance: The instance to set as the first end of the flow.
            p_port: The port to use for the connection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd1ViaPort(com.telelogic.rhapsody.core.IRPInstance pInstance, com.telelogic.rhapsody.core.IRPPort pPort)
        """
        raise NotImplementedError

    def set_end1_via_sys_ml_port(self, p_instance: "RPInstance", p_sys_m_l_port: "RPSysMLPort") -> None:
        """Sets the first end of the flow via a SysML port.

        Args:
            p_instance: The instance to set as the first end of the flow.
            p_sys_m_l_port: The SysML port to use for the connection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd1ViaSysMLPort(com.telelogic.rhapsody.core.IRPInstance pInstance, com.telelogic.rhapsody.core.IRPSysMLPort pSysMLPort)
        """
        raise NotImplementedError

    def set_end2(self, end2: "RPModelElement") -> None:
        """Sets the second end of the flow.

        Args:
            end2: The model element to set as the second end of the flow.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd2(com.telelogic.rhapsody.core.IRPModelElement end2)
        """
        raise NotImplementedError

    def set_end2_via_port(self, p_instance: "RPInstance", p_port: "RPPort") -> None:
        """Sets the second end of the flow via a port.

        Args:
            p_instance: The instance to set as the second end of the flow.
            p_port: The port to use for the connection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd2ViaPort(com.telelogic.rhapsody.core.IRPInstance pInstance, com.telelogic.rhapsody.core.IRPPort pPort)
        """
        raise NotImplementedError

    def set_end2_via_sys_ml_port(self, p_instance: "RPInstance", p_sys_m_l_port: "RPSysMLPort") -> None:
        """Sets the second end of the flow via a SysML port.

        Args:
            p_instance: The instance to set as the second end of the flow.
            p_sys_m_l_port: The SysML port to use for the connection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPFlow::setEnd2ViaSysMLPort(com.telelogic.rhapsody.core.IRPInstance pInstance, com.telelogic.rhapsody.core.IRPSysMLPort pSysMLPort)
        """
        raise NotImplementedError


class RPFlowItem(RPClassifier):
    """Wraps ``IRPFlowItem``: represents item flows in Rhapsody models."""

    # IRPFlowItem method parity checklist:
    # [ ] addRepresented               [ ] impl  [ ] docstring  [ ] test
    # [ ] getRepresented               [ ] impl  [ ] docstring  [ ] test
    # [ ] removeRepresented            [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPFlowItem methods.

    def add_represented(self, p_element: "RPModelElement") -> None:
        """Adds an element to the collection of information elements that are represented by the item flow.

        Args:
            p_element: The element to add to the collection.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowItem::addRepresented(com.telelogic.rhapsody.core.IRPModelElement pElement)
        """
        raise NotImplementedError

    def get_represented(self) -> "RPCollection":
        """Returns a collection of all the information elements that are represented by the item flow.

        Returns:
            RPCollection: All the information elements that are represented by the item flow.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowItem::getRepresented()
        """
        raise NotImplementedError

    def remove_represented(self, p_element: "RPModelElement") -> None:
        """Removes the specified element from the collection of information elements that are represented by the item flow.

        Args:
            p_element: The element that should be removed from the collection.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowItem::removeRepresented(com.telelogic.rhapsody.core.IRPModelElement pElement)
        """
        raise NotImplementedError


class RPFlowchart(RPStatechart):
    """Wraps ``IRPFlowchart``: represents activities in Rhapsody models."""

    # IRPFlowchart method parity checklist:
    # [ ] addAcceptEventAction         [ ] impl  [ ] docstring  [ ] test
    # [ ] addAcceptTimeEvent           [ ] impl  [ ] docstring  [ ] test
    # [ ] addActivityParameter         [ ] impl  [ ] docstring  [ ] test
    # [ ] addCallBehavior              [ ] impl  [ ] docstring  [ ] test
    # [ ] addCallOperation             [ ] impl  [ ] docstring  [ ] test
    # [ ] addObjectNode                [ ] impl  [ ] docstring  [ ] test
    # [ ] addReferenceActivity         [ ] impl  [ ] docstring  [ ] test
    # [ ] addSwimlane                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFlowchartDiagram          [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsAnalysisOnly            [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsOwner                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getSwimlanes                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsAnalysisOnly            [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsOwner                  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClass methods (covered by RPClass checklist)
    # [inherited] IRPClassifier methods (covered by RPClassifier checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPStatechart methods (covered by RPStatechart checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # [deprecated] getItsOwner  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] setItsOwner  - skipped (deprecated in Rhapsody Java API)
    # No non-deprecated IRPFlowchart methods.

    def add_accept_event_action(self, name: str, parent: "RPState") -> "RPAcceptEventAction":
        """Adds a new Accept Event Action element to the activity.

        Args:
            name: The name to use for the new Accept Event Action element.
            parent: The diagram element to which the new Accept Event Action
                element should be added. If the Accept Event Action element is
                being added to an Action Block, this parameter should be the
                Action Block. Otherwise, it should be the root state of the
                diagram (which is obtained by calling
                IRPStatechart.getRootState()).

        Returns:
            Any: The Accept Event Action element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addAcceptEventAction(java.lang.String name, com.telelogic.rhapsody.core.IRPState parent)
        """
        raise NotImplementedError

    def add_accept_time_event(self, name: str, parent: "RPState") -> "RPAcceptTimeEvent":
        """Adds a new Accept Time Event element to the activity.

        Args:
            name: The name to use for the new Accept Time Event element.
            parent: The diagram element to which the new Accept Time Event
                element should be added. If the Accept Time Event element is
                being added to an Action Block, this parameter should be the
                Action Block. Otherwise, it should be the root state of the
                diagram (which is obtained by calling
                IRPStatechart.getRootState()).

        Returns:
            Any: The Accept Time Event element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addAcceptTimeEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPState parent)
        """
        raise NotImplementedError

    def add_activity_parameter(self, name: str) -> "RPPin":
        """Adds an activity parameter to the frame of the activity.

        Args:
            name: The name to use for the new activity parameter.

        Returns:
            Any: The activity parameter element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addActivityParameter(java.lang.String name)
        """
        raise NotImplementedError

    def add_call_behavior(self, referenced: "RPModelElement") -> "RPState":
        """Adds a new Call Behavior element to the activity.

        Args:
            referenced: The activity that the new Call Behavior element should
                invoke.

        Returns:
            Any: The Call Behavior element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addCallBehavior(com.telelogic.rhapsody.core.IRPModelElement referenced)
        """
        raise NotImplementedError

    def add_call_operation(self, name: str, parent: "RPState") -> "RPCallOperation":
        """Adds a new Call Operation element to the activity.

        Args:
            name: The name to use for the new Call Operation element.
            parent: The diagram element to which the new Call Operation element
                should be added. If the Call Operation element is being added to
                an Action Block, this parameter should be the Action Block.
                Otherwise, it should be the root state of the diagram (which is
                obtained by calling IRPStatechart.getRootState()).

        Returns:
            Any: The Call Operation element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addCallOperation(java.lang.String name, com.telelogic.rhapsody.core.IRPState parent)
        """
        raise NotImplementedError

    def add_object_node(self, name: str, parent: "RPState") -> "RPObjectNode":
        """Adds a new Object Node element to the activity.

        Args:
            name: The name to use for the new Object Node element.
            parent: The diagram element to which the new Object Node element
                should be added. If the Object Node element is being added to an
                Action Block, this parameter should be the Action Block.
                Otherwise, it should be the root state of the diagram (which is
                obtained by calling IRPStatechart.getRootState()).

        Returns:
            Any: The Object Node element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addObjectNode(java.lang.String name, com.telelogic.rhapsody.core.IRPState parent)
        """
        raise NotImplementedError

    def add_reference_activity(self, referenced: "RPModelElement") -> "RPState":
        """Adds a new Call Behavior element to the activity. Performs same action as the addCallBehavior method.

        Args:
            referenced: The activity that the new Call Behavior element should
                invoke.

        Returns:
            Any: The Call Behavior element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addReferenceActivity(com.telelogic.rhapsody.core.IRPModelElement referenced)
        """
        raise NotImplementedError

    def add_swimlane(self, name: str) -> "RPSwimlane":
        """Adds a new swimlane to the activity.

        Args:
            name: The name to use for the new swimlane.

        Returns:
            Any: The swimlane that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::addSwimlane(java.lang.String name)
        """
        raise NotImplementedError

    def get_flowchart_diagram(self) -> "RPActivityDiagram":
        """Returns the IRPActivityDiagram object associated with the activity.

        Returns:
            Any: The IRPActivityDiagram object associated with the activity.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::getFlowchartDiagram()
        """
        raise NotImplementedError

    def get_is_analysis_only(self) -> int:
        """Checks whether the activity is defined as analysis-only, meaning that it is used only for modeling purposes and code is not generated for the activity.

        Returns:
            int: 1 if the activity is defined as analysis-only, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::getIsAnalysisOnly()
        """
        raise NotImplementedError

    def get_its_owner(self) -> "RPOperation":
        """Returns the operation that owns the activity. Deprecated: use IRPModelElement.getOwner instead.

        Returns:
            Any: The operation that owns the activity.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::getItsOwner()
        """
        raise NotImplementedError

    def get_swimlanes(self) -> "RPCollection":
        """Returns a collection of all the swimlanes in the activity.

        Returns:
            RPCollection: Collection of IRPSwimlane objects.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::getSwimlanes()
        """
        raise NotImplementedError

    def set_is_analysis_only(self, is_analysis_only: int) -> None:
        """Specifies whether the activity should be defined as analysis-only.

        Args:
            is_analysis_only: Use 1 to specify that the activity should be
                defined as analysis-only. Use 0 to specify that the activity
                should not be defined as analysis-only.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::setIsAnalysisOnly(int isAnalysisOnly)
        """
        raise NotImplementedError

    def set_its_owner(self, its_owner: "RPOperation") -> None:
        """Sets the owner of the activity. Deprecated: use IRPModelElement.setOwner instead.

        Args:
            its_owner: The operation that should own the activity.

        Reference:
            com.telelogic.rhapsody.core.IRPFlowchart::setItsOwner(com.telelogic.rhapsody.core.IRPOperation itsOwner)
        """
        raise NotImplementedError


class RPObjectNode(RPState):
    """Wraps ``IRPObjectNode``: represents Object Node elements in activity diagrams."""

    # IRPObjectNode method parity checklist:
    # [ ] addInState                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getInState                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getInStateList               [ ] impl  [ ] docstring  [ ] test
    # [ ] getRepresents                [ ] impl  [ ] docstring  [ ] test
    # [ ] removeInState                [ ] impl  [ ] docstring  [ ] test
    # [ ] setInState                   [ ] impl  [ ] docstring  [ ] test
    # [ ] setRepresents                [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPState methods (covered by RPState checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # [deprecated] getInState  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] setInState  - skipped (deprecated in Rhapsody Java API)
    # No non-deprecated IRPObjectNode methods.

    def add_in_state(self, val: "RPModelElement") -> None:
        """Adds the specified state to the list of "In State" states for the object node.

        Args:
            val: The state to add to the list of "In State" states.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::addInState(com.telelogic.rhapsody.core.IRPModelElement val)
        """
        raise NotImplementedError

    def get_in_state(self) -> str:
        """Returns the "In State" of the object node. Deprecated: use getInStateList() instead.

        Returns:
            str: The "In State" of the object node.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::getInState()
        """
        raise NotImplementedError

    def get_in_state_list(self) -> "RPCollection":
        """Returns a collection of the "In State" states for the object node.

        Returns:
            RPCollection: The "In State" states defined for the object node.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::getInStateList()
        """
        raise NotImplementedError

    def get_represents(self) -> "RPModelElement":
        """Returns the class/type that this object node represents.

        Returns:
            Any: The class/type that this object node represents.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::getRepresents()
        """
        raise NotImplementedError

    def remove_in_state(self, val: "RPModelElement") -> None:
        """Removes the specified state from the list of "In State" states for the object node.

        Args:
            val: The state to remove from the list.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::removeInState(com.telelogic.rhapsody.core.IRPModelElement val)
        """
        raise NotImplementedError

    def set_in_state(self, in_state: str) -> None:
        """Sets the "In State" of the object node. Deprecated: use addInState instead.

        Args:
            in_state: The "In State" value to set.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::setInState(java.lang.String inState)
        """
        raise NotImplementedError

    def set_represents(self, represents: "RPModelElement") -> None:
        """Specifies the class/type that this object node should represent.

        Args:
            represents: The class/type that this object node should represent.

        Reference:
            com.telelogic.rhapsody.core.IRPObjectNode::setRepresents(com.telelogic.rhapsody.core.IRPModelElement represents)
        """
        raise NotImplementedError


class RPSwimlane(RPModelElement):
    """Wraps ``IRPSwimlane``: represents swimlanes in an activity diagram."""

    # IRPSwimlane method parity checklist:
    # [ ] addSwimlane                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getContents                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRepresents                [ ] impl  [ ] docstring  [ ] test
    # [ ] getSwimlanes                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setRepresents                [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPSwimlane methods.

    def add_swimlane(self, name: str) -> "RPSwimlane":
        """For internal use only.

        Args:
            name: The name to use for the new swimlane.

        Returns:
            Any: The swimlane that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPSwimlane::addSwimlane(java.lang.String name)
        """
        raise NotImplementedError

    def get_contents(self) -> "RPCollection":
        """Returns a collection of the elements contained in the swimlane.

        Returns:
            RPCollection: The elements contained in the swimlane.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSwimlane::getContents()
        """
        raise NotImplementedError

    def get_represents(self) -> "RPModelElement":
        """Returns the model element that the swimlane represents.

        Returns:
            Any: The model element that the swimlane represents.

        Reference:
            com.telelogic.rhapsody.core.IRPSwimlane::getRepresents()
        """
        raise NotImplementedError

    def get_swimlanes(self) -> "RPCollection":
        """Returns a collection of the swimlanes that are nested under this swimlane.

        Returns:
            RPCollection: The swimlanes nested under this swimlane.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSwimlane::getSwimlanes()
        """
        raise NotImplementedError

    def set_represents(self, represents: "RPModelElement") -> None:
        """Specifies the model element that the swimlane is to represent.

        Args:
            represents: The model element that the swimlane is to represent.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSwimlane::setRepresents(com.telelogic.rhapsody.core.IRPModelElement represents)
        """
        raise NotImplementedError
