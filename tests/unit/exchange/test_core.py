"""Tests for RhapsodyModelHelper base class.

UTS_XCH_00009: find_or_create_package sanitizes name and delegates to add_new_aggr
UTS_XCH_00010: find_or_create_class creates via add_new_aggr
UTS_XCH_00011: find_or_create_operation on package uses add_global_function
UTS_XCH_00012: find_or_create_operation on class uses add_new_aggr
UTS_XCH_00013: find_or_create_argument uses add_argument
UTS_XCH_00014: find_or_create_attribute creates via add_new_aggr
UTS_XCH_00015: find_or_create_type sets kind after creation
UTS_XCH_00016: find_or_create_object creates via add_new_aggr
UTS_XCH_00017: find_or_create_enumeration_literal creates via add_new_aggr
UTS_XCH_00018: find_child_by_name returns matching child
UTS_XCH_00019: find_child_by_name returns None when no match
UTS_XCH_00020: apply_stereotypes infers meta_type from element
UTS_XCH_00021: apply_stereotypes skips already-applied stereotypes
UTS_XCH_00022: apply_tags uses set_property_value
UTS_XCH_00023: resolve_classifier searches project recursively
UTS_XCH_00024: resolve_classifier returns None when not found
UTS_XCH_00025: get_classifier_name is None-safe
UTS_XCH_00026: _set_type_kind calls set_kind
UTS_XCH_00027: _collect_children returns nested elements
UTS_XCH_00028: _collect_children merges package globals
UTS_XCH_00029: _get_project_name walks owner chain
UTS_XCH_00030: find_or_create returns existing element without creating duplicate
"""

from typing import Any
from unittest.mock import MagicMock

from rhapsody_cli.exchange.core import RhapsodyModelHelper
from rhapsody_cli.models.core import RPModelElement


def _make_helper(project: Any = None) -> RhapsodyModelHelper:
    """Build a RhapsodyModelHelper with a mocked app and project.

    Skips RhapsodyApplication.connect() entirely.
    """
    app = MagicMock()
    helper = RhapsodyModelHelper.__new__(RhapsodyModelHelper)
    helper.app = app  # type: ignore[assignment]
    helper.project = project
    return helper


class TestFindOrCreatePackage:
    """UTS_XCH_00009, UTS_XCH_00030: find_or_create_package."""

    def test_creates_package_with_sanitized_name(self) -> None:
        """UTS_XCH_00009: spaces in name replaced with underscores before add_new_aggr."""
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_pkg = MagicMock()
        new_pkg.get_name.return_value = "My_Pkg"
        parent.add_new_aggr.return_value = new_pkg
        helper = _make_helper()

        result = helper.find_or_create_package(parent, "My Pkg")

        parent.add_new_aggr.assert_called_once_with("Package", "My_Pkg")
        assert result.get_name() == "My_Pkg"

    def test_returns_existing_package_without_creating(self) -> None:
        """UTS_XCH_00030: if a Package child with matching name exists, return it."""
        existing = MagicMock()
        existing.get_meta_class.return_value = "Package"
        existing.get_name.return_value = "Existing"
        parent = MagicMock()
        parent.get_nested_elements.return_value = [existing]
        helper = _make_helper()

        result = helper.find_or_create_package(parent, "Existing")

        parent.add_new_aggr.assert_not_called()
        assert result.get_name() == "Existing"


class TestFindOrCreateClass:
    """UTS_XCH_00010, UTS_XCH_00030: find_or_create_class."""

    def test_creates_class_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_cls = MagicMock()
        new_cls.get_name.return_value = "Widget"
        parent.add_new_aggr.return_value = new_cls
        helper = _make_helper()

        result = helper.find_or_create_class(parent, "Widget")

        parent.add_new_aggr.assert_called_once_with("Class", "Widget")
        assert result.get_name() == "Widget"


