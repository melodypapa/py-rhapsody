"""Tests for rhapsody_cli.elements.class_.RPClass."""

import pytest

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier
from tests.unit.models.fakes import make_fake_element


def test_class_is_a_classifier() -> None:
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)

    assert isinstance(klass, RPClassifier)
    assert klass.get_name() == "Widget"


def test_class_add_superclass_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)

    klass.add_superclass(RPClass(base))

    fake.addSuperclass.assert_called_once_with(base)


def test_class_add_constructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    ctor = make_fake_element("Operation", getName="Widget")
    fake.addConstructor.return_value = ctor
    klass = RPClass(fake)

    result = klass.add_constructor("int x")

    fake.addConstructor.assert_called_once_with("int x")
    assert result.get_name() == "Widget"


def test_class_add_destructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    dtor = make_fake_element("Operation", getName="~Widget")
    fake.addDestructor.return_value = dtor
    klass = RPClass(fake)

    result = klass.add_destructor()

    fake.addDestructor.assert_called_once_with()
    assert result.get_name() == "~Widget"


def test_class_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)

    assert klass.get_is_abstract() is True


def test_class_add_class_nested_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Inner")
    fake.addClass.return_value = nested
    klass = RPClass(fake)

    result = klass.add_class("Inner")

    fake.addClass.assert_called_once_with("Inner")
    assert result.get_name() == "Inner"


def test_class_is_registered_for_meta_class_class() -> None:
    fake = make_fake_element("Class", getName="Widget")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPClass)


def test_class_add_event_reception_wraps_result() -> None:
    fake = make_fake_element("Class")
    reception = make_fake_element("EventReception", getName="onEvent")
    fake.addEventReception.return_value = reception
    klass = RPClass(fake)

    result = klass.add_event_reception("onEvent")

    fake.addEventReception.assert_called_once_with("onEvent")
    assert result.get_name() == "onEvent"


def test_class_add_event_reception_with_event_unwraps_and_wraps() -> None:
    fake = make_fake_element("Class")
    event = make_fake_element("Event", getName="Tick")
    reception = make_fake_element("EventReception", getName="onTick")
    fake.addEventReceptionWithEvent.return_value = reception
    klass = RPClass(fake)

    result = klass.add_event_reception_with_event("onTick", AbstractRPModelElement.wrap(event))

    fake.addEventReceptionWithEvent.assert_called_once_with("onTick", event)
    assert result.get_name() == "onTick"


def test_class_add_link_unwraps_all_args_and_wraps_result() -> None:
    fake = make_fake_element("Class")
    from_part = make_fake_element("Instance", getName="p1")
    to_part = make_fake_element("Instance", getName="p2")
    assoc = make_fake_element("Relation", getName="r1")
    from_port = make_fake_element("Port", getName="port1")
    to_port = make_fake_element("Port", getName="port2")
    link = make_fake_element("Link", getName="link1")
    fake.addLink.return_value = link
    klass = RPClass(fake)

    result = klass.add_link(
        AbstractRPModelElement.wrap(from_part), AbstractRPModelElement.wrap(to_part), AbstractRPModelElement.wrap(assoc), AbstractRPModelElement.wrap(from_port), AbstractRPModelElement.wrap(to_port)
    )

    fake.addLink.assert_called_once_with(from_part, to_part, assoc, from_port, to_port)
    assert result.get_name() == "link1"


def test_class_add_link_to_part_via_port_unwraps_and_wraps() -> None:
    fake = make_fake_element("Class")
    to_part = make_fake_element("Instance", getName="p1")
    part_port = make_fake_element("Instance", getName="pp")
    class_port = make_fake_element("Instance", getName="cp")
    assoc = make_fake_element("Relation", getName="r1")
    link = make_fake_element("Link", getName="link1")
    fake.addLinkToPartViaPort.return_value = link
    klass = RPClass(fake)

    result = klass.add_link_to_part_via_port(AbstractRPModelElement.wrap(to_part), AbstractRPModelElement.wrap(part_port), AbstractRPModelElement.wrap(class_port), AbstractRPModelElement.wrap(assoc))

    fake.addLinkToPartViaPort.assert_called_once_with(to_part, part_port, class_port, assoc)
    assert result.get_name() == "link1"


