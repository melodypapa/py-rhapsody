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

    def test_attribute_type_roundtrip(self, test_project: RPProject) -> None:
        """IRPVariable::setTypeDeclaration's Java doc states it searches for a matching
        existing type first and, if found, uses that real type instead of creating an
        on-the-fly declaration. Since 'int' matches Rhapsody's built-in int type, the
        attribute's type resolves to that real IRPClassifier -- get_declaration()
        legitimately stays empty in that case, so assert against get_type() instead."""
        pkg_name = self._unique("TypePkg")
        class_name = self._unique("TypeCls")
        attr_name = self._unique("typedAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_type_declaration("int")
            assert attr.get_type().get_name() == "int"
        finally:
            test_class.delete_from_project()

    def test_attribute_declaration_direct_set(self, test_project: RPProject) -> None:
        """Unlike set_type_declaration, IRPVariable::setDeclaration's Java doc guarantees
        the given string is always used as an on-the-fly declaration, even if it matches
        an existing type -- so get_declaration() should directly reflect it."""
        pkg_name = self._unique("DeclPkg")
        class_name = self._unique("DeclCls")
        attr_name = self._unique("declAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_declaration("int")
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
