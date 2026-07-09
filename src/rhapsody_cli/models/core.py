"""Core wrapping machinery shared by all rhapsody_cli element wrappers.

``call_com`` translates COM failures into ``RhapsodyRuntimeException``.
``AbstractRPModelElement`` is the abstract base class providing common utilities.
``RPModelElement`` is the base interface for every wrapped Rhapsody model
element, mirroring ``com.telelogic.rhapsody.core.IRPModelElement``.
``wrap()`` dispatches a raw COM object to its matching wrapper class using
a registry populated by each element module at import time.
"""

from enum import IntEnum
from typing import Any, Callable, Dict, Iterator, Type, TypeVar

from rhapsody_cli.exceptions import RhapsodyRuntimeException

try:
    import pywintypes
except ImportError:  # pragma: no cover - pywintypes is Windows-only
    pywintypes = None

T = TypeVar("T")


class AbstractRPModelElement:
    """Abstract base class providing common utilities for all Rhapsody element wrappers.

    Implements class methods for COM interaction, element wrapping, and registry management.
    """

    #: Maps a Rhapsody ``getMetaClass()`` string (e.g. "Class", "Package") to the
    #: wrapper class that should represent it. Populated by each element module
    #: at import time via ``register_wrapper``. Unmapped meta classes fall back
    #: to ``RPModelElement`` in ``wrap()``.
    _WRAPPER_REGISTRY: Dict[str, Type["AbstractRPModelElement"]] = {}

    @classmethod
    def register_wrapper(cls, meta_class: str, wrapper_cls: Type["AbstractRPModelElement"]) -> None:
        """Register ``wrapper_cls`` as the wrapper for COM objects of ``meta_class``."""
        cls._WRAPPER_REGISTRY[meta_class] = wrapper_cls

    @classmethod
    def call_com(cls, func: Callable[[], T]) -> T:
        """Invoke a COM call, translating COM errors into RhapsodyRuntimeException."""
        try:
            return func()
        except Exception as exc:
            # pywintypes is Windows-only; on other platforms there is no live COM
            # connection so a com_error cannot occur here.
            if pywintypes is not None and isinstance(exc, pywintypes.com_error):
                raise RhapsodyRuntimeException(str(exc)) from exc
            raise

    @classmethod
    def _wrap_if_element(cls, value: Any) -> Any:
        """Wrap ``value`` if it looks like a Rhapsody model element."""
        if hasattr(value, "getMetaClass") or hasattr(value, "metaClass"):
            return cls.wrap(value)
        return value

    @classmethod
    def wrap(cls, com_obj: Any) -> "AbstractRPModelElement":
        """Wrap a raw Rhapsody COM model element in its matching wrapper class."""
        meta_class = str(cls._get_method_or_property(com_obj, "getMetaClass", "metaClass"))
        wrapper_cls = cls._WRAPPER_REGISTRY.get(meta_class, RPModelElement)
        return wrapper_cls(com_obj)

    @classmethod
    def _get_method_or_property(cls, com_obj: Any, method_name: str, prop_name: str) -> Any:
        """Read a value from ``com_obj``, preferring the Java-style method.

        Some Rhapsody COM automation Prog IDs (e.g. the Java-mirroring
        ``Rhapsody.Application``) expose model element attributes as methods
        (``getName()``, ``getGUID()``, ...), while others (e.g.
        ``Rhapsody2.Application.1``) expose the same data as bare COM
        properties (``name``, ``GUID``, ...). Prefer the method when present,
        and fall back to the bare property otherwise.
        """
        if hasattr(com_obj, method_name):
            return cls.call_com(lambda: getattr(com_obj, method_name)())
        return cls.call_com(lambda: getattr(com_obj, prop_name))

    @classmethod
    def _set_method_or_property(cls, com_obj: Any, method_name: str, prop_name: str, value: Any) -> None:
        """Write a value to ``com_obj``, preferring the Java-style setter method.

        See :func:`_get_method_or_property` for why both forms exist.
        """
        if hasattr(com_obj, method_name):
            cls.call_com(lambda: getattr(com_obj, method_name)(value))
        else:
            cls.call_com(lambda: setattr(com_obj, prop_name, value))


# Module-level convenience functions for backward compatibility
def register_wrapper(meta_class: str, wrapper_cls: Type["AbstractRPModelElement"]) -> None:
    """Register ``wrapper_cls`` as the wrapper for COM objects of ``meta_class``.

    Backward compatibility wrapper that delegates to AbstractRPModelElement.register_wrapper().
    """
    AbstractRPModelElement.register_wrapper(meta_class, wrapper_cls)


def call_com(func: Callable[[], T]) -> T:
    """Invoke a COM call, translating COM errors into RhapsodyRuntimeException.

    Backward compatibility wrapper that delegates to AbstractRPModelElement.call_com().
    """
    return AbstractRPModelElement.call_com(func)


def _wrap_if_element(value: Any) -> Any:
    """Wrap ``value`` if it looks like a Rhapsody model element.

    Backward compatibility wrapper that delegates to AbstractRPModelElement._wrap_if_element().
    """
    return AbstractRPModelElement._wrap_if_element(value)


def wrap(com_obj: Any) -> "AbstractRPModelElement":
    """Wrap a raw Rhapsody COM model element in its matching wrapper class.

    Backward compatibility wrapper that delegates to AbstractRPModelElement.wrap().
    """
    return AbstractRPModelElement.wrap(com_obj)


def _get_method_or_property(com_obj: Any, method_name: str, prop_name: str) -> Any:
    """Read a value from ``com_obj``, preferring the Java-style method.

    Backward compatibility wrapper that delegates to AbstractRPModelElement._get_method_or_property().
    """
    return AbstractRPModelElement._get_method_or_property(com_obj, method_name, prop_name)


def _set_method_or_property(com_obj: Any, method_name: str, prop_name: str, value: Any) -> None:
    """Write a value to ``com_obj``, preferring the Java-style setter method.

    Backward compatibility wrapper that delegates to AbstractRPModelElement._set_method_or_property().
    """
    AbstractRPModelElement._set_method_or_property(com_obj, method_name, prop_name, value)


