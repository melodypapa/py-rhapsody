"""Wraps ``com.telelogic.rhapsody.core.IRPClass``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation
    from rhapsody_cli.models.elements.common.model_other_model import RPType
    from rhapsody_cli.models.elements.graphics.model_graphics import RPLink
    from rhapsody_cli.models.elements.interactions.model_interactions import RPEventReception


class RPClass(RPClassifier):
    """Wraps ``IRPClass``: represents a class in the model."""

    # IRPClass method parity checklist:
    # [x] add_class                 [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_constructor           [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_destructor            [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_superclass            [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] get_is_abstract            [x] impl  [x] docstring  [x] unit test  [x] integration test   (already implemented)
    # [x] add_event_reception        [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_event_reception_with_event [x] impl (raises NotImplementedError) [x] docstring [x] unit test  [x] integration test  (COM method not exposed)
    # [x] add_link                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_link_to_part_via_port     [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_reception             [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_triggered_operation    [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] add_type                  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_class              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_constructor        [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_destructor         [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_event_reception     [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_reception          [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_superclass         [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] delete_type               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_is_active              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_is_behavior_overriden   [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_is_composite           [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_is_final               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] get_is_reactive            [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_abstract (unimplemented -- raises not_implemented_error, see docstring)  [ ] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_active              [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_behavior_overriden   [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_final               [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] update_contained_diagrams_on_server [x] impl [x] docstring [x] unit test  [x] integration test
    # No deprecated methods in IRPClass.

    def add_superclass(self, super_class: "RPClass") -> None:
        """Adds a superclass to this class.

        Args:
            super_class: The class to inherit from.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addSuperclass(com.telelogic.rhapsody.core.IRPClass superClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addSuperclass(super_class._com))

    def add_constructor(self, arguments_data: str) -> "RPOperation":
        """Adds a constructor operation to this class.

        Args:
            arguments_data: The argument specification for the constructor.

        Returns:
            The wrapped ``IRPOperation`` for the new constructor.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addConstructor(java.lang.String argumentsData)
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addConstructor(arguments_data))))

    def add_destructor(self) -> "RPOperation":
        """Adds a destructor operation to this class.

        Returns:
            The wrapped ``IRPOperation`` for the new destructor.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addDestructor()
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDestructor())))

    def get_is_abstract(self) -> bool:
        """Checks whether this class is abstract.

        Returns:
            ``True`` if the class is abstract, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsAbstract()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsAbstract", "isAbstract"))

    def add_class(self, name: str) -> "RPClass":
        """Adds a nested class to this class.

        Args:
            name: The name of the new nested class.

        Returns:
            The wrapped ``IRPClass`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addClass(java.lang.String name)
        """
        return cast("RPClass", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name))))

    def add_event_reception(self, name: str) -> "RPEventReception":
        """Adds an event reception to the current class.

        It is preferable to use :meth:`add_reception` instead.

        Args:
            name: The name to use for the new event reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addEventReception(java.lang.String name)
        """
        return cast("RPEventReception", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReception(name))))

    def add_event_reception_with_event(self, name: str, event: RPModelElement) -> "RPEventReception":
        """Adds a new event reception, using the specified event.

        Note: ``addEventReceptionWithEvent`` is not exposed in the Rhapsody COM
        automation type library. This method raises ``NotImplementedError`` to
        prevent its use.

        Args:
            name: The name to use for the new event reception.
            event: The event that should be associated with the new event reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Raises:
            NotImplementedError: Always raised, as this method is not exposed
                in the Rhapsody COM type library.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addEventReceptionWithEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPEvent event)
        """
        raise NotImplementedError(
            "addEventReceptionWithEvent is not exposed in the Rhapsody COM automation type library. " "Use add_event_reception(name) instead and set the event via the reception object."
        )

    def add_link(
        self,
        from_part: RPModelElement,
        to_part: RPModelElement,
        assoc: RPModelElement,
        from_port: RPModelElement,
        to_port: RPModelElement,
    ) -> "RPLink":
        """Creates a link between two parts belonging to a class.

        In addition to the two parts, you must supply either the association the
        link should represent, or the two ports to use for the link. If you
        provide the two ports, use ``None`` for the association. If you specify an
        association, use ``None`` for the two ports. If you are not specifying the
        two ports, you must still provide an association as an argument even when
        only one relevant association exists.

        Args:
            from_part: The "from" part for the link.
            to_part: The "to" part for the link.
            assoc: The association that the link should represent.
            from_port: The "from" port for the link.
            to_port: The "to" port for the link.

        Returns:
            The wrapped ``IRPLink`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addLink(
                com.telelogic.rhapsody.core.IRPInstance fromPart,
                com.telelogic.rhapsody.core.IRPInstance toPart,
                com.telelogic.rhapsody.core.IRPRelation assoc,
                com.telelogic.rhapsody.core.IRPPort fromPort,
                com.telelogic.rhapsody.core.IRPPort toPort)
        """
        return cast("RPLink", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLink(from_part._com, to_part._com, assoc._com, from_port._com, to_port._com))))

    def add_link_to_part_via_port(
        self,
        to_part: RPModelElement,
        part_port: RPModelElement,
        class_port: RPModelElement,
        assoc: RPModelElement,
    ) -> "RPLink":
        """Creates a delegation connector between a class and one of its parts.

        You must supply either the association the link should represent, or the
        two ports (``part_port`` and ``class_port``) to use. If you provide the
        two ports, use ``None`` for ``assoc``; if you specify an association, use
        ``None`` for the two ports. If you are not specifying the two ports, you
        must still provide an association even when only one relevant
        association exists.

        Args:
            to_part: The part that should be linked to.
            part_port: The port to use on the part.
            class_port: The port to use on the class.
            assoc: The association that the link should represent.

        Returns:
            The wrapped ``IRPLink`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addLinkToPartViaPort(
                com.telelogic.rhapsody.core.IRPInstance toPart,
                com.telelogic.rhapsody.core.IRPInstance partPort,
                com.telelogic.rhapsody.core.IRPInstance classPort,
                com.telelogic.rhapsody.core.IRPRelation assoc)
        """
        return cast("RPLink", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLinkToPartViaPort(to_part._com, part_port._com, class_port._com, assoc._com))))

    def add_reception(self, name: str) -> "RPEventReception":
        """Adds a reception to the current class.

        Args:
            name: The name to use for the new reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addReception(java.lang.String name)
        """
        return cast("RPEventReception", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addReception(name))))

    def add_triggered_operation(self, name: str) -> "RPOperation":
        """Adds a new triggered operation to the current class.

        Args:
            name: The name to use for the new triggered operation.

        Returns:
            The wrapped ``IRPOperation`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addTriggeredOperation(java.lang.String name)
        """
        return cast("RPOperation", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTriggeredOperation(name))))

    def add_type(self, name: str) -> "RPType":
        """Adds a new type to the current class.

        Args:
            name: The name to use for the new type.

        Returns:
            The wrapped ``IRPType`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addType(java.lang.String name)
        """
        return cast("RPType", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addType(name))))

    def delete_class(self, name: str) -> None:
        """Deletes the specified class from the current class.

        Args:
            name: The name of the class that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteClass(java.lang.String name)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteClass(name))

    def delete_constructor(self, constructor: RPModelElement) -> None:
        """Deletes the specified constructor from the current class.

        Args:
            constructor: The constructor that should be deleted (an ``IRPOperation``).

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteConstructor(com.telelogic.rhapsody.core.IRPOperation constructor)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteConstructor(constructor._com))

    def delete_destructor(self) -> None:
        """Deletes the destructor for the class.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteDestructor()
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteDestructor())

    def delete_event_reception(self, p_val: RPModelElement) -> None:
        """Deletes the specified event reception.

        It is preferable to use :meth:`delete_reception` instead.

        Args:
            p_val: The reception that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteEventReception(com.telelogic.rhapsody.core.IRPEventReception pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteEventReception(p_val._com))

    def delete_reception(self, p_val: RPModelElement) -> None:
        """Deletes the specified reception from the current class.

        Args:
            p_val: The reception that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteReception(com.telelogic.rhapsody.core.IRPEventReception pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteReception(p_val._com))

    def delete_superclass(self, super_class: "RPClass") -> None:
        """Removes the inheritance relationship with the specified base class.

        Args:
            super_class: The base class of the current class.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteSuperclass(com.telelogic.rhapsody.core.IRPClass superClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteSuperclass(super_class._com))

    def delete_type(self, name: str) -> None:
        """Deletes the specified type from the current class.

        Args:
            name: The name of the type that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteType(java.lang.String name)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteType(name))

    def get_is_active(self) -> int:
        """Checks whether the class was defined as "active".

        "Active" means that during execution it runs on its own thread.

        Returns:
            ``1`` if the class is "active", ``0`` if it is "sequential".

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsActive()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsActive", "isActive"))

    def get_is_behavior_overriden(self) -> int:
        """Checks whether a class does not inherit the behavior of its base class statechart.

        Returns:
            ``1`` if the class does not inherit this behavior, ``0`` if it does.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsBehaviorOverriden()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehaviorOverriden", "isBehaviorOverriden"))

    def get_is_composite(self) -> int:
        """Checks whether the class is a composite class.

        Returns:
            ``1`` if the class is a composite class, ``0`` if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsComposite()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsComposite", "isComposite"))

    def get_is_final(self) -> int:
        """Checks whether the class is a final class.

        Relevant only for Java classes.

        Returns:
            ``1`` if the class is final, ``0`` if not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsFinal()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsFinal", "isFinal"))

    def get_is_reactive(self) -> int:
        """Checks whether the class is a reactive class.

        A reactive class has a statechart or activity diagram so that it
        reacts to events.

        Returns:
            ``1`` if the class is reactive, ``0`` if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsReactive()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsReactive", "isReactive"))

    def set_is_abstract(self, is_abstract: int) -> None:
        """Specifies that the class should be abstract.

        Args:
            is_abstract: ``1`` to make the class abstract, ``0`` to make it non-abstract.

        Raises:
            NotImplementedError: Always. Under Rhapsody2.Application.1 (build 9.0.2) a write to
                the ``isAbstract`` COM property is accepted without error (the typelib declares
                both PROPERTYGET and PROPERTYPUT for isAbstract under the same DISPID -- it is
                not read-only at the interface level), but the write does not persist --
                confirmed via immediate read-back, post-``saveAll()``, and a fresh re-fetch of
                the element. No workaround (e.g. the generic ``setPropertyValue`` metatype
                property system) is currently known; "Abstract" is not a defined key in
                ``Share/Properties/factory.prp``. Marked unimplemented rather than silently
                no-opping so callers cannot mistake this for a successful write. Revisit if a
                future Rhapsody build fixes this.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsAbstract(int isAbstract)
        """
        raise NotImplementedError("RPClass.set_is_abstract is unimplemented: Rhapsody2.Application.1 accepts the write but never persists it. See docstring for details.")

    def set_is_active(self, is_active: int) -> None:
        """Specifies that the class should be defined as "active".

        Args:
            is_active: ``1`` for "active", ``0`` for "sequential".

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsActive(int isActive)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsActive", "isActive", is_active)

    def set_is_behavior_overriden(self, is_behavior_overriden: int) -> None:
        """Specifies whether a class should inherit the statechart behavior of its base class.

        Args:
            is_behavior_overriden: ``1`` to not inherit, ``0`` to inherit.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsBehaviorOverriden(int isBehaviorOverriden)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehaviorOverriden", "isBehaviorOverriden", is_behavior_overriden)

    def set_is_final(self, new_val: int) -> None:
        """Specifies that the class should be a final class.

        Relevant only for Java classes.

        Args:
            new_val: ``1`` to make the class final, ``0`` to make it non-final.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsFinal(int newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsFinal", "isFinal", new_val)

    def update_contained_diagrams_on_server(self, enforce_update: int) -> int:
        """Updates the views on the Rhapsody Model Manager server for all diagrams.

        Args:
            enforce_update: ``0`` to update only if changes were made,
                ``1`` to update regardless.

        Returns:
            The number of views updated, ``0`` if no update needed, ``-1`` on failure.

        Raises:
            RhapsodyRuntimeException: if the server update fails.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::updateContainedDiagramsOnServer(int enforceUpdate)
        """
        return int(AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer(enforce_update)))


AbstractRPModelElement.register_wrapper("Class", RPClass)
