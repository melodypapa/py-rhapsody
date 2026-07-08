"""Tests for rhapsody_cli.elements.package.RPPackage."""

from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPPackage
from tests.unit.models.fakes import make_fake_element


def test_package_is_a_unit() -> None:
    fake = make_fake_element("Package", getName="MyPkg")
    package = RPPackage(fake)

    assert isinstance(package, RPUnit)
    assert package.getName() == "MyPkg"


def test_package_add_class_delegates_to_com_and_wraps_result() -> None:
    fake = make_fake_element("Package")
    new_class = make_fake_element("Class", getName="Widget")
    fake.addClass.return_value = new_class
    package = RPPackage(fake)

    result = package.addClass("Widget")

    fake.addClass.assert_called_once_with("Widget")
    assert result.getName() == "Widget"


def test_package_add_nested_package_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    nested = make_fake_element("Package", getName="Nested")
    fake.addNestedPackage.return_value = nested
    package = RPPackage(fake)

    result = package.addNestedPackage("Nested")

    fake.addNestedPackage.assert_called_once_with("Nested")
    assert result.getName() == "Nested"


def test_package_add_actor_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    actor = make_fake_element("Actor", getName="Driver")
    fake.addActor.return_value = actor
    package = RPPackage(fake)

    result = package.addActor("Driver")

    fake.addActor.assert_called_once_with("Driver")
    assert result.getName() == "Driver"


def test_package_add_global_function_delegates_to_com() -> None:
    fake = make_fake_element("Package")
    func = make_fake_element("Operation", getName="doThing")
    fake.addGlobalFunction.return_value = func
    package = RPPackage(fake)

    result = package.addGlobalFunction("doThing")

    fake.addGlobalFunction.assert_called_once_with("doThing")
    assert result.getName() == "doThing"


def test_package_is_registered_for_meta_class_package() -> None:
    fake = make_fake_element("Package", getName="MyPkg")

    wrapped = wrap(fake)

    assert isinstance(wrapped, RPPackage)
