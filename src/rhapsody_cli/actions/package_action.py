"""Package-related CLI actions.

SWR_PKG_0001: Package Create Command
SWR_PKG_0002: Package Delete Command
SWR_PKG_0003: Package View Command
SWR_PKG_0004: Package List Command
SWR_PKG_0005: Path Validation
SWR_PKG_0006: External JSON File Support
SWR_PKG_0007: Stereotype and Tag Support
SWR_PKG_0008: Multi-Format Output
SWR_PKG_0009: View-to-Create Workflow
SWR_PKG_0010: Error Handling and Logging
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


class AbstractPackageAction(ElementManagementAction):
    """Base class for package actions with common path validation.

    SWR_PKG_0005: Path Validation
    SWR_PKG_0010: Error Handling and Logging
    """

    def _resolve_and_validate_package(self, path: str) -> Any:
        """Resolve path and validate it's a Package element.

        Args:
            path: Package path to resolve.

        Returns:
            Package COM object.

        Raises:
            CliExecutionError: If path not found or not a Package.
        """
        root = self._get_active_root()
        container = self._resolve_container_or_element(root, path, resolve_element=False, operation=f"resolve package path '{path}'")

        meta_class = container.getMetaClass()
        if meta_class != "Package":
            raise CliExecutionError(f"Path '{path}' does not resolve to a Package (found {meta_class})")

        return container


class PackageCreateAction(AbstractPackageAction):
    """Create one or multiple packages.

    SWR_PKG_0001: Package Create Command
    SWR_PKG_0006: External JSON File Support
    SWR_PKG_0007: Stereotype and Tag Support
    SWR_PKG_0009: View-to-Create Workflow
    """

    VALID_ATTRIBUTES = {
        "name",
        "description",
        "description_html",
        "description_rtf",
        "display_name",
        "display_name_rtf",
        "properties",
        "stereotypes",
        "tags",
    }

    def __init__(self) -> None:
        """Initialize the 'create' action."""
        super().__init__(command_id="create")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'create' subcommand and its arguments."""
        parser = sub_parser.add_parser("create", help="Create a package")
        self.add_path_argument(parser, required=True, help_text="Parent package path")
        parser.add_argument("--input", default=None, help="JSON file with package attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package creation."""
        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)
        packages_data = data if isinstance(data, list) else [data]

        container = self._resolve_and_validate_package(args.path)

        created: List[str] = []
        errors: List[str] = []
        for pkg_attrs in packages_data:
            try:
                name = self._create_single_package(container, pkg_attrs, args.path)
                created.append(name)
            except CliExecutionError:
                raise
            except Exception as e:
                pkg_name = pkg_attrs.get("name", "unknown")
                self.logger.error("Failed to create package '%s': %s", pkg_name, e)
                errors.append(pkg_name)

        self._report_results(created, errors, len(packages_data))

    def _create_single_package(self, container: Any, pkg_attrs: Dict[str, Any], parent_path: str) -> str:
        """Create a single package and set its attributes. Returns the package name."""
        name = str(pkg_attrs.get("name", ""))
        if not name:
            raise CliExecutionError("'name' is required in attributes")

        unknown = set(pkg_attrs.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        package = container.addNestedPackage(name)
        self._set_attributes(package, pkg_attrs)

        full_path = f"{parent_path}/{name}"
        self.logger.info("Created package: %s", full_path)
        return name

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} packages; all failed")
        if errors:
            self.logger.info("Created %d/%d packages with %d error(s)", len(created), total, len(errors))

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file.

        SWR_PKG_0006: External JSON File Support
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

    def _set_attributes(self, package: Any, attrs: Dict[str, Any]) -> None:
        """Set validated attributes on package."""
        self._set_basic_attributes(package, attrs)
        self._set_properties(package, attrs)
        self._set_stereotypes(package, attrs)
        self._set_tags(package, attrs)

    def _set_basic_attributes(self, package: Any, attrs: Dict[str, Any]) -> None:
        """Set basic attributes."""
        if "description" in attrs:
            package.setDescription(attrs["description"])
        if "description_html" in attrs:
            package.setDescriptionHTML(attrs["description_html"])
        if "description_rtf" in attrs:
            package.setDescriptionRTF(attrs["description_rtf"])
        if "display_name" in attrs:
            package.setDisplayName(attrs["display_name"])
        if "display_name_rtf" in attrs:
            package.setDisplayNameRTF(attrs["display_name_rtf"])

    def _set_properties(self, package: Any, attrs: Dict[str, Any]) -> None:
        """Set custom properties."""
        if "properties" in attrs:
            for key, val in attrs["properties"].items():
                package.setPropertyValue(key, val)

    def _set_stereotypes(self, package: Any, attrs: Dict[str, Any]) -> None:
        """Apply stereotypes."""
        if "stereotypes" in attrs:
            for stereotype in attrs["stereotypes"]:
                package.addStereotype(stereotype, "Package")

    def _set_tags(self, package: Any, attrs: Dict[str, Any]) -> None:
        """Set tags."""
        if "tags" in attrs:
            for key, val in attrs["tags"].items():
                package.setPropertyValue(key, val)


