"""Graphics model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.interactions.model_interactions import RPMessage
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPStateVertex

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.activity.model_activity import RPFlow, RPSwimlane
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
    from rhapsody_cli.models.elements.common.model_other_model import (
        RPClassifierRole,
        RPSysMLPort,
    )
    from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
    from rhapsody_cli.models.elements.interactions.model_interactions import (
        RPInteractionOccurrence,
        RPInteractionOperator,
        RPTransition,
    )
    from rhapsody_cli.models.elements.relations.model_instance import RPInstance
    from rhapsody_cli.models.elements.relations.model_port import RPPort
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation
    from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState


class RPConditionMark(RPMessage):
    """Wraps ``IRPConditionMark``: represents condition marks in sequence diagrams."""

    # IRPConditionMark method parity checklist:
    # [inherited] IRPMessage methods (covered by RPMessage checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPConditionMark methods.

    pass


class RPConnector(RPStateVertex):
    """Wraps ``IRPConnector``: represents connector elements in a statechart.

    Includes condition connectors, history connectors, join sync bar connectors,
    and fork sync bar connectors.
    """

    # IRPConnector method parity checklist:
    # [ ] createDefaultTransition      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getConnectorType             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getDerivedInEdges            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getDerivedOutEdge            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getItsSwimlane               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getOfState                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isConditionConnector         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isDiagramConnector           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isForkConnector              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isHistoryConnector           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isJoinConnector              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isJunctionConnector          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isStubConnector              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isTerminationConnector       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setItsSwimlane               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setOfState                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # No deprecated IRPConnector methods.

    def create_default_transition(self, from_: "RPState") -> "RPTransition":
        """Creates a default transition leading to this connector, within the state specified.

        Args:
            from_: The state for which the default transition should be created.

        Returns:
            The default transition that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::createDefaultTransition(com.telelogic.rhapsody.core.IRPState from)
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.createDefaultTransition(from_._com)))

    def get_connector_type(self) -> str:
        """Returns the type of the connector.

        Returns:
            The type of the connector: Condition, Diagram, EnterExit, Fork,
            History, Join, Junction, Termination, InPin, OutPin, or InOutPin.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getConnectorType()
        """
        return self._get_method_or_property(self._com, "getConnectorType", "connectorType")

    def get_derived_in_edges(self) -> RPCollection:
        """Returns a collection of the transitions coming into the connector.

        Returns:
            The transitions coming into the connector (a collection of
            IRPTransition elements).

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getDerivedInEdges()
        """
        return RPCollection(self.call_com(lambda: self._com.getDerivedInEdges()))

    def get_derived_out_edge(self) -> "RPTransition":
        """Returns the transition exiting the connector.

        Returns:
            The transition exiting the connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getDerivedOutEdge()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getDerivedOutEdge()))

    def get_its_swimlane(self) -> "RPSwimlane":
        """For connectors in a swimlane, returns the swimlane that contains the connector.

        Returns:
            The swimlane that contains the connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getItsSwimlane()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getItsSwimlane()))

    def get_of_state(self) -> "RPState":
        """For history connectors, returns the state that the history connector belongs to.

        Returns:
            The state that this history connector belongs to.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getOfState()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getOfState()))

    def is_condition_connector(self) -> int:
        """Checks whether the connector is a condition connector.

        Returns:
            1 if the connector is a condition connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isConditionConnector()
        """
        return int(self.call_com(lambda: self._com.isConditionConnector()))

    def is_diagram_connector(self) -> int:
        """Checks whether the connector is a diagram connector.

        Returns:
            1 if the connector is a diagram connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isDiagramConnector()
        """
        return int(self.call_com(lambda: self._com.isDiagramConnector()))

    def is_fork_connector(self) -> int:
        """Checks whether the connector is a fork sync bar connector.

        Returns:
            1 if the connector is a fork sync bar connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isForkConnector()
        """
        return int(self.call_com(lambda: self._com.isForkConnector()))

    def is_history_connector(self) -> int:
        """Checks whether the connector is a history connector.

        Returns:
            1 if the connector is a history connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isHistoryConnector()
        """
        return int(self.call_com(lambda: self._com.isHistoryConnector()))

    def is_join_connector(self) -> int:
        """Checks whether the connector is a join sync bar connector.

        Returns:
            1 if the connector is a join sync bar connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isJoinConnector()
        """
        return int(self.call_com(lambda: self._com.isJoinConnector()))

    def is_junction_connector(self) -> int:
        """Checks whether the connector is a junction connector.

        Returns:
            1 if the connector is a junction connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isJunctionConnector()
        """
        return int(self.call_com(lambda: self._com.isJunctionConnector()))

    def is_stub_connector(self) -> int:
        """Checks whether the connector is an EnterExit point.

        Returns:
            1 if the connector is an EnterExit point, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isStubConnector()
        """
        return int(self.call_com(lambda: self._com.isStubConnector()))

    def is_termination_connector(self) -> int:
        """Checks whether the connector is a termination connector.

        Returns:
            1 if the connector is a termination connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isTerminationConnector()
        """
        return int(self.call_com(lambda: self._com.isTerminationConnector()))

    def set_its_swimlane(self, p_val: "RPSwimlane") -> None:
        """Specifies the swimlane that should contain this connector.

        Args:
            p_val: The swimlane that should contain this connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::setItsSwimlane(com.telelogic.rhapsody.core.IRPSwimlane pVal)
        """
        self.call_com(lambda: self._com.setItsSwimlane(p_val._com))

    def set_of_state(self, of_state: "RPState") -> None:
        """For history connectors, specifies the state for which the connector should maintain historical state information.

        Args:
            of_state: The state for which the connector should maintain
                historical state information.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::setOfState(com.telelogic.rhapsody.core.IRPState OfState)
        """
        self.call_com(lambda: self._com.setOfState(of_state._com))


class RPGraphElement(RPModelElement):
    """Wraps ``IRPGraphElement``."""

    # IRPGraphElement method parity checklist:
    # [ ] addProperty                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] applyDefaultFormat           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getAllGraphicalProperties    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getAllProperties             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getAssociatedImage           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getDiagram                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getGraphicalParent           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getGraphicalProperty         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getGraphicalPropertyOfText   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getImageLayout               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getLocalProperties           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getModelObject               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPropertyValue             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getSelectedImage             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] removeProperty               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setAssociatedImage           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setGraphicalProperty         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setGraphicalPropertyOfText   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setImageLayout               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setPropertyValue             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setSelectedImage             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # No deprecated IRPGraphElement methods.

    def add_property(self, property_key: str, property_type: str, property_value: str) -> None:
        """Adds a property to this graph element.

        Args:
            property_key: The property key.
            property_type: The property type.
            property_value: The property value.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::addProperty(java.lang.String propertyKey, java.lang.String propertyType, java.lang.String propertyValue)
        """
        self.call_com(lambda: self._com.addProperty(property_key, property_type, property_value))

    def apply_default_format(self) -> None:
        """Applies the default format to this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::applyDefaultFormat()
        """
        self.call_com(lambda: self._com.applyDefaultFormat())

    def get_all_graphical_properties(self) -> RPCollection:
        """Returns all graphical properties of this graph element.

        Returns:
            A collection of all graphical properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAllGraphicalProperties()
        """
        return RPCollection(self.call_com(lambda: self._com.getAllGraphicalProperties()))

    def get_all_properties(self) -> RPCollection:
        """Returns all properties of this graph element.

        Returns:
            A collection of all properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAllProperties()
        """
        return RPCollection(self.call_com(lambda: self._com.getAllProperties()))

    def get_associated_image(self) -> str:
        """Returns the associated image of this graph element.

        Returns:
            The associated image.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAssociatedImage()
        """
        return self._get_method_or_property(self._com, "getAssociatedImage", "associatedImage")

    def get_diagram(self) -> "RPDiagram":
        """Returns the diagram that contains this graph element.

        Returns:
            The diagram that contains this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getDiagram()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getDiagram()))

    def get_graphical_parent(self) -> "RPGraphElement":
        """Returns the graphical parent of this graph element.

        Returns:
            The graphical parent of this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getGraphicalParent()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getGraphicalParent()))

    def get_graphical_property(self, name: str) -> "RPGraphicalProperty":
        """Returns the specified graphical property of this graph element.

        Args:
            name: The name of the graphical property.

        Returns:
            The graphical property with the specified name.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getGraphicalProperty(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getGraphicalProperty(name)))

    def get_graphical_property_of_text(self, text_name: str, name: str) -> "RPGraphicalProperty":
        """Returns the specified graphical property for a textual element associated with the graphic element.

        Args:
            text_name: The specific textual element that you want the property
                for.
            name: The name of the graphical property, for example,
                "TextFontName", "TextColor", "TextFontItalic", "TextFontSize",
                "TextFontBold".

        Returns:
            The graphical property that was requested.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getGraphicalPropertyOfText(java.lang.String textName, java.lang.String name)
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getGraphicalPropertyOfText(text_name, name)))

    def get_image_layout(self) -> str:
        """Returns the image layout specified for the image linked to the graphic element.

        Returns:
            The image layout specified for the image linked to the graphic
            element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getImageLayout()
        """
        return self._get_method_or_property(self._com, "getImageLayout", "imageLayout")

    def get_interface_name(self) -> str:
        """Returns the interface name of this graph element.

        Returns:
            The interface name of this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getInterfaceName()
        """
        return self._get_method_or_property(self._com, "getInterfaceName", "interfaceName")

    def get_local_properties(self) -> RPCollection:
        """Returns the local properties of this graph element.

        Returns:
            A collection of the local properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getLocalProperties()
        """
        return RPCollection(self.call_com(lambda: self._com.getLocalProperties()))

    def get_model_object(self) -> "RPModelElement":
        """Returns the model object associated with this graph element.

        Returns:
            The model object associated with this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getModelObject()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getModelObject()))

    def get_property_value(self, property_key: str) -> str:
        """Returns the value of the specified property.

        Args:
            property_key: The key of the property whose value should be returned.

        Returns:
            The value of the specified property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getPropertyValue(java.lang.String propertyKey)
        """
        return self.call_com(lambda: self._com.getPropertyValue(property_key))

    def get_selected_image(self) -> str:
        """Returns the full path of the image that was linked to the graphic element.

        Returns:
            The full path of the image linked to the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getSelectedImage()
        """
        return self._get_method_or_property(self._com, "getSelectedImage", "selectedImage")

    def remove_property(self, property_key: str) -> None:
        """Removes the specified property from this graph element.

        Args:
            property_key: The key of the property to remove.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::removeProperty(java.lang.String propertyKey)
        """
        self.call_com(lambda: self._com.removeProperty(property_key))

    def set_associated_image(self, associated_image: str) -> None:
        """Sets the associated image for this graph element.

        Args:
            associated_image: The associated image to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setAssociatedImage(java.lang.String associatedImage)
        """
        self._set_method_or_property(self._com, "setAssociatedImage", "associatedImage", associated_image)

    def set_graphical_property(self, name: str, value: str) -> None:
        """Sets a new value for a graphical property.

        Args:
            name: The name of the graphical property to set.
            value: The value to use for the specified property.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setGraphicalProperty(java.lang.String name, java.lang.String value)
        """
        self.call_com(lambda: self._com.setGraphicalProperty(name, value))

    def set_graphical_property_of_text(self, text_name: str, name: str, value: str) -> None:
        """Sets a new value for a graphical property for the specified textual element associated with the graphic element.

        Args:
            text_name: The specific textual element that you want to set the
                property for.
            name: The name of the graphical property to set.
            value: The value to use for the specified property.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setGraphicalPropertyOfText(java.lang.String textName, java.lang.String name, java.lang.String value)
        """
        self.call_com(lambda: self._com.setGraphicalPropertyOfText(text_name, name, value))

    def set_image_layout(self, image_layout: str) -> None:
        """Specifies the image layout that should be used for the image linked to the graphic element.

        Args:
            image_layout: The image layout that should be used for the image
                linked to the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setImageLayout(java.lang.String imageLayout)
        """
        self._set_method_or_property(self._com, "setImageLayout", "imageLayout", image_layout)

    def set_property_value(self, property_key: str, property_value: str) -> None:
        """Sets the value of the specified property.

        Args:
            property_key: The key of the property to set.
            property_value: The value to use for the specified property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setPropertyValue(java.lang.String propertyKey, java.lang.String propertyValue)
        """
        self.call_com(lambda: self._com.setPropertyValue(property_key, property_value))

    def set_selected_image(self, selected_image: str) -> None:
        """Links the graphic element to the image represented by the path specified.

        Args:
            selected_image: The full path to the image that should be linked to
                the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setSelectedImage(java.lang.String selectedImage)
        """
        self._set_method_or_property(self._com, "setSelectedImage", "selectedImage", selected_image)


