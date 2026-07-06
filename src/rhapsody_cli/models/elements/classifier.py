"""RPClassifier: wraps IRPClassifier, the shared base of IRPClass/IRPActor/IRPUseCase."""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, wrap


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``."""

    def addAttribute(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAttributes()))

    def getOperations(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOperations()))

    def addGeneralization(self, base_classifier: RPClassifier) -> None:
        call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> Any:
        return wrap(call_com(lambda: self._com.addStatechart()))
