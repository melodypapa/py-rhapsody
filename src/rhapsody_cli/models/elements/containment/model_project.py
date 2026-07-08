"""Wraps ``com.telelogic.rhapsody.core.IRPProject``."""

from typing import Any

from rhapsody_cli.models._core import RPCollection, call_com, register_wrapper, wrap
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
        return wrap(call_com(lambda: self._com.addPackage(name)))

    def close(self) -> None:
        """Closes the project."""
        call_com(lambda: self._com.close())

    def becomeActiveProject(self) -> None:
        """Makes this project the active project in Rhapsody."""
        call_com(lambda: self._com.becomeActiveProject())

    def findComponent(self, name: str) -> Any:
        """Finds a component in the project by name.

        Args:
            name: The name of the component to find.

        Returns:
            The wrapped component element if found, otherwise empty wrapper.
        """
        return wrap(call_com(lambda: self._com.findComponent(name)))

    def getPackages(self) -> RPCollection:
        """Returns all top-level packages in the project.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getPackages()))

    def getRoot(self) -> "RPProject":
        """Returns the root project element.

        Returns:
            The project itself, which acts as the root container.
        """
        return self


register_wrapper("Project", RPProject)
