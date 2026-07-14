"""Wraps ``com.telelogic.rhapsody.core.IRPProject``."""

from typing import TYPE_CHECKING, Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment.model_package import RPPackage

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_actor import RPActor
    from rhapsody_cli.models.elements.classifiers.model_class import RPClass
    from rhapsody_cli.models.elements.containment.model_collaboration import RPCollaboration
    from rhapsody_cli.models.elements.containment.model_component import RPComponent
    from rhapsody_cli.models.elements.containment.model_configuration import RPConfiguration
    from rhapsody_cli.models.elements.containment.model_node import RPNode
    from rhapsody_cli.models.support.model_ide import RPProgressBar


class RPProject(RPPackage):
    """Wraps ``IRPProject``: represents the top-level project container."""

    # IRPProject method parity checklist:
    # [x] gatewayExportToXML  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] gatewayExportToXML2  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] generateReport  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] addComponent  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] addCustomViewOnBrowser  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] addCustomViewOnDiagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_package  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [ ] addProfile  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] addSpellCheckerResult  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] allowAutoSave  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] allowNonUniqueNames  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] applyBrowserCustomViewsOnDiagrams  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] applyRoundtripDiffMerge  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] become_active_project  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] checkEventsBaseIdsSolveCollisions  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] cleanUnresolvedElements  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] close  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] closeCSVFile  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] deleteComponent  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] enableRhapsodyModelManager  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] endTransactionOfNoCGInterest  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_component  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] findElementByBinaryID  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] findElementByFileName  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] find_element_by_guid  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] findElementsWithOSLCLink  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] getActiveComponent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] getActiveConfiguration  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getActiveCustomViewsOnBrowser  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getActiveCustomViewsOnDiagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getAllStereotypes  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] getCgSimplifiedModelPackage  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] getCodeGeneratedFiles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_components  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getDefaultDirectoryScheme  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] getNewCollaboration  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getNewProgressBar  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getNotifyPluginOnElementsChanged  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] getProfiles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getRemoteResourcePackages  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getRequirementsByID  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] getRoundtripShadowModel  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] highlightFromCode  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] importPackageFromRose  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] importProjectFromRose  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] isActivelyManaged  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] isModifiedRecursive  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] locateInIDE  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] migrateDesignManagerLinks  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [deprecated] moveToDesignManager  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] moveToDesignManagerAfterLogin  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [x] openCSVFile  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] recalculateEventsBaseIds  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] reloadCSVFile  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] removeCustomViewOnBrowser  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] removeCustomViewOnDiagram  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] save  [x] impl  [x] docstring  [ ] unit test  [ ] integration test   (inherited from RPUnit)
    # [x] saveAs  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] saveAsPrevVersion  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] setActiveComponent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] setActiveConfiguration  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setDefaultDirectoryScheme  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setGlobalConfiguration  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setNotifyPluginOnElementsChanged  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setObjectExplicit  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setObjectImplicit  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setUseUniqueStereotypeAndRefCache  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setWaitDialogWatchdogValue  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] startTransactionOfNoCGInterest  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] IRPPackage / IRPUnit / IRPModelElement methods (covered by RPPackage / RPUnit / RPModelElement checklists)
    # Deprecated IRPProject methods listed above.

    def add_package(self, name: str) -> "RPPackage":
        """Adds a new package to the project.

        Args:
            name: The name of the new package.

        Returns:
            The wrapped ``IRPPackage`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addPackage(java.lang.String name)
        """
        return cast("RPPackage", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addPackage(name))))

    def close(self) -> None:
        """Closes the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::close()
        """
        AbstractRPModelElement.call_com(lambda: self._com.close())

    def become_active_project(self) -> None:
        """Makes this project the active project in Rhapsody.

        Used when you have multiple projects open in Rhapsody.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::becomeActiveProject()
        """
        AbstractRPModelElement.call_com(lambda: self._com.becomeActiveProject())

    def find_component(self, name: str) -> "RPComponent":
        """Finds a component in the project by name.

        Args:
            name: The name of the component to find.

        Returns:
            The wrapped component element if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findComponent(java.lang.String name)
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findComponent(name))))

    def get_packages(self) -> RPCollection:
        """Returns all top-level packages in the project.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::getPackages()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPackages", "packages"))

    def get_root(self) -> "RPProject":
        """Returns the root project element.

        Returns:
            The project itself, which acts as the root container.
        """
        return self

    def add_class(self, name: str) -> "RPClass":
        """Adds a new class to the project's top level.

        Args:
            name: The name of the new class.

        Returns:
            The wrapped ``IRPClass`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addClass(java.lang.String name)
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name))))

    def add_actor(self, name: str) -> "RPActor":
        """Adds a new actor to the project's top level.

        Args:
            name: The name of the new actor.

        Returns:
            The wrapped ``IRPActor`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPPackage::addActor(java.lang.String name)
        """
        return cast("RPActor", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActor(name))))

    def get_components(self) -> RPCollection:
        """Returns all components in the project.

        Returns:
            An ``RPCollection`` of component elements.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getComponents()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getComponents", "components"))

    def find_by_name(self, name: str) -> Any:
        """Finds an element in the project by name.

        Args:
            name: The name of the element to find.

        Returns:
            The wrapped element if found.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findByName(name)))

    def find_by_meta_class(self, meta_class: str) -> RPCollection:
        """Finds all elements in the project with a given metaclass.

        Args:
            meta_class: The metaclass name to search for.

        Returns:
            An ``RPCollection`` of matching elements.
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.findByMetaClass(meta_class)))

    def find_element_by_guid(self, guid: str) -> "RPModelElement":
        """Finds an element in the project by GUID.

        Args:
            guid: The GUID of the element to find.

        Returns:
            The wrapped element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findElementByGUID(java.lang.String theGUID)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findElementByGUID(guid)))

    def get_is_dirty(self) -> int:
        """Checks whether the project has unsaved changes.

        Returns:
            ``1`` if the project is dirty (has unsaved changes), ``0`` otherwise.
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsDirty", "isDirty"))

    def set_dirty(self, is_dirty: int) -> None:
        """Sets the dirty flag of the project.

        Args:
            is_dirty: ``1`` to mark as dirty, ``0`` to mark as clean.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDirty", "dirty", is_dirty)

    # --- Component methods ---
    def add_component(self, name: str) -> "RPComponent":
        """Adds a new component to the project.

        Args:
            name: The name of the new component.

        Returns:
            The wrapped ``IRPComponent`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addComponent(java.lang.String name)
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addComponent(name))))

    def delete_component(self, component: Any) -> None:
        """Deletes a component from the project.

        Args:
            component: The component to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::deleteComponent(com.telelogic.rhapsody.core.IRPComponent component)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteComponent(component._com))

    # --- Node methods ---
    def add_node(self, name: str) -> "RPNode":
        """Adds a new node to the project.

        Args:
            name: The name of the new node.

        Returns:
            The wrapped ``IRPNode`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addNode(java.lang.String name)
        """
        return cast("RPNode", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNode(name))))

    def get_nodes(self) -> "RPCollection":
        """Returns all nodes in the project.

        Returns:
            An ``RPCollection`` of ``IRPNode`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getNodes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNodes", "nodes"))

    def find_node(self, name: str) -> "RPNode":
        """Finds a node in the project by name.

        Args:
            name: The name of the node to find.

        Returns:
            The wrapped ``IRPNode`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findNode(java.lang.String name)
        """
        return cast("RPNode", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNode(name))))

    def delete_node(self, node: Any) -> None:
        """Deletes a node from the project.

        Args:
            node: The node to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::deleteNode(com.telelogic.rhapsody.core.IRPNode node)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteNode(node._com))

    # --- Configuration methods ---
    def add_configuration(self, name: str) -> "RPConfiguration":
        """Adds a new configuration to the project.

        Args:
            name: The name of the new configuration.

        Returns:
            The wrapped ``IRPConfiguration`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addConfiguration(java.lang.String name)
        """
        return cast("RPConfiguration", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addConfiguration(name))))

    def get_configurations(self) -> "RPCollection":
        """Returns all configurations in the project.

        Returns:
            An ``RPCollection`` of ``IRPConfiguration`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getConfigurations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getConfigurations", "configurations"))

    def find_configuration(self, name: str) -> "RPConfiguration":
        """Finds a configuration in the project by name.

        Args:
            name: The name of the configuration to find.

        Returns:
            The wrapped ``IRPConfiguration`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findConfiguration(java.lang.String name)
        """
        return cast("RPConfiguration", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findConfiguration(name))))

    def delete_configuration(self, config: Any) -> None:
        """Deletes a configuration from the project.

        Args:
            config: The configuration to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::deleteConfiguration(com.telelogic.rhapsody.core.IRPConfiguration config)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteConfiguration(config._com))

    def get_active_configuration(self) -> "RPConfiguration":
        """Returns the active configuration of the project.

        Returns:
            The wrapped ``IRPConfiguration`` that is currently active.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getActiveConfiguration()
        """
        return cast("RPConfiguration", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getActiveConfiguration", "activeConfiguration")))

    def set_active_configuration(self, config: Any) -> None:
        """Sets the active configuration of the project.

        Args:
            config: The configuration to set as active.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setActiveConfiguration(com.telelogic.rhapsody.core.IRPConfiguration config)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setActiveConfiguration(config._com))

    def get_active_component(self) -> "RPComponent":
        """Returns the active component of the project.

        Returns:
            The wrapped ``IRPComponent`` that is currently active.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getActiveComponent()
        """
        return cast("RPComponent", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getActiveComponent", "activeComponent")))

    def set_active_component(self, component: Any) -> None:
        """Sets the active component of the project.

        Args:
            component: The component to set as active.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setActiveComponent(com.telelogic.rhapsody.core.IRPComponent component)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setActiveComponent(component._com))

    # --- Collaboration methods ---
    def add_collaboration(self, name: str) -> "RPCollaboration":
        """Adds a new collaboration to the project.

        Args:
            name: The name of the new collaboration.

        Returns:
            The wrapped ``IRPCollaboration`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addCollaboration(java.lang.String name)
        """
        return cast("RPCollaboration", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addCollaboration(name))))

    def get_collaborations(self) -> "RPCollection":
        """Returns all collaborations in the project.

        Returns:
            An ``RPCollection`` of ``IRPCollaboration`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getCollaborations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCollaborations", "collaborations"))

    def find_collaboration(self, name: str) -> "RPCollaboration":
        """Finds a collaboration in the project by name.

        Args:
            name: The name of the collaboration to find.

        Returns:
            The wrapped ``IRPCollaboration`` if found, otherwise empty wrapper.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findCollaboration(java.lang.String name)
        """
        return cast("RPCollaboration", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findCollaboration(name))))

    def delete_collaboration(self, collab: Any) -> None:
        """Deletes a collaboration from the project.

        Args:
            collab: The collaboration to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::deleteCollaboration(com.telelogic.rhapsody.core.IRPCollaboration collab)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteCollaboration(collab._com))

    # --- Stereotype methods ---
    def get_all_stereotypes(self) -> "RPCollection":
        """Returns all stereotypes in the project.

        Returns:
            An ``RPCollection`` of ``IRPStereotype`` objects.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getAllStereotypes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAllStereotypes", "allStereotypes"))

    def get_new_collaboration(self) -> "RPCollaboration":
        """Returns a new collaboration object.

        Returns:
            The wrapped ``IRPCollaboration`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getNewCollaboration()
        """
        return cast("RPCollaboration", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getNewCollaboration", "newCollaboration")))

    # --- Profile methods ---
    def add_profile(self, name: str) -> Any:
        """Adds a new profile to the project.

        Args:
            name: The name of the new profile.

        Returns:
            The wrapped profile element created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addProfile(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addProfile(name)))

    def get_profiles(self) -> "RPCollection":
        """Returns all profiles in the project.

        Returns:
            An ``RPCollection`` of profile elements.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getProfiles()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getProfiles", "profiles"))

    # --- Save methods ---
    def save_as(self, file_path: str) -> None:
        """Saves the project to a new file path.

        Args:
            file_path: The path to save the project to.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::saveAs(java.lang.String filePath)
        """
        AbstractRPModelElement.call_com(lambda: self._com.saveAs(file_path))

    # --- Find by binary ID ---
    def find_element_by_binary_id(self, binary_id: str) -> "RPModelElement":
        """Finds an element in the project by binary ID.

        Args:
            binary_id: The binary ID of the element to find.

        Returns:
            The wrapped element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findElementByBinaryID(java.lang.String binaryID)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findElementByBinaryID(binary_id)))

    def find_element_by_file_name(self, file_name: str) -> "RPModelElement":
        """Finds an element in the project by file name.

        Args:
            file_name: The file name to search for.

        Returns:
            The wrapped element if found.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findElementByFileName(java.lang.String fileName)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findElementByFileName(file_name)))

    # --- Code generation methods ---
    def get_code_generated_files(self) -> "RPCollection":
        """Returns all code-generated files in the project.

        Returns:
            An ``RPCollection`` of file elements.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getCodeGeneratedFiles()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getCodeGeneratedFiles", "codeGeneratedFiles"))

    # --- Other methods ---
    def allow_auto_save(self, allow: int) -> None:
        """Sets whether auto-save is allowed for the project.

        Args:
            allow: ``1`` to allow auto-save, ``0`` to disallow.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::allowAutoSave(int allow)
        """
        AbstractRPModelElement.call_com(lambda: self._com.allowAutoSave(allow))

    def allow_non_unique_names(self, allow: int) -> None:
        """Sets whether non-unique names are allowed for elements.

        Args:
            allow: ``1`` to allow non-unique names, ``0`` to disallow.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::allowNonUniqueNames(int allow)
        """
        AbstractRPModelElement.call_com(lambda: self._com.allowNonUniqueNames(allow))

    def get_cg_simplified_model_package(self) -> "RPPackage":
        """Returns the code generation simplified model package.

        Returns:
            The wrapped ``IRPPackage`` for the simplified model.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getCgSimplifiedModelPackage()
        """
        return cast("RPPackage", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getCgSimplifiedModelPackage", "cgSimplifiedModelPackage")))

    def locate_in_ide(self) -> None:
        """Locates this project in the Rhapsody IDE.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::locateInIDE()
        """
        AbstractRPModelElement.call_com(lambda: self._com.locateInIDE())

    def is_modified_recursive(self) -> bool:
        """Checks whether the project or any of its contents have unsaved changes.

        Returns:
            ``True`` if modified, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::isModifiedRecursive()
        """
        return bool(AbstractRPModelElement.call_com(lambda: self._com.isModifiedRecursive()))

    def highlight_from_code(self, file_path: str, line_number: int) -> None:
        """Highlights the element in Rhapsody based on code location.

        Args:
            file_path: The path of the source file.
            line_number: The line number in the source file.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::highlightFromCode(java.lang.String filePath, int lineNumber)
        """
        AbstractRPModelElement.call_com(lambda: self._com.highlightFromCode(file_path, line_number))

    # --- Gateway/Report methods ---
    def gateway_export_to_xml(self, file_path: str) -> None:
        """Exports the project to an XML file using the Gateway tool.

        Args:
            file_path: The path of the XML file to create.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::gatewayExportToXML(java.lang.String filePath)
        """
        AbstractRPModelElement.call_com(lambda: self._com.gatewayExportToXML(file_path))

    def gateway_export_to_xml2(self, file_path: str, options: str) -> None:
        """Exports the project to an XML file using the Gateway tool with options.

        Args:
            file_path: The path of the XML file to create.
            options: The options string to pass to the Gateway tool.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::gatewayExportToXML2(java.lang.String filePath, java.lang.String options)
        """
        AbstractRPModelElement.call_com(lambda: self._com.gatewayExportToXML2(file_path, options))

    def generate_report(self, template_path: str, output_path: str) -> None:
        """Generates a report from the project using the specified template.

        Args:
            template_path: The path of the report template file.
            output_path: The path of the output report file to create.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::generateReport(java.lang.String templatePath, java.lang.String outputPath)
        """
        AbstractRPModelElement.call_com(lambda: self._com.generateReport(template_path, output_path))

    # --- Custom Views methods ---
    def add_custom_view_on_browser(self, view: Any) -> None:
        """Adds a custom view to be applied on the Rhapsody browser.

        Args:
            view: The wrapped custom view to add.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addCustomViewOnBrowser(com.telelogic.rhapsody.core.IRPCustomView view)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addCustomViewOnBrowser(view._com))

    def add_custom_view_on_diagram(self, view: Any) -> None:
        """Adds a custom view to be applied on diagrams.

        Args:
            view: The wrapped custom view to add.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addCustomViewOnDiagram(com.telelogic.rhapsody.core.IRPCustomView view)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addCustomViewOnDiagram(view._com))

    def apply_browser_custom_views_on_diagrams(self) -> None:
        """Applies the browser custom views on diagrams.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::applyBrowserCustomViewsOnDiagrams()
        """
        AbstractRPModelElement.call_com(lambda: self._com.applyBrowserCustomViewsOnDiagrams())

    def get_active_custom_views_on_browser(self) -> RPCollection:
        """Returns the active custom views applied on the browser.

        Returns:
            An ``RPCollection`` of active browser custom views.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getActiveCustomViewsOnBrowser()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActiveCustomViewsOnBrowser", "activeCustomViewsOnBrowser"))

    def get_active_custom_views_on_diagram(self) -> RPCollection:
        """Returns the active custom views applied on diagrams.

        Returns:
            An ``RPCollection`` of active diagram custom views.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getActiveCustomViewsOnDiagram()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getActiveCustomViewsOnDiagram", "activeCustomViewsOnDiagram"))

    def remove_custom_view_on_browser(self, view: Any) -> None:
        """Removes a custom view from the browser.

        Args:
            view: The wrapped custom view to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::removeCustomViewOnBrowser(com.telelogic.rhapsody.core.IRPCustomView view)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeCustomViewOnBrowser(view._com))

    def remove_custom_view_on_diagram(self, view: Any) -> None:
        """Removes a custom view from diagrams.

        Args:
            view: The wrapped custom view to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::removeCustomViewOnDiagram(com.telelogic.rhapsody.core.IRPCustomView view)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeCustomViewOnDiagram(view._com))

    # --- CSV methods ---
    def close_csv_file(self) -> None:
        """Closes the CSV file currently open in the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::closeCSVFile()
        """
        AbstractRPModelElement.call_com(lambda: self._com.closeCSVFile())

    def open_csv_file(self, file_path: str, mode: int) -> None:
        """Opens a CSV file for requirements import.

        Args:
            file_path: The path of the CSV file to open.
            mode: The mode in which to open the file.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::openCSVFile(java.lang.String filePath, int mode)
        """
        AbstractRPModelElement.call_com(lambda: self._com.openCSVFile(file_path, mode))

    def reload_csv_file(self) -> None:
        """Reloads the CSV file currently open in the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::reloadCSVFile()
        """
        AbstractRPModelElement.call_com(lambda: self._com.reloadCSVFile())

    # --- Remote/Roundtrip methods ---
    def apply_roundtrip_diff_merge(self) -> None:
        """Applies the roundtrip diff merge for the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::applyRoundtripDiffMerge()
        """
        AbstractRPModelElement.call_com(lambda: self._com.applyRoundtripDiffMerge())

    def enable_rhapsody_model_manager(self, enabled: int) -> None:
        """Enables or disables Rhapsody Model Manager integration for the project.

        Args:
            enabled: ``1`` to enable, ``0`` to disable.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::enableRhapsodyModelManager(int enabled)
        """
        AbstractRPModelElement.call_com(lambda: self._com.enableRhapsodyModelManager(enabled))

    def find_elements_with_oslc_link(self, link: str) -> RPCollection:
        """Returns the elements that have an OSLC link matching the specified link.

        Args:
            link: The OSLC link to search for.

        Returns:
            An ``RPCollection`` of elements with the matching OSLC link.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::findElementsWithOSLCLink(java.lang.String link)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.findElementsWithOSLCLink(link)))

    def get_remote_resource_packages(self) -> RPCollection:
        """Returns the remote resource packages of the project.

        Returns:
            An ``RPCollection`` of remote resource packages.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getRemoteResourcePackages()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRemoteResourcePackages", "remoteResourcePackages"))

    def get_roundtrip_shadow_model(self) -> Any:
        """Returns the roundtrip shadow model of the project.

        Returns:
            The wrapped roundtrip shadow model.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getRoundtripShadowModel()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getRoundtripShadowModel", "roundtripShadowModel"))

    def is_actively_managed(self) -> int:
        """Checks whether the project is actively managed by Rhapsody Model Manager.

        Returns:
            ``1`` if the project is actively managed, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::isActivelyManaged()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isActivelyManaged", "activelyManaged"))

    def migrate_design_manager_links(self) -> None:
        """Migrates Design Manager links for the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::migrateDesignManagerLinks()
        """
        AbstractRPModelElement.call_com(lambda: self._com.migrateDesignManagerLinks())

    # --- Rose Import methods ---
    def import_package_from_rose(self, file_path: str) -> "RPPackage":
        """Imports a package from a Rational Rose model file.

        Args:
            file_path: The path of the Rose model file to import from.

        Returns:
            The wrapped ``IRPPackage`` created from the import.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::importPackageFromRose(java.lang.String filePath)
        """
        return cast("RPPackage", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.importPackageFromRose(file_path))))

    def import_project_from_rose(self, file_path: str) -> None:
        """Imports a project from a Rational Rose model file.

        Args:
            file_path: The path of the Rose model file to import from.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::importProjectFromRose(java.lang.String filePath)
        """
        AbstractRPModelElement.call_com(lambda: self._com.importProjectFromRose(file_path))

    # --- Events methods ---
    def check_events_base_ids_solve_collisions(self) -> int:
        """Checks events base IDs and solves collisions.

        Returns:
            The number of collisions solved.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::checkEventsBaseIdsSolveCollisions()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "checkEventsBaseIdsSolveCollisions", "eventsBaseIdsSolveCollisions"))

    def recalculate_events_base_ids(self) -> None:
        """Recalculates the events base IDs for the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::recalculateEventsBaseIds()
        """
        AbstractRPModelElement.call_com(lambda: self._com.recalculateEventsBaseIds())

    # --- Misc methods ---
    def add_spell_checker_result(self, word: str, suggestion: str) -> None:
        """Adds a spell checker result with a suggestion.

        Args:
            word: The misspelled word.
            suggestion: The suggested correction.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::addSpellCheckerResult(java.lang.String word, java.lang.String suggestion)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addSpellCheckerResult(word, suggestion))

    def clean_unresolved_elements(self) -> None:
        """Cleans unresolved elements from the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::cleanUnresolvedElements()
        """
        AbstractRPModelElement.call_com(lambda: self._com.cleanUnresolvedElements())

    def end_transaction_of_no_cg_interest(self) -> None:
        """Ends a transaction of no code generation interest.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::endTransactionOfNoCGInterest()
        """
        AbstractRPModelElement.call_com(lambda: self._com.endTransactionOfNoCGInterest())

    def get_default_directory_scheme(self) -> int:
        """Returns the default directory scheme of the project.

        Returns:
            The default directory scheme as an int.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getDefaultDirectoryScheme()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getDefaultDirectoryScheme", "defaultDirectoryScheme"))

    def get_new_progress_bar(self) -> "RPProgressBar":
        """Returns a new progress bar.

        Returns:
            The wrapped ``IRPProgressBar`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getNewProgressBar()
        """
        return cast("RPProgressBar", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getNewProgressBar", "newProgressBar")))

    def get_notify_plugin_on_elements_changed(self) -> int:
        """Checks whether plugins are notified when elements change.

        Returns:
            ``1`` if plugins are notified, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getNotifyPluginOnElementsChanged()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getNotifyPluginOnElementsChanged", "notifyPluginOnElementsChanged"))

    def get_requirements_by_id(self, id: str) -> RPCollection:
        """Returns the requirements matching the specified ID.

        Args:
            id: The requirement ID to search for.

        Returns:
            An ``RPCollection`` of matching requirements.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::getRequirementsByID(java.lang.String id)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getRequirementsByID(id)))

    def remove(self) -> None:
        """Removes the project.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::remove()
        """
        AbstractRPModelElement.call_com(lambda: self._com.remove())

    def save_as_prev_version(self, file_path: str) -> None:
        """Saves the project to a previous version file path.

        Args:
            file_path: The path to save the project to.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::saveAsPrevVersion(java.lang.String filePath)
        """
        AbstractRPModelElement.call_com(lambda: self._com.saveAsPrevVersion(file_path))

    def set_default_directory_scheme(self, scheme: int) -> None:
        """Sets the default directory scheme of the project.

        Args:
            scheme: The default directory scheme to set.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setDefaultDirectoryScheme(int scheme)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDefaultDirectoryScheme", "defaultDirectoryScheme", scheme)

    def set_global_configuration(self, config: str) -> None:
        """Sets the global configuration of the project.

        Args:
            config: The global configuration to set.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setGlobalConfiguration(java.lang.String config)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setGlobalConfiguration", "globalConfiguration", config)

    def set_notify_plugin_on_elements_changed(self, enabled: int) -> None:
        """Sets whether plugins are notified when elements change.

        Args:
            enabled: ``1`` to notify plugins, ``0`` to not notify.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setNotifyPluginOnElementsChanged(int enabled)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setNotifyPluginOnElementsChanged", "notifyPluginOnElementsChanged", enabled)

    def set_object_explicit(self, obj: Any) -> None:
        """Sets the specified object as explicit.

        Args:
            obj: The wrapped model element to set as explicit.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setObjectExplicit(com.telelogic.rhapsody.core.IRPModelElement obj)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setObjectExplicit(obj._com))

    def set_object_implicit(self, obj: Any) -> None:
        """Sets the specified object as implicit.

        Args:
            obj: The wrapped model element to set as implicit.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setObjectImplicit(com.telelogic.rhapsody.core.IRPModelElement obj)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setObjectImplicit(obj._com))

    def set_use_unique_stereotype_and_ref_cache(self, enabled: int) -> None:
        """Sets whether to use a unique stereotype and reference cache.

        Args:
            enabled: ``1`` to use the unique cache, ``0`` to not use it.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setUseUniqueStereotypeAndRefCache(int enabled)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setUseUniqueStereotypeAndRefCache", "useUniqueStereotypeAndRefCache", enabled)

    def set_wait_dialog_watchdog_value(self, value: int) -> None:
        """Sets the wait dialog watchdog value.

        Args:
            value: The wait dialog watchdog value to set.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::setWaitDialogWatchdogValue(int value)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setWaitDialogWatchdogValue", "waitDialogWatchdogValue", value)

    def start_transaction_of_no_cg_interest(self) -> None:
        """Starts a transaction of no code generation interest.

        Reference:
            com.telelogic.rhapsody.core.IRPProject::startTransactionOfNoCGInterest()
        """
        AbstractRPModelElement.call_com(lambda: self._com.startTransactionOfNoCGInterest())


AbstractRPModelElement.register_wrapper("Project", RPProject)
