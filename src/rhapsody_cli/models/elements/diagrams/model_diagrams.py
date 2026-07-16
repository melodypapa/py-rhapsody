"""Diagram-family wrappers: mirrors IRPDiagram from com.telelogic.rhapsody.core."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import (
    AbstractRPModelElement,
    RPCollection,
    RPModelElement,
    RPUnit,
)

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.graphics.model_graphics import RPGraphElement


class RPDiagram(RPUnit):
    """Wraps ``IRPDiagram``: represents a diagram in the model."""

    # IRPDiagram method parity checklist:
    # [ ] add_free_shape_by_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_image  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_new_edge_by_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_new_edge_for_element  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_new_node_by_type  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_new_node_for_element  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_text_box  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] create_diagram_view  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_custom_views  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_diagram_view_of  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_diagram_views  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] is_diagram_view  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] open_diagram_view  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] rearrange_ports  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_custom_views  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] update_view_on_server  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] close_diagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] complete_relations  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_corresponding_graphic_elements  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_elements_in_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_graphical_elements  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_last_visualization_modified_time  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_picture  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_picture_as  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_picture_as_divided_metafiles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_picture_ex  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_pictures_with_image_map  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] is_open  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] is_show_diagram_frame  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] open_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] populate_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] remove_graph_elements  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_show_diagram_frame  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_unit / irp_model_element methods (covered by rp_unit / rp_model_element checklists)
    # No deprecated IRPDiagram methods.

    def close_diagram(self) -> None:
        """Closes the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::closeDiagram()
        """
        AbstractRPModelElement.call_com(lambda: self._com.closeDiagram())

    def add_text_box(self, text: str, x_position: int, y_position: int, width: int, height: int) -> "RPGraphElement":
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
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTextBox(text, x_position, y_position, width, height))))

    def get_custom_views(self) -> RPCollection:
        """Gets the custom views that were applied to this diagram view.

        Returns:
            An ``RPCollection`` of custom view elements.

        Raises:
            RhapsodyRuntimeException: if the custom views cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getCustomViews()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCustomViews", "customViews"))

    def get_corresponding_graphic_elements(self, model_element: RPModelElement) -> RPCollection:
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

    def add_free_shape_by_type(self, type_: str, x: int, y: int, width: int, height: int) -> "RPGraphElement":
        """Adds a free shape to the diagram by type.

        Args:
            type_: The type of free shape to add.
            x: The X coordinate.
            y: The Y coordinate.
            width: The width.
            height: The height.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addFreeShapeByType(java.lang.String type, int x, int y, int width, int height)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addFreeShapeByType(type_, x, y, width, height))))

    def add_image(self, image_path: str, x: int, y: int, width: int, height: int) -> "RPGraphElement":
        """Adds an image to the diagram.

        Args:
            image_path: The path to the image file.
            x: The X coordinate.
            y: The Y coordinate.
            width: The width.
            height: The height.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addImage(java.lang.String imagePath, int x, int y, int width, int height)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addImage(image_path, x, y, width, height))))

    def add_new_edge_by_type(self, type_: str, source: "RPGraphElement", target: "RPGraphElement") -> "RPGraphElement":
        """Adds a new edge to the diagram by type.

        Args:
            type_: The type of edge to add.
            source: The source graph element.
            target: The target graph element.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addNewEdgeByType(java.lang.String type, com.telelogic.rhapsody.core.IRPGraphElement source, com.telelogic.rhapsody.core.IRPGraphElement target)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewEdgeByType(type_, source._com, target._com))))

    def add_new_edge_for_element(self, element: RPModelElement) -> "RPGraphElement":
        """Adds a new edge for the specified element.

        Args:
            element: The model element.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addNewEdgeForElement(com.telelogic.rhapsody.core.IRPModelElement element)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewEdgeForElement(element._com))))

    def add_new_node_by_type(self, type_: str, x: int, y: int, width: int, height: int) -> "RPGraphElement":
        """Adds a new node to the diagram by type.

        Args:
            type_: The type of node to add.
            x: The X coordinate.
            y: The Y coordinate.
            width: The width.
            height: The height.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addNewNodeByType(java.lang.String type, int x, int y, int width, int height)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewNodeByType(type_, x, y, width, height))))

    def add_new_node_for_element(self, element: RPModelElement, x: int, y: int, width: int, height: int) -> "RPGraphElement":
        """Adds a new node for the specified element.

        Args:
            element: The model element.
            x: The X coordinate.
            y: The Y coordinate.
            width: The width.
            height: The height.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::addNewNodeForElement(com.telelogic.rhapsody.core.IRPModelElement element, int x, int y, int width, int height)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewNodeForElement(element._com, x, y, width, height))))

    def create_diagram_view(self, name: str) -> "RPGraphElement":
        """Creates a diagram view with the specified name.

        Args:
            name: The name of the diagram view.

        Returns:
            The wrapped graph element created.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::createDiagramView(java.lang.String name)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.createDiagramView(name))))

    def get_diagram_view_of(self, name: str) -> "RPGraphElement":
        """Returns the diagram view with the specified name.

        Args:
            name: The name of the diagram view.

        Returns:
            The wrapped graph element, or None if not found.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getDiagramViewOf(java.lang.String name)
        """
        result = AbstractRPModelElement.call_com(lambda: self._com.getDiagramViewOf(name))
        return cast("RPGraphElement", AbstractRPModelElement.wrap(result)) if result else None

    def get_diagram_views(self) -> RPCollection:
        """Returns the diagram views for this diagram.

        Returns:
            An ``RPCollection`` of diagram views.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getDiagramViews()
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getDiagramViews()))

    def is_diagram_view(self) -> int:
        """Checks if this is a diagram view.

        Returns:
            1 if this is a diagram view, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::isDiagramView()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.isDiagramView()))

    def open_diagram_view(self, name: str) -> None:
        """Opens the diagram view with the specified name.

        Args:
            name: The name of the diagram view to open.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::openDiagramView(java.lang.String name)
        """
        AbstractRPModelElement.call_com(lambda: self._com.openDiagramView(name))

    def rearrange_ports(self) -> None:
        """Rearranges the ports on the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::rearrangePorts()
        """
        AbstractRPModelElement.call_com(lambda: self._com.rearrangePorts())

    def set_custom_views(self, views: RPCollection) -> None:
        """Sets the custom views for this diagram.

        Args:
            views: The collection of custom views.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::setCustomViews(com.telelogic.rhapsody.core.IRPCollection views)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setCustomViews(views._com))

    def update_view_on_server(self) -> None:
        """Updates the view on the server.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::updateViewOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateViewOnServer())

    def complete_relations(self) -> None:
        """Completes the relations in the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::completeRelations()
        """
        AbstractRPModelElement.call_com(lambda: self._com.completeRelations())

    def get_elements_in_diagram(self) -> RPCollection:
        """Returns the model elements in this diagram.

        Returns:
            An ``RPCollection`` of model elements.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getElementsInDiagram()
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getElementsInDiagram()))

    def get_graphical_elements(self) -> RPCollection:
        """Returns the graphical elements in this diagram.

        Returns:
            An ``RPCollection`` of graphical elements.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getGraphicalElements()
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getGraphicalElements()))

    def get_last_visualization_modified_time(self) -> str:
        """Returns the last visualization modified time.

        Returns:
            The last visualization modified time as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getLastVisualizationModifiedTime()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getLastVisualizationModifiedTime", "lastVisualizationModifiedTime"))

    def get_picture(self) -> "RPGraphElement":
        """Returns the picture for this diagram.

        Returns:
            The wrapped graph element representing the picture.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getPicture()
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.getPicture())))

    def get_picture_as(self, format_: str) -> "RPGraphElement":
        """Returns the picture in the specified format.

        Args:
            format_: The format for the picture.

        Returns:
            The wrapped graph element representing the picture.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getPictureAs(java.lang.String format)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.getPictureAs(format_))))

    def get_picture_as_divided_metafiles(self) -> RPCollection:
        """Returns the picture as divided metafiles.

        Returns:
            An ``RPCollection`` of graph elements.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getPictureAsDividedMetafiles()
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getPictureAsDividedMetafiles()))

    def get_picture_ex(self, x: int, y: int, width: int, height: int) -> "RPGraphElement":
        """Returns a picture for the specified region.

        Args:
            x: The X coordinate.
            y: The Y coordinate.
            width: The width.
            height: The height.

        Returns:
            The wrapped graph element representing the picture.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getPictureEx(int x, int y, int width, int height)
        """
        return cast("RPGraphElement", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.getPictureEx(x, y, width, height))))

    def get_pictures_with_image_map(self, first_file_name: str, diagram_map: "RPCollection") -> "RPCollection":
        """Saves the diagram as EMF file(s) and populates the given collection with image-map info.

        Saves the diagram as an EMF format file, breaking the diagram into a number of
        files if necessary (based on the ``General:Graphics:ExportedDiagramScale`` property).
        The ``diagram_map`` collection is populated with ``IRPImageMap`` objects containing
        the information needed to construct an HTML image map.

        Args:
            first_file_name: The base name for the created EMF file(s). If multiple files
                are created, names follow the convention ``firstFileNameZ_X_Y``.
            diagram_map: An empty ``RPCollection`` (obtainable via
                ``RhapsodyApplication.create_new_collection()``) that will be populated
                with ``IRPImageMap`` objects.

        Returns:
            An ``RPCollection`` containing the names of the files that were created.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::getPicturesWithImageMap(
                java.lang.String firstFileName, com.telelogic.rhapsody.core.IRPCollection diagrammap)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getPicturesWithImageMap(first_file_name, diagram_map._com)))

    def is_open(self) -> int:
        """Checks if the diagram is open.

        Returns:
            1 if the diagram is open, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::isOpen()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.isOpen()))

    def is_show_diagram_frame(self) -> int:
        """Checks if the diagram frame is shown.

        Returns:
            1 if the diagram frame is shown, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::isShowDiagramFrame()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.isShowDiagramFrame()))

    def open_diagram(self) -> None:
        """Opens the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::openDiagram()
        """
        AbstractRPModelElement.call_com(lambda: self._com.openDiagram())

    def populate_diagram(self) -> None:
        """Populates the diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::populateDiagram()
        """
        AbstractRPModelElement.call_com(lambda: self._com.populateDiagram())

    def remove_graph_elements(self, elements: RPCollection) -> None:
        """Removes the specified graph elements from the diagram.

        Args:
            elements: The collection of graph elements to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::removeGraphElements(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeGraphElements(elements._com))

    def set_show_diagram_frame(self, show: int) -> None:
        """Sets whether to show the diagram frame.

        Args:
            show: 1 to show the frame, 0 to hide it.

        Reference:
            com.telelogic.rhapsody.core.IRPDiagram::setShowDiagramFrame(int show)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setShowDiagramFrame(show))


AbstractRPModelElement.register_wrapper("ActivityDiagram", RPDiagram)
