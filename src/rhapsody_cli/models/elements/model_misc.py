"""Miscellaneous model element wrappers — RPComment, RPConstraint, RPEnumerationLiteral."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPEnumerationLiteral(RPModelElement):
    """Wraps ``IRPEnumerationLiteral``: a literal value in an enumeration."""

    # IRPEnumerationLiteral method parity checklist:
    # [ ] getValue  [ ] impl  [ ] docstring  [ ] test
    # [ ] setValue  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPEnumerationLiteral methods.

    pass


AbstractRPModelElement.register_wrapper("EnumerationLiteral", RPEnumerationLiteral)


class RPComment(RPModelElement):
    """Wraps ``IRPComment``: a free-text comment element."""

    # IRPComment method parity checklist:
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPComment methods.

    pass


AbstractRPModelElement.register_wrapper("Comment", RPComment)


class RPConstraint(RPModelElement):
    """Wraps ``IRPConstraint``: a constraint element."""

    # IRPConstraint method parity checklist:
    # [ ] getConstraintsByMe  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPConstraint methods.

    pass


AbstractRPModelElement.register_wrapper("Constraint", RPConstraint)
