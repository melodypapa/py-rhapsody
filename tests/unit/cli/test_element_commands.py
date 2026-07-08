"""Tests for element command classes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.cli.commands.element import (
    AddElementCommand,
    DeleteElementCommand,
    QueryElementCommand,
    ViewElementCommand,
)
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.exceptions import RhapsodyConnectionError


class TestAddElementCommand:
    """Tests for AddElementCommand."""

    def test_add_command_execute_signature(self) -> None:
        """Test: AddElementCommand has execute method."""
        cmd = AddElementCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_add_command_creates_class_on_active_project(self) -> None:
        """Test: add command creates a class on the Default package."""
        cmd = AddElementCommand(args=[])

        # Create a mock Default package
        fake_default_package = MagicMock(name="FakeDefaultPackage")
        fake_default_package.getName.return_value = "Default"
        fake_default_package.getMetaClass.return_value = "Package"

        # Create a mock root with nested elements
        fake_root = MagicMock(name="FakeRoot")
        fake_nested_elements = [fake_default_package]
        fake_root.getNestedElements.return_value = fake_nested_elements

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            # Should not raise
            cmd.execute(element_type="class", name="Foo")

        fake_default_package.addClass.assert_called_once_with("Foo")

    def test_add_command_exits_on_connection_error(self) -> None:
        """Test: add command exits when no Rhapsody is running."""
        cmd = AddElementCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(element_type="class", name="Foo")
            assert exc_info.value.code == 1


class TestViewElementCommand:
    """Tests for ViewElementCommand."""

    def test_view_command_execute_signature(self) -> None:
        """Test: ViewElementCommand has execute method."""
        cmd = ViewElementCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_view_command_exits_on_connection_error(self) -> None:
        """Test: view command exits when no Rhapsody is running."""
        cmd = ViewElementCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(path="Root::MyClass")
            assert exc_info.value.code == 1


class TestQueryElementCommand:
    """Tests for QueryElementCommand."""

    def test_query_command_execute_signature(self) -> None:
        """Test: QueryElementCommand has execute method."""
        cmd = QueryElementCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_query_command_lists_elements_from_active_project(self) -> None:
        """Test: query command lists elements from the active project's root."""
        cmd = QueryElementCommand(args=[])

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
            # Should not raise
            cmd.execute(pattern=None)

    def test_query_command_exits_on_connection_error(self) -> None:
        """Test: query command exits when no Rhapsody is running."""
        cmd = QueryElementCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(pattern=None)
            assert exc_info.value.code == 1


class TestDeleteElementCommand:
    """Tests for DeleteElementCommand."""

    def test_delete_command_execute_signature(self) -> None:
        """Test: DeleteElementCommand has execute method."""
        cmd = DeleteElementCommand(args=[])
        assert hasattr(cmd, "execute")
        assert callable(cmd.execute)

    def test_delete_command_deletes_class_from_active_project(self) -> None:
        """Test: delete command removes a class from the active project's root."""
        cmd = DeleteElementCommand(args=[])

        fake_element_com = MagicMock(name="FakeElementCOM")
        fake_element_to_delete = MagicMock(name="FakeElement")
        fake_element_to_delete.getMetaClass.return_value = "Class"
        fake_element_to_delete.getName.return_value = "TestClass"
        fake_element_to_delete._com = fake_element_com

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_element_to_delete]
        fake_root._com = MagicMock(name="FakeRootCOM")

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            # Should not raise
            cmd.execute(path="Root::TestClass")

    def test_delete_command_exits_on_connection_error(self) -> None:
        """Test: delete command exits when no Rhapsody is running."""
        cmd = DeleteElementCommand(args=[])

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                cmd.execute(path="Root::TestClass")
            assert exc_info.value.code == 1
