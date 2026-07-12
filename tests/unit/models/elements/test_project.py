"""Tests for rhapsody_cli.elements.project.RPProject."""

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_project_is_a_package() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPPackage)
    assert project.get_name() == "MyProject"


def test_project_add_package_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    new_pkg = make_fake_element("Package", getName="NewPkg")
    fake.addPackage.return_value = new_pkg
    project = RPProject(fake)

    result = project.add_package("NewPkg")

    fake.addPackage.assert_called_once_with("NewPkg")
    assert result.get_name() == "NewPkg"


def test_project_close_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.close()

    fake.close.assert_called_once_with()


def test_project_become_active_project_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.become_active_project()

    fake.becomeActiveProject.assert_called_once_with()


def test_project_find_component_wraps_result() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Component", getName="Comp1")
    fake.findComponent.return_value = found
    project = RPProject(fake)

    result = project.find_component("Comp1")

    fake.findComponent.assert_called_once_with("Comp1")
    assert result.get_name() == "Comp1"


def test_project_get_packages_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    fake.getPackages.return_value = make_fake_collection([make_fake_element("Package", getName="P1")])
    project = RPProject(fake)

    packages = project.get_packages()

    assert isinstance(packages, RPCollection)
    assert len(packages) == 1
    assert packages[0].get_name() == "P1"


def test_project_is_registered_for_meta_class_project() -> None:
    from rhapsody_cli.models.core import AbstractRPModelElement

    fake = make_fake_element("Project", getName="MyProject")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPProject)


def test_project_add_class_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    cls = make_fake_element("Class", getName="Class1")
    fake.addClass.return_value = cls
    project = RPProject(fake)

    result = project.add_class("Class1")

    fake.addClass.assert_called_once_with("Class1")
    assert result.get_name() == "Class1"


def test_project_add_actor_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    actor = make_fake_element("Actor", getName="Actor1")
    fake.addActor.return_value = actor
    project = RPProject(fake)

    result = project.add_actor("Actor1")

    fake.addActor.assert_called_once_with("Actor1")
    assert result.get_name() == "Actor1"


def test_project_get_components_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    comp1 = make_fake_element("Component", getName="Comp1")
    fake.getComponents.return_value = make_fake_collection([comp1])
    project = RPProject(fake)

    result = project.get_components()

    assert isinstance(result, RPCollection)


def test_project_find_by_name_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findByName.return_value = found
    project = RPProject(fake)

    result = project.find_by_name("MyClass")

    fake.findByName.assert_called_once_with("MyClass")
    assert result.get_name() == "MyClass"


def test_project_find_by_meta_class_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    cls1 = make_fake_element("Class", getName="Class1")
    fake.findByMetaClass.return_value = make_fake_collection([cls1])
    project = RPProject(fake)

    result = project.find_by_meta_class("Class")

    assert isinstance(result, RPCollection)


def test_project_find_element_by_guid_returns_wrapped_element() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findElementByGUID.return_value = found
    project = RPProject(fake)

    result = project.find_element_by_guid("12345")

    fake.findElementByGUID.assert_called_once_with("12345")
    assert result.get_name() == "MyClass"


def test_project_is_dirty_returns_int() -> None:
    fake = make_fake_element("Project", getIsDirty=1)
    project = RPProject(fake)

    result = project.get_is_dirty()

    fake.getIsDirty.assert_called_once_with()
    assert result == 1


def test_project_set_dirty_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.set_dirty(1)

    fake.setDirty.assert_called_once_with(1)
