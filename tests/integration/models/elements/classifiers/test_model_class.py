"""Integration tests for RPClass with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import time

import pytest

from rhapsody_cli.models.elements.classifiers import RPClass, RPOperation
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPClassIntegration:
    """Integration tests for RPClass with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_create_class_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("Pkg")
        class_name = self._unique("TestClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        assert test_class is not None
        assert isinstance(test_class, RPClass)
        assert test_class.get_name() == class_name
        assert test_class.get_meta_class() == "Class"

    def test_class_hierarchy_navigation(self, test_project: RPProject) -> None:
        pkg_name = self._unique("NavPkg")
        class_name = self._unique("ChildClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        parent = test_class.get_owner()
        assert parent is not None
        assert parent.get_name() == pkg_name
        assert isinstance(parent, RPPackage)

    def test_create_operation_in_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("OpPkg")
        class_name = self._unique("OpClass")
        pkg_name_op = f"{class_name}_op"
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        operation = test_class.add_operation(pkg_name_op)
        assert operation is not None
        assert isinstance(operation, RPOperation)
        assert operation.get_name() == pkg_name_op
        operations = test_class.get_operations()
        assert operation in list(operations)

    def test_class_delete(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelPkg")
        class_name = self._unique("DelClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        test_class.delete_from_project()
        classes = pkg.get_classes()
        class_names = [c.get_name() for c in classes]
        assert class_name not in class_names

    def test_class_inheritance(self, test_project: RPProject) -> None:
        pkg_name = self._unique("InhPkg")
        parent_name = self._unique("ParentCls")
        child_name = self._unique("ChildCls")
        pkg = self._create_package(test_project, pkg_name)
        parent = pkg.add_class(parent_name)
        child = pkg.add_class(child_name)
        try:
            child.add_superclass(parent)
            generalizations = list(child.get_generalizations())
            assert any(gen.get_base_class() == parent for gen in generalizations)
            child.delete_superclass(parent)
            generalizations_after = list(child.get_generalizations())
            assert not any(gen.get_base_class() == parent for gen in generalizations_after)
        finally:
            child.delete_from_project()
            parent.delete_from_project()

    def test_constructor_destructor(self, test_project: RPProject) -> None:
        pkg_name = self._unique("CtorPkg")
        class_name = self._unique("CtorCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            ctor = test_class.add_constructor("void()")
            assert ctor is not None
            assert isinstance(ctor, RPOperation)
            dtor = test_class.add_destructor()
            assert dtor is not None
            assert isinstance(dtor, RPOperation)
            operations = list(test_class.get_operations())
            assert ctor in operations
            assert dtor in operations
        finally:
            test_class.delete_from_project()

    def test_set_is_abstract_raises_not_implemented(self, test_project: RPProject) -> None:
        """RPClass.set_is_abstract is marked unimplemented: Rhapsody2.Application.1's automation
        server accepts a write to the 'isAbstract' COM property without error (confirmed via
        typelib inspection that both PROPERTYGET and PROPERTYPUT are declared for isAbstract
        under the same DISPID -- it is not read-only at the interface level), but the write does
        not persist (confirmed via immediate read-back, post-saveAll(), and a fresh re-fetch of
        the element). This is a genuine limitation of this Rhapsody build's IRPClass::isAbstract
        implementation, so the wrapper raises rather than silently no-opping."""
        pkg_name = self._unique("AbsPkg")
        class_name = self._unique("AbsCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_abstract() is False
            with pytest.raises(NotImplementedError):
                test_class.set_is_abstract(1)
        finally:
            test_class.delete_from_project()

    def test_type_management(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TypePkg")
        class_name = self._unique("TypeCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            added_type = test_class.add_type(self._unique("MyType"))
            assert added_type is not None
            assert added_type.get_meta_class() == "Type"
            added_type.delete_from_project()
        finally:
            test_class.delete_from_project()
