"""Exception types raised by py_rhapsody.

These mirror the failure modes of the Rhapsody Java API: a
``RhapsodyRuntimeException`` is raised by the Java API when a COM/JNI call
into Rhapsody fails; ``RhapsodyConnectionError`` is specific to py_rhapsody
and covers failures to attach to or launch a Rhapsody instance.
"""

from __future__ import annotations


class RhapsodyRuntimeException(Exception):
    """Raised when a call into the Rhapsody COM API fails.

    Mirrors ``com.telelogic.rhapsody.core.RhapsodyRuntimeException`` from the
    Java API. The original COM error message/HRESULT text is preserved as
    the exception message.
    """


class RhapsodyConnectionError(Exception):
    """Raised when py_rhapsody cannot attach to or launch a Rhapsody instance."""
