"""Tests for CLI dispatcher and command routing."""

from __future__ import annotations

import pytest

from rhapsody_cli.cli.cli import create_parser


class TestCliParser:
    """Test CLI argument parser."""
    
    def test_parser_help_works(self) -> None:
        """Test that help is available."""
        parser = create_parser()
        assert parser is not None
    
    def test_element_add_parsing(self) -> None:
        """Test element add command parsing."""
        parser = create_parser()
        args = parser.parse_args(["element", "add", "--type", "class", "--name", "TestClass"])
        assert args.command == "element"
        assert args.element_subcommand == "add"
        assert args.type == "class"
        assert args.name == "TestClass"
    
    def test_element_query_parsing(self) -> None:
        """Test element query command parsing."""
        parser = create_parser()
        args = parser.parse_args(["element", "query"])
        assert args.command == "element"
        assert args.element_subcommand == "query"
        assert args.pattern is None
    
    def test_element_query_with_pattern(self) -> None:
        """Test element query with search pattern."""
        parser = create_parser()
        args = parser.parse_args(["element", "query", "MyClass"])
        assert args.pattern == "MyClass"
    
    def test_element_delete_parsing(self) -> None:
        """Test element delete command parsing."""
        parser = create_parser()
        args = parser.parse_args(["element", "delete", "Root::MyClass"])
        assert args.command == "element"
        assert args.element_subcommand == "delete"
        assert args.path == "Root::MyClass"
    
    def test_element_view_parsing(self) -> None:
        """Test element view command parsing."""
        parser = create_parser()
        args = parser.parse_args(["element", "view", "--path", "Root::MyClass"])
        assert args.command == "element"
        assert args.element_subcommand == "view"
        assert args.path == "Root::MyClass"
    
    def test_verbose_flag_on_element(self) -> None:
        """Test --verbose flag on element group."""
        parser = create_parser()
        args = parser.parse_args(["element", "--verbose", "query"])
        assert args.verbose is True
        assert args.command == "element"
    
    def test_verbose_short_flag_on_element(self) -> None:
        """Test -v short flag on element group."""
        parser = create_parser()
        args = parser.parse_args(["element", "-v", "query"])
        assert args.verbose is True
    
    def test_io_import_parsing(self) -> None:
        """Test io import command parsing."""
        parser = create_parser()
        args = parser.parse_args(["io", "import", "model.xmi"])
        assert args.command == "io"
        assert args.io_subcommand == "import"
        assert args.source == "model.xmi"
        assert args.target == "Root"
    
    def test_io_import_with_target(self) -> None:
        """Test io import with custom target."""
        parser = create_parser()
        args = parser.parse_args(["io", "import", "model.xmi", "--target", "MyPackage"])
        assert args.target == "MyPackage"
    
    def test_io_export_parsing(self) -> None:
        """Test io export command parsing."""
        parser = create_parser()
        args = parser.parse_args(["io", "export", "output.xmi"])
        assert args.command == "io"
        assert args.io_subcommand == "export"
        assert args.output == "output.xmi"
        assert args.format == "xmi"
    
    def test_io_export_with_format(self) -> None:
        """Test io export with custom format."""
        parser = create_parser()
        args = parser.parse_args(["io", "export", "output.json", "--format", "json"])
        assert args.format == "json"
    
    def test_output_format_default(self) -> None:
        """Test --output format defaults to table."""
        parser = create_parser()
        args = parser.parse_args(["element", "query"])
        assert args.output == "table"
    
    def test_output_format_json(self) -> None:
        """Test --output format can be set to json."""
        parser = create_parser()
        args = parser.parse_args(["--output", "json", "element", "query"])
        assert args.output == "json"
    
    def test_output_format_csv(self) -> None:
        """Test --output format can be set to csv."""
        parser = create_parser()
        args = parser.parse_args(["--output", "csv", "element", "query"])
        assert args.output == "csv"
