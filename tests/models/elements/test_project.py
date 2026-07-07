"""Tests for rhapsody_cli.elements.project.RPProject."""

from __future__ import annotations

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from tests.models.fakes import make_fake_collection, make_fake_element


def test_project_is_a_package() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPPackage)
    assert project.getName() == "MyProject"


def test_project_add_package_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    new_pkg = make_fake_element("Package", getName="NewPkg")
    fake.addPackage.return_value = new_pkg
    project = RPProject(fake)

    result = project.addPackage("NewPkg")

    fake.addPackage.assert_called_once_with("NewPkg")
    assert result.getName() == "NewPkg"


def test_project_close_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.close()

    fake.close.assert_called_once_with()


def test_project_become_active_project_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.becomeActiveProject()

    fake.becomeActiveProject.assert_called_once_with()


def test_project_find_component_wraps_result() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Component", getName="Comp1")
    fake.findComponent.return_value = found
    project = RPProject(fake)

    result = project.findComponent("Comp1")

    fake.findComponent.assert_called_once_with("Comp1")
    assert result.getName() == "Comp1"


def test_project_get_packages_returns_collection() -> None:
    from rhapsody_cli.models._core import RPCollection

    fake = make_fake_element("Project")
    fake.getPackages.return_value = make_fake_collection(
        [make_fake_element("Package", getName="P1")]
    )
    project = RPProject(fake)

    packages = project.getPackages()

    assert isinstance(packages, RPCollection)
    assert len(packages) == 1
    assert packages[0].getName() == "P1"


def test_project_is_registered_for_meta_class_project() -> None:
    from rhapsody_cli.models._core import wrap

    fake = make_fake_element("Project", getName="MyProject")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPProject)