class RPModelElement(AbstractRPModelElement):
    """Wraps ``IRPModelElement``: the base interface for all model elements.

    Method names mirror the Rhapsody Java API exactly (``getName``,
    ``setName``, ``getMetaClass``, ``getGUID``, ...). Some Rhapsody COM Prog
    IDs expose these as bare properties instead of methods; see
    :func:`_get_method_or_property`.
    """

    # IRPModelElement method parity checklist:
    # [x] addAssociation                  [x] impl  [x] docstring  [x] test
    # [x] addDependency                   [x] impl  [x] docstring  [x] test
    # [x] addDependencyBetween            [x] impl  [x] docstring  [x] test
    # [x] addDependencyTo                 [x] impl  [x] docstring  [x] test
    # [x] addLinkToElement                [x] impl  [x] docstring  [x] test
    # [x] addNewAggr                      [x] impl  [x] docstring  [x] test
    # [x] addProperty                     [x] impl  [x] docstring  [x] test
    # [x] addRedefines                    [x] impl  [x] docstring  [x] test
    # [x] addRemoteDependencyTo           [x] impl  [x] docstring  [x] test
    # [x] addSpecificStereotype           [x] impl  [x] docstring  [x] test
    # [x] addStereotype                   [x] impl  [x] docstring  [x] test
    # [x] becomeTemplateInstantiationOf   [x] impl  [x] docstring  [x] test
    # [x] changeTo                        [x] impl  [x] docstring  [x] test
    # [x] clone                           [x] impl  [x] docstring  [x] test
    # [x] createOSLCLink                  [x] impl  [x] docstring  [x] test  (NotImplementedError)
    # [x] deleteDependency                [x] impl  [x] docstring  [x] test
    # [x] deleteFromProject               [x] impl  [x] docstring  [x] test
    # [x] deleteOSLCLink                  [x] impl  [x] docstring  [x] test  (NotImplementedError)
    # [x] errorMessage                    [x] impl  [x] docstring  [x] test
    # [x] findElementsByFullName          [x] impl  [x] docstring  [x] test
    # [x] findNestedElement               [x] impl  [x] docstring  [x] test
    # [x] findNestedElementRecursive      [x] impl  [x] docstring  [x] test
    # [x] getAllTags                      [x] impl  [x] docstring  [x] test
    # [x] getAnnotations                  [x] impl  [x] docstring  [x] test
    # [x] getAssociationClasses           [x] impl  [x] docstring  [x] test
    # [x] getBinaryID                     [x] impl  [x] docstring  [x] test
    # [x] getConstraints                  [x] impl  [x] docstring  [x] test
    # [x] getConstraintsByHim             [x] impl  [x] docstring  [x] test
    # [x] getControlledFiles              [x] impl  [x] docstring  [x] test
    # [x] getDecorationStyle              [x] impl  [x] docstring  [x] test
    # [x] getDependencies                 [x] impl  [x] docstring  [x] test
    # [x] getDescription                  [x] impl  [x] docstring  [x] test
    # [x] getDescriptionHTML              [x] impl  [x] docstring  [x] test
    # [x] getDescriptionPlainText         [x] impl  [x] docstring  [x] test
    # [x] getDescriptionRTF               [x] impl  [x] docstring  [x] test
    # [x] getDisplayName                  [x] impl  [x] docstring  [x] test
    # [x] getDisplayNameRTF               [x] impl  [x] docstring  [x] test
    # [x] getErrorMessage                 [x] impl  [x] docstring  [x] test
    # [x] getFullPathName                 [x] impl  [x] docstring  [x] test
    # [x] getFullPathNameIn               [x] impl  [x] docstring  [x] test
    # [x] getGUID                         [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getHyperLinks                   [x] impl  [x] docstring  [x] test
    # [x] getIconFileName                 [x] impl  [x] docstring  [x] test
    # [x] getInterfaceName                [x] impl  [x] docstring  [x] test
    # [x] getIsExternal                   [x] impl  [x] docstring  [x] test
    # [x] getIsOfMetaClass                [x] impl  [x] docstring  [x] test
    # [x] getIsShowDisplayName            [x] impl  [x] docstring  [x] test
    # [x] getIsUnresolved                 [x] impl  [x] docstring  [x] test
    # [x] getLocalTags                    [x] impl  [x] docstring  [x] test
    # [x] getMainDiagram                  [x] impl  [x] docstring  [x] test
    # [x] getMetaClass                    [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getName                         [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] getNestedElements               [x] impl  [x] docstring  [x] test
    # [x] getNestedElementsByMetaClass    [x] impl  [x] docstring  [x] test
    # [x] getNestedElementsRecursive      [x] impl  [x] docstring  [x] test
    # [x] getNewTermStereotype            [x] impl  [x] docstring  [x] test
    # [x] getOfTemplate                   [x] impl  [x] docstring  [x] test
    # [x] getOSLCLinks                    [x] impl  [x] docstring  [x] test  (NotImplementedError)
    # [x] getOverlayIconFileName          [x] impl  [x] docstring  [x] test
    # [x] getOverriddenProperties         [x] impl  [x] docstring  [x] test
    # [x] getOverriddenPropertiesByPattern [x] impl  [x] docstring  [x] test
    # [x] getOwnedDependencies            [x] impl  [x] docstring  [x] test
    # [x] getOwner                        [x] impl  [x] docstring  [x] test
    # [x] getProject                      [x] impl  [x] docstring  [x] test
    # [x] getPropertyValue                [x] impl  [x] docstring  [x] test
    # [x] getPropertyValueConditional     [x] impl  [x] docstring  [x] test
    # [x] getPropertyValueConditionalExplicit [x] impl  [x] docstring  [x] test
    # [x] getPropertyValueExplicit        [x] impl  [x] docstring  [x] test
    # [x] getRedefines                    [x] impl  [x] docstring  [x] test
    # [x] getReferences                   [x] impl  [x] docstring  [x] test
    # [x] getRemoteDependencies           [x] impl  [x] docstring  [x] test
    # [x] getRemoteURI                    [x] impl  [x] docstring  [x] test
    # [x] getRequirementTraceabilityHandle [x] impl  [x] docstring  [x] test
    # [x] getRmmUrl                       [x] impl  [x] docstring  [x] test
    # [x] getSaveUnit                     [x] impl  [x] docstring  [x] test
    # [x] getStereotypes                  [x] impl  [x] docstring  [x] test
    # [x] getTag                          [x] impl  [x] docstring  [x] test
    # [x] getTemplateParameters           [x] impl  [x] docstring  [x] test
    # [x] getTi                           [x] impl  [x] docstring  [x] test
    # [x] getToolTipHTML                  [x] impl  [x] docstring  [x] test
    # [x] getUserDefinedMetaClass         [x] impl  [x] docstring  [x] test
    # [x] hasNestedElements               [x] impl  [x] docstring  [x] test
    # [x] hasPanelWidget                  [x] impl  [x] docstring  [x] test
    # [x] highLightElement                [x] impl  [x] docstring  [x] test
    # [x] isATemplate                     [x] impl  [x] docstring  [x] test
    # [x] isDescriptionRTF                [x] impl  [x] docstring  [x] test
    # [x] isDisplayNameRTF                [x] impl  [x] docstring  [x] test
    # [x] isModified                      [x] impl  [x] docstring  [x] test
    # [x] isRemote                        [x] impl  [x] docstring  [x] test
    # [x] locateInBrowser                 [x] impl  [x] docstring  [x] test
    # [x] openFeaturesDialog              [x] impl  [x] docstring  [x] test
    # [x] removeProperty                  [x] impl  [x] docstring  [x] test
    # [x] removeRedefines                 [x] impl  [x] docstring  [x] test
    # [x] removeStereotype                [x] impl  [x] docstring  [x] test
    # [x] setDecorationStyle              [x] impl  [x] docstring  [x] test
    # [x] setDescription                  [x] impl  [x] docstring  [x] test
    # [x] setDescriptionAndHyperlinks     [x] impl  [x] docstring  [x] test
    # [x] setDescriptionHTML              [x] impl  [x] docstring  [x] test
    # [x] setDescriptionRTF               [x] impl  [x] docstring  [x] test
    # [x] setDisplayName                  [x] impl  [x] docstring  [x] test
    # [x] setDisplayNameRTF               [x] impl  [x] docstring  [x] test
    # [x] setGUID                         [x] impl  [x] docstring  [x] test
    # [x] setIsShowDisplayName            [x] impl  [x] docstring  [x] test
    # [x] setMainDiagram                  [x] impl  [x] docstring  [x] test
    # [x] setName                         [x] impl  [x] docstring  [x] test   (already implemented)
    # [x] setOfTemplate                   [x] impl  [x] docstring  [x] test
    # [x] setOwner                        [x] impl  [x] docstring  [x] test
    # [x] setPropertyValue                [x] impl  [x] docstring  [x] test
    # [x] setRequirementTraceabilityHandle [x] impl  [x] docstring  [x] test
    # [x] setTagContextValue              [x] impl  [x] docstring  [x] test
    # [x] setTagElementValue              [x] impl  [x] docstring  [x] test
    # [x] setTagValue                     [x] impl  [x] docstring  [x] test
    # [x] setTi                           [x] impl  [x] docstring  [x] test
    # [x] synchronizeTemplateInstantiation [x] impl  [x] docstring  [x] test
    # [deprecated] getStereotype          - skipped (use getStereotypes)
    # [deprecated] setStereotype          - skipped (use addSpecificStereotype / addStereotype / removeStereotype)
    # [deprecated] lockOnDesignManager    - skipped (Design Manager removed in Rhapsody 8.4)
    # [deprecated] unlockOnDesignManager  - skipped (Design Manager removed in Rhapsody 8.4)

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getName(self) -> str:
        """Returns the name of the element.

        Returns:
            The element's name as a string.
        """
        return str(_get_method_or_property(self._com, "getName", "name"))

    def setName(self, name: str) -> None:
        """Sets the specified string as the name of the element.

        Args:
            name: The new name for the element.
        """
        _set_method_or_property(self._com, "setName", "name", name)

    def getMetaClass(self) -> str:
        """Gets the name of the metaclass on which the model element is based.

        Returns:
            The metaclass name as a string (e.g. ``"Class"``, ``"Package"``).
        """
        return str(_get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def getGUID(self) -> str:
        """Returns the GUID of the model element.

        Returns:
            The element's GUID as a string.
        """
        return str(_get_method_or_property(self._com, "getGUID", "GUID"))

    def addAssociation(self, end1: "RPModelElement", end2: "RPModelElement", name: str) -> "RPModelElement":
        """Creates an association class using the specified IRPRelation elements.

        Can only be called on elements that can contain association classes -
        packages and classes.

        Args:
            end1: The relation element at one end of the association.
            end2: The relation element at the second end of the association.
            name: The name to use for the new association class.

        Returns:
            The wrapped association class that was created.
        """
        return wrap(call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def addDependency(self, depends_on_name: str, depends_on_type: str) -> "RPModelElement":
        """Adds a dependency from the model element to the model element specified by the parameters.

        The method searches the model recursively until it finds an element
        that matches the name and metaclass specified. Since a model may
        contain multiple elements with the same name and type in different
        packages, prefer :meth:`addDependencyTo` when a specific element is
        available.

        Args:
            depends_on_name: The name of the model element on which this
                element depends.
            depends_on_type: The type (metaclass) of the model element on
                which this element depends.

        Returns:
            The wrapped dependency that was created.
        """
        return wrap(call_com(lambda: self._com.addDependency(depends_on_name, depends_on_type)))

    def addDependencyBetween(self, dependent: "RPModelElement", depends_on: "RPModelElement") -> "RPModelElement":
        """Creates a dependency between the two specified elements.

        In most cases :meth:`addDependencyTo` should be used. This method is
        useful when creating a dependency between two read-only elements and
        assigning ownership of the dependency to a third model element.

        Args:
            dependent: The model element that is dependent on the other.
            depends_on: The model element that the first element depends upon.

        Returns:
            The wrapped dependency that was created.
        """
        return wrap(call_com(lambda: self._com.addDependencyBetween(dependent._com, depends_on._com)))

    def addDependencyTo(self, element: "RPModelElement") -> "RPModelElement":
        """Adds a dependency upon another model element.

        Args:
            element: The model element that this element depends upon.

        Returns:
            The wrapped dependency that was created.
        """
        return wrap(call_com(lambda: self._com.addDependencyTo(element._com)))

    def addLinkToElement(
        self,
        to_element: "RPModelElement",
        assoc: "RPModelElement",
        from_port: "RPModelElement",
        to_port: "RPModelElement",
    ) -> "RPModelElement":
        """Creates a link between this model element and the model element specified as an argument.

        In addition to the other element to connect, you must specify either
        the association that the link should represent, or the two ports to
        use for the link. Pass ``None`` for the association when specifying
        ports, and ``None`` for the ports when specifying an association.

        Args:
            to_element: The model element that the link should connect to.
            assoc: The association that the link should represent.
            from_port: The "from" port for the link.
            to_port: The "to" port for the link.

        Returns:
            The wrapped link that was created.
        """
        return wrap(call_com(lambda: self._com.addLinkToElement(to_element._com, assoc._com, from_port._com, to_port._com)))

    def addNewAggr(self, meta_type: str, name: str) -> "RPModelElement":
        """Adds a new model element to the current element, for example, adding a class to a package.

        Args:
            meta_type: The metaclass of the new element to create.
            name: The name of the new element.

        Returns:
            The wrapped model element that was created.
        """
        return wrap(call_com(lambda: self._com.addNewAggr(meta_type, name)))

    def addProperty(self, property_key: str, property_type: str, property_value: str) -> None:
        """Adds a new property to the model element and assigns a value to it.

        Args:
            property_key: The key (name) of the property to add.
            property_type: The type of the property.
            property_value: The value to assign to the property.
        """
        call_com(lambda: self._com.addProperty(property_key, property_type, property_value))

    def addRedefines(self, new_redefine: "RPModelElement") -> None:
        """Adds a redefine relationship to the model element.

        Args:
            new_redefine: The model element to redefine.
        """
        call_com(lambda: self._com.addRedefines(new_redefine._com))

    def addRemoteDependencyTo(self, element: "RPModelElement", link_type: str) -> "RPModelElement":
        """For Design Manager projects, creates a dependency from a model element to a remote element.

        Args:
            element: The remote model element that this element depends upon.
            link_type: The type of link to create.

        Returns:
            The wrapped dependency that was created.
        """
        return wrap(call_com(lambda: self._com.addRemoteDependencyTo(element._com, link_type)))

    def addSpecificStereotype(self, stereotype: "RPModelElement") -> None:
        """Applies the specified stereotype to the model element.

        Args:
            stereotype: The wrapped stereotype to apply.
        """
        call_com(lambda: self._com.addSpecificStereotype(stereotype._com))

    def addStereotype(self, name: str, meta_type: str) -> "RPModelElement":
        """Applies the specified stereotype to the model element.

        The stereotype is applied only if the project contains a stereotype
        with the given name applicable to the given metaclass.

        Args:
            name: The name of the stereotype to apply.
            meta_type: The metaclass to which the stereotype applies.

        Returns:
            The wrapped stereotype that was applied.
        """
        return wrap(call_com(lambda: self._com.addStereotype(name, meta_type)))

    def becomeTemplateInstantiationOf(self, new_val: "RPModelElement") -> None:
        """Makes the current model element a template instantiation of the specified template.

        Args:
            new_val: The template to instantiate.
        """
        call_com(lambda: self._com.becomeTemplateInstantiationOf(new_val._com))

    def changeTo(self, meta_class: str) -> "RPModelElement":
        """Changes the model element to the type of element specified by the parameter provided.

        Args:
            meta_class: The metaclass to change this element into.

        Returns:
            The wrapped model element after the change.
        """
        return wrap(call_com(lambda: self._com.changeTo(meta_class)))

    def clone(self, name: str, new_owner: "RPModelElement") -> "RPModelElement":
        """Clones a model element.

        Args:
            name: The name to use for the cloned element.
            new_owner: The model element that should own the clone.

        Returns:
            The wrapped clone that was created.
        """
        return wrap(call_com(lambda: self._com.clone(name, new_owner._com)))

    def createOSLCLink(self, type: str, purl: str) -> None:
        """Creates an OSLC link between the element and the element represented by the specified URL.

        Args:
            type: The type of OSLC link to create.
            purl: The URL of the target element.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                createOSLCLink; the method is defined for Java API parity only.
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose createOSLCLink; method is defined for Java API parity only.")

    def deleteDependency(self, dependency: "RPModelElement") -> None:
        """Deletes the specified dependency from the model.

        Args:
            dependency: The wrapped dependency to delete.
        """
        call_com(lambda: self._com.deleteDependency(dependency._com))

    def deleteFromProject(self) -> None:
        """Deletes the current model element from the model."""
        call_com(lambda: self._com.deleteFromProject())

    def deleteOSLCLink(self, type: str, purl: str) -> None:
        """Deletes the specified OSLC link from the model.

        Args:
            type: The type of OSLC link to delete.
            purl: The URL of the target element.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                deleteOSLCLink; the method is defined for Java API parity only.
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose deleteOSLCLink; method is defined for Java API parity only.")

    def errorMessage(self) -> str:
        """Returns error message for last method called.

        Returns:
            The error message as a string.
        """
        return str(call_com(lambda: self._com.errorMessage()))

    def findElementsByFullName(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches for the specified model element in the specified path under the current model element.

        Args:
            name: The full path name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.
        """
        return wrap(call_com(lambda: self._com.findElementsByFullName(name, meta_class)))

    def findNestedElement(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches for the specified model element.

        Args:
            name: The name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.
        """
        return wrap(call_com(lambda: self._com.findNestedElement(name, meta_class)))

    def findNestedElementRecursive(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches recursively for the specified model element.

        Args:
            name: The name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.
        """
        return wrap(call_com(lambda: self._com.findNestedElementRecursive(name, meta_class)))

    def getAllTags(self) -> "RPCollection":
        """Returns a collection of all the element's tags.

        Returns:
            An ``RPCollection`` of the element's tags.
        """
        return RPCollection(call_com(lambda: self._com.getAllTags()))

    def getAnnotations(self) -> "RPCollection":
        """Returns all of the element's annotations.

        Returns:
            An ``RPCollection`` of the element's annotations.
        """
        return RPCollection(call_com(lambda: self._com.getAnnotations()))

    def getAssociationClasses(self) -> "RPCollection":
        """Returns a collection of all the association classes directly beneath this model element.

        Returns:
            An ``RPCollection`` of association classes.
        """
        return RPCollection(call_com(lambda: self._com.getAssociationClasses()))

    def getBinaryID(self) -> bytes:
        """Returns the GUID of the model element as an array of bytes.

        As opposed to :meth:`getGUID`, which returns the GUID as a string.

        Returns:
            The element's GUID as bytes.
        """
        return bytes(call_com(lambda: self._com.getBinaryID()))

    def getConstraints(self) -> "RPCollection":
        """Returns all of the element's constraints.

        Returns:
            An ``RPCollection`` of the element's constraints.
        """
        return RPCollection(call_com(lambda: self._com.getConstraints()))

    def getConstraintsByHim(self) -> "RPCollection":
        """Returns all of the element's constraints (for internal use only).

        Returns:
            An ``RPCollection`` of constraints.
        """
        return RPCollection(call_com(lambda: self._com.getConstraintsByHim()))

    def getControlledFiles(self) -> "RPCollection":
        """Returns a collection of all the element's controlled files.

        Returns:
            An ``RPCollection`` of controlled files.
        """
        return RPCollection(call_com(lambda: self._com.getControlledFiles()))

    def getDecorationStyle(self) -> str:
        """Returns the name of the decoration style currently associated with the model element.

        Returns:
            The decoration style name as a string.
        """
        return str(call_com(lambda: self._com.getDecorationStyle()))

    def getDependencies(self) -> "RPCollection":
        """Returns all of the element's dependencies.

        Returns:
            An ``RPCollection`` of the element's dependencies.
        """
        return RPCollection(call_com(lambda: self._com.getDependencies()))

    def getDescription(self) -> str:
        """Returns the description defined for the element.

        Returns:
            The element's description as a string.
        """
        return str(call_com(lambda: self._com.getDescription()))

    def getDescriptionHTML(self) -> str:
        """Returns HTML representation of the element description.

        Returns:
            The element's description as an HTML string.
        """
        return str(call_com(lambda: self._com.getDescriptionHTML()))

    def getDescriptionPlainText(self) -> str:
        """Returns the description defined for the element in plain text format.

        Returns:
            The element's description as plain text.
        """
        return str(call_com(lambda: self._com.getDescriptionPlainText()))

    def getDescriptionRTF(self) -> str:
        """Returns the description defined for the element in RTF format.

        Returns:
            The element's description as an RTF string.
        """
        return str(call_com(lambda: self._com.getDescriptionRTF()))

    def getDisplayName(self) -> str:
        """Returns the label of the model element.

        Returns:
            The element's display label as a string.
        """
        return str(call_com(lambda: self._com.getDisplayName()))

    def getDisplayNameRTF(self) -> str:
        """Returns the label of the model element as an RTF string.

        Returns:
            The element's display label as an RTF string.
        """
        return str(call_com(lambda: self._com.getDisplayNameRTF()))

    def getErrorMessage(self) -> str:
        """Returns error message for last method called.

        Returns:
            The error message as a string.
        """
        return str(call_com(lambda: self._com.getErrorMessage()))

    def getFullPathName(self) -> str:
        """Returns the full path name of the model element.

        Returns:
            The element's full path name as a string.
        """
        return str(call_com(lambda: self._com.getFullPathName()))

    def getFullPathNameIn(self) -> str:
        """Retrieves the full path name of the element as ``(class) in (package)``.

        Returns:
            The element's full path name as a string.
        """
        return str(call_com(lambda: self._com.getFullPathNameIn()))

    def getHyperLinks(self) -> "RPCollection":
        """Returns a collection of all the hyperlinks associated with the element.

        Returns:
            An ``RPCollection`` of hyperlinks.
        """
        return RPCollection(call_com(lambda: self._com.getHyperLinks()))

    def getIconFileName(self) -> str:
        """Returns the full path of the graphic file used to represent elements of this type in the browser.

        Returns:
            The icon file path as a string.
        """
        return str(call_com(lambda: self._com.getIconFileName()))

    def getInterfaceName(self) -> str:
        """Returns the name of the API interface corresponding to the current element.

        For example, ``"IRPClass"`` for a class element, ``"IRPOperation"``
        for an operation element.

        Returns:
            The API interface name as a string.
        """
        return str(call_com(lambda: self._com.getInterfaceName()))

    def getIsExternal(self) -> int:
        """Checks whether the element is an "external" element.

        Corresponds to the value of the property ``UseAsExternal``.

        Returns:
            ``1`` if the element is external, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.getIsExternal()))

    def getIsOfMetaClass(self, meta_class: str) -> int:
        """Indicates whether the model element is based on the metaclass provided as a parameter.

        Args:
            meta_class: The metaclass name to check against.

        Returns:
            ``1`` if the element is based on the metaclass, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.getIsOfMetaClass(meta_class)))

    def getIsShowDisplayName(self) -> int:
        """Checks whether the model element is configured to display its label instead of its name in diagrams.

        Returns:
            ``1`` if the label is shown, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.getIsShowDisplayName()))

    def getIsUnresolved(self) -> int:
        """Checks if the element is an element that can't be resolved by Rhapsody.

        Returns:
            ``1`` if the element is unresolved, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.getIsUnresolved()))

    def getLocalTags(self) -> "RPCollection":
        """Returns a collection of the tags that were created locally for this model element.

        Returns:
            An ``RPCollection`` of locally created tags.
        """
        return RPCollection(call_com(lambda: self._com.getLocalTags()))

    def getMainDiagram(self) -> "RPModelElement":
        """Returns the "main" diagram for the element.

        Returns:
            The wrapped main diagram.
        """
        return wrap(call_com(lambda: self._com.getMainDiagram()))

    def getNestedElements(self) -> "RPCollection":
        """Gets a collection of all the model elements that are directly under the current element.

        Returns:
            An ``RPCollection`` of nested model elements.
        """
        return RPCollection(call_com(lambda: self._com.getNestedElements()))

    def getNestedElementsByMetaClass(self, meta_class: str, recursive: int) -> "RPCollection":
        """Retrieves all of the model elements of the specified type below the current element.

        Args:
            meta_class: The metaclass of the elements to retrieve.
            recursive: ``1`` to search recursively, ``0`` for direct children only.

        Returns:
            An ``RPCollection`` of matching nested elements.
        """
        return RPCollection(call_com(lambda: self._com.getNestedElementsByMetaClass(meta_class, recursive)))

    def getNestedElementsRecursive(self) -> "RPCollection":
        """Returns a collection that consists of the current element and all of the model elements below it.

        Returns:
            An ``RPCollection`` of this element and all nested elements.
        """
        return RPCollection(call_com(lambda: self._com.getNestedElementsRecursive()))

    def getNewTermStereotype(self) -> "RPModelElement":
        """If a "new term" stereotype has been applied to the element, returns the stereotype.

        Returns:
            The wrapped "new term" stereotype.
        """
        return wrap(call_com(lambda: self._com.getNewTermStereotype()))

    def getOfTemplate(self) -> "RPModelElement":
        """If the element is an instantiation of a template, returns the template that it instantiates.

        Returns:
            The wrapped template that this element instantiates.
        """
        return wrap(call_com(lambda: self._com.getOfTemplate()))

    def getOSLCLinks(self) -> "RPCollection":
        """Returns a collection of all the element's OSLC links.

        Returns:
            An ``RPCollection`` of OSLC links.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                getOSLCLinks; the method is defined for Java API parity only.
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose getOSLCLinks; method is defined for Java API parity only.")

    def getOverlayIconFileName(self) -> str:
        """Returns the full path of the graphic file used as an overlay on this specific model element.

        The overlay is drawn on top of the regular icon that represents
        elements of this type in the browser.

        Returns:
            The overlay icon file path as a string.
        """
        return str(call_com(lambda: self._com.getOverlayIconFileName()))

    def getOverriddenProperties(self, recursive: int) -> "RPCollection":
        """Returns a collection of all the properties whose value was overridden for this model element.

        Args:
            recursive: ``1`` to include overridden properties of nested
                elements, ``0`` for this element only.

        Returns:
            An ``RPCollection`` of overridden properties.
        """
        return RPCollection(call_com(lambda: self._com.getOverriddenProperties(recursive)))

    def getOverriddenPropertiesByPattern(self, pattern: str, localy_overriden_only: int, with_default_values: int) -> "RPCollection":
        """Returns the overridden properties matching the specified pattern.

        Args:
            pattern: The pattern to match property keys against.
            localy_overriden_only: ``1`` to return only locally overridden
                properties, ``0`` otherwise.
            with_default_values: ``1`` to include default values, ``0`` otherwise.

        Returns:
            An ``RPCollection`` of matching overridden properties.
        """
        return RPCollection(call_com(lambda: self._com.getOverriddenPropertiesByPattern(pattern, localy_overriden_only, with_default_values)))

    def getOwnedDependencies(self) -> "RPCollection":
        """Returns all of the dependencies that are owned by the element.

        Returns:
            An ``RPCollection`` of owned dependencies.
        """
        return RPCollection(call_com(lambda: self._com.getOwnedDependencies()))

    def getOwner(self) -> "RPModelElement":
        """Returns the model element that owns this model element.

        Returns:
            The wrapped owner element.
        """
        return wrap(call_com(lambda: self._com.getOwner()))

    def getProject(self) -> "RPModelElement":
        """Returns the project that the current element belongs to.

        Returns:
            The wrapped project element.
        """
        return wrap(call_com(lambda: self._com.getProject()))

    def getPropertyValue(self, property_key: str) -> str:
        """Returns the value of the specified property for the model element.

        Args:
            property_key: The key (name) of the property.

        Returns:
            The property value as a string.
        """
        return str(call_com(lambda: self._com.getPropertyValue(property_key)))

    def getPropertyValueConditional(self, property_key: str, formal_key: "RPCollection", actual_values: "RPCollection") -> str:
        """Returns the value of the specified property, taking into account the tokens and token values specified.

        Args:
            property_key: The key (name) of the property.
            formal_key: A collection of formal tokens.
            actual_values: A collection of token values.

        Returns:
            The property value as a string.
        """
        return str(call_com(lambda: self._com.getPropertyValueConditional(property_key, formal_key._com, actual_values._com)))

    def getPropertyValueConditionalExplicit(self, property_key: str, formal_key: "RPCollection", actual_values: "RPCollection") -> str:
        """Returns the property value if overridden, taking into account the tokens and token values specified.

        Args:
            property_key: The key (name) of the property.
            formal_key: A collection of formal tokens.
            actual_values: A collection of token values.

        Returns:
            The property value as a string.
        """
        return str(call_com(lambda: self._com.getPropertyValueConditionalExplicit(property_key, formal_key._com, actual_values._com)))

    def getPropertyValueExplicit(self, property_key: str) -> str:
        """Returns the value of the specified property if the default value was overridden.

        Args:
            property_key: The key (name) of the property.

        Returns:
            The property value as a string.
        """
        return str(call_com(lambda: self._com.getPropertyValueExplicit(property_key)))

    def getRedefines(self) -> "RPCollection":
        """Returns the redefine relationships of the model element.

        Returns:
            An ``RPCollection`` of redefine relationships.
        """
        return RPCollection(call_com(lambda: self._com.getRedefines()))

    def getReferences(self) -> "RPCollection":
        """Returns a collection of all the model elements that point to this model element.

        Returns:
            An ``RPCollection`` of referencing elements.
        """
        return RPCollection(call_com(lambda: self._com.getReferences()))

    def getRemoteDependencies(self) -> "RPCollection":
        """For Rhapsody Model Manager projects, returns the dependencies on remote artifacts.

        Returns:
            An ``RPCollection`` of remote dependencies.
        """
        return RPCollection(call_com(lambda: self._com.getRemoteDependencies()))

    def getRemoteURI(self) -> str:
        """For elements that are remote resources, returns the URI of the resource.

        Returns:
            The remote URI as a string.
        """
        return str(call_com(lambda: self._com.getRemoteURI()))

    def getRequirementTraceabilityHandle(self) -> int:
        """Returns the ID used by DOORS to refer to this requirement.

        Returns:
            The DOORS traceability handle as an int.
        """
        return int(call_com(lambda: self._com.getRequirementTraceabilityHandle()))

    def getRmmUrl(self) -> str:
        """Returns the Rhapsody Model Manager url for the model element.

        Returns:
            The RMM URL as a string.
        """
        return str(call_com(lambda: self._com.getRmmUrl()))

    def getSaveUnit(self) -> "RPModelElement":
        """Returns the unit that the model element is saved in.

        Returns:
            The wrapped save unit.
        """
        return wrap(call_com(lambda: self._com.getSaveUnit()))

    def getStereotypes(self) -> "RPCollection":
        """Returns a collection of the stereotypes that have been applied to the element.

        Returns:
            An ``RPCollection`` of applied stereotypes.
        """
        return RPCollection(call_com(lambda: self._com.getStereotypes()))

    def getTag(self, name: str) -> "RPModelElement":
        """Returns the tag specified.

        Args:
            name: The name of the tag to return.

        Returns:
            The wrapped tag.
        """
        return wrap(call_com(lambda: self._com.getTag(name)))

    def getTemplateParameters(self) -> "RPCollection":
        """For model elements that are templates, returns the template parameters.

        Returns:
            An ``RPCollection`` of template parameters.
        """
        return RPCollection(call_com(lambda: self._com.getTemplateParameters()))

    def getTi(self) -> "RPModelElement":
        """For template instantiations, returns an object containing the template instantiation parameters.

        Returns:
            The wrapped template instantiation.
        """
        return wrap(call_com(lambda: self._com.getTi()))

    def getToolTipHTML(self) -> str:
        """Returns the HTML that would be used to display the tooltip for the element in the user interface.

        Returns:
            The tooltip HTML as a string.
        """
        return str(call_com(lambda: self._com.getToolTipHTML()))

    def getUserDefinedMetaClass(self) -> str:
        """Gets the name of the New Term on which the model element is based.

        Returns:
            The user-defined metaclass name as a string.
        """
        return str(call_com(lambda: self._com.getUserDefinedMetaClass()))

    def hasNestedElements(self) -> int:
        """Checks whether the model element contains other elements.

        Returns:
            ``1`` if the element contains nested elements, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.hasNestedElements()))

    def hasPanelWidget(self) -> int:
        """Checks whether the model element is bound to a panel diagram widget.

        Returns:
            ``1`` if bound to a panel widget, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.hasPanelWidget()))

    def highLightElement(self) -> None:
        """Locates the element in the Rhapsody browser, and highlights it in the diagram where it appears."""
        call_com(lambda: self._com.highLightElement())

    def isATemplate(self) -> int:
        """Checks whether the model element is a template.

        Returns:
            ``1`` if the element is a template, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isATemplate()))

    def isDescriptionRTF(self) -> int:
        """Checks whether the description for the element is in RTF format.

        Returns:
            ``1`` if the description is RTF, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isDescriptionRTF()))

    def isDisplayNameRTF(self) -> int:
        """Checks whether the label of the element is in RTF format.

        Returns:
            ``1`` if the label is RTF, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isDisplayNameRTF()))

    def isModified(self) -> int:
        """Checks if the element was modified since the model was last saved.

        Returns:
            ``1`` if the element was modified, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isModified()))

    def isRemote(self) -> int:
        """Checks whether the model element is a remote resource such as a DOORS/DOORS Next requirement.

        Returns:
            ``1`` if the element is remote, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isRemote()))

    def locateInBrowser(self) -> int:
        """Locates the model element in the Rhapsody browser.

        Returns:
            ``1`` if the element was located, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.locateInBrowser()))

    def openFeaturesDialog(self, new_dialog: int) -> None:
        """Displays the information for the element in the Features window.

        Args:
            new_dialog: ``1`` to open in a new dialog, ``0`` otherwise.
        """
        call_com(lambda: self._com.openFeaturesDialog(new_dialog))

    def removeProperty(self, property_key: str) -> None:
        """Removes the value that was set for the specified property.

        Args:
            property_key: The key (name) of the property to remove.
        """
        call_com(lambda: self._com.removeProperty(property_key))

    def removeRedefines(self, removed_redefine: "RPModelElement") -> None:
        """Removes a redefine relationship from the model element.

        Args:
            removed_redefine: The redefine relationship to remove.
        """
        call_com(lambda: self._com.removeRedefines(removed_redefine._com))

    def removeStereotype(self, stereotype: "RPModelElement") -> None:
        """Removes the specified stereotype from the element.

        Args:
            stereotype: The wrapped stereotype to remove.
        """
        call_com(lambda: self._com.removeStereotype(stereotype._com))

    def setDecorationStyle(self, new_val: str) -> None:
        """Specifies the decoration style that should now be associated with the model element.

        Args:
            new_val: The decoration style name to associate.
        """
        call_com(lambda: self._com.setDecorationStyle(new_val))

    def setDescription(self, description: str) -> None:
        """Sets the specified string as the description of the element.

        Args:
            description: The description text to set.
        """
        call_com(lambda: self._com.setDescription(description))

    def setDescriptionAndHyperlinks(self, rtf_text: str, targets: "RPCollection") -> None:
        """Specifies an RTF description for the element and a collection of elements to hyperlink.

        Args:
            rtf_text: The RTF string to use as the description.
            targets: A collection of elements to which hyperlinks should be created.
        """
        call_com(lambda: self._com.setDescriptionAndHyperlinks(rtf_text, targets._com))

    def setDescriptionHTML(self, description_html: str) -> None:
        """Sets the HTML representation of the element description.

        Note: the Java API documents this method as not implemented.

        Args:
            description_html: The HTML description to set.
        """
        call_com(lambda: self._com.setDescriptionHTML(description_html))

    def setDescriptionRTF(self, description_rtf: str) -> None:
        """Specifies the RTF string to use for the description of the model element.

        Args:
            description_rtf: The RTF description to set.
        """
        call_com(lambda: self._com.setDescriptionRTF(description_rtf))

    def setDisplayName(self, display_name: str) -> None:
        """Specifies the text to use for the label of the model element.

        Args:
            display_name: The label text to set.
        """
        call_com(lambda: self._com.setDisplayName(display_name))

    def setDisplayNameRTF(self, new_val: str) -> None:
        """Specifies the RTF string to use for the label of the model element.

        Args:
            new_val: The RTF label text to set.
        """
        call_com(lambda: self._com.setDisplayNameRTF(new_val))

    def setGUID(self, guid: str) -> None:
        """Sets a new GUID for the model element.

        Args:
            guid: The new GUID to set.
        """
        call_com(lambda: self._com.setGUID(guid))

    def setIsShowDisplayName(self, is_show_display_name: int) -> None:
        """Specifies whether the label of the element should be displayed instead of the element name in diagrams.

        Args:
            is_show_display_name: ``1`` to show the label, ``0`` to show the name.
        """
        call_com(lambda: self._com.setIsShowDisplayName(is_show_display_name))

    def setMainDiagram(self, main_diagram: "RPModelElement") -> None:
        """Specifies the "main" diagram for the element.

        Args:
            main_diagram: The wrapped diagram to set as the main diagram.
        """
        call_com(lambda: self._com.setMainDiagram(main_diagram._com))

    def setOfTemplate(self, of_template: "RPModelElement") -> None:
        """Makes the current model element a template instantiation of the specified template.

        Args:
            of_template: The wrapped template to instantiate.
        """
        call_com(lambda: self._com.setOfTemplate(of_template._com))

    def setOwner(self, owner: "RPModelElement") -> None:
        """Specifies the model element that should be the owner of this element.

        Args:
            owner: The wrapped element that should own this element.
        """
        call_com(lambda: self._com.setOwner(owner._com))

    def setPropertyValue(self, property_key: str, property_value: str) -> None:
        """Sets the value of a property for the model element.

        Args:
            property_key: The key (name) of the property.
            property_value: The value to assign to the property.
        """
        call_com(lambda: self._com.setPropertyValue(property_key, property_value))

    def setRequirementTraceabilityHandle(self, requirement_traceability_handle: int) -> None:
        """Sets a new ID to be used to reference this requirement.

        Args:
            requirement_traceability_handle: The new DOORS traceability handle.
        """
        call_com(lambda: self._com.setRequirementTraceabilityHandle(requirement_traceability_handle))

    def setTagContextValue(self, tag: "RPModelElement", elements: "RPCollection", multiplicities: "RPCollection") -> "RPModelElement":
        """Applies the specified tag and sets its value to a specific instance of another model element.

        Args:
            tag: The wrapped tag to apply.
            elements: A collection of model elements.
            multiplicities: A collection of multiplicities.

        Returns:
            The wrapped tag that was set.
        """
        return wrap(call_com(lambda: self._com.setTagContextValue(tag._com, elements._com, multiplicities._com)))

    def setTagElementValue(self, tag: "RPModelElement", val: "RPModelElement") -> "RPModelElement":
        """Applies a tag whose type is a model element to the current element with the value specified.

        Args:
            tag: The wrapped tag to apply.
            val: The wrapped model element value.

        Returns:
            The wrapped tag that was set.
        """
        return wrap(call_com(lambda: self._com.setTagElementValue(tag._com, val._com)))

    def setTagValue(self, tag: "RPModelElement", val: str) -> "RPModelElement":
        """Applies the specified tag to the model element with the value specified.

        Args:
            tag: The wrapped tag to apply.
            val: The value to assign to the tag.

        Returns:
            The wrapped tag that was set.
        """
        return wrap(call_com(lambda: self._com.setTagValue(tag._com, val)))

    def setTi(self, ti: "RPModelElement") -> None:
        """Sets the template instantiation for the model element (for internal use only).

        Args:
            ti: The wrapped template instantiation to set.
        """
        call_com(lambda: self._com.setTi(ti._com))

    def synchronizeTemplateInstantiation(self) -> None:
        """Updates the instantiation to match changes made to its template.

        After changes are made to a template, this method can be called on
        each instantiation of the template in order to update the
        instantiation to match the changes that were made to the template.
        """
        call_com(lambda: self._com.synchronizeTemplateInstantiation())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RPModelElement):
            return NotImplemented
        return bool(self._com == other._com)

    def __hash__(self) -> int:
        return hash(id(self._com))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.getName()!r})"


