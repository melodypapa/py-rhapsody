"""RhapsodyApplication: the entry point for connecting to IBM Rhapsody."""

from typing import Any

try:
    import win32com.client
except ImportError:  # pragma: no cover - pywin32 is Windows-only
    # pywin32 is only installed on Windows (see pyproject.toml). Importing
    # this module must still succeed on other platforms (e.g. Sphinx
    # autodoc running on Read the Docs' Linux build image); the COM calls
    # themselves will simply fail at runtime with a clear error instead.
    win32com = None

from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException
from rhapsody_cli.models._core import RPCollection, _get_method_or_property, call_com
from rhapsody_cli.models.elements.containment import RPProject

_PROG_ID = "Rhapsody2.Application.1"


class RhapsodyApplication:
    """Wraps ``IRPApplication``, the top-level Rhapsody automation object."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    @classmethod
    def attach(cls) -> "RhapsodyApplication":
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = call_com(lambda: win32com.client.GetActiveObject(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"No running Rhapsody instance found: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def launch(cls) -> "RhapsodyApplication":
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = call_com(lambda: win32com.client.Dispatch(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"Failed to launch Rhapsody instance: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def connect(cls, prefer_attach: bool = True) -> "RhapsodyApplication":
        if prefer_attach:
            try:
                return cls.attach()
            except RhapsodyConnectionError:
                pass
        return cls.launch()

    def openProject(self, filename: str) -> RPProject:
        return RPProject(call_com(lambda: self._com.openProject(filename)))

    def createNewProject(self, project_location: str, project_name: str) -> RPProject:
        call_com(lambda: self._com.createNewProject(project_location, project_name))
        return self.activeProject()

    def activeProject(self) -> RPProject:
        return RPProject(call_com(lambda: self._com.activeProject()))

    def getProjects(self) -> RPCollection:
        return RPCollection(_get_method_or_property(self._com, "getProjects", "projects"))

    def quit(self) -> None:
        call_com(lambda: self._com.quit())
