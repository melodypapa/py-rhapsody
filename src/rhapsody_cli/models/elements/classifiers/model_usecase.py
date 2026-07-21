"""Wraps ``com.telelogic.rhapsody.core.IRPUseCase``."""

from typing import TYPE_CHECKING, Optional, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.diagrams import RPDiagram
    from rhapsody_cli.models.elements.interactions.model_interactions import RPEvent, RPEventReception


class RPExtensionPoint(RPModelElement):
    """Wraps extension point concept (returned as IRPModelElement from COM)."""

    pass


AbstractRPModelElement.register_wrapper("ExtensionPoint", RPExtensionPoint)


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``: represents a use case in the model."""

    # IRPUseCase method parity checklist:
    # [ ] add_describing_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] add_event_reception_with_event  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] add_extension_point  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] delete_describing_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_entry_point  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] delete_extension_point  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_entry_point  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] find_extension_point  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] get_describing_diagram  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] get_describing_diagrams  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_entry_points  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_extension_points  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] get_is_behavior_overriden  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] set_is_behavior_overriden  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [ ] update_contained_diagrams_on_server  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] irp_classifier / irp_unit / irp_model_element methods (covered by rp_classifier / rp_unit / rp_model_element checklists)
    # No deprecated IRPUseCase methods.

    def add_extension_point(self, entry_point: str) -> None:
        """Adds an extension point to the use case.

        Args:
            entry_point: The name of the extension point.

        Raises:
            RhapsodyRuntimeException: if the extension point cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::addExtensionPoint(java.lang.String entryPoint)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addExtensionPoint(entry_point))

    def get_extension_points(self) -> RPCollection:
        """Returns all extension points defined on the use case.

        Returns:
            An ``RPCollection`` of extension point strings.

        Raises:
            RhapsodyRuntimeException: if the extension points cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::getExtensionPoints()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getExtensionPoints", "extensionPoints"))

    def get_entry_points(self) -> RPCollection:
        """Returns all entry points defined on the use case.

        Returns:
            An ``RPCollection`` of entry point strings.

        Raises:
            RhapsodyRuntimeException: if the entry points cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::getEntryPoints()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getEntryPoints", "entryPoints"))

    def get_describing_diagrams(self) -> RPCollection:
        """Returns all diagrams that describe this use case.

        Returns:
            An ``RPCollection`` of ``IRPDiagram`` objects.

        Raises:
            RhapsodyRuntimeException: if the describing diagrams cannot be retrieved.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::getDescribingDiagrams()
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDescribingDiagrams", "describingDiagrams"))

    def add_describing_diagram(self, diagram: "RPDiagram") -> None:
        """Adds a diagram to describe this use case.

        Args:
            diagram: The wrapped diagram to add as a describing diagram.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::addDescribingDiagram(com.telelogic.rhapsody.core.IRPDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.addDescribingDiagram(diagram._com))

    def add_event_reception_with_event(self, name: str, event: "RPEvent") -> "RPEventReception":
        """Adds an event reception with the specified event.

        Args:
            name: The name to use for the new event reception.
            event: The wrapped event to use for the event reception.

        Returns:
            The wrapped event reception created.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::addEventReceptionWithEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPEvent event)
        """
        return cast("RPEventReception", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com))))

    def delete_describing_diagram(self, diagram: "RPDiagram") -> None:
        """Deletes a describing diagram from the use case.

        Args:
            diagram: The wrapped diagram to remove.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::deleteDescribingDiagram(com.telelogic.rhapsody.core.IRPDiagram diagram)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteDescribingDiagram(diagram._com))

    def delete_entry_point(self, entry_point: str) -> None:
        """Deletes an entry point from the use case.

        Args:
            entry_point: The name of the entry point to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::deleteEntryPoint(java.lang.String entryPoint)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteEntryPoint(entry_point))

    def delete_extension_point(self, extension_point: str) -> None:
        """Deletes an extension point from the use case.

        Args:
            extension_point: The name of the extension point to delete.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::deleteExtensionPoint(java.lang.String extensionPoint)
        """
        AbstractRPModelElement.call_com(lambda: self._com.deleteExtensionPoint(extension_point))

    def find_entry_point(self, name: str) -> Optional[RPModelElement]:
        """Finds an entry point by name.

        Args:
            name: The name of the entry point to find.

        Returns:
            The wrapped entry point, or None if not found.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::findEntryPoint(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findEntryPoint(name)))

    def find_extension_point(self, name: str) -> Optional[RPModelElement]:
        """Finds an extension point by name.

        Args:
            name: The name of the extension point to find.

        Returns:
            The wrapped extension point, or None if not found.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::findExtensionPoint(java.lang.String name)
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.findExtensionPoint(name)))

    def get_describing_diagram(self, name: str) -> "RPDiagram":
        """Returns a specific describing diagram by name.

        Args:
            name: The name of the diagram to find.

        Returns:
            The wrapped diagram, or None if not found.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::getDescribingDiagram(java.lang.String name)
        """
        return cast("RPDiagram", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.getDescribingDiagram(name))))

    def get_is_behavior_overriden(self) -> int:
        """Checks whether the behavior of this use case is overridden.

        Returns:
            ``1`` if the behavior is overridden, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::getIsBehaviorOverriden()
        """
        return int(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehaviorOverriden", "isBehaviorOverriden"))

    def set_is_behavior_overriden(self, is_overriden: int) -> None:
        """Sets whether the behavior of this use case is overridden.

        Args:
            is_overriden: ``1`` to mark as overridden, ``0`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::setIsBehaviorOverriden(int isBehaviorOverriden)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setIsBehaviorOverriden(is_overriden))

    def update_contained_diagrams_on_server(self) -> None:
        """Updates the contained diagrams on the server.

        This method is relevant when working with Design Manager.

        Reference:
            com.telelogic.rhapsody.core.IRPUseCase::updateContainedDiagramsOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer())


AbstractRPModelElement.register_wrapper("UseCase", RPUseCase)
