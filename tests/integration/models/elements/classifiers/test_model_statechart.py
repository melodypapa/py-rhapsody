import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPStatechart
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPStatechartIntegration:
    """Integration tests for RPStatechart with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_statechart_in_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("StPkg")
        class_name = self._unique("StCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            sc = test_class.add_statechart()
            assert sc is not None
            assert isinstance(sc, RPStatechart)
            assert sc.get_meta_class() == "Statechart"
        finally:
            test_class.delete_from_project()
