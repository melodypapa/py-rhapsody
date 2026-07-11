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
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.containment import RPProject

_PROG_ID = "Rhapsody2.Application.1"


class RhapsodyApplication:
    """Wraps ``IRPApplication``, the top-level Rhapsody automation object."""

    def __init__(self, com_obj: Any) -> None:
        """Initialize with a COM object representing IRPApplication.

        Args:
            com_obj: The COM object returned by GetActiveObject or Dispatch.
        """
        self._com = com_obj

    @classmethod
    def attach(cls) -> "RhapsodyApplication":
        """Attach to an already-running Rhapsody instance.

        Returns:
            A RhapsodyApplication wrapping the active COM object.

        Raises:
            RhapsodyConnectionError: If pywin32 is unavailable or no running
                Rhapsody instance can be found.
        """
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = AbstractRPModelElement.call_com(lambda: win32com.client.GetActiveObject(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"No running Rhapsody instance found: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def launch(cls) -> "RhapsodyApplication":
        """Launch a new Rhapsody instance.

        Returns:
            A RhapsodyApplication wrapping the newly launched COM object.

        Raises:
            RhapsodyConnectionError: If pywin32 is unavailable or launching
                Rhapsody fails.
        """
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = AbstractRPModelElement.call_com(lambda: win32com.client.Dispatch(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"Failed to launch Rhapsody instance: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def connect(cls, prefer_attach: bool = True) -> "RhapsodyApplication":
        """Connect to Rhapsody, preferring attach over launch.

        Args:
            prefer_attach: If True, first try to attach to an existing instance;
                if that fails or prefer_attach is False, launch a new instance.

        Returns:
            A RhapsodyApplication wrapping the connected COM object.
        """
        if prefer_attach:
            try:
                return cls.attach()
            except RhapsodyConnectionError:
                pass
        return cls.launch()

    def openProject(self, filename: str) -> RPProject:
        """Open a Rhapsody project file.

        Args:
            filename: Path to the .rpy project file.

        Returns:
            The opened RPProject object.
        """
        return RPProject(AbstractRPModelElement.call_com(lambda: self._com.openProject(filename)))

    def createNewProject(self, project_location: str, project_name: str) -> RPProject:
        """Create a new Rhapsody project.

        Args:
            project_location: Directory path where the project will be created.
            project_name: Name of the new project.

        Returns:
            The newly created RPProject object (active after creation).
        """
        AbstractRPModelElement.call_com(lambda: self._com.createNewProject(project_location, project_name))
        return self.activeProject()

    def activeProject(self) -> RPProject:
        """Get the currently active project in Rhapsody.

        Returns:
            The active RPProject object.
        """
        return RPProject(AbstractRPModelElement.call_com(lambda: self._com.activeProject()))

    def getProjects(self) -> RPCollection:
        """Get all open projects in Rhapsody.

        Returns:
            An RPCollection of RPProject objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getProjects", "projects"))

    def quit(self) -> None:
        """Quit the Rhapsody application.

        This closes all projects and exits the Rhapsody process.
        """
        AbstractRPModelElement.call_com(lambda: self._com.quit())

    def getIsHiddenUI(self) -> bool:
        """Get whether the Rhapsody GUI is hidden (mirrors ``IRPApplication.getIsHiddenUI()``).

        Returns:
            True if the Rhapsody UI is hidden, False if it is visible.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsHiddenUI", "isHiddenUI"))

    def setHiddenUI(self, hidden: bool) -> None:
        """Set whether the Rhapsody GUI is hidden (mirrors ``IRPApplication.setHiddenUI()``).

        Rhapsody instances launched via COM automation (``Dispatch()``) start
        with the UI hidden by default. Call ``setHiddenUI(False)`` after
        connecting to make the Rhapsody window visible.

        Args:
            hidden: False to show the GUI window, True to hide it.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setHiddenUI", "isHiddenUI", hidden)

    def bringWindowToTop(self) -> None:
        """Bring the Rhapsody application window to the top (mirrors ``IRPApplication.bringWindowToTop()``).

        Note: this brings an already-visible window to the foreground; it does
        not make a hidden window visible. Use :meth:`setHiddenUI` with ``False``
        to show the GUI first.
        """
        AbstractRPModelElement.call_com(lambda: self._com.bringWindowToTop())
