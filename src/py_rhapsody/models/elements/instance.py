"""RPInstance: wraps IRPInstance, an instance/object in the Rhapsody model."""

from __future__ import annotations

from py_rhapsody.models._core import RPCollection, RPUnit, call_com, register_wrapper


class RPInstance(RPUnit):
    """Wraps ``IRPInstance``."""

    def getAllNestedElements(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
