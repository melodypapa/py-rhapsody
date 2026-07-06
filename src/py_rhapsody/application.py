"""RhapsodyApplication: the entry point for connecting to IBM Rhapsody."""

from __future__ import annotations

from typing import Any

import win32com.client

from py_rhapsody.models._core import RPCollection, call_com
from py_rhapsody.models.elements.project import RPProject
from py_rhapsody.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

_PROG_ID = "Rhapsody.Application"


class RhapsodyApplication:
    """Wraps ``IRPApplication``, the top-level Rhapsody automation object."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    @classmethod
    def attach(cls) -> RhapsodyApplication:
        try:
            com_obj = call_com(lambda: win32com.client.GetActiveObject(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"No running Rhapsody instance found: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def launch(cls) -> RhapsodyApplication:
        try:
            com_obj = call_com(lambda: win32com.client.Dispatch(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"Failed to launch Rhapsody instance: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def connect(cls, prefer_attach: bool = True) -> RhapsodyApplication:
        if prefer_attach:
            try:
                return cls.attach()
            except RhapsodyConnectionError:
                pass
        return cls.launch()

    def openProject(self, filename: str) -> RPProject:
        return RPProject(call_com(lambda: self._com.openProject(filename)))

    def activeProject(self) -> RPProject:
        return RPProject(call_com(lambda: self._com.activeProject()))

    def getProjects(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getProjects()))

    def quit(self) -> None:
        call_com(lambda: self._com.quit())