def test_class_add_reception_wraps_result() -> None:
    fake = make_fake_element("Class")
    reception = make_fake_element("EventReception", getName="onSignal")
    fake.addReception.return_value = reception
    klass = RPClass(fake)

    result = klass.add_reception("onSignal")

    fake.addReception.assert_called_once_with("onSignal")
    assert result.get_name() == "onSignal"


def test_class_add_triggered_operation_wraps_result() -> None:
    fake = make_fake_element("Class")
    op = make_fake_element("Operation", getName="handle")
    fake.addTriggeredOperation.return_value = op
    klass = RPClass(fake)

    result = klass.add_triggered_operation("handle")

    fake.addTriggeredOperation.assert_called_once_with("handle")
    assert result.get_name() == "handle"


def test_class_add_type_wraps_result() -> None:
    fake = make_fake_element("Class")
    typ = make_fake_element("Type", getName="Color")
    fake.addType.return_value = typ
    klass = RPClass(fake)

    result = klass.add_type("Color")

    fake.addType.assert_called_once_with("Color")
    assert result.get_name() == "Color"


def test_class_delete_class_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.delete_class("Inner")

    fake.deleteClass.assert_called_once_with("Inner")


def test_class_delete_constructor_unwraps_arg() -> None:
    fake = make_fake_element("Class")
    ctor = make_fake_element("Operation", getName="Widget")
    klass = RPClass(fake)

    klass.delete_constructor(AbstractRPModelElement.wrap(ctor))

    fake.deleteConstructor.assert_called_once_with(ctor)


def test_class_delete_destructor_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.delete_destructor()

    fake.deleteDestructor.assert_called_once_with()


def test_class_delete_event_reception_unwraps_arg() -> None:
    fake = make_fake_element("Class")
    reception = make_fake_element("EventReception", getName="onEvent")
    klass = RPClass(fake)

    klass.delete_event_reception(AbstractRPModelElement.wrap(reception))

    fake.deleteEventReception.assert_called_once_with(reception)


def test_class_delete_reception_unwraps_arg() -> None:
    fake = make_fake_element("Class")
    reception = make_fake_element("EventReception", getName="onSignal")
    klass = RPClass(fake)

    klass.delete_reception(AbstractRPModelElement.wrap(reception))

    fake.deleteReception.assert_called_once_with(reception)


def test_class_delete_superclass_unwraps_arg() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)

    klass.delete_superclass(RPClass(base))

    fake.deleteSuperclass.assert_called_once_with(base)


def test_class_delete_type_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.delete_type("Color")

    fake.deleteType.assert_called_once_with("Color")


def test_class_get_is_active_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsActive=1)
    klass = RPClass(fake)

    assert klass.get_is_active() == 1


def test_class_get_is_behavior_overriden_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsBehaviorOverriden=0)
    klass = RPClass(fake)

    assert klass.get_is_behavior_overriden() == 0


def test_class_get_is_composite_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsComposite=1)
    klass = RPClass(fake)

    assert klass.get_is_composite() == 1


def test_class_get_is_final_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsFinal=0)
    klass = RPClass(fake)

    assert klass.get_is_final() == 0


def test_class_get_is_reactive_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsReactive=1)
    klass = RPClass(fake)

    assert klass.get_is_reactive() == 1


def test_class_set_is_abstract_raises_not_implemented() -> None:
    """RPClass.set_is_abstract is marked unimplemented: Rhapsody2.Application.1 accepts the
    write without error but never persists it, so it raises rather than silently no-opping."""
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    with pytest.raises(NotImplementedError):
        klass.set_is_abstract(1)

    fake.setIsAbstract.assert_not_called()


def test_class_set_is_active_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.set_is_active(0)

    fake.setIsActive.assert_called_once_with(0)


def test_class_set_is_behavior_overriden_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.set_is_behavior_overriden(1)

    fake.setIsBehaviorOverriden.assert_called_once_with(1)


def test_class_set_is_final_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    klass = RPClass(fake)

    klass.set_is_final(1)

    fake.setIsFinal.assert_called_once_with(1)


def test_class_update_contained_diagrams_on_server_delegates_to_com() -> None:
    fake = make_fake_element("Class", updateContainedDiagramsOnServer=3)
    klass = RPClass(fake)

    assert klass.update_contained_diagrams_on_server(1) == 3

    fake.updateContainedDiagramsOnServer.assert_called_once_with(1)
