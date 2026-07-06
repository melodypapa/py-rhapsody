"""RPUseCase: wraps IRPUseCase, a UML use case."""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, call_com, register_wrapper
from rhapsody_cli.models.elements.classifier import RPClassifier


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``."""

    def addExtensionPoint(self, entry_point: str) -> None:
        call_com(lambda: self._com.addExtensionPoint(entry_point))

    def getExtensionPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getExtensionPoints()))

    def getEntryPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getEntryPoints()))

    def getDescribingDiagrams(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getDescribingDiagrams()))


register_wrapper("UseCase", RPUseCase)
