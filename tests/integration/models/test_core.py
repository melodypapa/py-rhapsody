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


@pytest.mark.integration
class TestRPModelElementPropertiesIntegration:
    """Integration tests for RPModelElement property methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_add_property_and_get_property_value(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("AddPropPkg"))
        try:
            prop_key = "Custom::" + self._unique("MyProp")
            prop_value = self._unique("propVal")
            pkg.add_property(prop_key, "String", prop_value)
            retrieved = pkg.get_property_value(prop_key)
            assert retrieved == prop_value
            assert isinstance(retrieved, str)
        finally:
            pkg.delete_from_project()

    def test_set_property_value_and_read_back(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetPropPkg"))
        try:
            pkg.set_property_value("General::Graphics::ShowLabels", "False")
            value = pkg.get_property_value("General::Graphics::ShowLabels")
            assert isinstance(value, str)
            assert value == "False"
        finally:
            pkg.delete_from_project()

    def test_add_then_remove_property(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RemPropPkg"))
        try:
            prop_key = "Custom::" + self._unique("RemoveMe")
            pkg.add_property(prop_key, "String", "to_be_removed")
            before = pkg.get_property_value(prop_key)
            assert before == "to_be_removed"

            pkg.remove_property(prop_key)
            after = pkg.get_property_value(prop_key)
            assert isinstance(after, str)
            assert after == ""
        finally:
            pkg.delete_from_project()

    def test_get_property_value_explicit(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("PropExpPkg"))
        try:
            pkg.set_property_value("General::Graphics::ShowLabels", "False")
            explicit = pkg.get_property_value_explicit("General::Graphics::ShowLabels")
            assert isinstance(explicit, str)
            assert explicit == "False"
        finally:
            pkg.delete_from_project()

    def test_get_overridden_properties(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("OvPropPkg"))
        try:
            pkg.set_property_value("General::Graphics::ShowLabels", "True")
            overridden = pkg.get_overridden_properties(0)
            assert isinstance(overridden, RPCollection)
            assert isinstance(overridden.get_count(), int)
            assert overridden.get_count() > 0
        finally:
            pkg.delete_from_project()

    def test_get_overridden_properties_by_pattern(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("OvPropPatPkg"))
        try:
            pkg.set_property_value("General::Graphics::ShowLabels", "True")
            matched = pkg.get_overridden_properties_by_pattern("General*", 0, 0)
            assert isinstance(matched, RPCollection)
            assert isinstance(matched.get_count(), int)
            assert len(list(matched)) >= 1
        finally:
            pkg.delete_from_project()

    def test_get_property_value_conditional(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        pkg = self._create_package(test_project, self._unique("CondPkg"))
        try:
            formal = rhapsody_app.create_new_collection()
            actual = rhapsody_app.create_new_collection()
            pkg.set_property_value("General::Graphics::ShowLabels", "True")
            value = pkg.get_property_value_conditional("General::Graphics::ShowLabels", formal, actual)
            assert isinstance(value, str)
        finally:
            pkg.delete_from_project()

    def test_get_property_value_conditional_explicit(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        pkg = self._create_package(test_project, self._unique("CondExpPkg"))
        try:
            formal = rhapsody_app.create_new_collection()
            actual = rhapsody_app.create_new_collection()
            pkg.set_property_value("General::Graphics::ShowLabels", "True")
            value = pkg.get_property_value_conditional_explicit("General::Graphics::ShowLabels", formal, actual)
            assert isinstance(value, str)
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementNavigationIntegration:
    """Integration tests for RPModelElement navigation/search methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_find_nested_element(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("NavPkg"))
        try:
            class_name = self._unique("NavCls")
            pkg.add_class(class_name)
            found = pkg.find_nested_element(class_name, "Class")
            assert found is not None
            assert isinstance(found, RPModelElement)
            assert found.get_name() == class_name

            not_found = pkg.find_nested_element(self._unique("Missing"), "Class")
            assert not_found.get_name() == ""
        finally:
            pkg.delete_from_project()

    def test_find_nested_element_recursive(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RecPkg"))
        try:
            subpkg = pkg.add_package(self._unique("SubPkg"))
            class_name = self._unique("DeepCls")
            subpkg.add_class(class_name)
            not_found = pkg.find_nested_element(class_name, "Class")
            assert not_found.get_name() == ""
            found = pkg.find_nested_element_recursive(class_name, "Class")
            assert found is not None
            assert isinstance(found, RPModelElement)
            assert found.get_name() == class_name
        finally:
            pkg.delete_from_project()

    def test_find_elements_by_full_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("FullNamePkg"))
        try:
            class_name = self._unique("FullNameCls")
            pkg.add_class(class_name)
            full_path = f"{pkg.get_name()}::{class_name}"
            found = test_project.find_elements_by_full_name(full_path, "Class")
            assert found is not None
            assert isinstance(found, RPModelElement)
            assert found.get_name() == class_name
        finally:
            pkg.delete_from_project()

    def test_get_nested_elements_recursive(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RecNestPkg"))
        try:
            pkg.add_class(self._unique("Child1"))
            pkg.add_class(self._unique("Child2"))
            elements = pkg.get_nested_elements_recursive()
            assert isinstance(elements, RPCollection)
            assert isinstance(elements.get_count(), int)
            assert len(list(elements)) >= 3
        finally:
            pkg.delete_from_project()

    def test_get_full_path_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("PathPkg"))
        try:
            class_name = self._unique("PathCls")
            cls = pkg.add_class(class_name)
            full_path = cls.get_full_path_name()
            assert isinstance(full_path, str)
            assert pkg.get_name() in full_path
            assert class_name in full_path
        finally:
            pkg.delete_from_project()

    def test_get_full_path_name_in(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("PathInPkg"))
        try:
            class_name = self._unique("PathInCls")
            cls = pkg.add_class(class_name)
            path_in = cls.get_full_path_name_in()
            assert isinstance(path_in, str)
            assert class_name in path_in
            assert pkg.get_name() in path_in
        finally:
            pkg.delete_from_project()

    def test_get_project(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ProjPkg"))
        try:
            class_name = self._unique("ProjCls")
            cls = pkg.add_class(class_name)
            project = cls.get_project()
            assert project is not None
            assert isinstance(project, RPProject)
            assert project.get_name() == test_project.get_name()
        finally:
            pkg.delete_from_project()

    def test_set_owner(self, test_project: RPProject) -> None:
        pkg1 = self._create_package(test_project, self._unique("OwnerPkg1"))
        pkg2 = self._create_package(test_project, self._unique("OwnerPkg2"))
        try:
            cls = pkg1.add_class(self._unique("OwnerCls"))
            cls.set_owner(pkg2)
            owner = cls.get_owner()
            assert owner is not None
            assert isinstance(owner, RPModelElement)
            assert owner.get_name() == pkg2.get_name()
        finally:
            pkg2.delete_from_project()
            pkg1.delete_from_project()

    def test_has_nested_elements(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("HasNestPkg"))
        try:
            empty_pkg = pkg.add_package(self._unique("EmptyPkg"))
            assert empty_pkg.has_nested_elements() == 0
            assert isinstance(empty_pkg.has_nested_elements(), int)
            empty_pkg.add_class(self._unique("SomeCls"))
            assert empty_pkg.has_nested_elements() == 1
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementCloningTemplatesIntegration:
    """Integration tests for RPModelElement clone, change-to and template methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_clone(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ClonePkg"))
        try:
            cls = pkg.add_class(self._unique("Original"))
            original_guid = cls.get_guid()

            clone_name = self._unique("Clone")
            cloned = cls.clone(clone_name, pkg)
            assert cloned is not None
            assert isinstance(cloned, RPModelElement)
            assert cloned.get_name() == clone_name
            assert cloned.get_guid() != original_guid
        finally:
            pkg.delete_from_project()

    def test_change_to(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ChangePkg"))
        try:
            cls = pkg.add_class(self._unique("ToChange"))
            assert cls.get_meta_class() == "Class"

            changed = cls.change_to("ClassCategory")
            assert changed is not None
            assert isinstance(changed, RPModelElement)
            assert changed.get_meta_class() == "ClassCategory"
        finally:
            pkg.delete_from_project()

    def test_is_a_template(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IsTemplPkg"))
        try:
            cls = pkg.add_class(self._unique("PlainClass"))
            result = cls.is_a_template()
            assert result == 0
            assert isinstance(result, int)
        finally:
            pkg.delete_from_project()

    def test_get_of_template_on_plain_element(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("OfTemplPkg"))
        try:
            cls = pkg.add_class(self._unique("Plain"))
            of_tmpl = cls.get_of_template()
            assert of_tmpl is not None
            assert isinstance(of_tmpl, RPModelElement)
            assert of_tmpl.get_name() == ""
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Template instantiation API may not be available")
    def test_become_template_instantiation_of(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("TemplInstPkg"))
        try:
            template_cls = pkg.add_class(self._unique("TemplateClass"))
            normal_cls = pkg.add_class(self._unique("NormalClass"))
            normal_cls.become_template_instantiation_of(template_cls)
            of_tmpl = normal_cls.get_of_template()
            assert of_tmpl is not None
            assert of_tmpl.get_name() == template_cls.get_name()
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Template parameter API may not be available")
    def test_set_of_template(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetOfTemplPkg"))
        try:
            template_cls = pkg.add_class(self._unique("Templ"))
            normal_cls = pkg.add_class(self._unique("Normal"))
            normal_cls.set_of_template(template_cls)
            of_tmpl = normal_cls.get_of_template()
            assert of_tmpl is not None
            assert of_tmpl.get_name() == template_cls.get_name()
        finally:
            pkg.delete_from_project()

    def test_get_template_parameters_on_plain_element(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("TemplParamsPkg"))
        try:
            cls = pkg.add_class(self._unique("Plain"))
            params = cls.get_template_parameters()
            assert params is not None
            assert isinstance(params, RPCollection)
            assert isinstance(params.get_count(), int)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Template instantiation API may not be available")
    def test_get_ti(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("GetTiPkg"))
        try:
            template_cls = pkg.add_class(self._unique("TiTempl"))
            normal_cls = pkg.add_class(self._unique("TiNormal"))
            normal_cls.become_template_instantiation_of(template_cls)
            ti = normal_cls.get_ti()
            assert ti is not None
            assert isinstance(ti, RPModelElement)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Template instantiation API may not be available")
    def test_set_ti(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetTiPkg"))
        try:
            template_cls = pkg.add_class(self._unique("SetTiTempl"))
            normal_cls = pkg.add_class(self._unique("SetTiNormal"))
            normal_cls.become_template_instantiation_of(template_cls)
            ti = normal_cls.get_ti()
            assert ti is not None
            # set_ti should accept the same ti object
            normal_cls.set_ti(ti)
            ti_after = normal_cls.get_ti()
            assert ti_after is not None
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="Template instantiation API may not be available")
    def test_synchronize_template_instantiation(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SyncTemplPkg"))
        try:
            template_cls = pkg.add_class(self._unique("SyncTempl"))
            normal_cls = pkg.add_class(self._unique("SyncNormal"))
            normal_cls.become_template_instantiation_of(template_cls)
            normal_cls.synchronize_template_instantiation()
            # No return value: just verify no exception
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementRedefinesConstraintsIntegration:
    """Integration tests for RPModelElement redefine and constraint methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_add_redefines_and_get_redefines(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RedefPkg"))
        try:
            base_cls = pkg.add_class(self._unique("BaseCls"))
            base_op = base_cls.add_operation("baseOp")
            child_cls = pkg.add_class(self._unique("ChildCls"))
            new_op = child_cls.add_operation("baseOp")
            new_op.add_redefines(base_op)

            redefines = new_op.get_redefines()
            assert isinstance(redefines, RPCollection)
            assert isinstance(redefines.get_count(), int)
            assert redefines.get_count() >= 1
        finally:
            pkg.delete_from_project()

    def test_remove_redefines(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RemRedefPkg"))
        try:
            base_cls = pkg.add_class(self._unique("RemBaseCls"))
            base_op = base_cls.add_operation("baseOp")
            child_cls = pkg.add_class(self._unique("RemChildCls"))
            new_op = child_cls.add_operation("baseOp")
            new_op.add_redefines(base_op)

            redefines_before = new_op.get_redefines()
            assert isinstance(redefines_before, RPCollection)
            assert redefines_before.get_count() >= 1

            new_op.remove_redefines(base_op)

            redefines_after = new_op.get_redefines()
            assert isinstance(redefines_after, RPCollection)
            assert redefines_after.get_count() == 0
        finally:
            pkg.delete_from_project()

    def test_get_constraints(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ConstrPkg"))
        try:
            cls = pkg.add_class(self._unique("ConstrCls"))
            constraints = cls.get_constraints()
            assert constraints is not None
            assert isinstance(constraints, RPCollection)
            assert isinstance(constraints.get_count(), int)
        finally:
            pkg.delete_from_project()

    def test_get_constraints_by_him(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ConstrHimPkg"))
        try:
            cls = pkg.add_class(self._unique("ConstrHimCls"))
            constraints = cls.get_constraints_by_him()
            assert constraints is not None
            assert isinstance(constraints, RPCollection)
            assert isinstance(constraints.get_count(), int)
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementOslcRemoteIntegration:
    """Integration tests for RPModelElement OSLC, remote and requirement traceability methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_create_oslc_link_raises_not_implemented(self, test_project: RPProject) -> None:
        with pytest.raises(NotImplementedError):
            test_project.create_oslc_link("someType", "http://example.com")

    def test_delete_oslc_link_raises_not_implemented(self, test_project: RPProject) -> None:
        with pytest.raises(NotImplementedError):
            test_project.delete_oslc_link("someType", "http://example.com")

    def test_get_oslc_links_raises_not_implemented(self, test_project: RPProject) -> None:
        with pytest.raises(NotImplementedError):
            test_project.get_oslc_links()

    def test_get_hyper_links_returns_empty_collection(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("HyperLinkPkg"))
        try:
            cls = pkg.add_class(self._unique("HyperLinkCls"))
            hyper_links = cls.get_hyper_links()
            assert isinstance(hyper_links, RPCollection)
            assert isinstance(hyper_links.get_count(), int)
            assert hyper_links.get_count() == 0
            assert len(list(hyper_links)) == 0
        finally:
            pkg.delete_from_project()

    def test_get_remote_uri_returns_empty_string(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RemoteUriPkg"))
        try:
            cls = pkg.add_class(self._unique("RemoteUriCls"))
            uri = cls.get_remote_uri()
            assert isinstance(uri, str)
            assert uri == ""
        finally:
            pkg.delete_from_project()

    def test_is_remote_returns_zero(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IsRemotePkg"))
        try:
            cls = pkg.add_class(self._unique("IsRemoteCls"))
            result = cls.is_remote()
            assert isinstance(result, int)
            assert result == 0
        finally:
            pkg.delete_from_project()

    def test_get_rmm_url_returns_empty_string(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RmmUrlPkg"))
        try:
            cls = pkg.add_class(self._unique("RmmUrlCls"))
            url = cls.get_rmm_url()
            assert isinstance(url, str)
            assert url == ""
        finally:
            pkg.delete_from_project()

    def test_get_requirement_traceability_handle_default(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ReqTracePkg"))
        try:
            cls = pkg.add_class(self._unique("ReqTraceCls"))
            handle = cls.get_requirement_traceability_handle()
            assert isinstance(handle, int)
        finally:
            pkg.delete_from_project()

    def test_set_and_get_requirement_traceability_handle_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ReqTraceRoundPkg"))
        try:
            cls = pkg.add_class(self._unique("ReqTraceRoundCls"))
            handle_value = 12345
            cls.set_requirement_traceability_handle(handle_value)
            retrieved = cls.get_requirement_traceability_handle()
            assert isinstance(retrieved, int)
            assert retrieved == handle_value
        finally:
            pkg.delete_from_project()
