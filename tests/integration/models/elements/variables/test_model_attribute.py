import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.variables import RPAttribute


@pytest.mark.integration
class TestRPAttributeIntegration:
    """Integration tests for RPAttribute with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_add_attribute_to_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AttrPkg")
        class_name = self._unique("AttrCls")
        attr_name = self._unique("myAttribute")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            assert attr is not None
            assert isinstance(attr, RPAttribute)
            assert attr.get_name() == attr_name
            attrs = list(test_class.get_attributes())
            assert attr in attrs
        finally:
            test_class.delete_from_project()

    @pytest.mark.xfail(
        reason="Rhapsody2.Application.1 does not persist 'typeDeclaration' on an attribute (no-op); "
        "RPAttribute.set_type_declaration silently fails to update get_declaration(). "
        "TODO: persist type declaration via the metatype property system in a future Rhapsody build.",
        strict=False,
    )
    def test_attribute_type_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TypePkg")
        class_name = self._unique("TypeCls")
        attr_name = self._unique("typedAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_type_declaration("int")
            assert attr.get_declaration() == "int"
        finally:
            test_class.delete_from_project()

    def test_attribute_default_value(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DefPkg")
        class_name = self._unique("DefCls")
        attr_name = self._unique("defaultAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_default_value("42")
            assert attr.get_default_value() == "42"
        finally:
            test_class.delete_from_project()
