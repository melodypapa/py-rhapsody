"""Wraps ``com.telelogic.rhapsody.core.IRPStatechart``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_class import RPClass

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.graphics.model_graphics import RPGraphNode


class RPStatechart(RPClass):
    """Wraps ``IRPStatechart``: represents a statechart behavior."""

    # IRPStatechart method parity checklist:
    # [ ] addFreeShapeByType  [ ] impl  [ ] docstring  [ ] test
    # [ ] addImage  [ ] impl  [ ] docstring  [ ] test
    # [ ] addNewEdgeByType  [ ] impl  [ ] docstring  [ ] test
    # [ ] addNewEdgeForElement  [ ] impl  [ ] docstring  [ ] test
    # [x] addNewNodeByType  [x] impl  [x] docstring  [x] test
    # [ ] addNewNodeForElement  [ ] impl  [ ] docstring  [ ] test
    # [ ] addTextBox  [ ] impl  [ ] docstring  [ ] test
    # [ ] openDiagramView  [ ] impl  [ ] docstring  [ ] test
    # [ ] addNewAcceptEventAction  [ ] impl  [ ] docstring  [ ] test
    # [ ] addNewAcceptTimeEvent  [ ] impl  [ ] docstring  [ ] test
    # [x] closeDiagram  [x] impl  [x] docstring  [x] test
    # [x] createGraphics  [x] impl  [x] docstring  [x] test
    # [x] deleteState  [x] impl  [x] docstring  [x] test
    # [x] findTrigger  [x] impl  [x] docstring  [x] test   (inherited from RPClassifier)
    # [ ] getAllTriggers  [ ] impl  [ ] docstring  [ ] test
    # [ ] getElementsInDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] getGraphicalElements  [ ] impl  [ ] docstring  [ ] test
    # [ ] getInheritsFrom  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsMainBehavior  [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsOverridden  [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsClass  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPicture  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPictureAs  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPictureAsDividedMetafiles  [ ] impl  [ ] docstring  [ ] test
    # [ ] getPicturesWithImageMap  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRootState  [ ] impl  [ ] docstring  [ ] test
    # [ ] getStatechartDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] overrideInheritance  [ ] impl  [ ] docstring  [ ] test
    # [ ] populateDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] setAsMainBehavior  [ ] impl  [ ] docstring  [ ] test
    # [ ] setShowDiagramFrame  [ ] impl  [ ] docstring  [ ] test
    # [ ] unoverrideInheritance  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClass / IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClass / RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPStatechart methods.

    def addNewNodeByType(self, meta_type: str, x_position: int, y_position: int, width: int, height: int) -> "RPGraphNode":
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
        return cast("RPGraphNode", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height))))

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