class TestFindOrCreateOperation:
    """UTS_XCH_00011, UTS_XCH_00012: find_or_create_operation."""

    def test_on_package_uses_add_global_function(self) -> None:
        """UTS_XCH_00011: global function path when parent is a Package."""
        parent = MagicMock()
        parent.get_meta_class.return_value = "Package"
        parent.get_nested_elements.return_value = []
        new_op = MagicMock()
        new_op.get_name.return_value = "globalFn"
        parent.add_global_function.return_value = new_op
        helper = _make_helper()

        result = helper.find_or_create_operation(parent, "globalFn")

        parent.add_global_function.assert_called_once_with("globalFn")
        parent.add_new_aggr.assert_not_called()
        assert result.get_name() == "globalFn"

    def test_on_class_uses_add_new_aggr(self) -> None:
        """UTS_XCH_00012: regular add_new_aggr path when parent is a Class."""
        parent = MagicMock()
        parent.get_meta_class.return_value = "Class"
        parent.get_nested_elements.return_value = []
        new_op = MagicMock()
        new_op.get_name.return_value = "method"
        parent.add_new_aggr.return_value = new_op
        helper = _make_helper()

        helper.find_or_create_operation(parent, "method")

        parent.add_new_aggr.assert_called_once_with("Operation", "method")
        parent.add_global_function.assert_not_called()


