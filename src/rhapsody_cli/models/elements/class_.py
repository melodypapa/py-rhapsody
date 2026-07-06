"""RPClass: wraps IRPClass, a UML/SysML class in the Rhapsody model."""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifier import RPClassifier


class RPClass(RPClassifier):
    """Wraps ``IRPClass``."""

    def addSuperclass(self, super_class: RPClass) -> None:
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addClass(name)))


register_wrapper("Class", RPClass)
