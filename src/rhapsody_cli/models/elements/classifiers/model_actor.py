"""Wraps ``com.telelogic.rhapsody.core.IRPActor``."""

from typing import TYPE_CHECKING, cast

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier

if TYPE_CHECKING:
    from rhapsody_cli.models.elements.interactions.model_interactions import RPEventReception


class RPActor(RPClassifier):
    """Wraps ``IRPActor``: represents an actor in the model."""

    # IRPActor method parity checklist:
    # [x] add_event_reception_with_event  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] get_is_behavior_overriden  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [x] set_is_behavior_overriden  [x] impl  [x] docstring  [x] unit test  [ ] integration test
    # [ ] updateContainedDiagramsOnServer  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPClassifier / IRPUnit / IRPModelElement methods (covered by RPClassifier / RPUnit / RPModelElement checklists)
    # No deprecated IRPActor methods.

    def add_event_reception_with_event(self, name: str, event: RPModelElement) -> "RPEventReception":
        """Adds a new event reception to the actor, using the specified event.

        Args:
            name: The name to use for the new event reception.
            event: The event model element that should be associated with the
                new event reception.

        Returns:
            The wrapped ``IRPEventReception`` that was created.

        Raises:
            RhapsodyRuntimeException: if the event reception cannot be added.

        Reference:
            com.telelogic.rhapsody.core.IRPActor::addEventReceptionWithEvent(java.lang.String name, com.telelogic.rhapsody.core.IRPEvent event)
        """
        return cast("RPEventReception", AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com))))

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


AbstractRPModelElement.register_wrapper("Actor", RPActor)