class RPGraphicalProperty(RPModelElement):
    """Wraps ``IRPGraphicalProperty``."""

    # IRPGraphicalProperty method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getKey                       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getValue                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # No deprecated IRPGraphicalProperty methods.

    def get_interface_name(self) -> str:
        """Returns the interface name of this graphical property.

        Returns:
            The interface name of this graphical property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphicalProperty::getInterfaceName()
        """
        return self._get_method_or_property(self._com, "getInterfaceName", "interfaceName")

    def get_key(self) -> str:
        """Returns the key of this graphical property.

        Returns:
            The key of this graphical property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphicalProperty::getKey()
        """
        return self._get_method_or_property(self._com, "getKey", "key")

    def get_value(self) -> str:
        """Returns the value of this graphical property.

        Returns:
            The value of this graphical property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphicalProperty::getValue()
        """
        return self._get_method_or_property(self._com, "getValue", "value")


class RPImageMap(RPModelElement):
    """Wraps ``IRPImageMap``."""

    # IRPImageMap method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsGUID                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getName                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPictureFileName           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPoints                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getShape                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # No deprecated IRPImageMap methods.

    def get_interface_name(self) -> str:
        """Returns the interface name of this image map.

        Returns:
            The interface name of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getInterfaceName()
        """
        return self._get_method_or_property(self._com, "getInterfaceName", "interfaceName")

    def get_is_guid(self) -> int:
        """Returns whether this image map uses a GUID.

        Returns:
            Whether this image map uses a GUID.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getIsGUID()
        """
        return int(self._get_method_or_property(self._com, "getIsGUID", "isGUID"))

    def get_name(self) -> str:
        """Returns the name of this image map.

        Returns:
            The name of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getName()
        """
        return self._get_method_or_property(self._com, "getName", "name")

    def get_picture_file_name(self) -> str:
        """Returns the picture file name of this image map.

        Returns:
            The picture file name of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getPictureFileName()
        """
        return self._get_method_or_property(self._com, "getPictureFileName", "pictureFileName")

    def get_points(self) -> str:
        """Returns the points of this image map.

        Returns:
            The points of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getPoints()
        """
        return self._get_method_or_property(self._com, "getPoints", "points")

    def get_shape(self) -> str:
        """Returns the shape of this image map.

        Returns:
            The shape of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getShape()
        """
        return self._get_method_or_property(self._com, "getShape", "shape")

    def get_target(self) -> str:
        """Returns the target of this image map.

        Returns:
            The target of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getTarget()
        """
        return self._get_method_or_property(self._com, "getTarget", "target")


