"""Ide model-element wrappers (auto-generated stubs)."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import RPCollection, RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.application import RhapsodyApplication


class RPAXViewCtrl(RPModelElement):
    """Wraps ``IRPAXViewCtrl``."""

    # IRPAXViewCtrl method parity checklist:
    # [x] do_command                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] execute_command               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
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
        self.call_com(lambda: self._com.doCommand(command_i_d))

    def execute_command(self, command_type: str, p_command_initialization: "RPCollection", p_command_result: "RPCollection") -> None:
        """Execute command.

        Args:
            command_type: The type of command to execute.
            p_command_initialization: Collection used for command initialization.
            p_command_result: Collection to receive the command results.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPAXViewCtrl::executeCommand(
                java.lang.String commandType,
                com.telelogic.rhapsody.core.IRPCollection pCommandInitialization,
                com.telelogic.rhapsody.core.IRPCollection pCommandResult)
        """
        self.call_com(lambda: self._com.executeCommand(command_type, p_command_initialization._com, p_command_result._com))


class RPExternalIDERegistry(RPModelElement):
    """Wraps ``IRPExternalIDERegistry``."""

    # IRPExternalIDERegistry method parity checklist:
    # [x] progress_task_asynch_callback   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] progress_task_asynch_eliminate  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] send_ide_text_message           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
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
        self.call_com(lambda: self._com.progressTaskAsynchCallback(n_group_number, n_task_number))

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
        self.call_com(lambda: self._com.progressTaskAsynchEliminate(n_group_number, n_task_number))

    def send_ide_text_message(self, message: str) -> None:
        """Send an IDE text message.

        Args:
            message: The text message to send to the IDE.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPExternalIDERegistry::sendIDETextMessage(java.lang.String message)
        """
        self.call_com(lambda: self._com.sendIDETextMessage(message))


class RPInternalOEMPlugin(RPModelElement):
    """Wraps ``IRPInternalOEMPlugin``."""

    # IRPInternalOEMPlugin method parity checklist:
    # [x] active_project_about_to_change   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] active_project_has_changed      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] on_menu_item_select             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] on_menu_item_select_with_parameters [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhap_plugin_animation_stopped   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_animation_started    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_cleanup             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_do_command           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_final_cleanup        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_init                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_invoke_item          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_on_ide_build_done      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_plugin_set_application      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] rhp_saving_project             [x] impl  [x] docstring  [x] unit test  [ ] integration test
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
        return int(self.call_com(lambda: self._com.activeProjectAboutToChange()))

    def active_project_has_changed(self) -> int:
        """Notify the plugin that the active project has changed.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::activeProjectHasChanged()
        """
        return int(self.call_com(lambda: self._com.activeProjectHasChanged()))

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
        return str(self.call_com(lambda: self._com.onMenuItemSelect(menu_item)))

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
        return str(self.call_com(lambda: self._com.onMenuItemSelectWithParameters(menu_item, parameters)))

    def rhap_plugin_animation_stopped(self) -> int:
        """Notify the plugin that animation has stopped.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhapPluginAnimationStopped()
        """
        return int(self.call_com(lambda: self._com.rhapPluginAnimationStopped()))

    def rhp_plugin_animation_started(self) -> int:
        """Notify the plugin that animation has started.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginAnimationStarted()
        """
        return int(self.call_com(lambda: self._com.rhpPluginAnimationStarted()))

    def rhp_plugin_cleanup(self) -> int:
        """Perform cleanup of the plugin.

        Returns:
            The result of the cleanup operation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginCleanup()
        """
        return int(self.call_com(lambda: self._com.rhpPluginCleanup()))

    def rhp_plugin_do_command(self, the_command: str) -> None:
        """Notify the plugin to execute a command.

        Args:
            the_command: The command to execute.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginDoCommand(java.lang.String theCommand)
        """
        self.call_com(lambda: self._com.rhpPluginDoCommand(the_command))

    def rhp_plugin_final_cleanup(self) -> int:
        """Perform final cleanup of the plugin.

        Returns:
            The result of the final cleanup operation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginFinalCleanup()
        """
        return int(self.call_com(lambda: self._com.rhpPluginFinalCleanup()))

    def rhp_plugin_init(self) -> int:
        """Initialize the plugin.

        Returns:
            The result of the initialization.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginInit()
        """
        return int(self.call_com(lambda: self._com.rhpPluginInit()))

    def rhp_plugin_invoke_item(self) -> int:
        """Invoke an item of the plugin.

        Returns:
            The result of the item invocation.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginInvokeItem()
        """
        return int(self.call_com(lambda: self._com.rhpPluginInvokeItem()))

    def rhp_plugin_on_ide_build_done(self, build_status: str) -> None:
        """Notify the plugin that an IDE build is done.

        Args:
            build_status: The status of the build.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpPluginOnIDEBuildDone(java.lang.String buildStatus)
        """
        self.call_com(lambda: self._com.rhpPluginOnIDEBuildDone(build_status))

    def rhp_plugin_set_application(self, p_r_p_app: "RhapsodyApplication") -> int:
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
        return int(self.call_com(lambda: self._com.rhpPluginSetApplication(p_r_p_app._com)))

    def rhp_saving_project(self) -> int:
        """Notify the plugin that a Rhapsody save is occurring.

        Returns:
            The result of the notification.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPInternalOEMPlugin::rhpSavingProject()
        """
        return int(self.call_com(lambda: self._com.rhpSavingProject()))


class RPJavaPlugins(RPModelElement):
    """Wraps ``IRPJavaPlugins``."""

    # IRPJavaPlugins method parity checklist:
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
    # No deprecated IRPJavaPlugins methods.


class RPPlugInWindow(RPModelElement):
    """Wraps ``IRPPlugInWindow``."""

    # IRPPlugInWindow method parity checklist:
    # [x] destroy_window                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_docking                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_pos_string                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_window_handle              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_docking                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_pos_string                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_title                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] show_window                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
    # No deprecated IRPPlugInWindow methods.

    def destroy_window(self) -> None:
        """Destroy the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::destroyWindow()
        """
        self.call_com(lambda: self._com.destroyWindow())

    def get_docking(self) -> int:
        """Get the docking mode.

        Returns:
            The current docking mode.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getDocking()
        """
        return int(self._get_method_or_property(self._com, "getDocking", "docking"))

    def get_pos_string(self) -> str:
        """Get the position string.

        Returns:
            The position string of the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getPosString()
        """
        return str(self._get_method_or_property(self._com, "getPosString", "posString"))

    def get_window_handle(self) -> int:
        """Get the window handle.

        Returns:
            The window handle.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::getWindowHandle()
        """
        return int(self._get_method_or_property(self._com, "getWindowHandle", "windowHandle"))

    def set_docking(self, n_dock_pos: int) -> None:
        """Set the docking mode.

        Args:
            n_dock_pos: The docking position (0=floating, 1=top, 2=left, 3=right, 4=bottom).

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setDocking(int nDockPos)
        """
        self._set_method_or_property(self._com, "setDocking", "docking", n_dock_pos)

    def set_pos_string(self, s_pos: str) -> None:
        """Set the position string.

        Args:
            s_pos: The position string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setPosString(java.lang.String sPos)
        """
        self._set_method_or_property(self._com, "setPosString", "posString", s_pos)

    def set_title(self, s_title: str) -> None:
        """Set the window title.

        Args:
            s_title: The title to set for the window.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::setTitle(java.lang.String sTitle)
        """
        self._set_method_or_property(self._com, "setTitle", "title", s_title)

    def show_window(self, n_show: int) -> None:
        """Show or hide the window.

        Args:
            n_show: The show/hide flag.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPPlugInWindow::showWindow(int nShow)
        """
        self.call_com(lambda: self._com.showWindow(n_show))


class RPProgressBar(RPModelElement):
    """Wraps ``IRPProgressBar``."""

    # IRPProgressBar method parity checklist:
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
    # [x] reset                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] tick                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # No deprecated IRPProgressBar methods.

    def reset(self) -> None:
        """Reset the progress bar.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPProgressBar::reset()
        """
        self.call_com(lambda: self._com.reset())

    def tick(self, amount: int) -> None:
        """Advance the progress bar by a given amount.

        Args:
            amount: The amount to advance the progress bar.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPProgressBar::tick(int amount)
        """
        self.call_com(lambda: self._com.tick(amount))


class RPSelection(RPModelElement):
    """Wraps ``IRPSelection``: contains methods for cutting, copying, pasting, and deleting graphic elements on diagrams."""

    # IRPSelection method parity checklist:
    # [x] can_copy                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] can_cut                       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] can_delete                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] can_paste                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] copy_selected                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] cut_selected                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] delete_selected               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
    # [x] paste_selected                [x] impl  [x] docstring  [x] unit test  [ ] integration test
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
        return int(self.call_com(lambda: self._com.canCopy()))

    def can_cut(self) -> int:
        """Check whether the current selection can be cut.

        Returns:
            1 if the current selection can be cut, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canCut()
        """
        return int(self.call_com(lambda: self._com.canCut()))

    def can_delete(self) -> int:
        """Check whether the current selection can be deleted.

        Returns:
            1 if the current selection can be deleted, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canDelete()
        """
        return int(self.call_com(lambda: self._com.canDelete()))

    def can_paste(self) -> int:
        """Check whether the item in the clipboard can be pasted to the diagram that has the focus.

        Returns:
            1 if the item in the clipboard can be pasted, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::canPaste()
        """
        return int(self.call_com(lambda: self._com.canPaste()))

    def copy_selected(self) -> int:
        """Copy the currently selected graphic element.

        Returns:
            1 if the copy operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::copySelected()
        """
        return int(self.call_com(lambda: self._com.copySelected()))

    def cut_selected(self) -> int:
        """Cut the currently selected graphic element.

        Returns:
            1 if the cut operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::cutSelected()
        """
        return int(self.call_com(lambda: self._com.cutSelected()))

    def delete_selected(self) -> int:
        """Delete the currently selected graphic element.

        Returns:
            1 if the delete operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::deleteSelected()
        """
        return int(self.call_com(lambda: self._com.deleteSelected()))

    def paste_selected(self) -> int:
        """Paste the item in the clipboard to the diagram that has the focus.

        Returns:
            1 if the paste operation was successful, 0 otherwise.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPSelection::pasteSelected()
        """
        return int(self.call_com(lambda: self._com.pasteSelected()))


class RPowListListener(RPModelElement):
    """Wraps ``IRPowListListener``."""

    # IRPowListListener method parity checklist:
    # [x] dbl_click_notify               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_obj_id                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
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
        self.call_com(lambda: self._com.dblClickNotify(n_row, n_col, s_content))

    def set_obj_id(self, bstr_obj_i_d: str) -> None:
        """Set the object ID.

        Args:
            bstr_obj_i_d: The object ID string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowListListener::setObjID(java.lang.String bstrObjID)
        """
        self._set_method_or_property(self._com, "setObjID", "objID", bstr_obj_i_d)


class RPowPaneMgr(RPModelElement):
    """Wraps ``IRPowPaneMgr``."""

    # IRPowPaneMgr method parity checklist:
    # [x] add_tab_notify                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] close_tab_notify               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_ow_list_listener            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_ow_text_listener            [x] impl  [x] docstring  [x] unit test  [ ] integration test
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
        self.call_com(lambda: self._com.addTabNotify(n_type, n_sub_type, s_obj_i_d, s_title))

    def close_tab_notify(self, s_obj_i_d: str) -> None:
        """Notify when a tab is closed.

        Args:
            s_obj_i_d: The object ID of the tab being closed.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowPaneMgr::closeTabNotify(java.lang.String sObjID)
        """
        self.call_com(lambda: self._com.closeTabNotify(s_obj_i_d))

    def get_ow_list_listener(self, s_obj_i_d: str) -> "RPowListListener":
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
        return RPowListListener(self.call_com(lambda: self._com.getOWListListener(s_obj_i_d)))

    def get_ow_text_listener(self, s_obj_i_d: str) -> "RPowTextListener":
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
        return RPowTextListener(self.call_com(lambda: self._com.getOWTextListener(s_obj_i_d)))


class RPowTextListener(RPModelElement):
    """Wraps ``IRPowTextListener``."""

    # IRPowTextListener method parity checklist:
    # [x] dbl_click_notify               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_obj_id                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name             [x] impl (inherited from RPModelElement)  [x] docstring  [x] unit test  [ ] integration test
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
        self.call_com(lambda: self._com.dblClickNotify(n_line, sz_line))

    def set_obj_id(self, bstr_obj_i_d: str) -> None:
        """Set the object ID.

        Args:
            bstr_obj_i_d: The object ID string to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPowTextListener::setObjID(java.lang.String bstrObjID)
        """
        self._set_method_or_property(self._com, "setObjID", "objID", bstr_obj_i_d)
