"""RhapsodyApplication: the entry point for connecting to IBM Rhapsody."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rhapsody_cli.models.support import (
        RPCodeGenSimplifiersRegistry,
        RPDiagSynthAPI,
        RPExternalCheckRegistry,
        RPExternalIDERegistry,
        RPExternalRoundtripInvoker,
        RPowPaneMgr,
        RPSearchManager,
        RPSelection,
    )

try:
    import win32com.client
except ImportError:  # pragma: no cover - pywin32 is Windows-only
    # pywin32 is only installed on Windows (see pyproject.toml). Importing
    # this module must still succeed on other platforms (e.g. Sphinx
    # autodoc running on Read the Docs' Linux build image); the COM calls
    # themselves will simply fail at runtime with a clear error instead.
    win32com = None

from rhapsody_cli import com_utils
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException
from rhapsody_cli.models.core import RPCollection
from rhapsody_cli.models.elements.containment import RPProject

_PROG_ID = "Rhapsody2.Application.1"


class RhapsodyApplication:
    """Wraps the ``IRPApplication`` COM interface.

    The IRPApplication interface represents the Rhapsody application, and its
    methods reflect many of the commands that you can access from the Rhapsody
    menu bar.
    """

    def __init__(self, com_obj: Any) -> None:
        """Initialize with a COM object representing IRPApplication.

        Args:
            com_obj: The COM object returned by GetActiveObject or Dispatch.
        """
        self._com = com_obj

    @classmethod
    def _attach(cls) -> "RhapsodyApplication":
        """Attach to an already-running Rhapsody instance (internal helper).

        Returns:
            A RhapsodyApplication wrapping the active COM object.

        Raises:
            RhapsodyConnectionError: If pywin32 is unavailable or no running
                Rhapsody instance can be found.
        """
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = com_utils.call_com(lambda: win32com.client.GetActiveObject(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"No running Rhapsody instance found: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def _launch(cls) -> "RhapsodyApplication":
        """Launch a new Rhapsody instance (internal helper).

        Returns:
            A RhapsodyApplication wrapping the newly launched COM object.

        Raises:
            RhapsodyConnectionError: If pywin32 is unavailable or launching
                Rhapsody fails.
        """
        if win32com is None:
            raise RhapsodyConnectionError("pywin32 is not available; Rhapsody automation requires Windows.")
        try:
            com_obj = com_utils.call_com(lambda: win32com.client.Dispatch(_PROG_ID))
        except RhapsodyRuntimeException as exc:
            raise RhapsodyConnectionError(f"Failed to launch Rhapsody instance: {exc}") from exc
        return cls(com_obj)

    @classmethod
    def connect(cls, attach_only: bool = False, show_gui: bool = True) -> "RhapsodyApplication":
        """Connect to Rhapsody, trying attach first with fallback to launch.

        Args:
            attach_only: If True, only try to attach to a running instance.
                Raises RhapsodyConnectionError if no instance is running.
            show_gui: When a new instance is launched, controls whether its
                GUI window is visible. Ignored when attaching to a running
                instance.

        Returns:
            A RhapsodyApplication wrapping the connected COM object.
        """
        try:
            return cls._attach()
        except RhapsodyConnectionError:
            if attach_only:
                raise
        app = cls._launch()
        if show_gui:
            app.set_hidden_ui(False)
        return app

    def open_project(self, filename: str) -> RPProject:
        """Open an existing Rhapsody project.

        Args:
            filename: The name of the .rpy file, including the full path.

        Returns:
            RPProject: The opened Rhapsody project.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::openProject(java.lang.String filename)
        """
        return RPProject(com_utils.call_com(lambda: self._com.openProject(filename)))

    def create_new_project(self, project_location: str, project_name: str) -> RPProject:
        """Create a new Rhapsody project.

        Args:
            project_location: The directory where the project should be saved.
            project_name: The name to use for the project (used for the .rpy file).

        Returns:
            RPProject: The newly created project, active after creation.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::createNewProject(java.lang.String projectLocation, java.lang.String projectName)
        """
        com_utils.call_com(lambda: self._com.createNewProject(project_location, project_name))
        return self.active_project()

    def active_project(self) -> RPProject:
        """Return the project currently open in Rhapsody.

        Returns:
            RPProject: The project currently open in Rhapsody.

        Raises:
            RhapsodyRuntimeException: If no project is currently open in
                Rhapsody (the COM call returns None).

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::activeProject()
        """
        result = com_utils.call_com(lambda: self._com.activeProject())
        if result is None:
            raise RhapsodyRuntimeException("No active project is open in Rhapsody")
        return RPProject(result)

    def get_projects(self) -> RPCollection:
        """Return all open projects in Rhapsody.

        Returns:
            RPCollection: A collection of the open RPProject objects.

        Raises:
            RhapsodyRuntimeException: If the projects cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getProjects()
        """
        return RPCollection(com_utils._get_method_or_property(self._com, "getProjects", "projects"))

    def quit(self) -> None:
        """Quit the Rhapsody application.

        Closes all projects and exits the Rhapsody process.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::quit()
        """
        com_utils.call_com(lambda: self._com.quit())

    def disconnect(self) -> None:
        """Disconnect from Rhapsody. Calls quit() and provides a cleanup hook."""
        self.quit()

    def get_is_hidden_ui(self) -> bool:
        """Return whether the Rhapsody GUI is hidden.

        Mirrors ``IRPApplication.getIsHiddenUI()``.

        Returns:
            bool: True if the Rhapsody UI is hidden, False if it is visible.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getIsHiddenUI()
        """
        return bool(com_utils._get_method_or_property(self._com, "getIsHiddenUI", "isHiddenUI"))

    def set_hidden_ui(self, hidden: bool) -> None:
        """Set whether the Rhapsody GUI is hidden.

        Mirrors ``IRPApplication.setHiddenUI()``. Rhapsody instances launched via
        COM automation (``Dispatch()``) start with the UI hidden by default; call
        ``setHiddenUI(False)`` after connecting to make the window visible.

        Args:
            hidden: False to show the GUI window, True to hide it.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::setHiddenUI(boolean pVal)
        """
        com_utils._set_method_or_property(self._com, "setHiddenUI", "isHiddenUI", hidden)

    def bring_window_to_top(self) -> None:
        """Bring the Rhapsody application window to the top.

        Mirrors ``IRPApplication.bringWindowToTop()``. Brings an already-visible
        window to the foreground; it does not make a hidden window visible. Use
        :meth:`setHiddenUI` with ``False`` to show the GUI first.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::bringWindowToTop()
        """
        com_utils.call_com(lambda: self._com.bringWindowToTop())

    def close_all_projects(self) -> None:
        """Close all open projects without quitting Rhapsody."""
        com_utils.call_com(lambda: self._com.closeAllProjects())

    def save_all(self) -> None:
        """Save all open projects.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::saveAll()
        """
        com_utils.call_com(lambda: self._com.saveAll())

    def get_version(self) -> str:
        """Get the Rhapsody version string.

        Returns:
            The version string (e.g. ``"8.3.1"``).
        """
        return str(com_utils.call_com(lambda: self._com.getVersion()))

    def get_build_no(self) -> str:
        """Return the Rhapsody build number.

        Returns:
            str: The build number.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getBuildNo()
        """
        return str(com_utils.call_com(lambda: self._com.getBuildNo()))

    def get_rhapsody_dir(self) -> str:
        """Get the Rhapsody installation directory.

        Returns:
            The installation directory path.
        """
        return str(com_utils.call_com(lambda: self._com.getRhapsodyDir()))

    def get_omroot(self) -> str:
        """Return the OMROOT directory path.

        Returns:
            str: The OMROOT path.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getOMROOT()
        """
        return str(com_utils.call_com(lambda: self._com.getOMROOT()))

    def create_new_collection(self) -> RPCollection:
        """Create a new empty ``IRPCollection`` for use with COM calls that require a pre-allocated collection.

        Some Rhapsody COM methods (e.g. ``IRPDiagram.getPicturesWithImageMap``) populate a
        caller-provided collection rather than returning one. Use this method to create
        the empty collection, pass it to such methods, then read the results from it.

        Returns:
            RPCollection: A new, empty collection.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::createNewCollection()
        """
        return RPCollection(com_utils.call_com(lambda: self._com.createNewCollection()))

    def get_search_manager(self) -> "RPSearchManager":
        """Return the Rhapsody search manager.

        Returns:
            RPSearchManager: The search manager for finding model elements.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getSearchManager()
        """
        from rhapsody_cli.models.support import RPSearchManager

        return RPSearchManager(com_utils.call_com(lambda: self._com.getSearchManager()))

    def get_selection(self) -> "RPSelection":
        """Return the current Rhapsody selection.

        Returns:
            RPSelection: The current selection in the Rhapsody UI.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getSelection()
        """
        from rhapsody_cli.models.support import RPSelection

        return RPSelection(com_utils.call_com(lambda: self._com.getSelection()))

    def get_code_gen_simplifiers_registry(self) -> "RPCodeGenSimplifiersRegistry":
        """Return the code-gen simplifiers registry.

        Returns:
            RPCodeGenSimplifiersRegistry: The registry of code generation simplifiers.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getCodeGenSimplifiersRegistry()
        """
        from rhapsody_cli.models.support import RPCodeGenSimplifiersRegistry

        return RPCodeGenSimplifiersRegistry(com_utils.call_com(lambda: self._com.getCodeGenSimplifiersRegistry()))

    def get_diag_synth_api(self, client_name: str) -> "RPDiagSynthAPI":
        """Return the diagram synthesis API for the given client.

        Args:
            client_name: The name of the client requesting the API.

        Returns:
            RPDiagSynthAPI: The diagram synthesis API.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getDiagSynthAPI(java.lang.String clientName)
        """
        from rhapsody_cli.models.support import RPDiagSynthAPI

        return RPDiagSynthAPI(com_utils.call_com(lambda: self._com.getDiagSynthAPI(client_name)))

    def get_external_checker_registry(self) -> "RPExternalCheckRegistry":
        """Return the external checker registry.

        Returns:
            RPExternalCheckRegistry: The registry of external model checkers.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getExternalCheckerRegistry()
        """
        from rhapsody_cli.models.support import RPExternalCheckRegistry

        return RPExternalCheckRegistry(com_utils.call_com(lambda: self._com.getExternalCheckerRegistry()))

    def get_external_ide_registry(self, client_id: str) -> "RPExternalIDERegistry":
        """Return the external IDE registry for the given client.

        Args:
            client_id: The ID of the client requesting the registry.

        Returns:
            RPExternalIDERegistry: The external IDE registry.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getExternalIDERegistry(java.lang.String clientID)
        """
        from rhapsody_cli.models.support import RPExternalIDERegistry

        return RPExternalIDERegistry(com_utils.call_com(lambda: self._com.getExternalIDERegistry(client_id)))

    def get_external_roundtrip_invoker(self) -> "RPExternalRoundtripInvoker":
        """Return the external roundtrip invoker.

        Returns:
            RPExternalRoundtripInvoker: The external roundtrip invoker.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getExternalRoundtripInvoker()
        """
        from rhapsody_cli.models.support import RPExternalRoundtripInvoker

        return RPExternalRoundtripInvoker(com_utils.call_com(lambda: self._com.getExternalRoundtripInvoker()))

    def get_ow_pane_mgr(self, client_id: str) -> "RPowPaneMgr":
        """Return the output window pane manager for the given client.

        Args:
            client_id: The ID of the client requesting the pane manager.

        Returns:
            RPowPaneMgr: The output window pane manager.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::getOWPaneMgr(java.lang.String clientID)
        """
        from rhapsody_cli.models.support import RPowPaneMgr

        return RPowPaneMgr(com_utils.call_com(lambda: self._com.getOWPaneMgr(client_id)))

    def generate(self) -> None:
        """Generate code for the entire project.

        Uses the active component and configuration. Use
        ``RPProject.setActiveComponent`` and ``RPProject.setActiveConfiguration``
        to change them first if necessary.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::generate()
        """
        com_utils.call_com(lambda: self._com.generate())

    def generate_elements(self, elements: RPCollection) -> None:
        """Generate code for the given elements.

        Args:
            elements: An RPCollection of elements to generate code for.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::generateElements(com.telelogic.rhapsody.core.IRPCollection elements)
        """
        com_utils.call_com(lambda: self._com.generateElements(elements._com))

    def generate_entire_project(self) -> None:
        """Generate code for the entire active project.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::generateEntireProject()
        """
        com_utils.call_com(lambda: self._com.generateEntireProject())

    def regenerate(self) -> None:
        """Regenerate code for the active project (full regeneration).

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::regenerate()
        """
        com_utils.call_com(lambda: self._com.regenerate())

    def add_to_model(self, filename: str, with_descendant: int) -> None:
        """Add a model element from a file to the model.

        Args:
            filename: Path to the file to add.
            with_descendant: 1 to also add descendants, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::addToModel(java.lang.String filename, int withDescendant)
        """
        com_utils.call_com(lambda: self._com.addToModel(filename, with_descendant))

    def add_to_model_ex(self, filename: str, mode: int, add_sub_units: int, add_dependents: int) -> None:
        """Add a unit to the model with extended options.

        Args:
            filename: The full path to the file to add to the model.
            mode: How the unit should be added (see IRPApplication.AddToModel_Mode).
            add_sub_units: 1 to also add the unit's sub-units, 0 otherwise. Ignored
                when ``mode`` equals IRPApplication.AddToModel_Mode.AS_UNIT_WITHOUT_COPY.
            add_dependents: 1 to also add units that elements in the unit depend
                on, 0 otherwise. Ignored when ``mode`` equals
                IRPApplication.AddToModel_Mode.AS_UNIT_WITHOUT_COPY.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::addToModelEx(java.lang.String filename, int addToModelMode, int addSubUnits, int addDependents)
        """
        com_utils.call_com(lambda: self._com.addToModelEx(filename, mode, add_sub_units, add_dependents))

    def set_log(self, full_pathname: str) -> None:
        """Set the log file path.

        Args:
            full_pathname: Full path to the log file.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::setLog(java.lang.String logFile)
        """
        com_utils.call_com(lambda: self._com.setLog(full_pathname))

    def check_model(self) -> None:
        """Run model checking on the active project.

        Raises:
            RhapsodyRuntimeException: If the underlying COM call fails.

        Reference:
            com.telelogic.rhapsody.core.IRPApplication::checkModel()
        """
        com_utils.call_com(lambda: self._com.checkModel())
