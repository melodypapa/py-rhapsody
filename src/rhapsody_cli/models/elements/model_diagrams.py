"""Diagram-family wrappers: mirrors IRPDiagram from com.telelogic.rhapsody.core."""

from typing import Any

from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    RPCollection,
    RPModelElement,
    RPUnit,
)


class RPDiagram(RPUnit):
    """Wraps ``IRPDiagram``: represents a diagram in the model."""

    def closeDiagram(self) -> None:
        """Closes the diagram."""
        AbstractRPModelElement.call_com(lambda: self._com.closeDiagram())

    def addTextBox(self, text: str, x_position: int, y_position: int, width: int, height: int) -> Any:
        """Adds a text box to the diagram.

        Args:
            text: The text content for the box.
            x_position: The X coordinate for the text box.
            y_position: The Y coordinate for the text box.
            width: The width of the text box.
            height: The height of the text box.

        Returns:
            The wrapped text box element created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTextBox(text, x_position, y_position, width, height)))

    def getCustomViews(self) -> RPCollection:
        """Returns all custom views defined on the diagram.

        Returns:
            An ``RPCollection`` of custom view elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCustomViews", "customViews"))

    def getCorrespondingGraphicElements(self, model_element: RPModelElement) -> RPCollection:
        """Gets the graphic elements corresponding to a model element on the diagram.

        Args:
            model_element: The model element to find graphic representations for.

        Returns:
            An ``RPCollection`` of graphic elements.
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getCorrespondingGraphicElements(model_element._com)))


AbstractRPModelElement.register_wrapper("ActivityDiagram", RPDiagram)
