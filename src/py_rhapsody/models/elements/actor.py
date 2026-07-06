"""RPActor: wraps IRPActor, a UML actor (external role that interacts with the system)."""

from __future__ import annotations

from typing import Any

from py_rhapsody.models._core import RPModelElement, call_com, register_wrapper, wrap
from py_rhapsody.models.elements.classifier import RPClassifier


class RPActor(RPClassifier):
    """Wraps ``IRPActor``."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        return wrap(call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        call_com(lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0))


register_wrapper("Actor", RPActor)
