"""Wraps ``com.telelogic.rhapsody.core.IRPClass``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

# IRPClass method parity checklist:
# [x] addClass                 [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addConstructor           [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addDestructor            [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addSuperclass            [x] impl  [x] docstring  [x] test   (already implemented)
# [x] getIsAbstract            [x] impl  [x] docstring  [x] test   (already implemented)
# [x] addEventReception        [x] impl  [x] docstring  [x] test
# [x] addEventReceptionWithEvent [x] impl [x] docstring [x] test
# [x] addLink                  [x] impl  [x] docstring  [x] test
# [x] addLinkToPartViaPort     [x] impl  [x] docstring  [x] test
# [x] addReception             [x] impl  [x] docstring  [x] test
# [x] addTriggeredOperation    [x] impl  [x] docstring  [x] test
# [x] addType                  [x] impl  [x] docstring  [x] test
# [x] deleteClass              [x] impl  [x] docstring  [x] test
# [x] deleteConstructor        [x] impl  [x] docstring  [x] test
# [x] deleteDestructor         [x] impl  [x] docstring  [x] test
# [x] deleteEventReception     [x] impl  [x] docstring  [x] test
# [x] deleteReception          [x] impl  [x] docstring  [x] test
# [x] deleteSuperclass         [x] impl  [x] docstring  [x] test
# [x] deleteType               [x] impl  [x] docstring  [x] test
# [x] getIsActive              [x] impl  [x] docstring  [x] test
# [x] getIsBehaviorOverriden   [x] impl  [x] docstring  [x] test
# [x] getIsComposite           [x] impl  [x] docstring  [x] test
# [x] getIsFinal               [x] impl  [x] docstring  [x] test
# [x] getIsReactive            [x] impl  [x] docstring  [x] test
# [x] setIsAbstract            [x] impl  [x] docstring  [x] test
# [x] setIsActive              [x] impl  [x] docstring  [x] test
# [x] setIsBehaviorOverriden   [x] impl  [x] docstring  [x] test
# [x] setIsFinal               [x] impl  [x] docstring  [x] test
# [x] updateContainedDiagramsOnServer [x] impl [x] docstring [x] test
# No deprecated methods in IRPClass.


class RPClass(RPClassifier):
    """Wraps ``IRPClass``: represents a class in the model."""

    def addSuperclass(self, super_class: "RPClass") -> None:
        """Adds a superclass to this class.

        Args:
            super_class: The class to inherit from.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addSuperclass(com.telelogic.rhapsody.core.IRPClass superClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        """Adds a constructor operation to this class.

        Args:
            arguments_data: The argument specification for the constructor.

        Returns:
            The wrapped ``IRPOperation`` for the new constructor.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addConstructor(java.lang.String argumentsData)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        """Adds a destructor operation to this class.

        Returns:
            The wrapped ``IRPOperation`` for the new destructor.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addDestructor()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        """Checks whether this class is abstract.

        Returns:
            ``True`` if the class is abstract, ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsAbstract()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsAbstract", "isAbstract"))

    def addClass(self, name: str) -> Any:
        """Adds a nested class to this class.

        Args:
            name: The name of the new nested class.

        Returns:
            The wrapped ``IRPClass`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addClass(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addClass(name)))

    def addEventReception(self, name: str) -> Any:
        """Adds an event reception to the current class.

        It is preferable to use :meth:`addReception` instead.

        Args:
            name: The name to use for the new event reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addEventReception(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReception(name)))

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        """Adds a new event reception, using the specified event.

        Args:
            name: The name to use for the new event reception.
            event: The event that should be associated with the new event reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Raises:
            RhapsodyRuntimeException: if the event reception cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addEventReceptionWithEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPEvent event)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def addLink(
        self,
        from_part: RPModelElement,
        to_part: RPModelElement,
        assoc: RPModelElement,
        from_port: RPModelElement,
        to_port: RPModelElement,
    ) -> Any:
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
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLink(from_part._com, to_part._com, assoc._com, from_port._com, to_port._com)))

    def addLinkToPartViaPort(
        self,
        to_part: RPModelElement,
        part_port: RPModelElement,
        class_port: RPModelElement,
        assoc: RPModelElement,
    ) -> Any:
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
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addLinkToPartViaPort(to_part._com, part_port._com, class_port._com, assoc._com)))

    def addReception(self, name: str) -> Any:
        """Adds a reception to the current class.

        Args:
            name: The name to use for the new reception.

        Returns:
            The wrapped ``IRPEventReception`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addReception(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addReception(name)))

    def addTriggeredOperation(self, name: str) -> Any:
        """Adds a new triggered operation to the current class.

        Args:
            name: The name to use for the new triggered operation.

        Returns:
            The wrapped ``IRPOperation`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addTriggeredOperation(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addTriggeredOperation(name)))

    def addType(self, name: str) -> Any:
        """Adds a new type to the current class.

        Args:
            name: The name to use for the new type.

        Returns:
            The wrapped ``IRPType`` created.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::addType(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addType(name)))

    def deleteClass(self, name: str) -> None:
        """Deletes the specified class from the current class.

        Args:
            name: The name of the class that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteClass(java.lang.String name)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteClass(name))

    def deleteConstructor(self, constructor: RPModelElement) -> None:
        """Deletes the specified constructor from the current class.

        Args:
            constructor: The constructor that should be deleted (an ``IRPOperation``).

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteConstructor(com.telelogic.rhapsody.core.IRPOperation constructor)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteConstructor(constructor._com))

    def deleteDestructor(self) -> None:
        """Deletes the destructor for the class.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteDestructor()
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteDestructor())

    def deleteEventReception(self, p_val: RPModelElement) -> None:
        """Deletes the specified event reception.

        It is preferable to use :meth:`deleteReception` instead.

        Args:
            p_val: The reception that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteEventReception(com.telelogic.rhapsody.core.IRPEventReception pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteEventReception(p_val._com))

    def deleteReception(self, p_val: RPModelElement) -> None:
        """Deletes the specified reception from the current class.

        Args:
            p_val: The reception that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteReception(com.telelogic.rhapsody.core.IRPEventReception pVal)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteReception(p_val._com))

    def deleteSuperclass(self, super_class: "RPClass") -> None:
        """Removes the inheritance relationship with the specified base class.

        Args:
            super_class: The base class of the current class.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteSuperclass(com.telelogic.rhapsody.core.IRPClass superClass)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteSuperclass(super_class._com))

    def deleteType(self, name: str) -> None:
        """Deletes the specified type from the current class.

        Args:
            name: The name of the type that should be deleted.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::deleteType(java.lang.String name)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteType(name))

    def getIsActive(self) -> int:
        """Checks whether the class was defined as "active".

        "Active" means that during execution it runs on its own thread.

        Returns:
            ``1`` if the class is "active", ``0`` if it is "sequential".

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsActive()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsActive", "isActive"))

    def getIsBehaviorOverriden(self) -> int:
        """Checks whether a class does not inherit the behavior of its base class statechart.

        Returns:
            ``1`` if the class does not inherit this behavior, ``0`` if it does.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsBehaviorOverriden()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehaviorOverriden", "isBehaviorOverriden"))

    def getIsComposite(self) -> int:
        """Checks whether the class is a composite class.

        Returns:
            ``1`` if the class is a composite class, ``0`` if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsComposite()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsComposite", "isComposite"))

    def getIsFinal(self) -> int:
        """Checks whether the class is a final class.

        Relevant only for Java classes.

        Returns:
            ``1`` if the class is final, ``0`` if not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsFinal()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsFinal", "isFinal"))

    def getIsReactive(self) -> int:
        """Checks whether the class is a reactive class.

        A reactive class has a statechart or activity diagram so that it
        reacts to events.

        Returns:
            ``1`` if the class is reactive, ``0`` if it is not.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::getIsReactive()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsReactive", "isReactive"))

    def setIsAbstract(self, is_abstract: int) -> None:
        """Specifies that the class should be abstract.

        Args:
            is_abstract: ``1`` to make the class abstract, ``0`` to make it non-abstract.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsAbstract(int isAbstract)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsAbstract", "isAbstract", is_abstract)

    def setIsActive(self, is_active: int) -> None:
        """Specifies that the class should be defined as "active".

        Args:
            is_active: ``1`` for "active", ``0`` for "sequential".

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsActive(int isActive)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsActive", "isActive", is_active)

    def setIsBehaviorOverriden(self, is_behavior_overriden: int) -> None:
        """Specifies whether a class should inherit the statechart behavior of its base class.

        Args:
            is_behavior_overriden: ``1`` to not inherit, ``0`` to inherit.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsBehaviorOverriden(int isBehaviorOverriden)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehaviorOverriden", "isBehaviorOverriden", is_behavior_overriden)

    def setIsFinal(self, new_val: int) -> None:
        """Specifies that the class should be a final class.

        Relevant only for Java classes.

        Args:
            new_val: ``1`` to make the class final, ``0`` to make it non-final.

        Reference:
            com.telelogic.rhapsody.core.IRPClass::setIsFinal(int newVal)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsFinal", "isFinal", new_val)

    def updateContainedDiagramsOnServer(self, enforce_update: int) -> int:
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
