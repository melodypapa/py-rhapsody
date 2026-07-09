"""Tests for rhapsody_cli.elements.package.RPPackage."""

from rhapsody_cli.models.core import RPUnit, wrap
from rhapsody_cli.models.elements.containment import RPPackage
from tests.unit.models.fakes import make_fake_collection, make_fake_element


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


def test_package_get_nested_packages_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    nested1 = make_fake_element("Package", getName="Nested1")
    nested2 = make_fake_element("Package", getName="Nested2")
    fake.getNestedPackages.return_value = make_fake_collection([nested1, nested2])
    package = RPPackage(fake)

    result = package.getNestedPackages()

    fake.getNestedPackages.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 2
    assert result[0].getName() == "Nested1"
    assert result[1].getName() == "Nested2"


def test_package_get_classes_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    class1 = make_fake_element("Class", getName="Class1")
    class2 = make_fake_element("Class", getName="Class2")
    fake.getClasses.return_value = make_fake_collection([class1, class2])
    package = RPPackage(fake)

    result = package.getClasses()

    fake.getClasses.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 2


def test_package_get_actors_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    actor1 = make_fake_element("Actor", getName="Actor1")
    fake.getActors.return_value = make_fake_collection([actor1])
    package = RPPackage(fake)

    result = package.getActors()

    fake.getActors.assert_called_once_with()
    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_package_get_use_cases_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    uc1 = make_fake_element("UseCase", getName="UC1")
    fake.getUseCases.return_value = make_fake_collection([uc1])
    package = RPPackage(fake)

    result = package.getUseCases()

    fake.getUseCases.assert_called_once_with()
    assert isinstance(result, RPCollection)


def test_package_add_use_case_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    uc = make_fake_element("UseCase", getName="UC1")
    fake.addUseCase.return_value = uc
    package = RPPackage(fake)

    result = package.addUseCase("UC1")

    fake.addUseCase.assert_called_once_with("UC1")
    assert result.getName() == "UC1"


def test_package_add_interface_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    iface = make_fake_element("Classifier", getName="IFoo")
    fake.addInterface.return_value = iface
    package = RPPackage(fake)

    result = package.addInterface("IFoo")

    fake.addInterface.assert_called_once_with("IFoo")
    assert result.getName() == "IFoo"


def test_package_add_signal_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    sig = make_fake_element("Classifier", getName="Signal1")
    fake.addSignal.return_value = sig
    package = RPPackage(fake)

    package.addSignal("Signal1")

    fake.addSignal.assert_called_once_with("Signal1")


def test_package_add_exception_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    exc = make_fake_element("Classifier", getName="Exception1")
    fake.addException.return_value = exc
    package = RPPackage(fake)

    package.addException("Exception1")

    fake.addException.assert_called_once_with("Exception1")


def test_package_add_enumeration_returns_wrapped_element() -> None:
    fake = make_fake_element("Package")
    enum = make_fake_element("Classifier", getName="Enum1")
    fake.addEnumeration.return_value = enum
    package = RPPackage(fake)

    package.addEnumeration("Enum1")

    fake.addEnumeration.assert_called_once_with("Enum1")


def test_package_get_enumerations_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection

    fake = make_fake_element("Package")
    enum1 = make_fake_element("Classifier", getName="Enum1")
    fake.getEnumerations.return_value = make_fake_collection([enum1])
    package = RPPackage(fake)

    result = package.getEnumerations()

    assert isinstance(result, RPCollection)
