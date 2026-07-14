import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.diagrams import RPDiagram


@pytest.mark.integration
class TestRPDiagramIntegration:
    """Integration tests for RPDiagram with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_object_model_diagram(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DiagPkg")
        diag_name = self._unique("MyDiagram")
        pkg = self._create_package(test_project, pkg_name)
        try:
            diagram = pkg.add_object_model_diagram(diag_name)
            assert diagram is not None
            assert isinstance(diagram, RPDiagram)
            assert diagram.get_name() == diag_name
        finally:
            diagram.delete_from_project()
