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


class RPProject(RPPackage):
    """Wraps ``IRPProject``: represents the top-level project container."""

    # IRPProject method parity checklist:
    # [ ] gatewayExportToXML  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] gatewayExportToXML2  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] generateReport  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] addComponent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] addCustomViewOnBrowser  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] addCustomViewOnDiagram  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] add_package  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] addProfile  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] addSpellCheckerResult  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] allowAutoSave  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] allowNonUniqueNames  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] applyBrowserCustomViewsOnDiagrams  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] applyRoundtripDiffMerge  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] become_active_project  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] checkEventsBaseIdsSolveCollisions  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] cleanUnresolvedElements  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] close  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] closeCSVFile  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] deleteComponent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] enableRhapsodyModelManager  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] endTransactionOfNoCGInterest  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] find_component  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] findElementByBinaryID  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] findElementByFileName  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] find_element_by_guid  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] findElementsWithOSLCLink  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] getActiveComponent  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getActiveConfiguration  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] getActiveCustomViewsOnBrowser  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getActiveCustomViewsOnDiagram  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] getAllStereotypes  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getCgSimplifiedModelPackage  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getCodeGeneratedFiles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_components  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] getDefaultDirectoryScheme  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getNewCollaboration  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getNewProgressBar  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getNotifyPluginOnElementsChanged  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] getProfiles  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] getRemoteResourcePackages  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRequirementsByID  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] getRoundtripShadowModel  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] highlightFromCode  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] importPackageFromRose  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] importProjectFromRose  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] isActivelyManaged  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] isModifiedRecursive  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] locateInIDE  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] migrateDesignManagerLinks  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [deprecated] moveToDesignManager  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] moveToDesignManagerAfterLogin  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [ ] openCSVFile  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] recalculateEventsBaseIds  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] reloadCSVFile  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] remove  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] removeCustomViewOnBrowser  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] removeCustomViewOnDiagram  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] save  [x] impl  [x] docstring  [x] unit test  [ ] integration test   (inherited from RPUnit)
    # [x] saveAs  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] saveAsPrevVersion  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setActiveComponent  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [x] setActiveConfiguration  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] setDefaultDirectoryScheme  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setGlobalConfiguration  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setNotifyPluginOnElementsChanged  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setObjectExplicit  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setObjectImplicit  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setUseUniqueStereotypeAndRefCache  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] setWaitDialogWatchdogValue  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [ ] startTransactionOfNoCGInterest  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
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


AbstractRPModelElement.register_wrapper("Project", RPProject)
