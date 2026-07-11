"""Wraps ``com.telelogic.rhapsody.core.IRPUseCase``."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``: represents a use case in the model."""

    def addExtensionPoint(self, entry_point: str) -> None:
        """Adds an extension point to the use case.

        Args:
            entry_point: The name of the extension point.
        """
        AbstractRPModelElement.call_com(lambda: self._com.addExtensionPoint(entry_point))

    def getExtensionPoints(self) -> RPCollection:
        """Returns all extension points defined on the use case.

        Returns:
            An ``RPCollection`` of extension point strings.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getExtensionPoints", "extensionPoints"))

    def getEntryPoints(self) -> RPCollection:
        """Returns all entry points defined on the use case.

        Returns:
            An ``RPCollection`` of entry point strings.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getEntryPoints", "entryPoints"))

    def getDescribingDiagrams(self) -> RPCollection:
        """Returns all diagrams that describe this use case.

        Returns:
            An ``RPCollection`` of ``IRPDiagram`` objects.
        """
        return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getDescribingDiagrams", "describingDiagrams"))


AbstractRPModelElement.register_wrapper("UseCase", RPUseCase)
