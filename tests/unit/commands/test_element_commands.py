"""Tests for element actions and the ElementCommand dispatcher."""

import argparse
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.element_action import (
    ElementAddAction,
    ElementDeleteAction,
    ElementQueryAction,
    ElementViewAction,
)
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.commands.element_command import ElementCommand
from rhapsody_cli.exceptions import RhapsodyConnectionError

if TYPE_CHECKING:
    from pathlib import Path


class TestElementCommandDispatch:
    """Tests for the ElementCommand group dispatcher."""

    def test_add_subcommand_dispatches_to_add_action(self) -> None:
        """Test: 'add' subcommand is parsed and dispatched correctly."""
        cmd = ElementCommand(["add", "--type", "class", "--name", "Foo"])
        assert cmd._subcommand == "add"

    def test_missing_subcommand_exits(self) -> None:
        """Test: no subcommand causes SystemExit."""
        with pytest.raises(SystemExit):
            ElementCommand([])


class TestElementAddAction:
    """Tests for ElementAddAction."""

    def test_add_action_creates_class_on_active_project(self) -> None:
        """Test: add action creates a class directly on the project root when no --path is given."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", bulk=None, path=None, verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_root.addClass.assert_called_once_with("Foo")

    def test_add_action_creates_class_in_nested_path(self) -> None:
        """Test: add action navigates a multi-level --path before creating the element."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", bulk=None, path="pkg/subpkg", verbose=False)

        fake_subpkg = MagicMock(name="FakeSubPkg")
        fake_subpkg.getName.return_value = "subpkg"
        fake_subpkg.getNestedElements.return_value = []

        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getNestedElements.return_value = [fake_subpkg]

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_subpkg.addClass.assert_called_once_with("Foo")

    def test_add_action_reports_path_not_found(self) -> None:
        """Test: add action exits with an error when --path cannot be navigated."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", bulk=None, path="missing", verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1

    def test_add_action_requires_name_or_bulk(self) -> None:
        """Test: add action exits with an error when neither --name nor --bulk is given."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name=None, bulk=None, path=None, verbose=False)

        with pytest.raises(SystemExit) as exc_info:
            action.execute(args)
        assert exc_info.value.code == 1

    def test_add_action_rejects_both_name_and_bulk(self) -> None:
        """Test: add action exits with an error when both --name and --bulk are given."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", bulk="items.txt", path=None, verbose=False)

        with pytest.raises(SystemExit) as exc_info:
            action.execute(args)
        assert exc_info.value.code == 1

    def test_add_action_bulk_creates_multiple_items(self, tmp_path: "Path") -> None:
        """Test: add action with --bulk creates every non-empty line as an element."""
        items_file = tmp_path / "items.txt"
        items_file.write_text("Class1\nClass2\n\nClass3\n")

        action = ElementAddAction()
        args = argparse.Namespace(type="class", name=None, bulk=str(items_file), path=None, verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        assert fake_root.addClass.call_count == 3
        fake_root.addClass.assert_any_call("Class1")
        fake_root.addClass.assert_any_call("Class2")
        fake_root.addClass.assert_any_call("Class3")

    def test_add_action_bulk_reports_partial_failures(self, tmp_path: "Path") -> None:
        """Test: add action with --bulk continues past per-item failures and reports them."""
        items_file = tmp_path / "items.txt"
        items_file.write_text("Class1\nClass2\n")

        action = ElementAddAction()
        args = argparse.Namespace(type="class", name=None, bulk=str(items_file), path=None, verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []
        fake_root.addClass.side_effect = [None, RuntimeError("duplicate name")]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        assert fake_root.addClass.call_count == 2

    def test_add_action_exits_on_connection_error(self) -> None:
        """Test: add action exits when no Rhapsody is running."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", bulk=None, path=None, verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1


