"""Tests for rhapsody_cli.models.elements.containment.RPConfiguration."""

from rhapsody_cli.models.core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPConfiguration
from tests.unit.models.fakes import make_fake_element


def test_configuration_is_a_unit() -> None:
    fake = make_fake_element("Configuration", getName="Config1")
    config = RPConfiguration(fake)

    assert isinstance(config, RPUnit)
    assert config.getName() == "Config1"


def test_configuration_is_registered_for_meta_class_configuration() -> None:
    fake = make_fake_element("Configuration", getName="Config1")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPConfiguration)
