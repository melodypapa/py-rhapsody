"""Miscellaneous model element wrappers — RPComment, RPConstraint, RPEnumerationLiteral."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement


class RPEnumerationLiteral(RPModelElement):
    """Wraps ``IRPEnumerationLiteral``: a literal value in an enumeration."""

    # IRPEnumerationLiteral method parity checklist:
    # [x] getValue  [x] impl  [x] docstring  [ ] test
    # [x] setValue  [x] impl  [x] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPEnumerationLiteral methods.

    def get_value(self) -> int:
        """Returns the integer value of the enumeration literal.

        Returns:
            The enumeration literal value as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPEnumerationLiteral::getValue()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getValue", "value"))

    def set_value(self, value: int) -> None:
        """Sets the integer value of the enumeration literal.

        Args:
            value: The integer value to set.

        Reference:
            com.telelogic.rhapsody.core.IRPEnumerationLiteral::setValue(int value)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setValue(value))


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
    # [x] getConstraintsByMe  [x] impl  [x] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPConstraint methods.

    def get_constraints_by_me(self) -> RPCollection:
        """Returns the collection of elements constrained by this constraint.

        Returns:
            An ``RPCollection`` of model elements constrained by this constraint.

        Reference:
            com.telelogic.rhapsody.core.IRPConstraint::getConstraintsByMe()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getConstraintsByMe", "constraintsByMe"))


AbstractRPModelElement.register_wrapper("Constraint", RPConstraint)