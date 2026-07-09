"""Element actions - each subcommand of `element` as its own Action class."""

import argparse
from typing import Any, List, Optional, Tuple

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.cli.path_resolver import PathResolver, PathResolverError
from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.models.core import call_com


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
        add_parser.add_argument(
            "--path",
            default=None,
            help="Container path using '/' or '\\' separators (default: project root)",
        )
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

        try:
            project = self._get_active_project()
            root = project.getRoot()
            container = PathResolver.resolve_container(root, path)
        except PathResolverError as e:
            self.logger.error("%s", e)
            raise CliExecutionError(str(e)) from e
        except Exception as e:
            self._handle_execution_error(e, "Failed to resolve container path")

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
        view_parser.add_argument(
            "--path",
            required=True,
            help="Element path using '/' or '\\' separators (e.g. pkg/subpkg/MyClass)",
        )
        self.add_verbose_argument(view_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """View element details."""
        path = args.path
        try:
            project = self._get_active_project()
            root = project.getRoot()
            element = PathResolver.resolve_element(root, path)
        except PathResolverError as e:
            self.logger.error("%s", e)
            raise CliExecutionError(str(e)) from e
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view element '{path}'")

        data = {
            "path": path,
            "name": element.getName(),
            "type": element.getMetaClass(),  # type: ignore[attr-defined]
        }

        from rhapsody_cli.cli.context import RhapsodyContext

        ctx = RhapsodyContext()

        # NOTE: This is the command's result data (not a status/log message),
        # so it is written directly to stdout via print() rather than the
        # logger, to keep it safe for piping/redirection (e.g. `> out.json`).
        if ctx.output_format == "json":
            output = OutputFormatter.json_format(data)
        else:
            rows = [["path", path], ["name", data["name"]], ["type", data["type"]]]
            output = OutputFormatter.table(["Property", "Value"], rows)

        print(output)


class ElementQueryAction(ElementManagementAction):
    """Query element action - lists elements in the active project."""

    def __init__(self) -> None:
        """Initialize the 'query' action."""
        super().__init__(command_id="query")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'query' subcommand and its arguments."""
        query_parser = sub_parser.add_parser("query", help="Query elements in active project")
        query_parser.add_argument("pattern", nargs="?", default=None, help="Search pattern (optional)")
        query_parser.add_argument(
            "--path",
            default=None,
            help="Container path using '/' or '\\' separators (default: project root)",
        )
        query_parser.add_argument(
            "--recursive",
            action="store_true",
            help="Include elements nested at any depth below the container",
        )
        self.add_verbose_argument(query_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Query elements in active project."""
        path = args.path
        recursive = args.recursive

        try:
            project = self._get_active_project()
            root = project.getRoot()
            container = PathResolver.resolve_container(root, path)
        except PathResolverError as e:
            self.logger.error("%s", e)
            raise CliExecutionError(str(e)) from e
        except Exception as e:
            self._handle_execution_error(e, "Failed to query elements")

        base_path = path or ""
        results = self._collect_elements(container, base_path, recursive)

        from rhapsody_cli.cli.context import RhapsodyContext

        ctx = RhapsodyContext()

        # NOTE: This is the command's result data (not a status/log message),
        # so it is written directly to stdout via print() rather than the
        # logger, to keep it safe for piping/redirection (e.g. `> out.json`).
        if ctx.output_format == "json":
            data = {"elements": [{"name": name, "type": meta_class, "path": elem_path} for name, meta_class, elem_path in results]}
            output = OutputFormatter.json_format(data)
        elif recursive:
            rows = [[name, meta_class, elem_path] for name, meta_class, elem_path in results]
            output = OutputFormatter.table(["Name", "Type", "Path"], rows)
        else:
            rows = [[name, meta_class] for name, meta_class, _ in results]
            output = OutputFormatter.table(["Name", "Type"], rows)

        print(output)

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
        delete_parser.add_argument(
            "--recursive",
            action="store_true",
            help="Delete the element and all elements nested within it",
        )
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

        try:
            project = self._get_active_project()
            root = project.getRoot()
            element = PathResolver.resolve_element(root, path)
        except PathResolverError as e:
            self.logger.error("%s", e)
            raise CliExecutionError(str(e)) from e
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete element at path '{path}'")

        nested_count = 0
        if recursive:
            nested_count = self._count_nested(element)
            if not force:
                answer = input(f"This will delete '{path}' and {nested_count} nested element(s). Continue? [y/N] ")
                if answer.strip().lower() not in ("y", "yes"):
                    self.logger.info("Aborted delete of '%s'", path)
                    return

        try:
            call_com(lambda: element._com.delete())  # type: ignore[attr-defined]
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
