"""Tests for rhapsody_cli.models.elements.activity.model_activity flowchart classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.activity.model_activity import (
    RPFlow,
    RPFlowItem,
    RPFlowchart,
    RPObjectNode,
    RPSwimlane,
)
from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPFlow:
    """Tests for RPFlow (17 methods)."""

    def test_is_model_element(self) -> None:
        fake = make_fake_element("Flow", getName="MyFlow")
        flow = RPFlow(fake)
        assert isinstance(flow, RPModelElement)
        assert flow.get_name() == "MyFlow"

    def test_add_conveyed_delegates(self) -> None:
        fake = make_fake_element("Flow")
        element = make_fake_element("Class", getName="ConveyedClass")
        flow = RPFlow(fake)
        flow.add_conveyed(AbstractRPModelElement.wrap(element))
        fake.addConveyed.assert_called_once_with(element)

    def test_get_conveyed_returns_collection(self) -> None:
        fake = make_fake_element("Flow")
        item1 = make_fake_element("Class", getName="Item1")
        item2 = make_fake_element("Class", getName="Item2")
        fake.getConveyed.return_value = make_fake_collection([item1, item2])
        flow = RPFlow(fake)
        result = flow.get_conveyed()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getConveyed.assert_called_once_with()

    def test_get_direction_returns_string(self) -> None:
        fake = make_fake_element("Flow", getDirection="toEnd2")
        flow = RPFlow(fake)
        assert flow.get_direction() == "toEnd2"
        fake.getDirection.assert_called_once_with()

    def test_get_end1_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        end1 = make_fake_element("State", getName="End1State")
        fake.getEnd1.return_value = end1
        flow = RPFlow(fake)
        result = flow.get_end1()
        assert result.get_name() == "End1State"
        fake.getEnd1.assert_called_once_with()

    def test_get_end1_port_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        port = make_fake_element("Port", getName="Port1")
        fake.getEnd1Port.return_value = port
        flow = RPFlow(fake)
        result = flow.get_end1_port()
        assert result.get_name() == "Port1"
        fake.getEnd1Port.assert_called_once_with()

    def test_get_end1_sys_ml_port_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        sysml_port = make_fake_element("SysMLPort", getName="SysMLPort1")
        fake.getEnd1SysMLPort.return_value = sysml_port
        flow = RPFlow(fake)
        result = flow.get_end1_sys_ml_port()
        assert result.get_name() == "SysMLPort1"
        fake.getEnd1SysMLPort.assert_called_once_with()

    def test_get_end2_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        end2 = make_fake_element("State", getName="End2State")
        fake.getEnd2.return_value = end2
        flow = RPFlow(fake)
        result = flow.get_end2()
        assert result.get_name() == "End2State"
        fake.getEnd2.assert_called_once_with()

    def test_get_end2_port_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        port = make_fake_element("Port", getName="Port2")
        fake.getEnd2Port.return_value = port
        flow = RPFlow(fake)
        result = flow.get_end2_port()
        assert result.get_name() == "Port2"
        fake.getEnd2Port.assert_called_once_with()

    def test_get_end2_sys_ml_port_wraps_result(self) -> None:
        fake = make_fake_element("Flow")
        sysml_port = make_fake_element("SysMLPort", getName="SysMLPort2")
        fake.getEnd2SysMLPort.return_value = sysml_port
        flow = RPFlow(fake)
        result = flow.get_end2_sys_ml_port()
        assert result.get_name() == "SysMLPort2"
        fake.getEnd2SysMLPort.assert_called_once_with()

    def test_remove_conveyed_delegates(self) -> None:
        fake = make_fake_element("Flow")
        element = make_fake_element("Class", getName="ConveyedClass")
        flow = RPFlow(fake)
        flow.remove_conveyed(AbstractRPModelElement.wrap(element))
        fake.removeConveyed.assert_called_once_with(element)

    def test_set_direction_delegates(self) -> None:
        fake = make_fake_element("Flow")
        flow = RPFlow(fake)
        flow.set_direction("bidirectional")
        fake.setDirection.assert_called_once_with("bidirectional")

    def test_set_end1_delegates(self) -> None:
        fake = make_fake_element("Flow")
        end1 = make_fake_element("State", getName="End1State")
        flow = RPFlow(fake)
        flow.set_end1(AbstractRPModelElement.wrap(end1))
        fake.setEnd1.assert_called_once_with(end1)

    def test_set_end1_via_port_delegates(self) -> None:
        fake = make_fake_element("Flow")
        instance = make_fake_element("Instance", getName="MyInstance")
        port = make_fake_element("Port", getName="MyPort")
        flow = RPFlow(fake)
        flow.set_end1_via_port(AbstractRPModelElement.wrap(instance), AbstractRPModelElement.wrap(port))
        fake.setEnd1ViaPort.assert_called_once_with(instance, port)

    def test_set_end1_via_sys_ml_port_delegates(self) -> None:
        fake = make_fake_element("Flow")
        instance = make_fake_element("Instance", getName="MyInstance")
        sysml_port = make_fake_element("SysMLPort", getName="MySysMLPort")
        flow = RPFlow(fake)
        flow.set_end1_via_sys_ml_port(AbstractRPModelElement.wrap(instance), AbstractRPModelElement.wrap(sysml_port))
        fake.setEnd1ViaSysMLPort.assert_called_once_with(instance, sysml_port)

    def test_set_end2_delegates(self) -> None:
        fake = make_fake_element("Flow")
        end2 = make_fake_element("State", getName="End2State")
        flow = RPFlow(fake)
        flow.set_end2(AbstractRPModelElement.wrap(end2))
        fake.setEnd2.assert_called_once_with(end2)

    def test_set_end2_via_port_delegates(self) -> None:
        fake = make_fake_element("Flow")
        instance = make_fake_element("Instance", getName="MyInstance")
        port = make_fake_element("Port", getName="MyPort")
        flow = RPFlow(fake)
        flow.set_end2_via_port(AbstractRPModelElement.wrap(instance), AbstractRPModelElement.wrap(port))
        fake.setEnd2ViaPort.assert_called_once_with(instance, port)

    def test_set_end2_via_sys_ml_port_delegates(self) -> None:
        fake = make_fake_element("Flow")
        instance = make_fake_element("Instance", getName="MyInstance")
        sysml_port = make_fake_element("SysMLPort", getName="MySysMLPort")
        flow = RPFlow(fake)
        flow.set_end2_via_sys_ml_port(AbstractRPModelElement.wrap(instance), AbstractRPModelElement.wrap(sysml_port))
        fake.setEnd2ViaSysMLPort.assert_called_once_with(instance, sysml_port)

    def test_is_registered_for_meta_class_flow(self) -> None:
        fake = make_fake_element("Flow", getName="MyFlow")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlow)


class TestRPFlowItem:
    """Tests for RPFlowItem (3 methods)."""

    def test_is_classifier(self) -> None:
        fake = make_fake_element("FlowItem", getName="MyFlowItem")
        flow_item = RPFlowItem(fake)
        assert isinstance(flow_item, RPModelElement)
        assert flow_item.get_name() == "MyFlowItem"

    def test_add_represented_delegates(self) -> None:
        fake = make_fake_element("FlowItem")
        element = make_fake_element("Class", getName="RepresentedClass")
        flow_item = RPFlowItem(fake)
        flow_item.add_represented(AbstractRPModelElement.wrap(element))
        fake.addRepresented.assert_called_once_with(element)

    def test_get_represented_returns_collection(self) -> None:
        fake = make_fake_element("FlowItem")
        item1 = make_fake_element("Class", getName="Rep1")
        item2 = make_fake_element("Class", getName="Rep2")
        fake.getRepresented.return_value = make_fake_collection([item1, item2])
        flow_item = RPFlowItem(fake)
        result = flow_item.get_represented()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getRepresented.assert_called_once_with()

    def test_remove_represented_delegates(self) -> None:
        fake = make_fake_element("FlowItem")
        element = make_fake_element("Class", getName="RepresentedClass")
        flow_item = RPFlowItem(fake)
        flow_item.remove_represented(AbstractRPModelElement.wrap(element))
        fake.removeRepresented.assert_called_once_with(element)

    def test_is_registered_for_meta_class_flow_item(self) -> None:
        fake = make_fake_element("FlowItem", getName="MyFlowItem")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlowItem)


class TestRPFlowchart:
    """Tests for RPFlowchart (15 methods)."""

    def test_is_statechart(self) -> None:
        fake = make_fake_element("Flowchart", getName="MyActivity")
        flowchart = RPFlowchart(fake)
        assert isinstance(flowchart, RPStatechart)
        assert flowchart.get_name() == "MyActivity"

    def test_add_accept_event_action_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        parent = make_fake_element("State", getName="RootState")
        aea = make_fake_element("AcceptEventAction", getName="AEA1")
        fake.addAcceptEventAction.return_value = aea
        flowchart = RPFlowchart(fake)
        result = flowchart.add_accept_event_action("AEA1", RPState(parent))
        assert result.get_name() == "AEA1"
        fake.addAcceptEventAction.assert_called_once_with("AEA1", parent)

    def test_add_accept_time_event_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        parent = make_fake_element("State", getName="RootState")
        ate = make_fake_element("AcceptTimeEvent", getName="ATE1")
        fake.addAcceptTimeEvent.return_value = ate
        flowchart = RPFlowchart(fake)
        result = flowchart.add_accept_time_event("ATE1", RPState(parent))
        assert result.get_name() == "ATE1"
        fake.addAcceptTimeEvent.assert_called_once_with("ATE1", parent)

    def test_add_activity_parameter_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        pin = make_fake_element("Pin", getName="Param1")
        fake.addActivityParameter.return_value = pin
        flowchart = RPFlowchart(fake)
        result = flowchart.add_activity_parameter("Param1")
        assert result.get_name() == "Param1"
        fake.addActivityParameter.assert_called_once_with("Param1")

    def test_add_call_behavior_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        referenced = make_fake_element("Flowchart", getName="ReferencedActivity")
        state = make_fake_element("State", getName="CallBehaviorState")
        fake.addCallBehavior.return_value = state
        flowchart = RPFlowchart(fake)
        result = flowchart.add_call_behavior(AbstractRPModelElement.wrap(referenced))
        assert result.get_name() == "CallBehaviorState"
        fake.addCallBehavior.assert_called_once_with(referenced)

    def test_add_call_operation_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        parent = make_fake_element("State", getName="RootState")
        co = make_fake_element("CallOperation", getName="CO1")
        fake.addCallOperation.return_value = co
        flowchart = RPFlowchart(fake)
        result = flowchart.add_call_operation("CO1", RPState(parent))
        assert result.get_name() == "CO1"
        fake.addCallOperation.assert_called_once_with("CO1", parent)

    def test_add_object_node_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        parent = make_fake_element("State", getName="RootState")
        node = make_fake_element("ObjectNode", getName="ObjectNode1")
        fake.addObjectNode.return_value = node
        flowchart = RPFlowchart(fake)
        result = flowchart.add_object_node("ObjectNode1", RPState(parent))
        assert result.get_name() == "ObjectNode1"
        fake.addObjectNode.assert_called_once_with("ObjectNode1", parent)

    def test_add_reference_activity_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        referenced = make_fake_element("Flowchart", getName="ReferencedActivity")
        state = make_fake_element("State", getName="RefActivityState")
        fake.addReferenceActivity.return_value = state
        flowchart = RPFlowchart(fake)
        result = flowchart.add_reference_activity(AbstractRPModelElement.wrap(referenced))
        assert result.get_name() == "RefActivityState"
        fake.addReferenceActivity.assert_called_once_with(referenced)

    def test_add_swimlane_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        swimlane = make_fake_element("Swimlane", getName="Lane1")
        fake.addSwimlane.return_value = swimlane
        flowchart = RPFlowchart(fake)
        result = flowchart.add_swimlane("Lane1")
        assert result.get_name() == "Lane1"
        fake.addSwimlane.assert_called_once_with("Lane1")

    def test_get_flowchart_diagram_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        diagram = make_fake_element("ActivityDiagram", getName="ActivityDiagram1")
        fake.getFlowchartDiagram.return_value = diagram
        flowchart = RPFlowchart(fake)
        result = flowchart.get_flowchart_diagram()
        assert result.get_name() == "ActivityDiagram1"
        fake.getFlowchartDiagram.assert_called_once_with()

    def test_get_is_analysis_only_returns_int(self) -> None:
        fake = make_fake_element("Flowchart", getIsAnalysisOnly=1)
        flowchart = RPFlowchart(fake)
        assert flowchart.get_is_analysis_only() == 1
        fake.getIsAnalysisOnly.assert_called_once_with()

    def test_get_its_owner_wraps_result(self) -> None:
        fake = make_fake_element("Flowchart")
        owner = make_fake_element("Operation", getName="myOperation")
        fake.getItsOwner.return_value = owner
        flowchart = RPFlowchart(fake)
        result = flowchart.get_its_owner()
        assert result.get_name() == "myOperation"
        fake.getItsOwner.assert_called_once_with()

    def test_get_swimlanes_returns_collection(self) -> None:
        fake = make_fake_element("Flowchart")
        lane1 = make_fake_element("Swimlane", getName="Lane1")
        lane2 = make_fake_element("Swimlane", getName="Lane2")
        fake.getSwimlanes.return_value = make_fake_collection([lane1, lane2])
        flowchart = RPFlowchart(fake)
        result = flowchart.get_swimlanes()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getSwimlanes.assert_called_once_with()

    def test_set_is_analysis_only_delegates(self) -> None:
        fake = make_fake_element("Flowchart")
        flowchart = RPFlowchart(fake)
        flowchart.set_is_analysis_only(1)
        fake.setIsAnalysisOnly.assert_called_once_with(1)

    def test_set_its_owner_delegates(self) -> None:
        fake = make_fake_element("Flowchart")
        owner = make_fake_element("Operation", getName="myOperation")
        flowchart = RPFlowchart(fake)
        flowchart.set_its_owner(AbstractRPModelElement.wrap(owner))
        fake.setItsOwner.assert_called_once_with(owner)

    def test_is_registered_for_meta_class_flowchart(self) -> None:
        fake = make_fake_element("Flowchart", getName="MyActivity")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlowchart)


class TestRPObjectNode:
    """Tests for RPObjectNode (7 methods)."""

    def test_is_state(self) -> None:
        fake = make_fake_element("ObjectNode", getName="MyObjectNode")
        node = RPObjectNode(fake)
        assert isinstance(node, RPState)
        assert node.get_name() == "MyObjectNode"

    def test_add_in_state_delegates(self) -> None:
        fake = make_fake_element("ObjectNode")
        state = make_fake_element("State", getName="InStateValue")
        node = RPObjectNode(fake)
        node.add_in_state(AbstractRPModelElement.wrap(state))
        fake.addInState.assert_called_once_with(state)

    def test_get_in_state_returns_string(self) -> None:
        fake = make_fake_element("ObjectNode", getInState="SomeState")
        node = RPObjectNode(fake)
        assert node.get_in_state() == "SomeState"
        fake.getInState.assert_called_once_with()

    def test_get_in_state_list_returns_collection(self) -> None:
        fake = make_fake_element("ObjectNode")
        state1 = make_fake_element("State", getName="State1")
        state2 = make_fake_element("State", getName="State2")
        fake.getInStateList.return_value = make_fake_collection([state1, state2])
        node = RPObjectNode(fake)
        result = node.get_in_state_list()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getInStateList.assert_called_once_with()

    def test_get_represents_wraps_result(self) -> None:
        fake = make_fake_element("ObjectNode")
        represents = make_fake_element("Class", getName="MyClass")
        fake.getRepresents.return_value = represents
        node = RPObjectNode(fake)
        result = node.get_represents()
        assert result.get_name() == "MyClass"
        fake.getRepresents.assert_called_once_with()

    def test_remove_in_state_delegates(self) -> None:
        fake = make_fake_element("ObjectNode")
        state = make_fake_element("State", getName="InStateValue")
        node = RPObjectNode(fake)
        node.remove_in_state(AbstractRPModelElement.wrap(state))
        fake.removeInState.assert_called_once_with(state)

    def test_set_in_state_delegates(self) -> None:
        fake = make_fake_element("ObjectNode")
        node = RPObjectNode(fake)
        node.set_in_state("SomeState")
        fake.setInState.assert_called_once_with("SomeState")

    def test_set_represents_delegates(self) -> None:
        fake = make_fake_element("ObjectNode")
        represents = make_fake_element("Class", getName="MyClass")
        node = RPObjectNode(fake)
        node.set_represents(AbstractRPModelElement.wrap(represents))
        fake.setRepresents.assert_called_once_with(represents)

    def test_is_registered_for_meta_class_object_node(self) -> None:
        fake = make_fake_element("ObjectNode", getName="MyObjectNode")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPObjectNode)


class TestRPSwimlane:
    """Tests for RPSwimlane (5 methods - note: addSwimlane + getSwimlanes = 5 total)."""

    def test_is_model_element(self) -> None:
        fake = make_fake_element("Swimlane", getName="MySwimlane")
        swimlane = RPSwimlane(fake)
        assert isinstance(swimlane, RPModelElement)
        assert swimlane.get_name() == "MySwimlane"

    def test_add_swimlane_wraps_result(self) -> None:
        fake = make_fake_element("Swimlane")
        nested = make_fake_element("Swimlane", getName="NestedLane")
        fake.addSwimlane.return_value = nested
        swimlane = RPSwimlane(fake)
        result = swimlane.add_swimlane("NestedLane")
        assert result.get_name() == "NestedLane"
        fake.addSwimlane.assert_called_once_with("NestedLane")

    def test_get_contents_returns_collection(self) -> None:
        fake = make_fake_element("Swimlane")
        item1 = make_fake_element("State", getName="Content1")
        item2 = make_fake_element("State", getName="Content2")
        fake.getContents.return_value = make_fake_collection([item1, item2])
        swimlane = RPSwimlane(fake)
        result = swimlane.get_contents()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getContents.assert_called_once_with()

    def test_get_represents_wraps_result(self) -> None:
        fake = make_fake_element("Swimlane")
        represents = make_fake_element("Class", getName="MyClass")
        fake.getRepresents.return_value = represents
        swimlane = RPSwimlane(fake)
        result = swimlane.get_represents()
        assert result.get_name() == "MyClass"
        fake.getRepresents.assert_called_once_with()

    def test_get_swimlanes_returns_collection(self) -> None:
        fake = make_fake_element("Swimlane")
        lane1 = make_fake_element("Swimlane", getName="NestedLane1")
        lane2 = make_fake_element("Swimlane", getName="NestedLane2")
        fake.getSwimlanes.return_value = make_fake_collection([lane1, lane2])
        swimlane = RPSwimlane(fake)
        result = swimlane.get_swimlanes()
        assert isinstance(result, RPCollection)
        assert len(result) == 2
        fake.getSwimlanes.assert_called_once_with()

    def test_set_represents_delegates(self) -> None:
        fake = make_fake_element("Swimlane")
        represents = make_fake_element("Class", getName="MyClass")
        swimlane = RPSwimlane(fake)
        swimlane.set_represents(AbstractRPModelElement.wrap(represents))
        fake.setRepresents.assert_called_once_with(represents)

    def test_is_registered_for_meta_class_swimlane(self) -> None:
        fake = make_fake_element("Swimlane", getName="MySwimlane")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSwimlane)