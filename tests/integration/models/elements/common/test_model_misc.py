import uuid

import pytest

from rhapsody_cli.models.elements.common import RPComment, RPConstraint
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPCommentIntegration:
    """Integration tests for RPComment with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_comment_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ComPkg")
        comment_name = self._unique("MyComment")
        pkg = self._create_package(test_project, pkg_name)
        try:
            comment = pkg.add_new_aggr("Comment", comment_name)
            assert comment is not None
            assert isinstance(comment, RPComment)
            assert comment.get_name() == comment_name
            assert comment.get_meta_class() == "Comment"
        finally:
            comment.delete_from_project()


@pytest.mark.integration
class TestRPConstraintIntegration:
    """Integration tests for RPConstraint with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_constraint_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ConPkg")
        con_name = self._unique("MyConstraint")
        pkg = self._create_package(test_project, pkg_name)
        try:
            constraint = pkg.add_new_aggr("Constraint", con_name)
            assert constraint is not None
            assert isinstance(constraint, RPConstraint)
            assert constraint.get_name() == con_name
            assert constraint.get_meta_class() == "Constraint"
        finally:
            constraint.delete_from_project()
