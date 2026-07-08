"""Wraps ``com.telelogic.rhapsody.core.IRPStatechart``."""

from typing import Any

from rhapsody_cli.models._core import RPModelElement, call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPStatechart(RPClass):
    """Wraps ``IRPStatechart``: represents a statechart behavior."""

    def addNewNodeByType(self, meta_type: str, x_position: int, y_position: int, width: int, height: int) -> Any:
        """Adds a new node to the statechart.

        Args:
            meta_type: The type of node to create (e.g., 'State', 'Junction').
            x_position: The X coordinate for the node.
            y_position: The Y coordinate for the node.
            width: The width of the node.
            height: The height of the node.

        Returns:
            The wrapped node element created.
        """
        return wrap(call_com(lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height)))

    def createGraphics(self) -> None:
        """Creates the graphics/diagram representation for the statechart."""
        call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        """Closes the statechart diagram."""
        call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        """Deletes a state from the statechart.

        Args:
            state: The state element to delete.
        """
        call_com(lambda: self._com.deleteState(state._com))


register_wrapper("Statechart", RPStatechart)
