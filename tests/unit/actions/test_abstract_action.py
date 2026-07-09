"""Tests for AbstractAction and its subclasses' shared helpers."""

import argparse
from typing import Any, List, Optional
from unittest.mock import Mock

import pytest

from rhapsody_cli.actions.abstract_action import (
    AbstractAction,
    ElementManagementAction,
    RhapsodyContextAction,
)
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.path_resolver import PathResolver, PathResolverError
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractActionAddVerboseArgument:
    """Test the shared --verbose/-v flag registration."""

    def test_add_verbose_argument_registers_verbose_flag(self) -> None:
        """--verbose and -v should both parse as verbose=True."""
        parser = argparse.ArgumentParser()
        AbstractAction.add_verbose_argument(parser)

        args_long = parser.parse_args(["--verbose"])
        args_short = parser.parse_args(["-v"])

        assert args_long.verbose is True
        assert args_short.verbose is True

    def test_add_verbose_argument_defaults_to_false(self) -> None:
        """verbose should default to False when the flag is omitted."""
        parser = argparse.ArgumentParser()
        AbstractAction.add_verbose_argument(parser)

        args = parser.parse_args([])

        assert args.verbose is False


class TestElementManagementActionAddPathArgument:
    """Test the shared --path argument registration helper."""

    def test_add_path_argument_default_none_optional(self) -> None:
        """Optional --path should default to None when omitted."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_path_argument(parser)

        args = parser.parse_args([])

        assert args.path is None

    def test_add_path_argument_required_raises_without_flag(self) -> None:
        """Required --path should make argparse exit if the flag is missing."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_path_argument(parser, required=True)

        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_add_path_argument_accepts_separator_path(self) -> None:
        """--path should accept paths with '/' separators."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_path_argument(parser)

        args = parser.parse_args(["--path", "pkg/sub/Class"])

        assert args.path == "pkg/sub/Class"

    def test_add_path_argument_help_text_mentions_separators(self) -> None:
        """The default help text should mention path separators for discoverability."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_path_argument(parser)

        help_text = parser.format_help()

        assert "/" in help_text


