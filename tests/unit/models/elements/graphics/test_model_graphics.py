"""Tests for graphics package — RPGraphElement, RPGraphEdge, and 12 other classes (Task 15)."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.graphics import (
    RPConditionMark,
    RPConnector,
    RPGraphEdge,
    RPGraphElement,
    RPGraphicalProperty,
    RPGraphNode,
    RPImageMap,
    RPLink,
    RPMatrixLayout,
    RPMatrixView,
    RPMessagePoint,
    RPPin,
    RPTableLayout,
    RPTableView,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPGraphElementTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphElement", getName="ge1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphElement)

    def test_get_interface_name_returns_str(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("GraphElement")
        fake.getInterfaceName.return_value = "IFoo"
        ge = RPGraphElement(fake)
        assert ge.get_interface_name() == "IFoo"
        fake.getInterfaceName.assert_called_once_with()

    def test_get_model_object_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphElement")
        model_obj = make_fake_element("Class", getName="Widget")
        fake.getModelObject.return_value = model_obj
        ge = RPGraphElement(fake)
        wrapped = ge.get_model_object()
        assert wrapped.get_name() == "Widget"
        fake.getModelObject.assert_called_once_with()

    def test_get_all_graphical_properties_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning collection
        fake = make_fake_element("GraphElement")
        prop = make_fake_element("GraphicalProperty", getName="p1")
        fake.getAllGraphicalProperties.return_value = make_fake_collection([prop])
        ge = RPGraphElement(fake)
        result = ge.get_all_graphical_properties()
        assert isinstance(result, RPCollection)
        fake.getAllGraphicalProperties.assert_called_once_with()

    def test_set_associated_image_delegates(self) -> None:
        # Pattern D — single-arg setter (str)
        fake = make_fake_element("GraphElement")
        fake.setAssociatedImage.return_value = None
        ge = RPGraphElement(fake)
        ge.set_associated_image("img.png")
        fake.setAssociatedImage.assert_called_once_with("img.png")

    def test_add_property_delegates(self) -> None:
        # Pattern F — multi-arg void method (3 str args)
        fake = make_fake_element("GraphElement")
        fake.addProperty.return_value = None
        ge = RPGraphElement(fake)
        ge.add_property("key", "type", "value")
        fake.addProperty.assert_called_once_with("key", "type", "value")

    def test_get_graphical_property_uses_call_com_directly(self) -> None:
        # Parameterized getter — must use call_com (not _get_method_or_property)
        fake = make_fake_element("GraphElement")
        prop = make_fake_element("GraphicalProperty", getName="FillColor")
        fake.getGraphicalProperty.return_value = prop
        ge = RPGraphElement(fake)
        wrapped = ge.get_graphical_property("FillColor")
        assert wrapped.get_name() == "FillColor"
        fake.getGraphicalProperty.assert_called_once_with("FillColor")

    def test_remove_property_delegates(self) -> None:
        # Pattern F — single-arg void method (str)
        fake = make_fake_element("GraphElement")
        fake.removeProperty.return_value = None
        ge = RPGraphElement(fake)
        ge.remove_property("key")
        fake.removeProperty.assert_called_once_with("key")

    def test_get_diagram_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphElement")
        diagram = make_fake_element("ObjectModelDiagram", getName="Diagram1")
        fake.getDiagram.return_value = diagram
        ge = RPGraphElement(fake)
        wrapped = ge.get_diagram()
        assert wrapped.get_name() == "Diagram1"
        fake.getDiagram.assert_called_once_with()

    def test_get_graphical_parent_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphElement")
        parent = make_fake_element("GraphNode", getName="Parent")
        fake.getGraphicalParent.return_value = parent
        ge = RPGraphElement(fake)
        wrapped = ge.get_graphical_parent()
        assert wrapped.get_name() == "Parent"
        fake.getGraphicalParent.assert_called_once_with()

    def test_get_property_value_parameterized(self) -> None:
        # Parameterized getter — must use call_com
        fake = make_fake_element("GraphElement")
        fake.getPropertyValue.return_value = "someValue"
        ge = RPGraphElement(fake)
        result = ge.get_property_value("myKey")
        assert result == "someValue"
        fake.getPropertyValue.assert_called_once_with("myKey")

    def test_set_property_value_parameterized(self) -> None:
        # Parameterized setter — must use call_com
        fake = make_fake_element("GraphElement")
        fake.setPropertyValue.return_value = None
        ge = RPGraphElement(fake)
        ge.set_property_value("key", "value")
        fake.setPropertyValue.assert_called_once_with("key", "value")


class TestRPGraphEdgeTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphEdge", getName="edge1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphEdge)

    def test_is_graph_element(self) -> None:
        # RPGraphEdge extends RPGraphElement
        fake = make_fake_element("GraphEdge", getName="edge1")
        edge = RPGraphEdge(fake)
        assert isinstance(edge, RPGraphElement)

    def test_get_source_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphEdge")
        src = make_fake_element("GraphNode", getName="src")
        fake.getSource.return_value = src
        edge = RPGraphEdge(fake)
        wrapped = edge.get_source()
        assert wrapped.get_name() == "src"
        fake.getSource.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("GraphEdge")
        tgt = make_fake_element("GraphNode", getName="tgt")
        fake.getTarget.return_value = tgt
        edge = RPGraphEdge(fake)
        wrapped = edge.get_target()
        assert wrapped.get_name() == "tgt"
        fake.getTarget.assert_called_once_with()

    def test_embed_new_flow_returns_self(self) -> None:
        # Pattern E — no-arg method returning wrapped element (self)
        fake = make_fake_element("GraphEdge")
        fake.embedNewFlow.return_value = fake  # returns the same edge
        edge = RPGraphEdge(fake)
        result = edge.embed_new_flow()
        fake.embedNewFlow.assert_called_once_with()
        assert result is not None

    def test_get_containing_arrow_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("GraphEdge")
        arrow = make_fake_element("GraphEdge", getName="arrow")
        fake.getContainingArrow.return_value = arrow
        edge = RPGraphEdge(fake)
        wrapped = edge.get_containing_arrow()
        assert wrapped.get_name() == "arrow"
        fake.getContainingArrow.assert_called_once_with()


class TestRPGraphNodeTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphNode", getName="node1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphNode)

    def test_is_graph_element(self) -> None:
        fake = make_fake_element("GraphNode", getName="node1")
        node = RPGraphNode(fake)
        assert isinstance(node, RPGraphElement)

    def test_bring_to_front_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("GraphNode")
        fake.bringToFront.return_value = None
        node = RPGraphNode(fake)
        node.bring_to_front()
        fake.bringToFront.assert_called_once_with()

    def test_send_to_back_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("GraphNode")
        fake.sendToBack.return_value = None
        node = RPGraphNode(fake)
        node.send_to_back()
        fake.sendToBack.assert_called_once_with()

    def test_hide_all_ports_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("GraphNode")
        fake.hideAllPorts.return_value = None
        node = RPGraphNode(fake)
        node.hide_all_ports()
        fake.hideAllPorts.assert_called_once_with()

    def test_show_all_ports_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("GraphNode")
        fake.showAllPorts.return_value = None
        node = RPGraphNode(fake)
        node.show_all_ports()
        fake.showAllPorts.assert_called_once_with()

    def test_get_is_panel_widget_returns_int(self) -> None:
        # Pattern G — returns 0/1 int
        fake = make_fake_element("GraphNode")
        fake.getIsPanelWidget.return_value = 1
        node = RPGraphNode(fake)
        assert node.get_is_panel_widget() == 1
        fake.getIsPanelWidget.assert_called_once_with()


class TestRPConnectorTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Connector", getName="conn1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPConnector)

    def test_is_condition_connector_returns_int(self) -> None:
        # Pattern G — returns 0/1 int
        fake = make_fake_element("Connector")
        fake.isConditionConnector.return_value = 1
        conn = RPConnector(fake)
        assert conn.is_condition_connector() == 1
        fake.isConditionConnector.assert_called_once_with()

    def test_is_fork_connector_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Connector")
        fake.isForkConnector.return_value = 1
        conn = RPConnector(fake)
        assert conn.is_fork_connector() == 1
        fake.isForkConnector.assert_called_once_with()

    def test_is_join_connector_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Connector")
        fake.isJoinConnector.return_value = 0
        conn = RPConnector(fake)
        assert conn.is_join_connector() == 0
        fake.isJoinConnector.assert_called_once_with()

    def test_get_connector_type_returns_str(self) -> None:
        # Pattern A — returns str
        fake = make_fake_element("Connector")
        fake.getConnectorType.return_value = "Fork"
        conn = RPConnector(fake)
        assert conn.get_connector_type() == "Fork"
        fake.getConnectorType.assert_called_once_with()

    def test_get_derived_in_edges_returns_collection(self) -> None:
        # Pattern C — returns collection
        fake = make_fake_element("Connector")
        trans = make_fake_element("Transition", getName="T1")
        fake.getDerivedInEdges.return_value = make_fake_collection([trans])
        conn = RPConnector(fake)
        result = conn.get_derived_in_edges()
        assert isinstance(result, RPCollection)
        fake.getDerivedInEdges.assert_called_once_with()

    def test_get_of_state_wraps_result(self) -> None:
        # Pattern B — returns wrapped RPState
        fake = make_fake_element("Connector")
        state = make_fake_element("State", getName="S1")
        fake.getOfState.return_value = state
        conn = RPConnector(fake)
        wrapped = conn.get_of_state()
        assert wrapped.get_name() == "S1"
        fake.getOfState.assert_called_once_with()

    def test_set_of_state_delegates(self) -> None:
        # Pattern F — setter with wrapped element
        fake = make_fake_element("Connector")
        state = make_fake_element("State", getName="S1")
        fake.setOfState.return_value = None
        from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState

        conn = RPConnector(fake)
        conn.set_of_state(RPState(state))
        fake.setOfState.assert_called_once_with(state)


class TestRPPinTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Pin", getName="pin1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPPin)

    def test_is_connector(self) -> None:
        fake = make_fake_element("Pin", getName="pin1")
        pin = RPPin(fake)
        assert isinstance(pin, RPConnector)

    def test_get_pin_direction_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("Pin")
        fake.getPinDirection.return_value = "In"
        pin = RPPin(fake)
        assert pin.get_pin_direction() == "In"
        fake.getPinDirection.assert_called_once_with()

    def test_get_pin_type_wraps_result(self) -> None:
        # Pattern B — returns wrapped RPClassifier
        fake = make_fake_element("Pin")
        classifier = make_fake_element("Class", getName="DataType")
        fake.getPinType.return_value = classifier
        pin = RPPin(fake)
        wrapped = pin.get_pin_type()
        assert wrapped.get_name() == "DataType"
        fake.getPinType.assert_called_once_with()

    def test_set_pin_type_delegates(self) -> None:
        # Pattern F — setter with wrapped element
        fake = make_fake_element("Pin")
        classifier = make_fake_element("Class", getName="DataType")
        fake.setPinType.return_value = None
        from rhapsody_cli.models.elements.classifiers.model_class import RPClass

        pin = RPPin(fake)
        pin.set_pin_type(RPClass(classifier))
        fake.setPinType.assert_called_once_with(classifier)


class TestRPConditionMarkTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("ConditionMark", getName="cm1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPConditionMark)

    def test_is_message(self) -> None:
        fake = make_fake_element("ConditionMark", getName="cm1")
        cm = RPConditionMark(fake)
        from rhapsody_cli.models.elements.interactions.model_interactions import RPMessage

        assert isinstance(cm, RPMessage)


class TestRPGraphicalPropertyTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphicalProperty", getName="gp1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphicalProperty)

    def test_get_key_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("GraphicalProperty")
        fake.getKey.return_value = "FillColor"
        gp = RPGraphicalProperty(fake)
        assert gp.get_key() == "FillColor"
        fake.getKey.assert_called_once_with()

    def test_get_value_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("GraphicalProperty")
        fake.getValue.return_value = "255,0,0"
        gp = RPGraphicalProperty(fake)
        assert gp.get_value() == "255,0,0"
        fake.getValue.assert_called_once_with()


class TestRPImageMapTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("ImageMap", getName="im1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPImageMap)

    def test_get_name_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("ImageMap")
        fake.getName.return_value = "MyImageMap"
        im = RPImageMap(fake)
        assert im.get_name() == "MyImageMap"
        fake.getName.assert_called_once_with()

    def test_get_shape_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("ImageMap")
        fake.getShape.return_value = "rect"
        im = RPImageMap(fake)
        assert im.get_shape() == "rect"
        fake.getShape.assert_called_once_with()

    def test_get_is_guid_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("ImageMap")
        fake.getIsGUID.return_value = 1
        im = RPImageMap(fake)
        assert im.get_is_guid() == 1
        fake.getIsGUID.assert_called_once_with()


class TestRPLinkTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Link", getName="link1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPLink)

    def test_get_end1_name_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("Link")
        fake.getEnd1Name.return_value = "End1"
        link = RPLink(fake)
        assert link.get_end1_name() == "End1"
        fake.getEnd1Name.assert_called_once_with()

    def test_get_from_wraps_result(self) -> None:
        # Pattern B — returns wrapped RPInstance
        fake = make_fake_element("Link")
        instance = make_fake_element("Instance", getName="Inst1")
        fake.getFrom.return_value = instance
        link = RPLink(fake)
        wrapped = link.get_from()
        assert wrapped.get_name() == "Inst1"
        fake.getFrom.assert_called_once_with()

    def test_get_instantiates_wraps_result(self) -> None:
        # Pattern B — returns wrapped RPRelation
        fake = make_fake_element("Link")
        relation = make_fake_element("Association", getName="Assoc1")
        fake.getInstantiates.return_value = relation
        link = RPLink(fake)
        wrapped = link.get_instantiates()
        assert wrapped.get_name() == "Assoc1"
        fake.getInstantiates.assert_called_once_with()

    def test_set_end1_name_delegates(self) -> None:
        # Pattern D
        fake = make_fake_element("Link")
        fake.setEnd1Name.return_value = None
        link = RPLink(fake)
        link.set_end1_name("NewEnd1")
        fake.setEnd1Name.assert_called_once_with("NewEnd1")


class TestRPMessagePointTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("MessagePoint", getName="mp1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPMessagePoint)

    def test_get_type_returns_str(self) -> None:
        # Pattern A
        fake = make_fake_element("MessagePoint")
        fake.getType.return_value = "Send"
        mp = RPMessagePoint(fake)
        assert mp.get_type() == "Send"
        fake.getType.assert_called_once_with()

    def test_get_message_wraps_result(self) -> None:
        # Pattern B — returns wrapped RPMessage
        fake = make_fake_element("MessagePoint")
        message = make_fake_element("Message", getName="Msg1")
        fake.getMessage.return_value = message
        mp = RPMessagePoint(fake)
        wrapped = mp.get_message()
        assert wrapped.get_name() == "Msg1"
        fake.getMessage.assert_called_once_with()


class TestRPTableLayoutTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TableLayout", getName="tl1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTableLayout)

    def test_get_collapse_first_column_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("TableLayout")
        fake.getCollapseFirstColumn.return_value = 1
        tl = RPTableLayout(fake)
        assert tl.get_collapse_first_column() == 1
        fake.getCollapseFirstColumn.assert_called_once_with()

    def test_get_column_name_parameterized(self) -> None:
        # Parameterized getter — must use call_com
        fake = make_fake_element("TableLayout")
        fake.getColumnName.return_value = "Col1"
        tl = RPTableLayout(fake)
        assert tl.get_column_name(0) == "Col1"
        fake.getColumnName.assert_called_once_with(0)

    def test_add_column_delegates(self) -> None:
        # Pattern F — multi-arg void
        fake = make_fake_element("TableLayout")
        fake.addColumn.return_value = None
        tl = RPTableLayout(fake)
        tl.add_column("GENERAL_ATTRIBUTE", "NAME", "Name")
        fake.addColumn.assert_called_once_with("GENERAL_ATTRIBUTE", "NAME", "Name")

    def test_get_element_types_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("TableLayout")
        fake.getElementTypes.return_value = make_fake_collection([])
        tl = RPTableLayout(fake)
        result = tl.get_element_types()
        assert isinstance(result, RPCollection)
        fake.getElementTypes.assert_called_once_with()

    def test_get_relation_table_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("TableLayout")
        fake.getRelationTable.return_value = 1
        tl = RPTableLayout(fake)
        assert tl.get_relation_table() == 1
        fake.getRelationTable.assert_called_once_with()


class TestRPTableViewTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TableView", getName="tv1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTableView)

    def test_get_row_count_returns_int(self) -> None:
        # Pattern A (int)
        fake = make_fake_element("TableView")
        fake.getRowCount.return_value = 5
        tv = RPTableView(fake)
        assert tv.get_row_count() == 5
        fake.getRowCount.assert_called_once_with()

    def test_get_cell_string_parameterized(self) -> None:
        # Parameterized getter — must use call_com
        fake = make_fake_element("TableView")
        fake.getCellString.return_value = "CellText"
        tv = RPTableView(fake)
        assert tv.get_cell_string(0, 0) == "CellText"
        fake.getCellString.assert_called_once_with(0, 0)

    def test_get_its_table_layout_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("TableView")
        layout = make_fake_element("TableLayout", getName="TL1")
        fake.getItsTableLayout.return_value = layout
        tv = RPTableView(fake)
        wrapped = tv.get_its_table_layout()
        assert wrapped.get_name() == "TL1"
        fake.getItsTableLayout.assert_called_once_with()

    def test_open_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("TableView")
        fake.open.return_value = None
        tv = RPTableView(fake)
        tv.open()
        fake.open.assert_called_once_with()


class TestRPMatrixLayoutTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("MatrixLayout", getName="ml1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPMatrixLayout)

    def test_get_from_element_types_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("MatrixLayout")
        fake.getFromElementTypes.return_value = make_fake_collection([])
        ml = RPMatrixLayout(fake)
        result = ml.get_from_element_types()
        assert isinstance(result, RPCollection)
        fake.getFromElementTypes.assert_called_once_with()


class TestRPMatrixViewTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("MatrixView", getName="mv1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPMatrixView)

    def test_get_column_count_returns_int(self) -> None:
        # Pattern A (int)
        fake = make_fake_element("MatrixView")
        fake.getColumnCount.return_value = 3
        mv = RPMatrixView(fake)
        assert mv.get_column_count() == 3
        fake.getColumnCount.assert_called_once_with()

    def test_get_cell_elements_parameterized(self) -> None:
        # Parameterized getter returning collection — must use call_com
        fake = make_fake_element("MatrixView")
        el = make_fake_element("Class", getName="C1")
        fake.getCellElements.return_value = make_fake_collection([el])
        mv = RPMatrixView(fake)
        result = mv.get_cell_elements(0, 0)
        assert isinstance(result, RPCollection)
        fake.getCellElements.assert_called_once_with(0, 0)

    def test_open_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("MatrixView")
        fake.open.return_value = None
        mv = RPMatrixView(fake)
        mv.open()
        fake.open.assert_called_once_with()
