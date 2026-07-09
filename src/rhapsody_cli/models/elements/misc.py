"""Miscellaneous model element wrappers — RPComment, RPConstraint, RPEnumerationLiteral."""

from rhapsody_cli.models._core import RPModelElement, register_wrapper


class RPEnumerationLiteral(RPModelElement):
    """Wraps ``IRPEnumerationLiteral``: a literal value in an enumeration."""

    pass


register_wrapper("EnumerationLiteral", RPEnumerationLiteral)


class RPComment(RPModelElement):
    """Wraps ``IRPComment``: a free-text comment element."""

    pass


register_wrapper("Comment", RPComment)


class RPConstraint(RPModelElement):
    """Wraps ``IRPConstraint``: a constraint element."""

    pass


register_wrapper("Constraint", RPConstraint)
