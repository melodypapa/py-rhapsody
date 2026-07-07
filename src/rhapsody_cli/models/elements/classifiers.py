"""Classifier-family wrappers: mirrors IRPClassifier and its Java subtypes
(IRPClass, IRPActor, IRPUseCase, IRPOperation, IRPStatechart) from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)


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


class RPClass(RPClassifier):
    """Wraps ``IRPClass``."""

    def addSuperclass(self, super_class: RPClass) -> None:
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addClass(name)))


class RPActor(RPClassifier):
    """Wraps ``IRPActor``."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        return wrap(call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        call_com(lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0))


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


class RPOperation(RPUnit):
    """Wraps ``IRPOperation``."""

    def getBody(self) -> str:
        return call_com(lambda: str(self._com.getBody()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def getIsVirtual(self) -> bool:
        return call_com(lambda: bool(self._com.getIsVirtual()))

    def getReturns(self) -> Any:
        return wrap(call_com(lambda: self._com.getReturns()))

    def createAutoFlowChart(self) -> None:
        call_com(lambda: self._com.createAutoFlowChart())


class RPStatechart(RPUnit):
    """Wraps ``IRPStatechart``."""

    def addNewNodeByType(
        self, meta_type: str, x_position: int, y_position: int, width: int, height: int
    ) -> Any:
        return wrap(
            call_com(
                lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height)
            )
        )

    def createGraphics(self) -> None:
        call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        call_com(lambda: self._com.deleteState(state._com))


register_wrapper("Class", RPClass)
register_wrapper("Actor", RPActor)
register_wrapper("UseCase", RPUseCase)
register_wrapper("Operation", RPOperation)
register_wrapper("Statechart", RPStatechart)
