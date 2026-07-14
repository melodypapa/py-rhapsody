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


# --- New tests for RPProject ---
def test_project_add_component_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    comp = make_fake_element("Component", getName="Comp1")
    fake.addComponent.return_value = comp
    project = RPProject(fake)

    result = project.add_component("Comp1")

    fake.addComponent.assert_called_once_with("Comp1")
    assert result.get_name() == "Comp1"


def test_project_delete_component_delegates_to_com() -> None:
    from rhapsody_cli.models.core import RPUnit

    fake = make_fake_element("Project")
    project = RPProject(fake)
    comp_fake = make_fake_element("Component", getName="ToDelete")

    project.delete_component(RPUnit(comp_fake))

    fake.deleteComponent.assert_called_once_with(comp_fake)


def test_project_add_node_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.addNode.return_value = node
    project = RPProject(fake)

    result = project.add_node("Node1")

    fake.addNode.assert_called_once_with("Node1")
    assert result.get_name() == "Node1"


def test_project_get_nodes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.getNodes.return_value = make_fake_collection([node])
    project = RPProject(fake)

    result = project.get_nodes()

    assert isinstance(result, RPCollection)


def test_project_find_node_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    node = make_fake_element("Node", getName="Node1")
    fake.findNode.return_value = node
    project = RPProject(fake)

    result = project.find_node("Node1")

    fake.findNode.assert_called_once_with("Node1")
    assert result.get_name() == "Node1"


def test_project_add_configuration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.addConfiguration.return_value = config
    project = RPProject(fake)

    result = project.add_configuration("Default")

    fake.addConfiguration.assert_called_once_with("Default")
    assert result.get_name() == "Default"


def test_project_get_configurations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.getConfigurations.return_value = make_fake_collection([config])
    project = RPProject(fake)

    result = project.get_configurations()

    assert isinstance(result, RPCollection)


def test_project_find_configuration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    config = make_fake_element("Configuration", getName="Default")
    fake.findConfiguration.return_value = config
    project = RPProject(fake)

    result = project.find_configuration("Default")

    fake.findConfiguration.assert_called_once_with("Default")
    assert result.get_name() == "Default"


def test_project_add_collaboration_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    collab = make_fake_element("Collaboration", getName="Collab1")
    fake.addCollaboration.return_value = collab
    project = RPProject(fake)

    result = project.add_collaboration("Collab1")

    fake.addCollaboration.assert_called_once_with("Collab1")
    assert result.get_name() == "Collab1"


def test_project_get_collaborations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    collab = make_fake_element("Collaboration", getName="Collab1")
    fake.getCollaborations.return_value = make_fake_collection([collab])
    project = RPProject(fake)

    result = project.get_collaborations()

    assert isinstance(result, RPCollection)


def test_project_get_all_stereotypes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Project")
    st = make_fake_element("Stereotype", getName="MyStereotype")
    fake.getAllStereotypes.return_value = make_fake_collection([st])
    project = RPProject(fake)

    result = project.get_all_stereotypes()

    assert isinstance(result, RPCollection)


def test_project_save_as_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    project = RPProject(fake)

    project.save_as("C:/path/to/project.rpy")

    fake.saveAs.assert_called_once_with("C:/path/to/project.rpy")


def test_project_find_element_by_binary_id_delegates_to_com() -> None:
    fake = make_fake_element("Project")
    found = make_fake_element("Class", getName="MyClass")
    fake.findElementByBinaryID.return_value = found
    project = RPProject(fake)

    result = project.find_element_by_binary_id("abc123")

    fake.findElementByBinaryID.assert_called_once_with("abc123")
    assert result.get_name() == "MyClass"
