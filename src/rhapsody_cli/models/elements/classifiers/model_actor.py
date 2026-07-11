"""Wraps ``com.telelogic.rhapsody.core.IRPActor``."""

from typing import Any

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
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
        return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        """Checks whether the behavior of the actor is overridden.

        Returns:
            ``True`` if the behavior is overridden, ``False`` otherwise.
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehaviorOverriden", "isBehaviorOverriden"))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        """Sets whether the behavior of the actor is overridden.

        Args:
            is_overridden: ``True`` to mark the behavior as overridden, ``False`` otherwise.
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehaviorOverriden", "isBehaviorOverriden", 1 if is_overridden else 0)


AbstractRPModelElement.register_wrapper("Actor", RPActor)