class TestElementManagementActionAddRecursiveArgument:
    """Test the shared --recursive argument registration helper."""

    def test_add_recursive_argument_defaults_false(self) -> None:
        """--recursive should default to False when omitted."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_recursive_argument(parser, help_text="any help")

        args = parser.parse_args([])

        assert args.recursive is False

    def test_add_recursive_argument_sets_true_when_passed(self) -> None:
        """--recursive should parse as True when the flag is supplied."""
        parser = argparse.ArgumentParser()
        ElementManagementAction.add_recursive_argument(parser, help_text="any help")

        args = parser.parse_args(["--recursive"])

        assert args.recursive is True


class _FakeElementAction(ElementManagementAction):
    """Minimal concrete subclass for testing base-class helpers in isolation."""

    def init_arguments(self, sub_parser: Any) -> None:  # pragma: no cover - not exercised
        """Unused: test scaffold only."""

    def execute(self, args: argparse.Namespace) -> None:  # pragma: no cover - not exercised
        """Unused: test scaffold only."""


class TestElementManagementActionGetActiveRoot:
    """Test the _get_active_root() helper."""

    def test_get_active_root_returns_root_of_active_project(self) -> None:
        """_get_active_root() should return whatever project.getRoot() yields."""
        action = _FakeElementAction(command_id="fake")
        fake_root = Mock(name="root")
        fake_project = Mock(name="project")
        fake_project.getRoot.return_value = fake_root
        # Bypass the real _get_active_project (which hits RhapsodyContext).
        action._get_active_project = lambda: fake_project  # type: ignore[method-assign]

        result = action._get_active_root()

        assert result is fake_root
        fake_project.getRoot.assert_called_once_with()


class _FakeElement:
    """Minimal stand-in for a wrapped model element with a name and children."""

    def __init__(self, name: str, children: Optional[List["_FakeElement"]] = None) -> None:
        self._name = name
        self._children = children or []

    def getName(self) -> str:
        return self._name

    def getNestedElements(self) -> List["_FakeElement"]:
        return self._children


def _make_root_with(*children: _FakeElement) -> _FakeElement:
    """Build a root element with the given named children."""
    return _FakeElement("Root", list(children))


class TestElementManagementActionResolveContainer:
    """Test _resolve_container_or_element() in container mode."""

    def test_resolve_container_returns_container_for_valid_path(self) -> None:
        """Container mode should walk the path and return the matching child."""
        action = _FakeElementAction(command_id="fake")
        pkg = _FakeElement("pkg")
        root = _make_root_with(pkg)

        result = action._resolve_container_or_element(root, "pkg", resolve_element=False)

        assert result is pkg

    def test_resolve_container_returns_root_for_empty_path(self) -> None:
        """Container mode with empty/None path should return the root itself."""
        action = _FakeElementAction(command_id="fake")
        root = _make_root_with()

        result = action._resolve_container_or_element(root, None, resolve_element=False)

        assert result is root

    def test_resolve_container_raises_cli_error_on_path_error(self) -> None:
        """PathResolverError should be re-raised as CliExecutionError."""
        action = _FakeElementAction(command_id="fake")
        root = _make_root_with()

        with pytest.raises(CliExecutionError) as exc_info:
            action._resolve_container_or_element(root, "missing", resolve_element=False)

        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, PathResolverError)

    def test_resolve_container_raises_cli_error_on_unexpected_exception(self) -> None:
        """Non-PathResolverError exceptions should also surface as CliExecutionError."""
        action = _FakeElementAction(command_id="fake")
        root = _make_root_with()
        original = PathResolver.resolve_container

        def boom(root_arg: object, path: Optional[str]) -> _FakeElement:
            raise RuntimeError("boom")

        PathResolver.resolve_container = staticmethod(boom)  # type: ignore[method-assign]
        try:
            with pytest.raises(CliExecutionError):
                action._resolve_container_or_element(root, "pkg", resolve_element=False)
        finally:
            PathResolver.resolve_container = staticmethod(original)  # type: ignore[method-assign]


class TestElementManagementActionResolveElement:
    """Test _resolve_container_or_element() in element mode."""

    def test_resolve_element_returns_element_for_valid_path(self) -> None:
        """Element mode should walk the path and return the matching child."""
        action = _FakeElementAction(command_id="fake")
        cls = _FakeElement("MyClass")
        pkg = _FakeElement("pkg", [cls])
        root = _make_root_with(pkg)

        result = action._resolve_container_or_element(root, "pkg/MyClass", resolve_element=True)

        assert result is cls

    def test_resolve_element_raises_cli_error_on_path_error(self) -> None:
        """PathResolverError should be re-raised as CliExecutionError."""
        action = _FakeElementAction(command_id="fake")
        root = _make_root_with()

        with pytest.raises(CliExecutionError) as exc_info:
            action._resolve_container_or_element(root, "missing", resolve_element=True)

        assert isinstance(exc_info.value.__cause__, PathResolverError)

    def test_resolve_element_raises_cli_error_on_unexpected_exception(self) -> None:
        """Non-PathResolverError exceptions should also surface as CliExecutionError."""
        action = _FakeElementAction(command_id="fake")
        root = _make_root_with()
        original = PathResolver.resolve_element

        def boom(root_arg: object, path: str) -> _FakeElement:
            raise RuntimeError("boom")

        PathResolver.resolve_element = staticmethod(boom)  # type: ignore[method-assign]
        try:
            with pytest.raises(CliExecutionError):
                action._resolve_container_or_element(root, "pkg", resolve_element=True)
        finally:
            PathResolver.resolve_element = staticmethod(original)  # type: ignore[method-assign]


class _FakeContextAction(RhapsodyContextAction):
    """Minimal concrete subclass of RhapsodyContextAction for testing the _context property."""

    def init_arguments(self, sub_parser: Any) -> None:  # pragma: no cover - not exercised
        """Unused: test scaffold only."""

    def execute(self, args: argparse.Namespace) -> None:  # pragma: no cover - not exercised
        """Unused: test scaffold only."""


class TestRhapsodyContextActionContextProperty:
    """Test the _context lazily-cached property on RhapsodyContextAction."""

    def test_context_property_returns_rhapsody_context_instance(self) -> None:
        """_context should return a RhapsodyContext instance."""
        action = _FakeContextAction(command_id="fake")

        ctx = action._context

        assert isinstance(ctx, RhapsodyContext)

    def test_context_property_caches_instance_per_action(self) -> None:
        """Repeated access should return the same cached instance."""
        action = _FakeContextAction(command_id="fake")

        first = action._context
        second = action._context

        assert first is second


class TestRhapsodyContextActionPrintFormattedOutput:
    """Test the _print_formatted_output() helper."""

    def test_print_formatted_output_json_when_context_format_is_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        """When output_format is 'json', the helper should render data as JSON to stdout."""
        action = _FakeContextAction(command_id="fake")
        # Force the cached context into JSON mode without touching real COM.
        action._cached_context = Mock(spec=RhapsodyContext)
        action._cached_context.output_format = "json"  # type: ignore[attr-defined]

        action._print_formatted_output(data={"a": 1}, headers=["a"], table_rows=[[1]])

        captured = capsys.readouterr()
        assert '"a"' in captured.out
        assert "1" in captured.out

    def test_print_formatted_output_table_by_default(self, capsys: pytest.CaptureFixture[str]) -> None:
        """By default (non-json), the helper should render a table to stdout."""
        action = _FakeContextAction(command_id="fake")
        action._cached_context = Mock(spec=RhapsodyContext)
        action._cached_context.output_format = "table"  # type: ignore[attr-defined]

        action._print_formatted_output(data={}, headers=["Name"], table_rows=[["Foo"]])

        captured = capsys.readouterr()
        assert "Foo" in captured.out
        assert "Name" in captured.out

    def test_print_formatted_output_force_table_skips_json_branch(self, capsys: pytest.CaptureFixture[str]) -> None:
        """force_table=True should keep table output even when format is 'json'."""
        action = _FakeContextAction(command_id="fake")
        action._cached_context = Mock(spec=RhapsodyContext)
        action._cached_context.output_format = "json"  # type: ignore[attr-defined]

        action._print_formatted_output(data={"a": 1}, headers=["Name"], table_rows=[["Foo"]], force_table=True)

        captured = capsys.readouterr()
        assert "Foo" in captured.out
        # JSON serialization of {"a": 1} would not include the literal text "Name",
        # so the presence of "Name" signals the table branch was taken.
        assert "Name" in captured.out
