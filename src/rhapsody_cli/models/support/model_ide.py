"""Ide model-element wrappers (auto-generated stubs)."""

from typing import Any

from rhapsody_cli.models.core import RPModelElement


class RPAXViewCtrl(RPModelElement):
    """Wraps ``IRPAXViewCtrl``."""

    # IRPAXViewCtrl method parity checklist:
    # [ ] doCommand                    [ ] impl  [ ] docstring  [ ] test
    # [ ] executeCommand               [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPAXViewCtrl methods.

    def do_command(self, command_i_d: int) -> None:
        """Execute command by command ID.

        Args:
            command_i_d: The ID of the command to execute.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPAXViewCtrl::doCommand(long commandID)
        """
        raise NotImplementedError

    def execute_command(self, command_type: str, p_command_initialization: "RPCollection", p_command_result: "RPCollection") -> None:
        """Execute command.

        Args:
            command_type: The type of command to execute.
            p_command_initialization: Collection used for command initialization.
            p_command_result: Collection to receive the command results.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPAXViewCtrl::executeCommand(java.lang.String commandType, com.telelogic.rhapsody.core.IRPCollection pCommandInitialization, com.telelogic.rhapsody.core.IRPCollection pCommandResult)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPAXViewCtrl::getInterfaceName()
        """
        raise NotImplementedError


class RPExternalIDERegistry(RPModelElement):
    """Wraps ``IRPExternalIDERegistry``."""

    # IRPExternalIDERegistry method parity checklist:
    # [ ] progressTaskAsynchCallback   [ ] impl  [ ] docstring  [ ] test
    # [ ] progressTaskAsynchEliminate  [ ] impl  [ ] docstring  [ ] test
    # [ ] sendIDETextMessage           [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPExternalIDERegistry methods.

    def progress_task_asynch_callback(self, n_group_number: int, n_task_number: int) -> None:
        """Initiate progress task execution.

        Args:
            n_group_number: The group number of the task.
            n_task_number: The task number within the group.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalIDERegistry::progressTaskAsynchCallback(int nGroupNumber, int nTaskNumber)
        """
        raise NotImplementedError

    def progress_task_asynch_eliminate(self, n_group_number: int, n_task_number: int) -> None:
        """Initiate progress task execution.

        Args:
            n_group_number: The group number of the task.
            n_task_number: The task number within the group.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalIDERegistry::progressTaskAsynchEliminate(int nGroupNumber, int nTaskNumber)
        """
        raise NotImplementedError

    def send_i_d_e_text_message(self, message: str) -> None:
        """Send an IDE text message.

        Args:
            message: The text message to send to the IDE.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalIDERegistry::sendIDETextMessage(java.lang.String message)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalIDERegistry::getInterfaceName()
        """
        raise NotImplementedError


