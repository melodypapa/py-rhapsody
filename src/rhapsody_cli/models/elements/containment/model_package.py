"""Wraps ``com.telelogic.rhapsody.core.IRPPackage``."""

from typing import Any

from rhapsody_cli.models.core import RPCollection, RPUnit, call_com, register_wrapper, wrap


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

    def getNestedPackages(self) -> "RPCollection":
        """Returns all nested packages in this package.

        Returns:
            An ``RPCollection`` of ``IRPPackage`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getNestedPackages()))

    def getClasses(self) -> "RPCollection":
        """Returns all classes contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPClass`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getClasses()))

    def getActors(self) -> "RPCollection":
        """Returns all actors contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPActor`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getActors()))

    def getUseCases(self) -> "RPCollection":
        """Returns all use cases contained in this package.

        Returns:
            An ``RPCollection`` of ``IRPUseCase`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getUseCases()))

    def addUseCase(self, name: str) -> Any:
        """Adds a new use case to the package.

        Args:
            name: The name of the new use case.

        Returns:
            The wrapped ``IRPUseCase`` created.
        """
        return wrap(call_com(lambda: self._com.addUseCase(name)))

    def addInterface(self, name: str) -> Any:
        """Adds a new interface to the package.

        Args:
            name: The name of the new interface.

        Returns:
            The wrapped interface element created.
        """
        return wrap(call_com(lambda: self._com.addInterface(name)))

    def addSignal(self, name: str) -> Any:
        """Adds a new signal to the package.

        Args:
            name: The name of the new signal.

        Returns:
            The wrapped signal element created.
        """
        return wrap(call_com(lambda: self._com.addSignal(name)))

    def addException(self, name: str) -> Any:
        """Adds a new exception to the package.

        Args:
            name: The name of the new exception.

        Returns:
            The wrapped exception element created.
        """
        return wrap(call_com(lambda: self._com.addException(name)))

    def addEnumeration(self, name: str) -> Any:
        """Adds a new enumeration to the package.

        Args:
            name: The name of the new enumeration.

        Returns:
            The wrapped enumeration element created.
        """
        return wrap(call_com(lambda: self._com.addEnumeration(name)))

    def getEnumerations(self) -> "RPCollection":
        """Returns all enumerations contained in this package.

        Returns:
            An ``RPCollection`` of enumeration elements.
        """
        return RPCollection(call_com(lambda: self._com.getEnumerations()))


register_wrapper("Package", RPPackage)
