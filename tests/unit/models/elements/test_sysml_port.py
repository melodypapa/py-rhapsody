"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPSysMLPort."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.common import RPSysMLPort
from tests.unit.models.fakes import make_fake_element


class TestRPSysMLPort:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("SysMLPort", getName="P1")
        port = RPSysMLPort(fake)
        assert isinstance(port, RPModelElement)
        assert port.get_name() == "P1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("SysMLPort", getName="P1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSysMLPort)

    def test_get_is_reversed_returns_int(self) -> None:
        # Pattern G — boolean check returning int
        fake = make_fake_element("SysMLPort", getIsReversed=True)
        port = RPSysMLPort(fake)
        assert port.get_is_reversed() == 1
        fake.getIsReversed.assert_called_once_with()

    def test_get_port_direction_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("SysMLPort", getPortDirection="InOut")
        port = RPSysMLPort(fake)
        assert port.get_port_direction() == "InOut"
        fake.getPortDirection.assert_called_once_with()

    def test_get_type_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("SysMLPort")
        t = make_fake_element("Class", getName="T1")
        fake.getType.return_value = t
        port = RPSysMLPort(fake)
        wrapped = port.get_type()
        assert wrapped.get_name() == "T1"
        fake.getType.assert_called_once_with()

    def test_set_is_reversed_delegates(self) -> None:
        # Pattern D — single-arg setter (int arg)
        fake = make_fake_element("SysMLPort")
        port = RPSysMLPort(fake)
        port.set_is_reversed(1)
        fake.setIsReversed.assert_called_once_with(1)

    def test_set_port_direction_delegates(self) -> None:
        # Pattern D — single-arg setter (str arg)
        fake = make_fake_element("SysMLPort")
        port = RPSysMLPort(fake)
        port.set_port_direction("Out")
        fake.setPortDirection.assert_called_once_with("Out")

    def test_set_type_delegates(self) -> None:
        # Pattern F — multi-arg void method (single RPClassifier arg)
        fake = make_fake_element("SysMLPort")
        t = make_fake_element("Class", getName="T1")
        fake.setType.return_value = None
        port = RPSysMLPort(fake)
        port.set_type(RPClassifier(t))
        fake.setType.assert_called_once_with(t)

    def test_add_link_delegates_and_wraps(self) -> None:
        # Pattern E — multi-arg method returning wrapped element
        from rhapsody_cli.models.elements.containment import RPPackage
        from rhapsody_cli.models.elements.relations import RPInstance, RPRelation

        fake = make_fake_element("SysMLPort")
        from_part = make_fake_element("Instance", getName="From")
        to_part = make_fake_element("Instance", getName="To")
        assoc = make_fake_element("Relation", getName="R")
        to_port = make_fake_element("SysMLPort", getName="ToPort")
        new_owner = make_fake_element("Package", getName="Pkg")
        link = make_fake_element("Link", getName="L1")
        fake.addLink.return_value = link
        port = RPSysMLPort(fake)
        wrapped = port.add_link(
            RPInstance(from_part),
            RPInstance(to_part),
            RPRelation(assoc),
            RPSysMLPort(to_port),
            RPPackage(new_owner),
        )
        assert wrapped.get_name() == "L1"
        fake.addLink.assert_called_once_with(from_part, to_part, assoc, to_port, new_owner)
