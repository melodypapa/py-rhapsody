"""Graphics model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPModelElement, RPUnit
from rhapsody_cli.models.elements.model_interactions import RPMessage
from rhapsody_cli.models.elements.statemachine.model_statemachine import RPStateVertex

if TYPE_CHECKING:
    from rhapsody_cli.models.core import RPCollection
    from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
    from rhapsody_cli.models.elements.model_activity import RPFlow, RPSwimlane
    from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
    from rhapsody_cli.models.elements.model_interactions import (
        RPInteractionOccurrence,
        RPInteractionOperator,
        RPTransition,
    )
    from rhapsody_cli.models.elements.model_other_model import (
        RPClassifierRole,
        RPSysMLPort,
    )
    from rhapsody_cli.models.elements.statemachine.model_statemachine import RPState
    from rhapsody_cli.models.elements.relations.model_instance import RPInstance
    from rhapsody_cli.models.elements.relations.model_port import RPPort
    from rhapsody_cli.models.elements.relations.model_relation import RPRelation


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
    # [ ] createDefaultTransition      [ ] impl  [ ] docstring  [ ] test
    # [ ] getConnectorType             [ ] impl  [ ] docstring  [ ] test
    # [ ] getDerivedInEdges            [ ] impl  [ ] docstring  [ ] test
    # [ ] getDerivedOutEdge            [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsSwimlane               [ ] impl  [ ] docstring  [ ] test
    # [ ] getOfState                   [ ] impl  [ ] docstring  [ ] test
    # [ ] isConditionConnector         [ ] impl  [ ] docstring  [ ] test
    # [ ] isDiagramConnector           [ ] impl  [ ] docstring  [ ] test
    # [ ] isForkConnector              [ ] impl  [ ] docstring  [ ] test
    # [ ] isHistoryConnector           [ ] impl  [ ] docstring  [ ] test
    # [ ] isJoinConnector              [ ] impl  [ ] docstring  [ ] test
    # [ ] isJunctionConnector          [ ] impl  [ ] docstring  [ ] test
    # [ ] isStubConnector              [ ] impl  [ ] docstring  [ ] test
    # [ ] isTerminationConnector       [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsSwimlane               [ ] impl  [ ] docstring  [ ] test
    # [ ] setOfState                   [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_connector_type(self) -> str:
        """Returns the type of the connector.

        Returns:
            The type of the connector: Condition, Diagram, EnterExit, Fork,
            History, Join, Junction, Termination, InPin, OutPin, or InOutPin.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getConnectorType()
        """
        raise NotImplementedError

    def get_derived_in_edges(self) -> "RPCollection":
        """Returns a collection of the transitions coming into the connector.

        Returns:
            The transitions coming into the connector (a collection of
            IRPTransition elements).

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getDerivedInEdges()
        """
        raise NotImplementedError

    def get_derived_out_edge(self) -> "RPTransition":
        """Returns the transition exiting the connector.

        Returns:
            The transition exiting the connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getDerivedOutEdge()
        """
        raise NotImplementedError

    def get_its_swimlane(self) -> "RPSwimlane":
        """For connectors in a swimlane, returns the swimlane that contains the connector.

        Returns:
            The swimlane that contains the connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getItsSwimlane()
        """
        raise NotImplementedError

    def get_of_state(self) -> "RPState":
        """For history connectors, returns the state that the history connector belongs to.

        Returns:
            The state that this history connector belongs to.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::getOfState()
        """
        raise NotImplementedError

    def is_condition_connector(self) -> int:
        """Checks whether the connector is a condition connector.

        Returns:
            1 if the connector is a condition connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isConditionConnector()
        """
        raise NotImplementedError

    def is_diagram_connector(self) -> int:
        """Checks whether the connector is a diagram connector.

        Returns:
            1 if the connector is a diagram connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isDiagramConnector()
        """
        raise NotImplementedError

    def is_fork_connector(self) -> int:
        """Checks whether the connector is a fork sync bar connector.

        Returns:
            1 if the connector is a fork sync bar connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isForkConnector()
        """
        raise NotImplementedError

    def is_history_connector(self) -> int:
        """Checks whether the connector is a history connector.

        Returns:
            1 if the connector is a history connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isHistoryConnector()
        """
        raise NotImplementedError

    def is_join_connector(self) -> int:
        """Checks whether the connector is a join sync bar connector.

        Returns:
            1 if the connector is a join sync bar connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isJoinConnector()
        """
        raise NotImplementedError

    def is_junction_connector(self) -> int:
        """Checks whether the connector is a junction connector.

        Returns:
            1 if the connector is a junction connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isJunctionConnector()
        """
        raise NotImplementedError

    def is_stub_connector(self) -> int:
        """Checks whether the connector is an EnterExit point.

        Returns:
            1 if the connector is an EnterExit point, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isStubConnector()
        """
        raise NotImplementedError

    def is_termination_connector(self) -> int:
        """Checks whether the connector is a termination connector.

        Returns:
            1 if the connector is a termination connector, 0 otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::isTerminationConnector()
        """
        raise NotImplementedError

    def set_its_swimlane(self, p_val: "RPSwimlane") -> None:
        """Specifies the swimlane that should contain this connector.

        Args:
            p_val: The swimlane that should contain this connector.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::setItsSwimlane(com.telelogic.rhapsody.core.IRPSwimlane pVal)
        """
        raise NotImplementedError

    def set_of_state(self, of_state: "RPState") -> None:
        """For history connectors, specifies the state for which the connector should maintain historical state information.

        Args:
            of_state: The state for which the connector should maintain
                historical state information.

        Reference:
            com.telelogic.rhapsody.core.IRPConnector::setOfState(com.telelogic.rhapsody.core.IRPState OfState)
        """
        raise NotImplementedError


class RPGraphElement(RPModelElement):
    """Wraps ``IRPGraphElement``."""

    # IRPGraphElement method parity checklist:
    # [ ] addProperty                  [ ] impl  [ ] docstring  [ ] test
    # [ ] applyDefaultFormat           [ ] impl  [ ] docstring  [ ] test
    # [ ] getAllGraphicalProperties    [ ] impl  [ ] docstring  [ ] test
    # [ ] getAllProperties             [ ] impl  [ ] docstring  [ ] test
    # [ ] getAssociatedImage           [ ] impl  [ ] docstring  [ ] test
    # [ ] getDiagram                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getGraphicalParent           [ ] impl  [ ] docstring  [ ] test
    # [ ] getGraphicalProperty         [ ] impl  [ ] docstring  [ ] test
    # [ ] getGraphicalPropertyOfText   [ ] impl  [ ] docstring  [ ] test
    # [ ] getImageLayout               [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getLocalProperties           [ ] impl  [ ] docstring  [ ] test
    # [ ] getModelObject               [ ] impl  [ ] docstring  [ ] test
    # [ ] getPropertyValue             [ ] impl  [ ] docstring  [ ] test
    # [ ] getSelectedImage             [ ] impl  [ ] docstring  [ ] test
    # [ ] removeProperty               [ ] impl  [ ] docstring  [ ] test
    # [ ] setAssociatedImage           [ ] impl  [ ] docstring  [ ] test
    # [ ] setGraphicalProperty         [ ] impl  [ ] docstring  [ ] test
    # [ ] setGraphicalPropertyOfText   [ ] impl  [ ] docstring  [ ] test
    # [ ] setImageLayout               [ ] impl  [ ] docstring  [ ] test
    # [ ] setPropertyValue             [ ] impl  [ ] docstring  [ ] test
    # [ ] setSelectedImage             [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def apply_default_format(self) -> None:
        """Applies the default format to this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::applyDefaultFormat()
        """
        raise NotImplementedError

    def get_all_graphical_properties(self) -> "RPCollection":
        """Returns all graphical properties of this graph element.

        Returns:
            A collection of all graphical properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAllGraphicalProperties()
        """
        raise NotImplementedError

    def get_all_properties(self) -> "RPCollection":
        """Returns all properties of this graph element.

        Returns:
            A collection of all properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAllProperties()
        """
        raise NotImplementedError

    def get_associated_image(self) -> str:
        """Returns the associated image of this graph element.

        Returns:
            The associated image.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getAssociatedImage()
        """
        raise NotImplementedError

    def get_diagram(self) -> "RPDiagram":
        """Returns the diagram that contains this graph element.

        Returns:
            The diagram that contains this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getDiagram()
        """
        raise NotImplementedError

    def get_graphical_parent(self) -> "RPGraphElement":
        """Returns the graphical parent of this graph element.

        Returns:
            The graphical parent of this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getGraphicalParent()
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_image_layout(self) -> str:
        """Returns the image layout specified for the image linked to the graphic element.

        Returns:
            The image layout specified for the image linked to the graphic
            element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getImageLayout()
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Returns the interface name of this graph element.

        Returns:
            The interface name of this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getInterfaceName()
        """
        raise NotImplementedError

    def get_local_properties(self) -> "RPCollection":
        """Returns the local properties of this graph element.

        Returns:
            A collection of the local properties.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getLocalProperties()
        """
        raise NotImplementedError

    def get_model_object(self) -> "RPModelElement":
        """Returns the model object associated with this graph element.

        Returns:
            The model object associated with this graph element.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getModelObject()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_selected_image(self) -> str:
        """Returns the full path of the image that was linked to the graphic element.

        Returns:
            The full path of the image linked to the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::getSelectedImage()
        """
        raise NotImplementedError

    def remove_property(self, property_key: str) -> None:
        """Removes the specified property from this graph element.

        Args:
            property_key: The key of the property to remove.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::removeProperty(java.lang.String propertyKey)
        """
        raise NotImplementedError

    def set_associated_image(self, associated_image: str) -> None:
        """Sets the associated image for this graph element.

        Args:
            associated_image: The associated image to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setAssociatedImage(java.lang.String associatedImage)
        """
        raise NotImplementedError

    def set_graphical_property(self, name: str, value: str) -> None:
        """Sets a new value for a graphical property.

        Args:
            name: The name of the graphical property to set.
            value: The value to use for the specified property.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setGraphicalProperty(java.lang.String name, java.lang.String value)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def set_image_layout(self, image_layout: str) -> None:
        """Specifies the image layout that should be used for the image linked to the graphic element.

        Args:
            image_layout: The image layout that should be used for the image
                linked to the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setImageLayout(java.lang.String imageLayout)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def set_selected_image(self, selected_image: str) -> None:
        """Links the graphic element to the image represented by the path specified.

        Args:
            selected_image: The full path to the image that should be linked to
                the graphic element.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphElement::setSelectedImage(java.lang.String selectedImage)
        """
        raise NotImplementedError


class RPGraphicalProperty(RPModelElement):
    """Wraps ``IRPGraphicalProperty``."""

    # IRPGraphicalProperty method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getKey                       [ ] impl  [ ] docstring  [ ] test
    # [ ] getValue                     [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_key(self) -> str:
        """Returns the key of this graphical property.

        Returns:
            The key of this graphical property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphicalProperty::getKey()
        """
        raise NotImplementedError

    def get_value(self) -> str:
        """Returns the value of this graphical property.

        Returns:
            The value of this graphical property.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphicalProperty::getValue()
        """
        raise NotImplementedError


class RPImageMap(RPModelElement):
    """Wraps ``IRPImageMap``."""

    # IRPImageMap method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsGUID                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getName                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getPictureFileName           [ ] impl  [ ] docstring  [ ] test
    # [ ] getPoints                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getShape                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_is_g_u_i_d(self) -> int:
        """Returns whether this image map uses a GUID.

        Returns:
            Whether this image map uses a GUID.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getIsGUID()
        """
        raise NotImplementedError

    def get_name(self) -> str:
        """Returns the name of this image map.

        Returns:
            The name of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getName()
        """
        raise NotImplementedError

    def get_picture_file_name(self) -> str:
        """Returns the picture file name of this image map.

        Returns:
            The picture file name of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getPictureFileName()
        """
        raise NotImplementedError

    def get_points(self) -> str:
        """Returns the points of this image map.

        Returns:
            The points of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getPoints()
        """
        raise NotImplementedError

    def get_shape(self) -> str:
        """Returns the shape of this image map.

        Returns:
            The shape of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getShape()
        """
        raise NotImplementedError

    def get_target(self) -> str:
        """Returns the target of this image map.

        Returns:
            The target of this image map.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPImageMap::getTarget()
        """
        raise NotImplementedError


class RPLink(RPUnit):
    """Wraps ``IRPLink``: represents links in Rhapsody models."""

    # IRPLink method parity checklist:
    # [ ] getEnd1Multiplicity          [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd1Name                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2Multiplicity          [ ] impl  [ ] docstring  [ ] test
    # [ ] getEnd2Name                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFrom                      [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElement               [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromPort                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromSysMLPort             [ ] impl  [ ] docstring  [ ] test
    # [ ] getInstantiates              [ ] impl  [ ] docstring  [ ] test
    # [ ] getOther                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getTo                        [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElement                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getToPort                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getToSysMLPort               [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd1Multiplicity          [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd1Name                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd2Multiplicity          [ ] impl  [ ] docstring  [ ] test
    # [ ] setEnd2Name                  [ ] impl  [ ] docstring  [ ] test
    # [ ] setInstantiates              [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_end1_name(self) -> str:
        """Returns the name of the first end of this link.

        Returns:
            The name of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd1Name()
        """
        raise NotImplementedError

    def get_end2_multiplicity(self) -> str:
        """Returns the multiplicity of the second end of this link.

        Returns:
            The multiplicity of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd2Multiplicity()
        """
        raise NotImplementedError

    def get_end2_name(self) -> str:
        """Returns the name of the second end of this link.

        Returns:
            The name of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getEnd2Name()
        """
        raise NotImplementedError

    def get_from(self) -> "RPInstance":
        """Returns the source instance of this link.

        Returns:
            The source instance of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFrom()
        """
        raise NotImplementedError

    def get_from_element(self) -> "RPModelElement":
        """Returns the source element of this link.

        Returns:
            The source element of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromElement()
        """
        raise NotImplementedError

    def get_from_port(self) -> "RPPort":
        """Returns the source port of this link.

        Returns:
            The source port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromPort()
        """
        raise NotImplementedError

    def get_from_sys_m_l_port(self) -> "RPSysMLPort":
        """Returns the source SysML port of this link.

        Returns:
            The source SysML port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getFromSysMLPort()
        """
        raise NotImplementedError

    def get_instantiates(self) -> "RPRelation":
        """Returns the relation that this link instantiates.

        Returns:
            The relation that this link instantiates.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getInstantiates()
        """
        raise NotImplementedError

    def get_other(self) -> "RPLink":
        """Returns the other link in a bidirectional relationship.

        Returns:
            The other link in a bidirectional relationship.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getOther()
        """
        raise NotImplementedError

    def get_to(self) -> "RPInstance":
        """Returns the target of a link.

        Returns:
            The target of the link.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getTo()
        """
        raise NotImplementedError

    def get_to_element(self) -> "RPModelElement":
        """Returns the target element of this link.

        Returns:
            The target element of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToElement()
        """
        raise NotImplementedError

    def get_to_port(self) -> "RPPort":
        """Returns the port through which a link reaches a target object.

        Returns:
            The port through which the link reaches its target object.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToPort()
        """
        raise NotImplementedError

    def get_to_sys_m_l_port(self) -> "RPSysMLPort":
        """Returns the target SysML port of this link.

        Returns:
            The target SysML port of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::getToSysMLPort()
        """
        raise NotImplementedError

    def set_end1_multiplicity(self, end1_multiplicity: str) -> None:
        """Sets the multiplicity of the first end of this link.

        Args:
            end1_multiplicity: The multiplicity of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd1Multiplicity(java.lang.String end1Multiplicity)
        """
        raise NotImplementedError

    def set_end1_name(self, end1_name: str) -> None:
        """Sets the name of the first end of this link.

        Args:
            end1_name: The name of the first end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd1Name(java.lang.String end1Name)
        """
        raise NotImplementedError

    def set_end2_multiplicity(self, end2_multiplicity: str) -> None:
        """Sets the multiplicity of the second end of this link.

        Args:
            end2_multiplicity: The multiplicity of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd2Multiplicity(java.lang.String end2Multiplicity)
        """
        raise NotImplementedError

    def set_end2_name(self, end2_name: str) -> None:
        """Sets the name of the second end of this link.

        Args:
            end2_name: The name of the second end of this link.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setEnd2Name(java.lang.String end2Name)
        """
        raise NotImplementedError

    def set_instantiates(self, p_val: "RPRelation") -> None:
        """Sets the relation that this link instantiates.

        Args:
            p_val: The relation that this link should instantiate.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPLink::setInstantiates(com.telelogic.rhapsody.core.IRPRelation pVal)
        """
        raise NotImplementedError


class RPMatrixLayout(RPUnit):
    """Wraps ``IRPMatrixLayout``."""

    # IRPMatrixLayout method parity checklist:
    # [ ] getCellElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypes            [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] setCellElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypes            [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPMatrixLayout methods.

    def get_cell_element_types(self) -> "RPCollection":
        """Returns a collection of the element types that were specified to be displayed in the cells of the matrix.

        Returns:
            The element types that were specified to be displayed in the cells
            of the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getCellElementTypes()
        """
        raise NotImplementedError

    def get_from_element_types(self) -> "RPCollection":
        """Returns a collection of the "from" element types specified to be displayed in the matrix.

        Returns:
            The "from" element types specified to be displayed in the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypes()
        """
        raise NotImplementedError

    def get_from_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query that was specified to determine the "from" element types.

        Returns:
            The query that was specified to determine the "from" element types
            for the matrix layout.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypesQueryToUse()
        """
        raise NotImplementedError

    def get_from_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or collection of element types was used to specify the "from" element types.

        Returns:
            One of the constants contained in the class
            IRPMatrixLayout.QueryOrElementsList: QUERY if a query was used,
            ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getFromElementTypesUseQueryOrElementsList()
        """
        raise NotImplementedError

    def get_to_element_types(self) -> "RPCollection":
        """Returns a collection of the "to" element types specified to be displayed in the matrix.

        Returns:
            The "to" element types specified to be displayed in the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypes()
        """
        raise NotImplementedError

    def get_to_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query that was specified to determine the "to" element types.

        Returns:
            The query that was specified to determine the "to" element types
            for the matrix layout.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypesQueryToUse()
        """
        raise NotImplementedError

    def get_to_element_types_use_query_or_elements_list(self) -> int:
        """Checks whether a query or collection of element types was used to specify the "to" element types.

        Returns:
            One of the constants contained in the class
            IRPMatrixLayout.QueryOrElementsList: QUERY if a query was used,
            ELEMENTS_LIST if a collection of element types was used.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::getToElementTypesUseQueryOrElementsList()
        """
        raise NotImplementedError

    def set_cell_element_types(self, p_collection: "RPCollection") -> None:
        """Specifies the element types to display in the cells of the matrix.

        Args:
            p_collection: The element types to display in the cells of the matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setCellElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

    def set_from_element_types(self, p_collection: "RPCollection") -> None:
        """Specifies the "from" element types that should be displayed in the matrix.

        Args:
            p_collection: The "from" element types that should be displayed in the
                matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setFromElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

    def set_from_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query to use to determine the "from" element types for the matrix layout.

        Args:
            query: The query to use to determine the "from" element types for
                the matrix layout. To clear a previous query, use null.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setFromElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def set_to_element_types(self, p_collection: "RPCollection") -> None:
        """Specifies the "to" element types that should be displayed in the matrix.

        Args:
            p_collection: The "to" element types that should be displayed in the
                matrix.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setToElementTypes(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

    def set_to_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query to use to determine the "to" element types for the matrix layout.

        Args:
            query: The query to use to determine the "to" element types for the
                matrix layout. To clear a previous query, use null.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixLayout::setToElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        raise NotImplementedError

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
        raise NotImplementedError


class RPMatrixView(RPUnit):
    """Wraps ``IRPMatrixView``: represents Matrix View elements in Rhapsody models."""

    # IRPMatrixView method parity checklist:
    # [ ] getCellElements              [ ] impl  [ ] docstring  [ ] test
    # [ ] getCellString                [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] test
    # [ ] getContent                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromScope                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getHTMLContent               [ ] impl  [ ] docstring  [ ] test
    # [ ] getImageCollection           [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsMatrixLayout           [ ] impl  [ ] docstring  [ ] test
    # [ ] getRowCount                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getToScope                   [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromScope                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsMatrixLayout           [ ] impl  [ ] docstring  [ ] test
    # [ ] setToScope                   [ ] impl  [ ] docstring  [ ] test
    # [ ] updateViewOnServer           [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludeDescendantsFromScope [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludeDescendantsToScope [ ] impl  [ ] docstring  [ ] test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludeDescendantsFromScope [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludeDescendantsToScope [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPMatrixView methods.

    def get_cell_elements(self, row: int, column: int) -> "RPCollection":
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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_column_count(self) -> int:
        """Returns the number of columns in the matrix.

        Returns:
            The number of columns in the matrix.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getColumnCount()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_from_scope(self) -> "RPCollection":
        """Returns the "from" scope of this matrix view.

        Returns:
            The "from" scope of this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getFromScope()
        """
        raise NotImplementedError

    def get_h_t_m_l_content(self) -> str:
        """Returns the content of the matrix as HTML.

        Returns:
            The content of the matrix as HTML.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getHTMLContent()
        """
        raise NotImplementedError

    def get_image_collection(self, s_folder: str, s_filename: str, s_extension: str) -> "RPCollection":
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
        raise NotImplementedError

    def get_its_matrix_layout(self) -> "RPMatrixLayout":
        """Returns the matrix layout used by this matrix view.

        Returns:
            The matrix layout used by this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getItsMatrixLayout()
        """
        raise NotImplementedError

    def get_row_count(self) -> int:
        """Returns the number of rows in the matrix.

        Returns:
            The number of rows in the matrix.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getRowCount()
        """
        raise NotImplementedError

    def get_to_scope(self) -> "RPCollection":
        """Returns the "to" scope of this matrix view.

        Returns:
            The "to" scope of this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getToScope()
        """
        raise NotImplementedError

    def set_from_scope(self, p_collection: "RPCollection") -> None:
        """Specifies the "from" scope to use for this matrix view.

        Args:
            p_collection: The "from" scope to use for this matrix view. Note that
                the parameter is a Rhapsody collection, but at the moment, only
                the first value in the collection is used for the "from" scope.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setFromScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

    def set_its_matrix_layout(self, p_val: "RPMatrixLayout") -> None:
        """Specifies the matrix layout to use for this matrix view.

        Args:
            p_val: The matrix layout to use for this matrix view.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setItsMatrixLayout(com.telelogic.rhapsody.core.IRPMatrixLayout pVal)
        """
        raise NotImplementedError

    def set_to_scope(self, p_collection: "RPCollection") -> None:
        """Specifies the "to" scope to use for this matrix view.

        Args:
            p_collection: The "to" scope to use for this matrix view. Note that
                the parameter is a Rhapsody collection, but at the moment, only
                the first value in the collection is used for the "to" scope.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setToScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_include_descendants_from_scope(self) -> int:
        """Returns whether descendants are included in the "from" scope.

        Returns:
            Whether descendants are included in the "from" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getIncludeDescendantsFromScope()
        """
        raise NotImplementedError

    def get_include_descendants_to_scope(self) -> int:
        """Returns whether descendants are included in the "to" scope.

        Returns:
            Whether descendants are included in the "to" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::getIncludeDescendantsToScope()
        """
        raise NotImplementedError

    def open(self) -> None:
        """Opens this matrix view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::open()
        """
        raise NotImplementedError

    def set_include_descendants_from_scope(self, include_descendants_from_scope: int) -> None:
        """Sets whether descendants are included in the "from" scope.

        Args:
            include_descendants_from_scope: Whether descendants should be included in the "from" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setIncludeDescendantsFromScope(int includeDescendantsFromScope)
        """
        raise NotImplementedError

    def set_include_descendants_to_scope(self, include_descendants_to_scope: int) -> None:
        """Sets whether descendants are included in the "to" scope.

        Args:
            include_descendants_to_scope: Whether descendants should be included in the "to" scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMatrixView::setIncludeDescendantsToScope(int includeDescendantsToScope)
        """
        raise NotImplementedError


