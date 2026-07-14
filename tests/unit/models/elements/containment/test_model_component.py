"""Tests for rhapsody_cli.models.elements.containment.RPComponent."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit
from rhapsody_cli.models.elements.containment import RPComponent, RPConfiguration
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_component_is_a_unit() -> None:
    fake = make_fake_element("Component", getName="Comp1")
    component = RPComponent(fake)

    assert isinstance(component, RPUnit)
    assert component.get_name() == "Comp1"


def test_component_is_registered_for_meta_class_component() -> None:
    fake = make_fake_element("Component", getName="Comp1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPComponent)


# Tests for methods from Task 12


def test_component_add_configuration_delegates_and_wraps() -> None:
    fake = make_fake_element("Component")
    config = make_fake_element("Configuration", getName="Config1")
    fake.addConfiguration.return_value = config
    comp = RPComponent(fake)

    result = comp.add_configuration("Config1")

    fake.addConfiguration.assert_called_once_with("Config1")
    assert result.get_name() == "Config1"


def test_component_add_file_delegates_and_wraps() -> None:
    fake = make_fake_element("Component")
    file_elem = make_fake_element("File", getName="File1")
    fake.addFile.return_value = file_elem
    comp = RPComponent(fake)

    result = comp.add_file("File1")

    fake.addFile.assert_called_once_with("File1")
    assert result.get_name() == "File1"


def test_component_get_configurations_returns_collection() -> None:
    fake = make_fake_element("Component")
    config = make_fake_element("Configuration", getName="Config1")
    fake.getConfigurations.return_value = make_fake_collection([config])
    comp = RPComponent(fake)

    result = comp.get_configurations()

    fake.getConfigurations.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_component_find_configuration_wraps_result() -> None:
    fake = make_fake_element("Component")
    config = make_fake_element("Configuration", getName="Config1")
    fake.findConfiguration.return_value = config
    comp = RPComponent(fake)

    result = comp.find_configuration("Config1")

    fake.findConfiguration.assert_called_once_with("Config1")
    assert result is not None
    assert result.get_name() == "Config1"


def test_component_find_configuration_returns_none_when_not_found() -> None:
    fake = make_fake_element("Component")
    fake.findConfiguration.return_value = None
    comp = RPComponent(fake)

    result = comp.find_configuration("NonExistent")

    fake.findConfiguration.assert_called_once_with("NonExistent")
    assert result is None


def test_component_delete_configuration_delegates() -> None:
    fake = make_fake_element("Component")
    comp = RPComponent(fake)
    config_fake = make_fake_element("Configuration", getName="ToDelete")
    config = RPConfiguration(config_fake)

    comp.delete_configuration(config)

    fake.deleteConfiguration.assert_called_once_with(config_fake)


def test_component_get_path_returns_str() -> None:
    fake = make_fake_element("Component")
    fake.getPath.return_value = "/some/path"
    comp = RPComponent(fake)

    result = comp.get_path()

    fake.getPath.assert_called_once_with()
    assert result == "/some/path"


def test_component_set_path_delegates() -> None:
    fake = make_fake_element("Component")
    comp = RPComponent(fake)

    comp.set_path("/new/path")

    fake.setPath.assert_called_once_with("/new/path")