class TestElementViewAction:
    """Tests for ElementViewAction."""

    def test_view_action_displays_element_details(self) -> None:
        """Test: view action resolves the path and prints element details."""
        action = ElementViewAction()
        args = argparse.Namespace(path="pkg/MyClass", verbose=False)

        fake_class = MagicMock(name="FakeClass")
        fake_class.getName.return_value = "MyClass"
        fake_class.getMetaClass.return_value = "Class"

        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getNestedElements.return_value = [fake_class]

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

    def test_view_action_reports_path_not_found(self) -> None:
        """Test: view action exits with an error when --path cannot be navigated."""
        action = ElementViewAction()
        args = argparse.Namespace(path="missing", verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1

    def test_view_action_exits_on_connection_error(self) -> None:
        """Test: view action exits when no Rhapsody is running."""
        action = ElementViewAction()
        args = argparse.Namespace(path="MyClass", verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1


class TestElementQueryAction:
    """Tests for ElementQueryAction."""

    def test_query_action_lists_elements_from_active_project(self) -> None:
        """Test: query action lists elements from the active project's root."""
        action = ElementQueryAction()
        args = argparse.Namespace(pattern=None, path=None, recursive=False, verbose=False)

        fake_element = MagicMock(name="FakeElement")
        fake_element.getName.return_value = "MyClass"
        fake_element.getMetaClass.return_value = "Class"

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_element]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

    def test_query_action_recursive_includes_nested_elements(self) -> None:
        """Test: query action with --recursive walks into nested packages."""
        action = ElementQueryAction()
        args = argparse.Namespace(pattern=None, path=None, recursive=True, verbose=False)

        fake_nested_class = MagicMock(name="FakeNestedClass")
        fake_nested_class.getName.return_value = "NestedClass"
        fake_nested_class.getMetaClass.return_value = "Class"
        fake_nested_class.getNestedElements.return_value = []

        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getMetaClass.return_value = "Package"
        fake_pkg.getNestedElements.return_value = [fake_nested_class]

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_pkg.getNestedElements.assert_called()
        fake_nested_class.getNestedElements.assert_called()

    def test_query_action_reports_path_not_found(self) -> None:
        """Test: query action exits with an error when --path cannot be navigated."""
        action = ElementQueryAction()
        args = argparse.Namespace(pattern=None, path="missing", recursive=False, verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1

    def test_query_action_exits_on_connection_error(self) -> None:
        """Test: query action exits when no Rhapsody is running."""
        action = ElementQueryAction()
        args = argparse.Namespace(pattern=None, path=None, recursive=False, verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1


class TestElementDeleteAction:
    """Tests for ElementDeleteAction."""

    def test_delete_action_deletes_class_from_active_project(self) -> None:
        """Test: delete action removes a class from the active project's root."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="TestClass", recursive=False, force=False, verbose=False)

        fake_element_com = MagicMock(name="FakeElementCOM")
        fake_element_to_delete = MagicMock(name="FakeElement")
        fake_element_to_delete.getMetaClass.return_value = "Class"
        fake_element_to_delete.getName.return_value = "TestClass"
        fake_element_to_delete._com = fake_element_com

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_element_to_delete]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_element_com.delete.assert_called_once()

    def test_delete_action_reports_path_not_found(self) -> None:
        """Test: delete action exits with an error when the path cannot be navigated."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="Missing", recursive=False, force=False, verbose=False)

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = []

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1

    def test_delete_action_recursive_prompts_and_deletes_with_confirmation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test: delete action with --recursive counts nested elements and deletes after 'y' confirmation."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="pkg", recursive=True, force=False, verbose=False)

        fake_child = MagicMock(name="FakeChild")
        fake_child.getNestedElements.return_value = []

        fake_pkg_com = MagicMock(name="FakePkgCOM")
        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getMetaClass.return_value = "Package"
        fake_pkg.getNestedElements.return_value = [fake_child]
        fake_pkg._com = fake_pkg_com

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        monkeypatch.setattr("builtins.input", lambda _: "y")

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_pkg_com.delete.assert_called_once()

    def test_delete_action_recursive_aborts_without_confirmation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test: delete action with --recursive does not delete if the user declines to confirm."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="pkg", recursive=True, force=False, verbose=False)

        fake_pkg_com = MagicMock(name="FakePkgCOM")
        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getMetaClass.return_value = "Package"
        fake_pkg.getNestedElements.return_value = []
        fake_pkg._com = fake_pkg_com

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        monkeypatch.setattr("builtins.input", lambda _: "n")

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_pkg_com.delete.assert_not_called()

    def test_delete_action_recursive_force_skips_confirmation(self) -> None:
        """Test: delete action with --recursive --force deletes without prompting."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="pkg", recursive=True, force=True, verbose=False)

        fake_pkg_com = MagicMock(name="FakePkgCOM")
        fake_pkg = MagicMock(name="FakePkg")
        fake_pkg.getName.return_value = "pkg"
        fake_pkg.getMetaClass.return_value = "Package"
        fake_pkg.getNestedElements.return_value = []
        fake_pkg._com = fake_pkg_com

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_pkg]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_pkg_com.delete.assert_called_once()

    def test_delete_action_exits_on_connection_error(self) -> None:
        """Test: delete action exits when no Rhapsody is running."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="TestClass", recursive=False, force=False, verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1