class PackageDeleteAction(AbstractPackageAction):
    """Delete a package.

    SWR_PKG_0002: Package Delete Command
    """

    def __init__(self) -> None:
        """Initialize the 'delete' action."""
        super().__init__(command_id="delete")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'delete' subcommand and its arguments."""
        parser = sub_parser.add_parser("delete", help="Delete a package")
        self.add_path_argument(parser, required=True, help_text="Package path to delete")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package deletion."""
        package = self._resolve_and_validate_package(args.path)

        try:
            package.deleteFromProject()
            self.logger.info("Deleted package: %s", args.path)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete package '{args.path}'")


class PackageViewAction(AbstractPackageAction):
    """View package details.

    SWR_PKG_0003: Package View Command
    SWR_PKG_0008: Multi-Format Output
    """

    _VIEW_HEADERS = ["Name", "GUID", "Description", "MetaClass", "FullPath"]
    _VIEW_KEYS = ["name", "guid", "description", "metaClass", "fullPath"]

    def __init__(self) -> None:
        """Initialize the 'view' action."""
        super().__init__(command_id="view")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'view' subcommand and its arguments."""
        parser = sub_parser.add_parser("view", help="View package details")
        self.add_path_argument(parser, required=True, help_text="Package path to view")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package view."""
        package = self._resolve_and_validate_package(args.path)

        try:
            data = self._collect_package_data(package)
            output = self._format_output(data, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote package details to: %s", args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to view package '{args.path}'")

    def _collect_package_data(self, package: Any) -> Dict[str, str]:
        """Collect package details into a data dictionary."""
        return {
            "name": package.getName(),
            "guid": package.getGUID(),
            "description": package.getDescription(),
            "metaClass": package.getMetaClass(),
            "fullPath": package.getFullPathName(),
        }

    def _format_output(self, data: Dict[str, str], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(data)
        elif format_type == "csv":
            data_row = [data[key] for key in self._VIEW_KEYS]
            return OutputFormatter.csv_format(self._VIEW_HEADERS, [data_row])
        else:
            table_rows = [[k, v] for k, v in data.items()]
            return OutputFormatter.table(["Property", "Value"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e


class PackageListAction(AbstractPackageAction):
    """List nested packages.

    SWR_PKG_0004: Package List Command
    SWR_PKG_0008: Multi-Format Output
    """

    def __init__(self) -> None:
        """Initialize the 'list' action."""
        super().__init__(command_id="list")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'list' subcommand and its arguments."""
        parser = sub_parser.add_parser("list", help="List nested packages")
        self.add_path_argument(parser, required=True, help_text="Package path")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", default=None, help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package list."""
        package = self._resolve_and_validate_package(args.path)

        try:
            package_names = self._collect_nested_package_names(package)
            output = self._format_output(package_names, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote %d packages to: %s", len(package_names), args.output)
            else:
                print(output)
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, f"Failed to list packages in '{args.path}'")

    def _collect_nested_package_names(self, package: Any) -> List[str]:
        """Collect names of nested packages."""
        nested_packages = package.getNestedPackages()
        return [pkg.getName() for pkg in nested_packages]

    def _format_output(self, package_names: List[str], format_type: str) -> str:
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(package_names)
        elif format_type == "csv":
            table_rows = [[name] for name in package_names]
            return OutputFormatter.csv_format(["Name"], table_rows)
        else:
            table_rows = [[name] for name in package_names]
            return OutputFormatter.table(["Name"], table_rows)

    def _write_to_file(self, file_path: str, content: str) -> None:
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}") from e
