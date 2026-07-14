import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPOperationIntegration:
    """Integration tests for RPOperation with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    @pytest.mark.xfail(
        reason="Rhapsody2.Application.1 does not expose the 'setIsStatic' COM method; " "RPOperation.set_is_static raises AttributeError. TODO: persist via metatype property system.",
        strict=False,
    )
    def test_static_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("StatPkg")
        class_name = self._unique("StatCls")
        op_name = self._unique("staticOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_static() is False
            op.set_is_static(1)
            assert op.get_is_static() is True
            op.set_is_static(0)
            assert op.get_is_static() is False
        finally:
            test_class.delete_from_project()

    @pytest.mark.xfail(
        reason="Rhapsody2.Application.1 does not expose the 'setIsVirtual' COM method; " "RPOperation.set_is_virtual raises AttributeError. TODO: persist via metatype property system.",
        strict=False,
    )
    def test_virtual_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("VirtPkg")
        class_name = self._unique("VirtCls")
        op_name = self._unique("virtualOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_virtual() is False
            op.set_is_virtual(1)
            assert op.get_is_virtual() is True
            op.set_is_virtual(0)
            assert op.get_is_virtual() is False
        finally:
            test_class.delete_from_project()

    @pytest.mark.xfail(
        reason="Rhapsody2.Application.1 does not expose the 'setIsAbstract' COM method; " "RPOperation.set_is_abstract raises AttributeError. TODO: persist via metatype property system.",
        strict=False,
    )
    def test_abstract_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AbsOpPkg")
        class_name = self._unique("AbsOpCls")
        op_name = self._unique("abstractOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_abstract() is False
            op.set_is_abstract(1)
            assert op.get_is_abstract() is True
            op.set_is_abstract(0)
            assert op.get_is_abstract() is False
        finally:
            test_class.delete_from_project()

    def test_return_type_declaration(self, test_project: RPProject) -> None:
        pkg_name = self._unique("RetPkg")
        class_name = self._unique("RetCls")
        op_name = self._unique("getValue")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            op.set_return_type_declaration("int")
            assert op.get_return_type_declaration() == "int"
        finally:
            test_class.delete_from_project()

    def test_get_body(self, test_project: RPProject) -> None:
        pkg_name = self._unique("BodyPkg")
        class_name = self._unique("BodyCls")
        op_name = self._unique("doSomething")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            body = op.get_body()
            assert isinstance(body, str)
        finally:
            test_class.delete_from_project()
