"""Wraps ``com.telelogic.rhapsody.core.IRPUseCase``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``: represents a use case in the model."""

    # IRPUseCase method parity checklist:
    # [ ] addDescribingDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] addEventReceptionWithEvent  [ ] impl  [ ] docstring  [ ] test
    # [x] add_extension_point  [x] impl  [x] docstring  [x] test
    # [ ] deleteDescribingDiagram  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteEntryPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] deleteExtensionPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] findEntryPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] findExtensionPoint  [ ] impl  [ ] docstring  [ ] test
    # [ ] getDescribingDiagram  [ ] impl  [ ] docstring  [ ] test
    # [x] get_describing_diagrams  [x] impl  [x] docstring  [x] test
    # [x] get_entry_points  [x] impl  [x] docstring  [x] test
    # [x] get_extension_points  [x] impl  [x] docstring  [x] test
    # [ ] getIsBehaviorOverriden  [ ] impl  [ ] docstring  [ ] test
    # [ ] setIsBehaviorOverriden  [ ] impl  [ ] docstring  [ ] test
    # [ ] updateContainedDiagramsOnServer  [ ] impl  [ ] docstring  [ ] test
    # [inherited] IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClassifier / RPUnit / RPModelElement checklists)
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


AbstractRPModelElement.register_wrapper("UseCase", RPUseCase)
