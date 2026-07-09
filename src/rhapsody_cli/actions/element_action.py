"""Element actions - each subcommand of `element` as its own Action class."""

import argparse
from typing import Any, List, Optional, Tuple

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.models.core import AbstractRPModelElement


class ElementAddAction(ElementManagementAction):
    """Add element action - handles adding new elements to the project."""

    def __init__(self) -> None:
        """Initialize the 'add' action."""
        super().__init__(command_id="add")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'add' subcommand and its arguments."""
        add_parser = sub_parser.add_parser("add", help="Add a new element")
        add_parser.add_argument("--type", required=True, help="Element type (class, actor, package)")
        add_parser.add_argument("--name", default=None, help="Element name (required unless --bulk is used)")
        add_parser.add_argument("--bulk", default=None, help="Path to a file with one element name per line")
        self.add_path_argument(add_parser)
        self.add_verbose_argument(add_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Add one or more new elements to the project."""
        element_type = args.type
        name = args.name
        bulk_file = args.bulk
        path = args.path

        if not name and not bulk_file:
            raise CliExecutionError("either --name or --bulk must be provided")

        if name and bulk_file:
            raise CliExecutionError("--name and --bulk cannot be used together")

        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False, operation="resolve container path")

        if bulk_file:
            self._execute_bulk(element_type, bulk_file, container, path)
        else:
            self._execute_single(element_type, name, container, path)

    def _execute_single(self, element_type: str, name: str, container: Any, path: Optional[str]) -> None:
        """Create a single element under `container` and report the result."""
        try:
            self._create_element(element_type, name, container)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to create {element_type} '{name}'")

        full_path = f"{path}/{name}" if path else name
        self.logger.info("Created %s: %s", element_type, full_path)

    def _execute_bulk(self, element_type: str, bulk_file: str, container: Any, path: Optional[str]) -> None:
        """Create one element per non-empty line of `bulk_file` under `container`."""
        try:
            with open(bulk_file, encoding="utf-8") as f:
                lines = f.readlines()
        except OSError as e:
            raise CliExecutionError(f"Could not read bulk file '{bulk_file}': {e}") from e

        created: List[Tuple[str, str]] = []
        errors: List[Tuple[int, str, str]] = []
        for line_num, raw_line in enumerate(lines, start=1):
            item_name = raw_line.strip()
            if not item_name:
                continue
            try:
                self._create_element(element_type, item_name, container)
                full_path = f"{path}/{item_name}" if path else item_name
                created.append((item_name, full_path))
                self.logger.info("Created %s: %s", element_type, full_path)
            except Exception as e:
                errors.append((line_num, item_name, str(e)))
                self.logger.error("Line %d (%s): %s", line_num, item_name, e)

        total = len(created) + len(errors)
        if errors:
            self.logger.info("Added %d/%d items with %d error(s)", len(created), total, len(errors))
        else:
            self.logger.info("Added %d item(s)", len(created))

        if errors and not created:
            raise CliExecutionError(f"Added 0/{total} items; all items failed")

    def _create_element(self, element_type: str, name: str, container: Any) -> None:
        """Dispatch element creation to the right container method by type."""
        element_type_lower = element_type.lower()
        if element_type_lower == "class":
            container.addClass(name)
        elif element_type_lower == "actor":
            container.addActor(name)
        elif element_type_lower == "package":
            if hasattr(container, "addPackage"):
                container.addPackage(name)
            else:
                container.addNestedPackage(name)
        else:
            raise ValueError(f"Unknown element type '{element_type}'")


