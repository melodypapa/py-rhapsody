"""Core wrapping machinery shared by all rhapsody_cli element wrappers.

``AbstractRPModelElement.call_com()`` translates COM failures into ``RhapsodyRuntimeException``.
``AbstractRPModelElement`` is the abstract base class providing common utilities.
``RPModelElement`` is the base interface for every wrapped Rhapsody model
element, mirroring ``com.telelogic.rhapsody.core.IRPModelElement``.
``AbstractRPModelElement.wrap()`` dispatches a raw COM object to its matching wrapper class using
a registry populated by each element module at import time.
"""

from enum import IntEnum
from typing import Any, Callable, Dict, Iterator, Type, TypeVar

from rhapsody_cli import com_utils

T = TypeVar("T")


class AbstractRPModelElement:
    """Abstract base class providing common utilities for all Rhapsody element wrappers.

    Implements class methods for COM interaction, element wrapping, and registry management.
    """

    #: Maps a Rhapsody ``getMetaClass()`` string (e.g. "Class", "Package") to the
    #: wrapper class that should represent it. Populated by each element module
    #: at import time via ``register_wrapper``. Unmapped meta classes fall back
    #: to ``RPModelElement`` in ``AbstractRPModelElement.wrap()``.
    _WRAPPER_REGISTRY: Dict[str, Type["RPModelElement"]] = {}

    @classmethod
    def register_wrapper(cls, meta_class: str, wrapper_cls: Type["RPModelElement"]) -> None:
        """Register ``wrapper_cls`` as the wrapper for COM objects of ``meta_class``."""
        cls._WRAPPER_REGISTRY[meta_class] = wrapper_cls

    @classmethod
    def call_com(cls, func: Callable[[], T]) -> T:
        """Invoke a COM call, translating COM errors into RhapsodyRuntimeException.

        Forwards to :func:`rhapsody_cli.com_utils.call_com`.
        """
        return com_utils.call_com(func)

    @classmethod
    def _wrap_if_element(cls, value: Any) -> Any:
        """Wrap ``value`` if it looks like a Rhapsody model element."""
        if hasattr(value, "getMetaClass") or hasattr(value, "metaClass"):
            return cls.wrap(value)
        return value

    @classmethod
    def wrap(cls, com_obj: Any) -> "RPModelElement":
        """Wrap a raw Rhapsody COM model element in its matching wrapper class.

        Returns an RPModelElement wrapping a None COM object if com_obj is None
        (e.g., when findNestedElement returns no result).
        """
        if com_obj is None:
            return RPModelElement(None)
        meta_class = str(cls._get_method_or_property(com_obj, "getMetaClass", "metaClass"))
        wrapper_cls = cls._WRAPPER_REGISTRY.get(meta_class, RPModelElement)
        return wrapper_cls(com_obj)

    @classmethod
    def _get_method_or_property(cls, com_obj: Any, method_name: str, prop_name: str) -> Any:
        """Read a value from ``com_obj``, preferring the Java-style method.

        Forwards to :func:`rhapsody_cli.com_utils._get_method_or_property`.
        """
        return com_utils._get_method_or_property(com_obj, method_name, prop_name)

    @classmethod
    def _set_method_or_property(cls, com_obj: Any, method_name: str, prop_name: str, value: Any) -> None:
        """Write a value to ``com_obj``, preferring the Java-style setter method.

        Forwards to :func:`rhapsody_cli.com_utils._set_method_or_property`.
        """
        com_utils._set_method_or_property(com_obj, method_name, prop_name, value)


