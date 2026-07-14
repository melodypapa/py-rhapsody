import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.relations import RPGeneralization


@pytest.mark.integration
class TestRPGeneralizationIntegration:
    """Integration tests for RPGeneralization with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_generalization(self, test_project: RPProject) -> None:
        pkg_name = self._unique("GenPkg")
        parent_name = self._unique("Parent")
        child_name = self._unique("Child")
        pkg = self._create_package(test_project, pkg_name)
        parent = pkg.add_class(parent_name)
        child = pkg.add_class(child_name)
        try:
            child.add_generalization(parent)
            gen = child.find_generalization(parent_name)
            assert gen is not None
            assert isinstance(gen, RPGeneralization)
            assert gen.get_meta_class() == "Generalization"
            assert gen.get_base_class() == parent
        finally:
            child.delete_from_project()
            parent.delete_from_project()
