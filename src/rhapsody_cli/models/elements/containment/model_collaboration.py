"""Wraps ``com.telelogic.rhapsody.core.IRPCollaboration``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPUnit


class RPCollaboration(RPUnit):
    """Wraps ``IRPCollaboration``: a collaboration that extends ``IRPUnit``."""

    # IRPCollaboration method parity checklist:
    # [ ] addActionBlock  [ ] impl  [ ] docstring  [ ] test
    # [ ] addCancelledTimeout  [ ] impl  [ ] docstring  [ ] test
    # [ ] addClassifierRole  [ ] impl  [ ] docstring  [ ] test
    # [ ] addClassifierRoleByName  [ ] impl  [ ] docstring  [ ] test
    # [ ] addClassifierRoleForInstance  [ ] impl  [ ] docstring  [ ] test
    # [ ] addConditionMark  [ ] impl  [ ] docstring  [ ] test
    # [ ] addCtor  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDataFlow  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDestructionEvent  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDtor  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDurationConstraint  [ ] impl  [ ] docstring  [ ] test
    # [ ] addDurationObservation  [ ] impl  [ ] docstring  [ ] test
    # [ ] addFoundMessage  [ ] impl  [ ] docstring  [ ] test
    # [ ] addInteractionOccurrence  [ ] impl  [ ] docstring  [ ] test
    # [ ] addInteractionOperator  [ ] impl  [ ] docstring  [ ] test
    # [ ] addLostMessage  [ ] impl  [ ] docstring  [ ] test
    # [ ] addMessage  [ ] impl  [ ] docstring  [ ] test
    # [ ] addReplyMessage  [ ] impl  [ ] docstring  [ ] test
    # [ ] addStateInvariant  [ ] impl  [ ] docstring  [ ] test
    # [ ] addSystemBorder  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTimeConstraint  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTimeInterval  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTimeObservation  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTimeout  [ ] impl  [ ] docstring  [ ] test
    # [ ] generateSequence  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActivationCondition  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActivationMode  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActivator  [ ] impl  [ ] docstring  [ ] test
    # [ ] getAssociations  [ ] impl  [ ] docstring  [ ] test
    # [ ] getClassifier  [ ] impl  [ ] docstring  [ ] test
    # [ ] getConcurrentGroup  [ ] impl  [ ] docstring  [ ] test
    # [ ] getExecutionOccurrences  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionOccurrences  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionOperators  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMessagePoints  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMessages  [ ] impl  [ ] docstring  [ ] test
    # [ ] getMode  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPredecessor  [ ] impl  [ ] docstring  [ ] test
    # [ ] getSuccessor  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPUnit / IRPModelElement methods (covered by RPUnit / RPModelElement checklists)
    # No deprecated IRPCollaboration methods.

    pass


AbstractRPModelElement.register_wrapper("Collaboration", RPCollaboration)