class RPModelElement(AbstractRPModelElement):
    """Wraps ``IRPModelElement``: the base interface for all model elements.

    Method names use snake_case (``get_name``, ``set_name``,
    ``get_meta_class``, ``get_guid``, ...). Internal COM calls preserve
    the camelCase API (``self._com.methodName(...)``). Some Rhapsody COM
    Prog IDs expose these as bare properties instead of methods; see
    :func:`_get_method_or_property`.
    """

    # IRPModelElement method parity checklist:
    # [x] add_association                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_dependency                   [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_dependency_between            [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_dependency_to                 [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_link_to_element                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_new_aggr                      [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_property                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_redefines                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] add_remote_dependency_to           [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_specific_stereotype           [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_stereotype                   [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] become_template_instantiation_of   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] change_to                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] clone                           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] create_oslc_link                  [x] impl  [x] docstring  [x] unit test  [ ] integration test  (NotImplementedError)
    # [x] delete_dependency                [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_from_project               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_oslc_link                  [x] impl  [x] docstring  [x] unit test  [ ] integration test  (NotImplementedError)
    # [x] error_message                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_elements_by_full_name          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_nested_element               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] find_nested_element_recursive      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_all_tags                      [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_annotations                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_association_classes           [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_binary_id                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_constraints                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_constraints_by_him             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_controlled_files              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_decoration_style              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_dependencies                 [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_description                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_description_html              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_description_plain_text         [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_description_rtf               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_display_name                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_display_name_rtf               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_error_message                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_full_path_name                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_full_path_name_in               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_guid                         [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_hyper_links                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_icon_file_name                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_interface_name                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_external                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_of_meta_class                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_show_display_name            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_unresolved                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_local_tags                    [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_main_diagram                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_meta_class                    [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_name                         [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_nested_elements               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_nested_elements_by_meta_class    [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_nested_elements_recursive      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_new_term_stereotype            [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_of_template                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_oslc_links                    [x] impl  [x] docstring  [x] unit test  [ ] integration test  (NotImplementedError)
    # [x] get_overlay_icon_file_name          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_overridden_properties         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_overridden_properties_by_pattern [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_owned_dependencies            [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_owner                        [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_project                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_property_value                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_property_value_conditional     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_property_value_conditional_explicit [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_property_value_explicit        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_redefines                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_references                   [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_remote_dependencies           [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_remote_uri                    [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_requirement_traceability_handle [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_rmm_url                       [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_save_unit                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_stereotypes                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_tag                          [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_template_parameters           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_ti                           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_tool_tip_html                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_user_defined_meta_class         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] has_nested_elements               [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] has_panel_widget                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] high_light_element                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_a_template                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_description_rtf                [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] is_display_name_rtf                [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] is_modified                      [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_remote                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] locate_in_browser                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] open_features_dialog              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove_property                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove_redefines                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove_stereotype                [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_decoration_style              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_description                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_description_and_hyperlinks     [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_description_html              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_description_rtf               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_display_name                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_display_name_rtf               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_guid                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_is_show_display_name            [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_main_diagram                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_name                         [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] set_of_template                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_owner                        [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_property_value                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_requirement_traceability_handle [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_tag_context_value              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_tag_element_value              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_tag_value                     [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_ti                           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] synchronize_template_instantiation [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [deprecated] getStereotype          - skipped (use getStereotypes)
    # [deprecated] setStereotype          - skipped (use addSpecificStereotype / addStereotype / removeStereotype)
    # [deprecated] lockOnDesignManager    - skipped (Design Manager removed in Rhapsody 8.4)
    # [deprecated] unlockOnDesignManager  - skipped (Design Manager removed in Rhapsody 8.4)

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def get_name(self) -> str:
        """Returns the name of the element.

        Returns:
            The element's name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getName", "name"))

    def set_name(self, name: str) -> None:
        """Sets the specified string as the name of the element.

        Args:
            name: The new name for the element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setName(java.lang.String name)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setName", "name", name)

    def get_meta_class(self) -> str:
        """Gets the name of the metaclass on which the model element is based.

        Returns:
            The metaclass name as a string (e.g. ``"Class"``, ``"Package"``).

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getMetaClass()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def get_guid(self) -> str:
        """Returns the GUID of the model element.

        Returns:
            The element's GUID as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getGUID()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getGUID", "GUID"))

    def add_association(self, end1: "RPModelElement", end2: "RPModelElement", name: str) -> "RPModelElement":
        """Creates an association class using the specified IRPRelation elements.

        Can only be called on elements that can contain association classes -
        packages and classes.

        Args:
            end1: The relation element at one end of the association.
            end2: The relation element at the second end of the association.
            name: The name to use for the new association class.

        Returns:
            The wrapped association class that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addAssociation(com.telelogic.rhapsody.core.IRPRelation end1, com.telelogic.rhapsody.core.IRPRelation end2, java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addAssociation(end1._com, end2._com, name)))

    def add_dependency(self, depends_on_name: str, depends_on_type: str) -> "RPModelElement":
        """Adds a dependency from the model element to the model element specified by the parameters.

        The method searches the model recursively until it finds an element
        that matches the name and metaclass specified. Since a model may
        contain multiple elements with the same name and type in different
        packages, prefer :meth:`add_dependency_to` when a specific element is
        available.

        Args:
            depends_on_name: The name of the model element on which this
                element depends.
            depends_on_type: The type (metaclass) of the model element on
                which this element depends.

        Returns:
            The wrapped dependency that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addDependency(java.lang.String dependsOnName, java.lang.String dependsOnType)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDependency(depends_on_name, depends_on_type)))

    def add_dependency_between(self, dependent: "RPModelElement", depends_on: "RPModelElement") -> "RPModelElement":
        """Creates a dependency between the two specified elements.

        In most cases :meth:`add_dependency_to` should be used. This method is
        useful when creating a dependency between two read-only elements and
        assigning ownership of the dependency to a third model element.

        Args:
            dependent: The model element that is dependent on the other.
            depends_on: The model element that the first element depends upon.

        Returns:
            The wrapped dependency that was created.

        Raises:
            RhapsodyRuntimeException: If the dependency cannot be created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addDependencyBetween(com.telelogic.rhapsody.core.IRPModelElement dependent, com.telelogic.rhapsody.core.IRPModelElement dependsOn)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDependencyBetween(dependent._com, depends_on._com)))

    def add_dependency_to(self, element: "RPModelElement") -> "RPModelElement":
        """Adds a dependency upon another model element.

        Args:
            element: The model element that this element depends upon.

        Returns:
            The wrapped dependency that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addDependencyTo(com.telelogic.rhapsody.core.IRPModelElement element)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDependencyTo(element._com)))

    def add_link_to_element(
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

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addLinkToElement(
                com.telelogic.rhapsody.core.IRPModelElement toElement,
                com.telelogic.rhapsody.core.IRPRelation assoc,
                com.telelogic.rhapsody.core.IRPModelElement fromPort,
                com.telelogic.rhapsody.core.IRPModelElement toPort)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLinkToElement(to_element._com, assoc._com, from_port._com, to_port._com)))

    def add_new_aggr(self, meta_type: str, name: str) -> "RPModelElement":
        """Adds a new model element to the current element, for example, adding a class to a package.

        Args:
            meta_type: The metaclass of the new element to create.
            name: The name of the new element.

        Returns:
            The wrapped model element that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addNewAggr(java.lang.String metaType, java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addNewAggr(meta_type, name)))

    def add_property(self, property_key: str, property_type: str, property_value: str) -> None:
        """Adds a new property to the model element and assigns a value to it.

        Args:
            property_key: The key (name) of the property to add.
            property_type: The type of the property.
            property_value: The value to assign to the property.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addProperty(java.lang.String propertyKey, java.lang.String propertyType, java.lang.String propertyValue)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addProperty(property_key, property_type, property_value))

    def add_redefines(self, new_redefine: "RPModelElement") -> None:
        """Adds a redefine relationship to the model element.

        Args:
            new_redefine: The model element to redefine.

        Raises:
            RhapsodyRuntimeException: If the redefine relationship cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addRedefines(com.telelogic.rhapsody.core.IRPModelElement newRedefine)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addRedefines(new_redefine._com))

    def add_remote_dependency_to(self, element: "RPModelElement", link_type: str) -> "RPModelElement":
        """For Design Manager projects, creates a dependency from a model element to a remote element.

        Args:
            element: The remote model element that this element depends upon.
            link_type: The type of link to create.

        Returns:
            The wrapped dependency that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addRemoteDependencyTo(com.telelogic.rhapsody.core.IRPModelElement element, java.lang.String linkType)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addRemoteDependencyTo(element._com, link_type)))

    def add_specific_stereotype(self, stereotype: "RPModelElement") -> None:
        """Applies the specified stereotype to the model element.

        Args:
            stereotype: The wrapped stereotype to apply.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addSpecificStereotype(com.telelogic.rhapsody.core.IRPStereotype stereotype)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addSpecificStereotype(stereotype._com))

    def add_stereotype(self, name: str, meta_type: str) -> "RPModelElement":
        """Applies the specified stereotype to the model element.

        If the project already contains a stereotype with the given name
        applicable to the given metaclass, that stereotype is applied. If the
        project does not yet contain such a stereotype, it is created in the
        package that owns this element and then applied.

        Args:
            name: The name of the stereotype to apply (or create and apply).
            meta_type: The metaclass to which the stereotype applies.

        Returns:
            The wrapped stereotype that was applied (or created and applied).

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::addStereotype(java.lang.String name, java.lang.String metaType)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addStereotype(name, meta_type)))

    def become_template_instantiation_of(self, new_val: "RPModelElement") -> None:
        """Makes the current model element a template instantiation of the specified template.

        Args:
            new_val: The template to instantiate.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::becomeTemplateInstantiationOf(com.telelogic.rhapsody.core.IRPModelElement newVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.becomeTemplateInstantiationOf(new_val._com))

    def change_to(self, meta_class: str) -> "RPModelElement":
        """Changes the model element to the type of element specified by the parameter provided.

        The original model element is destroyed by this operation, so the
        returned element must be captured in a variable; accessing the
        original element afterwards is unsafe.

        Args:
            meta_class: The metaclass to change this element into.

        Returns:
            The wrapped model element after the change.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::changeTo(java.lang.String metaClass)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.changeTo(meta_class)))

    def clone(self, name: str, new_owner: "RPModelElement") -> "RPModelElement":
        """Clones a model element.

        Args:
            name: The name to use for the cloned element.
            new_owner: The model element that should own the clone.

        Returns:
            The wrapped clone that was created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::clone(java.lang.String name, com.telelogic.rhapsody.core.IRPModelElement newOwner)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.clone(name, new_owner._com)))

    def create_oslc_link(self, type: str, purl: str) -> None:
        """Creates an OSLC link between the element and the element represented by the specified URL.

        Args:
            type: The type of OSLC link to create.
            purl: The URL of the target element.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                createOSLCLink; the method is defined for Java API parity only.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::createOSLCLink(java.lang.String type, java.lang.String purl)
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose createOSLCLink; method is defined for Java API parity only.")

    def delete_dependency(self, dependency: "RPModelElement") -> None:
        """Deletes the specified dependency from the model.

        Args:
            dependency: The wrapped dependency to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::deleteDependency(com.telelogic.rhapsody.core.IRPDependency dependency)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteDependency(dependency._com))

    def delete_from_project(self) -> None:
        """Deletes the current model element from the model.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::deleteFromProject()
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteFromProject())

    def delete_oslc_link(self, type: str, purl: str) -> None:
        """Deletes the specified OSLC link from the model.

        Args:
            type: The type of OSLC link to delete.
            purl: The URL of the target element.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                deleteOSLCLink; the method is defined for Java API parity only.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::deleteOSLCLink(java.lang.String type, java.lang.String purl)
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose deleteOSLCLink; method is defined for Java API parity only.")

    def error_message(self) -> str:
        """Returns the error message for the last method called.

        If the last method completed successfully, an empty string is returned,
        so this must be called immediately after the method it concerns.

        Returns:
            The error message as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::errorMessage()
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.errorMessage()))

    def find_elements_by_full_name(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches for the specified model element in the specified path under the current model element.

        Args:
            name: The full path name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::findElementsByFullName(java.lang.String name, java.lang.String metaClass)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findElementsByFullName(name, meta_class)))

    def find_nested_element(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches for the specified model element.

        Only the first level of nesting below the current element is searched;
        use :meth:`find_nested_element_recursive` to search all levels.

        Args:
            name: The name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::findNestedElement(java.lang.String name, java.lang.String metaClass)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedElement(name, meta_class)))

    def find_nested_element_recursive(self, name: str, meta_class: str) -> "RPModelElement":
        """Searches recursively for the specified model element.

        All levels of nesting below the current element are searched; use
        :meth:`find_nested_element` to search only the first level.

        Args:
            name: The name of the element to find.
            meta_class: The metaclass of the element to find.

        Returns:
            The wrapped matching model element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::findNestedElementRecursive(java.lang.String name, java.lang.String metaClass)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findNestedElementRecursive(name, meta_class)))

    def get_all_tags(self) -> "RPCollection":
        """Returns a collection of all the element's tags.

        Returns:
            An ``RPCollection`` of the element's tags.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getAllTags()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAllTags", "allTags"))

    def get_annotations(self) -> "RPCollection":
        """Returns all of the element's annotations.

        Annotations include comments, constraints, and requirements.

        Returns:
            An ``RPCollection`` of the element's annotations.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getAnnotations()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAnnotations", "annotations"))

    def get_association_classes(self) -> "RPCollection":
        """Returns a collection of all the association classes directly beneath this model element.

        Returns:
            An ``RPCollection`` of association classes.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getAssociationClasses()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getAssociationClasses", "associationClasses"))

    def get_binary_id(self) -> bytes:
        """Returns the GUID of the model element as an array of bytes.

        As opposed to :meth:`get_guid`, which returns the GUID as a string.

        Returns:
            The element's GUID as bytes.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getBinaryID()
        """
        return bytes(AbstractRPModelElement._get_method_or_property(self._com, "getBinaryID", "binaryID"))

    def get_constraints(self) -> "RPCollection":
        """Returns all of the element's constraints.

        Returns:
            An ``RPCollection`` of the element's constraints.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getConstraints()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getConstraints", "constraints"))

    def get_constraints_by_him(self) -> "RPCollection":
        """Returns all of the element's constraints (for internal use only).

        Returns:
            An ``RPCollection`` of constraints.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getConstraintsByHim()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getConstraintsByHim", "constraintsByHim"))

    def get_controlled_files(self) -> "RPCollection":
        """Returns a collection of all the element's controlled files.

        Returns:
            An ``RPCollection`` of controlled files.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getControlledFiles()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getControlledFiles", "controlledFiles"))

    def get_decoration_style(self) -> str:
        """Returns the name of the decoration style currently associated with the model element.

        Returns:
            The decoration style name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDecorationStyle()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDecorationStyle", "decorationStyle"))

    def get_dependencies(self) -> "RPCollection":
        """Returns all of the element's dependencies.

        Returns:
            An ``RPCollection`` of the element's dependencies.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDependencies()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDependencies", "dependencies"))

    def get_description(self) -> str:
        """Returns the description defined for the element.

        Returns:
            The element's description as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDescription()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDescription", "description"))

    def get_description_html(self) -> str:
        """Returns HTML representation of the element description.

        Returns:
            The element's description as an HTML string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDescriptionHTML()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDescriptionHTML", "descriptionHTML"))

    def get_description_plain_text(self) -> str:
        """Returns the description defined for the element in plain text format.

        Returns:
            The element's description as plain text.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDescriptionPlainText()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDescriptionPlainText", "descriptionPlainText"))

    def get_description_rtf(self) -> str:
        """Returns the description defined for the element in RTF format.

        Returns:
            The element's description as an RTF string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDescriptionRTF()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDescriptionRTF", "descriptionRTF"))

    def get_display_name(self) -> str:
        """Returns the label of the model element.

        Returns:
            The element's display label as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDisplayName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDisplayName", "displayName"))

    def get_display_name_rtf(self) -> str:
        """Returns the label of the model element as an RTF string.

        Returns:
            The element's display label as an RTF string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getDisplayNameRTF()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getDisplayNameRTF", "displayNameRTF"))

    def get_error_message(self) -> str:
        """Returns the error message for the last method called.

        If the last method completed successfully, an empty string is returned,
        so this must be called immediately after the method it concerns.

        Returns:
            The error message as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getErrorMessage()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getErrorMessage", "errorMessage"))

    def get_full_path_name(self) -> str:
        """Returns the full path name of the model element.

        The returned string uses the format ``package::subpackage::class``.

        Returns:
            The element's full path name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getFullPathName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getFullPathName", "fullPathName"))

    def get_full_path_name_in(self) -> str:
        """Retrieves the full path name of the element as ``(class) in (package)``.

        Returns:
            The element's full path name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getFullPathNameIn()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getFullPathNameIn", "fullPathNameIn"))

    def get_hyper_links(self) -> "RPCollection":
        """Returns a collection of all the hyperlinks associated with the element.

        Returns:
            An ``RPCollection`` of hyperlinks.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getHyperLinks()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getHyperLinks", "hyperLinks"))

    def get_icon_file_name(self) -> str:
        """Returns the full path of the graphic file used to represent elements of this type in the browser.

        Returns:
            The icon file path as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getIconFileName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getIconFileName", "iconFileName"))

    def get_interface_name(self) -> str:
        """Returns the name of the API interface corresponding to the current element.

        For example, ``"IRPClass"`` for a class element, ``"IRPOperation"``
        for an operation element.

        Returns:
            The API interface name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getInterfaceName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getInterfaceName", "interfaceName"))

    def get_is_external(self) -> int:
        """Checks whether the element is an "external" element.

        Corresponds to the value of the property ``UseAsExternal``.

        Returns:
            ``1`` if the element is external, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getIsExternal()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsExternal", "isExternal"))

    def get_is_of_meta_class(self, meta_class: str) -> int:
        """Indicates whether the model element is based on the metaclass provided as a parameter.

        Args:
            meta_class: The metaclass name to check against.

        Returns:
            ``1`` if the element is based on the metaclass, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getIsOfMetaClass(java.lang.String metaClass)
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.getIsOfMetaClass(meta_class)))

    def get_is_show_display_name(self) -> int:
        """Checks whether the model element is configured to display its label instead of its name in diagrams.

        Returns:
            ``1`` if the label is shown, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getIsShowDisplayName()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsShowDisplayName", "isShowDisplayName"))

    def get_is_unresolved(self) -> int:
        """Checks if the element is an element that can't be resolved by Rhapsody.

        Returns:
            ``1`` if the element is unresolved, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getIsUnresolved()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsUnresolved", "isUnresolved"))

    def get_local_tags(self) -> "RPCollection":
        """Returns a collection of the tags that were created locally for this model element.

        Returns:
            An ``RPCollection`` of locally created tags.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getLocalTags()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getLocalTags", "localTags"))

    def get_main_diagram(self) -> "RPModelElement":
        """Returns the "main" diagram for the element.

        This operation is valid only for packages, classes, actors, use
        cases, objects, and interfaces.

        Returns:
            The wrapped main diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getMainDiagram()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getMainDiagram", "mainDiagram"))

    def get_nested_elements(self) -> "RPCollection":
        """Gets a collection of all the model elements that are directly under the current element.

        Note that when called on a package, the returned collection does not
        include functions, global variables, or global objects, because these
        are contained in a class called ``TopLevel``. Use the ``IRPPackage``
        methods ``getGlobalFunctions``, ``getGlobalVariables``, and
        ``getGlobalObjects`` to retrieve them.

        Returns:
            An ``RPCollection`` of nested model elements.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getNestedElements()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedElements", "nestedElements"))

    def get_nested_elements_by_meta_class(self, meta_class: str, recursive: int) -> "RPCollection":
        """Retrieves all of the model elements of the specified type below the current element.

        Args:
            meta_class: The metaclass of the elements to retrieve.
            recursive: ``1`` to search recursively, ``0`` for direct children only.

        Returns:
            An ``RPCollection`` of matching nested elements.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getNestedElementsByMetaClass(java.lang.String metaClass, int recursive)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getNestedElementsByMetaClass(meta_class, recursive)))

    def get_nested_elements_recursive(self) -> "RPCollection":
        """Returns a collection that consists of the current element and all of the model elements below it.

        Returns:
            An ``RPCollection`` of this element and all nested elements.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getNestedElementsRecursive()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedElementsRecursive", "nestedElementsRecursive"))

    def get_new_term_stereotype(self) -> "RPModelElement":
        """If a "new term" stereotype has been applied to the element, returns the stereotype.

        Returns:
            The wrapped "new term" stereotype.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getNewTermStereotype()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getNewTermStereotype", "newTermStereotype"))

    def get_of_template(self) -> "RPModelElement":
        """If the element is an instantiation of a template, returns the template that it instantiates.

        Returns:
            The wrapped template that this element instantiates.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOfTemplate()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOfTemplate", "ofTemplate"))

    def get_oslc_links(self) -> "RPCollection":
        """Returns a collection of all the element's OSLC links.

        Each item in the collection is a string using the format
        ``Type=<<link type>>`` (newline) ``URL=<<linked item URL>>``.

        Returns:
            An ``RPCollection`` of OSLC links.

        Raises:
            NotImplementedError: Rhapsody2.Application.1 does not expose
                getOSLCLinks; the method is defined for Java API parity only.
        """
        raise NotImplementedError("Rhapsody2.Application.1 does not expose getOSLCLinks; method is defined for Java API parity only.")

    def get_overlay_icon_file_name(self) -> str:
        """Returns the full path of the graphic file used as an overlay on this specific model element.

        The overlay is drawn on top of the regular icon that represents
        elements of this type in the browser.

        Returns:
            The overlay icon file path as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOverlayIconFileName()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getOverlayIconFileName", "overlayIconFileName"))

    def get_overridden_properties(self, recursive: int) -> "RPCollection":
        """Returns a collection of all the properties whose value was overridden for this model element.

        Args:
            recursive: ``1`` to include overridden properties of nested
                elements, ``0`` for this element only.

        Returns:
            An ``RPCollection`` of overridden properties.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOverriddenProperties(int recursive)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getOverriddenProperties(recursive)))

    def get_overridden_properties_by_pattern(self, pattern: str, localy_overriden_only: int, with_default_values: int) -> "RPCollection":
        """Returns the overridden properties matching the specified pattern.

        Args:
            pattern: The pattern to match property keys against.
            localy_overriden_only: ``1`` to return only locally overridden
                properties, ``0`` otherwise.
            with_default_values: ``1`` to include default values, ``0`` otherwise.

        Returns:
            An ``RPCollection`` of matching overridden properties.

        Raises:
            RhapsodyRuntimeException: if the pattern is invalid or the
                overridden properties cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOverriddenPropertiesByPattern(java.lang.String pattern, int localyOverridenOnly, int withDefaultValues)
        """
        return RPCollection(AbstractRPModelElement.call_com(lambda: self._com.getOverriddenPropertiesByPattern(pattern, localy_overriden_only, with_default_values)))

    def get_owned_dependencies(self) -> "RPCollection":
        """Returns all of the dependencies that are owned by the element.

        Returns:
            An ``RPCollection`` of owned dependencies.

        Raises:
            RhapsodyRuntimeException: if the owned dependencies cannot be
                retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOwnedDependencies()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getOwnedDependencies", "ownedDependencies"))

    def get_owner(self) -> "RPModelElement":
        """Returns the model element that owns this model element.

        Returns:
            The wrapped owner element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getOwner()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getOwner", "owner"))

    def get_project(self) -> "RPModelElement":
        """Returns the project that the current element belongs to.

        Returns:
            The wrapped project element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getProject()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getProject", "project"))

    def get_property_value(self, property_key: str) -> str:
        """Returns the value of the specified property for the model element.

        The property key uses the syntax ``Subject.Metaclass.Property``
        (for example, ``CG.Class.ActiveThreadName``). If no value has been set
        specifically for this element, the default value propagated from a
        higher level is returned.

        Args:
            property_key: The key (name) of the property.

        Returns:
            The property value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getPropertyValue(java.lang.String propertyKey)
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.getPropertyValue(property_key)))

    def get_property_value_conditional(self, property_key: str, formal_key: "RPCollection", actual_values: "RPCollection") -> str:
        """Returns the value of the specified property, taking into account the tokens and token values specified.

        The property key uses the syntax ``Subject.Metaclass.Property``. For
        details on using tokens in property values, see "Conditional
        Properties" in the Rhapsody help.

        Args:
            property_key: The key (name) of the property.
            formal_key: A collection of formal tokens.
            actual_values: A collection of token values.

        Returns:
            The property value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getPropertyValueConditional(
                java.lang.String propertyKey,
                com.telelogic.rhapsody.core.IRPCollection formalKey,
                com.telelogic.rhapsody.core.IRPCollection actualValues)
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.getPropertyValueConditional(property_key, formal_key._com, actual_values._com)))

    def get_property_value_conditional_explicit(self, property_key: str, formal_key: "RPCollection", actual_values: "RPCollection") -> str:
        """Returns the property value if overridden, taking into account the tokens and token values specified.

        Unlike :meth:`get_property_value_conditional`, this returns only the value
        that was explicitly set for the model element; if no explicit value
        exists, the default value is not returned.

        Args:
            property_key: The key (name) of the property.
            formal_key: A collection of formal tokens.
            actual_values: A collection of token values.

        Returns:
            The explicitly-set property value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getPropertyValueConditionalExplicit(
                java.lang.String propertyKey,
                com.telelogic.rhapsody.core.IRPCollection formalKey,
                com.telelogic.rhapsody.core.IRPCollection actualValues)
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.getPropertyValueConditionalExplicit(property_key, formal_key._com, actual_values._com)))

    def get_property_value_explicit(self, property_key: str) -> str:
        """Returns the value of the specified property if the default value was overridden.

        Unlike :meth:`get_property_value`, this returns only the value that was
        explicitly set for the model element; if no explicit value exists, the
        default value is not returned.

        Args:
            property_key: The key (name) of the property.

        Returns:
            The explicitly-set property value as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getPropertyValueExplicit(java.lang.String propertyKey)
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.getPropertyValueExplicit(property_key)))

    def get_redefines(self) -> "RPCollection":
        """Returns the redefine relationships of the model element.

        Returns:
            An ``RPCollection`` of redefine relationships.

        Raises:
            RhapsodyRuntimeException: if the redefine relationships cannot be
                retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getRedefines()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRedefines", "redefines"))

    def get_references(self) -> "RPCollection":
        """Returns a collection of all the model elements that point to this model element.

        Returns:
            An ``RPCollection`` of referencing elements.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getReferences()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getReferences", "references"))

    def get_remote_dependencies(self) -> "RPCollection":
        """For Rhapsody Model Manager projects, returns the dependencies on remote artifacts.

        Returns:
            An ``RPCollection`` of remote dependencies.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getRemoteDependencies()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getRemoteDependencies", "remoteDependencies"))

    def get_remote_uri(self) -> str:
        """For elements that are remote resources, returns the URI of the resource.

        If called on an element that is not a remote resource, an empty string
        is returned.

        Returns:
            The remote URI as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getRemoteURI()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRemoteURI", "remoteURI"))

    def get_requirement_traceability_handle(self) -> int:
        """Returns the ID used by DOORS to refer to this requirement.

        Returns:
            The DOORS traceability handle as an int.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getRequirementTraceabilityHandle()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getRequirementTraceabilityHandle", "requirementTraceabilityHandle"))

    def get_rmm_url(self) -> str:
        """Returns the Rhapsody Model Manager url for the model element.

        Returns:
            The RMM URL as a string.

        Raises:
            RhapsodyRuntimeException: if the RMM URL cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getRmmUrl()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getRmmUrl", "rmmUrl"))

    def get_save_unit(self) -> "RPModelElement":
        """Returns the unit that the model element is saved in.

        Returns:
            The wrapped save unit.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getSaveUnit()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getSaveUnit", "saveUnit"))

    def get_stereotypes(self) -> "RPCollection":
        """Returns a collection of the stereotypes that have been applied to the element.

        Returns:
            An ``RPCollection`` of applied stereotypes.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getStereotypes()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getStereotypes", "stereotypes"))

    def get_tag(self, name: str) -> "RPModelElement":
        """Returns the tag specified.

        This method can be used for both local tags and global tags.

        Args:
            name: The name of the tag to return.

        Returns:
            The wrapped tag.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getTag(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.getTag(name)))

    def get_template_parameters(self) -> "RPCollection":
        """For model elements that are templates, returns the template parameters.

        Returns:
            An ``RPCollection`` of template parameters.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getTemplateParameters()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getTemplateParameters", "templateParameters"))

    def get_ti(self) -> "RPModelElement":
        """For template instantiations, returns an object containing the template instantiation parameters.

        Returns:
            The wrapped template instantiation.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getTi()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTi", "ti"))

    def get_tool_tip_html(self) -> str:
        """Returns the HTML that would be used to display the tooltip for the element in the user interface.

        Returns:
            The tooltip HTML as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getToolTipHTML()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getToolTipHTML", "toolTipHTML"))

    def get_user_defined_meta_class(self) -> str:
        """Gets the name of the New Term on which the model element is based.

        To get the name of the metaclass on which the New Term is based, use
        :meth:`get_meta_class`.

        Returns:
            The user-defined metaclass name as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::getUserDefinedMetaClass()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getUserDefinedMetaClass", "userDefinedMetaClass"))

    def has_nested_elements(self) -> int:
        """Checks whether the model element contains other elements.

        Returns:
            ``1`` if the element contains nested elements, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::hasNestedElements()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.hasNestedElements()))

    def has_panel_widget(self) -> int:
        """Checks whether the model element is bound to a panel diagram widget.

        Returns:
            ``1`` if bound to a panel widget, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::hasPanelWidget()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.hasPanelWidget()))

    def high_light_element(self) -> None:
        """Locates the element in the Rhapsody browser, and highlights it in the diagram where it appears.

        The element is highlighted in the diagram only if it is the kind of
        element that can appear in only one diagram, for example a state.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::highLightElement()
        """
        AbstractRPModelElement.call_com(lambda: self._com.highLightElement())

    def is_a_template(self) -> int:
        """Checks whether the model element is a template.

        Returns:
            ``1`` if the element is a template, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::isATemplate()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isATemplate", "aTemplate"))

    def is_description_rtf(self) -> int:
        """Checks whether the description for the element is in RTF format.

        Returns:
            ``1`` if the description is RTF, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::isDescriptionRTF()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isDescriptionRTF", "descriptionRTF"))

    def is_display_name_rtf(self) -> int:
        """Checks whether the label of the element is in RTF format.

        Returns:
            ``1`` if the label is RTF, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::isDisplayNameRTF()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isDisplayNameRTF", "displayNameRTF"))

    def is_modified(self) -> int:
        """Checks if the element was modified since the model was last saved.

        Returns:
            ``1`` if the element was modified, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::isModified()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isModified", "modified"))

    def is_remote(self) -> int:
        """Checks whether the model element is a remote resource such as a DOORS/DOORS Next requirement.

        Returns:
            ``1`` if the element is remote, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::isRemote()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isRemote", "remote"))

    def locate_in_browser(self) -> int:
        """Locates the model element in the Rhapsody browser.

        Returns:
            ``1`` if the element was located, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::locateInBrowser()
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.locateInBrowser()))

    def open_features_dialog(self, new_dialog: int) -> None:
        """Displays the information for the element in the Features window.

        Depending on ``new_dialog``, opens a new Features window or uses an
        already-open one.

        Args:
            new_dialog: ``1`` to open in a new dialog, ``0`` to use an existing
                window (or a new one if none is open).

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::openFeaturesDialog(int newDialog)
        """
        AbstractRPModelElement.call_com(lambda: self._com.openFeaturesDialog(new_dialog))

    def remove_property(self, property_key: str) -> None:
        """Removes the value that was set for the specified property.

        This is equivalent to the "un-override" option in the Features window.
        The property key uses the syntax ``Subject.Metaclass.Property``.

        Args:
            property_key: The key (name) of the property to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::removeProperty(java.lang.String propertyKey)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeProperty(property_key))

    def remove_redefines(self, removed_redefine: "RPModelElement") -> None:
        """Removes a redefine relationship from the model element.

        Args:
            removed_redefine: The redefine relationship to remove.

        Raises:
            RhapsodyRuntimeException: if the redefine relationship cannot be
                removed.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::removeRedefines(com.telelogic.rhapsody.core.IRPModelElement removedRedefine)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeRedefines(removed_redefine._com))

    def remove_stereotype(self, stereotype: "RPModelElement") -> None:
        """Removes the specified stereotype from the element.

        Args:
            stereotype: The wrapped stereotype to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::removeStereotype(com.telelogic.rhapsody.core.IRPStereotype stereotype)
        """
        AbstractRPModelElement.call_com(lambda: self._com.removeStereotype(stereotype._com))

    def set_decoration_style(self, new_val: str) -> None:
        """Specifies the decoration style that should now be associated with the model element.

        The value must be one of the strings defined by the
        ``Format::Decoration::StyleNames`` property.

        Args:
            new_val: The decoration style name to associate.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDecorationStyle(java.lang.String newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDecorationStyle", "decorationStyle", new_val)

    def set_description(self, description: str) -> None:
        """Sets the specified string as the description of the element.

        Args:
            description: The description text to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDescription(java.lang.String description)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDescription", "description", description)

    def set_description_and_hyperlinks(self, rtf_text: str, targets: "RPCollection") -> None:
        """Specifies an RTF description for the element and a collection of elements to hyperlink.

        Args:
            rtf_text: The RTF string to use as the description (must be RTF).
            targets: A collection of elements to which hyperlinks should be created.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDescriptionAndHyperlinks(java.lang.String rtfText, com.telelogic.rhapsody.core.IRPCollection targets)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setDescriptionAndHyperlinks(rtf_text, targets._com))

    def set_description_html(self, description_html: str) -> None:
        """Sets the HTML representation of the element description.

        Note: the Java API documents this method as not implemented and it
        should not be used.

        Args:
            description_html: The HTML description to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDescriptionHTML(java.lang.String descriptionHTML)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDescriptionHTML", "descriptionHTML", description_html)

    def set_description_rtf(self, description_rtf: str) -> None:
        """Specifies the RTF string to use for the description of the model element.

        Args:
            description_rtf: The RTF description to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDescriptionRTF(java.lang.String descriptionRTF)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDescriptionRTF", "descriptionRTF", description_rtf)

    def set_display_name(self, display_name: str) -> None:
        """Specifies the text to use for the label of the model element.

        Args:
            display_name: The label text to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDisplayName(java.lang.String displayName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDisplayName", "displayName", display_name)

    def set_display_name_rtf(self, new_val: str) -> None:
        """Specifies the RTF string to use for the label of the model element.

        Args:
            new_val: The RTF label text to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setDisplayNameRTF(java.lang.String newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setDisplayNameRTF", "displayNameRTF", new_val)

    def set_guid(self, guid: str) -> None:
        """Sets a new GUID for the model element.

        Args:
            guid: The new GUID to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setGUID(java.lang.String gUID)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setGUID", "GUID", guid)

    def set_is_show_display_name(self, is_show_display_name: int) -> None:
        """Specifies whether the label of the element should be displayed instead of the element name in diagrams.

        This changes the value of the ``General::Graphics::ShowLabels``
        property.

        Args:
            is_show_display_name: ``1`` to show the label, ``0`` to show the name.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setIsShowDisplayName(int isShowDisplayName)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsShowDisplayName", "isShowDisplayName", is_show_display_name)

    def set_main_diagram(self, main_diagram: "RPModelElement") -> None:
        """Specifies the "main" diagram for the element.

        This operation is valid only for packages, classes, actors, use
        cases, objects, and interfaces.

        Args:
            main_diagram: The wrapped diagram to set as the main diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setMainDiagram(com.telelogic.rhapsody.core.IRPDiagram mainDiagram)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setMainDiagram", "mainDiagram", main_diagram._com)

    def set_of_template(self, of_template: "RPModelElement") -> None:
        """Makes the current model element a template instantiation of the specified template.

        Args:
            of_template: The wrapped template to instantiate.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setOfTemplate(com.telelogic.rhapsody.core.IRPModelElement ofTemplate)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOfTemplate", "ofTemplate", of_template._com)

    def set_owner(self, owner: "RPModelElement") -> None:
        """Specifies the model element that should be the owner of this element.

        Args:
            owner: The wrapped element that should own this element.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setOwner(com.telelogic.rhapsody.core.IRPModelElement owner)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setOwner", "owner", owner._com)

    def set_property_value(self, property_key: str, property_value: str) -> None:
        """Sets the value of a property for the model element.

        The property key uses the syntax ``Subject.Metaclass.Property`` (for
        example, ``CG.Class.ActiveThreadName``). For boolean properties, use
        ``"True"`` or ``"False"``.

        Args:
            property_key: The key (name) of the property.
            property_value: The value to assign to the property.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setPropertyValue(java.lang.String propertyKey, java.lang.String propertyValue)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setPropertyValue(property_key, property_value))

    def set_requirement_traceability_handle(self, requirement_traceability_handle: int) -> None:
        """Sets a new ID to be used to reference this requirement.

        Args:
            requirement_traceability_handle: The new DOORS traceability handle.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setRequirementTraceabilityHandle(int requirementTraceabilityHandle)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setRequirementTraceabilityHandle", "requirementTraceabilityHandle", requirement_traceability_handle)

    def set_tag_context_value(self, tag: "RPModelElement", elements: "RPCollection", multiplicities: "RPCollection") -> "RPModelElement":
        """Applies the specified tag and sets its value to a specific instance of another model element.

        ``elements`` is a collection of model elements representing the full
        path to the target element (used to set the value to its full path);
        it must contain ``IRPModelElement`` objects. ``multiplicities`` is a
        collection of the relevant indices for each element in ``elements``
        (as strings), allowing the value to point to a specific instance when
        multiplicity is greater than one.

        Args:
            tag: The wrapped tag to apply.
            elements: A collection of model elements forming the target path.
            multiplicities: A collection of multiplicities (indices) as strings.

        Returns:
            The wrapped tag that was set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setTagContextValue(
                com.telelogic.rhapsody.core.IRPTag tag,
                com.telelogic.rhapsody.core.IRPCollection elements,
                com.telelogic.rhapsody.core.IRPCollection multiplicities)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setTagContextValue(tag._com, elements._com, multiplicities._com)))

    def set_tag_element_value(self, tag: "RPModelElement", val: "RPModelElement") -> "RPModelElement":
        """Applies a tag whose type is a model element to the current element with the value specified.

        If the tag has already been applied, this method can be used to modify
        its value.

        Args:
            tag: The wrapped tag to apply.
            val: The wrapped model element value.

        Returns:
            The wrapped tag that was set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setTagElementValue(com.telelogic.rhapsody.core.IRPTag tag, com.telelogic.rhapsody.core.IRPModelElement val)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setTagElementValue(tag._com, val._com)))

    def set_tag_value(self, tag: "RPModelElement", val: str) -> "RPModelElement":
        """Applies the specified tag to the model element with the value specified.

        If the tag has already been applied, this method can be used to modify
        its value.

        Args:
            tag: The wrapped tag to apply.
            val: The value to assign to the tag.

        Returns:
            The wrapped tag that was set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setTagValue(com.telelogic.rhapsody.core.IRPTag tag, java.lang.String val)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.setTagValue(tag._com, val)))

    def set_ti(self, ti: "RPModelElement") -> None:
        """Sets the template instantiation for the model element (for internal use only).

        Args:
            ti: The wrapped template instantiation to set.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::setTi(com.telelogic.rhapsody.core.IRPTemplateInstantiation ti)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setTi", "ti", ti._com)

    def synchronize_template_instantiation(self) -> None:
        """Updates the instantiation to match changes made to its template.

        After changes are made to a template, this method can be called on
        each instantiation of the template in order to update the
        instantiation to match the changes that were made to the template.

        Reference:
            com.telelogic.rhapsody.core.IRPModelElement::synchronizeTemplateInstantiation()
        """
        AbstractRPModelElement.call_com(lambda: self._com.synchronizeTemplateInstantiation())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RPModelElement):
            return NotImplemented
        return bool(self._com == other._com)

    def __hash__(self) -> int:
        return hash(id(self._com))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.get_name()!r})"


