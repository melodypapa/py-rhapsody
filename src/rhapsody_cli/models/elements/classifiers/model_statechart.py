"""Wraps ``com.telelogic.rhapsody.core.IRPStatechart``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_class import RPClass


class RPStatechart(RPClass):
    """Wraps ``IRPStatechart``: represents a statechart behavior."""

    def addNewNodeByType(self, meta_type: str, x_position: int, y_position: int, width: int, height: int) -> Any:
        """Adds a statechart element of the specified type to the statechart.

        The element is placed at the given position with the given dimensions.
        This method works only for elements that have purely graphical
        representations and are not actual model elements. To add an "ordinary"
        model element to a statechart, first add the element to your model and
        then add its graphical representation via ``addNewNodeForElement``.

        Args:
            meta_type: The type of node to create (e.g., 'State', 'Junction').
            x_position: The X coordinate for the node.
            y_position: The Y coordinate for the node.
            width: The width of the node.
            height: The height of the node.

        Returns:
            The wrapped node element created.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechart::addNewNodeByType(java.lang.String metaType, int xPosition, int yPosition, int nWidth, int nHeight)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height)))

    def createGraphics(self) -> None:
        """Creates the graphical representation of the statechart's elements.

        When a statechart is created through the API, its graphical
        representation is not created by default; the first time you open it in
        Rhapsody you would be prompted whether to create the graphics. Calling
        this method creates the graphical representation directly.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechart::createGraphics()
        """
        AbstractRPModelElement.call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        """Closes the statechart diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechart::closeDiagram()
        """
        AbstractRPModelElement.call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        """Deletes a state from the statechart.

        Args:
            state: The state element to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPStatechart::deleteState(com.telelogic.rhapsody.core.IRPState state)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteState(state._com))


AbstractRPModelElement.register_wrapper("Statechart", RPStatechart)
