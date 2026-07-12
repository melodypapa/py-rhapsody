"""Statemachine model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
    from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
    from rhapsody_cli.models.elements.activity.model_actions import RPAction, RPSendAction
    from rhapsody_cli.models.elements.activity.model_activity import RPSwimlane
    from rhapsody_cli.models.elements.graphics.model_graphics import RPConnector
    from rhapsody_cli.models.elements.model_interactions import RPTransition


class RPStateVertex(RPModelElement):
    """Wraps ``IRPStateVertex``: represents the characteristics shared by various statechart elements such as states, join/fork connectors, and condition connectors."""

    # IRPStateVertex method parity checklist:
    # [ ] addFlow                      [ ] impl  [ ] docstring  [ ] test
    # [ ] addTransition                [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteTransition             [ ] impl  [ ] docstring  [ ] test
    # [ ] getInTransitions             [ ] impl  [ ] docstring  [ ] test
    # [ ] getOutTransitions            [ ] impl  [ ] docstring  [ ] test
    # [ ] getParent                    [ ] impl  [ ] docstring  [ ] test
    # [ ] setParent                    [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPStateVertex methods.

    def add_flow(self, type_: str, to: "RPStateVertex") -> "RPTransition":
        """Adds a control flow or object flow from this element to the specified element.

        Args:
            type_: The type of flow to create — valid values are ``"ControlFlow"``
                and ``"ObjectFlow"``.
            to: The target element for the new flow.

        Returns:
            The flow that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::addFlow(java.lang.String type, com.telelogic.rhapsody.core.IRPStateVertex to)
        """
        raise NotImplementedError

    def add_transition(self, to: "RPStateVertex") -> "RPTransition":
        """Adds a transition from this element to the specified element.

        Args:
            to: The target element for the new transition.

        Returns:
            The transition that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::addTransition(com.telelogic.rhapsody.core.IRPStateVertex to)
        """
        raise NotImplementedError

    def delete_transition(self, transition: "RPTransition") -> None:
        """Deletes the specified transition.

        Args:
            transition: The transition to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::deleteTransition(com.telelogic.rhapsody.core.IRPTransition transition)
        """
        raise NotImplementedError

    def get_in_transitions(self) -> "RPCollection":
        """Returns all of the transitions that enter the element.

        Internal transitions are also included in the returned collection. To
        identify which transitions are internal, use
        ``IRPTransition.isStaticReaction()``.

        Returns:
            All the transitions that enter the element (collection of
            ``IRPTransition`` elements).

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::getInTransitions()
        """
        raise NotImplementedError

    def get_out_transitions(self) -> "RPCollection":
        """Returns all of the transitions that exit the element.

        Internal transitions are also included in the returned collection. To
        identify which transitions are internal, use
        ``IRPTransition.isStaticReaction()``.

        Returns:
            All the transitions that exit the element (collection of
            ``IRPTransition`` elements).

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::getOutTransitions()
        """
        raise NotImplementedError

    def get_parent(self) -> "RPState":
        """Returns the element's parent.

        If the element is not contained in a specific state, the root state of
        the diagram is returned.

        Returns:
            The element's parent.

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::getParent()
        """
        raise NotImplementedError

    def set_parent(self, parent: "RPState") -> None:
        """Sets the parent state of the element.

        Args:
            parent: The state that should serve as the parent of the element.

        Reference:
            com.telelogic.rhapsody.core.IRPStateVertex::setParent(com.telelogic.rhapsody.core.IRPState parent)
        """
        raise NotImplementedError


class RPState(RPStateVertex):
    """Wraps ``IRPState``: represents states in a statechart."""

    # IRPState method parity checklist:
    # [ ] addActivityFinal             [ ] impl  [ ] docstring  [ ] test
    # [ ] addConnector                 [ ] impl  [ ] docstring  [ ] test
    # [ ] addInternalTransition        [ ] impl  [ ] docstring  [ ] test
    # [ ] addState                     [ ] impl  [ ] docstring  [ ] test
    # [ ] addStaticReaction            [ ] impl  [ ] docstring  [ ] test
    # [ ] addTerminationState          [ ] impl  [ ] docstring  [ ] test
    # [ ] createDefaultTransition      [ ] impl  [ ] docstring  [ ] test
    # [ ] createNestedStatechart       [ ] impl  [ ] docstring  [ ] test
    # [ ] createSubStatechart          [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteConnector              [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteInternalTransition     [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteStaticReaction         [ ] impl  [ ] docstring  [ ] test
    # [ ] getDefaultTransition         [ ] impl  [ ] docstring  [ ] test
    # [ ] getEntryAction               [ ] impl  [ ] docstring  [ ] test
    # [ ] getExitAction                [ ] impl  [ ] docstring  [ ] test
    # [ ] getFullNameInStatechart      [ ] impl  [ ] docstring  [ ] test
    # [ ] getInheritsFrom              [ ] impl  [ ] docstring  [ ] test
    # [ ] getInternalTransitions       [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsOverridden              [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsReferenceActivity       [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsStatechart             [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsSwimlane               [ ] impl  [ ] docstring  [ ] test
    # [ ] getLogicalStates             [ ] impl  [ ] docstring  [ ] test
    # [ ] getNestedStatechart          [ ] impl  [ ] docstring  [ ] test
    # [ ] getReferenceToActivity       [ ] impl  [ ] docstring  [ ] test
    # [ ] getSendAction                [ ] impl  [ ] docstring  [ ] test
    # [ ] getStateType                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getStaticReactions           [ ] impl  [ ] docstring  [ ] test
    # [ ] getSubStateVertices          [ ] impl  [ ] docstring  [ ] test
    # [ ] getSubStates                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getTheEntryAction            [ ] impl  [ ] docstring  [ ] test
    # [ ] getTheExitAction             [ ] impl  [ ] docstring  [ ] test
    # [ ] isAnd                        [ ] impl  [ ] docstring  [ ] test
    # [ ] isCompound                   [ ] impl  [ ] docstring  [ ] test
    # [ ] isLeaf                       [ ] impl  [ ] docstring  [ ] test
    # [ ] isRoot                       [ ] impl  [ ] docstring  [ ] test
    # [ ] isSendActionState            [ ] impl  [ ] docstring  [ ] test
    # [ ] overrideInheritance          [ ] impl  [ ] docstring  [ ] test
    # [ ] resetEntryActionInheritance  [ ] impl  [ ] docstring  [ ] test
    # [ ] resetExitActionInheritance   [ ] impl  [ ] docstring  [ ] test
    # [ ] setEntryAction               [ ] impl  [ ] docstring  [ ] test
    # [ ] setExitAction                [ ] impl  [ ] docstring  [ ] test
    # [ ] setInternalTransition        [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsSwimlane               [ ] impl  [ ] docstring  [ ] test
    # [ ] setReferenceToActivity       [ ] impl  [ ] docstring  [ ] test
    # [ ] setStateType                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setStaticReaction            [ ] impl  [ ] docstring  [ ] test
    # [ ] unoverrideInheritance        [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # [deprecated] createNestedStatechart  - skipped (deprecated in Rhapsody Java API)
    # [deprecated] createSubStatechart  - skipped (deprecated in Rhapsody Java API)
    # No non-deprecated IRPState methods.

    def add_activity_final(self) -> "RPState":
        """Adds an ActivityFinal element to an Activity.

        This method should be called on the root state of the diagram, which you
        can get by calling ``IRPStatechart.getRootState()``.

        Returns:
            The ActivityFinal element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addActivityFinal()
        """
        raise NotImplementedError

    def add_connector(self, type_: str) -> "RPConnector":
        """Adds a connector element of the specified type to the state.

        Args:
            type_: The type of connector to add. Valid values are ``"Condition"``,
                ``"Fork"``, ``"History"``, ``"Join"``, ``"Termination"``,
                ``"InPin"``, ``"OutPin"``, and ``"InOutPin"``.

        Returns:
            The connector element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addConnector(java.lang.String type)
        """
        raise NotImplementedError

    def add_internal_transition(self, trigger: "RPInterfaceItem") -> "RPTransition":
        """Adds an internal transition to the state.

        Args:
            trigger: The trigger to use for the internal transition.

        Returns:
            The internal transition that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addInternalTransition(com.telelogic.rhapsody.core.IRPInterfaceItem trigger)
        """
        raise NotImplementedError

    def add_state(self, name: str) -> "RPState":
        """Adds a new substate to this state.

        To add a new top-level state to a statechart, call this method on the
        root state of the statechart, which you can get by calling
        ``IRPStatechart.getRootState()``.

        Args:
            name: The name to use for the new state.

        Returns:
            The state that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addState(java.lang.String name)
        """
        raise NotImplementedError

    def add_static_reaction(self, trigger: "RPInterfaceItem") -> "RPTransition":
        """Adds an internal transition to the state.

        Args:
            trigger: The trigger to use for the internal transition.

        Returns:
            The internal transition that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addStaticReaction(com.telelogic.rhapsody.core.IRPInterfaceItem trigger)
        """
        raise NotImplementedError

    def add_termination_state(self) -> "RPState":
        """Adds a termination state to a statechart.

        This method should be called on the root state of the statechart, which
        you can get by calling ``IRPStatechart.getRootState()``.

        Returns:
            The termination state that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::addTerminationState()
        """
        raise NotImplementedError

    def create_default_transition(self, from_: "RPState") -> "RPTransition":
        """Creates a default transition to this state from the state specified with the parameter.

        Args:
            from_: The source of the default transition, for example, the root
                state.

        Returns:
            The default transition that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPState::createDefaultTransition(com.telelogic.rhapsody.core.IRPState from)
        """
        raise NotImplementedError

    def create_nested_statechart(self) -> "RPStatechart":
        """Deprecated. Use ``create_sub_statechart()`` instead.

        Reference:
            com.telelogic.rhapsody.core.IRPState::createNestedStatechart()
        """
        raise NotImplementedError

    def create_sub_statechart(self) -> "RPStatechart":
        """Creates a sub-statechart for the state.

        Returns:
            The new statechart that was created.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::createSubStatechart()
        """
        raise NotImplementedError

    def delete_connector(self, connector: "RPConnector") -> None:
        """Deletes the specified connector element.

        Args:
            connector: The connector element that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPState::deleteConnector(com.telelogic.rhapsody.core.IRPConnector connector)
        """
        raise NotImplementedError

    def delete_internal_transition(self, p_val: "RPTransition") -> None:
        """Deletes the specified internal transition.

        Args:
            p_val: The internal transition to delete.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::deleteInternalTransition(com.telelogic.rhapsody.core.IRPTransition pVal)
        """
        raise NotImplementedError

    def delete_static_reaction(self, p_val: "RPTransition") -> None:
        """Deletes the specified internal transition.

        Args:
            p_val: The internal transition that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPState::deleteStaticReaction(com.telelogic.rhapsody.core.IRPTransition pVal)
        """
        raise NotImplementedError

    def get_default_transition(self) -> "RPTransition":
        """Returns the default transition within the state.

        Returns:
            The default transition within the state.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getDefaultTransition()
        """
        raise NotImplementedError

    def get_entry_action(self) -> str:
        """Returns the entry action that was defined for the state.

        Returns:
            The entry action that was defined for the state.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getEntryAction()
        """
        raise NotImplementedError

    def get_exit_action(self) -> str:
        """Returns the exit action that was defined for the state.

        Returns:
            The exit action that was defined for the state.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getExitAction()
        """
        raise NotImplementedError

    def get_full_name_in_statechart(self) -> str:
        """Returns the full name of the state within the statechart, including its hierarchical position.

        For example, if the statechart includes a state called ``Listening``
        within a top-level state called ``On``, the full name would be
        ``ROOT.On.Listening``.

        Returns:
            The full name of the state within the statechart.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getFullNameInStatechart()
        """
        raise NotImplementedError

    def get_inherits_from(self) -> "RPState":
        """Returns the corresponding state from the statechart of the class that this class is derived from.

        Returns:
            The corresponding state from the statechart of the class that this
            class is derived from.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getInheritsFrom()
        """
        raise NotImplementedError

    def get_internal_transitions(self) -> "RPCollection":
        """Returns a collection of the state's internal transitions.

        Returns:
            The state's internal transitions.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getInternalTransitions()
        """
        raise NotImplementedError

    def get_is_overridden(self) -> int:
        """Checks whether there is still an inheritance relationship between this state and the corresponding state from the statechart of the class that this class is derived from.

        Returns:
            1 if the inheritance relationship is overridden, 0 if there is an
            inheritance relationship.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getIsOverridden()
        """
        raise NotImplementedError

    def get_is_reference_activity(self) -> int:
        """Checks whether this element is a call behavior element.

        The Rhapsody API does not provide a method to change an existing
        ``IRPState`` element to a call behavior element. The only way to create
        a call behavior element is to call ``IRPFlowchart.addCallBehavior`` or
        ``IRPFlowchart.addReferenceActivity``.

        Returns:
            1 if the element is a call behavior element, 0 if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getIsReferenceActivity()
        """
        raise NotImplementedError

    def get_its_statechart(self) -> "RPStatechart":
        """Returns the statechart that this state belongs to.

        Returns:
            The statechart that this state belongs to.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getItsStatechart()
        """
        raise NotImplementedError

    def get_its_swimlane(self) -> "RPSwimlane":
        """Returns the swimlane that the action is located in.

        Returns:
            The swimlane that the action is located in.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getItsSwimlane()
        """
        raise NotImplementedError

    def get_logical_states(self) -> "RPCollection":
        """Returns a collection of all the substates of the current state and all the first-level substates of those states, down to the second level.

        Returns:
            A collection of all the substates of the current state and all the
            first-level substates of those states.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getLogicalStates()
        """
        raise NotImplementedError

    def get_nested_statechart(self) -> "RPStatechart":
        """Returns the state's sub-statechart.

        Returns:
            The state's sub-statechart.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getNestedStatechart()
        """
        raise NotImplementedError

    def get_reference_to_activity(self) -> "RPModelElement":
        """For call behavior elements, returns the activity that is referenced.

        Returns:
            The activity that is referenced.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getReferenceToActivity()
        """
        raise NotImplementedError

    def get_send_action(self) -> "RPSendAction":
        """Returns the Send Action element associated with the state.

        A Send Action element is an object of type ``IRPState`` for which the
        state type was set to ``"EventState"`` using the ``setStateType`` method.
        To manipulate a Send Action element (for example, to set the event),
        first get the Send Action element using this method.

        Returns:
            The Send Action element associated with the state.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getSendAction()
        """
        raise NotImplementedError

    def get_state_type(self) -> str:
        """Returns the type of the state, for example, an And state or a Termination state.

        For the full list of state types, see the documentation for
        ``set_state_type``.

        Returns:
            The state's type.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getStateType()
        """
        raise NotImplementedError

    def get_static_reactions(self) -> "RPCollection":
        """Returns a collection of the state's internal transitions.

        Returns:
            The state's internal transitions.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getStaticReactions()
        """
        raise NotImplementedError

    def get_sub_state_vertices(self) -> "RPCollection":
        """Returns a collection of all the first-level elements contained in this state, including both node and connector elements.

        The method does not return elements nested within these first-level
        elements.

        Returns:
            A collection of all the first-level elements contained in this
            state.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getSubStateVertices()
        """
        raise NotImplementedError

    def get_sub_states(self) -> "RPCollection":
        """Returns a collection of the substates contained in this state.

        Note that this will not work if a state contains a sub-statechart. In
        such a case, you would need to navigate to the sub-statechart's root
        state first.

        Returns:
            The substates contained in this state (collection of ``IRPState``
            objects).

        Reference:
            com.telelogic.rhapsody.core.IRPState::getSubStates()
        """
        raise NotImplementedError

    def get_the_entry_action(self) -> "RPAction":
        """Returns the entry action element of the state.

        Returns:
            The entry action element of the state.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getTheEntryAction()
        """
        raise NotImplementedError

    def get_the_exit_action(self) -> "RPAction":
        """Returns the exit action element of the state.

        Returns:
            The exit action element of the state.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::getTheExitAction()
        """
        raise NotImplementedError

    def is_and(self) -> int:
        """Checks whether the state contains one or more And Lines.

        Returns:
            1 if the state contains one or more And Lines, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPState::isAnd()
        """
        raise NotImplementedError

    def is_compound(self) -> int:
        """Checks whether the state is a compound state, meaning a state that contains one or more substates.

        Returns:
            1 if the state is a compound state, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPState::isCompound()
        """
        raise NotImplementedError

    def is_leaf(self) -> int:
        """Checks whether the state is a leaf state, meaning a state that does not contain any substates.

        Returns:
            1 if the state is a leaf state, 0 if the state contains one or more
            substates.

        Reference:
            com.telelogic.rhapsody.core.IRPState::isLeaf()
        """
        raise NotImplementedError

    def is_root(self) -> int:
        """Checks whether the state is the root state of the statechart.

        Returns:
            1 if the state is the root state of the statechart, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPState::isRoot()
        """
        raise NotImplementedError

    def is_send_action_state(self) -> int:
        """Checks whether the state is a Send Action element.

        Returns:
            1 if it is a Send Action element, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPState::isSendActionState()
        """
        raise NotImplementedError

    def override_inheritance(self) -> None:
        """Breaks the inheritance relationship between this state and the corresponding state from the statechart of the class that this class is derived from.

        Reference:
            com.telelogic.rhapsody.core.IRPState::overrideInheritance()
        """
        raise NotImplementedError

    def reset_entry_action_inheritance(self) -> "RPState":
        """Restores the inheritance relationship between this state and the corresponding state from the statechart of the class that this class is derived from, for the entry action.

        Returns:
            The state on which the method was called.

        Reference:
            com.telelogic.rhapsody.core.IRPState::resetEntryActionInheritance()
        """
        raise NotImplementedError

    def reset_exit_action_inheritance(self) -> "RPState":
        """Restores the inheritance relationship between this state and the corresponding state from the statechart of the class that this class is derived from, for the exit action.

        Returns:
            The state on which the method was called.

        Reference:
            com.telelogic.rhapsody.core.IRPState::resetExitActionInheritance()
        """
        raise NotImplementedError

    def set_entry_action(self, entry_action: str) -> None:
        """Sets the entry action for the state.

        Args:
            entry_action: The code to use for the state's entry action.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setEntryAction(java.lang.String entryAction)
        """
        raise NotImplementedError

    def set_exit_action(self, exit_action: str) -> None:
        """Sets the exit action for the state.

        Args:
            exit_action: The code to use for the state's exit action.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setExitAction(java.lang.String exitAction)
        """
        raise NotImplementedError

    def set_internal_transition(self, trig_val: str, guard_val: str, action_val: str) -> None:
        """Sets the internal transition for the state.

        Args:
            trig_val: The trigger to set for the internal transition.
            guard_val: The guard to set for the internal transition.
            action_val: The action to set for the internal transition.

        Raises:
            RhapsodyRuntimeException: If an error occurs during the operation.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setInternalTransition(java.lang.String trigVal, java.lang.String guardVal, java.lang.String actionVal)
        """
        raise NotImplementedError

    def set_its_swimlane(self, its_swimlane: "RPSwimlane") -> None:
        """Specifies the swimlane that the action should be in.

        Args:
            its_swimlane: The swimlane that the action should be in.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setItsSwimlane(com.telelogic.rhapsody.core.IRPSwimlane itsSwimlane)
        """
        raise NotImplementedError

    def set_reference_to_activity(self, reference_to_activity: "RPModelElement") -> None:
        """For call behavior elements, sets the activity that is referenced by the element.

        Args:
            reference_to_activity: The activity that should be referenced by the
                call behavior element.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setReferenceToActivity(com.telelogic.rhapsody.core.IRPModelElement referenceToActivity)
        """
        raise NotImplementedError

    def set_state_type(self, state_type: str) -> None:
        """Specifies the type of the state.

        Args:
            state_type: The type of the state. Valid values are ``"And"``,
                ``"Or"`` (for a state that is not an "And" state),
                ``"LocalTermination"`` (for Termination State), ``"Block"``
                (for Action Block), ``"Action"``, ``"SubActivity"``,
                ``"EventState"`` (for Send Action), and ``"FlowFinal"``.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setStateType(java.lang.String stateType)
        """
        raise NotImplementedError

    def set_static_reaction(self, trig_val: str, guard_val: str, action_val: str) -> None:
        """Adds a new internal transition to the state.

        Args:
            trig_val: The trigger to set for the internal transition.
            guard_val: The guard to set for the internal transition.
            action_val: The action to set for the internal transition.

        Reference:
            com.telelogic.rhapsody.core.IRPState::setStaticReaction(java.lang.String trigVal, java.lang.String guardVal, java.lang.String actionVal)
        """
        raise NotImplementedError

    def unoverride_inheritance(self) -> None:
        """Restores the inheritance relationship between this state and the corresponding state from the statechart of the class that this class is derived from.

        This method is used to restore the relationship that was severed with
        ``override_inheritance()``.

        Reference:
            com.telelogic.rhapsody.core.IRPState::unoverrideInheritance()
        """
        raise NotImplementedError
