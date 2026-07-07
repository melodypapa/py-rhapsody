"""Tests for the public rhapsody_cli package API surface."""

from __future__ import annotations

import importlib

import rhapsody_cli
from rhapsody_cli.models._core import wrap
from tests.models.fakes import make_fake_element


def test_rhapsody_application_is_exported() -> None:
    assert rhapsody_cli.RhapsodyApplication is not None


def test_exceptions_are_exported() -> None:
    assert rhapsody_cli.RhapsodyConnectionError is not None
    assert rhapsody_cli.RhapsodyRuntimeException is not None


def test_importing_package_registers_all_core_element_wrappers() -> None:
    for meta_class, expected_name in [
        ("Project", "RPProject"),
        ("Package", "RPPackage"),
        ("Class", "RPClass"),
        ("Attribute", "RPAttribute"),
        ("Operation", "RPOperation"),
        ("Actor", "RPActor"),
        ("UseCase", "RPUseCase"),
        ("Instance", "RPInstance"),
        ("Statechart", "RPStatechart"),
        ("Requirement", "RPRequirement"),
        ("ActivityDiagram", "RPDiagram"),
    ]:
        fake = make_fake_element(meta_class, getName="X")
        wrapped = wrap(fake)
        assert type(wrapped).__name__ == expected_name, meta_class


def test_legacy_element_modules_still_import_their_original_wrapper_classes() -> None:
    for module_name, class_name in [
        ("rhapsody_cli.models.elements.actor", "RPActor"),
        ("rhapsody_cli.models.elements.attribute", "RPAttribute"),
        ("rhapsody_cli.models.elements.class_", "RPClass"),
        ("rhapsody_cli.models.elements.classifier", "RPClassifier"),
        ("rhapsody_cli.models.elements.diagram", "RPDiagram"),
        ("rhapsody_cli.models.elements.instance", "RPInstance"),
        ("rhapsody_cli.models.elements.operation", "RPOperation"),
        ("rhapsody_cli.models.elements.package", "RPPackage"),
        ("rhapsody_cli.models.elements.project", "RPProject"),
        ("rhapsody_cli.models.elements.requirement", "RPRequirement"),
        ("rhapsody_cli.models.elements.statechart", "RPStatechart"),
        ("rhapsody_cli.models.elements.usecase", "RPUseCase"),
    ]:
        module = importlib.import_module(module_name)

        assert getattr(module, class_name).__name__ == class_name
