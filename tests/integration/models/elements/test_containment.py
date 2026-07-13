"""Integration tests for RPProject and RPPackage with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import time

import pytest

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPProjectIntegration:
    """Integration tests for RPProject with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    def test_project_properties(self, test_project: RPProject) -> None:
        assert test_project.get_name()
        assert isinstance(test_project.get_name(), str)
        assert test_project.get_meta_class() == "Project"
        guid = test_project.get_guid()
        assert isinstance(guid, str)
        assert len(guid) > 0

    def test_project_is_rp_project(self, test_project: RPProject) -> None:
        assert isinstance(test_project, RPProject)
        assert isinstance(test_project, RPPackage)
        assert isinstance(test_project, RPModelElement)

    def test_add_package_to_project(self, test_project: RPProject) -> None:
        name = self._unique("TopLevelPkg")
        new_pkg = test_project.add_package(name)
        assert new_pkg is not None
        assert isinstance(new_pkg, RPPackage)
        assert new_pkg.get_name() == name
        assert new_pkg.get_meta_class() == "Package"
        pkgs = test_project.get_packages()
        names = [p.get_name() for p in pkgs]
        assert name in names

    def test_project_get_packages_returns_collection(self, test_project: RPProject) -> None:
        pkgs = test_project.get_packages()
        assert pkgs is not None


@pytest.mark.integration
class TestRPPackageIntegration:
    """Integration tests for RPPackage with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_create_nested_packages(self, test_project: RPProject) -> None:
        parent_name = self._unique("ParentPkg")
        child_name = self._unique("ChildPkg")
        parent_pkg = self._create_package(test_project, parent_name)
        child_pkg = parent_pkg.add_nested_package(child_name)
        assert child_pkg is not None
        assert isinstance(child_pkg, RPPackage)
        assert child_pkg.get_name() == child_name
        children = parent_pkg.get_nested_packages()
        child_names = [c.get_name() for c in children]
        assert child_name in child_names

    def test_package_navigation(self, test_project: RPProject) -> None:
        parent_name = self._unique("NavParent")
        child_name = self._unique("NavChild")
        parent_pkg = self._create_package(test_project, parent_name)
        child_pkg = parent_pkg.add_nested_package(child_name)
        owner = child_pkg.get_owner()
        assert owner is not None
        assert owner.get_name() == parent_name
        assert isinstance(owner, RPPackage)

    def test_add_class_to_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ClassPkg")
        class_name = self._unique("TestClass")
        pkg = self._create_package(test_project, pkg_name)
        new_class = pkg.add_class(class_name)
        assert new_class is not None
        assert new_class.get_name() == class_name
        assert new_class.get_meta_class() == "Class"
        classes = pkg.get_classes()
        class_names = [c.get_name() for c in classes]
        assert class_name in class_names
