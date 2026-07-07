"""Containment-family wrappers: mirrors IRPPackage and IRPProject from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, register_wrapper, wrap


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


class RPProject(RPPackage):
    """Wraps ``IRPProject``."""

    def addPackage(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addPackage(name)))

    def close(self) -> None:
        call_com(lambda: self._com.close())

    def becomeActiveProject(self) -> None:
        call_com(lambda: self._com.becomeActiveProject())

    def findComponent(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.findComponent(name)))

    def getPackages(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getPackages()))


register_wrapper("Package", RPPackage)
register_wrapper("Project", RPProject)
