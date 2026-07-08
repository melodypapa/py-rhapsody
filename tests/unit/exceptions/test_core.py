"""Tests for rhapsody_cli.exceptions."""

from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException


def test_rhapsody_runtime_exception_preserves_message() -> None:
    exc = RhapsodyRuntimeException("boom")

    assert str(exc) == "boom"
    assert isinstance(exc, Exception)


def test_rhapsody_connection_error_preserves_message() -> None:
    exc = RhapsodyConnectionError("no running instance found")

    assert str(exc) == "no running instance found"
    assert isinstance(exc, Exception)


def test_rhapsody_runtime_exception_is_not_a_connection_error() -> None:
    # These are two distinct failure modes and must not be conflated by callers.
    assert not issubclass(RhapsodyRuntimeException, RhapsodyConnectionError)
    assert not issubclass(RhapsodyConnectionError, RhapsodyRuntimeException)
