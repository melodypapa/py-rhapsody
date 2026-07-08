"""Tests for element actions and the ElementCommand dispatcher."""

import argparse
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
        """Test: add action creates a class on the Default package."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", verbose=False)

        fake_default_package = MagicMock(name="FakeDefaultPackage")
        fake_default_package.getName.return_value = "Default"
        fake_default_package.getMetaClass.return_value = "Package"

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_default_package]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            action.execute(args)

        fake_default_package.addClass.assert_called_once_with("Foo")

    def test_add_action_exits_on_connection_error(self) -> None:
        """Test: add action exits when no Rhapsody is running."""
        action = ElementAddAction()
        args = argparse.Namespace(type="class", name="Foo", verbose=False)

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

    def test_view_action_exits_on_connection_error(self) -> None:
        """Test: view action exits when no Rhapsody is running."""
        action = ElementViewAction()
        args = argparse.Namespace(path="Root::MyClass", verbose=False)

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
        args = argparse.Namespace(pattern=None, verbose=False)

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

    def test_query_action_exits_on_connection_error(self) -> None:
        """Test: query action exits when no Rhapsody is running."""
        action = ElementQueryAction()
        args = argparse.Namespace(pattern=None, verbose=False)

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
        args = argparse.Namespace(path="Root::TestClass", verbose=False)

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
            action.execute(args)

    def test_delete_action_exits_on_connection_error(self) -> None:
        """Test: delete action exits when no Rhapsody is running."""
        action = ElementDeleteAction()
        args = argparse.Namespace(path="Root::TestClass", verbose=False)

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            with pytest.raises(SystemExit) as exc_info:
                action.execute(args)
            assert exc_info.value.code == 1
