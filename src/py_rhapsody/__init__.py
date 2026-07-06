"""py_rhapsody: Pythonic wrapper around the IBM Rhapsody COM API.

Method names on wrapped elements mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge transfers directly. Importing this package registers all core
element wrappers with the internal ``wrap()`` dispatch factory.
"""

from __future__ import annotations

from py_rhapsody import models  # noqa: F401
from py_rhapsody.application import RhapsodyApplication
from py_rhapsody.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException
from py_rhapsody.models import RPCollection, RPModelElement, RPUnit

__all__ = [
    "RPCollection",
    "RPModelElement",
    "RPUnit",
    "RhapsodyApplication",
    "RhapsodyConnectionError",
    "RhapsodyRuntimeException",
]
