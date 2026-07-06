"""RPDiagram: wraps IRPDiagram, the base interface for all Rhapsody diagram types."""

from __future__ import annotations

from typing import Any

from py_rhapsody.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)


class RPDiagram(RPUnit):
    """Wraps ``IRPDiagram``."""

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def addTextBox(
        self, text: str, x_position: int, y_position: int, width: int, height: int
    ) -> Any:
        return wrap(
            call_com(lambda: self._com.addTextBox(text, x_position, y_position, width, height))
        )

    def getCustomViews(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getCustomViews()))

    def getCorrespondingGraphicElements(self, model_element: RPModelElement) -> RPCollection:
        return RPCollection(
            call_com(lambda: self._com.getCorrespondingGraphicElements(model_element._com))
        )


register_wrapper("ActivityDiagram", RPDiagram)
