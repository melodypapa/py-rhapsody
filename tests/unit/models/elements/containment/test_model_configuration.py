"""Tests for rhapsody_cli.models.elements.containment.RPConfiguration."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPUnit
from rhapsody_cli.models.elements.containment import RPComponent, RPConfiguration
from rhapsody_cli.models.elements.relations import RPInstance
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_configuration_is_a_unit() -> None:
    fake = make_fake_element("Configuration", getName="Config1")
    config = RPConfiguration(fake)

    assert isinstance(config, RPUnit)
    assert config.get_name() == "Config1"


def test_configuration_is_registered_for_meta_class_configuration() -> None:
    fake = make_fake_element("Configuration", getName="Config1")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPConfiguration)


# Tests for methods from Task 12


def test_configuration_add_initial_instance_delegates() -> None:
    fake = make_fake_element("Configuration")
    config = RPConfiguration(fake)
    instance_fake = make_fake_element("Instance", getName="Inst1")
    instance = RPInstance(instance_fake)

    config.add_initial_instance(instance)

    fake.addInitialInstance.assert_called_once_with(instance_fake)


def test_configuration_get_initial_instances_returns_collection() -> None:
    fake = make_fake_element("Configuration")
    instance = make_fake_element("Instance", getName="Inst1")
    fake.getInitialInstances.return_value = make_fake_collection([instance])
    config = RPConfiguration(fake)

    result = config.get_initial_instances()

    fake.getInitialInstances.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_configuration_delete_initial_instance_delegates() -> None:
    fake = make_fake_element("Configuration")
    config = RPConfiguration(fake)
    instance_fake = make_fake_element("Instance", getName="Inst1")
    instance = RPInstance(instance_fake)

    config.delete_initial_instance(instance)

    fake.deleteInitialInstance.assert_called_once_with(instance_fake)


def test_configuration_get_directory_returns_str() -> None:
    fake = make_fake_element("Configuration")
    fake.getDirectory.return_value = "/some/dir"
    config = RPConfiguration(fake)

    result = config.get_directory()

    fake.getDirectory.assert_called_once_with()
    assert result == "/some/dir"


def test_configuration_set_directory_delegates() -> None:
    fake = make_fake_element("Configuration")
    config = RPConfiguration(fake)

    config.set_directory("/new/dir")

    fake.setDirectory.assert_called_once_with("/new/dir")


def test_configuration_get_its_component_wraps_result() -> None:
    fake = make_fake_element("Configuration")
    comp = make_fake_element("Component", getName="Comp1")
    fake.getItsComponent.return_value = comp
    config = RPConfiguration(fake)

    result = config.get_its_component()

    fake.getItsComponent.assert_called_once_with()
    assert result.get_name() == "Comp1"


def test_configuration_set_its_component_delegates() -> None:
    fake = make_fake_element("Configuration")
    config = RPConfiguration(fake)
    comp_fake = make_fake_element("Component", getName="Comp1")
    comp = RPComponent(comp_fake)

    config.set_its_component(comp)

    fake.setItsComponent.assert_called_once_with(comp_fake)


def test_configuration_needs_code_generation_returns_int() -> None:
    fake = make_fake_element("Configuration")
    fake.needsCodeGeneration.return_value = 1
    config = RPConfiguration(fake)

    result = config.needs_code_generation()

    fake.needsCodeGeneration.assert_called_once_with()
    assert result == 1
