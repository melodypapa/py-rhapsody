"""Wraps ``com.telelogic.rhapsody.core.IRPClass``."""

from typing import Any

from rhapsody_cli.models._core import call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPClass(RPClassifier):
    """Wraps ``IRPClass``: represents a class in the model."""

    def addSuperclass(self, super_class: "RPClass") -> None:
        """Adds a superclass to this class.

        Args:
            super_class: The class to inherit from.
        """
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        """Adds a constructor operation to this class.

        Args:
            arguments_data: The argument specification for the constructor.

        Returns:
            The wrapped ``IRPOperation`` for the new constructor.
        """
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        """Adds a destructor operation to this class.

        Returns:
            The wrapped ``IRPOperation`` for the new destructor.
        """
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        """Checks whether this class is abstract.

        Returns:
            ``True`` if the class is abstract, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> Any:
        """Adds a nested class to this class.

        Args:
            name: The name of the new nested class.

        Returns:
            The wrapped ``IRPClass`` created.
        """
        return wrap(call_com(lambda: self._com.addClass(name)))


register_wrapper("Class", RPClass)
