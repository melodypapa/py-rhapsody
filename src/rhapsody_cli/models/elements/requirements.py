"""Requirement-family wrappers: mirrors IRPAnnotation and IRPRequirement
from com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, call_com, register_wrapper


class RPRequirement(RPUnit):
    """Wraps ``IRPRequirement``."""

    def getRequirementID(self) -> str:
        return call_com(lambda: str(self._com.getRequirementID()))

    def setRequirementID(self, requirement_id: str) -> None:
        call_com(lambda: self._com.setRequirementID(requirement_id))


register_wrapper("Requirement", RPRequirement)
