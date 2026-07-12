"""Parses and navigates multi-level element paths using "/" or "\\" separators."""

from typing import List, Optional, Protocol


class PathResolverError(Exception):
    """Raised when a path string cannot be parsed or navigated to an element."""


class _Navigable(Protocol):
    """Structural type for anything PathResolver can navigate: needs a name and children."""

    def get_name(self) -> str: ...  # pragma: no cover - structural protocol

    def get_nested_elements(self) -> object: ...  # pragma: no cover - structural protocol


class PathResolver:
    """Parses "/" or "\\"-separated element paths and navigates element hierarchies.

    Paths may optionally start with a "Root" segment (case-insensitive), which is
    ignored since navigation always starts from the caller-supplied root element.
    """

    _ROOT_ALIAS = "root"

    @staticmethod
    def normalize(path: str) -> str:
        """Convert "\\" separators to "/" and strip leading/trailing slashes."""
        normalized = path.replace("\\", "/").strip()
        return normalized.strip("/")

    @staticmethod
    def split_segments(path: str) -> List[str]:
        """Split a path into non-empty segments, dropping a leading "Root" alias.

        Args:
            path: The raw path string (e.g. "pkg/subpkg/class" or "Root\\pkg").

        Returns:
            The list of path segments, excluding a leading "Root" alias.

        Raises:
            PathResolverError: If the path is empty, or contains an empty
                segment (e.g. "pkg//class").
        """
        normalized = PathResolver.normalize(path)
        if not normalized:
            raise PathResolverError("Path cannot be empty")

        raw_segments = normalized.split("/")
        if any(segment == "" for segment in raw_segments):
            raise PathResolverError(f"Invalid path syntax: '{path}'")

        if raw_segments[0].lower() == PathResolver._ROOT_ALIAS:
            raw_segments = raw_segments[1:]

        if not raw_segments:
            raise PathResolverError("Path cannot be empty")

        return raw_segments

    @staticmethod
    def resolve_container(root: _Navigable, path: Optional[str]) -> _Navigable:
        """Navigate from root to the container described by path.

        Args:
            root: The starting element (typically the project root).
            path: A "/" or "\\"-separated path to the container, or None/""
                to mean the root itself.

        Returns:
            The element found at the end of the path (or root if path is empty).

        Raises:
            PathResolverError: If any path segment cannot be found.
        """
        if not path:
            return root
        segments = PathResolver.split_segments(path)
        return PathResolver._navigate(root, segments, path)

    @staticmethod
    def resolve_element(root: _Navigable, path: str) -> _Navigable:
        """Navigate from root to the element described by path.

        Args:
            root: The starting element (typically the project root).
            path: A "/" or "\\"-separated path to the element (the last
                segment is the element itself, not a container).

        Returns:
            The element found at the end of the path.

        Raises:
            PathResolverError: If the path is empty or any segment cannot be found.
        """
        segments = PathResolver.split_segments(path)
        return PathResolver._navigate(root, segments, path)

    @staticmethod
    def _navigate(root: _Navigable, segments: List[str], original_path: str) -> _Navigable:
        """Walk `segments` from `root`, matching each against child get_name()."""
        current = root
        visited: List[str] = []
        for segment in segments:
            found = None
            for child in current.get_nested_elements():  # type: ignore[attr-defined]
                if child.get_name() == segment:
                    found = child
                    break
            if found is None:
                stopped_at = "/".join(visited) if visited else "<root>"
                raise PathResolverError(f"Could not navigate to '{original_path}' — stopped at " f"'{stopped_at}' (not found: '{segment}')")
            current = found
            visited.append(segment)
        return current
