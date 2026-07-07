"""Tests for rhapsody_cli.elements.class_.RPClass."""

from __future__ import annotations

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier
from tests.models.fakes import make_fake_element


def test_class_is_a_classifier() -> None:
    fake = make_fake_element("Class", getName="Widget")
    klass = RPClass(fake)

    assert isinstance(klass, RPClassifier)
    assert klass.getName() == "Widget"


def test_class_add_superclass_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    klass = RPClass(fake)

    klass.addSuperclass(RPClass(base))

    fake.addSuperclass.assert_called_once_with(base)


def test_class_add_constructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    ctor = make_fake_element("Operation", getName="Widget")
    fake.addConstructor.return_value = ctor
    klass = RPClass(fake)

    result = klass.addConstructor("int x")

    fake.addConstructor.assert_called_once_with("int x")
    assert result.getName() == "Widget"


def test_class_add_destructor_wraps_result() -> None:
    fake = make_fake_element("Class")
    dtor = make_fake_element("Operation", getName="~Widget")
    fake.addDestructor.return_value = dtor
    klass = RPClass(fake)

    result = klass.addDestructor()

    fake.addDestructor.assert_called_once_with()
    assert result.getName() == "~Widget"


def test_class_get_is_abstract_delegates_to_com() -> None:
    fake = make_fake_element("Class", getIsAbstract=1)
    klass = RPClass(fake)

    assert klass.getIsAbstract() is True


def test_class_add_class_nested_wraps_result() -> None:
    fake = make_fake_element("Class")
    nested = make_fake_element("Class", getName="Inner")
    fake.addClass.return_value = nested
    klass = RPClass(fake)

    result = klass.addClass("Inner")

    fake.addClass.assert_called_once_with("Inner")
    assert result.getName() == "Inner"


def test_class_is_registered_for_meta_class_class() -> None:
    fake = make_fake_element("Class", getName="Widget")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPClass)