class AddToModelMode(IntEnum):
    """Constant values mirroring ``IRPApplication.AddToModel_Mode``.

    Returned by :meth:`RPUnit.getAddToModelMode` to indicate how a unit was
    added to the model. ``IntEnum`` so callers may compare the raw ``int``
    returned by the COM call directly against these constants.
    """

    AS_REFERENCE = 0
    AS_UNIT_WITH_COPY = 1
    AS_UNIT_WITHOUT_COPY = 2


class RPUnit(RPModelElement):
    """Wraps ``IRPUnit``: model elements that can be saved as separate files."""

    # IRPUnit method parity checklist:
    # [x] copy_to_another_project                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_add_to_model_mode                   [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_cm_header                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_cm_state                          [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_current_directory                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_filename                         [x] impl  [x] docstring  [x] unit test  [ ] integration test  (pre-existing)
    # [x] get_include_in_next_load                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_stub                           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_language                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_last_modified_time                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_nested_save_units                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_nested_save_units_count             [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_structure_diagrams                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_unit_path                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_read_only                          [x] impl  [x] docstring  [x] unit test  [ ] integration test  (pre-existing)
    # [x] is_reference_unit                     [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] is_separate_save_unit                  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] load                                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] move_to_another_project_leave_a_reference [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] reference_to_another_project           [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] save                                [x] impl  [x] docstring  [x] unit test  [ ] integration test  (pre-existing)
    # [x] set_cm_header                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_filename                         [x] impl  [x] docstring  [x] unit test  [ ] integration test  (pre-existing)
    # [x] set_include_in_next_load                [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_language                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_read_only                         [x] impl  [x] docstring  [x] unit test  [ ] integration test  (pre-existing)
    # [x] set_separate_save_unit                 [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_unit_path                         [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] unload                              [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] getNestedElements - provided by RPModelElement
    # No deprecated IRPUnit methods.

    def copy_to_another_project(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Makes an editable copy of the unit in a different project.

        Args:
            parent_in_target: The model element that will be the parent of the
                new unit in the target project.

        Returns:
            The wrapped unit that was created in the target project.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::copyToAnotherProject(com.telelogic.rhapsody.core.IRPModelElement parentInTarget)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.copyToAnotherProject(parent_in_target._com)))

    def get_add_to_model_mode(self) -> int:
        """Returns an indication of how the unit was added to the model.

        The returned value corresponds to one of the :class:`AddToModelMode`
        constants.

        Returns:
            A value indicating how the unit was added to the model (see
            :class:`AddToModelMode`).

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getAddToModelMode()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getAddToModelMode", "addToModelMode"))

    def get_cm_header(self) -> str:
        """Returns the header used by the Configuration Management tool for the unit.

        Returns:
            The Configuration Management tool header as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getCMHeader()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getCMHeader", "cMHeader"))

    def get_cm_state(self) -> int:
        """Returns the configuration management state of the unit.

        Returns:
            The configuration management state of the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getCMState()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getCMState", "cMState"))

    def get_current_directory(self) -> str:
        """Gets the name of the directory that contains the file used to store the unit.

        The string returned consists of the full path except for the name of
        the file itself.

        Returns:
            The name of the directory that contains the file used to store the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getCurrentDirectory()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getCurrentDirectory", "currentDirectory"))

    def get_filename(self) -> str:
        """Gets the name of the file used to store the unit.

        The string returned consists only of the filename, not the entire path.

        Returns:
            The name of the file used to store the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getFilename()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getFilename", "filename"))

    def get_include_in_next_load(self) -> int:
        """Checks whether the unit is going to be loaded the next time the model is loaded.

        Returns:
            ``1`` if the unit is going to be loaded the next time the model is
            loaded, ``0`` if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getIncludeInNextLoad()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIncludeInNextLoad", "includeInNextLoad"))

    def get_is_stub(self) -> int:
        """Checks whether the unit is currently unloaded.

        Returns:
            ``1`` if the unit is not currently loaded, ``0`` if it is currently loaded.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getIsStub()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsStub", "isStub"))

    def get_language(self) -> str:
        """Gets the language of the unit.

        Returns:
            The language of the unit as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getLanguage()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getLanguage", "language"))

    def get_last_modified_time(self) -> str:
        """Returns the time at which the file representing the unit was last modified.

        Returns:
            The last modified time as a string.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getLastModifiedTime()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getLastModifiedTime", "lastModifiedTime"))

    def get_nested_save_units(self) -> "RPCollection":
        """Returns a collection of any sub-elements of the unit that were saved as individual files.

        Returns:
            An ``RPCollection`` of sub-elements that were saved as individual files.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getNestedSaveUnits()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getNestedSaveUnits", "nestedSaveUnits"))

    def get_nested_save_units_count(self) -> int:
        """Returns the number of sub-elements of the unit that were saved as individual files.

        Returns:
            The number of sub-elements that were saved as individual files.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getNestedSaveUnitsCount()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getNestedSaveUnitsCount", "nestedSaveUnitsCount"))

    def get_structure_diagrams(self) -> "RPCollection":
        """Returns a collection of any structure diagrams that are sub-elements of the unit.

        Used primarily for structure diagrams that belong to individual classes.

        Returns:
            An ``RPCollection`` of structure diagrams that are sub-elements of the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getStructureDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getStructureDiagrams", "structureDiagrams"))

    def get_unit_path(self, b_full_path: int) -> str:
        """Returns the path of the unit, including the filename.

        Args:
            b_full_path: ``1`` to return the full path, ``0`` to return a
                relative path. For relative paths, the path returned is relative
                to the saved unit that owns this unit.

        Returns:
            The path of the unit, including the filename.

        Raises:
            RhapsodyRuntimeException: if the unit path cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::getUnitPath(int bFullPath)
        """
        return str(AbstractRPModelElement.call_com(lambda: self._com.getUnitPath(b_full_path)))

    def is_read_only(self) -> bool:
        """Checks whether the file used to store the unit is read-only.

        Returns:
            ``True`` if the file is read-only, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::isReadOnly()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "isReadOnly", "readOnly"))

    def is_reference_unit(self) -> int:
        """Checks whether the unit was added to the model as a reference.

        Returns:
            ``1`` if the unit was added to the model as a reference, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::isReferenceUnit()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isReferenceUnit", "referenceUnit"))

    def is_separate_save_unit(self) -> int:
        """Checks whether the current IRPUnit object is saved in its own file.

        ``IRPUnit`` objects represent any element that can in theory be saved
        as a separate file, even if this is not the case for a specific element
        in your model.

        Returns:
            ``1`` if the unit is saved in its own file, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::isSeparateSaveUnit()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "isSeparateSaveUnit", "separateSaveUnit"))

    def load(self, with_subs: int) -> "RPModelElement":
        """Loads the unit.

        Args:
            with_subs: ``1`` to load the unit's subunits as well, ``0`` to load
                only the unit itself.

        Returns:
            The wrapped unit that was loaded.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::load(int withSubs)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.load(with_subs)))

    def move_to_another_project_leave_a_reference(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Moves the unit to a different project, and adds a reference to it in the original project.

        Args:
            parent_in_target: The model element that will be the parent of the
                new unit in the target project.

        Returns:
            The wrapped unit that was created in the target project.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::moveToAnotherProjectLeaveAReference(com.telelogic.rhapsody.core.IRPModelElement parentInTarget)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.moveToAnotherProjectLeaveAReference(parent_in_target._com)))

    def reference_to_another_project(self, parent_in_target: "RPModelElement") -> "RPModelElement":
        """Creates a reference to the unit in a different project.

        Args:
            parent_in_target: The model element that will be the parent of the
                reference (read-only) unit created in the target project.

        Returns:
            The wrapped reference (read-only) unit that was created in the target project.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::referenceToAnotherProject(com.telelogic.rhapsody.core.IRPModelElement parentInTarget)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.referenceToAnotherProject(parent_in_target._com)))

    def save(self) -> None:
        """Saves the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::save(int)
        """
        AbstractRPModelElement.call_com(lambda: self._com.save())

    def set_cm_header(self, cm_header: str) -> None:
        """Sets the Configuration Management tool header for the unit.

        Args:
            cm_header: The Configuration Management tool header to use for the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setCMHeader(java.lang.String cmHeader)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setCMHeader", "cMHeader", cm_header)

    def set_filename(self, filename: str) -> None:
        """Specifies the name that should be used for the file representing the unit.

        The string should only include the first part of the filename;
        Rhapsody handles the file extension. Note that if you change the
        filename, the old file remains on disk.

        Args:
            filename: The name that should be used for the file representing the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setFilename(java.lang.String filename)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setFilename", "filename", filename)

    def set_include_in_next_load(self, include_in_next_load: int) -> None:
        """Toggles whether the unit is going to be loaded the next time the model is loaded.

        Args:
            include_in_next_load: ``1`` to load the unit the next time the model
                is loaded, ``0`` to not load it.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setIncludeInNextLoad(int)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIncludeInNextLoad", "includeInNextLoad", include_in_next_load)

    def set_language(self, new_language: str, recursive: int) -> None:
        """Specifies the programming language that should be used when code is generated for the unit.

        This method can be used for mixed-language models.

        Args:
            new_language: One of ``"C++"``/``"cpp"``, ``"C"``, ``"Java"``,
                ``"Ada"``, or ``"C#"``.
            recursive: ``1`` to set the language for all subunits of the
                element, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setLanguage(java.lang.String newLanguage, int recursive)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setLanguage(new_language, recursive))

    def set_read_only(self, read_only: bool) -> None:
        """Toggles the read-only status of the file used to store the unit.

        Args:
            read_only: ``True`` to change the file to read-only, ``False`` to
                change the file to read/write.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setReadOnly(int)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setReadOnly", "readOnly", 1 if read_only else 0)

    def set_separate_save_unit(self, p_val: int) -> None:
        """Specifies whether the current IRPUnit object should be saved in its own file.

        Args:
            p_val: ``1`` to save the element in its own file, ``0`` to not save
                it in its own file.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setSeparateSaveUnit(int)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setSeparateSaveUnit", "separateSaveUnit", p_val)

    def set_unit_path(self, new_path: str) -> None:
        """Specifies the path that should be used to locate the unit when it is added to a model "By Reference".

        Args:
            new_path: The path that should be used to locate the unit when it is
                added to a model "By Reference".

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::setUnitPath(java.lang.String newPath)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setUnitPath", "unitPath", new_path)

    def unload(self) -> None:
        """Unloads the unit.

        Reference:
            com.telelogic.rhapsody.core.IRPUnit::unload()
        """
        AbstractRPModelElement.call_com(lambda: self._com.unload())


