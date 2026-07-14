"""Tests for rhapsody_cli.models.elements.misc wrappers."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.common.model_misc import (
    RPComment,
    RPConstraint,
    RPEnumerationLiteral,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_enumeration_literal_is_a_model_element() -> None:
    fake = make_fake_element("EnumerationLiteral", getName="LITERAL1")
    literal = RPEnumerationLiteral(fake)

    assert isinstance(literal, RPModelElement)
    assert literal.get_name() == "LITERAL1"


def test_enumeration_literal_is_registered() -> None:
    fake = make_fake_element("EnumerationLiteral", getName="LITERAL1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPEnumerationLiteral)


def test_comment_is_a_model_element() -> None:
    fake = make_fake_element("Comment", getName="Comment1")
    comment = RPComment(fake)

    assert isinstance(comment, RPModelElement)
    assert comment.get_name() == "Comment1"


def test_comment_is_registered() -> None:
    fake = make_fake_element("Comment", getName="Comment1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPComment)


def test_constraint_is_a_model_element() -> None:
    fake = make_fake_element("Constraint", getName="Constraint1")
    constraint = RPConstraint(fake)

    assert isinstance(constraint, RPModelElement)
    assert constraint.get_name() == "Constraint1"


def test_constraint_is_registered() -> None:
    fake = make_fake_element("Constraint", getName="Constraint1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPConstraint)


def test_enumeration_literal_get_value_returns_int() -> None:
    fake = make_fake_element("EnumerationLiteral")
    fake.getValue.return_value = 42
    literal = RPEnumerationLiteral(fake)
    assert literal.get_value() == 42
    fake.getValue.assert_called_once_with()


def test_enumeration_literal_set_value_delegates() -> None:
    fake = make_fake_element("EnumerationLiteral")
    fake.setValue.return_value = None
    literal = RPEnumerationLiteral(fake)
    literal.set_value(99)
    fake.setValue.assert_called_once_with(99)


def test_constraint_get_constraints_by_me_returns_collection() -> None:
    fake = make_fake_element("Constraint")
    inner = make_fake_element("Class", getName="ConstrainedClass")
    fake.getConstraintsByMe.return_value = make_fake_collection([inner])
    constraint = RPConstraint(fake)
    result = constraint.get_constraints_by_me()
    assert isinstance(result, RPCollection)
    fake.getConstraintsByMe.assert_called_once_with()
