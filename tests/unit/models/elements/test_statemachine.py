"""Tests for rhapsody_cli.elements.statemachine.RPStateVertex and RPState."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.statemachine import RPState, RPStateVertex
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPStateVertex:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("StateVertex", getName="SV1")
        sv = RPStateVertex(fake)
        assert isinstance(sv, RPModelElement)
        assert sv.get_name() == "SV1"

    def test_add_flow_delegates_and_wraps(self) -> None:
        fake = make_fake_element("StateVertex")
        to = make_fake_element("StateVertex", getName="Target")
        result = make_fake_element("Transition", getName="Flow1")
        fake.addFlow.return_value = result
        sv = RPStateVertex(fake)
        wrapped = sv.add_flow("ControlFlow", RPStateVertex(to))
        assert wrapped.get_name() == "Flow1"
        fake.addFlow.assert_called_once_with("ControlFlow", to)

    def test_add_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("StateVertex")
        to = make_fake_element("StateVertex", getName="Target")
        result = make_fake_element("Transition", getName="T1")
        fake.addTransition.return_value = result
        sv = RPStateVertex(fake)
        wrapped = sv.add_transition(RPStateVertex(to))
        assert wrapped.get_name() == "T1"
        fake.addTransition.assert_called_once_with(to)

    def test_delete_transition_delegates(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteTransition.return_value = None
        sv = RPStateVertex(fake)
        sv.delete_transition(RPModelElement(trans))
        fake.deleteTransition.assert_called_once_with(trans)

    def test_get_in_transitions_returns_collection(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.getInTransitions.return_value = make_fake_collection([trans])
        sv = RPStateVertex(fake)
        result = sv.get_in_transitions()
        assert isinstance(result, RPCollection)
        fake.getInTransitions.assert_called_once_with()

    def test_get_out_transitions_returns_collection(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.getOutTransitions.return_value = make_fake_collection([trans])
        sv = RPStateVertex(fake)
        result = sv.get_out_transitions()
        assert isinstance(result, RPCollection)
        fake.getOutTransitions.assert_called_once_with()

    def test_get_parent_wraps_result(self) -> None:
        fake = make_fake_element("StateVertex")
        parent = make_fake_element("State", getName="Parent")
        fake.getParent.return_value = parent
        sv = RPStateVertex(fake)
        result = sv.get_parent()
        assert isinstance(result, RPState)
        assert result.get_name() == "Parent"
        fake.getParent.assert_called_once_with()

    def test_set_parent_delegates(self) -> None:
        fake = make_fake_element("StateVertex")
        parent = make_fake_element("State", getName="Parent")
        fake.setParent.return_value = None
        sv = RPStateVertex(fake)
        sv.set_parent(RPState(parent))
        fake.setParent.assert_called_once_with(parent)

    def test_is_registered(self) -> None:
        fake = make_fake_element("StateVertex", getName="SV1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPStateVertex)


class TestRPState:
    def test_is_state_vertex(self) -> None:
        fake = make_fake_element("State", getName="S1")
        s = RPState(fake)
        assert isinstance(s, RPStateVertex)

    def test_add_activity_final_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Final")
        fake.addActivityFinal.return_value = result
        s = RPState(fake)
        wrapped = s.add_activity_final()
        assert wrapped.get_name() == "Final"
        fake.addActivityFinal.assert_called_once_with()

    def test_add_connector_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Connector", getName="Fork1")
        fake.addConnector.return_value = result
        s = RPState(fake)
        wrapped = s.add_connector("Fork")
        assert isinstance(wrapped, RPModelElement)
        fake.addConnector.assert_called_once_with("Fork")

    def test_add_internal_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        trigger = make_fake_element("Operation", getName="ev")
        result = make_fake_element("Transition", getName="T1")
        fake.addInternalTransition.return_value = result
        s = RPState(fake)
        wrapped = s.add_internal_transition(RPModelElement(trigger))
        assert wrapped.get_name() == "T1"
        fake.addInternalTransition.assert_called_once_with(trigger)

    def test_add_state_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Sub")
        fake.addState.return_value = result
        s = RPState(fake)
        wrapped = s.add_state("Sub")
        assert wrapped.get_name() == "Sub"
        fake.addState.assert_called_once_with("Sub")

    def test_add_static_reaction_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        trigger = make_fake_element("Operation", getName="ev")
        result = make_fake_element("Transition", getName="T1")
        fake.addStaticReaction.return_value = result
        s = RPState(fake)
        wrapped = s.add_static_reaction(RPModelElement(trigger))
        assert wrapped.get_name() == "T1"
        fake.addStaticReaction.assert_called_once_with(trigger)

    def test_add_termination_state_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Term")
        fake.addTerminationState.return_value = result
        s = RPState(fake)
        wrapped = s.add_termination_state()
        assert wrapped.get_name() == "Term"
        fake.addTerminationState.assert_called_once_with()

    def test_create_default_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        from_ = make_fake_element("State", getName="Root")
        result = make_fake_element("Transition", getName="DT1")
        fake.createDefaultTransition.return_value = result
        s = RPState(fake)
        wrapped = s.create_default_transition(RPState(from_))
        assert wrapped.get_name() == "DT1"
        fake.createDefaultTransition.assert_called_once_with(from_)

    def test_create_sub_statechart_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Statechart", getName="Sub")
        fake.createSubStatechart.return_value = result
        s = RPState(fake)
        wrapped = s.create_sub_statechart()
        assert wrapped.get_name() == "Sub"
        fake.createSubStatechart.assert_called_once_with()

    def test_delete_connector_delegates(self) -> None:
        fake = make_fake_element("State")
        conn = make_fake_element("Connector", getName="C1")
        fake.deleteConnector.return_value = None
        s = RPState(fake)
        s.delete_connector(RPModelElement(conn))
        fake.deleteConnector.assert_called_once_with(conn)

    def test_delete_internal_transition_delegates(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteInternalTransition.return_value = None
        s = RPState(fake)
        s.delete_internal_transition(RPModelElement(trans))
        fake.deleteInternalTransition.assert_called_once_with(trans)

    def test_delete_static_reaction_delegates(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteStaticReaction.return_value = None
        s = RPState(fake)
        s.delete_static_reaction(RPModelElement(trans))
        fake.deleteStaticReaction.assert_called_once_with(trans)

    def test_get_default_transition_wraps_result(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Transition", getName="DT1")
        fake.getDefaultTransition.return_value = result
        s = RPState(fake)
        wrapped = s.get_default_transition()
        assert wrapped.get_name() == "DT1"
        fake.getDefaultTransition.assert_called_once_with()

    def test_get_entry_action_returns_string(self) -> None:
        fake = make_fake_element("State", getEntryAction="entry()")
        s = RPState(fake)
        assert s.get_entry_action() == "entry()"
        fake.getEntryAction.assert_called_once_with()

    def test_get_exit_action_returns_string(self) -> None:
        fake = make_fake_element("State", getExitAction="exit()")
        s = RPState(fake)
        assert s.get_exit_action() == "exit()"
        fake.getExitAction.assert_called_once_with()

    def test_get_full_name_in_statechart_returns_string(self) -> None:
        fake = make_fake_element("State", getFullNameInStatechart="ROOT.On.Idle")
        s = RPState(fake)
        assert s.get_full_name_in_statechart() == "ROOT.On.Idle"
        fake.getFullNameInStatechart.assert_called_once_with()

    def test_get_inherits_from_wraps_result(self) -> None:
        fake = make_fake_element("State")
        parent = make_fake_element("State", getName="Parent")
        fake.getInheritsFrom.return_value = parent
        s = RPState(fake)
        wrapped = s.get_inherits_from()
        assert isinstance(wrapped, RPState)
        assert wrapped.get_name() == "Parent"
        fake.getInheritsFrom.assert_called_once_with()

    def test_get_internal_transitions_returns_collection(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.getInternalTransitions.return_value = make_fake_collection([trans])
        s = RPState(fake)
        result = s.get_internal_transitions()
        assert isinstance(result, RPCollection)
        fake.getInternalTransitions.assert_called_once_with()

    def test_get_is_overridden_returns_int(self) -> None:
        fake = make_fake_element("State", getIsOverridden=1)
        s = RPState(fake)
        assert s.get_is_overridden() == 1
        fake.getIsOverridden.assert_called_once_with()

    def test_get_is_reference_activity_returns_int(self) -> None:
        fake = make_fake_element("State", getIsReferenceActivity=0)
        s = RPState(fake)
        assert s.get_is_reference_activity() == 0
        fake.getIsReferenceActivity.assert_called_once_with()

    def test_get_its_statechart_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sc = make_fake_element("Statechart", getName="SC1")
        fake.getItsStatechart.return_value = sc
        s = RPState(fake)
        wrapped = s.get_its_statechart()
        assert wrapped.get_name() == "SC1"
        fake.getItsStatechart.assert_called_once_with()

    def test_get_its_swimlane_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sw = make_fake_element("Swimlane", getName="Lane1")
        fake.getItsSwimlane.return_value = sw
        s = RPState(fake)
        wrapped = s.get_its_swimlane()
        assert wrapped.get_name() == "Lane1"
        fake.getItsSwimlane.assert_called_once_with()

    def test_get_logical_states_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getLogicalStates.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_logical_states()
        assert isinstance(result, RPCollection)
        fake.getLogicalStates.assert_called_once_with()

    def test_get_nested_statechart_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sc = make_fake_element("Statechart", getName="Sub")
        fake.getNestedStatechart.return_value = sc
        s = RPState(fake)
        wrapped = s.get_nested_statechart()
        assert wrapped.get_name() == "Sub"
        fake.getNestedStatechart.assert_called_once_with()

    def test_get_reference_to_activity_wraps_result(self) -> None:
        fake = make_fake_element("State")
        act = make_fake_element("Class", getName="Act1")
        fake.getReferenceToActivity.return_value = act
        s = RPState(fake)
        wrapped = s.get_reference_to_activity()
        assert wrapped.get_name() == "Act1"
        fake.getReferenceToActivity.assert_called_once_with()

    def test_get_send_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sa = make_fake_element("SendAction", getName="SA1")
        fake.getSendAction.return_value = sa
        s = RPState(fake)
        wrapped = s.get_send_action()
        assert wrapped.get_name() == "SA1"
        fake.getSendAction.assert_called_once_with()

    def test_get_state_type_returns_string(self) -> None:
        fake = make_fake_element("State", getStateType="And")
        s = RPState(fake)
        assert s.get_state_type() == "And"
        fake.getStateType.assert_called_once_with()

    def test_get_static_reactions_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sr = make_fake_element("Transition", getName="SR1")
        fake.getStaticReactions.return_value = make_fake_collection([sr])
        s = RPState(fake)
        result = s.get_static_reactions()
        assert isinstance(result, RPCollection)
        fake.getStaticReactions.assert_called_once_with()

    def test_get_sub_state_vertices_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getSubStateVertices.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_sub_state_vertices()
        assert isinstance(result, RPCollection)
        fake.getSubStateVertices.assert_called_once_with()

    def test_get_sub_states_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getSubStates.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_sub_states()
        assert isinstance(result, RPCollection)
        fake.getSubStates.assert_called_once_with()

    def test_get_the_entry_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        action = make_fake_element("Action", getName="entryAct")
        fake.getTheEntryAction.return_value = action
        s = RPState(fake)
        wrapped = s.get_the_entry_action()
        assert wrapped.get_name() == "entryAct"
        fake.getTheEntryAction.assert_called_once_with()

    def test_get_the_exit_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        action = make_fake_element("Action", getName="exitAct")
        fake.getTheExitAction.return_value = action
        s = RPState(fake)
        wrapped = s.get_the_exit_action()
        assert wrapped.get_name() == "exitAct"
        fake.getTheExitAction.assert_called_once_with()

    def test_is_and_returns_int(self) -> None:
        fake = make_fake_element("State", isAnd=True)
        s = RPState(fake)
        assert s.is_and() == 1
        fake.isAnd.assert_called_once_with()

    def test_is_compound_returns_int(self) -> None:
        fake = make_fake_element("State", isCompound=True)
        s = RPState(fake)
        assert s.is_compound() == 1

    def test_is_leaf_returns_int(self) -> None:
        fake = make_fake_element("State", isLeaf=True)
        s = RPState(fake)
        assert s.is_leaf() == 1

    def test_is_root_returns_int(self) -> None:
        fake = make_fake_element("State", isRoot=True)
        s = RPState(fake)
        assert s.is_root() == 1

    def test_is_send_action_state_returns_int(self) -> None:
        fake = make_fake_element("State", isSendActionState=True)
        s = RPState(fake)
        assert s.is_send_action_state() == 1

    def test_override_inheritance_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.overrideInheritance.return_value = None
        s = RPState(fake)
        s.override_inheritance()
        fake.overrideInheritance.assert_called_once_with()

    def test_reset_entry_action_inheritance_wraps_self(self) -> None:
        fake = make_fake_element("State")
        fake.resetEntryActionInheritance.return_value = fake
        s = RPState(fake)
        result = s.reset_entry_action_inheritance()
        assert isinstance(result, RPState)
        fake.resetEntryActionInheritance.assert_called_once_with()

    def test_reset_exit_action_inheritance_wraps_self(self) -> None:
        fake = make_fake_element("State")
        fake.resetExitActionInheritance.return_value = fake
        s = RPState(fake)
        result = s.reset_exit_action_inheritance()
        assert isinstance(result, RPState)
        fake.resetExitActionInheritance.assert_called_once_with()

    def test_set_entry_action_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setEntryAction.return_value = None
        s = RPState(fake)
        s.set_entry_action("entry()")
        fake.setEntryAction.assert_called_once_with("entry()")

    def test_set_exit_action_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setExitAction.return_value = None
        s = RPState(fake)
        s.set_exit_action("exit()")
        fake.setExitAction.assert_called_once_with("exit()")

    def test_set_internal_transition_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setInternalTransition.return_value = None
        s = RPState(fake)
        s.set_internal_transition("ev", "[g]", "act")
        fake.setInternalTransition.assert_called_once_with("ev", "[g]", "act")

    def test_set_its_swimlane_delegates(self) -> None:
        fake = make_fake_element("State")
        sw = make_fake_element("Swimlane", getName="L1")
        fake.setItsSwimlane.return_value = None
        s = RPState(fake)
        s.set_its_swimlane(RPModelElement(sw))
        fake.setItsSwimlane.assert_called_once_with(sw)

    def test_set_reference_to_activity_delegates(self) -> None:
        fake = make_fake_element("State")
        act = make_fake_element("Class", getName="Act1")
        fake.setReferenceToActivity.return_value = None
        s = RPState(fake)
        s.set_reference_to_activity(RPModelElement(act))
        fake.setReferenceToActivity.assert_called_once_with(act)

    def test_set_state_type_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setStateType.return_value = None
        s = RPState(fake)
        s.set_state_type("And")
        fake.setStateType.assert_called_once_with("And")

    def test_set_static_reaction_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setStaticReaction.return_value = None
        s = RPState(fake)
        s.set_static_reaction("ev", "[g]", "act")
        fake.setStaticReaction.assert_called_once_with("ev", "[g]", "act")

    def test_unoverride_inheritance_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.unoverrideInheritance.return_value = None
        s = RPState(fake)
        s.unoverride_inheritance()
        fake.unoverrideInheritance.assert_called_once_with()

    def test_is_registered(self) -> None:
        fake = make_fake_element("State", getName="S1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPState)
