"""Tests for CLI dispatcher and command routing - PanGu style architecture."""

import pytest

from rhapsody_cli.commands.element_command import ElementCommand
from rhapsody_cli.commands.io_command import IOCommand
from rhapsody_cli.commands.project_command import ProjectCommand


class TestElementCommandParsing:
    """Test ElementCommand argument parsing."""

    def test_element_add_parsing(self) -> None:
        """Test element add command parsing."""
        cmd = ElementCommand(["add", "--type", "class", "--name", "TestClass"])
        assert cmd._subcommand == "add"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.type == "class"
        assert cmd._parsed_args.name == "TestClass"

    def test_element_query_parsing(self) -> None:
        """Test element query command parsing."""
        cmd = ElementCommand(["query"])
        assert cmd._subcommand == "query"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.pattern is None

    def test_element_query_with_pattern(self) -> None:
        """Test element query with search pattern."""
        cmd = ElementCommand(["query", "MyClass"])
        assert cmd._subcommand == "query"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.pattern == "MyClass"

    def test_element_delete_parsing(self) -> None:
        """Test element delete command parsing."""
        cmd = ElementCommand(["delete", "Root::MyClass"])
        assert cmd._subcommand == "delete"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.path == "Root::MyClass"

    def test_element_view_parsing(self) -> None:
        """Test element view command parsing."""
        cmd = ElementCommand(["view", "--path", "Root::MyClass"])
        assert cmd._subcommand == "view"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.path == "Root::MyClass"

    def test_element_missing_subcommand(self) -> None:
        """Test element with no subcommand exits."""
        with pytest.raises(SystemExit):
            ElementCommand([])

    def test_element_add_missing_args(self) -> None:
        """Test element add without required args exits."""
        with pytest.raises(SystemExit):
            ElementCommand(["add", "--type", "class"])


class TestIOCommandParsing:
    """Test IOCommand argument parsing."""

    def test_io_import_parsing(self) -> None:
        """Test io import command parsing."""
        cmd = IOCommand(["import", "model.xmi"])
        assert cmd._subcommand == "import"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.source == "model.xmi"
        assert cmd._parsed_args.target == "Root"

    def test_io_import_with_target(self) -> None:
        """Test io import with custom target."""
        cmd = IOCommand(["import", "model.xmi", "--target", "MyPackage"])
        assert cmd._subcommand == "import"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.source == "model.xmi"
        assert cmd._parsed_args.target == "MyPackage"

    def test_io_export_parsing(self) -> None:
        """Test io export command parsing."""
        cmd = IOCommand(["export", "output.xmi"])
        assert cmd._subcommand == "export"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.output == "output.xmi"
        assert cmd._parsed_args.format == "xmi"

    def test_io_export_with_format(self) -> None:
        """Test io export with custom format."""
        cmd = IOCommand(["export", "output.json", "--format", "json"])
        assert cmd._subcommand == "export"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.output == "output.json"
        assert cmd._parsed_args.format == "json"

    def test_io_missing_subcommand(self) -> None:
        """Test io with no subcommand exits."""
        with pytest.raises(SystemExit):
            IOCommand([])

    def test_io_import_missing_source(self) -> None:
        """Test io import without source exits."""
        with pytest.raises(SystemExit):
            IOCommand(["import"])


class TestProjectCommandParsing:
    """Test ProjectCommand argument parsing."""

    def test_project_open_parsing(self) -> None:
        """Test project open command parsing."""
        cmd = ProjectCommand(["open", "/path/to/project.rpy"])
        assert cmd._subcommand == "open"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.project_path == "/path/to/project.rpy"

    def test_project_list_parsing(self) -> None:
        """Test project list command parsing."""
        cmd = ProjectCommand(["list"])
        assert cmd._subcommand == "list"

    def test_project_close_parsing(self) -> None:
        """Test project close command parsing."""
        cmd = ProjectCommand(["close"])
        assert cmd._subcommand == "close"

    def test_project_new_parsing(self) -> None:
        """Test project new command parsing."""
        cmd = ProjectCommand(["new", "/location", "MyProject"])
        assert cmd._subcommand == "new"
        assert cmd._parsed_args is not None
        assert cmd._parsed_args.project_location == "/location"
        assert cmd._parsed_args.project_name == "MyProject"

    def test_project_missing_subcommand(self) -> None:
        """Test project with no subcommand exits."""
        with pytest.raises(SystemExit):
            ProjectCommand([])
