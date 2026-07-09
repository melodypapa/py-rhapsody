"""Tests for rhapsody_cli.models.elements.requirements.RPRequirement."""

from rhapsody_cli.models.core import wrap
from rhapsody_cli.models.elements.model_requirements import RPAnnotation, RPRequirement
from tests.unit.models.fakes import make_fake_element


def test_requirement_is_an_annotation() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")
    requirement = RPRequirement(fake)

    assert isinstance(requirement, RPAnnotation)
    assert requirement.getName() == "REQ-1"


def test_requirement_get_requirement_id_delegates_to_com() -> None:
    fake = make_fake_element("Requirement", getRequirementID="REQ-001")
    requirement = RPRequirement(fake)

    assert requirement.getRequirementID() == "REQ-001"


def test_requirement_set_requirement_id_delegates_to_com() -> None:
    fake = make_fake_element("Requirement")
    requirement = RPRequirement(fake)

    requirement.setRequirementID("REQ-002")

    fake.setRequirementID.assert_called_once_with("REQ-002")


def test_requirement_is_registered_for_meta_class_requirement() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPRequirement)