class RPLink(RPUnit):
    """Wraps ``IRPLink``: represents links in Rhapsody models."""

    # IRPLink method parity checklist:
    # [ ] getEnd1Multiplicity          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getEnd1Name                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getEnd2Multiplicity          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getEnd2Name                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFrom                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElement               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromPort                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromSysMLPort             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getInstantiates              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getOther                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getTo                        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElement                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToPort                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToSysMLPort               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setEnd1Multiplicity          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setEnd1Name                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setEnd2Multiplicity          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setEnd2Name                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setInstantiates              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPLink methods.

    def get_end1_multiplicity(self) -> str:
        """Returns the multiplicity of the first end of this link.

        Returns:
            The multiplicity of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd1Multiplicity()
        """
        return self._get_method_or_property(self._com, "getEnd1Multiplicity", "end1Multiplicity")

    def get_end1_name(self) -> str:
        """Returns the name of the first end of this link.

        Returns:
            The name of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd1Name()
        """
        return self._get_method_or_property(self._com, "getEnd1Name", "end1Name")

    def get_end2_multiplicity(self) -> str:
        """Returns the multiplicity of the second end of this link.

        Returns:
            The multiplicity of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd2Multiplicity()
        """
        return self._get_method_or_property(self._com, "getEnd2Multiplicity", "end2Multiplicity")

    def get_end2_name(self) -> str:
        """Returns the name of the second end of this link.

        Returns:
            The name of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd2Name()
        """
        return self._get_method_or_property(self._com, "getEnd2Name", "end2Name")

    def get_from(self) -> "RPInstance":
        """Returns the source instance of this link.

        Returns:
            The source instance of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFrom()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFrom()))

    def get_from_element(self) -> "RPModelElement":
        """Returns the source element of this link.

        Returns:
            The source element of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromElement()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFromElement()))

    def get_from_port(self) -> "RPPort":
        """Returns the source port of this link.

        Returns:
            The source port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromPort()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFromPort()))

    def get_from_sys_ml_port(self) -> "RPSysMLPort":
        """Returns the source SysML port of this link.

        Returns:
            The source SysML port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromSysMLPort()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFromSysMLPort()))

    def get_instantiates(self) -> "RPRelation":
        """Returns the relation that this link instantiates.

        Returns:
            The relation that this link instantiates.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getInstantiates()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getInstantiates()))

    def get_other(self) -> "RPLink":
        """Returns the other link in a bidirectional relationship.

        Returns:
            The other link in a bidirectional relationship.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getOther()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getOther()))

    def get_to(self) -> "RPInstance":
        """Returns the target of a link.

        Returns:
            The target of the link.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getTo()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getTo()))

    def get_to_element(self) -> "RPModelElement":
        """Returns the target element of this link.

        Returns:
            The target element of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToElement()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getToElement()))

    def get_to_port(self) -> "RPPort":
        """Returns the port through which a link reaches a target object.

        Returns:
            The port through which the link reaches its target object.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToPort()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getToPort()))

    def get_to_sys_ml_port(self) -> "RPSysMLPort":
        """Returns the target SysML port of this link.

        Returns:
            The target SysML port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToSysMLPort()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getToSysMLPort()))

    def set_end1_multiplicity(self, end1_multiplicity: str) -> None:
        """Sets the multiplicity of the first end of this link.

        Args:
            end1_multiplicity: The multiplicity of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd1Multiplicity(java.lang.String end1Multiplicity)
        """
        self._set_method_or_property(self._com, "setEnd1Multiplicity", "end1Multiplicity", end1_multiplicity)

    def set_end1_name(self, end1_name: str) -> None:
        """Sets the name of the first end of this link.

        Args:
            end1_name: The name of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd1Name(java.lang.String end1Name)
        """
        self._set_method_or_property(self._com, "setEnd1Name", "end1Name", end1_name)

    def set_end2_multiplicity(self, end2_multiplicity: str) -> None:
        """Sets the multiplicity of the second end of this link.

        Args:
            end2_multiplicity: The multiplicity of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd2Multiplicity(java.lang.String end2Multiplicity)
        """
        self._set_method_or_property(self._com, "setEnd2Multiplicity", "end2Multiplicity", end2_multiplicity)

    def set_end2_name(self, end2_name: str) -> None:
        """Sets the name of the second end of this link.

        Args:
            end2_name: The name of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd2Name(java.lang.String end2Name)
        """
        self._set_method_or_property(self._com, "setEnd2Name", "end2Name", end2_name)

    def set_instantiates(self, p_val: "RPRelation") -> None:
        """Sets the relation that this link instantiates.

        Args:
            p_val: The relation that this link should instantiate.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setInstantiates(com.telelogic.rhapsody.core.IRPRelation pVal)
        """
        self.call_com(lambda: self._com.setInstantiates(p_val._com))


class RPMatrixLayout(RPUnit):
    """Wraps ``IRPMatrixLayout``."""

    # IRPMatrixLayout method parity checklist:
    # [ ] getCellElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypes            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setCellElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypes            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPMatrixLayout methods.

    def get_cell_element_types(self) -> RPCollection:
        """Returns a collection of the element types that were specified to be displayed in the cells of the matrix.

        Returns:
            The element types that were specified to be displayed in the cells
            of the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getCellElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getCellElementTypes()))

    def get_from_element_types(self) -> RPCollection:
        """Returns a collection of the "from" element types specified to be displayed in the matrix.

        Returns:
            The "from" element types specified to be displayed in the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getFromElementTypes()))

    def get_from_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query that was specified to determine the "from" element types.

        Returns:
            The query that was specified to determine the "from" element types
            for the matrix layout.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypesQueryToUse()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFromElementTypesQueryToUse()))

    def get_from_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or collection of element types was used to specify the "from" element types.

        Returns:
            One of the constants contained in the class
            IRPMatrixLayout.QueryOrElementsList: QUERY if a query was used,
            ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypesUseQueryOrElementsList()
        """
        return int(self.call_com(lambda: self._com.getFromElementTypesUseQueryOrElementsList()))

    def get_to_element_types(self) -> RPCollection:
        """Returns a collection of the "to" element types specified to be displayed in the matrix.

        Returns:
            The "to" element types specified to be displayed in the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getToElementTypes()))

    def get_to_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query that was specified to determine the "to" element types.

        Returns:
            The query that was specified to determine the "to" element types
            for the matrix layout.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypesQueryToUse()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getToElementTypesQueryToUse()))

    def get_to_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or collection of element types was used to specify the "to" element types.

        Returns:
            One of the constants contained in the class
            IRPMatrixLayout.QueryOrElementsList: QUERY if a query was used,
            ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypesUseQueryOrElementsList()
        """
        return int(self.call_com(lambda: self._com.getToElementTypesUseQueryOrElementsList()))

    def set_cell_element_types(self, p_collection: RPCollection) -> None:
        """Specifies the element types to display in the cells of the matrix.

        Args:
            p_collection: The element types to display in the cells of the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setCellElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setCellElementTypes(p_collection._com))

    def set_from_element_types(self, p_collection: RPCollection) -> None:
        """Specifies the "from" element types that should be displayed in the matrix.

        Args:
            p_collection: The "from" element types that should be displayed in the
                matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setFromElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setFromElementTypes(p_collection._com))

    def set_from_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query to use to determine the "from" element types for the matrix layout.

        Args:
            query: The query to use to determine the "from" element types for
                the matrix layout. To clear a previous query, use null.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setFromElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        self.call_com(lambda: self._com.setFromElementTypesQueryToUse(query._com if query is not None else None))

    def set_from_element_types_use_query_or_elements_list(self, query_or_elements_list: int) -> None:
        """Specifies whether a query or collection of element types should be used to determine the "from" element types.

        Args:
            query_or_elements_list: One of the constants contained in the class
                IRPMatrixLayout.QueryOrElementsList: QUERY if a query should be
                used, ELEMENTS_LIST if a collection of element types should be
                used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setFromElementTypesUseQueryOrElementsList(int queryOrElementsList)
        """
        self.call_com(lambda: self._com.setFromElementTypesUseQueryOrElementsList(query_or_elements_list))

    def set_to_element_types(self, p_collection: RPCollection) -> None:
        """Specifies the "to" element types that should be displayed in the matrix.

        Args:
            p_collection: The "to" element types that should be displayed in the
                matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setToElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setToElementTypes(p_collection._com))

    def set_to_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query to use to determine the "to" element types for the matrix layout.

        Args:
            query: The query to use to determine the "to" element types for the
                matrix layout. To clear a previous query, use null.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setToElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        self.call_com(lambda: self._com.setToElementTypesQueryToUse(query._com if query is not None else None))

    def set_to_element_types_use_query_or_elements_list(self, query_or_elements_list: int) -> None:
        """Specifies whether a query or collection of element types should be used to determine the "to" element types.

        Args:
            query_or_elements_list: One of the constants contained in the class
                IRPMatrixLayout.QueryOrElementsList: QUERY if a query should be
                used, ELEMENTS_LIST if a collection of element types should be
                used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setToElementTypesUseQueryOrElementsList(int queryOrElementsList)
        """
        self.call_com(lambda: self._com.setToElementTypesUseQueryOrElementsList(query_or_elements_list))