class AddToModelMode(IntEnum):
    """Constant values mirroring ``IRPApplication.AddToModel_Mode``.

    Returned by :meth:`RPUnit.getAddToModelMode` to indicate how a unit was
    added to the model. ``IntEnum`` so callers may compare the raw ``int``
    returned by the COM call directly against these constants.
    """

    AS_REFERENCE = 0
    AS_UNIT_WITH_COPY = 1
    AS_UNIT_WITHOUT_COPY = 2


# IRPUnit method parity checklist:
# [x] copyToAnotherProject                [x] impl  [x] docstring  [x] test
# [x] getAddToModelMode                   [x] impl  [x] docstring  [x] test
# [x] getCMHeader                         [x] impl  [x] docstring  [x] test
# [x] getCMState                          [x] impl  [x] docstring  [x] test
# [x] getCurrentDirectory                 [x] impl  [x] docstring  [x] test
# [x] getFilename                         [x] impl  [x] docstring  [x] test  (pre-existing)
# [x] getIncludeInNextLoad                [x] impl  [x] docstring  [x] test
# [x] getIsStub                           [x] impl  [x] docstring  [x] test
# [x] getLanguage                         [x] impl  [x] docstring  [x] test
# [x] getLastModifiedTime                 [x] impl  [x] docstring  [x] test
# [x] getNestedSaveUnits                  [x] impl  [x] docstring  [x] test
# [x] getNestedSaveUnitsCount             [x] impl  [x] docstring  [x] test
# [x] getStructureDiagrams                [x] impl  [x] docstring  [x] test
# [x] getUnitPath                         [x] impl  [x] docstring  [x] test
# [x] isReadOnly                          [x] impl  [x] docstring  [x] test  (pre-existing)
# [x] isReferenceUnit                     [x] impl  [x] docstring  [x] test
# [x] isSeparateSaveUnit                  [x] impl  [x] docstring  [x] test
# [x] load                                [x] impl  [x] docstring  [x] test
# [x] moveToAnotherProjectLeaveAReference [x] impl  [x] docstring  [x] test
# [x] referenceToAnotherProject           [x] impl  [x] docstring  [x] test
# [x] save                                [x] impl  [x] docstring  [x] test  (pre-existing)
# [x] setCMHeader                         [x] impl  [x] docstring  [x] test
# [x] setFilename                         [x] impl  [x] docstring  [x] test  (pre-existing)
# [x] setIncludeInNextLoad                [x] impl  [x] docstring  [x] test
# [x] setLanguage                         [x] impl  [x] docstring  [x] test
# [x] setReadOnly                         [x] impl  [x] docstring  [x] test  (pre-existing)
# [x] setSeparateSaveUnit                 [x] impl  [x] docstring  [x] test
# [x] setUnitPath                         [x] impl  [x] docstring  [x] test
# [x] unload                              [x] impl  [x] docstring  [x] test
# [inherited] getNestedElements - provided by RPModelElement
# No deprecated IRPUnit methods.
class RPUnit(RPModelElement):
    """Wraps ``IRPUnit``: model elements that can be saved as separate files."""

    def copyToAnotherProject(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Makes an editable copy of the unit in a different project.

        Args:
            parent_in_target: The model element that will be the parent of the
                new unit in the target project.

        Returns:
            The wrapped unit that was created in the target project.
        """
        return wrap(call_com(lambda: self._com.copyToAnotherProject(parent_in_target._com)))

    def getAddToModelMode(self) -> int:
        """Returns an indication of how the unit was added to the model.

        The returned value corresponds to one of the :class:`AddToModelMode`
        constants.

        Returns:
            A value indicating how the unit was added to the model (see
            :class:`AddToModelMode`).
        """
        return int(call_com(lambda: self._com.getAddToModelMode()))

    def getCMHeader(self) -> str:
        """Returns the header used by the Configuration Management tool for the unit.

        Returns:
            The Configuration Management tool header as a string.
        """
        return str(call_com(lambda: self._com.getCMHeader()))

    def getCMState(self) -> int:
        """Returns the configuration management state of the unit.

        Returns:
            The configuration management state of the unit.
        """
        return int(call_com(lambda: self._com.getCMState()))

    def getCurrentDirectory(self) -> str:
        """Gets the name of the directory that contains the file used to store the unit.

        The string returned consists of the full path except for the name of
        the file itself.

        Returns:
            The name of the directory that contains the file used to store the unit.
        """
        return str(call_com(lambda: self._com.getCurrentDirectory()))

    def getFilename(self) -> str:
        """Gets the name of the file used to store the unit.

        The string returned consists only of the filename, not the entire path.

        Returns:
            The name of the file used to store the unit.
        """
        return str(_get_method_or_property(self._com, "getFilename", "filename"))

    def getIncludeInNextLoad(self) -> int:
        """Checks whether the unit is going to be loaded the next time the model is loaded.

        Returns:
            ``1`` if the unit is going to be loaded the next time the model is
            loaded, ``0`` if it is not.
        """
        return int(call_com(lambda: self._com.getIncludeInNextLoad()))

    def getIsStub(self) -> int:
        """Checks whether the unit is currently unloaded.

        Returns:
            ``1`` if the unit is not currently loaded, ``0`` if it is currently loaded.
        """
        return int(call_com(lambda: self._com.getIsStub()))

    def getLanguage(self) -> str:
        """Gets the language of the unit.

        Returns:
            The language of the unit as a string.
        """
        return str(call_com(lambda: self._com.getLanguage()))

    def getLastModifiedTime(self) -> str:
        """Returns the time at which the file representing the unit was last modified.

        Returns:
            The last modified time as a string.
        """
        return str(call_com(lambda: self._com.getLastModifiedTime()))

    def getNestedSaveUnits(self) -> "RPCollection":
        """Returns a collection of any sub-elements of the unit that were saved as individual files.

        Returns:
            An ``RPCollection`` of sub-elements that were saved as individual files.
        """
        return RPCollection(call_com(lambda: self._com.getNestedSaveUnits()))

    def getNestedSaveUnitsCount(self) -> int:
        """Returns the number of sub-elements of the unit that were saved as individual files.

        Returns:
            The number of sub-elements that were saved as individual files.
        """
        return int(call_com(lambda: self._com.getNestedSaveUnitsCount()))

    def getStructureDiagrams(self) -> "RPCollection":
        """Returns a collection of any structure diagrams that are sub-elements of the unit.

        Used primarily for structure diagrams that belong to individual classes.

        Returns:
            An ``RPCollection`` of structure diagrams that are sub-elements of the unit.
        """
        return RPCollection(call_com(lambda: self._com.getStructureDiagrams()))

    def getUnitPath(self, b_full_path: int) -> str:
        """Returns the path of the unit, including the filename.

        Args:
            b_full_path: ``1`` to return the full path, ``0`` to return a
                relative path. For relative paths, the path returned is relative
                to the saved unit that owns this unit.

        Returns:
            The path of the unit, including the filename.
        """
        return str(call_com(lambda: self._com.getUnitPath(b_full_path)))

    def isReadOnly(self) -> bool:
        """Checks whether the file used to store the unit is read-only.

        Returns:
            ``True`` if the file is read-only, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.isReadOnly()))

    def isReferenceUnit(self) -> int:
        """Checks whether the unit was added to the model as a reference.

        Returns:
            ``1`` if the unit was added to the model as a reference, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isReferenceUnit()))

    def isSeparateSaveUnit(self) -> int:
        """Checks whether the current IRPUnit object is saved in its own file.

        ``IRPUnit`` objects represent any element that can in theory be saved
        as a separate file, even if this is not the case for a specific element
        in your model.

        Returns:
            ``1`` if the unit is saved in its own file, ``0`` otherwise.
        """
        return int(call_com(lambda: self._com.isSeparateSaveUnit()))

    def load(self, with_subs: int) -> "RPModelElement":
        """Loads the unit.

        Args:
            with_subs: ``1`` to load the unit's subunits as well, ``0`` to load
                only the unit itself.

        Returns:
            The wrapped unit that was loaded.
        """
        return wrap(call_com(lambda: self._com.load(with_subs)))

    def moveToAnotherProjectLeaveAReference(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Moves the unit to a different project, and adds a reference to it in the original project.

        Args:
            parent_in_target: The model element that will be the parent of the
                new unit in the target project.

        Returns:
            The wrapped unit that was created in the target project.
        """
        return wrap(call_com(lambda: self._com.moveToAnotherProjectLeaveAReference(parent_in_target._com)))

    def referenceToAnotherProject(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Creates a reference to the unit in a different project.

        Args:
            parent_in_target: The model element that will be the parent of the
                reference (read-only) unit created in the target project.

        Returns:
            The wrapped reference (read-only) unit that was created in the target project.
        """
        return wrap(call_com(lambda: self._com.referenceToAnotherProject(parent_in_target._com)))

    def save(self) -> None:
        """Saves the unit."""
        call_com(lambda: self._com.save())

    def setCMHeader(self, cm_header: str) -> None:
        """Sets the Configuration Management tool header for the unit.

        Args:
            cm_header: The Configuration Management tool header to use for the unit.
        """
        call_com(lambda: self._com.setCMHeader(cm_header))

    def setFilename(self, filename: str) -> None:
        """Specifies the name that should be used for the file representing the unit.

        The string should only include the first part of the filename;
        Rhapsody handles the file extension. Note that if you change the
        filename, the old file remains on disk.

        Args:
            filename: The name that should be used for the file representing the unit.
        """
        _set_method_or_property(self._com, "setFilename", "filename", filename)

    def setIncludeInNextLoad(self, include_in_next_load: int) -> None:
        """Toggles whether the unit is going to be loaded the next time the model is loaded.

        Args:
            include_in_next_load: ``1`` to load the unit the next time the model
                is loaded, ``0`` to not load it.
        """
        call_com(lambda: self._com.setIncludeInNextLoad(include_in_next_load))

    def setLanguage(self, new_language: str, recursive: int) -> None:
        """Specifies the programming language that should be used when code is generated for the unit.

        This method can be used for mixed-language models.

        Args:
            new_language: One of ``"C++"``/``"cpp"``, ``"C"``, ``"Java"``,
                ``"Ada"``, or ``"C#"``.
            recursive: ``1`` to set the language for all subunits of the
                element, ``0`` otherwise.
        """
        call_com(lambda: self._com.setLanguage(new_language, recursive))

    def setReadOnly(self, read_only: bool) -> None:
        """Toggles the read-only status of the file used to store the unit.

        Args:
            read_only: ``True`` to change the file to read-only, ``False`` to
                change the file to read/write.
        """
        call_com(lambda: self._com.setReadOnly(1 if read_only else 0))

    def setSeparateSaveUnit(self, p_val: int) -> None:
        """Specifies whether the current IRPUnit object should be saved in its own file.

        Args:
            p_val: ``1`` to save the element in its own file, ``0`` to not save
                it in its own file.
        """
        call_com(lambda: self._com.setSeparateSaveUnit(p_val))

    def setUnitPath(self, new_path: str) -> None:
        """Specifies the path that should be used to locate the unit when it is added to a model "By Reference".

        Args:
            new_path: The path that should be used to locate the unit when it is
                added to a model "By Reference".
        """
        call_com(lambda: self._com.setUnitPath(new_path))

    def unload(self) -> None:
        """Unloads the unit."""
        call_com(lambda: self._com.unload())


class RPCollection:
    """Wraps ``IRPCollection``: an iterable/indexable container of elements."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getCount(self) -> int:
        return int(_get_method_or_property(self._com, "getCount", "Count"))

    def getItem(self, index: int) -> Any:
        if hasattr(self._com, "getItem"):
            raw_item = call_com(lambda: self._com.getItem(index))
        else:
            raw_item = call_com(lambda: self._com.Item(index))
        return _wrap_if_element(raw_item)

    def addItem(self, element: RPModelElement) -> None:
        call_com(lambda: self._com.addItem(element._com))

    def __len__(self) -> int:
        return self.getCount()

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            raise IndexError("negative indices are not supported")
        return self.getItem(index + 1)

    def __iter__(self) -> Iterator[Any]:
        for index in range(1, len(self) + 1):
            yield self.getItem(index)