class RPInternalOEMPlugin(RPModelElement):
    """Wraps ``IRPInternalOEMPlugin``."""

    # IRPInternalOEMPlugin method parity checklist:
    # [ ] activeProjectAboutToChange   [ ] impl  [ ] docstring  [ ] test
    # [ ] activeProjectHasChanged      [ ] impl  [ ] docstring  [ ] test
    # [ ] onMenuItemSelect             [ ] impl  [ ] docstring  [ ] test
    # [ ] onMenuItemSelectWithParameters [ ] impl  [ ] docstring  [ ] test
    # [ ] rhapPluginAnimationStopped   [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginAnimationStarted    [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginCleanup             [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginDoCommand           [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginFinalCleanup        [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginInit                [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginInvokeItem          [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginOnIDEBuildDone      [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpPluginSetApplication      [ ] impl  [ ] docstring  [ ] test
    # [ ] rhpSavingProject             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPInternalOEMPlugin methods.

    def active_project_about_to_change(self) -> int:
        """Notify the plugin that the active project is about to change.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::activeProjectAboutToChange()
        """
        raise NotImplementedError

    def active_project_has_changed(self) -> int:
        """Notify the plugin that the active project has changed.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::activeProjectHasChanged()
        """
        raise NotImplementedError

    def on_menu_item_select(self, menu_item: str) -> str:
        """Select a given menu item.

        Args:
            menu_item: The menu item to select.

        Returns:
            The result of the menu item selection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::onMenuItemSelect(java.lang.String menuItem)
        """
        raise NotImplementedError

    def on_menu_item_select_with_parameters(self, menu_item: str, parameters: str) -> str:
        """For internal use only.

        Args:
            menu_item: The menu item to select.
            parameters: Additional parameters for the menu item selection.

        Returns:
            The result of the menu item selection.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::onMenuItemSelectWithParameters(java.lang.String menuItem, java.lang.String parameters)
        """
        raise NotImplementedError

    def rhap_plugin_animation_stopped(self) -> int:
        """Notify the plugin that animation has stopped.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhapPluginAnimationStopped()
        """
        raise NotImplementedError

    def rhp_plugin_animation_started(self) -> int:
        """Notify the plugin that animation has started.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginAnimationStarted()
        """
        raise NotImplementedError

    def rhp_plugin_cleanup(self) -> int:
        """Perform cleanup of the plugin.

        Returns:
            The result of the cleanup operation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginCleanup()
        """
        raise NotImplementedError

    def rhp_plugin_do_command(self, the_command: str) -> None:
        """Notify the plugin to execute a command.

        Args:
            the_command: The command to execute.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginDoCommand(java.lang.String theCommand)
        """
        raise NotImplementedError

    def rhp_plugin_final_cleanup(self) -> int:
        """Perform final cleanup of the plugin.

        Returns:
            The result of the final cleanup operation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginFinalCleanup()
        """
        raise NotImplementedError

    def rhp_plugin_init(self) -> int:
        """Initialize the plugin.

        Returns:
            The result of the initialization.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginInit()
        """
        raise NotImplementedError

    def rhp_plugin_invoke_item(self) -> int:
        """Invoke an item of the plugin.

        Returns:
            The result of the item invocation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginInvokeItem()
        """
        raise NotImplementedError

    def rhp_plugin_on_i_d_e_build_done(self, build_status: str) -> None:
        """Notify the plugin that an IDE build is done.

        Args:
            build_status: The status of the build.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginOnIDEBuildDone(java.lang.String buildStatus)
        """
        raise NotImplementedError

    def rhp_plugin_set_application(self, p_r_p_app: "RPApplication") -> int:
        """Set the IRPApplication of the plugin.

        Args:
            p_r_p_app: The IRPApplication instance to set.

        Returns:
            The result of setting the application.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginSetApplication(com.telelogic.rhapsody.core.IRPApplication pRPApp)
        """
        raise NotImplementedError

    def rhp_saving_project(self) -> int:
        """Notify the plugin that a Rhapsody save is occurring.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpSavingProject()
        """
        raise NotImplementedError


