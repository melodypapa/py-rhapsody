"""Tests for rhapsody_cli.models.elements.misc wrappers."""

from rhapsody_cli.models._core import RPModelElement, wrap
from rhapsody_cli.models.elements.misc import (
    RPComment,
    RPConstraint,
    RPEnumerationLiteral,
)
from tests.unit.models.fakes import make_fake_element


def test_enumeration_literal_is_a_model_element() -> None:
    fake = make_fake_element("EnumerationLiteral", getName="LITERAL1")
    literal = RPEnumerationLiteral(fake)

    assert isinstance(literal, RPModelElement)
    assert literal.getName() == "LITERAL1"


def test_enumeration_literal_is_registered() -> None:
    fake = make_fake_element("EnumerationLiteral", getName="LITERAL1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPEnumerationLiteral)


def test_comment_is_a_model_element() -> None:
    fake = make_fake_element("Comment", getName="Comment1")
    comment = RPComment(fake)

    assert isinstance(comment, RPModelElement)
    assert comment.getName() == "Comment1"


def test_comment_is_registered() -> None:
    fake = make_fake_element("Comment", getName="Comment1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPComment)


def test_constraint_is_a_model_element() -> None:
    fake = make_fake_element("Constraint", getName="Constraint1")
    constraint = RPConstraint(fake)

    assert isinstance(constraint, RPModelElement)
    assert constraint.getName() == "Constraint1"


def test_constraint_is_registered() -> None:
    fake = make_fake_element("Constraint", getName="Constraint1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPConstraint)
