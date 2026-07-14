"""Tests for rhapsody_cli.elements.project.RPProject."""

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_project_is_a_package() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPPackage)
    assert project.get_name() == "MyProject"


def test_project_add_package_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    new_pkg = make_fake_element("Package", getName="NewPkg")
    fake.addPackage.return_value = new_pkg
    project = RPProject(fake)

    result = project.add_package("NewPkg")

    fake.addPackage.assert_called_once_with("NewPkg")
    assert result.get_name() == "NewPkg"


def test_project_close_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.close()

    fake.close.assert_called_once_with()


def test_project_become_active_project_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.become_active_project()

    fake.becomeActiveProject.assert_called_once_with()


def test_project_find_component_wraps_result() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Component", getName="Comp1")
    fake.findComponent.return_value = found
    project = RPProject(fake)

    result = project.find_component("Comp1")

    fake.findComponent.assert_called_once_with("Comp1")
    assert result.get_name() == "Comp1"


def test_project_get_packages_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    fake.getPackages.return_value = make_fake_collection([make_fake_element("Package", getName="P1")])
    project = RPProject(fake)

    packages = project.get_packages()

    assert isinstance(packages, RPCollection)
    assert len(packages) == 1
    assert packages[0].get_name() == "P1"


def test_project_is_registered_for_meta_class_project() -> None:
    from rhapsody_cli.models.core import AbstractRPModelElement

    fake = make_fake_element("Project", getName="MyProject")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPProject)


def test_project_add_class_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    cls = make_fake_element("Class", getName="Class1")
    fake.addClass.return_value = cls
    project = RPProject(fake)

    result = project.add_class("Class1")

    fake.addClass.assert_called_once_with("Class1")
    assert result.get_name() == "Class1"


def test_project_add_actor_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    actor = make_fake_element("Actor", getName="Actor1")
    fake.addActor.return_value = actor
    project = RPProject(fake)

    result = project.add_actor("Actor1")

    fake.addActor.assert_called_once_with("Actor1")
    assert result.get_name() == "Actor1"


def test_project_get_components_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    comp1 = make_fake_element("Component", getName="Comp1")
    fake.getComponents.return_value = make_fake_collection([comp1])
    project = RPProject(fake)

    result = project.get_components()

    assert isinstance(result, RPCollection)


def test_project_find_by_name_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findByName.return_value = found
    project = RPProject(fake)

    result = project.find_by_name("MyClass")

    fake.findByName.assert_called_once_with("MyClass")
    assert result.get_name() == "MyClass"


def test_project_find_by_meta_class_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    cls1 = make_fake_element("Class", getName="Class1")
    fake.findByMetaClass.return_value = make_fake_collection([cls1])
    project = RPProject(fake)

    result = project.find_by_meta_class("Class")

    assert isinstance(result, RPCollection)


def test_project_find_element_by_guid_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findElementByGUID.return_value = found
    project = RPProject(fake)

    result = project.find_element_by_guid("12345")

    fake.findElementByGUID.assert_called_once_with("12345")
    assert result.get_name() == "MyClass"


def test_project_is_dirty_returns_int() -> None:
    fake = make_fake_element("Project", getIsDirty=1)
    project = RPProject(fake)

    result = project.get_is_dirty()

    fake.getIsDirty.assert_called_once_with()
    assert result == 1


def test_project_set_dirty_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_dirty(1)

    fake.setDirty.assert_called_once_with(1)


# --- New tests for RPProject ---
def test_project_add_component_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    comp = make_fake_element("Component", getName="Comp1")
    fake.addComponent.return_value = comp
    project = RPProject(fake)

    result = project.add_component("Comp1")

    fake.addComponent.assert_called_once_with("Comp1")
    assert result.get_name() == "Comp1"


def test_project_delete_component_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPUnit

    fake = make_fake_element("Project")
    project = RPProject(fake)
    comp_fake = make_fake_element("Component", getName="ToDelete")

    project.delete_component(RPUnit(comp_fake))

    fake.deleteComponent.assert_called_once_with(comp_fake)


