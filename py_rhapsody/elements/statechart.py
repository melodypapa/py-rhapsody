"""RPStatechart: wraps IRPStatechart, a class's behavioral state machine."""

from __future__ import annotations

from typing import Any

from py_rhapsody._core import RPModelElement, RPUnit, call_com, register_wrapper, wrap


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


register_wrapper("Statechart", RPStatechart)
