"""RPAttribute: wraps IRPAttribute, a class/package-level attribute or variable."""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, call_com, register_wrapper


class RPAttribute(RPUnit):
    """Wraps ``IRPAttribute``."""

    def getMultiplicity(self) -> str:
        return call_com(lambda: str(self._com.getMultiplicity()))

    def setMultiplicity(self, multiplicity: str) -> None:
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def setIsStatic(self, is_static: bool) -> None:
        call_com(lambda: self._com.setIsStatic(1 if is_static else 0))

    def getVisibility(self) -> str:
        return call_com(lambda: str(self._com.getVisibility()))

    def setVisibility(self, visibility: str) -> None:
        call_com(lambda: self._com.setVisibility(visibility))

    def getDefaultValue(self) -> str:
        return call_com(lambda: str(self._com.getDefaultValue()))

    def setDefaultValue(self, default_value: str) -> None:
        call_com(lambda: self._com.setDefaultValue(default_value))


register_wrapper("Attribute", RPAttribute)
