"""RPPackage: wraps IRPPackage, a container for classes, actors, and other elements."""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPUnit, call_com, register_wrapper, wrap


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``."""

    def addClass(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addClass(name)))

    def addNestedPackage(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addNestedPackage(name)))

    def addActor(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addActor(name)))

    def addGlobalFunction(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addGlobalFunction(name)))


register_wrapper("Package", RPPackage)
