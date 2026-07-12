"""Wraps ``com.telelogic.rhapsody.core.IRPProject``."""

from typing import TYPE_CHECKING, Any, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment.model_package import RPPackage

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_actor import RPActor
    from rhapsody_cli.models.elements.classifiers.model_class import RPClass
    from rhapsody_cli.models.elements.containment.model_component import RPComponent


class RPProject(RPPackage):
    """Wraps ``IRPProject``: represents the top-level project container."""

    # IRPProject method parity checklist:
    # [ ] gatewayExportToXML  [ ] impl  [ ] docstring  [ ] test
    # [ ] gatewayExportToXML2  [ ] impl  [ ] docstring  [ ] test
    # [ ] generateReport  [ ] impl  [ ] docstring  [ ] test
    # [ ] addComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] addCustomViewOnBrowser  [ ] impl  [ ] docstring  [ ] test
    # [ ] addCustomViewOnDiagram  [ ] impl  [ ] docstring  [ ] test
    # [x] add_package  [x] impl  [x] docstring  [x] test
    # [ ] addProfile  [ ] impl  [ ] docstring  [ ] test
    # [ ] addSpellCheckerResult  [ ] impl  [ ] docstring  [ ] test
    # [ ] allowAutoSave  [ ] impl  [ ] docstring  [ ] test
    # [ ] allowNonUniqueNames  [ ] impl  [ ] docstring  [ ] test
    # [ ] applyBrowserCustomViewsOnDiagrams  [ ] impl  [ ] docstring  [ ] test
    # [ ] applyRoundtripDiffMerge  [ ] impl  [ ] docstring  [ ] test
    # [x] become_active_project  [x] impl  [x] docstring  [x] test
    # [ ] checkEventsBaseIdsSolveCollisions  [ ] impl  [ ] docstring  [ ] test
    # [ ] cleanUnresolvedElements  [ ] impl  [ ] docstring  [ ] test
    # [x] close  [x] impl  [x] docstring  [x] test
    # [ ] closeCSVFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] enableRhapsodyModelManager  [ ] impl  [ ] docstring  [ ] test
    # [ ] endTransactionOfNoCGInterest  [ ] impl  [ ] docstring  [ ] test
    # [x] find_component  [x] impl  [x] docstring  [x] test
    # [ ] findElementByBinaryID  [ ] impl  [ ] docstring  [ ] test
    # [ ] findElementByFileName  [ ] impl  [ ] docstring  [ ] test
    # [x] find_element_by_guid  [x] impl  [x] docstring  [x] test
    # [ ] findElementsWithOSLCLink  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActiveComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActiveConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActiveCustomViewsOnBrowser  [ ] impl  [ ] docstring  [ ] test
    # [ ] getActiveCustomViewsOnDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] getAllStereotypes  [ ] impl  [ ] docstring  [ ] test
    # [ ] getCgSimplifiedModelPackage  [ ] impl  [ ] docstring  [ ] test
    # [ ] getCodeGeneratedFiles  [ ] impl  [ ] docstring  [ ] test
    # [x] get_components  [x] impl  [x] docstring  [x] test
    # [ ] getDefaultDirectoryScheme  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNewCollaboration  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNewProgressBar  [ ] impl  [ ] docstring  [ ] test
    # [ ] getNotifyPluginOnElementsChanged  [ ] impl  [ ] docstring  [ ] test
    # [ ] getProfiles  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRemoteResourcePackages  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRequirementsByID  [ ] impl  [ ] docstring  [ ] test
    # [ ] getRoundtripShadowModel  [ ] impl  [ ] docstring  [ ] test
    # [ ] highlightFromCode  [ ] impl  [ ] docstring  [ ] test
    # [ ] importPackageFromRose  [ ] impl  [ ] docstring  [ ] test
    # [ ] importProjectFromRose  [ ] impl  [ ] docstring  [ ] test
    # [ ] isActivelyManaged  [ ] impl  [ ] docstring  [ ] test
    # [ ] isModifiedRecursive  [ ] impl  [ ] docstring  [ ] test
    # [ ] locateInIDE  [ ] impl  [ ] docstring  [ ] test
    # [ ] migrateDesignManagerLinks  [ ] impl  [ ] docstring  [ ] test
    # [deprecated] moveToDesignManager  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] moveToDesignManagerAfterLogin  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [ ] openCSVFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] recalculateEventsBaseIds  [ ] impl  [ ] docstring  [ ] test
    # [ ] reloadCSVFile  [ ] impl  [ ] docstring  [ ] test
    # [ ] remove  [ ] impl  [ ] docstring  [ ] test
    # [ ] removeCustomViewOnBrowser  [ ] impl  [ ] docstring  [ ] test
    # [ ] removeCustomViewOnDiagram  [ ] impl  [ ] docstring  [ ] test
    # [x] save  [x] impl  [x] docstring  [x] test   (inherited from RPUnit)
    # [ ] saveAs  [ ] impl  [ ] docstring  [ ] test
    # [ ] saveAsPrevVersion  [ ] impl  [ ] docstring  [ ] test
    # [ ] setActiveComponent  [ ] impl  [ ] docstring  [ ] test
    # [ ] setActiveConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] setDefaultDirectoryScheme  [ ] impl  [ ] docstring  [ ] test
    # [ ] setGlobalConfiguration  [ ] impl  [ ] docstring  [ ] test
    # [ ] setNotifyPluginOnElementsChanged  [ ] impl  [ ] docstring  [ ] test
    # [ ] setObjectExplicit  [ ] impl  [ ] docstring  [ ] test
    # [ ] setObjectImplicit  [ ] impl  [ ] docstring  [ ] test
    # [ ] setUseUniqueStereotypeAndRefCache  [ ] impl  [ ] docstring  [ ] test
    # [ ] setWaitDialogWatchdogValue  [ ] impl  [ ] docstring  [ ] test
    # [ ] startTransactionOfNoCGInterest  [ ] impl  [ ] docstring  [ ] test
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


AbstractRPModelElement.register_wrapper("Project", RPProject)
