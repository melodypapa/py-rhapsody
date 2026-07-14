"""Wraps ``com.telelogic.rhapsody.core.IRPInstance``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.relations.model_relation import RPRelation

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation


class RPInstance(RPRelation):
    """Wraps ``IRPInstance``: represents an instance in the model."""

    # IRPInstance method parity checklist:
    # [x] add_relation_to_the_whole        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_all_nested_elements         [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_attribute_value            [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_in_links                   [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] get_instantiated_by            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_list_of_initializer_arguments [x] impl [x] docstring  [x] unit test  [ ] integration test
    # [x] get_out_links                  [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_attribute_value            [x] impl  [x] docstring  [x] unit test  [ ] integration test   (already implemented)
    # [x] set_explicit                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_implicit                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_initializer_argument_value  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_instantiated_by            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] update_contained_diagrams_on_server [x] impl [x] docstring [x] unit test  [ ] integration test
    # No deprecated methods in IRPInstance.

    def get_all_nested_elements(self) -> RPCollection:
        """Returns a collection of all the model elements that are directly under the object.

        This method should be used instead of the inherited ``getNestedElements``
        method, because the latter does not return a complete list in the case
        of implicit objects.

        Returns:
            An ``RPCollection`` of nested model elements.

        Raises:
            RhapsodyRuntimeException: if the nested elements cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getAllNestedElements()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAllNestedElements", "allNestedElements"))

    def get_attribute_value(self, attribute_name: str) -> str:
        """Gets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.

        Returns:
            The attribute value as a string.

        Raises:
            RhapsodyRuntimeException: if the attribute value cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getAttributeValue(java.lang.String attName)
        """
        return AbstractRPModelElement.call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def set_attribute_value(self, attribute_name: str, attribute_value: str) -> None:
        """Sets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.
            attribute_value: The new value to set.

        Raises:
            RhapsodyRuntimeException: if the attribute value cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::setAttributeValue(java.lang.String attName, java.lang.String attValue)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def get_in_links(self) -> RPCollection:
        """Returns all incoming links to this instance.

        Returns:
            An ``RPCollection`` of incoming link elements.

        Raises:
            RhapsodyRuntimeException: if the incoming links cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getInLinks()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInLinks", "inLinks"))

    def get_out_links(self) -> RPCollection:
        """Returns all outgoing links from this instance.

        Returns:
            An ``RPCollection`` of outgoing link elements.

        Raises:
            RhapsodyRuntimeException: if the outgoing links cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getOutLinks()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getOutLinks", "outLinks"))

    def add_relation_to_the_whole(self, rel_name: str) -> "RPRelation":
        """Adds a relation to the whole for this instance.

        Args:
            rel_name: The name of the relation to add.

        Returns:
            The wrapped ``IRPRelation`` created.

        Raises:
            RhapsodyRuntimeException: if the relation cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::addRelationToTheWhole(java.lang.String relName)
        """
        return cast("RPRelation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addRelationToTheWhole(rel_name))))

    def get_instantiated_by(self) -> "RPOperation":
        """Returns the operation that instantiates this instance.

        Returns:
            The wrapped ``IRPOperation`` that instantiates this instance.

        Raises:
            RhapsodyRuntimeException: if the instantiating operation cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getInstantiatedBy()
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInstantiatedBy", "instantiatedBy")))

    def get_list_of_initializer_arguments(self) -> RPCollection:
        """Returns the list of initializer arguments for this instance.

        Returns:
            An ``RPCollection`` of initializer argument elements.

        Raises:
            RhapsodyRuntimeException: if the initializer arguments cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::getListOfInitializerArguments()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getListOfInitializerArguments", "listOfInitializerArguments"))

    def set_explicit(self) -> None:
        """Sets the instance to be explicit.

        Raises:
            RhapsodyRuntimeException: if the instance cannot be set explicit.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::setExplicit()
        """
        AbstractRPModelElement.call_com(lambda: self._com.setExplicit())

    def set_implicit(self) -> None:
        """Sets the instance to be implicit.

        Raises:
            RhapsodyRuntimeException: if the instance cannot be set implicit.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::setImplicit()
        """
        AbstractRPModelElement.call_com(lambda: self._com.setImplicit())

    def set_initializer_argument_value(self, arg_name: str, arg_value: str) -> None:
        """Sets the value of an initializer argument on the instance.

        Args:
            arg_name: The name of the initializer argument.
            arg_value: The new value to set.

        Raises:
            RhapsodyRuntimeException: if the initializer argument value cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::setInitializerArgumentValue(java.lang.String argName, java.lang.String argValue)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setInitializerArgumentValue(arg_name, arg_value))

    def set_instantiated_by(self, instantiated_by: RPModelElement) -> None:
        """Sets the operation that instantiates this instance.

        Args:
            instantiated_by: The operation (``IRPOperation``) that instantiates this instance.

        Raises:
            RhapsodyRuntimeException: if the instantiating operation cannot be set.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::setInstantiatedBy(com.telelogic.rhapsody.core.IRPOperation instantiatedBy)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setInstantiatedBy", "instantiatedBy", instantiated_by._com)

    def update_contained_diagrams_on_server(self, enforce_update: int) -> int:
        """Updates the views on the Rhapsody Model Manager server for all diagrams.

        Args:
            enforce_update: ``0`` to update only if changes were made,
                ``1`` to update regardless.

        Returns:
            The number of views updated, ``0`` if no update needed, ``-1`` on failure.

        Raises:
            RhapsodyRuntimeException: if the server update fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInstance::updateContainedDiagramsOnServer(int enforceUpdate)
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer(enforce_update)))


AbstractRPModelElement.register_wrapper("Instance", RPInstance)
