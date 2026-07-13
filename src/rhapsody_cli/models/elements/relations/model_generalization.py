"""Wraps ``com.telelogic.rhapsody.core.IRPGeneralization``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_usecase import RPExtensionPoint


class RPGeneralization(RPModelElement):
    """Wraps ``IRPGeneralization``: a generalization (inheritance) relationship."""

    # IRPGeneralization method parity checklist:
    # [x] getBaseClass  [x] impl  [x] docstring  [ ] test
    # [x] getDerivedClass  [x] impl  [x] docstring  [ ] test
    # [x] getExtensionPoint  [x] impl  [x] docstring  [ ] test
    # [x] getIsVirtual  [x] impl  [x] docstring  [ ] test
    # [x] getVisibility  [x] impl  [x] docstring  [ ] test
    # [x] setBaseClass  [x] impl  [x] docstring  [ ] test
    # [x] setDerivedClass  [x] impl  [x] docstring  [ ] test
    # [x] setExtensionPoint  [x] impl  [x] docstring  [ ] test
    # [x] setIsVirtual  [x] impl  [x] docstring  [ ] test
    # [x] setVisibility  [x] impl  [x] docstring  [ ] test
    # [inherited] IRPModelElement methods (covered by RPModelElement checklists)
    # No deprecated IRPGeneralization methods.

    def get_base_class(self) -> RPClassifier:
        """Returns the base class (parent) of the generalization.

        Returns:
            The wrapped base classifier.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::getBaseClass()
        """
        return cast(RPClassifier, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getBaseClass", "baseClass")))

    def get_derived_class(self) -> RPClassifier:
        """Returns the derived class (child) of the generalization.

        Returns:
            The wrapped derived classifier.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::getDerivedClass()
        """
        return cast(RPClassifier, AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getDerivedClass", "derivedClass")))

    def get_extension_point(self) -> "RPExtensionPoint":
        """Returns the extension point for this generalization (for use case extension).

        Returns:
            The wrapped extension point, or None if not applicable.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::getExtensionPoint()
        """
        return cast("RPExtensionPoint", AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getExtensionPoint", "extensionPoint")))

    def get_is_virtual(self) -> int:
        """Checks whether this generalization is virtual.

        Returns:
            ``1`` if virtual, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::getIsVirtual()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsVirtual", "isVirtual"))

    def get_visibility(self) -> int:
        """Returns the visibility of the generalization.

        Returns:
            The visibility as an integer (0=private, 1=protected, 2=public, 3=package).

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::getVisibility()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getVisibility", "visibility"))

    def set_base_class(self, base_class: RPClassifier) -> None:
        """Sets the base class (parent) of the generalization.

        Args:
            base_class: The wrapped classifier to set as the base class.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::setBaseClass(com.telelogic.rhapsody.core.IRPClassifier baseClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setBaseClass(base_class._com))

    def set_derived_class(self, derived_class: RPClassifier) -> None:
        """Sets the derived class (child) of the generalization.

        Args:
            derived_class: The wrapped classifier to set as the derived class.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::setDerivedClass(com.telelogic.rhapsody.core.IRPClassifier derivedClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setDerivedClass(derived_class._com))

    def set_extension_point(self, extension_point: RPModelElement) -> None:
        """Sets the extension point for this generalization.

        Args:
            extension_point: The wrapped extension point to set.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::setExtensionPoint(com.telelogic.rhapsody.core.IRPExtensionPoint extensionPoint)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setExtensionPoint(extension_point._com))

    def set_is_virtual(self, is_virtual: int) -> None:
        """Sets whether this generalization is virtual.

        Args:
            is_virtual: ``1`` to mark as virtual, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::setIsVirtual(int isVirtual)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsVirtual(is_virtual))

    def set_visibility(self, visibility: int) -> None:
        """Sets the visibility of the generalization.

        Args:
            visibility: The visibility value (0=private, 1=protected, 2=public, 3=package).

        Reference:
            com.telelogic.rhapsody.core.IRPGeneralization::setVisibility(int visibility)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setVisibility(visibility))


AbstractRPModelElement.register_wrapper("Generalization", RPGeneralization)