"""Wraps ``com.telelogic.rhapsody.core.IRPClassifier``."""

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, wrap


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``: the base class for all classifiable elements."""

    def addAttribute(self, name: str) -> Any:
        """Adds a new attribute to the classifier.

        Args:
            name: The name of the new attribute.

        Returns:
            The wrapped ``IRPAttribute`` created.
        """
        return wrap(call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> Any:
        """Adds a new operation to the classifier.

        Args:
            name: The name of the new operation.

        Returns:
            The wrapped ``IRPOperation`` created.
        """
        return wrap(call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        """Returns all attributes defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPAttribute`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getAttributes()))

    def getOperations(self) -> RPCollection:
        """Returns all operations defined on the classifier.

        Returns:
            An ``RPCollection`` of ``IRPOperation`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getOperations()))

    def addGeneralization(self, base_classifier: "RPClassifier") -> None:
        """Adds a generalization relationship from this classifier to another.

        Args:
            base_classifier: The base classifier to generalize from.
        """
        call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> Any:
        """Adds a statechart behavior to this classifier.

        Returns:
            The wrapped ``IRPStatechart`` created.
        """
        return wrap(call_com(lambda: self._com.addStatechart()))
