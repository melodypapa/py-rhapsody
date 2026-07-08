"""Tests for rhapsody_cli.models.elements.requirements.RPAnnotation."""

from rhapsody_cli.models._core import RPCollection, RPUnit, wrap
from rhapsody_cli.models.elements.requirements import RPAnnotation
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_annotation_is_a_unit() -> None:
    fake = make_fake_element("Annotation", getName="Note1")
    annotation = RPAnnotation(fake)

    assert isinstance(annotation, RPUnit)
    assert annotation.getName() == "Note1"


def test_annotation_add_anchor_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    target = make_fake_element("Class", getName="Widget")
    annotation = RPAnnotation(fake)

    annotation.addAnchor(wrap(target))

    fake.addAnchor.assert_called_once_with(target)


def test_annotation_get_anchored_by_me_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = make_fake_element("Annotation")
    fake.getAnchoredByMe.return_value = make_fake_collection([inner])
    annotation = RPAnnotation(fake)

    result = annotation.getAnchoredByMe()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_annotation_get_body_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getBody="Some note text")
    annotation = RPAnnotation(fake)

    assert annotation.getBody() == "Some note text"


def test_annotation_get_specification_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getSpecification="Some spec text")
    annotation = RPAnnotation(fake)

    assert annotation.getSpecification() == "Some spec text"


def test_annotation_get_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getSpecificationRTF="{\\rtf1}")
    annotation = RPAnnotation(fake)

    assert annotation.getSpecificationRTF() == "{\\rtf1}"


def test_annotation_is_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", isSpecificationRTF=1)
    annotation = RPAnnotation(fake)

    assert annotation.isSpecificationRTF() is True


def test_annotation_remove_anchor_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    target = make_fake_element("Class", getName="Widget")
    annotation = RPAnnotation(fake)

    annotation.removeAnchor(wrap(target))

    fake.removeAnchor.assert_called_once_with(target)


def test_annotation_set_body_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setBody("New note text")

    fake.setBody.assert_called_once_with("New note text")


def test_annotation_set_specification_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setSpecification("New spec text")

    fake.setSpecification.assert_called_once_with("New spec text")


def test_annotation_set_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setSpecificationRTF("{\\rtf1 new}")

    fake.setSpecificationRTF.assert_called_once_with("{\\rtf1 new}")
