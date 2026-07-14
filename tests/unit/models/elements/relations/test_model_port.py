"""Tests for rhapsody_cli.models.elements.relations.RPPort."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier
from rhapsody_cli.models.elements.relations import RPInstance, RPPort
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_port_is_an_instance() -> None:
    fake = make_fake_element("Port", getName="clientPort")
    port = RPPort(fake)

    assert isinstance(port, RPInstance)
    assert port.get_name() == "clientPort"


def test_port_is_registered_for_meta_class_port() -> None:
    fake = make_fake_element("Port")

    wrapped = AbstractRPModelElement.wrap(fake)

    assert isinstance(wrapped, RPPort)


def test_port_get_is_behavioral_delegates_to_com() -> None:
    fake = make_fake_element("Port", getIsBehavioral=1)
    port = RPPort(fake)

    assert port.get_is_behavioral() == 1

    fake.getIsBehavioral.assert_called_once_with()


def test_port_set_is_behavioral_delegates_to_com() -> None:
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.set_is_behavioral(1)

    fake.setIsBehavioral.assert_called_once_with(1)


def test_port_get_is_reversed_delegates_to_com() -> None:
    fake = make_fake_element("Port", getIsReversed=0)
    port = RPPort(fake)

    assert port.get_is_reversed() == 0

    fake.getIsReversed.assert_called_once_with()


def test_port_set_is_reversed_delegates_to_com() -> None:
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.set_is_reversed(1)

    fake.setIsReversed.assert_called_once_with(1)


def test_port_get_port_contract_wraps_result() -> None:
    contract_fake = make_fake_element("Class", getName="IEngine")
    fake = make_fake_element("Port")
    fake.getPortContract.return_value = contract_fake
    port = RPPort(fake)

    result = port.get_port_contract()

    assert isinstance(result, RPClass)
    assert result.get_name() == "IEngine"


def test_port_set_port_contract_delegates_to_com() -> None:
    contract_fake = make_fake_element("Class", getName="IEngine")
    contract = RPClass(contract_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.set_port_contract(contract)

    fake.setPortContract.assert_called_once_with(contract_fake)


def test_port_get_provided_interfaces_returns_collection() -> None:
    fake = make_fake_element("Port")
    interface = make_fake_element("Class", getName="IProvided")
    fake.getProvidedInterfaces.return_value = make_fake_collection([interface])
    port = RPPort(fake)

    result = port.get_provided_interfaces()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "IProvided"


def test_port_add_provided_interface_delegates_to_com() -> None:
    interface_fake = make_fake_element("Class", getName="IProvided")
    interface = RPClass(interface_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.add_provided_interface(interface)

    fake.addProvidedInterface.assert_called_once_with(interface_fake)


def test_port_remove_provided_interface_delegates_to_com() -> None:
    interface_fake = make_fake_element("Class", getName="IProvided")
    interface = RPClass(interface_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.remove_provided_interface(interface)

    fake.removeProvidedInterface.assert_called_once_with(interface_fake)


def test_port_get_required_interfaces_returns_collection() -> None:
    fake = make_fake_element("Port")
    interface = make_fake_element("Class", getName="IRequired")
    fake.getRequiredInterfaces.return_value = make_fake_collection([interface])
    port = RPPort(fake)

    result = port.get_required_interfaces()

    assert isinstance(result, RPCollection)
    assert len(result) == 1
    assert result[0].get_name() == "IRequired"


def test_port_add_required_interface_delegates_to_com() -> None:
    interface_fake = make_fake_element("Class", getName="IRequired")
    interface = RPClass(interface_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.add_required_interface(interface)

    fake.addRequiredInterface.assert_called_once_with(interface_fake)


def test_port_remove_required_interface_delegates_to_com() -> None:
    interface_fake = make_fake_element("Class", getName="IRequired")
    interface = RPClass(interface_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.remove_required_interface(interface)

    fake.removeRequiredInterface.assert_called_once_with(interface_fake)


def test_port_get_contract_wraps_result() -> None:
    contract_fake = make_fake_element("Class", getName="IEngine")
    fake = make_fake_element("Port")
    fake.getContract.return_value = contract_fake
    port = RPPort(fake)

    result = port.get_contract()

    assert isinstance(result, RPClass)
    assert result.get_name() == "IEngine"


def test_port_set_contract_delegates_to_com() -> None:
    contract_fake = make_fake_element("Class", getName="IEngine")
    contract = RPClass(contract_fake)
    fake = make_fake_element("Port")
    port = RPPort(fake)

    port.set_contract(contract)

    fake.setContract.assert_called_once_with(contract_fake)


def test_classifier_get_ports_returns_actual_rpport_instances() -> None:
    fake = make_fake_element("Class")
    fake.getPorts.return_value = make_fake_collection([make_fake_element("Port", getName="clientPort")])
    classifier = RPClassifier(fake)

    result = classifier.get_ports()

    assert len(result) == 1
    assert isinstance(result[0], RPPort)
    assert result[0].get_name() == "clientPort"
