"""Tests for rhapsody_cli.elements.actor.RPActor."""

from __future__ import annotations

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.actor import RPActor
from rhapsody_cli.models.elements.classifier import RPClassifier
from tests.fakes import make_fake_element


def test_actor_is_a_classifier() -> None:
    fake = make_fake_element("Actor", getName="Driver")
    actor = RPActor(fake)

    assert isinstance(actor, RPClassifier)
    assert actor.getName() == "Driver"


def test_actor_add_event_reception_with_event_wraps_result() -> None:
    fake = make_fake_element("Actor")
    event = make_fake_element("Event", getName="Start")
    reception = make_fake_element("EventReception", getName="onStart")
    fake.addEventReceptionWithEvent.return_value = reception
    actor = RPActor(fake)

    from rhapsody_cli.models._core import RPModelElement

    result = actor.addEventReceptionWithEvent("onStart", RPModelElement(event))

    fake.addEventReceptionWithEvent.assert_called_once_with("onStart", event)
    assert result.getName() == "onStart"


def test_actor_get_is_behavior_overridden_delegates_to_com() -> None:
    fake = make_fake_element("Actor", getIsBehaviorOverriden=1)
    actor = RPActor(fake)

    assert actor.getIsBehaviorOverriden() is True


def test_actor_set_is_behavior_overridden_delegates_to_com() -> None:
    fake = make_fake_element("Actor")
    actor = RPActor(fake)

    actor.setIsBehaviorOverriden(False)

    fake.setIsBehaviorOverriden.assert_called_once_with(0)


def test_actor_is_registered_for_meta_class_actor() -> None:
    fake = make_fake_element("Actor", getName="Driver")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPActor)
