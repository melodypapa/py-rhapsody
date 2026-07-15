"""Integration tests for RPModelElement and RPCollection with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid

import pytest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.models.core import RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


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


@pytest.mark.integration
class TestRPModelElementDependenciesIntegration:
    """Integration tests for RPModelElement dependency/association methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_add_dependency_to_and_get_dependencies(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DepPkg"))
        try:
            source = pkg.add_class(self._unique("Source"))
            target = pkg.add_class(self._unique("Target"))
            dependency = source.add_dependency_to(target)
            assert dependency is not None
            assert isinstance(dependency, RPModelElement)
            assert dependency.get_meta_class() == "Dependency"

            deps = source.get_dependencies()
            assert isinstance(deps, RPCollection)
            assert isinstance(deps.get_count(), int)
            assert deps.get_count() >= 0
            assert len(list(deps)) >= 1

            source.delete_dependency(dependency)
            deps_after = source.get_dependencies()
            assert len(list(deps_after)) == 0
        finally:
            pkg.delete_from_project()

    def test_add_dependency(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AddDepPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            target = pkg.add_class(self._unique("Target"))
            target_name = target.get_name()
            source = pkg.add_class(self._unique("Source"))
            dependency = source.add_dependency(target_name, "Class")
            assert dependency is not None
            assert isinstance(dependency, RPModelElement)
            assert dependency.get_meta_class() == "Dependency"
            deps = source.get_dependencies()
            assert len(list(deps)) >= 1
            source.delete_dependency(dependency)
        finally:
            pkg.delete_from_project()

    def test_add_dependency_between(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DepBetPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            source = pkg.add_class(self._unique("Source"))
            target = pkg.add_class(self._unique("Target"))
            dependency = pkg.add_dependency_between(source, target)
            assert dependency is not None
            assert isinstance(dependency, RPModelElement)
            assert dependency.get_meta_class() == "Dependency"
            deps = pkg.get_dependencies()
            assert isinstance(deps, RPCollection)
            assert isinstance(deps.get_count(), int)
            assert deps.get_count() >= 0
            assert len(list(deps)) >= 1
            pkg.delete_dependency(dependency)
        finally:
            pkg.delete_from_project()

    def test_get_owned_dependencies(self, test_project: RPProject) -> None:
        pkg_name = self._unique("OwnedDepPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            source = pkg.add_class(self._unique("Source"))
            target = pkg.add_class(self._unique("Target"))
            dependency = source.add_dependency_to(target)
            owned = source.get_owned_dependencies()
            assert isinstance(owned, RPCollection)
            assert isinstance(owned.get_count(), int)
            assert owned.get_count() >= 0
            assert len(list(owned)) >= 1
            source.delete_dependency(dependency)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires RMM-enabled project", strict=False)
    def test_add_remote_dependency_to_and_get_remote_dependencies(self, test_project: RPProject) -> None:
        pkg_name = self._unique("RemoteDepPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            source = pkg.add_class(self._unique("Source"))
            target = pkg.add_class(self._unique("Target"))
            dependency = source.add_remote_dependency_to(target, "dependency")
            assert dependency is not None
            assert isinstance(dependency, RPModelElement)
            assert dependency.get_meta_class() == "Dependency"
            remote_deps = source.get_remote_dependencies()
            assert isinstance(remote_deps, RPCollection)
            assert isinstance(remote_deps.get_count(), int)
            assert remote_deps.get_count() >= 0
            source.delete_dependency(dependency)
        finally:
            pkg.delete_from_project()

    def test_get_association_classes(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AssocClsPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            assoc_classes = pkg.get_association_classes()
            assert isinstance(assoc_classes, RPCollection)
            # smoke test: no associations created, but confirm the COM call returns a valid RPCollection
            assert isinstance(assoc_classes.get_count(), int)
        finally:
            pkg.delete_from_project()

    def test_get_references(self, test_project: RPProject) -> None:
        pkg_name = self._unique("RefPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            source = pkg.add_class(self._unique("Source"))
            target = pkg.add_class(self._unique("Target"))
            dependency = source.add_dependency_to(target)
            references = target.get_references()
            assert isinstance(references, RPCollection)
            assert isinstance(references.get_count(), int)
            assert references.get_count() >= 0
            source.delete_dependency(dependency)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires RPRelation helper from relations subpackage", strict=False)
    def test_add_association(self, test_project: RPProject) -> None:
        # RPPackage.add_association has a different signature (name: str), so call RPModelElement's version directly
        pkg_name = self._unique("AssocPkg")
        pkg = self._create_package(test_project, pkg_name)
        try:
            cls1 = pkg.add_class(self._unique("Class1"))
            cls2 = pkg.add_class(self._unique("Class2"))
            assoc = RPModelElement.add_association(pkg, cls1, cls2, self._unique("AssocName"))
            assert assoc is not None
            assert isinstance(assoc, RPModelElement)
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementStereotypesTagsIntegration:
    """Integration tests for RPModelElement stereotype and tag methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_get_stereotypes_initially_empty(self, test_project: RPProject) -> None:
        stereotypes = test_project.get_stereotypes()
        assert stereotypes is not None
        assert isinstance(stereotypes, RPCollection)
        assert len(list(stereotypes)) == 0

    def test_add_stereotype_and_get_stereotypes(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("StereoPkg"))
        try:
            stereo = pkg.add_stereotype(self._unique("TestStereo"), "Package")
            assert stereo is not None
            assert isinstance(stereo, RPModelElement)
            stereotypes = pkg.get_stereotypes()
            assert isinstance(stereotypes, RPCollection)
            names = [s.get_name() for s in stereotypes]
            assert stereo.get_name() in names
        finally:
            pkg.delete_from_project()

    def test_remove_stereotype(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RemoveStereoPkg"))
        try:
            stereo = pkg.add_stereotype(self._unique("RemoveMe"), "Package")
            assert stereo is not None
            assert isinstance(stereo, RPModelElement)
            pkg.remove_stereotype(stereo)
            stereotypes = pkg.get_stereotypes()
            assert isinstance(stereotypes, RPCollection)
            names = [s.get_name() for s in stereotypes]
            assert stereo.get_name() not in names
        finally:
            pkg.delete_from_project()

    def test_add_specific_stereotype(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SpecificStereoPkg"))
        try:
            stereo = pkg.add_stereotype(self._unique("SpecificStereo"), "Package")
            assert stereo is not None
            assert isinstance(stereo, RPModelElement)
            pkg.remove_stereotype(stereo)
            result = pkg.add_specific_stereotype(stereo)
            assert result is not None
            assert isinstance(result, RPModelElement)
            stereotypes = pkg.get_stereotypes()
            assert isinstance(stereotypes, RPCollection)
            names = [s.get_name() for s in stereotypes]
            assert stereo.get_name() in names
        finally:
            pkg.delete_from_project()

    def test_get_all_tags(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("AllTagsTestPkg"))
        try:
            stereo = pkg.add_stereotype(self._unique("TagTestStereo"), "Package")
            assert stereo is not None
            assert isinstance(stereo, RPModelElement)
            tags = pkg.get_all_tags()
            assert tags is not None
            assert isinstance(tags, RPCollection)
        finally:
            pkg.delete_from_project()

    def test_get_local_tags(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("LocalTagsTestPkg"))
        try:
            stereo = pkg.add_stereotype(self._unique("LocalTagTestStereo"), "Package")
            assert stereo is not None
            assert isinstance(stereo, RPModelElement)
            tags = pkg.get_local_tags()
            assert tags is not None
            assert isinstance(tags, RPCollection)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Requires stereotype with tag definition")
    def test_get_tag(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("GetTagTestPkg"))
        try:
            cls = pkg.add_class(self._unique("GetTagTestClass"))
            assert cls is not None
            assert isinstance(cls, RPModelElement)
            cls.add_stereotype(self._unique("TaggedStereo"), "Class")
            tag = cls.get_tag("SomeTag")
            assert tag is not None
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="New term stereotype not available on base project")
    def test_get_new_term_stereotype(self, test_project: RPProject) -> None:
        stereotypes = test_project.get_new_term_stereotype()
        assert stereotypes is not None

    @pytest.mark.xfail(strict=False, reason="Requires stereotype with tag definition")
    def test_set_tag_value(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetTagValTestPkg"))
        try:
            cls = pkg.add_class(self._unique("SetTagValTestClass"))
            assert cls is not None
            assert isinstance(cls, RPModelElement)
            cls.add_stereotype(self._unique("TaggedStereo"), "Class")
            tag = cls.get_tag("SomeTag")
            assert tag is not None
            result = cls.set_tag_value(tag, "test_value")
            assert result is not None
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Requires stereotype with tag definition")
    def test_set_tag_element_value(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetTagElemTestPkg"))
        try:
            cls = pkg.add_class(self._unique("SetTagElemTestClass"))
            assert cls is not None
            assert isinstance(cls, RPModelElement)
            cls.add_stereotype(self._unique("TaggedStereo"), "Class")
            tag = cls.get_tag("SomeTag")
            assert tag is not None
            result = cls.set_tag_element_value(tag, cls)
            assert result is not None
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Requires stereotype with tag definition")
    def test_set_tag_context_value(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetTagCtxTestPkg"))
        try:
            cls = pkg.add_class(self._unique("SetTagCtxTestClass"))
            assert cls is not None
            assert isinstance(cls, RPModelElement)
            cls.add_stereotype(self._unique("TaggedStereo"), "Class")
            tag = cls.get_tag("SomeTag")
            assert tag is not None
            elements = cls.get_all_tags()
            multiplicities = cls.get_local_tags()
            assert isinstance(elements, RPCollection)
            assert isinstance(multiplicities, RPCollection)
            result = cls.set_tag_context_value(tag, elements, multiplicities)
            assert result is not None
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementDescriptionDisplayNameIntegration:
    """Integration tests for RPModelElement description and display-name methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_set_and_get_description_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DescPkg"))
        try:
            cls = pkg.add_class(self._unique("DescCls"))
            cls.set_description("A test description")
            description = cls.get_description()
            assert description == "A test description"
            assert isinstance(description, str)

            plain_text = cls.get_description_plain_text()
            assert isinstance(plain_text, str)
            assert "A test description" in plain_text
        finally:
            pkg.delete_from_project()

    def test_set_and_get_description_rtf_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RtfDescPkg"))
        try:
            cls = pkg.add_class(self._unique("RtfDescCls"))
            rtf_string = r"{\rtf1 Hello}"
            cls.set_description_rtf(rtf_string)

            is_rtf = cls.is_description_rtf()
            assert is_rtf
            assert isinstance(is_rtf, (bool, int))

            retrieved_rtf = cls.get_description_rtf()
            assert isinstance(retrieved_rtf, str)
            assert retrieved_rtf == rtf_string

            description = cls.get_description()
            assert isinstance(description, str)
            assert "Hello" in description
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Rhapsody documents setDescriptionHTML as unimplemented")
    def test_set_and_get_description_html(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("HtmlDescPkg"))
        try:
            cls = pkg.add_class(self._unique("HtmlDescCls"))
            html = "<html><body>Hello</body></html>"
            cls.set_description_html(html)

            retrieved_html = cls.get_description_html()
            assert isinstance(retrieved_html, str)
        finally:
            pkg.delete_from_project()

    def test_get_description_html_on_empty(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("HtmlEmptyPkg"))
        try:
            result = pkg.get_description_html()
            assert isinstance(result, str)
        finally:
            pkg.delete_from_project()

    def test_set_description_and_hyperlinks(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        pkg = self._create_package(test_project, self._unique("HyperlinkPkg"))
        try:
            cls1 = pkg.add_class(self._unique("Target1"))
            cls2 = pkg.add_class(self._unique("Target2"))

            new_collection = rhapsody_app.create_new_collection()
            assert isinstance(new_collection, RPCollection)
            new_collection.add_item(cls1)
            new_collection.add_item(cls2)

            rtf_text = r"{\rtf1 Description with hyperlinks}"
            cls1.set_description_and_hyperlinks(rtf_text, new_collection)

            description = cls1.get_description()
            assert isinstance(description, str)
            assert "Description with hyperlinks" in description
        finally:
            pkg.delete_from_project()

    def test_set_and_get_display_name_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DispNamePkg"))
        try:
            cls = pkg.add_class(self._unique("DispNameCls"))
            display_name = "My Custom Label"
            cls.set_display_name(display_name)

            retrieved = cls.get_display_name()
            assert retrieved == display_name
            assert isinstance(retrieved, str)
        finally:
            pkg.delete_from_project()

    def test_set_and_get_display_name_rtf_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DispNameRtfPkg"))
        try:
            cls = pkg.add_class(self._unique("DispNameRtfCls"))
            rtf_string = r"{\rtf1 Bold Label}"
            cls.set_display_name_rtf(rtf_string)

            is_rtf = cls.is_display_name_rtf()
            assert is_rtf
            assert isinstance(is_rtf, (bool, int))

            retrieved_rtf = cls.get_display_name_rtf()
            assert isinstance(retrieved_rtf, str)
            assert retrieved_rtf == rtf_string

            display_name = cls.get_display_name()
            assert isinstance(display_name, str)
        finally:
            pkg.delete_from_project()