class RPMessagePoint(RPModelElement):
    """Wraps ``IRPMessagePoint``."""

    # IRPMessagePoint method parity checklist:
    # [ ] getClassifierRole            [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionOccurrence     [ ] impl  [ ] docstring  [ ] test
    # [ ] getInteractionOperator       [ ] impl  [ ] docstring  [ ] test
    # [ ] getMessage                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getType                      [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_interaction_occurrence(self) -> "RPInteractionOccurrence":
        """Returns the interaction occurrence associated with this message point.

        Returns:
            The interaction occurrence associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getInteractionOccurrence()
        """
        raise NotImplementedError

    def get_interaction_operator(self) -> "RPInteractionOperator":
        """Returns the interaction operator associated with this message point.

        Returns:
            The interaction operator associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getInteractionOperator()
        """
        raise NotImplementedError

    def get_message(self) -> "RPMessage":
        """Returns the message associated with this message point.

        Returns:
            The message associated with this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getMessage()
        """
        raise NotImplementedError

    def get_type(self) -> str:
        """Returns the type of this message point.

        Returns:
            The type of this message point.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPMessagePoint::getType()
        """
        raise NotImplementedError


class RPTableLayout(RPUnit):
    """Wraps ``IRPTableLayout``."""

    # IRPTableLayout method parity checklist:
    # [ ] addColumn                    [ ] impl  [ ] docstring  [ ] test
    # [ ] addColumnEx                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getCollapseFirstColumn       [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnContext             [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnDefaultWidth        [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationAllowNew [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationAllowSelect [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationCellType [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationDisplayProperty [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationGetterCode [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationImports [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationPickerCode [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnImplementationSetterCode [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnName                [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnProperty            [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnType                [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumns                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getElementTypes              [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] test
    # [ ] getFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] getRelationTable             [ ] impl  [ ] docstring  [ ] test
    # [ ] getResultList                [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypes            [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] test
    # [ ] getToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] removeColumn                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setCollapseFirstColumn       [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnContext             [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnDefaultWidth        [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationAllowNew [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationAllowSelect [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationCellType [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationDisplayProperty [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationGetterCode [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationImports [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationPickerCode [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnImplementationSetterCode [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnName                [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnProperty            [ ] impl  [ ] docstring  [ ] test
    # [ ] setColumnType                [ ] impl  [ ] docstring  [ ] test
    # [ ] setElementTypes              [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypes          [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypesQueryToUse [ ] impl  [ ] docstring  [ ] test
    # [ ] setFromElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] setRelationTable             [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypes            [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypesQueryToUse  [ ] impl  [ ] docstring  [ ] test
    # [ ] setToElementTypesUseQueryOrElementsList [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_collapse_first_column(self) -> int:
        """Checks whether the first column includes controls for collapsing and expanding rows.

        Returns:
            ``1`` if the first column includes collapse/expand controls, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getCollapseFirstColumn()
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_columns(self) -> "RPCollection":
        """Returns a collection of the columns in this table layout.

        Returns:
            An RPCollection of the columns in this table layout.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumns()
        """
        raise NotImplementedError

    def get_element_types(self) -> "RPCollection":
        """Returns a collection of the element types displayed in the table.

        The collection consists of strings (from the list of types displayed on the
        ElementTypes tab of the Features window for table layouts).

        Returns:
            An RPCollection of the element types that were specified to be displayed in the table.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getElementTypes()
        """
        raise NotImplementedError

    def get_from_element_types(self) -> "RPCollection":
        """Returns the "from" element types for "relation tables".

        Returns a collection of the element types specified as the "from" element types. The
        collection consists of strings (from the From Element Types tab of the Features window).

        Returns:
            An RPCollection of the types specified as the "from" element types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getFromElementTypes()
        """
        raise NotImplementedError

    def get_from_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query used to determine the "from" element types for "relation tables".

        Returns:
            The query (an RPTableLayout) that was specified to determine the "from" element
            types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getFromElementTypesQueryToUse()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_relation_table(self) -> int:
        """Checks whether the table was defined as a "relation table".

        Returns:
            ``1`` if the table was defined as a "relation table", ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getRelationTable()
        """
        raise NotImplementedError

    def get_result_list(self, scope: "RPModelElement") -> "RPCollection":
        """Returns the result list for the given scope.

        Args:
            scope: The scope (an IRPModelElement) for which to compute the result list.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getResultList(com.telelogic.rhapsody.core.IRPModelElement scope)
        """
        raise NotImplementedError

    def get_to_element_types(self) -> "RPCollection":
        """Returns the "to" element types for "relation tables".

        Returns a collection of the element types specified as the "to" element types. The
        collection consists of strings (from the To Element Types tab of the Features window).

        Returns:
            An RPCollection of the types specified as the "to" element types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getToElementTypes()
        """
        raise NotImplementedError

    def get_to_element_types_query_to_use(self) -> "RPTableLayout":
        """Returns the query used to determine the "to" element types for "relation tables".

        Returns:
            The query (an RPTableLayout) that was specified to determine the "to" element
            types for the table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getToElementTypesQueryToUse()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def remove_column(self, index: int) -> None:
        """Removes the specified column from the table layout.

        Args:
            index: The index representing the position of the column in the table. The index
                for the first column in the table is 0.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::removeColumn(int Index)
        """
        raise NotImplementedError

    def set_collapse_first_column(self, collapse: int) -> None:
        """Specifies whether the first column includes collapse/expand controls.

        Args:
            collapse: Use ``1`` if the first column should include collapse/expand controls,
                ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setCollapseFirstColumn(int collapse)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def set_element_types(self, elements: "RPCollection") -> None:
        """Specifies the element types displayed in the table.

        The parameter must be a collection of strings (from the list of types displayed on the
        ElementTypes tab of the Features window for table layouts).

        Args:
            elements: The element types that should be displayed in the table.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        raise NotImplementedError

    def set_from_element_types(self, elements: "RPCollection") -> None:
        """Specifies the "from" element types for "relation tables".

        For "relation tables", specifies the list of element types to use as the "from" element
        types. The parameter must be a collection of strings (from the From Element Types tab).

        Args:
            elements: Collection of element types to use as the "from" element types for the
                table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setFromElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        raise NotImplementedError

    def set_from_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query used to determine the "from" element types for "relation tables".

        Args:
            query: The query to use to determine the "from" element types for the table layout.
                Use ``None`` to clear a previous query.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setFromElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def set_relation_table(self, relation: int) -> None:
        """Specifies whether the table is defined as a "relation table".

        Args:
            relation: Use ``1`` if the table should be defined as a "relation table", ``0``
                otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setRelationTable(int relation)
        """
        raise NotImplementedError

    def set_to_element_types(self, elements: "RPCollection") -> None:
        """Specifies the "to" element types for "relation tables".

        For "relation tables", specifies the list of element types to use as the "to" element
        types. The parameter must be a collection of strings (from the To Element Types tab).

        Args:
            elements: Collection of element types to use as the "to" element types for the
                table layout.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setToElementTypes(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        raise NotImplementedError

    def set_to_element_types_query_to_use(self, query: "RPTableLayout") -> None:
        """Specifies the query used to determine the "to" element types for "relation tables".

        Args:
            query: The query to use to determine the "to" element types for the table layout.
                Use ``None`` to clear a previous query.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::setToElementTypesQueryToUse(com.telelogic.rhapsody.core.IRPTableLayout query)
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_column_count(self) -> int:
        """Returns the number of columns in the table layout.

        Returns:
            The number of columns in the table layout.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableLayout::getColumnCount()
        """
        raise NotImplementedError


class RPTableView(RPUnit):
    """Wraps ``IRPTableView``: represents Table View elements in Rhapsody models."""

    # IRPTableView method parity checklist:
    # [ ] getCellElements              [ ] impl  [ ] docstring  [ ] test
    # [ ] getCellString                [ ] impl  [ ] docstring  [ ] test
    # [ ] getColumnCount               [ ] impl  [ ] docstring  [ ] test
    # [ ] getContent                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getHTMLContent               [ ] impl  [ ] docstring  [ ] test
    # [ ] getImageCollection           [ ] impl  [ ] docstring  [ ] test
    # [ ] getItsTableLayout            [ ] impl  [ ] docstring  [ ] test
    # [ ] getRowCount                  [ ] impl  [ ] docstring  [ ] test
    # [ ] getScope                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getUseOwnerScope             [ ] impl  [ ] docstring  [ ] test
    # [ ] setItsTableLayout            [ ] impl  [ ] docstring  [ ] test
    # [ ] setScope                     [ ] impl  [ ] docstring  [ ] test
    # [ ] setUseOwnerScope             [ ] impl  [ ] docstring  [ ] test
    # [ ] updateViewOnServer           [ ] impl  [ ] docstring  [ ] test
    # [ ] getIncludeDescendants        [ ] impl  [ ] docstring  [ ] test
    # [ ] open                         [ ] impl  [ ] docstring  [ ] test
    # [ ] setIncludeDescendants        [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklist)
    # [inherited] IRPUnit methods (covered by RPUnit checklist)
    # No deprecated IRPTableView methods.

    def get_cell_elements(self, row: int, column: int) -> "RPCollection":
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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_column_count(self) -> int:
        """Returns the number of columns in the table.

        Returns:
            The number of columns in the table.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getColumnCount()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_h_t_m_l_content(self) -> str:
        """Returns the content of the table as HTML.

        Returns:
            The content of the table as HTML.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getHTMLContent()
        """
        raise NotImplementedError

    def get_image_collection(self, s_folder: str, s_filename: str, s_extension: str) -> "RPCollection":
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
        raise NotImplementedError

    def get_its_table_layout(self) -> "RPTableLayout":
        """Returns the table layout used by this table view.

        Returns:
            The table layout used by this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getItsTableLayout()
        """
        raise NotImplementedError

    def get_row_count(self) -> int:
        """Returns the number of rows in the table.

        Returns:
            The number of rows in the table.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getRowCount()
        """
        raise NotImplementedError

    def get_scope(self) -> "RPCollection":
        """Returns the scope of this table view.

        Returns:
            The scope of this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getScope()
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def set_its_table_layout(self, p_val: "RPTableLayout") -> None:
        """Specifies the table layout to use for this table view.

        Args:
            p_val: The table layout to use for this table view.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setItsTableLayout(com.telelogic.rhapsody.core.IRPTableLayout pVal)
        """
        raise NotImplementedError

    def set_scope(self, p_collection: "RPCollection") -> None:
        """Specifies the scope to use for this table view.

        Args:
            p_collection: The scope to use for this table view. Note that the
                parameter is a Rhapsody collection, but at the moment, only the
                first value in the collection is used for the scope.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setScope(com.telelogic.rhapsody.core.IRPCollection pCollection)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_include_descendants(self) -> int:
        """Returns whether descendants are included in the scope.

        Returns:
            Whether descendants are included in the scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::getIncludeDescendants()
        """
        raise NotImplementedError

    def open(self) -> None:
        """Opens this table view.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::open()
        """
        raise NotImplementedError

    def set_include_descendants(self, include_descendants: int) -> None:
        """Sets whether descendants are included in the scope.

        Args:
            include_descendants: Whether descendants should be included in the scope.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPTableView::setIncludeDescendants(int includeDescendants)
        """
        raise NotImplementedError


class RPPin(RPConnector):
    """Wraps ``IRPPin``: represents action pins added to actions, or activity parameters added to action blocks, in an activity diagram."""

    # IRPPin method parity checklist:
    # [ ] getIsParameter               [ ] impl  [ ] docstring  [ ] test
    # [ ] getPinDirection              [ ] impl  [ ] docstring  [ ] test
    # [ ] getPinType                   [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsParameter               [ ] impl  [ ] docstring  [ ] test
    # [ ] setPinDirection              [ ] impl  [ ] docstring  [ ] test
    # [ ] setPinType                   [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def get_pin_direction(self) -> str:
        """Returns the direction of the pin/parameter: In, Out, or InOut.

        Returns:
            The direction of the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::getPinDirection()
        """
        raise NotImplementedError

    def get_pin_type(self) -> "RPClassifier":
        """Returns the type of the value held by the pin/parameter.

        Returns:
            The type of the value held by the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::getPinType()
        """
        raise NotImplementedError

    def set_is_parameter(self, is_parameter: int) -> None:
        """Specifies whether the element should be an activity parameter or an action pin.

        Args:
            is_parameter: Use 1 if you want the element to be an activity
                parameter, use 0 if you want the element to be an action pin.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setIsParameter(int isParameter)
        """
        raise NotImplementedError

    def set_pin_direction(self, pin_direction: str) -> None:
        """Specifies the direction of the pin/parameter.

        Args:
            pin_direction: The direction that should be used for the
                pin/parameter. The valid strings for this parameter are: In,
                Out, and InOut.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setPinDirection(java.lang.String pinDirection)
        """
        raise NotImplementedError

    def set_pin_type(self, pin_type: "RPClassifier") -> None:
        """Specifies the type to use for the value held by the pin/parameter.

        Args:
            pin_type: The type to use for the value held by the pin/parameter.

        Reference:
            com.telelogic.rhapsody.core.IRPPin::setPinType(com.telelogic.rhapsody.core.IRPClassifier pinType)
        """
        raise NotImplementedError


class RPGraphEdge(RPGraphElement):
    """Wraps ``IRPGraphEdge``."""

    # IRPGraphEdge method parity checklist:
    # [ ] embedFlow                    [ ] impl  [ ] docstring  [ ] test
    # [ ] embedNewFlow                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getContainingArrow           [ ] impl  [ ] docstring  [ ] test
    # [ ] getSource                    [ ] impl  [ ] docstring  [ ] test
    # [ ] getTarget                    [ ] impl  [ ] docstring  [ ] test
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
        raise NotImplementedError

    def embed_new_flow(self) -> "RPGraphEdge":
        """Embeds a new flow in this graph edge.

        Returns:
            The graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::embedNewFlow()
        """
        raise NotImplementedError

    def get_containing_arrow(self) -> "RPGraphEdge":
        """Returns the containing arrow of this graph edge.

        Returns:
            The containing arrow of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getContainingArrow()
        """
        raise NotImplementedError

    def get_source(self) -> "RPGraphElement":
        """Returns the source graph element of this graph edge.

        Returns:
            The source graph element of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getSource()
        """
        raise NotImplementedError

    def get_target(self) -> "RPGraphElement":
        """Returns the target graph element of this graph edge.

        Returns:
            The target graph element of this graph edge.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphEdge::getTarget()
        """
        raise NotImplementedError


class RPGraphNode(RPGraphElement):
    """Wraps ``IRPGraphNode``."""

    # IRPGraphNode method parity checklist:
    # [ ] bringToFront                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getIsPanelWidget             [ ] impl  [ ] docstring  [ ] test
    # [ ] getPanelWidgetInstancePath   [ ] impl  [ ] docstring  [ ] test
    # [ ] hideAllPorts                 [ ] impl  [ ] docstring  [ ] test
    # [ ] sendToBack                   [ ] impl  [ ] docstring  [ ] test
    # [ ] setPanelWidgetInstancePath   [ ] impl  [ ] docstring  [ ] test
    # [ ] showAllPorts                 [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPGraphElement methods (covered by RPGraphElement checklist)
    # No deprecated IRPGraphNode methods.

    def bring_to_front(self) -> None:
        """Brings this graph node to the front.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::bringToFront()
        """
        raise NotImplementedError

    def get_is_panel_widget(self) -> int:
        """Returns whether this graph node is a panel widget.

        Returns:
            Whether this graph node is a panel widget.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::getIsPanelWidget()
        """
        raise NotImplementedError

    def get_panel_widget_instance_path(self) -> "RPCollection":
        """Returns the panel widget instance path of this graph node.

        Returns:
            The panel widget instance path of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::getPanelWidgetInstancePath()
        """
        raise NotImplementedError

    def hide_all_ports(self) -> None:
        """Hides all ports of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::hideAllPorts()
        """
        raise NotImplementedError

    def send_to_back(self) -> None:
        """Sends this graph node to the back.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::sendToBack()
        """
        raise NotImplementedError

    def set_panel_widget_instance_path(self, panel_widget_instance_path: "RPCollection") -> None:
        """Specifies the panel widget instance path of this graph node.

        Args:
            panel_widget_instance_path: The panel widget instance path to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::setPanelWidgetInstancePath(com.telelogic.rhapsody.core.IRPCollection panelWidgetInstancePath)
        """
        raise NotImplementedError

    def show_all_ports(self) -> None:
        """Shows all ports of this graph node.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPGraphNode::showAllPorts()
        """
        raise NotImplementedError
