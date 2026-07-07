"""Tests for rhapsody_cli.elements.classifier.RPClassifier."""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit
from rhapsody_cli.models.elements.classifier import RPClassifier
from tests.models.fakes import make_fake_collection, make_fake_element


def test_classifier_is_a_unit() -> None:
    fake = make_fake_element("Class", getName="Widget")
    classifier = RPClassifier(fake)

    assert isinstance(classifier, RPUnit)
    assert classifier.getName() == "Widget"


def test_classifier_add_attribute_wraps_result() -> None:
    fake = make_fake_element("Class")
    attr = make_fake_element("Attribute", getName="count")
    fake.addAttribute.return_value = attr
    classifier = RPClassifier(fake)

    result = classifier.addAttribute("count")

    fake.addAttribute.assert_called_once_with("count")
    assert result.getName() == "count"


def test_classifier_add_operation_wraps_result() -> None:
    fake = make_fake_element("Class")
    op = make_fake_element("Operation", getName="doIt")
    fake.addOperation.return_value = op
    classifier = RPClassifier(fake)

    result = classifier.addOperation("doIt")

    fake.addOperation.assert_called_once_with("doIt")
    assert result.getName() == "doIt"


def test_classifier_get_attributes_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getAttributes.return_value = make_fake_collection(
        [make_fake_element("Attribute", getName="count")]
    )
    classifier = RPClassifier(fake)

    attributes = classifier.getAttributes()

    assert len(attributes) == 1
    assert attributes[0].getName() == "count"


def test_classifier_get_operations_returns_collection() -> None:
    fake = make_fake_element("Class")
    fake.getOperations.return_value = make_fake_collection(
        [make_fake_element("Operation", getName="doIt")]
    )
    classifier = RPClassifier(fake)

    operations = classifier.getOperations()

    assert len(operations) == 1
    assert operations[0].getName() == "doIt"


def test_classifier_add_generalization_delegates_to_com() -> None:
    fake = make_fake_element("Class")
    base = make_fake_element("Class", getName="Base")
    classifier = RPClassifier(fake)

    classifier.addGeneralization(RPClassifier(base))

    fake.addGeneralization.assert_called_once_with(base)


def test_classifier_add_statechart_wraps_result() -> None:
    fake = make_fake_element("Class")
    statechart = make_fake_element("Statechart", getName="Behavior")
    fake.addStatechart.return_value = statechart
    classifier = RPClassifier(fake)

    result = classifier.addStatechart()

    fake.addStatechart.assert_called_once_with()
    assert result.getName() == "Behavior"