def test_project_add_node_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.addNode.return_value = node
    project = RPProject(fake)

    result = project.add_node("Node1")

    fake.addNode.assert_called_once_with("Node1")
    assert result.get_name() == "Node1"


def test_project_get_nodes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.getNodes.return_value = make_fake_collection([node])
    project = RPProject(fake)

    result = project.get_nodes()

    assert isinstance(result, RPCollection)


def test_project_find_node_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.findNode.return_value = node
    project = RPProject(fake)

    result = project.find_node("Node1")

    fake.findNode.assert_called_once_with("Node1")
    assert result.get_name() == "Node1"


def test_project_add_configuration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.addConfiguration.return_value = config
    project = RPProject(fake)

    result = project.add_configuration("Default")

    fake.addConfiguration.assert_called_once_with("Default")
    assert result.get_name() == "Default"


def test_project_get_configurations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.getConfigurations.return_value = make_fake_collection([config])
    project = RPProject(fake)

    result = project.get_configurations()

    assert isinstance(result, RPCollection)


def test_project_find_configuration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.findConfiguration.return_value = config
    project = RPProject(fake)

    result = project.find_configuration("Default")

    fake.findConfiguration.assert_called_once_with("Default")
    assert result.get_name() == "Default"


def test_project_add_collaboration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    collab = make_fake_element("Collaboration", getName="Collab1")
    fake.addCollaboration.return_value = collab
    project = RPProject(fake)

    result = project.add_collaboration("Collab1")

    fake.addCollaboration.assert_called_once_with("Collab1")
    assert result.get_name() == "Collab1"


def test_project_get_collaborations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    collab = make_fake_element("Collaboration", getName="Collab1")
    fake.getCollaborations.return_value = make_fake_collection([collab])
    project = RPProject(fake)

    result = project.get_collaborations()

    assert isinstance(result, RPCollection)


def test_project_get_all_stereotypes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    st = make_fake_element("Stereotype", getName="MyStereotype")
    fake.getAllStereotypes.return_value = make_fake_collection([st])
    project = RPProject(fake)

    result = project.get_all_stereotypes()

    assert isinstance(result, RPCollection)


def test_project_save_as_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.save_as("C:/path/to/project.rpy")

    fake.saveAs.assert_called_once_with("C:/path/to/project.rpy")


def test_project_find_element_by_binary_id_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findElementByBinaryID.return_value = found
    project = RPProject(fake)

    result = project.find_element_by_binary_id("abc123")

    fake.findElementByBinaryID.assert_called_once_with("abc123")
    assert result.get_name() == "MyClass"


# --- Task 6: Gateway/Report methods ---
def test_project_gateway_export_to_xml_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.gateway_export_to_xml("C:/out.xml")

    fake.gatewayExportToXML.assert_called_once_with("C:/out.xml")


def test_project_gateway_export_to_xml2_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.gateway_export_to_xml2("C:/out.xml", "-verbose")

    fake.gatewayExportToXML2.assert_called_once_with("C:/out.xml", "-verbose")


def test_project_generate_report_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.generate_report("C:/tmpl.tpl", "C:/report.html")

    fake.generateReport.assert_called_once_with("C:/tmpl.tpl", "C:/report.html")


# --- Task 7: Custom Views methods ---
def test_project_add_custom_view_on_browser_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    view_fake = make_fake_element("CustomView", getName="V1")

    project.add_custom_view_on_browser(RPModelElement(view_fake))

    fake.addCustomViewOnBrowser.assert_called_once_with(view_fake)


def test_project_add_custom_view_on_diagram_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    view_fake = make_fake_element("CustomView", getName="V1")

    project.add_custom_view_on_diagram(RPModelElement(view_fake))

    fake.addCustomViewOnDiagram.assert_called_once_with(view_fake)


def test_project_apply_browser_custom_views_on_diagrams_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.apply_browser_custom_views_on_diagrams()

    fake.applyBrowserCustomViewsOnDiagrams.assert_called_once_with()


