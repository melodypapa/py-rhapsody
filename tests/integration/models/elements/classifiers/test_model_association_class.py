"""Integration tests for RPAssociationClass with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPAssociationClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.relations import RPRelation


@pytest.mark.integration
class TestRPAssociationClassIntegration:
    """Integration tests for RPAssociationClass with real Rhapsody COM API.

    Note: In this Rhapsody build, ``addRelationTo`` with a non-empty ``linkName``
    does not actually create an association class — it creates a regular
    association with metaclass ``AssociationEnd`` roles.  The four
    ``RPAssociationClass``-specific methods therefore cannot be exercised via
    live COM in this environment.  They **do** have unit-test coverage via
    fakes, and the integration test below is marked ``xfail`` with a clear
    description of the limitation.
    """

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    @pytest.mark.xfail(strict=False, reason="addRelationTo(linkName) does not create AssociationClass in this Rhapsody COM build")
    def test_association_class_found_via_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AssocPkg")
        class_a_name = self._unique("ClassA")
        class_b_name = self._unique("ClassB")
        link_name = self._unique("LinkCls")
        pkg = self._create_package(test_project, pkg_name)
        class_a = pkg.add_class(class_a_name)
        class_b = pkg.add_class(class_b_name)
        try:
            class_a.add_relation_to(class_b, "roleA", "Association", "1", "roleB", "Association", "1", link_name)
            assoc_classes = pkg.get_association_classes()
            found = None
            for ac in assoc_classes:
                if isinstance(ac, RPAssociationClass) and ac.get_name() == link_name:
                    found = ac
                    break
            assert found is not None, f"AssociationClass '{link_name}' not found via get_association_classes()"
            end1 = found.get_end1()
            end2 = found.get_end2()
            assert end1 is not None
            assert isinstance(end1, RPRelation)
            assert end2 is not None
            assert isinstance(end2, RPRelation)
            assert found.get_is_class() in (0, 1)
            found.set_is_class(1)
            assert found.get_is_class() == 1
        finally:
            class_a.delete_from_project()
            class_b.delete_from_project()
