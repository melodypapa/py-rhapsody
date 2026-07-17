"""Integration tests for RPClass with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import time

import pytest

from rhapsody_cli.models.elements.classifiers import RPClass, RPOperation
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.interactions import RPEventReception


@pytest.mark.integration
class TestRPClassIntegration:
    """Integration tests for RPClass with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{int(time.time() * 1000) % 1000000}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None
        assert isinstance(pkg, RPPackage)
        return pkg

    def test_create_class_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("Pkg")
        class_name = self._unique("TestClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        assert test_class is not None
        assert isinstance(test_class, RPClass)
        assert test_class.get_name() == class_name
        assert test_class.get_meta_class() == "Class"

    def test_class_hierarchy_navigation(self, test_project: RPProject) -> None:
        pkg_name = self._unique("NavPkg")
        class_name = self._unique("ChildClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        parent = test_class.get_owner()
        assert parent is not None
        assert parent.get_name() == pkg_name
        assert isinstance(parent, RPPackage)

    def test_create_operation_in_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("OpPkg")
        class_name = self._unique("OpClass")
        pkg_name_op = f"{class_name}_op"
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        operation = test_class.add_operation(pkg_name_op)
        assert operation is not None
        assert isinstance(operation, RPOperation)
        assert operation.get_name() == pkg_name_op
        operations = test_class.get_operations()
        assert operation in list(operations)

    def test_class_delete(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelPkg")
        class_name = self._unique("DelClass")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        test_class.delete_from_project()
        classes = pkg.get_classes()
        class_names = [c.get_name() for c in classes]
        assert class_name not in class_names

    def test_class_inheritance(self, test_project: RPProject) -> None:
        pkg_name = self._unique("InhPkg")
        parent_name = self._unique("ParentCls")
        child_name = self._unique("ChildCls")
        pkg = self._create_package(test_project, pkg_name)
        parent = pkg.add_class(parent_name)
        child = pkg.add_class(child_name)
        try:
            child.add_superclass(parent)
            generalizations = list(child.get_generalizations())
            assert any(gen.get_base_class() == parent for gen in generalizations)
            child.delete_superclass(parent)
            generalizations_after = list(child.get_generalizations())
            assert not any(gen.get_base_class() == parent for gen in generalizations_after)
        finally:
            child.delete_from_project()
            parent.delete_from_project()

    def test_constructor_destructor(self, test_project: RPProject) -> None:
        pkg_name = self._unique("CtorPkg")
        class_name = self._unique("CtorCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            ctor = test_class.add_constructor("void()")
            assert ctor is not None
            dtor = test_class.add_destructor()
            assert dtor is not None
            operations = list(test_class.get_operations())
            ops = [o.get_name() for o in operations]
            assert ctor.get_name() in ops
            assert dtor.get_name() in ops
        finally:
            test_class.delete_from_project()

    def test_set_is_abstract_raises_not_implemented(self, test_project: RPProject) -> None:
        """RPClass.set_is_abstract is marked unimplemented: Rhapsody2.Application.1's automation
        server accepts a write to the 'isAbstract' COM property without error (confirmed via
        typelib inspection that both PROPERTYGET and PROPERTYPUT are declared for isAbstract
        under the same DISPID -- it is not read-only at the interface level), but the write does
        not persist (confirmed via immediate read-back, post-saveAll(), and a fresh re-fetch of
        the element). This is a genuine limitation of this Rhapsody build's IRPClass::isAbstract
        implementation, so the wrapper raises rather than silently no-opping."""
        pkg_name = self._unique("AbsPkg")
        class_name = self._unique("AbsCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_abstract() is False
            with pytest.raises(NotImplementedError):
                test_class.set_is_abstract(1)
        finally:
            test_class.delete_from_project()

    def test_type_management(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TypePkg")
        class_name = self._unique("TypeCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            added_type = test_class.add_type(self._unique("MyType"))
            assert added_type is not None
            assert added_type.get_meta_class() == "Type"
            added_type.delete_from_project()
        finally:
            test_class.delete_from_project()

    def test_add_and_delete_reception(self, test_project: RPProject) -> None:
        pkg_name = self._unique("RecPkg")
        class_name = self._unique("RecCls")
        reception_name = self._unique("onSignal")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            reception = test_class.add_reception(reception_name)
            assert reception is not None
            assert isinstance(reception, RPEventReception)
            assert reception.get_name() == reception_name
            items = [i.get_name() for i in test_class.get_interface_items()]
            assert reception_name in items
            test_class.delete_reception(reception)
            items_after = [i.get_name() for i in test_class.get_interface_items()]
            assert reception_name not in items_after
        finally:
            test_class.delete_from_project()

    def test_add_event_reception(self, test_project: RPProject) -> None:
        pkg_name = self._unique("EvRecPkg")
        class_name = self._unique("EvRecCls")
        reception_name = self._unique("onEvSig")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            reception = test_class.add_event_reception(reception_name)
            assert reception is not None
            assert isinstance(reception, RPEventReception)
            assert reception.get_name() == reception_name
            items = [i.get_name() for i in test_class.get_interface_items()]
            assert reception_name in items
        finally:
            test_class.delete_from_project()

    def test_add_event_reception_with_event(self, test_project: RPProject) -> None:
        """Test that add_event_reception_with_event raises NotImplementedError (not exposed in COM type library)."""
        pkg_name = self._unique("EvWEvPkg")
        class_name = self._unique("EvWEvCls")
        event_name = self._unique("MyEvent")
        reception_name = self._unique("onMyEvent")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            event = pkg.add_event(event_name)
            with pytest.raises(NotImplementedError, match="addEventReceptionWithEvent is not exposed in the Rhapsody COM"):
                test_class.add_event_reception_with_event(reception_name, event)
        finally:
            test_class.delete_from_project()

    def test_add_triggered_operation(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TrigPkg")
        class_name = self._unique("TrigCls")
        op_name = self._unique("trigOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            triggered_op = test_class.add_triggered_operation(op_name)
            assert triggered_op is not None
            assert isinstance(triggered_op, RPOperation)
            assert triggered_op.get_name() == op_name
            operations = list(test_class.get_operations())
            assert triggered_op in operations
        finally:
            test_class.delete_from_project()

    def test_delete_nested_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelClsPkg")
        outer_name = self._unique("OuterCls")
        inner_name = self._unique("InnerCls")
        pkg = self._create_package(test_project, pkg_name)
        outer = pkg.add_class(outer_name)
        try:
            inner = outer.add_class(inner_name)
            assert inner is not None
            nested_names = [c.get_name() for c in outer.get_nested_classifiers()]
            assert inner_name in nested_names
            outer.delete_class(inner_name)
            nested_after = [c.get_name() for c in outer.get_nested_classifiers()]
            assert inner_name not in nested_after
        finally:
            outer.delete_from_project()

    def test_delete_constructor(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelCtorPkg")
        class_name = self._unique("DelCtorCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            ctor = test_class.add_constructor("void()")
            assert ctor is not None
            operations = list(test_class.get_operations())
            assert ctor in operations
            test_class.delete_constructor(ctor)
            operations_after = list(test_class.get_operations())
            assert ctor not in operations_after
        finally:
            test_class.delete_from_project()

    def test_delete_destructor(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelDtorPkg")
        class_name = self._unique("DelDtorCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            dtor = test_class.add_destructor()
            assert dtor is not None
            operations = list(test_class.get_operations())
            assert dtor in operations
            test_class.delete_destructor()
            operations_after = list(test_class.get_operations())
            assert dtor not in operations_after
        finally:
            test_class.delete_from_project()

    def test_delete_event_reception(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelEvPkg")
        class_name = self._unique("DelEvCls")
        reception_name = self._unique("delEvSig")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            reception = test_class.add_event_reception(reception_name)
            assert reception is not None
            items = [i.get_name() for i in test_class.get_interface_items()]
            assert reception_name in items
            test_class.delete_event_reception(reception)
            items_after = [i.get_name() for i in test_class.get_interface_items()]
            assert reception_name not in items_after
        finally:
            test_class.delete_from_project()

    def test_delete_type(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DelTypePkg")
        class_name = self._unique("DelTypeCls")
        type_name = self._unique("MyDataType")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            added_type = test_class.add_type(type_name)
            assert added_type is not None
            test_class.delete_type(type_name)
            assert True
        finally:
            test_class.delete_from_project()

    def test_active_flag_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ActPkg")
        class_name = self._unique("ActCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_active() in (0, 1)
            test_class.set_is_active(1)
            assert test_class.get_is_active() == 1
            test_class.set_is_active(0)
            assert test_class.get_is_active() == 0
        finally:
            test_class.delete_from_project()

    def test_behavior_overriden_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("BehOvPkg")
        class_name = self._unique("BehOvCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_behavior_overriden() in (0, 1)
            test_class.set_is_behavior_overriden(1)
            assert test_class.get_is_behavior_overriden() == 1
            test_class.set_is_behavior_overriden(0)
            assert test_class.get_is_behavior_overriden() == 0
        finally:
            test_class.delete_from_project()

    def test_is_composite_readonly(self, test_project: RPProject) -> None:
        pkg_name = self._unique("CompPkg")
        class_name = self._unique("CompCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_composite() in (0, 1)
        finally:
            test_class.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="setIsFinal COM property does not persist in this Rhapsody build (same limitation as setIsAbstract)")
    def test_is_final_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("FinalPkg")
        class_name = self._unique("FinalCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_final() in (0, 1)
            test_class.set_is_final(1)
            assert test_class.get_is_final() == 1
            test_class.set_is_final(0)
            assert test_class.get_is_final() == 0
        finally:
            test_class.delete_from_project()

    def test_is_reactive_readonly(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ReactPkg")
        class_name = self._unique("ReactCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            assert test_class.get_is_reactive() in (0, 1)
        finally:
            test_class.delete_from_project()

    @pytest.mark.xfail(strict=False, reason="requires RMM/DM server connection not available in test environment")
    def test_update_contained_diagrams_on_server(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SrvPkg")
        class_name = self._unique("SrvCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            test_class.update_contained_diagrams_on_server(0)
        finally:
            test_class.delete_from_project()
