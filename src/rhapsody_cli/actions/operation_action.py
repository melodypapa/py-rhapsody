"""Operation-related CLI actions.

SWR_OP_00001: Operation Create Command
SWR_OP_00002: Operation Delete Command
SWR_OP_00003: Operation View Command
SWR_OP_00004: Operation List Command
SWR_OP_00005: Operation Update Command
SWR_OP_00006: Path and Name Validation
SWR_OP_00007: External JSON File Support
SWR_OP_00008: Multi-Format Output
SWR_OP_00009: Error Handling and Logging
SWR_OP_00010: GUID Lookup Support
SWR_OP_00011: Returns Type Resolution
SWR_OP_00012: Boolean Flag Support
SWR_OP_00013: Bulk Creation Support
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class AbstractOperationAction(ElementManagementAction):
    """Base class for operation actions with common path, name and GUID validation.

    SWR_OP_00006: Path and Name Validation
    SWR_OP_00009: Error Handling and Logging
    SWR_OP_00010: GUID Lookup Support
    """

    def _resolve_classifier(self, path: str) -> Any:
        """Resolve a parent classifier path.

        Args:
            path: Classifier path to resolve.

        Returns:
            Classifier COM object.

        Raises:
            CliExecutionError: If path not found.
        """
        root = self._get_active_root()
        return self._resolve_container_or_element(root, path, resolve_element=True, operation=f"resolve classifier path '{path}'")

    def _resolve_operation(self, classifier: Any, name: str) -> Any:
        """Find an operation by name within a classifier.

        Args:
            classifier: The parent classifier COM object.
            name: The operation name to find.

        Returns:
            Operation COM object.

        Raises:
            CliExecutionError: If operation not found.
        """
        operation = classifier.find_interface_item(name)
        if operation is None:
            raise CliExecutionError(f"Operation '{name}' not found in classifier")
        return operation

    def _resolve_operation_by_guid(self, guid: str) -> Any:
        """Locate an operation by GUID and validate it's an Operation element.

        SWR_OP_00010: GUID Lookup Support

        Args:
            guid: GUID string in format 12345678-1234-1234-1234-123456789abc.

        Returns:
            Operation COM object.

        Raises:
            CliExecutionError: If GUID not found or element is not an Operation.
        """
        project = self._get_active_project()
        try:
            element = project.find_element_by_guid(guid)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to locate operation by GUID '{guid}'")

        if element is None:
            raise CliExecutionError(f"No element found with GUID '{guid}'")

        meta_class = element.get_meta_class()
        if meta_class != "Operation":
            raise CliExecutionError(f"GUID '{guid}' does not resolve to an Operation (found {meta_class})")

        return element


class OperationCreateAction(AbstractOperationAction):
    """Create one or multiple operations.

    SWR_OP_00001: Operation Create Command
    SWR_OP_00007: External JSON File Support
    SWR_OP_00011: Returns Type Resolution
    SWR_OP_00012: Boolean Flag Support
    SWR_OP_00013: Bulk Creation Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "body",
        "isAbstract",
        "isStatic",
        "isVirtual",
        "returns",
        "visibility",
        "arguments",
        "description",
    }

    def __init__(self) -> None:
        """Initialize the 'create' action."""
        super().__init__(command_id="create")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'create' subcommand and its arguments."""
        parser = sub_parser.add_parser("create", help="Create an operation")
        self.add_path_argument(parser, required=True, help_text="Parent classifier path")
        parser.add_argument("--input", default=None, help="JSON file with operation attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute operation creation."""
        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)
        ops_data = data if isinstance(data, list) else [data]

        classifier = self._resolve_classifier(args.path)

        created: List[str] = []
        errors: List[str] = []
        for op_attrs in ops_data:
            try:
                name = self._create_single_operation(classifier, op_attrs, args.path)
                created.append(name)
            except CliExecutionError:
                raise
            except Exception as e:
                op_name = op_attrs.get("name", "unknown")
                self.logger.error("Failed to create operation '%s': %s", op_name, e)
                errors.append(op_name)

        self._report_results(created, errors, len(ops_data))

    def _create_single_operation(self, classifier: Any, op_attrs: Dict[str, Any], parent_path: str) -> str:
        """Create a single operation and set its attributes. Returns the operation name."""
        name = str(op_attrs.get("name", ""))
        if not name:
            raise CliExecutionError("'name' is required in attributes")

        unknown = set(op_attrs.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        operation = classifier.add_operation(name)
        self._set_attributes(classifier, operation, op_attrs)

        full_path = f"{parent_path}/{name}"
        self.logger.info("Created operation: %s", full_path)
        return name

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} operations; all failed")
        if errors:
            self.logger.info("Created %d/%d operations with %d error(s)", len(created), total, len(errors))

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_OP_00007: External JSON File Support
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

    def _set_attributes(self, classifier: Any, operation: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on operation."""
        if "name" in attrs:
            operation.set_name(attrs["name"])
        if "body" in attrs:
            operation.set_body(attrs["body"])
        if "description" in attrs:
            operation.set_description(attrs["description"])
        if "visibility" in attrs:
            operation.set_visibility(attrs["visibility"])
        if "arguments" in attrs:
            operation.set_arguments(attrs["arguments"])
        self._set_boolean_flags(operation, attrs)
        self._set_returns(classifier, operation, attrs)

    def _set_boolean_flags(self, operation: Any, attrs: Dict[str, Any]) -> None:
        """Set boolean flags isAbstract, isStatic, isVirtual.

        SWR_OP_00012: Boolean Flag Support
        """
        if "isAbstract" in attrs:
            operation.set_is_abstract(1 if attrs["isAbstract"] else 0)
        if "isStatic" in attrs:
            operation.set_is_static(1 if attrs["isStatic"] else 0)
        if "isVirtual" in attrs:
            operation.set_is_virtual(1 if attrs["isVirtual"] else 0)

    def _set_returns(self, classifier: Any, operation: Any, attrs: Dict[str, Any]) -> None:
        """Resolve and set the returns type.

        SWR_OP_00011: Returns Type Resolution
        """
        if "returns" in attrs:
            type_name = attrs["returns"]
            owner = classifier.get_owner()
            target = owner.find_nested_classifier_recursive(type_name)
            if target is None:
                raise CliExecutionError(f"Returns type '{type_name}' not found")
            operation.set_returns(target)


class OperationDeleteAction(AbstractOperationAction):
    """Delete an operation.

    SWR_OP_00002: Operation Delete Command
    SWR_OP_00010: GUID Lookup Support
    """

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'delete' subcommand and its arguments."""
        parser = sub_parser.add_parser("delete", help="Delete an operation")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Operation GUID to delete")
        parser.add_argument("--name", default=None, help="Operation name within classifier")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute operation deletion."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            operation = self._resolve_operation_by_guid(args.guid)
            classifier = operation.get_owner()
            label = f"GUID '{args.guid}'"
        else:
            classifier = self._resolve_classifier(args.path)
            operation = self._resolve_operation(classifier, args.name)
            label = args.name

        try:
            classifier.delete_operation(operation)
            self.logger.info("Deleted operation: %s", label)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete operation '{label}'")


class OperationListAction(AbstractOperationAction):
    """List operations on a classifier.

    SWR_OP_00004: Operation List Command
    SWR_OP_00008: Multi-Format Output
    """

    def __init__(self) -> None:
        """Initialize the 'list' action."""
        super().__init__(command_id="list")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'list' subcommand and its arguments."""
        parser = sub_parser.add_parser("list", help="List operations on a classifier")
        self.add_path_argument(parser, required=True, help_text="Classifier path")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute operation list."""
        classifier = self._resolve_classifier(args.path)

        try:
            op_names = self._collect_operation_names(classifier)
            output = self._format_output(op_names, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote %d operations to: %s", len(op_names), args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to list operations in '{args.path}'")

    def _collect_operation_names(self, classifier: Any) -> List[str]:
        """Collect names of operations on a classifier."""
        operations = classifier.get_operations()
        return [op.get_name() for op in operations]

    def _format_output(self, op_names: List[str], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(op_names)
        elif format_type == "csv":
            table_rows = [[name] for name in op_names]
            return OutputFormatter.csv_format(["Name"], table_rows)
        else:
            table_rows = [[name] for name in op_names]
            return OutputFormatter.table(["Name"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class OperationViewAction(AbstractOperationAction):
    """View operation details.

    SWR_OP_00003: Operation View Command
    SWR_OP_00008: Multi-Format Output
    SWR_OP_00010: GUID Lookup Support
    """

    _VIEW_HEADERS = [
        "Name",
        "GUID",
        "Description",
        "Body",
        "IsAbstract",
        "IsStatic",
        "IsVirtual",
        "Returns",
        "Visibility",
        "Arguments",
        "MetaClass",
        "FullPath",
    ]
    _VIEW_KEYS = [
        "name",
        "guid",
        "description",
        "body",
        "isAbstract",
        "isStatic",
        "isVirtual",
        "returns",
        "visibility",
        "arguments",
        "metaClass",
        "fullPath",
    ]

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'view' subcommand and its arguments."""
        parser = sub_parser.add_parser("view", help="View operation details")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Operation GUID to view")
        parser.add_argument("--name", default=None, help="Operation name within classifier")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute operation view."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            operation = self._resolve_operation_by_guid(args.guid)
        else:
            classifier = self._resolve_classifier(args.path)
            operation = self._resolve_operation(classifier, args.name)

        try:
            data = self._collect_operation_data(operation)
            output = self._format_output(data, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote operation details to: %s", args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view operation '{args.name or args.guid}'")

    def _collect_operation_data(self, operation: Any) -> Dict[str, Any]:
        """Collect operation details into a data dictionary.

        Normalizes boolean flags to int for clean JSON round-trip.
        """
        returns = operation.get_returns()
        returns_name = returns.get_name() if returns is not None else ""
        arguments = operation.get_arguments()
        return {
            "name": operation.get_name(),
            "guid": operation.get_guid(),
            "description": operation.get_description(),
            "body": operation.get_body(),
            "isAbstract": int(operation.get_is_abstract()),
            "isStatic": int(operation.get_is_static()),
            "isVirtual": int(operation.get_is_virtual()),
            "returns": returns_name,
            "visibility": operation.get_visibility(),
            "arguments": [arg.get_name() for arg in arguments],
            "metaClass": operation.get_meta_class(),
            "fullPath": operation.get_full_path_name(),
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
                ["Body", data["body"]],
                ["IsAbstract", data["isAbstract"]],
                ["IsStatic", data["isStatic"]],
                ["IsVirtual", data["isVirtual"]],
                ["Returns", data["returns"]],
                ["Visibility", data["visibility"]],
                ["Arguments", ", ".join(data["arguments"])],
                ["MetaClass", data["metaClass"]],
                ["FullPath", data["fullPath"]],
            ]
            return OutputFormatter.table(["Property", "Value"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class OperationUpdateAction(AbstractOperationAction):
    """Update attributes of an existing operation.

    SWR_OP_00005: Operation Update Command
    SWR_OP_00007: External JSON File Support
    SWR_OP_00010: GUID Lookup Support
    SWR_OP_00011: Returns Type Resolution
    SWR_OP_00012: Boolean Flag Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "body",
        "isAbstract",
        "isStatic",
        "isVirtual",
        "returns",
        "visibility",
        "arguments",
        "description",
    }

    def __init__(self) -> None:
        """Initialize the 'update' action."""
        super().__init__(command_id="update")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'update' subcommand and its arguments."""
        parser = sub_parser.add_parser("update", help="Update attributes of an existing operation")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Operation GUID to update")
        parser.add_argument("--name", default=None, help="Operation name within classifier")
        parser.add_argument("--input", default=None, help="JSON file with operation attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute operation update."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            operation = self._resolve_operation_by_guid(args.guid)
            classifier = operation.get_owner()
        else:
            classifier = self._resolve_classifier(args.path)
            operation = self._resolve_operation(classifier, args.name)

        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)

        unknown = set(data.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        self._set_attributes(classifier, operation, data)

        self.logger.info("Successfully updated operation: %s", operation.get_name())

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_OP_00007: External JSON File Support
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

    def _set_attributes(self, classifier: Any, operation: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on operation (partial update)."""
        if "name" in attrs:
            operation.set_name(attrs["name"])
        if "body" in attrs:
            operation.set_body(attrs["body"])
        if "description" in attrs:
            operation.set_description(attrs["description"])
        if "visibility" in attrs:
            operation.set_visibility(attrs["visibility"])
        if "arguments" in attrs:
            operation.set_arguments(attrs["arguments"])
        if "isAbstract" in attrs:
            operation.set_is_abstract(1 if attrs["isAbstract"] else 0)
        if "isStatic" in attrs:
            operation.set_is_static(1 if attrs["isStatic"] else 0)
        if "isVirtual" in attrs:
            operation.set_is_virtual(1 if attrs["isVirtual"] else 0)
        if "returns" in attrs:
            type_name = attrs["returns"]
            owner = classifier.get_owner()
            target = owner.find_nested_classifier_recursive(type_name)
            if target is None:
                raise CliExecutionError(f"Returns type '{type_name}' not found")
            operation.set_returns(target)
