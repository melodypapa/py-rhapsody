"""Wraps ``com.telelogic.rhapsody.core.IRPActor``."""

from typing import Any

from rhapsody_cli.models._core import RPModelElement, call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier


class RPActor(RPClassifier):
    """Wraps ``IRPActor``: represents an actor in the model."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        """Adds a new event reception to the actor.

        Args:
            name: The name of the event reception.
            event: The event model element associated with the reception.

        Returns:
            The wrapped ``IRPEventReception`` created.
        """
        return wrap(call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        """Checks whether the behavior of the actor is overridden.

        Returns:
            ``True`` if the behavior is overridden, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        """Sets whether the behavior of the actor is overridden.

        Args:
            is_overridden: ``True`` to mark the behavior as overridden, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0))


register_wrapper("Actor", RPActor)
