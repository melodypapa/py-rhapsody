"""rhapsody_cli: Pythonic wrapper around the IBM Rhapsody COM API.

Method names on wrapped elements mirror the Rhapsody Java API
(`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API
knowledge transfers directly. Importing this package registers all core
element wrappers with the internal ``wrap()`` dispatch factory.
"""

from __future__ import annotations

from rhapsody_cli import models  # noqa: F401
from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException
from rhapsody_cli.models import RPCollection, RPModelElement, RPUnit

__all__ = [
    "RPCollection",
    "RPModelElement",
    "RPUnit",
    "RhapsodyApplication",
    "RhapsodyConnectionError",
    "RhapsodyRuntimeException",
]
