"""Tests for element command classes."""

from __future__ import annotations

from py_rhapsody.cli.commands.element import ElementCommandGroup


class TestElementCommandGroup:
    """Tests for ElementCommandGroup."""

    def test_element_group_has_add_command(self) -> None:
        """Test: ElementCommandGroup includes add command."""
        group = ElementCommandGroup()
        assert "add" in group.commands
        assert group.commands["add"].name == "add"

    def test_element_group_has_view_command(self) -> None:
        """Test: ElementCommandGroup includes view command."""
        group = ElementCommandGroup()
        assert "view" in group.commands
        assert group.commands["view"].name == "view"

    def test_element_group_has_query_command(self) -> None:
        """Test: ElementCommandGroup includes query command."""
        group = ElementCommandGroup()
        assert "query" in group.commands
        assert group.commands["query"].name == "query"

    def test_element_group_name_is_element(self) -> None:
        """Test: ElementCommandGroup name is 'element'."""
        group = ElementCommandGroup()
        assert group.name == "element"

    def test_element_group_has_help(self) -> None:
        """Test: ElementCommandGroup has help text."""
        group = ElementCommandGroup()
        assert group.help is not None
        assert "element" in group.help.lower()


class TestAddElementCommand:
    """Tests for AddElementCommand."""

    def test_add_command_name_is_add(self) -> None:
        """Test: add command name is 'add'."""
        group = ElementCommandGroup()
        add_cmd = group.commands["add"]
        assert add_cmd.name == "add"

    def test_add_command_has_help(self) -> None:
        """Test: add command has help text."""
        group = ElementCommandGroup()
        add_cmd = group.commands["add"]
        assert add_cmd.help is not None
        assert "add" in add_cmd.help.lower()


class TestViewElementCommand:
    """Tests for ViewElementCommand."""

    def test_view_command_name_is_view(self) -> None:
        """Test: view command name is 'view'."""
        group = ElementCommandGroup()
        view_cmd = group.commands["view"]
        assert view_cmd.name == "view"

    def test_view_command_has_help(self) -> None:
        """Test: view command has help text."""
        group = ElementCommandGroup()
        view_cmd = group.commands["view"]
        assert view_cmd.help is not None
        assert "view" in view_cmd.help.lower()


class TestQueryElementCommand:
    """Tests for QueryElementCommand."""

    def test_query_command_name_is_query(self) -> None:
        """Test: query command name is 'query'."""
        group = ElementCommandGroup()
        query_cmd = group.commands["query"]
        assert query_cmd.name == "query"

    def test_query_command_has_help(self) -> None:
        """Test: query command has help text."""
        group = ElementCommandGroup()
        query_cmd = group.commands["query"]
        assert query_cmd.help is not None
        assert "query" in query_cmd.help.lower()
