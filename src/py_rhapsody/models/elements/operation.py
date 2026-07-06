"""RPOperation: wraps IRPOperation, a class/package-level operation or function."""

from __future__ import annotations

from typing import Any

from py_rhapsody.models._core import RPUnit, call_com, register_wrapper, wrap


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


register_wrapper("Operation", RPOperation)
