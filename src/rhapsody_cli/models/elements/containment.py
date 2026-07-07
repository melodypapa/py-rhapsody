"""Containment-family wrappers: mirrors IRPPackage and IRPProject from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, register_wrapper, wrap


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``: represents a package that contains model elements."""

    def addClass(self, name: str) -> Any:
        """Adds a new class to the package.

        Args:
            name: The name of the new class.

        Returns:
            The wrapped ``IRPClass`` created.
        """
        return wrap(call_com(lambda: self._com.addClass(name)))

    def addNestedPackage(self, name: str) -> Any:
        """Adds a nested package to this package.

        Args:
            name: The name of the new nested package.

        Returns:
            The wrapped ``IRPPackage`` created.
        """
        return wrap(call_com(lambda: self._com.addNestedPackage(name)))

    def addActor(self, name: str) -> Any:
        """Adds a new actor to the package.

        Args:
            name: The name of the new actor.

        Returns:
            The wrapped ``IRPActor`` created.
        """
        return wrap(call_com(lambda: self._com.addActor(name)))

    def addGlobalFunction(self, name: str) -> Any:
        """Adds a new global function to the package.

        Args:
            name: The name of the new global function.

        Returns:
            The wrapped function element created.
        """
        return wrap(call_com(lambda: self._com.addGlobalFunction(name)))


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


register_wrapper("Package", RPPackage)
register_wrapper("Project", RPProject)