def test_project_get_active_custom_views_on_browser_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    view = make_fake_element("CustomView", getName="V1")
    fake.getActiveCustomViewsOnBrowser.return_value = make_fake_collection([view])
    project = RPProject(fake)

    result = project.get_active_custom_views_on_browser()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "V1"


def test_project_get_active_custom_views_on_diagram_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    view = make_fake_element("CustomView", getName="V1")
    fake.getActiveCustomViewsOnDiagram.return_value = make_fake_collection([view])
    project = RPProject(fake)

    result = project.get_active_custom_views_on_diagram()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "V1"


def test_project_remove_custom_view_on_browser_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    view_fake = make_fake_element("CustomView", getName="V1")

    project.remove_custom_view_on_browser(RPModelElement(view_fake))

    fake.removeCustomViewOnBrowser.assert_called_once_with(view_fake)


def test_project_remove_custom_view_on_diagram_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    view_fake = make_fake_element("CustomView", getName="V1")

    project.remove_custom_view_on_diagram(RPModelElement(view_fake))

    fake.removeCustomViewOnDiagram.assert_called_once_with(view_fake)


# --- Task 8: CSV methods ---
def test_project_close_csv_file_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.close_csv_file()

    fake.closeCSVFile.assert_called_once_with()


def test_project_open_csv_file_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.open_csv_file("C:/data.csv", 1)

    fake.openCSVFile.assert_called_once_with("C:/data.csv", 1)


def test_project_reload_csv_file_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.reload_csv_file()

    fake.reloadCSVFile.assert_called_once_with()


# --- Task 9: Remote/Roundtrip methods ---
def test_project_apply_roundtrip_diff_merge_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.apply_roundtrip_diff_merge()

    fake.applyRoundtripDiffMerge.assert_called_once_with()


def test_project_enable_rhapsody_model_manager_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.enable_rhapsody_model_manager(1)

    fake.enableRhapsodyModelManager.assert_called_once_with(1)


def test_project_find_elements_with_oslc_link_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    elem = make_fake_element("Class", getName="C1")
    fake.findElementsWithOSLCLink.return_value = make_fake_collection([elem])
    project = RPProject(fake)

    result = project.find_elements_with_oslc_link("http://example.com/link")

    fake.findElementsWithOSLCLink.assert_called_once_with("http://example.com/link")
    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "C1"


def test_project_get_remote_resource_packages_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    pkg = make_fake_element("Package", getName="RemotePkg")
    fake.getRemoteResourcePackages.return_value = make_fake_collection([pkg])
    project = RPProject(fake)

    result = project.get_remote_resource_packages()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "RemotePkg"


def test_project_get_roundtrip_shadow_model_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    shadow = make_fake_element("Model", getName="ShadowModel")
    fake.getRoundtripShadowModel.return_value = shadow
    project = RPProject(fake)

    result = project.get_roundtrip_shadow_model()

    fake.getRoundtripShadowModel.assert_called_once_with()
    assert result.get_name() == "ShadowModel"


def test_project_is_actively_managed_returns_int() -> None:
    fake = make_fake_element("Project", isActivelyManaged=1)
    project = RPProject(fake)

    result = project.is_actively_managed()

    fake.isActivelyManaged.assert_called_once_with()
    assert result == 1


def test_project_migrate_design_manager_links_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.migrate_design_manager_links()

    fake.migrateDesignManagerLinks.assert_called_once_with()


# --- Task 10: Rose Import methods ---
def test_project_import_package_from_rose_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    pkg = make_fake_element("Package", getName="RosePkg")
    fake.importPackageFromRose.return_value = pkg
    project = RPProject(fake)

    result = project.import_package_from_rose("C:/rose.mdl")

    fake.importPackageFromRose.assert_called_once_with("C:/rose.mdl")
    assert result.get_name() == "RosePkg"


def test_project_import_project_from_rose_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.import_project_from_rose("C:/rose.mdl")

    fake.importProjectFromRose.assert_called_once_with("C:/rose.mdl")


# --- Task 11: Events methods ---
def test_project_check_events_base_ids_solve_collisions_returns_int() -> None:
    fake = make_fake_element("Project", checkEventsBaseIdsSolveCollisions=2)
    project = RPProject(fake)

    result = project.check_events_base_ids_solve_collisions()

    fake.checkEventsBaseIdsSolveCollisions.assert_called_once_with()
    assert result == 2


