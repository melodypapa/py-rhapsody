"""Wraps ``com.telelogic.rhapsody.core.IRPInstance``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.relations.model_relation import RPRelation

# IRPInstance method parity checklist:
# [x] addRelationToTheWhole        [x] impl  [x] docstring  [x] test
# [x] getAllNestedElements         [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getAttributeValue            [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getInLinks                   [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getInstantiatedBy            [x] impl  [x] docstring  [x] test
# [x] getListOfInitializerArguments [x] impl [x] docstring  [x] test
# [x] getOutLinks                  [x] impl  [x] docstring  [x] test   (already implemented)
# [x] setAttributeValue            [x] impl  [x] docstring  [x] test   (already implemented)
# [x] setExplicit                  [x] impl  [x] docstring  [x] test
# [x] setImplicit                  [x] impl  [x] docstring  [x] test
# [x] setInitializerArgumentValue  [x] impl  [x] docstring  [x] test
# [x] setInstantiatedBy            [x] impl  [x] docstring  [x] test
# [x] updateContainedDiagramsOnServer [x] impl [x] docstring [x] test
# No deprecated methods in IRPInstance.


class RPInstance(RPRelation):
    """Wraps ``IRPInstance``: represents an instance in the model."""

    def getAllNestedElements(self) -> RPCollection:
        """Returns all nested elements within this instance.

        Returns:
            An ``RPCollection`` of nested model elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAllNestedElements", "allNestedElements"))

    def getAttributeValue(self, attribute_name: str) -> str:
        """Gets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.

        Returns:
            The attribute value as a string.
        """
        return AbstractRPModelElement.call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        """Sets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.
            attribute_value: The new value to set.
        """
        AbstractRPModelElement.call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        """Returns all incoming links to this instance.

        Returns:
            An ``RPCollection`` of incoming link elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getInLinks", "inLinks"))

    def getOutLinks(self) -> RPCollection:
        """Returns all outgoing links from this instance.

        Returns:
            An ``RPCollection`` of outgoing link elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getOutLinks", "outLinks"))

    def addRelationToTheWhole(self, rel_name: str) -> Any:
        """Adds a relation to the whole for this instance.

        Args:
            rel_name: The name of the relation to add.

        Returns:
            The wrapped ``IRPRelation`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addRelationToTheWhole(rel_name)))

    def getInstantiatedBy(self) -> Any:
        """Returns the operation that instantiates this instance.

        Returns:
            The wrapped ``IRPOperation`` that instantiates this instance.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getInstantiatedBy", "instantiatedBy"))

    def getListOfInitializerArguments(self) -> RPCollection:
        """Returns the list of initializer arguments for this instance.

        Returns:
            An ``RPCollection`` of initializer argument elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getListOfInitializerArguments", "listOfInitializerArguments"))

    def setExplicit(self) -> None:
        """Sets the instance to be explicit."""
        AbstractRPModelElement.call_com(lambda: self._com.setExplicit())

    def setImplicit(self) -> None:
        """Sets the instance to be implicit."""
        AbstractRPModelElement.call_com(lambda: self._com.setImplicit())

    def setInitializerArgumentValue(self, arg_name: str, arg_value: str) -> None:
        """Sets the value of an initializer argument on the instance.

        Args:
            arg_name: The name of the initializer argument.
            arg_value: The new value to set.
        """
        AbstractRPModelElement.call_com(lambda: self._com.setInitializerArgumentValue(arg_name, arg_value))

    def setInstantiatedBy(self, instantiated_by: RPModelElement) -> None:
        """Sets the operation that instantiates this instance.

        Args:
            instantiated_by: The operation (``IRPOperation``) that instantiates this instance.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setInstantiatedBy", "instantiatedBy", instantiated_by._com)

    def updateContainedDiagramsOnServer(self, enforce_update: int) -> int:
        """Updates the views on the Rhapsody Model Manager server for all diagrams.

        Args:
            enforce_update: ``0`` to update only if changes were made,
                ``1`` to update regardless.

        Returns:
            The number of views updated, ``0`` if no update needed, ``-1`` on failure.
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer(enforce_update)))


AbstractRPModelElement.register_wrapper("Instance", RPInstance)