class RPMatrixView(RPUnit):
    """Wraps ``IRPMatrixView``: represents Matrix View elements in Rhapsody models."""

    # IRPMatrixView method parity checklist:
    # [ ] getCellElements              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getCellString                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getContent                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromScope                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getHTMLContent               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getImageCollection           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getItsMatrixLayout           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRowCount                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToScope                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromScope                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setItsMatrixLayout           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToScope                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] updateViewOnServer           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIncludeDescendantsFromScope [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIncludeDescendantsToScope [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIncludeDescendantsFromScope [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIncludeDescendantsToScope [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPMatrixView methods.

    def get_cell_elements(self, row: int, column: int) -> RPCollection:
        """Returns the model elements contained in the specified cell.

        Args:
            row: The number of the row that the cell is in - row count begins
                at zero.
            column: The number of the column that the cell is in - column count
                begins at zero.

        Returns:
            The model elements contained in the specified cell.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getCellElements(int row, int column)
        """
        return RPCollection(self.call_com(lambda: self._com.getCellElements(row, column)))

    def get_cell_string(self, row: int, column: int) -> str:
        """Returns the text contained in the specified cell.

        Args:
            row: The number of the row that the cell is in - row count begins
                at zero.
            column: The number of the column that the cell is in - column count
                begins at zero.

        Returns:
            The text contained in the specified cell.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getCellString(int row, int column)
        """
        return self.call_com(lambda: self._com.getCellString(row, column))

    def get_column_count(self) -> int:
        """Returns the number of columns in the matrix.

        Returns:
            The number of columns in the matrix.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getColumnCount()
        """
        return int(self._get_method_or_property(self._com, "getColumnCount", "columnCount"))

    def get_content(self, format_: str) -> str:
        """Retrieves the content of the matrix in the specified format.

        Args:
            format_: One of the formats defined in the class
                IRPMatrixView.ContentFormat, for example,
                IRPMatrixView.ContentFormat.CSV.

        Returns:
            The content of the matrix in the specified format.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getContent(java.lang.String format)
        """
        return self.call_com(lambda: self._com.getContent(format_))

    def get_from_scope(self) -> RPCollection:
        """Returns the "from" scope of this matrix view.

        Returns:
            The "from" scope of this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getFromScope()
        """
        return RPCollection(self.call_com(lambda: self._com.getFromScope()))

    def get_html_content(self) -> str:
        """Returns the content of the matrix as HTML.

        Returns:
            The content of the matrix as HTML.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getHTMLContent()
        """
        return self._get_method_or_property(self._com, "getHTMLContent", "hTMLContent")

    def get_image_collection(self, s_folder: str, s_filename: str, s_extension: str) -> RPCollection:
        """Returns a collection of images for the matrix view.

        Args:
            s_folder: The folder path for the images.
            s_filename: The filename for the images.
            s_extension: The file extension for the images.

        Returns:
            A collection of images for the matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getImageCollection(java.lang.String sFolder, java.lang.String sFilename, java.lang.String sExtension)
        """
        return RPCollection(self.call_com(lambda: self._com.getImageCollection(s_folder, s_filename, s_extension)))

    def get_its_matrix_layout(self) -> "RPMatrixLayout":
        """Returns the matrix layout used by this matrix view.

        Returns:
            The matrix layout used by this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getItsMatrixLayout()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getItsMatrixLayout()))

    def get_row_count(self) -> int:
        """Returns the number of rows in the matrix.

        Returns:
            The number of rows in the matrix.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getRowCount()
        """
        return int(self._get_method_or_property(self._com, "getRowCount", "rowCount"))

    def get_to_scope(self) -> RPCollection:
        """Returns the "to" scope of this matrix view.

        Returns:
            The "to" scope of this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getToScope()
        """
        return RPCollection(self.call_com(lambda: self._com.getToScope()))

    def set_from_scope(self, p_collection: RPCollection) -> None:
        """Specifies the "from" scope to use for this matrix view.

        Args:
            p_collection: The "from" scope to use for this matrix view. Note that
                the parameter is a Rhapsody collection, but at the moment, only
                the first value in the collection is used for the "from" scope.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setFromScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setFromScope(p_collection._com))

    def set_its_matrix_layout(self, p_val: "RPMatrixLayout") -> None:
        """Specifies the matrix layout to use for this matrix view.

        Args:
            p_val: The matrix layout to use for this matrix view.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setItsMatrixLayout(com.telelogic.rhapsody.core.IRPMatrixLayout pVal)
        """
        self.call_com(lambda: self._com.setItsMatrixLayout(p_val._com))

    def set_to_scope(self, p_collection: RPCollection) -> None:
        """Specifies the "to" scope to use for this matrix view.

        Args:
            p_collection: The "to" scope to use for this matrix view. Note that
                the parameter is a Rhapsody collection, but at the moment, only
                the first value in the collection is used for the "to" scope.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setToScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setToScope(p_collection._com))

    def update_view_on_server(self, enforce_update: int) -> int:
        """Updates the view for the matrix on the Rhapsody Model Manager server.

        Args:
            enforce_update: Use 0 to specify that the view should be updated
                only if changes that affect the matrix were made since the last
                update. Use 1 to specify that the view should be updated
                regardless of whether or not changes were made.

        Returns:
            1 if the view for the matrix was updated on the server. If the
            matrix does not require an update, 0 is returned. If the update
            attempt failed, -1 is returned.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::updateViewOnServer(int enforceUpdate)
        """
        return int(self.call_com(lambda: self._com.updateViewOnServer(enforce_update)))

    def get_include_descendants_from_scope(self) -> int:
        """Returns whether descendants are included in the "from" scope.

        Returns:
            Whether descendants are included in the "from" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getIncludeDescendantsFromScope()
        """
        return int(self._get_method_or_property(self._com, "getIncludeDescendantsFromScope", "includeDescendantsFromScope"))

    def get_include_descendants_to_scope(self) -> int:
        """Returns whether descendants are included in the "to" scope.

        Returns:
            Whether descendants are included in the "to" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getIncludeDescendantsToScope()
        """
        return int(self._get_method_or_property(self._com, "getIncludeDescendantsToScope", "includeDescendantsToScope"))

    def open(self) -> None:
        """Opens this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::open()
        """
        self.call_com(lambda: self._com.open())

    def set_include_descendants_from_scope(self, include_descendants_from_scope: int) -> None:
        """Sets whether descendants are included in the "from" scope.

        Args:
            include_descendants_from_scope: Whether descendants should be included in the "from" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setIncludeDescendantsFromScope(int includeDescendantsFromScope)
        """
        self._set_method_or_property(self._com, "setIncludeDescendantsFromScope", "includeDescendantsFromScope", include_descendants_from_scope)

    def set_include_descendants_to_scope(self, include_descendants_to_scope: int) -> None:
        """Sets whether descendants are included in the "to" scope.

        Args:
            include_descendants_to_scope: Whether descendants should be included in the "to" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setIncludeDescendantsToScope(int includeDescendantsToScope)
        """
        self._set_method_or_property(self._com, "setIncludeDescendantsToScope", "includeDescendantsToScope", include_descendants_to_scope)


class RPMessagePoint(RPModelElement):
    """Wraps ``IRPMessagePoint``."""

    # IRPMessagePoint method parity checklist:
    # [ ] getClassifierRole            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getInteractionOccurrence     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getInteractionOperator       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getMessage                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # No deprecated IRPMessagePoint methods.

    def get_classifier_role(self) -> "RPClassifierRole":
        """Returns the classifier role associated with this message point.

        Returns:
            The classifier role associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getClassifierRole()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getClassifierRole()))

    def get_interaction_occurrence(self) -> "RPInteractionOccurrence":
        """Returns the interaction occurrence associated with this message point.

        Returns:
            The interaction occurrence associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getInteractionOccurrence()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getInteractionOccurrence()))

    def get_interaction_operator(self) -> "RPInteractionOperator":
        """Returns the interaction operator associated with this message point.

        Returns:
            The interaction operator associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getInteractionOperator()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getInteractionOperator()))

    def get_message(self) -> "RPMessage":
        """Returns the message associated with this message point.

        Returns:
            The message associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getMessage()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getMessage()))

    def get_type(self) -> str:
        """Returns the type of this message point.

        Returns:
            The type of this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getType()
        """
        return self._get_method_or_property(self._com, "getType", "type")


class RPTableLayout(RPUnit):
    """Wraps ``IRPTableLayout``."""

    # IRPTableLayout method parity checklist:
    # [ ] addColumn                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] addColumnEx                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getCollapseFirstColumn       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnContext             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnDefaultWidth        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationAllowNew [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationAllowSelect [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationCellType [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationDisplayProperty [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationGetterCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationImports [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationPickerCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnImplementationSetterCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnName                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnProperty            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnType                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumns                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getElementTypes              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRelationTable             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getResultList                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypes            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] removeColumn                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setCollapseFirstColumn       [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnContext             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnDefaultWidth        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationAllowNew [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationAllowSelect [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationCellType [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationDisplayProperty [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationGetterCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationImports [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationPickerCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnImplementationSetterCode [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnName                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnProperty            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setColumnType                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setElementTypes              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypes          [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setRelationTable             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypes            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPTableLayout methods.

    def add_column(self, type_: str, property: str, column_name: str) -> None:
        """Adds a new column to the table layout.

        Args:
            type_: The column type (equivalent to the Type field in the UI). Valid values are
                the constants defined in the class IRPTableLayout.Column, for example
                IRPTableLayout.Column.ANNOTATION_ATTRIBUTE.
            property: The column property (equivalent to the Property field in the UI). Valid
                values are the constants defined in the classes nested beneath
                IRPTableLayout.Column; the nested class used depends on the value of ``type_``.
            column_name: The text to use as the heading for the column.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::addColumn(java.lang.String type, java.lang.String Property, java.lang.String ColumnName)
        """
        self.call_com(lambda: self._com.addColumn(type_, property, column_name))

    def add_column_ex(self, type_: str, property: str, column_name: str, context: str) -> int:
        """Adds a new column to the table layout and returns its index.

        Differs from addColumn in that it also allows specifying a label from a context
        pattern and returns the index of the newly added column.

        Args:
            type_: The column type (one of the constants defined in IRPTableLayout.Column,
                for example IRPTableLayout.Column.GENERAL_ATTRIBUTE).
            property: The column property. Valid values are the constants defined in the classes
                nested under IRPTableLayout.Column and must match the column type.
            column_name: The text to use as the heading for the column.
            context: A label from the defined context pattern. Use an empty string if no
                context pattern label should be specified.

        Returns:
            The index of the newly created column (the index of the first column is 0).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::addColumnEx(java.lang.String type, java.lang.String Property, java.lang.String ColumnName, java.lang.String Context)
        """
        return int(self.call_com(lambda: self._com.addColumnEx(type_, property, column_name, context)))

    def get_collapse_first_column(self) -> int:
        """Checks whether the first column includes controls for collapsing and expanding rows.

        Returns:
            ``1`` if the first column includes collapse/expand controls, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getCollapseFirstColumn()
        """
        return int(self._get_method_or_property(self._com, "getCollapseFirstColumn", "collapseFirstColumn"))

    def get_column_context(self, index: int) -> str:
        """Returns the context pattern label specified for the column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The context pattern label that was specified for the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnContext(int Index)
        """
        return self.call_com(lambda: self._com.getColumnContext(index))

    def get_column_default_width(self, index: int) -> int:
        """Returns the default width defined for the specified column.

        Args:
            index: The index of the column whose default width should be returned
                (the index of the first column is 0).

        Returns:
            The default width defined for the specified column, in pixels.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnDefaultWidth(int Index)
        """
        return int(self.call_com(lambda: self._com.getColumnDefaultWidth(index)))

    def get_column_implementation_allow_new(self, index: int) -> int:
        """Checks whether the user-defined picker for the column includes the New option.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            ``1`` if the picker includes the New option, ``0`` if it does not.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationAllowNew(int Index)
        """
        return int(self.call_com(lambda: self._com.getColumnImplementationAllowNew(index)))

    def get_column_implementation_allow_select(self, index: int) -> int:
        """Checks whether the user-defined picker for the column includes the Select option.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            ``1`` if the picker includes the Select option, ``0`` if it does not.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationAllowSelect(int Index)
        """
        return int(self.call_com(lambda: self._com.getColumnImplementationAllowSelect(index)))

    def get_column_implementation_cell_type(self, index: int) -> str:
        """Returns the type of information displayed in the column's cells.

        The returned value is one of the constants defined in
        IRPTableLayout.Column.ImplementationCellType (string, model element, or list of
        model elements).

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The type of information displayed in the column's cells (one of the constants
            defined in IRPTableLayout.Column.ImplementationCellType, for example
            IRPTableLayout.Column.ImplementationCellType.MODEL_ELEMENT).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationCellType(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationCellType(index))

    def get_column_implementation_display_property(self, index: int) -> str:
        """Returns the element information displayed when the cell value type is model element or list.

        The returned value is one of the constants defined in
        IRPTableLayout.Column.GeneralAttribute.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The type of element information displayed when the cell value type is set to model
            element or list of model elements (one of the constants in
            IRPTableLayout.Column.GeneralAttribute, for example
            IRPTableLayout.Column.GeneralAttribute.NAME).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationDisplayProperty(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationDisplayProperty(index))

    def get_column_implementation_getter_code(self, index: int) -> str:
        """Returns the Java code for the getter of the cells in the specified column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The Java code for the getter of the cells in the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationGetterCode(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationGetterCode(index))

    def get_column_implementation_imports(self, index: int) -> str:
        """Returns the list of imports specified for a column with customized cell behavior.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            A comma-separated list of the imports specified for the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationImports(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationImports(index))

    def get_column_implementation_picker_code(self, index: int) -> str:
        """Returns the Java code for the picker of the cells in the specified column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The Java code for the picker of the cells in the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationPickerCode(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationPickerCode(index))

    def get_column_implementation_setter_code(self, index: int) -> str:
        """Returns the Java code for the setter of the cells in the specified column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The Java code for the setter of the cells in the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnImplementationSetterCode(int Index)
        """
        return self.call_com(lambda: self._com.getColumnImplementationSetterCode(index))

    def get_column_name(self, index: int) -> str:
        """Returns the name of the specified column.

        Args:
            index: The index of the column whose name should be returned
                (the index of the first column is 0).

        Returns:
            The name of the specified column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnName(int Index)
        """
        return self.call_com(lambda: self._com.getColumnName(index))

    def get_column_property(self, index: int) -> str:
        """Returns the property of the specified column.

        Corresponds to the Property field on the Columns tab for table layouts. The returned
        value is one of the constants defined in the classes nested under IRPTableLayout.Column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The property of the specified column (one of the constants defined in the classes
            nested under IRPTableLayout.Column, for example
            IRPTableLayout.Column.GeneralAttribute.NAME).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnProperty(int Index)
        """
        return self.call_com(lambda: self._com.getColumnProperty(index))

    def get_column_type(self, index: int) -> str:
        """Returns the type of the specified table column.

        The returned value is one of the constants defined in IRPTableLayout.Column.

        Args:
            index: The index of the column (the index of the first column is 0).

        Returns:
            The type of the table column (one of the constants defined in
            IRPTableLayout.Column, for example IRPTableLayout.Column.ANNOTATION_ATTRIBUTE).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnType(int Index)
        """
        return self.call_com(lambda: self._com.getColumnType(index))

    def get_columns(self) -> RPCollection:
        """Returns a collection of the columns in this table layout.

        Returns:
            An RPCollection of the columns in this table layout.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumns()
        """
        return RPCollection(self.call_com(lambda: self._com.getColumns()))

    def get_element_types(self) -> RPCollection:
        """Returns a collection of the element types displayed in the table.

        The collection consists of strings (from the list of types displayed on the
        ElementTypes tab of the Features window for table layouts).

        Returns:
            An RPCollection of the element types that were specified to be displayed in the table.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getElementTypes()))

    def get_from_element_types(self) -> RPCollection:
        """Returns the "from" element types for "relation tables".

        Returns a collection of the element types specified as the "from" element types. The
        collection consists of strings (from the From Element Types tab of the Features window).

        Returns:
            An RPCollection of the types specified as the "from" element types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getFromElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getFromElementTypes()))

    def get_from_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query used to determine the "from" element types for "relation tables".

        Returns:
            The query (an RPTableLayout) that was specified to determine the "from" element
            types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getFromElementTypesQueryToUse()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getFromElementTypesQueryToUse()))

    def get_from_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or element-types collection specifies the "from" element types.

        For "relation tables", checks whether a query or collection of element types was used
        to specify the "from" element types.

        Returns:
            One of the constants in IRPTableLayout.QueryOrElementsList: QUERY if a query was
            used, ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getFromElementTypesUseQueryOrElementsList()
        """
        return int(self.call_com(lambda: self._com.getFromElementTypesUseQueryOrElementsList()))

    def get_relation_table(self) -> int:
        """Checks whether the table was defined as a "relation table".

        Returns:
            ``1`` if the table was defined as a "relation table", ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getRelationTable()
        """
        return int(self._get_method_or_property(self._com, "getRelationTable", "relationTable"))

    def get_result_list(self, scope: "RPModelElement") -> RPCollection:
        """Returns the result list for the given scope.

        Args:
            scope: The scope (an IRPModelElement) for which to compute the result list.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getResultList(com.telelogic.rhapsody.core.IRPModelElement scope)
        """
        return RPCollection(self.call_com(lambda: self._com.getResultList(scope._com)))

    def get_to_element_types(self) -> RPCollection:
        """Returns the "to" element types for "relation tables".

        Returns a collection of the element types specified as the "to" element types. The
        collection consists of strings (from the To Element Types tab of the Features window).

        Returns:
            An RPCollection of the types specified as the "to" element types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getToElementTypes()
        """
        return RPCollection(self.call_com(lambda: self._com.getToElementTypes()))

    def get_to_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query used to determine the "to" element types for "relation tables".

        Returns:
            The query (an RPTableLayout) that was specified to determine the "to" element
            types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getToElementTypesQueryToUse()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getToElementTypesQueryToUse()))

    def get_to_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or element-types collection specifies the "to" element types.

        For "relation tables", checks whether a query or collection of element types was used
        to specify the "to" element types.

        Returns:
            One of the constants in IRPTableLayout.QueryOrElementsList: QUERY if a query was
            used, ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getToElementTypesUseQueryOrElementsList()
        """
        return int(self.call_com(lambda: self._com.getToElementTypesUseQueryOrElementsList()))

    def remove_column(self, index: int) -> None:
        """Removes the specified column from the table layout.

        Args:
            index: The index representing the position of the column in the table. The index
                for the first column in the table is 0.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::removeColumn(int Index)
        """
        self.call_com(lambda: self._com.removeColumn(index))

    def set_collapse_first_column(self, collapse: int) -> None:
        """Specifies whether the first column includes collapse/expand controls.

        Args:
            collapse: Use ``1`` if the first column should include collapse/expand controls,
                ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setCollapseFirstColumn(int collapse)
        """
        self._set_method_or_property(self._com, "setCollapseFirstColumn", "collapseFirstColumn", collapse)

    def set_column_context(self, index: int, context: str) -> None:
        """Specifies a context pattern label for the specified column.

        If a context pattern has been defined, this method specifies a label from that pattern
        for the column.

        Args:
            index: The index of the column (the index of the first column is 0).
            context: A label from the defined context pattern.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnContext(int Index, java.lang.String Context)
        """
        self.call_com(lambda: self._com.setColumnContext(index, context))

    def set_column_default_width(self, index: int, width: int) -> None:
        """Sets the default width of the specified column.

        If a user double-clicks the column border after manually changing the width, the width
        returns to this value.

        Args:
            index: The index of the column whose default width should be set
                (the index of the first column is 0).
            width: The default width to use for the column, in pixels.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnDefaultWidth(int Index, int width)
        """
        self.call_com(lambda: self._com.setColumnDefaultWidth(index, width))

    def set_column_implementation_allow_new(self, index: int, value: int) -> None:
        """Includes the New option in the picker for a column with customized cell behavior.

        For columns that use customized cell behavior, this method can include the New option
        in the list provided by the picker.

        Args:
            index: The index of the column (the index of the first column is 0).
            value: Use ``1`` if the New option should be included in the list, ``0`` if it
                should not.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationAllowNew(int Index, int value)
        """
        self.call_com(lambda: self._com.setColumnImplementationAllowNew(index, value))

    def set_column_implementation_allow_select(self, index: int, value: int) -> None:
        """Includes the Select option in the picker for a column with customized cell behavior.

        For columns that use customized cell behavior, this method can include the Select option
        in the list provided by the picker.

        Args:
            index: The index of the column (the index of the first column is 0).
            value: Use ``1`` if the Select option should be included in the list, ``0`` if it
                should not.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationAllowSelect(int Index, int value)
        """
        self.call_com(lambda: self._com.setColumnImplementationAllowSelect(index, value))

    def set_column_implementation_cell_type(self, index: int, cell_type: str) -> None:
        """Specifies the cell information type for a column with customized cell behavior.

        For columns that use customized cell behavior, this method specifies the type of
        information displayed in the column's cells (string, model element, or list of model
        elements).

        Args:
            index: The index of the column (the index of the first column is 0).
            cell_type: The type of information displayed in the column's cells. Valid values
                are the constants defined in IRPTableLayout.Column.ImplementationCellType,
                for example IRPTableLayout.Column.ImplementationCellType.MODEL_ELEMENT.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationCellType(int Index, java.lang.String cellType)
        """
        self.call_com(lambda: self._com.setColumnImplementationCellType(index, cell_type))

    def set_column_implementation_display_property(self, index: int, property_to_display: str) -> None:
        """Specifies the displayed element information for a column with customized cell behavior.

        For columns that use customized cell behavior, this method specifies the type of element
        information displayed when the cell value type is model element or list of model elements
        (for example, the name or value of the element).

        Args:
            index: The index of the column (the index of the first column is 0).
            property_to_display: The type of element information to display for the element or
                elements in the cell. Valid values are the constants defined in
                IRPTableLayout.Column.GeneralAttribute, such as
                IRPTableLayout.Column.GeneralAttribute.NAME.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationDisplayProperty(int Index, java.lang.String propertyToDisplay)
        """
        self.call_com(lambda: self._com.setColumnImplementationDisplayProperty(index, property_to_display))

    def set_column_implementation_getter_code(self, index: int, code: str) -> None:
        """Specifies the getter Java code for a column with customized cell behavior.

        Args:
            index: The index of the column (the index of the first column is 0).
            code: The Java code to use for the getter.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationGetterCode(int Index, java.lang.String code)
        """
        self.call_com(lambda: self._com.setColumnImplementationGetterCode(index, code))

    def set_column_implementation_imports(self, index: int, imports: str) -> None:
        """Specifies the imports for a column with customized cell behavior.

        For columns that use customized cell behavior, this method specifies the classes required
        by the code. Corresponds to the Imports field in the User Defined Implementation dialog.
        The list of imports should be comma-separated.

        Args:
            index: The index of the column (the index of the first column is 0).
            imports: A comma-separated list of classes to import.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationImports(int Index, java.lang.String imports)
        """
        self.call_com(lambda: self._com.setColumnImplementationImports(index, imports))

    def set_column_implementation_picker_code(self, index: int, code: str) -> None:
        """Specifies the picker Java code for a column with customized cell behavior.

        Args:
            index: The index of the column (the index of the first column is 0).
            code: The Java code to use for the picker.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationPickerCode(int Index, java.lang.String code)
        """
        self.call_com(lambda: self._com.setColumnImplementationPickerCode(index, code))

    def set_column_implementation_setter_code(self, index: int, code: str) -> None:
        """Specifies the setter Java code for a column with customized cell behavior.

        Args:
            index: The index of the column (the index of the first column is 0).
            code: The Java code to use for the setter.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnImplementationSetterCode(int Index, java.lang.String code)
        """
        self.call_com(lambda: self._com.setColumnImplementationSetterCode(index, code))

    def set_column_name(self, index: int, name: str) -> None:
        """Sets the name of the specified column.

        Args:
            index: The index of the column whose name should be set
                (the index of the first column is 0).
            name: The name to use for the column.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnName(int Index, java.lang.String name)
        """
        self.call_com(lambda: self._com.setColumnName(index, name))

    def set_column_property(self, index: int, property: str) -> None:
        """Sets the property of the specified column.

        Corresponds to the Property field on the Columns tab for table layouts. The value must
        match the column type.

        Args:
            index: The index of the column (the index of the first column is 0).
            property: The property to use for the specified column. Valid values are the
                constants defined in the classes nested under IRPTableLayout.Column, for example
                IRPTableLayout.Column.GeneralAttribute.NAME.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnProperty(int Index, java.lang.String Property)
        """
        self.call_com(lambda: self._com.setColumnProperty(index, property))

    def set_column_type(self, index: int, type_: str) -> None:
        """Sets the type of the specified table column.

        The type must be one of the constants defined in IRPTableLayout.Column.

        Args:
            index: The index of the column (the index of the first column is 0).
            type_: The type to use for the column (one of the constants defined in
                IRPTableLayout.Column, for example IRPTableLayout.Column.GENERAL_ATTRIBUTE).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setColumnType(int Index, java.lang.String type)
        """
        self.call_com(lambda: self._com.setColumnType(index, type_))

    def set_element_types(self, elements: RPCollection) -> None:
        """Specifies the element types displayed in the table.

        The parameter must be a collection of strings (from the list of types displayed on the
        ElementTypes tab of the Features window for table layouts).

        Args:
            elements: The element types that should be displayed in the table.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        self.call_com(lambda: self._com.setElementTypes(elements._com))

    def set_from_element_types(self, elements: RPCollection) -> None:
        """Specifies the "from" element types for "relation tables".

        For "relation tables", specifies the list of element types to use as the "from" element
        types. The parameter must be a collection of strings (from the From Element Types tab).

        Args:
            elements: Collection of element types to use as the "from" element types for the
                table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setFromElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        self.call_com(lambda: self._com.setFromElementTypes(elements._com))

    def set_from_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query used to determine the "from" element types for "relation tables".

        Args:
            query: The query to use to determine the "from" element types for the table layout.
                Use ``None`` to clear a previous query.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setFromElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        self.call_com(lambda: self._com.setFromElementTypesQueryToUse(query._com if query is not None else None))

    def set_from_element_types_use_query_or_elements_list(self, query_or_elements_list: int) -> None:
        """Specifies whether a query or element-types collection determines the "from" element types.

        For "relation tables", specifies whether a query or collection of element types should be
        used to determine the "from" element types.

        Args:
            query_or_elements_list: One of the constants in IRPTableLayout.QueryOrElementsList:
                QUERY if a query should be used, ELEMENTS_LIST if a collection of element types
                should be used.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setFromElementTypesUseQueryOrElementsList(int queryOrElementsList)
        """
        self.call_com(lambda: self._com.setFromElementTypesUseQueryOrElementsList(query_or_elements_list))

    def set_relation_table(self, relation: int) -> None:
        """Specifies whether the table is defined as a "relation table".

        Args:
            relation: Use ``1`` if the table should be defined as a "relation table", ``0``
                otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setRelationTable(int relation)
        """
        self._set_method_or_property(self._com, "setRelationTable", "relationTable", relation)

    def set_to_element_types(self, elements: RPCollection) -> None:
        """Specifies the "to" element types for "relation tables".

        For "relation tables", specifies the list of element types to use as the "to" element
        types. The parameter must be a collection of strings (from the To Element Types tab).

        Args:
            elements: Collection of element types to use as the "to" element types for the
                table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setToElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        self.call_com(lambda: self._com.setToElementTypes(elements._com))

    def set_to_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query used to determine the "to" element types for "relation tables".

        Args:
            query: The query to use to determine the "to" element types for the table layout.
                Use ``None`` to clear a previous query.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setToElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        self.call_com(lambda: self._com.setToElementTypesQueryToUse(query._com if query is not None else None))

    def set_to_element_types_use_query_or_elements_list(self, query_or_elements_list: int) -> None:
        """Specifies whether a query or element-types collection determines the "to" element types.

        For "relation tables", specifies whether a query or collection of element types should be
        used to determine the "to" element types.

        Args:
            query_or_elements_list: One of the constants in IRPTableLayout.QueryOrElementsList:
                QUERY if a query should be used, ELEMENTS_LIST if a collection of element types
                should be used.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setToElementTypesUseQueryOrElementsList(int queryOrElementsList)
        """
        self.call_com(lambda: self._com.setToElementTypesUseQueryOrElementsList(query_or_elements_list))

    def get_column_count(self) -> int:
        """Returns the number of columns in the table layout.

        Returns:
            The number of columns in the table layout.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnCount()
        """
        return int(self._get_method_or_property(self._com, "getColumnCount", "columnCount"))


class RPTableView(RPUnit):
    """Wraps ``IRPTableView``: represents Table View elements in Rhapsody models."""

    # IRPTableView method parity checklist:
    # [ ] getCellElements              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getCellString                [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getContent                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getHTMLContent               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getImageCollection           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getItsTableLayout            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRowCount                  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getScope                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getUseOwnerScope             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setItsTableLayout            [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setScope                     [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setUseOwnerScope             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] updateViewOnServer           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIncludeDescendants        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIncludeDescendants        [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPTableView methods.

    def get_cell_elements(self, row: int, column: int) -> RPCollection:
        """Returns the model elements contained in the specified cell.

        Args:
            row: The number of the row that the cell is in - row count begins
                at zero.
            column: The number of the column that the cell is in - column count
                begins at zero.

        Returns:
            The model elements contained in the specified cell.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getCellElements(int row, int column)
        """
        return RPCollection(self.call_com(lambda: self._com.getCellElements(row, column)))

    def get_cell_string(self, row: int, column: int) -> str:
        """Returns the text contained in the specified cell.

        Args:
            row: The number of the row that the cell is in - row count begins
                at zero.
            column: The number of the column that the cell is in - column count
                begins at zero.

        Returns:
            The text contained in the specified cell.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getCellString(int row, int column)
        """
        return self.call_com(lambda: self._com.getCellString(row, column))

    def get_column_count(self) -> int:
        """Returns the number of columns in the table.

        Returns:
            The number of columns in the table.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getColumnCount()
        """
        return int(self._get_method_or_property(self._com, "getColumnCount", "columnCount"))

    def get_content(self, format_: str) -> str:
        """Retrieves the content of the table in the specified format.

        Args:
            format_: One of the formats defined in the class
                IRPTableView.ContentFormat, for example,
                IRPTableView.ContentFormat.CSV.

        Returns:
            The content of the table in the specified format.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getContent(java.lang.String format)
        """
        return self.call_com(lambda: self._com.getContent(format_))

    def get_html_content(self) -> str:
        """Returns the content of the table as HTML.

        Returns:
            The content of the table as HTML.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getHTMLContent()
        """
        return self._get_method_or_property(self._com, "getHTMLContent", "hTMLContent")

    def get_image_collection(self, s_folder: str, s_filename: str, s_extension: str) -> RPCollection:
        """Returns a collection of images for the table view.

        Args:
            s_folder: The folder path for the images.
            s_filename: The filename for the images.
            s_extension: The file extension for the images.

        Returns:
            A collection of images for the table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getImageCollection(java.lang.String sFolder, java.lang.String sFilename, java.lang.String sExtension)
        """
        return RPCollection(self.call_com(lambda: self._com.getImageCollection(s_folder, s_filename, s_extension)))

    def get_its_table_layout(self) -> "RPTableLayout":
        """Returns the table layout used by this table view.

        Returns:
            The table layout used by this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getItsTableLayout()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getItsTableLayout()))

    def get_row_count(self) -> int:
        """Returns the number of rows in the table.

        Returns:
            The number of rows in the table.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getRowCount()
        """
        return int(self._get_method_or_property(self._com, "getRowCount", "rowCount"))

    def get_scope(self) -> RPCollection:
        """Returns the scope of this table view.

        Returns:
            The scope of this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getScope()
        """
        return RPCollection(self.call_com(lambda: self._com.getScope()))

    def get_use_owner_scope(self) -> int:
        """Checks whether the scope of the table view was defined as including the "owner" of the table view.

        Returns:
            1 if the scope of the table view was defined as including the
            "owner", 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getUseOwnerScope()
        """
        return int(self._get_method_or_property(self._com, "getUseOwnerScope", "useOwnerScope"))

    def set_its_table_layout(self, p_val: "RPTableLayout") -> None:
        """Specifies the table layout to use for this table view.

        Args:
            p_val: The table layout to use for this table view.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setItsTableLayout(com.telelogic.rhapsody.core.IRPTableLayout pVal)
        """
        self.call_com(lambda: self._com.setItsTableLayout(p_val._com))

    def set_scope(self, p_collection: RPCollection) -> None:
        """Specifies the scope to use for this table view.

        Args:
            p_collection: The scope to use for this table view. Note that the
                parameter is a Rhapsody collection, but at the moment, only the
                first value in the collection is used for the scope.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        self.call_com(lambda: self._com.setScope(p_collection._com))

    def set_use_owner_scope(self, p_val: int) -> None:
        """Specifies whether the scope of the table view should include the element that owns the table view.

        Args:
            p_val: Use 1 to have the scope of the table view include the owner,
                use 0 to clear the setting.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setUseOwnerScope(int pVal)
        """
        self._set_method_or_property(self._com, "setUseOwnerScope", "useOwnerScope", p_val)

    def update_view_on_server(self, enforce_update: int) -> int:
        """Updates the view for the table on the Rhapsody Model Manager server.

        Args:
            enforce_update: Use 0 to specify that the view should be updated
                only if changes that affect the table were made since the last
                update. Use 1 to specify that the view should be updated
                regardless of whether or not changes were made.

        Returns:
            1 if the view for the table was updated on the server. If the
            table does not require an update, 0 is returned. If the update
            attempt failed, -1 is returned.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::updateViewOnServer(int enforceUpdate)
        """
        return int(self.call_com(lambda: self._com.updateViewOnServer(enforce_update)))

    def get_include_descendants(self) -> int:
        """Returns whether descendants are included in the scope.

        Returns:
            Whether descendants are included in the scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getIncludeDescendants()
        """
        return int(self._get_method_or_property(self._com, "getIncludeDescendants", "includeDescendants"))

    def open(self) -> None:
        """Opens this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::open()
        """
        self.call_com(lambda: self._com.open())

    def set_include_descendants(self, include_descendants: int) -> None:
        """Sets whether descendants are included in the scope.

        Args:
            include_descendants: Whether descendants should be included in the scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setIncludeDescendants(int includeDescendants)
        """
        self._set_method_or_property(self._com, "setIncludeDescendants", "includeDescendants", include_descendants)


class RPPin(RPConnector):
    """Wraps ``IRPPin``: represents action pins added to actions, or activity parameters added to action blocks, in an activity diagram."""

    # IRPPin method parity checklist:
    # [ ] getIsParameter               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPinDirection              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPinType                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setIsParameter               [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setPinDirection              [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setPinType                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPConnector methods (covered by RPConnector checklist)
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPStateVertex methods (covered by RPStateVertex checklist)
    # No deprecated IRPPin methods.

    def get_is_parameter(self) -> int:
        """Checks whether the element is an activity parameter or an action pin.

        Returns:
            1 if the element is an activity parameter, 0 if the element is an
            action pin.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::getIsParameter()
        """
        return int(self._get_method_or_property(self._com, "getIsParameter", "isParameter"))

    def get_pin_direction(self) -> str:
        """Returns the direction of the pin/parameter: In, Out, or InOut.

        Returns:
            The direction of the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::getPinDirection()
        """
        return self._get_method_or_property(self._com, "getPinDirection", "pinDirection")

    def get_pin_type(self) -> "RPClassifier":
        """Returns the type of the value held by the pin/parameter.

        Returns:
            The type of the value held by the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::getPinType()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getPinType()))

    def set_is_parameter(self, is_parameter: int) -> None:
        """Specifies whether the element should be an activity parameter or an action pin.

        Args:
            is_parameter: Use 1 if you want the element to be an activity
                parameter, use 0 if you want the element to be an action pin.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setIsParameter(int isParameter)
        """
        self._set_method_or_property(self._com, "setIsParameter", "isParameter", is_parameter)

    def set_pin_direction(self, pin_direction: str) -> None:
        """Specifies the direction of the pin/parameter.

        Args:
            pin_direction: The direction that should be used for the
                pin/parameter. The valid strings for this parameter are: In,
                Out, and InOut.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setPinDirection(java.lang.String pinDirection)
        """
        self._set_method_or_property(self._com, "setPinDirection", "pinDirection", pin_direction)

    def set_pin_type(self, pin_type: "RPClassifier") -> None:
        """Specifies the type to use for the value held by the pin/parameter.

        Args:
            pin_type: The type to use for the value held by the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setPinType(com.telelogic.rhapsody.core.IRPClassifier pinType)
        """
        self.call_com(lambda: self._com.setPinType(pin_type._com))


