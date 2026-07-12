from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.support.model_ide import (
    RPAXViewCtrl,
    RPExternalIDERegistry,
    RPInternalOEMPlugin,
    RPowListListener,
    RPowPaneMgr,
    RPowTextListener,
    RPPlugInWindow,
    RPProgressBar,
    RPSelection,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_RPAXViewCtrl_do_command_delegates_to_com():
    fake = make_fake_element("AXViewCtrl")
    obj = RPAXViewCtrl(fake)
    obj.do_command(1)
    fake.doCommand.assert_called_once_with(1)


def test_RPAXViewCtrl_execute_command_delegates_to_com():
    fake = make_fake_element("AXViewCtrl")
    coll = RPCollection(make_fake_collection([make_fake_element("X")]))
    obj = RPAXViewCtrl(fake)
    obj.execute_command("x", coll, coll)
    fake.executeCommand.assert_called_once_with("x", coll._com, coll._com)


def test_RPExternalIDERegistry_progress_task_asynch_callback_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.progress_task_asynch_callback(1, 1)
    fake.progressTaskAsynchCallback.assert_called_once_with(1, 1)


def test_RPExternalIDERegistry_progress_task_asynch_eliminate_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.progress_task_asynch_eliminate(1, 1)
    fake.progressTaskAsynchEliminate.assert_called_once_with(1, 1)


def test_RPExternalIDERegistry_send_i_d_e_text_message_delegates_to_com():
    fake = make_fake_element("ExternalIDERegistry")
    obj = RPExternalIDERegistry(fake)
    obj.send_i_d_e_text_message("x")
    fake.sendIDETextMessage.assert_called_once_with("x")


def test_RPInternalOEMPlugin_active_project_about_to_change_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.activeProjectAboutToChange.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.active_project_about_to_change()
    fake.activeProjectAboutToChange.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_active_project_has_changed_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.activeProjectHasChanged.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.active_project_has_changed()
    fake.activeProjectHasChanged.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_on_menu_item_select_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.onMenuItemSelect.return_value = "value"
    obj = RPInternalOEMPlugin(fake)
    result = obj.on_menu_item_select("x")
    fake.onMenuItemSelect.assert_called_once_with("x")
    assert result == "value"


def test_RPInternalOEMPlugin_on_menu_item_select_with_parameters_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.onMenuItemSelectWithParameters.return_value = "value"
    obj = RPInternalOEMPlugin(fake)
    result = obj.on_menu_item_select_with_parameters("x", "x")
    fake.onMenuItemSelectWithParameters.assert_called_once_with("x", "x")
    assert result == "value"


def test_RPInternalOEMPlugin_rhap_plugin_animation_stopped_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhapPluginAnimationStopped.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhap_plugin_animation_stopped()
    fake.rhapPluginAnimationStopped.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_animation_started_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginAnimationStarted.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_animation_started()
    fake.rhpPluginAnimationStarted.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_cleanup_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginCleanup.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_cleanup()
    fake.rhpPluginCleanup.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_do_command_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    obj = RPInternalOEMPlugin(fake)
    obj.rhp_plugin_do_command("x")
    fake.rhpPluginDoCommand.assert_called_once_with("x")


def test_RPInternalOEMPlugin_rhp_plugin_final_cleanup_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginFinalCleanup.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_final_cleanup()
    fake.rhpPluginFinalCleanup.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_init_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginInit.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_init()
    fake.rhpPluginInit.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_invoke_item_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpPluginInvokeItem.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_invoke_item()
    fake.rhpPluginInvokeItem.assert_called_once_with()
    assert result == 1


def test_RPInternalOEMPlugin_rhp_plugin_on_i_d_e_build_done_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    obj = RPInternalOEMPlugin(fake)
    obj.rhp_plugin_on_i_d_e_build_done("x")
    fake.rhpPluginOnIDEBuildDone.assert_called_once_with("x")


def test_RPInternalOEMPlugin_rhp_plugin_set_application_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    target = make_fake_element("X")
    fake.rhpPluginSetApplication.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_plugin_set_application(AbstractRPModelElement.wrap(target))
    fake.rhpPluginSetApplication.assert_called_once_with(target)
    assert result == 1


def test_RPInternalOEMPlugin_rhp_saving_project_delegates_to_com():
    fake = make_fake_element("InternalOEMPlugin")
    fake.rhpSavingProject.return_value = 1
    obj = RPInternalOEMPlugin(fake)
    result = obj.rhp_saving_project()
    fake.rhpSavingProject.assert_called_once_with()
    assert result == 1


def test_RPPlugInWindow_destroy_window_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.destroy_window()
    fake.destroyWindow.assert_called_once_with()


def test_RPPlugInWindow_get_docking_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getDocking.return_value = 1
    obj = RPPlugInWindow(fake)
    assert obj.get_docking() == 1


def test_RPPlugInWindow_get_pos_string_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getPosString.return_value = "value"
    obj = RPPlugInWindow(fake)
    assert obj.get_pos_string() == "value"


def test_RPPlugInWindow_get_window_handle_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    fake.getWindowHandle.return_value = 1
    obj = RPPlugInWindow(fake)
    assert obj.get_window_handle() == 1


def test_RPPlugInWindow_set_docking_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_docking(1)
    fake.setDocking.assert_called_once_with(1)


def test_RPPlugInWindow_set_pos_string_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_pos_string("file.txt")
    fake.setPosString.assert_called_once_with("file.txt")


def test_RPPlugInWindow_set_title_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.set_title("file.txt")
    fake.setTitle.assert_called_once_with("file.txt")


def test_RPPlugInWindow_show_window_delegates_to_com():
    fake = make_fake_element("PlugInWindow")
    obj = RPPlugInWindow(fake)
    obj.show_window(1)
    fake.showWindow.assert_called_once_with(1)


def test_RPProgressBar_reset_delegates_to_com():
    fake = make_fake_element("ProgressBar")
    obj = RPProgressBar(fake)
    obj.reset()
    fake.reset.assert_called_once_with()


def test_RPProgressBar_tick_delegates_to_com():
    fake = make_fake_element("ProgressBar")
    obj = RPProgressBar(fake)
    obj.tick(1)
    fake.tick.assert_called_once_with(1)


def test_RPSelection_can_copy_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canCopy.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_copy()
    fake.canCopy.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_cut_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canCut.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_cut()
    fake.canCut.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_delete_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canDelete.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_delete()
    fake.canDelete.assert_called_once_with()
    assert result == 1


def test_RPSelection_can_paste_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.canPaste.return_value = 1
    obj = RPSelection(fake)
    result = obj.can_paste()
    fake.canPaste.assert_called_once_with()
    assert result == 1


def test_RPSelection_copy_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.copySelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.copy_selected()
    fake.copySelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_cut_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.cutSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.cut_selected()
    fake.cutSelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_delete_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.deleteSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.delete_selected()
    fake.deleteSelected.assert_called_once_with()
    assert result == 1


def test_RPSelection_paste_selected_delegates_to_com():
    fake = make_fake_element("Selection")
    fake.pasteSelected.return_value = 1
    obj = RPSelection(fake)
    result = obj.paste_selected()
    fake.pasteSelected.assert_called_once_with()
    assert result == 1


def test_RPowListListener_dbl_click_notify_delegates_to_com():
    fake = make_fake_element("owListListener")
    obj = RPowListListener(fake)
    obj.dbl_click_notify(1, 1, "x")
    fake.dblClickNotify.assert_called_once_with(1, 1, "x")


def test_RPowListListener_set_obj_i_d_delegates_to_com():
    fake = make_fake_element("owListListener")
    obj = RPowListListener(fake)
    obj.set_obj_i_d("file.txt")
    fake.setObjID.assert_called_once_with("file.txt")


def test_RPowPaneMgr_add_tab_notify_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    obj = RPowPaneMgr(fake)
    obj.add_tab_notify(1, 1, "x", "x")
    fake.addTabNotify.assert_called_once_with(1, 1, "x", "x")


def test_RPowPaneMgr_close_tab_notify_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    obj = RPowPaneMgr(fake)
    obj.close_tab_notify("x")
    fake.closeTabNotify.assert_called_once_with("x")


def test_RPowPaneMgr_get_o_w_list_listener_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    inner = make_fake_element("X", getName="y")
    fake.getOWListListener.return_value = inner
    obj = RPowPaneMgr(fake)
    result = obj.get_o_w_list_listener("x")
    assert isinstance(result, RPowListListener)


def test_RPowPaneMgr_get_o_w_text_listener_delegates_to_com():
    fake = make_fake_element("owPaneMgr")
    inner = make_fake_element("X", getName="y")
    fake.getOWTextListener.return_value = inner
    obj = RPowPaneMgr(fake)
    result = obj.get_o_w_text_listener("x")
    assert isinstance(result, RPowTextListener)


def test_RPowTextListener_dbl_click_notify_delegates_to_com():
    fake = make_fake_element("owTextListener")
    obj = RPowTextListener(fake)
    obj.dbl_click_notify(1, "x")
    fake.dblClickNotify.assert_called_once_with(1, "x")


def test_RPowTextListener_set_obj_i_d_delegates_to_com():
    fake = make_fake_element("owTextListener")
    obj = RPowTextListener(fake)
    obj.set_obj_i_d("file.txt")
    fake.setObjID.assert_called_once_with("file.txt")
