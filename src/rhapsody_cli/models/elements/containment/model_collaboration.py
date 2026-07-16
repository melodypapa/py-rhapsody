"""Wraps ``com.telelogic.rhapsody.core.IRPCollaboration``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.common import RPClassifierRole, RPInteractionOccurrence, RPInteractionOperator, RPMessage
    from rhapsody_cli.models.elements.graphics import RPConditionMark


class RPCollaboration(RPUnit):
    """Wraps ``IRPCollaboration``: a collaboration that extends ``IRPUnit``."""

    # IRPCollaboration method parity checklist:
    # [ ] add_action_block  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_cancelled_timeout  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_classifier_role  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_classifier_role_by_name  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_classifier_role_for_instance  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_condition_mark  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_ctor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_data_flow  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_destruction_event  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_dtor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_duration_constraint  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_duration_observation  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_found_message  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_interaction_occurrence  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_interaction_operator  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_lost_message  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_message  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] add_reply_message  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_state_invariant  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_system_border  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_time_constraint  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_time_interval  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_time_observation  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_timeout  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] generate_sequence  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_activation_condition  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_activation_mode  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_activator  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_associations  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_classifier  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_concurrent_group  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_execution_occurrences  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_interaction_occurrences  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_interaction_operators  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_message_points  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_messages  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_mode  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_predecessor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_successor  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPCollaboration methods.

    def add_action_block(self, name: str) -> "RPUnit":
        """Adds an action block to the collaboration.

        Args:
            name: The name of the action block.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addActionBlock(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addActionBlock(name))))

    def add_cancelled_timeout(self, name: str) -> "RPUnit":
        """Adds a cancelled timeout to the collaboration.

        Args:
            name: The name of the cancelled timeout.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addCancelledTimeout(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addCancelledTimeout(name))))

    def add_classifier_role(self, name: str) -> "RPClassifierRole":
        """Adds a classifier role to the collaboration.

        Args:
            name: The name of the classifier role.

        Returns:
            The wrapped ``IRPClassifierRole`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addClassifierRole(java.lang.String name)
        """
        return cast("RPClassifierRole", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addClassifierRole(name))))

    def add_classifier_role_by_name(self, name: str) -> "RPClassifierRole":
        """Adds a classifier role by name to the collaboration.

        Args:
            name: The name of the classifier role.

        Returns:
            The wrapped ``IRPClassifierRole`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addClassifierRoleByName(java.lang.String name)
        """
        return cast("RPClassifierRole", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addClassifierRoleByName(name))))

    def add_classifier_role_for_instance(self, instance: RPUnit) -> "RPClassifierRole":
        """Adds a classifier role for an instance to the collaboration.

        Args:
            instance: The instance to create a classifier role for.

        Returns:
            The wrapped ``IRPClassifierRole`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addClassifierRoleForInstance(IRPInstance instance)
        """
        return cast("RPClassifierRole", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addClassifierRoleForInstance(instance._com))))

    def add_condition_mark(self, name: str) -> "RPConditionMark":
        """Adds a condition mark to the collaboration.

        Args:
            name: The name of the condition mark.

        Returns:
            The wrapped ``IRPConditionMark`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addConditionMark(java.lang.String name)
        """
        return cast("RPConditionMark", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addConditionMark(name))))

    def add_ctor(self, name: str) -> "RPUnit":
        """Adds a constructor to the collaboration.

        Args:
            name: The name of the constructor.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addCtor(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addCtor(name))))

    def add_data_flow(self, name: str) -> "RPUnit":
        """Adds a data flow to the collaboration.

        Args:
            name: The name of the data flow.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addDataFlow(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addDataFlow(name))))

    def add_destruction_event(self, name: str) -> "RPUnit":
        """Adds a destruction event to the collaboration.

        Args:
            name: The name of the destruction event.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addDestructionEvent(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addDestructionEvent(name))))

    def add_dtor(self, name: str) -> "RPUnit":
        """Adds a destructor to the collaboration.

        Args:
            name: The name of the destructor.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addDtor(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addDtor(name))))

    def add_duration_constraint(self, name: str) -> "RPUnit":
        """Adds a duration constraint to the collaboration.

        Args:
            name: The name of the duration constraint.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addDurationConstraint(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addDurationConstraint(name))))

    def add_duration_observation(self, name: str) -> "RPUnit":
        """Adds a duration observation to the collaboration.

        Args:
            name: The name of the duration observation.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addDurationObservation(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addDurationObservation(name))))

    def add_found_message(self, name: str) -> "RPMessage":
        """Adds a found message to the collaboration.

        Args:
            name: The name of the found message.

        Returns:
            The wrapped ``IRPMessage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addFoundMessage(java.lang.String name)
        """
        return cast("RPMessage", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addFoundMessage(name))))

    def add_interaction_occurrence(self, name: str) -> "RPInteractionOccurrence":
        """Adds an interaction occurrence to the collaboration.

        Args:
            name: The name of the interaction occurrence.

        Returns:
            The wrapped ``IRPInteractionOccurrence`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addInteractionOccurrence(java.lang.String name)
        """
        return cast("RPInteractionOccurrence", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addInteractionOccurrence(name))))

    def add_interaction_operator(self, name: str) -> "RPInteractionOperator":
        """Adds an interaction operator to the collaboration.

        Args:
            name: The name of the interaction operator.

        Returns:
            The wrapped ``IRPInteractionOperator`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addInteractionOperator(java.lang.String name)
        """
        return cast("RPInteractionOperator", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addInteractionOperator(name))))

    def add_lost_message(self, name: str) -> "RPMessage":
        """Adds a lost message to the collaboration.

        Args:
            name: The name of the lost message.

        Returns:
            The wrapped ``IRPMessage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addLostMessage(java.lang.String name)
        """
        return cast("RPMessage", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addLostMessage(name))))

    def add_message(self, name: str) -> "RPMessage":
        """Adds a message to the collaboration.

        Args:
            name: The name of the message.

        Returns:
            The wrapped ``IRPMessage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addMessage(java.lang.String name)
        """
        return cast("RPMessage", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addMessage(name))))

    def add_reply_message(self, name: str) -> "RPMessage":
        """Adds a reply message to the collaboration.

        Args:
            name: The name of the reply message.

        Returns:
            The wrapped ``IRPMessage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addReplyMessage(java.lang.String name)
        """
        return cast("RPMessage", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addReplyMessage(name))))

    def add_state_invariant(self, name: str) -> "RPUnit":
        """Adds a state invariant to the collaboration.

        Args:
            name: The name of the state invariant.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addStateInvariant(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addStateInvariant(name))))

    def add_system_border(self, name: str) -> "RPUnit":
        """Adds a system border to the collaboration.

        Args:
            name: The name of the system border.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addSystemBorder(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addSystemBorder(name))))

    def add_time_constraint(self, name: str) -> "RPUnit":
        """Adds a time constraint to the collaboration.

        Args:
            name: The name of the time constraint.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addTimeConstraint(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addTimeConstraint(name))))

    def add_time_interval(self, name: str) -> "RPUnit":
        """Adds a time interval to the collaboration.

        Args:
            name: The name of the time interval.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addTimeInterval(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addTimeInterval(name))))

    def add_time_observation(self, name: str) -> "RPUnit":
        """Adds a time observation to the collaboration.

        Args:
            name: The name of the time observation.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addTimeObservation(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addTimeObservation(name))))

    def add_timeout(self, name: str) -> "RPUnit":
        """Adds a timeout to the collaboration.

        Args:
            name: The name of the timeout.

        Returns:
            The wrapped ``IRPUnit`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::addTimeout(java.lang.String name)
        """
        return cast("RPUnit", AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addTimeout(name))))

    def generate_sequence(self) -> None:
        """Generates sequence diagram from collaboration.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::generateSequence()
        """
        self.call_com(lambda: self._com.generateSequence())

    def get_activation_condition(self) -> str:
        """Returns the activation condition of the collaboration.

        Returns:
            The activation condition string.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getActivationCondition()
        """
        return self._get_method_or_property(self._com, "getActivationCondition", "activationCondition")

    def get_activation_mode(self) -> int:
        """Returns the activation mode of the collaboration.

        Returns:
            The activation mode as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getActivationMode()
        """
        return int(self.call_com(lambda: self._com.getActivationMode()))

    def get_activator(self) -> "RPUnit | None":
        """Returns the activator of the collaboration.

        Returns:
            The wrapped ``IRPUnit`` activator if set, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getActivator()
        """
        result = self.call_com(lambda: self._com.getActivator())
        if result is None:
            return None
        return cast("RPUnit", AbstractRPModelElement.wrap(result))

    def get_associations(self) -> "RPCollection":
        """Returns all associations in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPAssociation`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getAssociations()
        """
        return RPCollection(self.call_com(lambda: self._com.getAssociations()))

    def get_classifier_roles(self) -> "RPCollection":
        """Returns all classifier roles in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPClassifierRole`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getClassifierRoles()
        """
        return RPCollection(self.call_com(lambda: self._com.getClassifierRoles()))

    def get_classifier(self) -> "RPUnit | None":
        """Returns the classifier of the collaboration.

        Returns:
            The wrapped ``IRPUnit`` classifier if set, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getClassifier()
        """
        result = self.call_com(lambda: self._com.getClassifier())
        if result is None:
            return None
        return cast("RPUnit", AbstractRPModelElement.wrap(result))

    def get_concurrent_group(self) -> int:
        """Returns the concurrent group of the collaboration.

        Returns:
            The concurrent group as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getConcurrentGroup()
        """
        return int(self.call_com(lambda: self._com.getConcurrentGroup()))

    def get_execution_occurrences(self) -> "RPCollection":
        """Returns all execution occurrences in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPExecutionOccurrence`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getExecutionOccurrences()
        """
        return RPCollection(self.call_com(lambda: self._com.getExecutionOccurrences()))

    def get_interaction_occurrences(self) -> "RPCollection":
        """Returns all interaction occurrences in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPInteractionOccurrence`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getInteractionOccurrences()
        """
        return RPCollection(self.call_com(lambda: self._com.getInteractionOccurrences()))

    def get_interaction_operators(self) -> "RPCollection":
        """Returns all interaction operators in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPInteractionOperator`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getInteractionOperators()
        """
        return RPCollection(self.call_com(lambda: self._com.getInteractionOperators()))

    def get_message_points(self) -> "RPCollection":
        """Returns all message points in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPMessagePoint`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getMessagePoints()
        """
        return RPCollection(self.call_com(lambda: self._com.getMessagePoints()))

    def get_messages(self) -> "RPCollection":
        """Returns all messages in the collaboration.

        Returns:
            An ``RPCollection`` of ``IRPMessage`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getMessages()
        """
        return RPCollection(self.call_com(lambda: self._com.getMessages()))

    def get_mode(self) -> int:
        """Returns the mode of the collaboration.

        Returns:
            The mode as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getMode()
        """
        return int(self.call_com(lambda: self._com.getMode()))

    def get_predecessor(self) -> "RPUnit | None":
        """Returns the predecessor of the collaboration.

        Returns:
            The wrapped ``IRPUnit`` predecessor if set, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getPredecessor()
        """
        result = self.call_com(lambda: self._com.getPredecessor())
        if result is None:
            return None
        return cast("RPUnit", AbstractRPModelElement.wrap(result))

    def get_successor(self) -> "RPUnit | None":
        """Returns the successor of the collaboration.

        Returns:
            The wrapped ``IRPUnit`` successor if set, ``None`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPCollaboration::getSuccessor()
        """
        result = self.call_com(lambda: self._com.getSuccessor())
        if result is None:
            return None
        return cast("RPUnit", AbstractRPModelElement.wrap(result))


AbstractRPModelElement.register_wrapper("Collaboration", RPCollaboration)
