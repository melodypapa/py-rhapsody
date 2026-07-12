"""Tests for PathResolver path parsing and navigation."""

from typing import List, Optional

import pytest

from rhapsody_cli.cli.path_resolver import PathResolver, PathResolverError


class _FakeElement:
    """Minimal stand-in for a wrapped model element with a name and children."""

    def __init__(self, name: str, children: Optional[List["_FakeElement"]] = None) -> None:
        self._name = name
        self._children = children or []

    def get_name(self) -> str:
        return self._name

    def get_nested_elements(self) -> List["_FakeElement"]:
        return self._children


class TestNormalize:
    """Tests for PathResolver.normalize."""

    def test_converts_backslashes_to_forward_slashes(self) -> None:
        assert PathResolver.normalize("pkg\\subpkg") == "pkg/subpkg"

    def test_strips_leading_and_trailing_slashes(self) -> None:
        assert PathResolver.normalize("/pkg/subpkg/") == "pkg/subpkg"

    def test_handles_mixed_separators(self) -> None:
        assert PathResolver.normalize("pkg/subpkg\\class") == "pkg/subpkg/class"


class TestSplitSegments:
    """Tests for PathResolver.split_segments."""

    def test_splits_simple_path(self) -> None:
        assert PathResolver.split_segments("pkg/subpkg/class") == ["pkg", "subpkg", "class"]

    def test_drops_leading_root_alias(self) -> None:
        assert PathResolver.split_segments("Root/pkg/class") == ["pkg", "class"]

    def test_raises_on_empty_path(self) -> None:
        with pytest.raises(PathResolverError, match="cannot be empty"):
            PathResolver.split_segments("")

    def test_raises_on_double_slash(self) -> None:
        with pytest.raises(PathResolverError, match="Invalid path syntax"):
            PathResolver.split_segments("pkg//class")


class TestResolveContainer:
    """Tests for PathResolver.resolve_container."""

    def test_returns_root_when_path_is_none(self) -> None:
        root = _FakeElement("Root")
        assert PathResolver.resolve_container(root, None) is root

    def test_returns_root_when_path_is_empty_string(self) -> None:
        root = _FakeElement("Root")
        assert PathResolver.resolve_container(root, "") is root

    def test_navigates_single_level(self) -> None:
        pkg = _FakeElement("pkg")
        root = _FakeElement("Root", children=[pkg])
        assert PathResolver.resolve_container(root, "pkg") is pkg

    def test_navigates_multiple_levels(self) -> None:
        subpkg = _FakeElement("subpkg")
        pkg = _FakeElement("pkg", children=[subpkg])
        root = _FakeElement("Root", children=[pkg])
        assert PathResolver.resolve_container(root, "pkg/subpkg") is subpkg

    def test_navigates_using_backslash_separators(self) -> None:
        subpkg = _FakeElement("subpkg")
        pkg = _FakeElement("pkg", children=[subpkg])
        root = _FakeElement("Root", children=[pkg])
        assert PathResolver.resolve_container(root, "pkg\\subpkg") is subpkg

    def test_raises_when_segment_not_found(self) -> None:
        pkg = _FakeElement("pkg")
        root = _FakeElement("Root", children=[pkg])
        with pytest.raises(PathResolverError, match="not found: 'unknown'"):
            PathResolver.resolve_container(root, "pkg/unknown")


class TestResolveElement:
    """Tests for PathResolver.resolve_element."""

    def test_navigates_to_leaf_element(self) -> None:
        cls = _FakeElement("MyClass")
        pkg = _FakeElement("pkg", children=[cls])
        root = _FakeElement("Root", children=[pkg])
        assert PathResolver.resolve_element(root, "pkg/MyClass") is cls

    def test_navigates_single_segment_from_root(self) -> None:
        cls = _FakeElement("MyClass")
        root = _FakeElement("Root", children=[cls])
        assert PathResolver.resolve_element(root, "MyClass") is cls

    def test_raises_on_empty_path(self) -> None:
        root = _FakeElement("Root")
        with pytest.raises(PathResolverError, match="cannot be empty"):
            PathResolver.resolve_element(root, "")

    def test_raises_when_element_not_found(self) -> None:
        pkg = _FakeElement("pkg")
        root = _FakeElement("Root", children=[pkg])
        with pytest.raises(PathResolverError, match="not found: 'Missing'"):
            PathResolver.resolve_element(root, "pkg/Missing")
