"""Attribute-related CLI actions.

SWR_ATTR_00001: Attribute Create Command
SWR_ATTR_00002: Attribute Delete Command
SWR_ATTR_00003: Attribute View Command
SWR_ATTR_00004: Attribute List Command
SWR_ATTR_00005: Attribute Update Command
SWR_ATTR_00006: Path and Name Validation
SWR_ATTR_00007: External JSON File Support
SWR_ATTR_00008: Multi-Format Output
SWR_ATTR_00009: Error Handling and Logging
SWR_ATTR_00010: GUID Lookup Support
SWR_ATTR_00011: Type Resolution
SWR_ATTR_00012: IsStatic Flag Support
SWR_ATTR_00013: Bulk Creation Support
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


class AbstractAttributeAction(ElementManagementAction):
    """Base class for attribute actions with common path, name and GUID validation.

    SWR_ATTR_00006: Path and Name Validation
    SWR_ATTR_00009: Error Handling and Logging
    SWR_ATTR_00010: GUID Lookup Support
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

    def _resolve_attribute(self, classifier: Any, name: str) -> Any:
        """Find an attribute by name within a classifier.

        Args:
            classifier: The parent classifier COM object.
            name: The attribute name to find.

        Returns:
            Attribute COM object.

        Raises:
            CliExecutionError: If attribute not found.
        """
        attribute = classifier.find_attribute(name)
        if attribute is None:
            raise CliExecutionError(f"Attribute '{name}' not found in classifier")
        return attribute

    def _resolve_attribute_by_guid(self, guid: str) -> Any:
        """Locate an attribute by GUID and validate it's an Attribute element.

        SWR_ATTR_00010: GUID Lookup Support

        Args:
            guid: GUID string in format 12345678-1234-1234-1234-123456789abc.

        Returns:
            Attribute COM object.

        Raises:
            CliExecutionError: If GUID not found or element is not an Attribute.
        """
        project = self._get_active_project()
        try:
            element = project.find_element_by_guid(guid)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to locate attribute by GUID '{guid}'")

        if element is None:
            raise CliExecutionError(f"No element found with GUID '{guid}'")

        meta_class = element.get_meta_class()
        if meta_class != "Attribute":
            raise CliExecutionError(f"GUID '{guid}' does not resolve to an Attribute (found {meta_class})")

        return element