class RPJavaPlugins(RPModelElement):
    """Wraps ``IRPJavaPlugins``."""

    # IRPJavaPlugins method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPJavaPlugins methods.

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPJavaPlugins::getInterfaceName()
        """
        raise NotImplementedError


class RPPlugInWindow(RPModelElement):
    """Wraps ``IRPPlugInWindow``."""

    # IRPPlugInWindow method parity checklist:
    # [ ] destroyWindow                [ ] impl  [ ] docstring  [ ] test
    # [ ] getDocking                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getPosString                 [ ] impl  [ ] docstring  [ ] test
    # [ ] getWindowHandle              [ ] impl  [ ] docstring  [ ] test
    # [ ] setDocking                   [ ] impl  [ ] docstring  [ ] test
    # [ ] setPosString                 [ ] impl  [ ] docstring  [ ] test
    # [ ] setTitle                     [ ] impl  [ ] docstring  [ ] test
    # [ ] showWindow                   [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPPlugInWindow methods.

    def destroy_window(self) -> None:
        """Destroy the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::destroyWindow()
        """
        raise NotImplementedError

    def get_docking(self) -> int:
        """Get the docking mode.

        Returns:
            The current docking mode.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getDocking()
        """
        raise NotImplementedError

    def get_pos_string(self) -> str:
        """Get the position string.

        Returns:
            The position string of the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getPosString()
        """
        raise NotImplementedError

    def get_window_handle(self) -> int:
        """Get the window handle.

        Returns:
            The window handle.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getWindowHandle()
        """
        raise NotImplementedError

    def set_docking(self, n_dock_pos: int) -> None:
        """Set the docking mode.

        Args:
            n_dock_pos: The docking position (0=floating, 1=top, 2=left, 3=right, 4=bottom).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setDocking(int nDockPos)
        """
        raise NotImplementedError

    def set_pos_string(self, s_pos: str) -> None:
        """Set the position string.

        Args:
            s_pos: The position string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setPosString(java.lang.String sPos)
        """
        raise NotImplementedError

    def set_title(self, s_title: str) -> None:
        """Set the window title.

        Args:
            s_title: The title to set for the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setTitle(java.lang.String sTitle)
        """
        raise NotImplementedError

    def show_window(self, n_show: int) -> None:
        """Show or hide the window.

        Args:
            n_show: The show/hide flag.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::showWindow(int nShow)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getInterfaceName()
        """
        raise NotImplementedError


class RPProgressBar(RPModelElement):
    """Wraps ``IRPProgressBar``."""

    # IRPProgressBar method parity checklist:
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] reset                        [ ] impl  [ ] docstring  [ ] test
    # [ ] tick                         [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPProgressBar methods.

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPProgressBar::getInterfaceName()
        """
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the progress bar.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPProgressBar::reset()
        """
        raise NotImplementedError

    def tick(self, amount: int) -> None:
        """Advance the progress bar by a given amount.

        Args:
            amount: The amount to advance the progress bar.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPProgressBar::tick(int amount)
        """
        raise NotImplementedError


class RPSelection(RPModelElement):
    """Wraps ``IRPSelection``: contains methods for cutting, copying, pasting, and deleting graphic elements on diagrams."""

    # IRPSelection method parity checklist:
    # [ ] canCopy                      [ ] impl  [ ] docstring  [ ] test
    # [ ] canCut                       [ ] impl  [ ] docstring  [ ] test
    # [ ] canDelete                    [ ] impl  [ ] docstring  [ ] test
    # [ ] canPaste                     [ ] impl  [ ] docstring  [ ] test
    # [ ] copySelected                 [ ] impl  [ ] docstring  [ ] test
    # [ ] cutSelected                  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteSelected               [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] pasteSelected                [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPSelection methods.

    def can_copy(self) -> int:
        """Check whether the current selection can be copied.

        Returns:
            1 if the current selection can be copied, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canCopy()
        """
        raise NotImplementedError

    def can_cut(self) -> int:
        """Check whether the current selection can be cut.

        Returns:
            1 if the current selection can be cut, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canCut()
        """
        raise NotImplementedError

    def can_delete(self) -> int:
        """Check whether the current selection can be deleted.

        Returns:
            1 if the current selection can be deleted, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canDelete()
        """
        raise NotImplementedError

    def can_paste(self) -> int:
        """Check whether the item in the clipboard can be pasted to the diagram that has the focus.

        Returns:
            1 if the item in the clipboard can be pasted, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canPaste()
        """
        raise NotImplementedError

    def copy_selected(self) -> int:
        """Copy the currently selected graphic element.

        Returns:
            1 if the copy operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::copySelected()
        """
        raise NotImplementedError

    def cut_selected(self) -> int:
        """Cut the currently selected graphic element.

        Returns:
            1 if the cut operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::cutSelected()
        """
        raise NotImplementedError

    def delete_selected(self) -> int:
        """Delete the currently selected graphic element.

        Returns:
            1 if the delete operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::deleteSelected()
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Return the name of the API interface corresponding to the object it is called on.

        Returns:
            The name of the API interface corresponding to the object.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::getInterfaceName()
        """
        raise NotImplementedError

    def paste_selected(self) -> int:
        """Paste the item in the clipboard to the diagram that has the focus.

        Returns:
            1 if the paste operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::pasteSelected()
        """
        raise NotImplementedError


class RPowListListener(RPModelElement):
    """Wraps ``IRPowListListener``."""

    # IRPowListListener method parity checklist:
    # [ ] dblClickNotify               [ ] impl  [ ] docstring  [ ] test
    # [ ] setObjID                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPowListListener methods.

    def dbl_click_notify(self, n_row: int, n_col: int, s_content: str) -> None:
        """Notify on double-click in the list.

        Args:
            n_row: The row index of the double-clicked cell.
            n_col: The column index of the double-clicked cell.
            s_content: The content of the double-clicked cell.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowListListener::dblClickNotify(int nRow, int nCol, java.lang.String sContent)
        """
        raise NotImplementedError

    def set_obj_i_d(self, bstr_obj_i_d: str) -> None:
        """Set the object ID.

        Args:
            bstr_obj_i_d: The object ID string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowListListener::setObjID(java.lang.String bstrObjID)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowListListener::getInterfaceName()
        """
        raise NotImplementedError


class RPowPaneMgr(RPModelElement):
    """Wraps ``IRPowPaneMgr``."""

    # IRPowPaneMgr method parity checklist:
    # [ ] addTabNotify                 [ ] impl  [ ] docstring  [ ] test
    # [ ] closeTabNotify               [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # [ ] getOWListListener            [ ] impl  [ ] docstring  [ ] test
    # [ ] getOWTextListener            [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPowPaneMgr methods.

    def add_tab_notify(self, n_type: int, n_sub_type: int, s_obj_i_d: str, s_title: str) -> None:
        """Notify when a tab is added.

        Args:
            n_type: The type of the tab.
            n_sub_type: The sub-type of the tab.
            s_obj_i_d: The object ID associated with the tab.
            s_title: The title of the tab.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::addTabNotify(int nType, int nSubType, java.lang.String sObjID, java.lang.String sTitle)
        """
        raise NotImplementedError

    def close_tab_notify(self, s_obj_i_d: str) -> None:
        """Notify when a tab is closed.

        Args:
            s_obj_i_d: The object ID of the tab being closed.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::closeTabNotify(java.lang.String sObjID)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::getInterfaceName()
        """
        raise NotImplementedError

    def get_o_w_list_listener(self, s_obj_i_d: str) -> Any:
        """Get the list listener for the given object ID.

        Args:
            s_obj_i_d: The object ID to look up.

        Returns:
            The IRPowListListener for the given object ID.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::getOWListListener(java.lang.String sObjID)
        """
        raise NotImplementedError

    def get_o_w_text_listener(self, s_obj_i_d: str) -> Any:
        """Get the text listener for the given object ID.

        Args:
            s_obj_i_d: The object ID to look up.

        Returns:
            The IRPowTextListener for the given object ID.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::getOWTextListener(java.lang.String sObjID)
        """
        raise NotImplementedError


class RPowTextListener(RPModelElement):
    """Wraps ``IRPowTextListener``."""

    # IRPowTextListener method parity checklist:
    # [ ] dblClickNotify               [ ] impl  [ ] docstring  [ ] test
    # [ ] setObjID                     [ ] impl  [ ] docstring  [ ] test
    # [ ] getInterfaceName             [ ] impl  [ ] docstring  [ ] test
    # No deprecated IRPowTextListener methods.

    def dbl_click_notify(self, n_line: int, sz_line: str) -> None:
        """Notify on double-click in the text pane.

        Args:
            n_line: The line number of the double-clicked text.
            sz_line: The text content of the double-clicked line.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowTextListener::dblClickNotify(int nLine, java.lang.String szLine)
        """
        raise NotImplementedError

    def set_obj_i_d(self, bstr_obj_i_d: str) -> None:
        """Set the object ID.

        Args:
            bstr_obj_i_d: The object ID string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowTextListener::setObjID(java.lang.String bstrObjID)
        """
        raise NotImplementedError

    def get_interface_name(self) -> str:
        """Get the interfaceName property.

        Returns:
            The name of the interface.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowTextListener::getInterfaceName()
        """
        raise NotImplementedError