def test_project_recalculate_events_base_ids_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.recalculate_events_base_ids()

    fake.recalculateEventsBaseIds.assert_called_once_with()


# --- Task 12: Misc methods ---
def test_project_add_spell_checker_result_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.add_spell_checker_result("misspel", "misspelled")

    fake.addSpellCheckerResult.assert_called_once_with("misspel", "misspelled")


def test_project_clean_unresolved_elements_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.clean_unresolved_elements()

    fake.cleanUnresolvedElements.assert_called_once_with()


def test_project_end_transaction_of_no_cg_interest_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.end_transaction_of_no_cg_interest()

    fake.endTransactionOfNoCGInterest.assert_called_once_with()


def test_project_get_default_directory_scheme_returns_int() -> None:
    fake = make_fake_element("Project", getDefaultDirectoryScheme=1)
    project = RPProject(fake)

    result = project.get_default_directory_scheme()

    fake.getDefaultDirectoryScheme.assert_called_once_with()
    assert result == 1


def test_project_get_new_progress_bar_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    bar = make_fake_element("ProgressBar", getName="PB1")
    fake.getNewProgressBar.return_value = bar
    project = RPProject(fake)

    result = project.get_new_progress_bar()

    fake.getNewProgressBar.assert_called_once_with()
    assert result.get_name() == "PB1"


def test_project_get_notify_plugin_on_elements_changed_returns_int() -> None:
    fake = make_fake_element("Project", getNotifyPluginOnElementsChanged=1)
    project = RPProject(fake)

    result = project.get_notify_plugin_on_elements_changed()

    fake.getNotifyPluginOnElementsChanged.assert_called_once_with()
    assert result == 1


def test_project_get_requirements_by_id_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    req = make_fake_element("Requirement", getName="Req1")
    fake.getRequirementsByID.return_value = make_fake_collection([req])
    project = RPProject(fake)

    result = project.get_requirements_by_id("REQ-001")

    fake.getRequirementsByID.assert_called_once_with("REQ-001")
    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "Req1"


def test_project_remove_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.remove()

    fake.remove.assert_called_once_with()


def test_project_save_as_prev_version_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.save_as_prev_version("C:/old.rpy")

    fake.saveAsPrevVersion.assert_called_once_with("C:/old.rpy")


def test_project_set_default_directory_scheme_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_default_directory_scheme(2)

    fake.setDefaultDirectoryScheme.assert_called_once_with(2)


def test_project_set_global_configuration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_global_configuration("MyConfig")

    fake.setGlobalConfiguration.assert_called_once_with("MyConfig")


def test_project_set_notify_plugin_on_elements_changed_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_notify_plugin_on_elements_changed(1)

    fake.setNotifyPluginOnElementsChanged.assert_called_once_with(1)


def test_project_set_object_explicit_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    obj_fake = make_fake_element("Class", getName="Obj1")

    project.set_object_explicit(RPModelElement(obj_fake))

    fake.setObjectExplicit.assert_called_once_with(obj_fake)


def test_project_set_object_implicit_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPModelElement

    fake = make_fake_element("Project")
    project = RPProject(fake)
    obj_fake = make_fake_element("Class", getName="Obj1")

    project.set_object_implicit(RPModelElement(obj_fake))

    fake.setObjectImplicit.assert_called_once_with(obj_fake)


def test_project_set_use_unique_stereotype_and_ref_cache_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_use_unique_stereotype_and_ref_cache(1)

    fake.setUseUniqueStereotypeAndRefCache.assert_called_once_with(1)


def test_project_set_wait_dialog_watchdog_value_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_wait_dialog_watchdog_value(5000)

    fake.setWaitDialogWatchdogValue.assert_called_once_with(5000)


def test_project_start_transaction_of_no_cg_interest_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.start_transaction_of_no_cg_interest()

    fake.startTransactionOfNoCGInterest.assert_called_once_with()