class RPGraphEdge(RPGraphElement):
    """Wraps ``IRPGraphEdge``."""

    # IRPGraphEdge method parity checklist:
    # [ ] embedFlow                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] embedNewFlow                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getContainingArrow           [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getSource                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPGraphElement methods (covered by RPGraphElement checklist)
    # No deprecated IRPGraphEdge methods.

    def embed_flow(self, flow: "RPFlow") -> "RPGraphEdge":
        """Embeds the specified flow in this graph edge.

        Args:
            flow: The flow to embed in this graph edge.

        Returns:
            The graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::embedFlow(com.telelogic.rhapsody.core.IRPFlow flow)
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.embedFlow(flow._com)))

    def embed_new_flow(self) -> "RPGraphEdge":
        """Embeds a new flow in this graph edge.

        Returns:
            The graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::embedNewFlow()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.embedNewFlow()))

    def get_containing_arrow(self) -> "RPGraphEdge":
        """Returns the containing arrow of this graph edge.

        Returns:
            The containing arrow of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getContainingArrow()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getContainingArrow()))

    def get_source(self) -> "RPGraphElement":
        """Returns the source graph element of this graph edge.

        Returns:
            The source graph element of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getSource()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getSource()))

    def get_target(self) -> "RPGraphElement":
        """Returns the target graph element of this graph edge.

        Returns:
            The target graph element of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getTarget()
        """
        return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getTarget()))


