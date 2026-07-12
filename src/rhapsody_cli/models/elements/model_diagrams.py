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
        """Closes the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::closeDiagram()
        """
        AbstractRPModelElement.call_com(lambda: self._com.closeDiagram())

    def addTextBox(self, text: str, x_position: int, y_position: int, width: int, height: int) -> Any:
        """Adds a text box using the specified text, starting point, width, and height.

        Args:
            text: The text content for the box.
            x_position: The X coordinate for the text box.
            y_position: The Y coordinate for the text box.
            width: The width of the text box.
            height: The height of the text box.

        Returns:
            The wrapped text box element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addTextBox(java.lang.String text, int xPosition, int yPosition, int nWidth, int nHeight)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTextBox(text, x_position, y_position, width, height)))

    def getCustomViews(self) -> RPCollection:
        """Gets the custom views that were applied to this diagram view.

        Returns:
            An ``RPCollection`` of custom view elements.

        Raises:
            RhapsodyRuntimeException: if the custom views cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getCustomViews()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCustomViews", "customViews"))

    def getCorrespondingGraphicElements(self, model_element: RPModelElement) -> RPCollection:
        """Returns the graphical elements that represent the specified model element.

        In cases where the same model element appears multiple times in a single
        diagram, the collection returned will contain more than one graphical element.

        Args:
            model_element: The model element to find graphic representations for.

        Returns:
            An ``RPCollection`` of graphic elements.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getCorrespondingGraphicElements(com.telelogic.rhapsody.core.IRPModelElement modelElement)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getCorrespondingGraphicElements(model_element._com)))


AbstractRPModelElement.register_wrapper("ActivityDiagram", RPDiagram)
