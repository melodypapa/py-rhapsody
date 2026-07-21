"""Wraps ``com.telelogic.rhapsody.core.IRPActor``."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.interactions.model_interactions import RPEvent, RPEventReception


class RPActor(RPClassifier):
    """Wraps ``IRPActor``: represents an actor in the model."""

    # IRPActor method parity checklist:
    # [x] add_event_reception_with_event  [x] impl (raises NotImplementedError)  [x] docstring  [x] unit test  [x] integration test  (COM method not exposed)
    # [x] get_is_behavior_overriden  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] set_is_behavior_overriden  [x] impl  [x] docstring  [x] unit test  [x] integration test
    # [x] update_contained_diagrams_on_server  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [inherited] irp_classifier / irp_unit / irp_model_element methods (covered by rp_classifier / rp_unit / rp_model_element checklists)
    # No deprecated IRPActor methods.

    def add_event_reception_with_event(self, name: str, event: "RPEvent") -> "RPEventReception":
        """Adds a new event reception to the actor, using the specified event.

        Note: ``addEventReceptionWithEvent`` is not exposed in the Rhapsody COM
        automation type library. This method raises ``NotImplementedError`` to
        prevent its use.

        Args:
            name: The name to use for the new event reception.
            event: The event model element that should be associated with the
                new event reception.

        Returns:
            The wrapped ``IRPEventReception`` that was created.

        Raises:
            NotImplementedError: Always raised, as this method is not exposed
                in the Rhapsody COM type library.

        Reference:
            com.telelogic.rhapsody.core.IRPActor::addEventReceptionWithEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPEvent event)
        """
        raise NotImplementedError(
            "addEventReceptionWithEvent is not exposed in the Rhapsody COM automation type library. " "Use add_event_reception(name) instead and set the event via the reception object."
        )

    def get_is_behavior_overriden(self) -> bool:
        """Checks whether the actor overrides the behavior defined in its base class's statechart.

        When you create a statechart for an actor, by default it inherits the
        behavior defined in the statechart of its base class. Rhapsody lets you
        specify that the actor should not inherit this behavior; this method
        reports whether that option has been exercised.

        Returns:
            ``True`` if the actor does not inherit its base class's statechart
            behavior (i.e. behavior is overridden), ``False`` otherwise.

        Reference:
            com.telelogic.rhapsody.core.IRPActor::getIsBehaviorOverriden()
        """
        return bool(AbstractRPModelElement._get_method_or_property(self._com, "getIsBehaviorOverriden", "isBehaviorOverriden"))

    def set_is_behavior_overriden(self, is_overridden: bool) -> None:
        """Specifies whether the actor should inherit the behavior defined in its base class's statechart.

        When you create a statechart for an actor, by default it inherits the
        behavior defined in the statechart of its base class. Rhapsody lets you
        specify that the actor should not inherit this behavior.

        Args:
            is_overridden: ``True`` to stop the actor inheriting its base
                class's statechart behavior (override it), ``False`` to inherit.

        Reference:
            com.telelogic.rhapsody.core.IRPActor::setIsBehaviorOverriden(int)
        """
        AbstractRPModelElement._set_method_or_property(self._com, "setIsBehaviorOverriden", "isBehaviorOverriden", 1 if is_overridden else 0)

    def update_contained_diagrams_on_server(self) -> None:
        """Updates the contained diagrams on the remote requirements server.

        Raises:
            RhapsodyRuntimeException: If the operation fails.

        Reference:
            com.telelogic.rhapsody.core.IRPActor::updateContainedDiagramsOnServer()
        """
        AbstractRPModelElement.call_com(lambda: self._com.updateContainedDiagramsOnServer())


AbstractRPModelElement.register_wrapper("Actor", RPActor)