class RPGraphNode(RPGraphElement):
    """Wraps ``IRPGraphNode``."""

    # IRPGraphNode method parity checklist:
    # [ ] bringToFront                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getIsPanelWidget             [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getPanelWidgetInstancePath   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] hideAllPorts                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] sendToBack                   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setPanelWidgetInstancePath   [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] showAllPorts                 [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPGraphElement methods (covered by RPGraphElement checklist)
    # No deprecated IRPGraphNode methods.

    def bring_to_front(self) -> None:
        """Brings this graph node to the front.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::bringToFront()
        """
        self.call_com(lambda: self._com.bringToFront())

    def get_is_panel_widget(self) -> int:
        """Returns whether this graph node is a panel widget.

        Returns:
            Whether this graph node is a panel widget.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::getIsPanelWidget()
        """
        return int(self._get_method_or_property(self._com, "getIsPanelWidget", "isPanelWidget"))

    def get_panel_widget_instance_path(self) -> RPCollection:
        """Returns the panel widget instance path of this graph node.

        Returns:
            The panel widget instance path of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::getPanelWidgetInstancePath()
        """
        return RPCollection(self.call_com(lambda: self._com.getPanelWidgetInstancePath()))

    def hide_all_ports(self) -> None:
        """Hides all ports of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::hideAllPorts()
        """
        self.call_com(lambda: self._com.hideAllPorts())

    def send_to_back(self) -> None:
        """Sends this graph node to the back.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::sendToBack()
        """
        self.call_com(lambda: self._com.sendToBack())

    def set_panel_widget_instance_path(self, panel_widget_instance_path: RPCollection) -> None:
        """Specifies the panel widget instance path of this graph node.

        Args:
            panel_widget_instance_path: The panel widget instance path to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::setPanelWidgetInstancePath(com.telelogic.rhapsody.core.IRPCollection panelWidgetInstancePath)
        """
        self.call_com(lambda: self._com.setPanelWidgetInstancePath(panel_widget_instance_path._com))

    def show_all_ports(self) -> None:
        """Shows all ports of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::showAllPorts()
        """
        self.call_com(lambda: self._com.showAllPorts())


AbstractRPModelElement.register_wrapper("ConditionMark", RPConditionMark)
AbstractRPModelElement.register_wrapper("Connector", RPConnector)
AbstractRPModelElement.register_wrapper("GraphElement", RPGraphElement)
AbstractRPModelElement.register_wrapper("GraphicalProperty", RPGraphicalProperty)
AbstractRPModelElement.register_wrapper("ImageMap", RPImageMap)
AbstractRPModelElement.register_wrapper("Link", RPLink)
AbstractRPModelElement.register_wrapper("MatrixLayout", RPMatrixLayout)
AbstractRPModelElement.register_wrapper("MatrixView", RPMatrixView)
AbstractRPModelElement.register_wrapper("MessagePoint", RPMessagePoint)
AbstractRPModelElement.register_wrapper("TableLayout", RPTableLayout)
AbstractRPModelElement.register_wrapper("TableView", RPTableView)
AbstractRPModelElement.register_wrapper("Pin", RPPin)
AbstractRPModelElement.register_wrapper("GraphEdge", RPGraphEdge)
AbstractRPModelElement.register_wrapper("GraphNode", RPGraphNode)
