"""Integration tests for RPModelElement and RPCollection with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import pytest

from rhapsody_cli.models.core import RPModelElement
from rhapsody_cli.models.elements.containment import RPProject


@pytest.mark.integration
class TestRPModelElementIntegration:
    """Integration tests for RPModelElement with real Rhapsody COM API."""

    def test_get_name(self, test_project: RPProject) -> None:
        assert isinstance(test_project, RPModelElement)
        name = test_project.get_name()
        assert name == "TestProject"
        assert isinstance(name, str)

    def test_set_name(self, test_project: RPProject) -> None:
        original_name = test_project.get_name()
        test_project.set_name("RenamedProject")
        new_name = test_project.get_name()
        assert new_name == "RenamedProject"
        assert isinstance(new_name, str)
        test_project.set_name(original_name)

    def test_get_meta_class(self, test_project: RPProject) -> None:
        meta_class = test_project.get_meta_class()
        assert meta_class == "Project"
        assert isinstance(meta_class, str)

    def test_get_guid(self, test_project: RPProject) -> None:
        guid = test_project.get_guid()
        assert isinstance(guid, str)
        assert len(guid) > 0


@pytest.mark.integration
class TestRPCollectionIntegration:
    """Integration tests for RPCollection with real Rhapsody COM API."""

    def test_get_nested_elements_iteration(self, test_project: RPProject) -> None:
        elements = test_project.get_nested_elements()
        assert elements is not None
        assert len(list(elements)) >= 0

    def test_get_nested_elements_filtering(self, test_project: RPProject) -> None:
        all_elements = test_project.get_nested_elements()
        packages = test_project.get_nested_elements_by_meta_class("Package", 0)
        assert all_elements is not None
        assert packages is not None
        all_list = list(all_elements)
        package_list = list(packages)
        assert len(package_list) <= len(all_list)
