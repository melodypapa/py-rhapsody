"""Element actions - each subcommand of `element` as its own Action class."""

import argparse
import sys

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter


class ElementAddAction(ElementManagementAction):
    """Add element action - handles adding new elements to the project."""

    def __init__(self) -> None:
        """Initialize the 'add' action."""
        super().__init__(command_id="add")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'add' subcommand and its arguments."""
        add_parser = sub_parser.add_parser("add", help="Add a new element")
        add_parser.add_argument("--type", required=True, help="Element type (class, actor, package)")
        add_parser.add_argument("--name", required=True, help="Element name")
        self.add_verbose_argument(add_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Add a new element to the project."""
        element_type = args.type
        name = args.name

        try:
            project = self._get_active_project()
            root = project.getRoot()
            container = root

            # For classes and actors, try to use the Default package if it exists
            if element_type.lower() in ("class", "actor"):
                nested_elements = root.getNestedElements()
                for elem in nested_elements:
                    if elem.getName() == "Default" and elem.getMetaClass() == "Package":
                        container = elem
                        break

            if element_type.lower() == "class":
                container.addClass(name)
            elif element_type.lower() == "actor":
                container.addActor(name)
            elif element_type.lower() == "package":
                container.addNestedPackage(name) if container != root else root.addPackage(name)
            else:
                print(f"Error: Unknown element type '{element_type}'", file=sys.stderr)
                sys.exit(1)

            self.logger.info("Created %s: %s", element_type, name)
            print(f"Created {element_type}: {name}")
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to create {element_type} '{name}'")
            sys.exit(1)


class ElementViewAction(ElementManagementAction):
    """View element action - shows details for a single element."""

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'view' subcommand and its arguments."""
        view_parser = sub_parser.add_parser("view", help="View element details")
        view_parser.add_argument("--path", required=True, help="Element path (e.g., Root::MyClass)")
        self.add_verbose_argument(view_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """View element details."""
        path = args.path
        try:
            self._get_active_project()

            data = {
                "path": path,
                "type": "unknown",
                "properties": {"status": "read-only for demo"},
            }

            from rhapsody_cli.cli.context import RhapsodyContext
            ctx = RhapsodyContext()

            if ctx.output_format == "json":
                output = OutputFormatter.json_format(data)
            else:
                rows = [["path", path], ["type", "unknown"]]
                output = OutputFormatter.table(["Property", "Value"], rows)

            print(output)
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view element '{path}'")
            sys.exit(1)


class ElementQueryAction(ElementManagementAction):
    """Query element action - lists elements in the active project."""

    def __init__(self) -> None:
        """Initialize the 'query' action."""
        super().__init__(command_id="query")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'query' subcommand and its arguments."""
        query_parser = sub_parser.add_parser("query", help="Query elements in active project")
        query_parser.add_argument("pattern", nargs="?", default=None, help="Search pattern (optional)")
        self.add_verbose_argument(query_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Query elements in active project."""
        try:
            project = self._get_active_project()
            root = project.getRoot()
            elements = list(root.getNestedElements())

            # Also search in the Default package for classes
            for elem in root.getNestedElements():
                if elem.getName() == "Default" and elem.getMetaClass() == "Package":
                    try:
                        elements.extend(list(elem.getNestedElements()))
                    except Exception:
                        pass  # If we can't get nested elements, just skip

            from rhapsody_cli.cli.context import RhapsodyContext
            ctx = RhapsodyContext()

            if ctx.output_format == "json":
                data = {
                    "elements": [
                        {
                            "name": elem.getName(),
                            "type": elem.getMetaClass(),
                        }
                        for elem in elements
                    ]
                }
                output = OutputFormatter.json_format(data)
            else:
                rows = [[elem.getName(), elem.getMetaClass()] for elem in elements]
                output = OutputFormatter.table(["Name", "Type"], rows)

            print(output)
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, "Failed to query elements")
            sys.exit(1)


class ElementDeleteAction(ElementManagementAction):
    """Delete element action - removes an element from the project."""

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: 'argparse._SubParsersAction[argparse.ArgumentParser]') -> None:
        """Register the 'delete' subcommand and its arguments."""
        delete_parser = sub_parser.add_parser("delete", help="Delete an element")
        delete_parser.add_argument("path", help="Element path to delete")
        self.add_verbose_argument(delete_parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Delete an element from the project."""
        path = args.path
        try:
            project = self._get_active_project()
            root = project.getRoot()

            # Parse path to extract parent path and element name
            path_parts = path.split("::")
            if len(path_parts) < 2:
                msg = f"Error: Invalid path format '{path}'. Use 'Root::ElementName'"
                print(msg, file=sys.stderr)
                sys.exit(1)

            element_name = path_parts[-1]
            parent_path_parts = path_parts[:-1]

            # Navigate to parent container
            parent = root
            for part in parent_path_parts[1:]:  # Skip 'Root'
                nested = parent.getNestedElements()
                found = None
                for elem in nested:
                    if elem.getName() == part:
                        found = elem
                        break
                if not found:
                    print(f"Error: Parent path not found: {part}", file=sys.stderr)
                    sys.exit(1)
                parent = found

            # Find and delete the element
            nested = parent.getNestedElements()
            element_to_delete = None
            for elem in nested:
                if elem.getName() == element_name:
                    element_to_delete = elem
                    break

            # If not found in parent and parent is root, try Default package
            if not element_to_delete and parent == root:
                for elem in parent.getNestedElements():
                    if elem.getName() == "Default" and elem.getMetaClass() == "Package":
                        parent = elem
                        nested = parent.getNestedElements()
                        for elem_in_default in nested:
                            if elem_in_default.getName() == element_name:
                                element_to_delete = elem_in_default
                                break
                        break

            if not element_to_delete:
                error_msg = f"Error: Element '{element_name}' not found at path '{path}'"
                print(error_msg, file=sys.stderr)
                sys.exit(1)

            # Try to delete using different methods based on element type
            meta_class = element_to_delete.getMetaClass()
            deleted = False

            # Try direct delete method first (if available)
            if hasattr(element_to_delete._com, "delete"):
                element_to_delete._com.delete()
                deleted = True
            else:
                # Fall back to parent container methods
                if meta_class == "Class":
                    parent._com.deleteClass(element_to_delete._com)
                    deleted = True
                elif meta_class == "Actor":
                    parent._com.deleteActor(element_to_delete._com)
                    deleted = True
                elif meta_class == "Package":
                    parent._com.deletePackage(element_to_delete._com)
                    deleted = True

            if not deleted:
                print(f"Error: Unable to delete element of type '{meta_class}'", file=sys.stderr)
                sys.exit(1)

            self.logger.info("Deleted %s: %s", meta_class, element_name)
            print(f"Deleted {meta_class.lower()}: {element_name}")
        except SystemExit:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete element at path '{path}'")
            sys.exit(1)
