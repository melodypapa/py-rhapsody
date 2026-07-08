"""Element-related CLI commands for argparse."""

from __future__ import annotations

import sys
import logging
from typing import Optional

from rhapsody_cli.cli.abstract_command import AbstractCommand
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import RhapsodyConnectionError

logger = logging.getLogger(__name__)

_NO_ACTIVE_INSTANCE_MESSAGE = (
    "No running Rhapsody instance found. Please open Rhapsody and a project first."
)


class AddElementCommand(AbstractCommand):
    """Command: Add a new element to the project."""

    def execute(self, element_type: str, name: str) -> None:
        """Execute the add command.
        
        Args:
            element_type: Type of element to add (class, actor, package)
            name: Name of the new element
        """
        ctx = RhapsodyContext()
        try:
            project = ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            print(_NO_ACTIVE_INSTANCE_MESSAGE, file=sys.stderr)
            sys.exit(1)

        try:
            root = project.getRoot()  # type: ignore[attr-defined]
            
            # Find or use a suitable container
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

            logger.info("Created %s: %s", element_type, name)
            print(f"Created {element_type}: {name}")
        except Exception as e:
            logger.error("Failed to create %s '%s': %s", element_type, name, e)
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class ViewElementCommand(AbstractCommand):
    """Command: View element details."""

    def execute(self, path: str) -> None:
        """Execute the view command.
        
        Args:
            path: Element path (e.g., Root::MyClass)
        """
        ctx = RhapsodyContext()
        try:
            ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            print(_NO_ACTIVE_INSTANCE_MESSAGE, file=sys.stderr)
            sys.exit(1)

        try:
            data = {
                "path": path,
                "type": "unknown",
                "properties": {"status": "read-only for demo"},
            }

            if ctx.output_format == "json":
                output = OutputFormatter.json_format(data)
            else:
                rows = [["path", path], ["type", "unknown"]]
                output = OutputFormatter.table(["Property", "Value"], rows)

            print(output)
        except Exception as e:
            logger.error("Failed to view element '%s': %s", path, e)
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class QueryElementCommand(AbstractCommand):
    """Command: Query elements in active project."""

    def execute(self, pattern: Optional[str] = None) -> None:
        """Execute the query command.
        
        Args:
            pattern: Optional search pattern (not yet implemented)
        """
        ctx = RhapsodyContext()
        try:
            project = ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            print(_NO_ACTIVE_INSTANCE_MESSAGE, file=sys.stderr)
            sys.exit(1)

        try:
            root = project.getRoot()  # type: ignore[attr-defined]
            elements = list(root.getNestedElements())
            
            # Also search in the Default package for classes
            for elem in root.getNestedElements():
                if elem.getName() == "Default" and elem.getMetaClass() == "Package":
                    try:
                        elements.extend(list(elem.getNestedElements()))
                    except Exception:
                        pass  # If we can't get nested elements, just skip

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
        except Exception as e:
            logger.error("Failed to query elements: %s", e)
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


class DeleteElementCommand(AbstractCommand):
    """Command: Delete an element from the project."""

    def execute(self, path: str) -> None:
        """Execute the delete command.
        
        Args:
            path: Element path to delete (e.g., Root::MyClass)
        """
        ctx = RhapsodyContext()
        try:
            project = ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            print(_NO_ACTIVE_INSTANCE_MESSAGE, file=sys.stderr)
            sys.exit(1)

        try:
            root = project.getRoot()  # type: ignore[attr-defined]

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
                print(f"Error: Element '{element_name}' not found at path '{path}'", file=sys.stderr)
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

            logger.info("Deleted %s: %s", meta_class, element_name)
            print(f"Deleted {meta_class.lower()}: {element_name}")
        except Exception as e:
            logger.error("Failed to delete element at path '%s': %s", path, e)
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

