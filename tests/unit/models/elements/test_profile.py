"""Tests for rhapsody_cli.models.elements.containment.RPProfile."""

from rhapsody_cli.models.core import wrap
from rhapsody_cli.models.elements.containment import RPPackage, RPProfile
from tests.unit.models.fakes import make_fake_element


def test_profile_is_a_package() -> None:
    fake = make_fake_element("Profile", getName="SysML")
    profile = RPProfile(fake)

    assert isinstance(profile, RPPackage)
    assert profile.getName() == "SysML"


def test_profile_is_registered_for_meta_class_profile() -> None:
    fake = make_fake_element("Profile", getName="SysML")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPProfile)