class AttributeCreateAction(AbstractAttributeAction):
    """Create one or multiple attributes.

    SWR_ATTR_00001: Attribute Create Command
    SWR_ATTR_00007: External JSON File Support
    SWR_ATTR_00011: Type Resolution
    SWR_ATTR_00012: IsStatic Flag Support
    SWR_ATTR_00013: Bulk Creation Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "type",
        "defaultValue",
        "multiplicity",
        "isStatic",
        "visibility",
        "declaration",
        "description",
    }

    def __init__(self) -> None:
        """Initialize the 'create' action."""
        super().__init__(command_id="create")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'create' subcommand and its arguments."""
        parser = sub_parser.add_parser("create", help="Create an attribute")
        self.add_path_argument(parser, required=True, help_text="Parent classifier path")
        parser.add_argument("--input", default=None, help="JSON file with attribute attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute attribute creation."""
        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)
        attrs_data = data if isinstance(data, list) else [data]

        classifier = self._resolve_classifier(args.path)

        created: List[str] = []
        errors: List[str] = []
        for attr_attrs in attrs_data:
            try:
                name = self._create_single_attribute(classifier, attr_attrs, args.path)
                created.append(name)
            except CliExecutionError:
                raise
            except Exception as e:
                attr_name = attr_attrs.get("name", "unknown")
                self.logger.error("Failed to create attribute '%s': %s", attr_name, e)
                errors.append(attr_name)

        self._report_results(created, errors, len(attrs_data))

    def _create_single_attribute(self, classifier: Any, attr_attrs: Dict[str, Any], parent_path: str) -> str:
        """Create a single attribute and set its attributes. Returns the attribute name."""
        name = str(attr_attrs.get("name", ""))
        if not name:
            raise CliExecutionError("'name' is required in attributes")

        unknown = set(attr_attrs.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        attribute = classifier.add_attribute(name)
        self._set_attributes(classifier, attribute, attr_attrs)

        full_path = f"{parent_path}/{name}"
        self.logger.info("Created attribute: %s", full_path)
        return name

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} attributes; all failed")
        if errors:
            self.logger.info("Created %d/%d attributes with %d error(s)", len(created), total, len(errors))

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_ATTR_00007: External JSON File Support
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

    def _set_attributes(self, classifier: Any, attribute: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on attribute."""
        if "name" in attrs:
            attribute.set_name(attrs["name"])
        if "defaultValue" in attrs:
            attribute.set_default_value(attrs["defaultValue"])
        if "multiplicity" in attrs:
            attribute.set_multiplicity(attrs["multiplicity"])
        if "visibility" in attrs:
            attribute.set_visibility(attrs["visibility"])
        if "declaration" in attrs:
            attribute.set_declaration(attrs["declaration"])
        if "description" in attrs:
            attribute.set_description(attrs["description"])
        self._set_boolean_flags(attribute, attrs)
        self._set_type(classifier, attribute, attrs)

    def _set_boolean_flags(self, attribute: Any, attrs: Dict[str, Any]) -> None:
        """Set boolean flag isStatic.

        SWR_ATTR_00012: IsStatic Flag Support
        """
        if "isStatic" in attrs:
            attribute.set_is_static(1 if attrs["isStatic"] else 0)

    def _set_type(self, classifier: Any, attribute: Any, attrs: Dict[str, Any]) -> None:
        """Resolve and set the attribute type.

        SWR_ATTR_00011: Type Resolution
        """
        if "type" in attrs:
            type_name = attrs["type"]
            owner = classifier.get_owner()
            target = owner.find_nested_classifier_recursive(type_name)
            if target is None:
                raise CliExecutionError(f"Type '{type_name}' not found")
            attribute.set_type(target)


class AttributeDeleteAction(AbstractAttributeAction):
    """Delete an attribute.

    SWR_ATTR_00002: Attribute Delete Command
    SWR_ATTR_00010: GUID Lookup Support
    """

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'delete' subcommand and its arguments."""
        parser = sub_parser.add_parser("delete", help="Delete an attribute")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Attribute GUID to delete")
        parser.add_argument("--name", default=None, help="Attribute name within classifier")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute attribute deletion."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            attribute = self._resolve_attribute_by_guid(args.guid)
            classifier = attribute.get_owner()
            label = f"GUID '{args.guid}'"
        else:
            classifier = self._resolve_classifier(args.path)
            attribute = self._resolve_attribute(classifier, args.name)
            label = args.name

        try:
            classifier.delete_attribute(attribute)
            self.logger.info("Deleted attribute: %s", label)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete attribute '{label}'")


class AttributeListAction(AbstractAttributeAction):
    """List attributes on a classifier.

    SWR_ATTR_00004: Attribute List Command
    SWR_ATTR_00008: Multi-Format Output
    """

    def __init__(self) -> None:
        """Initialize the 'list' action."""
        super().__init__(command_id="list")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'list' subcommand and its arguments."""
        parser = sub_parser.add_parser("list", help="List attributes on a classifier")
        self.add_path_argument(parser, required=True, help_text="Classifier path")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute attribute list."""
        classifier = self._resolve_classifier(args.path)

        try:
            attr_names = self._collect_attribute_names(classifier)
            output = self._format_output(attr_names, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote %d attributes to: %s", len(attr_names), args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to list attributes in '{args.path}'")

    def _collect_attribute_names(self, classifier: Any) -> List[str]:
        """Collect names of attributes on a classifier."""
        attributes = classifier.get_attributes()
        return [attr.get_name() for attr in attributes]

    def _format_output(self, attr_names: List[str], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(attr_names)
        elif format_type == "csv":
            table_rows = [[name] for name in attr_names]
            return OutputFormatter.csv_format(["Name"], table_rows)
        else:
            table_rows = [[name] for name in attr_names]
            return OutputFormatter.table(["Name"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class AttributeViewAction(AbstractAttributeAction):
    """View attribute details.

    SWR_ATTR_00003: Attribute View Command
    SWR_ATTR_00008: Multi-Format Output
    SWR_ATTR_00010: GUID Lookup Support
    """

    _VIEW_HEADERS = [
        "Name",
        "GUID",
        "Description",
        "Type",
        "DefaultValue",
        "Multiplicity",
        "IsStatic",
        "Visibility",
        "Declaration",
        "MetaClass",
        "FullPath",
    ]
    _VIEW_KEYS = [
        "name",
        "guid",
        "description",
        "type",
        "defaultValue",
        "multiplicity",
        "isStatic",
        "visibility",
        "declaration",
        "metaClass",
        "fullPath",
    ]

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'view' subcommand and its arguments."""
        parser = sub_parser.add_parser("view", help="View attribute details")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Attribute GUID to view")
        parser.add_argument("--name", default=None, help="Attribute name within classifier")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute attribute view."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            attribute = self._resolve_attribute_by_guid(args.guid)
        else:
            classifier = self._resolve_classifier(args.path)
            attribute = self._resolve_attribute(classifier, args.name)

        try:
            data = self._collect_attribute_data(attribute)
            output = self._format_output(data, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote attribute details to: %s", args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view attribute '{args.name or args.guid}'")

    def _collect_attribute_data(self, attribute: Any) -> Dict[str, Any]:
        """Collect attribute details into a data dictionary.

        Normalizes boolean flags to int for clean JSON round-trip.
        """
        attr_type = attribute.get_type()
        type_name = attr_type.get_name() if attr_type is not None else ""
        return {
            "name": attribute.get_name(),
            "guid": attribute.get_guid(),
            "description": attribute.get_description(),
            "type": type_name,
            "defaultValue": attribute.get_default_value(),
            "multiplicity": attribute.get_multiplicity(),
            "isStatic": int(attribute.get_is_static()),
            "visibility": attribute.get_visibility(),
            "declaration": attribute.get_declaration(),
            "metaClass": attribute.get_meta_class(),
            "fullPath": attribute.get_full_path_name(),
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
                ["Type", data["type"]],
                ["DefaultValue", data["defaultValue"]],
                ["Multiplicity", data["multiplicity"]],
                ["IsStatic", data["isStatic"]],
                ["Visibility", data["visibility"]],
                ["Declaration", data["declaration"]],
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


class AttributeUpdateAction(AbstractAttributeAction):
    """Update attributes of an existing attribute.

    SWR_ATTR_00005: Attribute Update Command
    SWR_ATTR_00007: External JSON File Support
    SWR_ATTR_00010: GUID Lookup Support
    SWR_ATTR_00011: Type Resolution
    SWR_ATTR_00012: IsStatic Flag Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "type",
        "defaultValue",
        "multiplicity",
        "isStatic",
        "visibility",
        "declaration",
        "description",
    }

    def __init__(self) -> None:
        """Initialize the 'update' action."""
        super().__init__(command_id="update")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'update' subcommand and its arguments."""
        parser = sub_parser.add_parser("update", help="Update attributes of an existing attribute")
        self.add_path_argument(parser, required=False, help_text="Parent classifier path")
        parser.add_argument("--guid", default=None, help="Attribute GUID to update")
        parser.add_argument("--name", default=None, help="Attribute name within classifier")
        parser.add_argument("--input", default=None, help="JSON file with attribute attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute attribute update."""
        has_path_name = args.path and args.name
        has_guid = args.guid is not None

        if has_path_name and has_guid:
            raise CliExecutionError("Only one of --path + --name or --guid may be specified")
        if not has_path_name and not has_guid:
            raise CliExecutionError("Either --path + --name or --guid must be specified")

        if has_guid:
            attribute = self._resolve_attribute_by_guid(args.guid)
            classifier = attribute.get_owner()
        else:
            classifier = self._resolve_classifier(args.path)
            attribute = self._resolve_attribute(classifier, args.name)

        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)

        unknown = set(data.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        self._set_attributes(classifier, attribute, data)

        self.logger.info("Successfully updated attribute: %s", attribute.get_name())

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_ATTR_00007: External JSON File Support
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

    def _set_attributes(self, classifier: Any, attribute: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on attribute (partial update)."""
        if "name" in attrs:
            attribute.set_name(attrs["name"])
        if "defaultValue" in attrs:
            attribute.set_default_value(attrs["defaultValue"])
        if "multiplicity" in attrs:
            attribute.set_multiplicity(attrs["multiplicity"])
        if "visibility" in attrs:
            attribute.set_visibility(attrs["visibility"])
        if "declaration" in attrs:
            attribute.set_declaration(attrs["declaration"])
        if "description" in attrs:
            attribute.set_description(attrs["description"])
        if "isStatic" in attrs:
            attribute.set_is_static(1 if attrs["isStatic"] else 0)
        if "type" in attrs:
            type_name = attrs["type"]
            owner = classifier.get_owner()
            target = owner.find_nested_classifier_recursive(type_name)
            if target is None:
                raise CliExecutionError(f"Type '{type_name}' not found")
            attribute.set_type(target)
