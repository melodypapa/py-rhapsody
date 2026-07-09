"""Tests for rhapsody_cli.models.elements.classifiers.RPStereotype."""

from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier, RPStereotype
from tests.unit.models.fakes import make_fake_element


def test_stereotype_is_a_classifier() -> None:
    fake = make_fake_element("Stereotype", getName="MyStereo")
    stereo = RPStereotype(fake)

    assert isinstance(stereo, RPClassifier)
    assert stereo.getName() == "MyStereo"


def test_stereotype_is_registered_for_meta_class_stereotype() -> None:
    fake = make_fake_element("Stereotype", getName="MyStereo")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPStereotype)
