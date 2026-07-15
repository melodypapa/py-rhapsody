"""Integration tests for RPModelElement and RPCollection with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid
from pathlib import Path

import pytest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.models.core import AddToModelMode, RPCollection, RPModelElement, RPUnit
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from tests.integration.conftest import TEST_PROJECT_DIR


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
class TestRPCollectionAddItemIntegration:
    """Integration tests for RPCollection.add_item with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_add_item_appends_and_count_increases(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        pkg = self._create_package(test_project, self._unique("AddItemPkg"))
        try:
            cls1 = pkg.add_class(self._unique("AddItemCls1"))
            cls2 = pkg.add_class(self._unique("AddItemCls2"))

            collection = rhapsody_app.create_new_collection()
            assert isinstance(collection, RPCollection)

            before = collection.get_count()
            assert isinstance(before, int)
            assert before == 0

            collection.add_item(cls1)
            collection.add_item(cls2)
            after = collection.get_count()
            assert isinstance(after, int)
            assert after == before + 2

            items = [item.get_name() for item in collection]
            assert cls1.get_name() in items
            assert cls2.get_name() in items
        finally:
            pkg.delete_from_project()

    def test_add_item_idempotent_on_same_element(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        pkg = self._create_package(test_project, self._unique("AddItemIdemPkg"))
        try:
            cls = pkg.add_class(self._unique("AddItemIdemCls"))

            collection = rhapsody_app.create_new_collection()
            assert isinstance(collection, RPCollection)

            collection.add_item(cls)
            collection.add_item(cls)
            assert collection.get_count() == 2

            names = [item.get_name() for item in collection]
            assert names.count(cls.get_name()) == 2
        finally:
            pkg.delete_from_project()


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


@pytest.mark.integration
class TestRPModelElementMetadataIntegration:
    """Integration tests for RPModelElement metadata/icon/GUID methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_get_binary_id(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("BinIdPkg"))
        try:
            cls = pkg.add_class(self._unique("BinIdCls"))
            binary_id = cls.get_binary_id()
            assert isinstance(binary_id, bytes)
            assert len(binary_id) > 0

            guid = cls.get_guid()
            assert isinstance(guid, str)
            assert len(guid) > 0
        finally:
            pkg.delete_from_project()

    def test_get_interface_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IntNamePkg"))
        try:
            cls = pkg.add_class(self._unique("IntNameCls"))
            iface = cls.get_interface_name()
            assert isinstance(iface, str)
            assert iface == "IRPClass"
        finally:
            pkg.delete_from_project()

    def test_get_is_of_meta_class_class(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IsOfPkg"))
        try:
            cls = pkg.add_class(self._unique("IsOfCls"))
            result = cls.get_is_of_meta_class("Class")
            assert result

            not_result = cls.get_is_of_meta_class("Package")
            assert not not_result
        finally:
            pkg.delete_from_project()

    def test_get_icon_file_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IconPkg"))
        try:
            cls = pkg.add_class(self._unique("IconCls"))
            icon = cls.get_icon_file_name()
            assert isinstance(icon, str)
            assert len(icon) > 0
        finally:
            pkg.delete_from_project()

    def test_get_overlay_icon_file_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("OverlayIconPkg"))
        try:
            cls = pkg.add_class(self._unique("OverlayIconCls"))
            overlay = cls.get_overlay_icon_file_name()
            assert isinstance(overlay, str)
        finally:
            pkg.delete_from_project()

    def test_get_decoration_style_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DecoPkg"))
        try:
            cls = pkg.add_class(self._unique("DecoCls"))
            style = cls.get_decoration_style()
            assert isinstance(style, str)

            cls.set_decoration_style("None")
            after = cls.get_decoration_style()
            assert after == "None"
        finally:
            pkg.delete_from_project()

    def test_get_is_external(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IsExtPkg"))
        try:
            cls = pkg.add_class(self._unique("IsExtCls"))
            result = cls.get_is_external()
            assert isinstance(result, int)
            assert result == 0
        finally:
            pkg.delete_from_project()

    def test_get_is_unresolved(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("IsUnresPkg"))
        try:
            cls = pkg.add_class(self._unique("IsUnresCls"))
            result = cls.get_is_unresolved()
            assert isinstance(result, int)
            assert result == 0
        finally:
            pkg.delete_from_project()

    def test_get_user_defined_meta_class(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("UdmcPkg"))
        try:
            cls = pkg.add_class(self._unique("UdmcCls"))
            udmc = cls.get_user_defined_meta_class()
            assert isinstance(udmc, str)
            assert udmc == ""
        finally:
            pkg.delete_from_project()

    def test_is_modified_after_set_name(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ModPkg"))
        try:
            cls = pkg.add_class(self._unique("ModCls"))
            cls.set_name(self._unique("Renamed"))
            modified = cls.is_modified()
            assert modified
        finally:
            pkg.delete_from_project()

    def test_set_guid_and_get_guid(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("GuidPkg"))
        try:
            cls = pkg.add_class(self._unique("GuidCls"))
            guid_hex = uuid.uuid4().hex.upper()
            new_guid = "{" + guid_hex[:8] + "-" + guid_hex[8:12] + "-" + guid_hex[12:16] + "-" + guid_hex[16:20] + "-" + guid_hex[20:32] + "}"
            cls.set_guid(new_guid)
            retrieved = cls.get_guid()
            assert isinstance(retrieved, str)
            assert retrieved == new_guid
        finally:
            pkg.delete_from_project()

    def test_get_tool_tip_html(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ToolTipPkg"))
        try:
            cls = pkg.add_class(self._unique("ToolTipCls"))
            html = cls.get_tool_tip_html()
            assert isinstance(html, str)
            assert len(html) > 0
        finally:
            pkg.delete_from_project()

    def test_get_is_show_display_name_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ShowDnPkg"))
        try:
            cls = pkg.add_class(self._unique("ShowDnCls"))
            original = cls.get_is_show_display_name()
            assert isinstance(original, int)

            cls.set_is_show_display_name(0)
            assert cls.get_is_show_display_name() == 0

            cls.set_is_show_display_name(1)
            assert cls.get_is_show_display_name() == 1
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPModelElementDiagnosticsUiIntegration:
    """Integration tests for RPModelElement diagnostics/annotations/UI-action methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_error_message_empty_after_success(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ErrPkg"))
        try:
            cls = pkg.add_class(self._unique("ErrCls"))
            cls.get_name()
            message = cls.error_message()
            assert message == ""
            assert isinstance(message, str)
        finally:
            pkg.delete_from_project()

    def test_get_error_message_empty_after_success(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("GetErrPkg"))
        try:
            cls = pkg.add_class(self._unique("GetErrCls"))
            cls.get_name()
            message = cls.get_error_message()
            assert message == ""
            assert isinstance(message, str)
        finally:
            pkg.delete_from_project()

    def test_get_annotations_empty_for_plain_class(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("AnnPkg"))
        try:
            cls = pkg.add_class(self._unique("AnnCls"))
            annotations = cls.get_annotations()
            assert isinstance(annotations, RPCollection)
            assert isinstance(annotations.get_count(), int)
            assert annotations.get_count() == 0
            assert len(list(annotations)) == 0
        finally:
            pkg.delete_from_project()

    def test_get_controlled_files_empty(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("CtrlPkg"))
        try:
            cls = pkg.add_class(self._unique("CtrlCls"))
            files = cls.get_controlled_files()
            assert isinstance(files, RPCollection)
            assert isinstance(files.get_count(), int)
            assert files.get_count() == 0
            assert len(list(files)) == 0
        finally:
            pkg.delete_from_project()

    def test_get_save_unit(self, test_project: RPProject) -> None:
        from rhapsody_cli.models.core import RPUnit

        pkg = self._create_package(test_project, self._unique("SaveUnitPkg"))
        try:
            cls = pkg.add_class(self._unique("SaveUnitCls"))
            unit = cls.get_save_unit()
            assert isinstance(unit, RPUnit)
            unit_name = unit.get_name()
            assert isinstance(unit_name, str)
            assert pkg.get_name() in unit_name
        finally:
            pkg.delete_from_project()

    def test_get_main_diagram_and_set_main_diagram_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        try:
            cls = pkg.add_class(self._unique("DiagCls"))
            diagram_name = self._unique("MyClassDiagram")
            diagram = cls.add_new_aggr("ClassDiagram", diagram_name)
            assert diagram is not None
            diagram_guid = diagram.get_guid()
            assert isinstance(diagram_guid, str)
            assert len(diagram_guid) > 0

            cls.set_main_diagram(diagram)
            retrieved = cls.get_main_diagram()
            assert retrieved is not None
            assert retrieved.get_guid() == diagram_guid
        finally:
            pkg.delete_from_project()

    def test_has_panel_widget_returns_zero(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("PanelPkg"))
        try:
            cls = pkg.add_class(self._unique("PanelCls"))
            result = cls.has_panel_widget()
            assert isinstance(result, int)
            assert result == 0
        finally:
            pkg.delete_from_project()

    def test_high_light_element_does_not_raise(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("HLPkg"))
        try:
            cls = pkg.add_class(self._unique("HLCls"))
            cls.high_light_element()
        finally:
            pkg.delete_from_project()

    def test_locate_in_browser_returns_int(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("LocPkg"))
        try:
            cls = pkg.add_class(self._unique("LocCls"))
            result = cls.locate_in_browser()
            assert isinstance(result, int)
        finally:
            pkg.delete_from_project()

    def test_open_features_dialog_does_not_raise(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("FeatPkg"))
        try:
            cls = pkg.add_class(self._unique("FeatCls"))
            cls.open_features_dialog(0)
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires RPRelation/port helpers from relations subpackage", strict=False)
    def test_add_link_to_element(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("LinkPkg"))
        try:
            cls1 = pkg.add_class(self._unique("LinkSrc"))
            cls2 = pkg.add_class(self._unique("LinkTgt"))
            from typing import cast

            none_elem: RPModelElement = cast(RPModelElement, None)
            cls1.add_link_to_element(cls2, none_elem, none_elem, none_elem)
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPUnitPersistenceIntegration:
    """Integration tests for RPUnit filename/language/path/lifecycle methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        assert isinstance(pkg, RPUnit)
        return pkg

    def test_set_and_get_filename_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("UnitPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            new_filename = self._unique("renamed_unit")
            pkg.set_filename(new_filename)
            filename = pkg.get_filename()
            assert new_filename in filename
            assert isinstance(filename, str)
        finally:
            pkg.delete_from_project()

    def test_set_and_get_language_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("LangPkg"))
        try:
            original = pkg.get_language()
            assert isinstance(original, str)
            pkg.set_language("C++", 0)
            language = pkg.get_language()
            assert language == "C++"
            assert isinstance(language, str)
            pkg.set_language(original, 0)
        finally:
            pkg.delete_from_project()

    def test_get_unit_path_full_and_relative(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("UnitPathPkg"))
        try:
            full_path = pkg.get_unit_path(1)
            assert isinstance(full_path, str)
            assert len(full_path) > 0
            assert pkg.get_filename() in full_path

            rel_path = pkg.get_unit_path(0)
            assert isinstance(rel_path, str)
            assert len(rel_path) > 0
            assert pkg.get_filename() in rel_path
        finally:
            pkg.delete_from_project()

    def test_set_and_get_unit_path_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SetUnitPathPkg"))
        try:
            original = pkg.get_unit_path(1)
            assert isinstance(original, str)

            new_path = original
            pkg.set_unit_path(new_path)
            updated = pkg.get_unit_path(1)
            assert updated == new_path
            assert isinstance(updated, str)
        finally:
            pkg.delete_from_project()

    def test_get_current_directory_matches_project(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("CurDirPkg"))
        try:
            current_dir = pkg.get_current_directory()
            assert isinstance(current_dir, str)
            current_path = Path(current_dir)
            assert TEST_PROJECT_DIR == current_path or TEST_PROJECT_DIR in current_path.parents
        finally:
            pkg.delete_from_project()

    def test_save_after_mutation_clears_modified(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SavePkg"))
        try:
            pkg.set_name(self._unique("SavePkgRenamed"))
            assert pkg.is_modified() == 1
            pkg.save()
            assert pkg.is_modified() == 0
        finally:
            pkg.delete_from_project()

    def test_load_and_unload_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("LoadPkg"))
        try:
            pkg.unload()
            assert pkg.get_is_stub() == 1
            pkg.load(1)
            assert pkg.get_is_stub() == 0
        finally:
            pkg.delete_from_project()

    def test_get_last_modified_time_after_save(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ModTimePkg"))
        try:
            pkg.set_name(self._unique("ModTimePkgRenamed"))
            pkg.save()
            modified_time = pkg.get_last_modified_time()
            assert isinstance(modified_time, str)
            assert len(modified_time) > 0
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPUnitCmStateIntegration:
    """Integration tests for RPUnit configuration-management/read-only/stub methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        assert isinstance(pkg, RPUnit)
        return pkg

    def test_set_and_get_read_only_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ReadOnlyPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            pkg.set_read_only(True)
            assert pkg.is_read_only() is True
            pkg.set_read_only(False)
            assert pkg.is_read_only() is False
        finally:
            pkg.delete_from_project()

    def test_set_and_get_cm_header_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("CmHeaderPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            header = self._unique("CMHeader")
            pkg.set_cm_header(header)
            retrieved = pkg.get_cm_header()
            assert isinstance(retrieved, str)
            assert retrieved == header
        finally:
            pkg.delete_from_project()

    def test_get_cm_state_returns_int(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("CmStatePkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            state = pkg.get_cm_state()
            assert isinstance(state, int)
        finally:
            pkg.delete_from_project()

    def test_get_is_stub_after_unload(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("StubPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            assert pkg.get_is_stub() == 0
            pkg.unload()
            assert pkg.get_is_stub() == 1
            pkg.load(1)
            assert pkg.get_is_stub() == 0
        finally:
            pkg.delete_from_project()

    def test_set_and_get_separate_save_unit_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("SeparatePkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            original = pkg.is_separate_save_unit()
            assert isinstance(original, int)
            pkg.set_separate_save_unit(1)
            assert pkg.is_separate_save_unit() == 1
            pkg.set_separate_save_unit(0)
            assert pkg.is_separate_save_unit() == 0
            pkg.set_separate_save_unit(original)
        finally:
            pkg.delete_from_project()

    def test_set_and_get_include_in_next_load_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("NextLoadPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            original = pkg.get_include_in_next_load()
            assert isinstance(original, int)
            pkg.set_include_in_next_load(1)
            assert pkg.get_include_in_next_load() == 1
            pkg.set_include_in_next_load(0)
            assert pkg.get_include_in_next_load() == 0
            pkg.set_include_in_next_load(original)
        finally:
            pkg.delete_from_project()


@pytest.mark.integration
class TestRPUnitCrossProjectIntegration:
    """Integration tests for RPUnit cross-project and nesting methods."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        assert isinstance(pkg, RPUnit)
        return pkg

    def test_get_nested_save_units_empty_on_plain_package(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("NestPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            units = pkg.get_nested_save_units()
            assert isinstance(units, RPCollection)
            assert isinstance(units.get_count(), int)
            assert len(list(units)) == 0
        finally:
            pkg.delete_from_project()

    def test_get_nested_save_units_count_matches_collection(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("NestPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            sub_pkg = pkg.add_package(self._unique("SubPkg"))
            sub_pkg.set_separate_save_unit(1)
            sub_pkg.save()

            count = pkg.get_nested_save_units_count()
            units = pkg.get_nested_save_units()
            assert isinstance(count, int)
            assert count == len(list(units))
            assert count >= 1
        finally:
            pkg.delete_from_project()

    def test_get_structure_diagrams_empty_on_class(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("StructPkg"))
        try:
            cls = pkg.add_class(self._unique("StructCls"))
            assert isinstance(cls, RPUnit)
            diagrams = cls.get_structure_diagrams()
            assert isinstance(diagrams, RPCollection)
            assert isinstance(diagrams.get_count(), int)
            assert len(list(diagrams)) == 0
        finally:
            pkg.delete_from_project()

    def test_get_add_to_model_mode_returns_int(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("AddModePkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            mode = pkg.get_add_to_model_mode()
            assert isinstance(mode, int)
            assert mode in (member.value for member in AddToModelMode)
        finally:
            pkg.delete_from_project()

    def test_is_reference_unit_false_for_local_unit(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("RefPkg"))
        try:
            assert isinstance(pkg, RPUnit)
            pkg.save()
            assert pkg.is_reference_unit() == 0
        finally:
            pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires a second live project as copy target", strict=False)
    def test_copy_to_another_project(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        import shutil
        import tempfile

        src_pkg = self._create_package(test_project, self._unique("CopySrcPkg"))
        tmp_dir = tempfile.mkdtemp(prefix="rhapsody_copy_")
        try:
            src_pkg.save()
            target_project = rhapsody_app.create_new_project(tmp_dir, self._unique("CopyTarget"))
            try:
                copied = src_pkg.copy_to_another_project(target_project)
                assert copied is not None
                assert isinstance(copied, RPModelElement)
                assert copied.get_name() == src_pkg.get_name()
                assert copied.is_reference_unit() == 0
            finally:
                target_project.close()
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            src_pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires a second live project as move target", strict=False)
    def test_move_to_another_project_leave_a_reference(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        import shutil
        import tempfile

        src_pkg = self._create_package(test_project, self._unique("MoveSrcPkg"))
        tmp_dir = tempfile.mkdtemp(prefix="rhapsody_move_")
        try:
            src_pkg.save()
            target_project = rhapsody_app.create_new_project(tmp_dir, self._unique("MoveTarget"))
            try:
                moved = src_pkg.move_to_another_project_leave_a_reference(target_project)
                assert moved is not None
                assert isinstance(moved, RPModelElement)
                assert moved.get_name() == src_pkg.get_name()
            finally:
                target_project.close()
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            src_pkg.delete_from_project()

    @pytest.mark.xfail(reason="requires a second live project as reference target", strict=False)
    def test_reference_to_another_project(self, test_project: RPProject, rhapsody_app: RhapsodyApplication) -> None:
        import shutil
        import tempfile

        src_pkg = self._create_package(test_project, self._unique("RefSrcPkg"))
        tmp_dir = tempfile.mkdtemp(prefix="rhapsody_ref_")
        try:
            src_pkg.save()
            target_project = rhapsody_app.create_new_project(tmp_dir, self._unique("RefTarget"))
            try:
                ref = src_pkg.reference_to_another_project(target_project)
                assert ref is not None
                assert isinstance(ref, RPModelElement)
                assert isinstance(ref, RPUnit)
                assert ref.is_reference_unit() == 1
            finally:
                target_project.close()
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            src_pkg.delete_from_project()
