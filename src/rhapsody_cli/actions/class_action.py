"""Class-related CLI actions.

SWR_CLS_00001: Class Create Command
SWR_CLS_00002: Class Delete Command
SWR_CLS_00003: Class View Command
SWR_CLS_00004: Class List Command
SWR_CLS_00005: Path Validation
SWR_CLS_00006: External JSON File Support
SWR_CLS_00007: Stereotype and Tag Support
SWR_CLS_00008: Multi-Format Output
SWR_CLS_00009: View-to-Create Workflow
SWR_CLS_00010: Error Handling and Logging
SWR_CLS_00011: Class Link Command
SWR_CLS_00012: Boolean Flag Support
SWR_CLS_00013: GUID Lookup Support
SWR_CLS_00014: Class Update Command
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, cast

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class AbstractClassAction(ElementManagementAction):
    """Base class for class actions with common path and GUID validation.

    SWR_CLS_00005: Path Validation
    SWR_CLS_00010: Error Handling and Logging
    SWR_CLS_00013: GUID Lookup Support
    """

    _PACKAGE_META_CLASSES = {"Package", "Project"}

    def _resolve_and_validate_package(self, path: str) -> Any:
        """Resolve path and validate it's a Package or Project element.

        Used by create and list. RPProject inherits addClass/getClasses from
        RPPackage, so the project root is a valid parent.

        Args:
            path: Package path to resolve.

        Returns:
            Package or Project COM object.

        Raises:
            CliExecutionError: If path not found or not a Package/Project.
        """
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False, operation=f"resolve package path '{path}'")

        meta_class = container.get_meta_class()
        if meta_class not in self._PACKAGE_META_CLASSES:
            raise CliExecutionError(f"Path '{path}' does not resolve to a Package or Project (found {meta_class})")

        return container

    def _resolve_and_validate_class(self, path: str) -> Any:
        """Resolve path and validate it's a Class element.

        Used by delete, view, and link.

        Args:
            path: Class path to resolve.

        Returns:
            Class COM object.

        Raises:
            CliExecutionError: If path not found or not a Class.
        """
        root = self._get_active_root()
        element = self._resolve_container_or_element(root, path, resolve_element=True, operation=f"resolve class path '{path}'")

        meta_class = element.get_meta_class()
        if meta_class != "Class":
            raise CliExecutionError(f"Path '{path}' does not resolve to a Class (found {meta_class})")

        return element

    def _resolve_class_by_guid(self, guid: str) -> Any:
        """Locate a class by GUID and validate it's a Class element.

        SWR_CLS_00013: GUID Lookup Support

        Args:
            guid: GUID string in format 12345678-1234-1234-1234-123456789abc.

        Returns:
            Class COM object.

        Raises:
            CliExecutionError: If GUID not found or element is not a Class.
        """
        project = self._get_active_project()
        try:
            element = project.find_element_by_guid(guid)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to locate class by GUID '{guid}'")

        if element is None:
            raise CliExecutionError(f"No element found with GUID '{guid}'")

        meta_class = element.get_meta_class()
        if meta_class != "Class":
            raise CliExecutionError(f"GUID '{guid}' does not resolve to a Class (found {meta_class})")

        return element


class ClassCreateAction(AbstractClassAction):
    """Create one or multiple classes.

    SWR_CLS_00001: Class Create Command
    SWR_CLS_00006: External JSON File Support
    SWR_CLS_00007: Stereotype and Tag Support
    SWR_CLS_00009: View-to-Create Workflow
    SWR_CLS_00012: Boolean Flag Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "description",
        "isAbstract",
        "isFinal",
        "isActive",
        "stereotypes",
        "tags",
        "operations",
        "attributes",
        "superclasses",
    }

    def __init__(self) -> None:
        """Initialize the 'create' action."""
        super().__init__(command_id="create")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'create' subcommand and its arguments."""
        parser = sub_parser.add_parser("create", help="Create a class")
        self.add_path_argument(parser, required=True, help_text="Parent package path")
        parser.add_argument("--input", default=None, help="JSON file with class attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class creation."""
        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)
        classes_data = data if isinstance(data, list) else [data]

        parent = self._resolve_and_validate_package(args.path)

        created: List[str] = []
        errors: List[str] = []
        for cls_attrs in classes_data:
            try:
                name = self._create_single_class(parent, cls_attrs, args.path)
                created.append(name)
            except CliExecutionError:
                raise
            except Exception as e:
                cls_name = cls_attrs.get("name", "unknown")
                self.logger.error("Failed to create class '%s': %s", cls_name, e)
                errors.append(cls_name)

        self._report_results(created, errors, len(classes_data))

    def _create_single_class(self, parent: Any, cls_attrs: Dict[str, Any], parent_path: str) -> str:
        """Create a single class and set its attributes. Returns the class name."""
        name = str(cls_attrs.get("name", ""))
        if not name:
            raise CliExecutionError("'name' is required in attributes")

        unknown = set(cls_attrs.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        cls = parent.add_class(name)
        self._set_attributes(parent, cls, cls_attrs)

        full_path = f"{parent_path}/{name}"
        self.logger.info("Created class: %s", full_path)
        return name

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} classes; all failed")
        if errors:
            self.logger.info("Created %d/%d classes with %d error(s)", len(created), total, len(errors))

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_CLS_0006: External JSON File Support
        """
        if attributes_input.startswith("{") or attributes_input.startswith("["):
            try:
                return json.loads(attributes_input)
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}") from e

        if not Path(attributes_input).exists():
            raise CliExecutionError(f"File not found: {attributes_input}")

        try:
            with open(attributes_input, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise CliExecutionError(f"Invalid JSON in file: {e}") from e
        except OSError as e:
            raise CliExecutionError(f"Failed to read file: {e}") from e

    def _set_attributes(self, parent: Any, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on class."""
        self._set_basic_attributes(cls, attrs)
        self._set_boolean_flags(cls, attrs)
        self._set_properties(cls, attrs)
        self._set_stereotypes(cls, attrs)
        self._set_operations(cls, attrs)
        self._set_attributes_list(cls, attrs)
        self._set_superclasses(parent, cls, attrs)

    def _set_basic_attributes(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set basic attributes."""
        if "description" in attrs:
            cls.set_description(attrs["description"])

    def _set_boolean_flags(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set boolean flags isAbstract, isFinal, isActive.

        SWR_CLS_00012: Boolean Flag Support
        """
        if "isAbstract" in attrs:
            cls.set_is_abstract(1 if attrs["isAbstract"] else 0)
        if "isFinal" in attrs:
            cls.set_is_final(1 if attrs["isFinal"] else 0)
        if "isActive" in attrs:
            cls.set_is_active(1 if attrs["isActive"] else 0)

    def _set_properties(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set custom properties (tags)."""
        if "tags" in attrs:
            for key, val in attrs["tags"].items():
                cls.set_property_value(key, val)

    def _set_stereotypes(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Apply stereotypes."""
        if "stereotypes" in attrs:
            for stereotype in attrs["stereotypes"]:
                cls.add_stereotype(stereotype, "Class")

    def _set_operations(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add operations."""
        if "operations" in attrs:
            for op_name in attrs["operations"]:
                cls.add_operation(op_name)

    def _set_attributes_list(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add attributes."""
        if "attributes" in attrs:
            for attr_name in attrs["attributes"]:
                cls.add_attribute(attr_name)

    def _set_superclasses(self, parent: Any, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add generalization relationships to superclasses.

        SWR_CLS_00001: resolves superclass names via parent.findNestedClassifierRecursive(name).
        """
        if "superclasses" in attrs:
            for name in attrs["superclasses"]:
                target = parent.find_nested_classifier_recursive(name)
                if target is None:
                    raise CliExecutionError(f"Superclass '{name}' not found in package")
                cls.add_generalization(target)


class ClassDeleteAction(AbstractClassAction):
    """Delete a class.

    SWR_CLS_00002: Class Delete Command
    SWR_CLS_00013: GUID Lookup Support
    """

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'delete' subcommand and its arguments."""
        parser = sub_parser.add_parser("delete", help="Delete a class")
        self.add_path_argument(parser, required=False, help_text="Class path to delete")
        parser.add_argument("--guid", default=None, help="Class GUID to delete")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class deletion."""
        if args.path and args.guid:
            raise CliExecutionError("Only one of --path or --guid may be specified")
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid must be specified")

        if args.guid:
            cls = self._resolve_class_by_guid(args.guid)
            label = f"GUID '{args.guid}'"
        else:
            cls = self._resolve_and_validate_class(args.path)
            label = args.path

        try:
            cls.delete_from_project()
            self.logger.info("Deleted class: %s", label)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete class '{label}'")


class ClassListAction(AbstractClassAction):
    """List classes in a package.

    SWR_CLS_00004: Class List Command
    SWR_CLS_00008: Multi-Format Output
    """

    def __init__(self) -> None:
        """Initialize the 'list' action."""
        super().__init__(command_id="list")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'list' subcommand and its arguments."""
        parser = sub_parser.add_parser("list", help="List classes in a package")
        self.add_path_argument(parser, required=True, help_text="Package path")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class list."""
        package = self._resolve_and_validate_package(args.path)

        try:
            class_names = self._collect_class_names(package)
            output = self._format_output(class_names, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote %d classes to: %s", len(class_names), args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to list classes in '{args.path}'")

    def _collect_class_names(self, package: Any) -> List[str]:
        """Collect names of classes in package."""
        classes = package.get_classes()
        return [cls.get_name() for cls in classes]

    def _format_output(self, class_names: List[str], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(class_names)
        elif format_type == "csv":
            table_rows = [[name] for name in class_names]
            return OutputFormatter.csv_format(["Name"], table_rows)
        else:
            table_rows = [[name] for name in class_names]
            return OutputFormatter.table(["Name"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class ClassViewAction(AbstractClassAction):
    """View class details.

    SWR_CLS_00003: Class View Command
    SWR_CLS_00008: Multi-Format Output
    SWR_CLS_00013: GUID Lookup Support
    """

    _VIEW_HEADERS = [
        "Name",
        "GUID",
        "Description",
        "IsAbstract",
        "IsActive",
        "IsFinal",
        "IsComposite",
        "IsReactive",
        "MetaClass",
        "FullPath",
        "Operations",
        "Attributes",
    ]
    _VIEW_KEYS = [
        "name",
        "guid",
        "description",
        "isAbstract",
        "isActive",
        "isFinal",
        "isComposite",
        "isReactive",
        "metaClass",
        "fullPath",
        "operations",
        "attributes",
    ]

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'view' subcommand and its arguments."""
        parser = sub_parser.add_parser("view", help="View class details")
        self.add_path_argument(parser, required=False, help_text="Class path to view")
        parser.add_argument("--guid", default=None, help="Class GUID to view")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class view."""
        if args.path and args.guid:
            raise CliExecutionError("Only one of --path or --guid may be specified")
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid must be specified")

        if args.guid:
            cls = self._resolve_class_by_guid(args.guid)
        else:
            cls = self._resolve_and_validate_class(args.path)

        try:
            data = self._collect_class_data(cls)
            output = self._format_output(data, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote class details to: %s", args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view class '{args.path or args.guid}'")

    def _collect_class_data(self, cls: Any) -> Dict[str, Any]:
        """Collect class details into a data dictionary.

        Normalizes IsAbstract (bool) to int for clean JSON round-trip.
        """
        operations = cls.get_operations()
        attributes = cls.get_attributes()
        return {
            "name": cls.get_name(),
            "guid": cls.get_guid(),
            "description": cls.get_description(),
            "isAbstract": int(cls.get_is_abstract()),
            "isActive": int(cls.get_is_active()),
            "isFinal": int(cls.get_is_final()),
            "isComposite": int(cls.get_is_composite()),
            "isReactive": int(cls.get_is_reactive()),
            "metaClass": cls.get_meta_class(),
            "fullPath": cls.get_full_path_name(),
            "operations": [op.get_name() for op in operations],
            "attributes": [attr.get_name() for attr in attributes],
        }

    def _format_output(self, data: Dict[str, Any], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(data)
        elif format_type == "csv":
            data_row = [data[key] for key in self._VIEW_KEYS]
            return OutputFormatter.csv_format(self._VIEW_HEADERS, [data_row])
        else:
            table_rows = [
                ["Name", data["name"]],
                ["GUID", data["guid"]],
                ["Description", data["description"]],
                ["IsAbstract", data["isAbstract"]],
                ["IsActive", data["isActive"]],
                ["IsFinal", data["isFinal"]],
                ["IsComposite", data["isComposite"]],
                ["IsReactive", data["isReactive"]],
                ["MetaClass", data["metaClass"]],
                ["FullPath", data["fullPath"]],
                ["Operations", ", ".join(data["operations"])],
                ["Attributes", ", ".join(data["attributes"])],
            ]
            return OutputFormatter.table(["Property", "Value"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class ClassLinkAction(AbstractClassAction):
    """Add or remove generalization relationships between classes.

    SWR_CLS_00011: Class Link Command (generalization only — association
        and unidirectional deferred to future iteration)
    SWR_CLS_00013: GUID Lookup Support
    """

    def __init__(self) -> None:
        """Initialize the 'link' action."""
        super().__init__(command_id="link")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'link' subcommand and its arguments."""
        parser = sub_parser.add_parser("link", help="Add or remove generalization relationships")
        self.add_path_argument(parser, required=False, help_text="Class path to modify")
        parser.add_argument("--guid", default=None, help="Class GUID to modify")
        parser.add_argument("--add", default=None, help="Add a generalization to target class by name")
        parser.add_argument("--remove", default=None, help="Remove a generalization to target class by name")
        parser.add_argument(
            "--type",
            choices=["generalization"],
            default="generalization",
            help="Relationship type (v1 supports only generalization)",
        )
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class link operation."""
        if args.path and args.guid:
            raise CliExecutionError("Only one of --path or --guid may be specified")
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid must be specified")
        if args.add and args.remove:
            raise CliExecutionError("Only one of --add or --remove may be specified")
        if not args.add and not args.remove:
            raise CliExecutionError("Either --add or --remove must be specified")

        if args.guid:
            source = self._resolve_class_by_guid(args.guid)
        else:
            source = self._resolve_and_validate_class(args.path)

        target_name = args.add if args.add else args.remove
        target = source.find_nested_classifier_recursive(target_name)
        if target is None:
            raise CliExecutionError(f"Class '{target_name}' not found")

        try:
            if args.add:
                source.add_generalization(target)
                self.logger.info(
                    "Added generalization: %s -> %s",
                    args.path or args.guid,
                    target_name,
                )
            else:
                source.delete_generalization(target)
                self.logger.info(
                    "Removed generalization: %s -/-> %s",
                    args.path or args.guid,
                    target_name,
                )
        except Exception as e:
            self._handle_execution_error(e, f"Failed to modify generalization for class '{args.path or args.guid}'")


class ClassUpdateAction(AbstractClassAction):
    """Update attributes of an existing class.

    SWR_CLS_00014: Class Update Command
    SWR_CLS_00006: External JSON File Support
    SWR_CLS_00007: Stereotype and Tag Support
    SWR_CLS_00012: Boolean Flag Support
    SWR_CLS_00013: GUID Lookup Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "description",
        "isAbstract",
        "isFinal",
        "isActive",
        "stereotypes",
        "tags",
    }

    def __init__(self) -> None:
        """Initialize the 'update' action."""
        super().__init__(command_id="update")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'update' subcommand and its arguments."""
        parser = sub_parser.add_parser("update", help="Update attributes of an existing class")
        self.add_path_argument(parser, required=False, help_text="Class path to update")
        parser.add_argument("--guid", default=None, help="GUID of the class to update")
        parser.add_argument("--input", default=None, help="JSON file with class attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def _load_json_data(self, args: Any) -> Dict[str, Any]:
        """Load JSON data from inline string or file.

        SWR_CLS_0006: External JSON File Support

        Args:
            args: Parsed argparse.Namespace with `input` and `attributes`.

        Returns:
            Dictionary of class attributes (empty if neither provided).
        """
        if args.input:
            try:
                with open(args.input, encoding="utf-8") as f:
                    return cast(Dict[str, Any], json.load(f))
            except FileNotFoundError:
                raise CliExecutionError(f"File not found: {args.input}") from None
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}") from e
        elif args.attributes:
            data_str = args.attributes.strip()
            if data_str.startswith("{"):
                try:
                    return cast(Dict[str, Any], json.loads(data_str))
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}") from e
            else:
                try:
                    with open(data_str, encoding="utf-8") as f:
                        return cast(Dict[str, Any], json.load(f))
                except FileNotFoundError:
                    raise CliExecutionError(f"File not found: {data_str}") from None
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}") from e
        return {}

    def _set_attributes(self, cls: Any, data: Dict[str, Any]) -> None:
        """Set validated attributes on class (partial update).

        SWR_CLS_00012: Boolean Flag Support

        Only fields present in `data` are modified; unknown fields are
        skipped with a warning log.

        Args:
            cls: Class COM object to update.
            data: Dictionary of attributes to apply.
        """
        for key, value in data.items():
            if key not in self.VALID_ATTRIBUTES:
                self.logger.warning("Skipping unknown attribute: %s", key)
                continue
            if key == "name":
                cls.set_name(value)
            elif key == "description":
                cls.set_description(value)
            elif key == "isAbstract":
                cls.set_is_abstract(1 if value else 0)
            elif key == "isFinal":
                cls.set_is_final(1 if value else 0)
            elif key == "isActive":
                cls.set_is_active(1 if value else 0)
            elif key == "stereotypes":
                for stereotype in value:
                    cls.add_stereotype(stereotype, "Class")
            elif key == "tags":
                for tag_key, tag_value in value.items():
                    cls.set_property_value(tag_key, tag_value)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute class update.

        Args:
            args: Parsed argparse.Namespace with path/guid and attribute data.
        """
        self.logger.info("Starting class update...")
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid is required")
        if args.guid:
            self.logger.info("Resolving class by GUID '%s'...", args.guid)
            cls = self._resolve_class_by_guid(args.guid)
        else:
            self.logger.info("Resolving class path '%s'...", args.path)
            cls = self._resolve_and_validate_class(args.path)
        data = self._load_json_data(args)
        self._set_attributes(cls, data)
        self.logger.info("Successfully updated class: %s", cls.get_name())
