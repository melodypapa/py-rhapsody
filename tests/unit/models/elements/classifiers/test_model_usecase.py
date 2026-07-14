"""Tests for rhapsody_cli.elements.usecase.RPUseCase."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.classifiers import RPClassifier, RPUseCase
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_usecase_is_a_classifier() -> None:
    fake = make_fake_element("UseCase", getName="Login")
    usecase = RPUseCase(fake)

    assert isinstance(usecase, RPClassifier)
    assert usecase.get_name() == "Login"


def test_usecase_add_extension_point_delegates_to_com() -> None:
    fake = make_fake_element("UseCase")
    usecase = RPUseCase(fake)

    usecase.add_extension_point("failure")

    fake.addExtensionPoint.assert_called_once_with("failure")


def test_usecase_get_extension_points_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    fake.getExtensionPoints.return_value = make_fake_collection(["failure"])
    usecase = RPUseCase(fake)

    points = usecase.get_extension_points()

    assert len(points) == 1
    assert points[0] == "failure"


def test_usecase_get_entry_points_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    fake.getEntryPoints.return_value = make_fake_collection(["start"])
    usecase = RPUseCase(fake)

    points = usecase.get_entry_points()

    assert len(points) == 1
    assert points[0] == "start"


def test_usecase_get_describing_diagrams_returns_collection() -> None:
    fake = make_fake_element("UseCase")
    diagram = make_fake_element("StatechartDiagram", getName="Flow")
    fake.getDescribingDiagrams.return_value = make_fake_collection([diagram])
    usecase = RPUseCase(fake)

    diagrams = usecase.get_describing_diagrams()

    assert len(diagrams) == 1
    assert diagrams[0].get_name() == "Flow"


def test_usecase_is_registered_for_meta_class_usecase() -> None:
    fake = make_fake_element("UseCase", getName="Login")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPUseCase)
