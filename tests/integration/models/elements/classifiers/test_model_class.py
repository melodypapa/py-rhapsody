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
