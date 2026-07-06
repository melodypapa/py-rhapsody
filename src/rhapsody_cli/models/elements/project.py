"""RPProject: wraps IRPProject, the top-level container for a Rhapsody model."""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, register_wrapper, wrap


class RPProject(RPUnit):
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


register_wrapper("Project", RPProject)
