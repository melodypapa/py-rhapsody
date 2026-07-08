"""Wraps ``com.telelogic.rhapsody.core.IRPInstance``."""

from rhapsody_cli.models._core import RPCollection, call_com, register_wrapper
from rhapsody_cli.models.elements.relations.model_relation import RPRelation


class RPInstance(RPRelation):
    """Wraps ``IRPInstance``: represents an instance in the model."""

    def getAllNestedElements(self) -> RPCollection:
        """Returns all nested elements within this instance.

        Returns:
            An ``RPCollection`` of nested model elements.
        """
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        """Gets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.

        Returns:
            The attribute value as a string.
        """
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        """Sets the value of an attribute on the instance.

        Args:
            attribute_name: The name of the attribute.
            attribute_value: The new value to set.
        """
        call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        """Returns all incoming links to this instance.

        Returns:
            An ``RPCollection`` of incoming link elements.
        """
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        """Returns all outgoing links from this instance.

        Returns:
            An ``RPCollection`` of outgoing link elements.
        """
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