class TestFindOrCreateArgument:
    """UTS_XCH_00013: find_or_create_argument."""

    def test_uses_add_argument(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_arg = MagicMock()
        new_arg.get_name.return_value = "x"
        parent.add_argument.return_value = new_arg
        helper = _make_helper()

        result = helper.find_or_create_argument(parent, "x")

        parent.add_argument.assert_called_once_with("x")
        assert result.get_name() == "x"


class TestFindOrCreateAttribute:
    """UTS_XCH_00014: find_or_create_attribute."""

    def test_creates_attribute_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_attr = MagicMock()
        new_attr.get_name.return_value = "count"
        parent.add_new_aggr.return_value = new_attr
        helper = _make_helper()

        result = helper.find_or_create_attribute(parent, "count")

        parent.add_new_aggr.assert_called_once_with("Attribute", "count")
        assert result.get_name() == "count"


class TestFindOrCreateType:
    """UTS_XCH_00015, UTS_XCH_00026: find_or_create_type + _set_type_kind."""

    def test_creates_type_and_sets_kind(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_type = MagicMock()
        new_type.get_name.return_value = "Color"
        parent.add_new_aggr.return_value = new_type
        helper = _make_helper()

        result = helper.find_or_create_type(parent, "Color", kind="Enumeration")

        parent.add_new_aggr.assert_called_once_with("Type", "Color")
        new_type.set_kind.assert_called_once_with("Enumeration")
        assert result.get_name() == "Color"

    def test_creates_type_without_kind_skips_set_kind(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_type = MagicMock()
        new_type.get_name.return_value = "Plain"
        parent.add_new_aggr.return_value = new_type
        helper = _make_helper()

        helper.find_or_create_type(parent, "Plain")

        new_type.set_kind.assert_not_called()


class TestFindOrCreateObject:
    """UTS_XCH_00016: find_or_create_object."""

    def test_creates_object_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_obj = MagicMock()
        new_obj.get_name.return_value = "myObj"
        parent.add_new_aggr.return_value = new_obj
        helper = _make_helper()

        result = helper.find_or_create_object(parent, "myObj")

        parent.add_new_aggr.assert_called_once_with("Object", "myObj")
        assert result.get_name() == "myObj"


class TestFindOrCreateEnumerationLiteral:
    """UTS_XCH_00017: find_or_create_enumeration_literal."""

    def test_creates_literal_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_lit = MagicMock()
        new_lit.get_name.return_value = "RED"
        parent.add_new_aggr.return_value = new_lit
        helper = _make_helper()

        result = helper.find_or_create_enumeration_literal(parent, "RED")

        parent.add_new_aggr.assert_called_once_with("EnumerationLiteral", "RED")
        assert result.get_name() == "RED"


class TestFindChildByName:
    """UTS_XCH_00018, UTS_XCH_00019: find_child_by_name."""

    def test_returns_matching_child(self) -> None:
        match = MagicMock()
        match.get_meta_class.return_value = "Class"
        match.get_name.return_value = "Widget"
        other = MagicMock()
        other.get_meta_class.return_value = "Class"
        other.get_name.return_value = "Other"
        parent = MagicMock()
        parent.get_nested_elements.return_value = [other, match]
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Widget")

        assert result is not None
        assert result.get_name() == "Widget"

    def test_returns_none_when_no_match(self) -> None:
        other = MagicMock()
        other.get_meta_class.return_value = "Class"
        other.get_name.return_value = "Other"
        parent = MagicMock()
        parent.get_nested_elements.return_value = [other]
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Missing")

        assert result is None

    def test_filters_by_meta_class(self) -> None:
        """A child with the right name but wrong metaclass is not returned."""
        same_name_diff_type = MagicMock()
        same_name_diff_type.get_meta_class.return_value = "Package"
        same_name_diff_type.get_name.return_value = "Widget"
        parent = MagicMock()
        parent.get_nested_elements.return_value = [same_name_diff_type]
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Widget")

        assert result is None


class TestApplyStereotypes:
    """UTS_XCH_00020, UTS_XCH_00021: apply_stereotypes."""

    def test_infers_meta_type_and_calls_add_stereotype(self) -> None:
        element = MagicMock()
        element.get_meta_class.return_value = "Class"
        element.get_stereotypes.return_value = []
        helper = _make_helper()

        helper.apply_stereotypes(element, ["Interface", "SwComponent"])

        assert element.add_stereotype.call_count == 2
        element.add_stereotype.assert_any_call("Interface", "Class")
        element.add_stereotype.assert_any_call("SwComponent", "Class")

    def test_skips_already_applied_stereotypes(self) -> None:
        """If get_stereotypes() returns an existing stereotype, don't re-add it."""
        existing = MagicMock()
        existing.get_name.return_value = "Interface"
        element = MagicMock()
        element.get_meta_class.return_value = "Class"
        element.get_stereotypes.return_value = [existing]
        helper = _make_helper()

        helper.apply_stereotypes(element, ["Interface", "SwComponent"])

        # Only SwComponent should be added; Interface already present
        element.add_stereotype.assert_called_once_with("SwComponent", "Class")


class TestApplyTags:
    """UTS_XCH_00022: apply_tags uses set_property_value."""

    def test_calls_set_property_value_for_each_tag(self) -> None:
        element = MagicMock()
        helper = _make_helper()

        helper.apply_tags(element, {"status": "active", "count": "3"})

        assert element.set_property_value.call_count == 2
        element.set_property_value.assert_any_call("status", "active")
        element.set_property_value.assert_any_call("count", "3")

    def test_empty_tags_dict_does_nothing(self) -> None:
        element = MagicMock()
        helper = _make_helper()

        helper.apply_tags(element, {})

        element.set_property_value.assert_not_called()


class TestResolveClassifier:
    """UTS_XCH_00023, UTS_XCH_00024: resolve_classifier."""

    def test_searches_project_nested_elements_recursively(self) -> None:
        """Found classifier is returned."""
        target = MagicMock()
        target.get_name.return_value = "Widget"
        target.get_meta_class.return_value = "Class"
        target.get_nested_elements.return_value = []
        sibling = MagicMock()
        sibling.get_name.return_value = "Other"
        sibling.get_meta_class.return_value = "Class"
        sibling.get_nested_elements.return_value = []
        nested_pkg = MagicMock()
        nested_pkg.get_name.return_value = "Sub"
        nested_pkg.get_meta_class.return_value = "Package"
        nested_pkg.get_nested_elements.return_value = [target]
        project = MagicMock()
        project.get_name.return_value = "P"
        project.get_meta_class.return_value = "Project"
        project.get_nested_elements.return_value = [sibling, nested_pkg]
        helper = _make_helper(project=project)

        result = helper.resolve_classifier("Widget")

        assert result is not None
        assert result.get_name() == "Widget"

    def test_returns_none_when_not_found(self) -> None:
        sibling = MagicMock()
        sibling.get_name.return_value = "Other"
        sibling.get_meta_class.return_value = "Class"
        sibling.get_nested_elements.return_value = []
        project = MagicMock()
        project.get_name.return_value = "P"
        project.get_meta_class.return_value = "Project"
        project.get_nested_elements.return_value = [sibling]
        helper = _make_helper(project=project)

        result = helper.resolve_classifier("Missing")

        assert result is None

    def test_returns_none_when_project_is_none(self) -> None:
        helper = _make_helper(project=None)

        result = helper.resolve_classifier("Anything")

        assert result is None


class TestGetClassifierName:
    """UTS_XCH_00025: get_classifier_name."""

    def test_returns_name_of_classifier(self) -> None:
        classifier = MagicMock()
        classifier.get_name.return_value = "Widget"
        helper = _make_helper()

        assert helper.get_classifier_name(classifier) == "Widget"

    def test_returns_none_for_none_input(self) -> None:
        helper = _make_helper()

        assert helper.get_classifier_name(None) is None


class TestSetTypeKind:
    """UTS_XCH_00026: _set_type_kind."""

    def test_calls_set_kind_on_type_element(self) -> None:
        type_element = MagicMock()
        helper = _make_helper()

        helper._set_type_kind(type_element, "Enumeration")

        type_element.set_kind.assert_called_once_with("Enumeration")


class TestCollectChildren:
    """UTS_XCH_00027, UTS_XCH_00028: _collect_children."""

    def test_returns_nested_elements_for_class(self) -> None:
        child1 = MagicMock()
        child1.get_name.return_value = "a"
        child2 = MagicMock()
        child2.get_name.return_value = "b"
        container = MagicMock()
        container.get_meta_class.return_value = "Class"
        container.get_nested_elements.return_value = [child1, child2]
        helper = _make_helper()

        result = helper._collect_children(container)

        assert len(result) == 2
        assert result[0].get_name() == "a"
        assert result[1].get_name() == "b"

    def test_merges_package_globals_when_available(self) -> None:
        """UTS_XCH_00028: Package globals merged into children."""
        nested = MagicMock()
        nested.get_name.return_value = "Nested"
        global_fn = MagicMock()
        global_fn.get_name.return_value = "globalFn"
        global_var = MagicMock()
        global_var.get_name.return_value = "globalVar"
        global_obj = MagicMock()
        global_obj.get_name.return_value = "globalObj"
        pkg = MagicMock()
        pkg.get_meta_class.return_value = "Package"
        pkg.get_nested_elements.return_value = [nested]
        pkg.get_global_functions.return_value = [global_fn]
        pkg.get_global_variables.return_value = [global_var]
        pkg.get_global_objects.return_value = [global_obj]
        helper = _make_helper()

        result = helper._collect_children(pkg)

        names = [e.get_name() for e in result]
        assert "Nested" in names
        assert "globalFn" in names
        assert "globalVar" in names
        assert "globalObj" in names

    def test_package_without_global_getters_returns_only_nested(self) -> None:
        """If global getters are unavailable, fall back to nested elements only.

        Uses spec=RPModelElement so the package-specific global getters are
        absent (they live on RPPackage, not the base class). The implementation's
        ``getattr(container, getter_name, None)`` returns None and skips them.
        """
        nested = MagicMock()
        nested.get_name.return_value = "Nested"
        pkg = MagicMock(spec=RPModelElement)
        pkg.get_meta_class.return_value = "Package"
        pkg.get_nested_elements.return_value = [nested]
        helper = _make_helper()

        result = helper._collect_children(pkg)

        assert len(result) == 1
        assert result[0].get_name() == "Nested"


class TestGetProjectName:
    """UTS_XCH_00029: _get_project_name."""

    def test_walks_owner_chain_to_project(self) -> None:
        project = MagicMock()
        project.get_meta_class.return_value = "Project"
        project.get_name.return_value = "MyProject"
        project.get_owner.return_value = None
        pkg = MagicMock()
        pkg.get_meta_class.return_value = "Package"
        pkg.get_name.return_value = "Sub"
        pkg.get_owner.return_value = project
        helper = _make_helper()

        result = helper._get_project_name(pkg)

        assert result == "MyProject"

    def test_returns_project_name_when_container_is_project(self) -> None:
        project = MagicMock()
        project.get_meta_class.return_value = "Project"
        project.get_name.return_value = "TopLevel"
        project.get_owner.return_value = None
        helper = _make_helper()

        result = helper._get_project_name(project)

        assert result == "TopLevel"

    def test_returns_empty_string_when_no_project_in_chain(self) -> None:
        """If owner chain never reaches a Project, return empty string (defensive)."""
        orphan = MagicMock()
        orphan.get_meta_class.return_value = "Package"
        orphan.get_name.return_value = "Orphan"
        orphan.get_owner.return_value = None
        helper = _make_helper()

        result = helper._get_project_name(orphan)

        assert result == ""


class TestFindOrCreateDependency:
    """UTS_XCH_00031: find_or_create_dependency."""

    def test_creates_dependency_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_dep = MagicMock()
        new_dep.get_name.return_value = "dep1"
        parent.add_new_aggr.return_value = new_dep
        helper = _make_helper()

        result = helper.find_or_create_dependency(parent, "dep1")

        parent.add_new_aggr.assert_called_once_with("Dependency", "dep1")
        assert result.get_name() == "dep1"

    def test_returns_existing_dependency(self) -> None:
        existing = MagicMock()
        existing.get_meta_class.return_value = "Dependency"
        existing.get_name.return_value = "dep1"
        parent = MagicMock()
        parent.get_nested_elements.return_value = [existing]
        helper = _make_helper()

        result = helper.find_or_create_dependency(parent, "dep1")

        parent.add_new_aggr.assert_not_called()
        assert result.get_name() == "dep1"


class TestFindOrCreateGeneralization:
    """UTS_XCH_00032: find_or_create_generalization."""

    def test_creates_generalization_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_gen = MagicMock()
        new_gen.get_name.return_value = "gen1"
        parent.add_new_aggr.return_value = new_gen
        helper = _make_helper()

        result = helper.find_or_create_generalization(parent, "gen1")

        parent.add_new_aggr.assert_called_once_with("Generalization", "gen1")
        assert result.get_name() == "gen1"


class TestFindOrCreateRelation:
    """UTS_XCH_00033: find_or_create_relation."""

    def test_creates_relation_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_rel = MagicMock()
        new_rel.get_name.return_value = "assoc1"
        parent.add_new_aggr.return_value = new_rel
        helper = _make_helper()

        result = helper.find_or_create_relation(parent, "assoc1")

        parent.add_new_aggr.assert_called_once_with("Relation", "assoc1")
        assert result.get_name() == "assoc1"


class TestFindOrCreatePort:
    """UTS_XCH_00034: find_or_create_port."""

    def test_creates_port_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_port = MagicMock()
        new_port.get_name.return_value = "p1"
        parent.add_new_aggr.return_value = new_port
        helper = _make_helper()

        result = helper.find_or_create_port(parent, "p1")

        parent.add_new_aggr.assert_called_once_with("Port", "p1")
        assert result.get_name() == "p1"


class TestFindOrCreateEvent:
    """UTS_XCH_00035: find_or_create_event."""

    def test_creates_event_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_evt = MagicMock()
        new_evt.get_name.return_value = "TickEvent"
        parent.add_new_aggr.return_value = new_evt
        helper = _make_helper()

        result = helper.find_or_create_event(parent, "TickEvent")

        parent.add_new_aggr.assert_called_once_with("Event", "TickEvent")
        assert result.get_name() == "TickEvent"


class TestFindOrCreateEventReception:
    """UTS_XCH_00036: find_or_create_event_reception."""

    def test_creates_reception_via_add_new_aggr(self) -> None:
        parent = MagicMock()
        parent.get_nested_elements.return_value = []
        new_rec = MagicMock()
        new_rec.get_name.return_value = "onTick"
        parent.add_new_aggr.return_value = new_rec
        helper = _make_helper()

        result = helper.find_or_create_event_reception(parent, "onTick")

        parent.add_new_aggr.assert_called_once_with("EventReception", "onTick")
        assert result.get_name() == "onTick"
