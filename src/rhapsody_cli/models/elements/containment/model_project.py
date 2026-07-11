"""Wraps ``com.telelogic.rhapsody.core.IRPProject``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.containment.model_package import RPPackage


class RPProject(RPPackage):
    """Wraps ``IRPProject``: represents the top-level project container."""

    def addPackage(self, name: str) -> Any:
        """Adds a new package to the project.

        Args:
            name: The name of the new package.

        Returns:
            The wrapped ``IRPPackage`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addPackage(name)))

    def close(self) -> None:
        """Closes the project."""
        AbstractRPModelElement.call_com(lambda: self._com.close())

    def becomeActiveProject(self) -> None:
        """Makes this project the active project in Rhapsody."""
        AbstractRPModelElement.call_com(lambda: self._com.becomeActiveProject())

    def findComponent(self, name: str) -> Any:
        """Finds a component in the project by name.

        Args:
            name: The name of the component to find.

        Returns:
            The wrapped component element if found, otherwise empty wrapper.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findComponent(name)))

    def getPackages(self) -> RPCollection:
        """Returns all top-level packages in the project.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getPackages", "packages"))

    def getRoot(self) -> "RPProject":
        """Returns the root project element.

        Returns:
            The project itself, which acts as the root container.
        """
        return self

    def addClass(self, name: str) -> Any:
        """Adds a new class to the project's top level.

        Args:
            name: The name of the new class.

        Returns:
            The wrapped ``IRPClass`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name)))

    def addActor(self, name: str) -> Any:
        """Adds a new actor to the project's top level.

        Args:
            name: The name of the new actor.

        Returns:
            The wrapped ``IRPActor`` created.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addActor(name)))

    def getComponents(self) -> RPCollection:
        """Returns all components in the project.

        Returns:
            An ``RPCollection`` of component elements.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getComponents", "components"))

    def findByName(self, name: str) -> Any:
        """Finds an element in the project by name.

        Args:
            name: The name of the element to find.

        Returns:
            The wrapped element if found.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findByName(name)))

    def findByMetaClass(self, meta_class: str) -> RPCollection:
        """Finds all elements in the project with a given metaclass.

        Args:
            meta_class: The metaclass name to search for.

        Returns:
            An ``RPCollection`` of matching elements.
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.findByMetaClass(meta_class)))

    def findElementByGUID(self, guid: str) -> Any:
        """Finds an element in the project by GUID.

        Args:
            guid: The GUID of the element to find.

        Returns:
            The wrapped element if found.
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findElementByGUID(guid)))

    def getIsDirty(self) -> int:
        """Checks whether the project has unsaved changes.

        Returns:
            ``1`` if the project is dirty (has unsaved changes), ``0`` otherwise.
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsDirty", "isDirty"))

    def setDirty(self, is_dirty: int) -> None:
        """Sets the dirty flag of the project.

        Args:
            is_dirty: ``1`` to mark as dirty, ``0`` to mark as clean.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDirty", "dirty", is_dirty)


AbstractRPModelElement.register_wrapper("Project", RPProject)