class ElementViewAction(ElementManagementAction):
    """View element action - shows details for a single element."""

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'view' subcommand and its arguments."""
        view_parser = sub_parser.add_parser("view", help="View element details")
        self.add_path_argument(
            view_parser,
            required=True,
            help_text="Element path using '/' or '\\' separators (e.g. pkg/subpkg/MyClass)",
        )
        self.add_verbose_argument(view_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """View element details."""
        path = args.path
        root = self._get_active_root()
        element = self._resolve_container_or_element(root, path, resolve_element=True, operation=f"view element '{path}'")

        name = element.getName()
        meta_class = element.getMetaClass()  # type: ignore[attr-defined]
        data = {"path": path, "name": name, "type": meta_class}

        # NOTE: This is the command's result data (not a status/log message),
        # so it is written directly to stdout via print() rather than the
        # logger, to keep it safe for piping/redirection (e.g. `> out.json`).
        self._print_formatted_output(
            data=data,
            headers=["Property", "Value"],
            table_rows=[["path", path], ["name", name], ["type", meta_class]],
        )


class ElementQueryAction(ElementManagementAction):
    """Query element action - lists elements in the active project."""

    def __init__(self) -> None:
        """Initialize the 'query' action."""
        super().__init__(command_id="query")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'query' subcommand and its arguments."""
        query_parser = sub_parser.add_parser("query", help="Query elements in active project")
        query_parser.add_argument("pattern", nargs="?", default=None, help="Search pattern (optional)")
        self.add_path_argument(query_parser)
        self.add_recursive_argument(query_parser, help_text=self._RECURSIVE_QUERY_HELP)
        self.add_verbose_argument(query_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Query elements in active project."""
        path = args.path
        recursive = args.recursive

        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False, operation="query elements")

        base_path = path or ""
        results = self._collect_elements(container, base_path, recursive)

        data = {"elements": [{"name": n, "type": m, "path": p} for n, m, p in results]}
        headers = ["Name", "Type", "Path"] if recursive else ["Name", "Type"]
        table_rows = [list(row) for row in ([n, m, p] if recursive else [n, m] for n, m, p in results)]

        # NOTE: This is the command's result data (not a status/log message),
        # so it is written directly to stdout via print() rather than the
        # logger, to keep it safe for piping/redirection (e.g. `> out.json`).
        self._print_formatted_output(data=data, headers=headers, table_rows=table_rows)

    def _collect_elements(self, container: Any, base_path: str, recursive: bool) -> List[Tuple[str, str, str]]:
        """Collect (name, meta_class, path) tuples for direct or recursive children."""
        results: List[Tuple[str, str, str]] = []
        for elem in container.getNestedElements():
            name = elem.getName()
            meta_class = elem.getMetaClass()
            elem_path = f"{base_path}/{name}" if base_path else name
            results.append((name, meta_class, elem_path))
            if recursive:
                results.extend(self._collect_elements(elem, elem_path, recursive))
        return results


class ElementDeleteAction(ElementManagementAction):
    """Delete element action - removes an element from the project."""

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'delete' subcommand and its arguments."""
        delete_parser = sub_parser.add_parser("delete", help="Delete an element")
        delete_parser.add_argument("path", help="Element path using '/' or '\\' separators")
        self.add_recursive_argument(delete_parser, help_text=self._RECURSIVE_DELETE_HELP)
        delete_parser.add_argument(
            "--force",
            action="store_true",
            help="Skip the confirmation prompt when using --recursive",
        )
        self.add_verbose_argument(delete_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Delete an element from the project."""
        path = args.path
        recursive = args.recursive
        force = args.force

        root = self._get_active_root()
        element = self._resolve_container_or_element(root, path, resolve_element=True, operation=f"delete element at path '{path}'")

        nested_count = 0
        if recursive:
            nested_count = self._count_nested(element)
            if not force:
                answer = input(f"This will delete '{path}' and {nested_count} nested element(s). Continue? [y/N] ")
                if answer.strip().lower() not in ("y", "yes"):
                    self.logger.info("Aborted delete of '%s'", path)
                    return

        try:
            AbstractRPModelElement.call_com(lambda: element._com.delete())  # type: ignore[attr-defined]
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete element at path '{path}'")

        meta_class = element.getMetaClass()  # type: ignore[attr-defined]
        if recursive:
            self.logger.info("Deleted %s: %s (and %d nested elements)", meta_class, path, nested_count)
        else:
            self.logger.info("Deleted %s: %s", meta_class, path)

    def _count_nested(self, element: Any) -> int:
        """Recursively count all elements nested within `element`."""
        count = 0
        for child in element.getNestedElements():
            count += 1
            count += self._count_nested(child)
        return count