class RPCollection:
    """Wraps ``IRPCollection``: an iterable/indexable container of elements."""

    # IRPCollection method parity checklist:
    # [x] get_count  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_item  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_item  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] addGraphicalItem  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] toList  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setSize  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] remove  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setString  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setModelElement  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] empty  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] setInteger  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # No deprecated IRPCollection methods.

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def get_count(self) -> int:
        """Returns the number of elements in the collection.

        Returns:
            The number of elements in the collection as an integer.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::getCount()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getCount", "Count"))

    def get_item(self, index: int) -> Any:
        """Returns the element at the specified index in the collection.

        Args:
            index: The 1-based position of the element to retrieve.

        Returns:
            The wrapped element at the given index.

        Raises:
            RhapsodyRuntimeException: if the element at the given index
                cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::getItem(int)
        """
        if hasattr(self._com, "getItem"):
            raw_item = AbstractRPModelElement.call_com(lambda: self._com.getItem(index))
        else:
            raw_item = AbstractRPModelElement.call_com(lambda: self._com.Item(index))
        return AbstractRPModelElement._wrap_if_element(raw_item)

    def add_item(self, element: RPModelElement) -> None:
        """Adds an element to the collection.

        Args:
            element: The model element to add to the collection.

        Raises:
            RhapsodyRuntimeException: if the element cannot be added to
                the collection.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::addItem(com.telelogic.rhapsody.core.IRPModelElement)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addItem(element._com))

    def add_graphical_item(self, item: "RPModelElement") -> None:
        """Adds a graphical item to the collection.

        Args:
            item: The graphical model element to add.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::addGraphicalItem(com.telelogic.rhapsody.core.IRPModelElement)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addGraphicalItem(item._com))

    def to_list(self) -> list:
        """Converts the collection to a Python list.

        Returns:
            A Python list containing all elements in the collection.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::toList()
        """
        return list(self)

    def set_size(self, size: int) -> None:
        """Sets the size of the collection.

        Args:
            size: The new size for the collection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::setSize(int)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setSize(size))

    def remove(self, index: int) -> None:
        """Removes the element at the specified index.

        Args:
            index: The 1-based index of the element to remove.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::remove(int)
        """
        AbstractRPModelElement.call_com(lambda: self._com.remove(index))

    def set_string(self, index: int, value: str) -> None:
        """Sets a string value at the specified index.

        Args:
            index: The 1-based index where to set the value.
            value: The string value to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::setString(int, java.lang.String)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setString(index, value))

    def set_model_element(self, index: int, element: "RPModelElement") -> None:
        """Sets a model element at the specified index.

        Args:
            index: The 1-based index where to set the element.
            element: The model element to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::setModelElement(int, com.telelogic.rhapsody.core.IRPModelElement)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setModelElement(index, element._com))

    def empty(self) -> None:
        """Removes all elements from the collection.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::empty()
        """
        AbstractRPModelElement.call_com(lambda: self._com.empty())

    def set_integer(self, index: int, value: int) -> None:
        """Sets an integer value at the specified index.

        Args:
            index: The 1-based index where to set the value.
            value: The integer value to set.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPCollection::setInteger(int, int)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setInteger(index, value))

    def __len__(self) -> int:
        return self.get_count()

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, slice):
            return [self.get_item(i + 1) for i in range(*index.indices(len(self)))]
        if index < 0:
            raise IndexError("negative indices are not supported")
        return self.get_item(index + 1)

    def __iter__(self) -> Iterator[Any]:
        for index in range(1, len(self) + 1):
            yield self.get_item(index)
