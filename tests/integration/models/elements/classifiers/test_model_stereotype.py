import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPStereotype
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPStereotypeIntegration:
    """Integration tests for RPStereotype with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_stereotype_on_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SterPkg")
        class_name = self._unique("SterCls")
        stereo_name = self._unique("MyStereotype")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            stereotype = test_class.add_stereotype(stereo_name, "Class")
            assert stereotype is not None
            assert isinstance(stereotype, RPStereotype)
            assert stereotype.get_name() == stereo_name
            assert stereotype.get_meta_class() == "Stereotype"
        finally:
            test_class.delete_from_project()
            stereotype.delete_from_project()

    def test_stereotype_owner(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SterOwnPkg")
        class_name = self._unique("SterOwnCls")
        stereo_name = self._unique("OwnedStereo")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            stereotype = test_class.add_stereotype(stereo_name, "Class")
            owner = stereotype.get_owner()
            assert owner is not None
            assert owner.get_name() == pkg_name
            assert isinstance(owner, RPPackage)
        finally:
            test_class.delete_from_project()
            stereotype.delete_from_project()
