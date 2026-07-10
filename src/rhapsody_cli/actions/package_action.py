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
SWR_PKG_0016: Package Update Command
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
        self.add_path_argument(parser, required=False, help_text="Parent package path (optional; defaults to project root)")
        parser.add_argument("--input", default=None, help="JSON file with package attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package creation."""
        self.logger.info("Starting package creation...")
        input_data = args.input if args.input else args.attributes
        if not input_data:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        data = self._load_json_data(input_data)
        packages_data = data if isinstance(data, list) else [data]

        # Branch on whether path is provided (falsy = use project root)
        is_root = not args.path
        if is_root:
            self.logger.info("Creating packages at project root...")
            container = self._get_active_root()
        else:
            self.logger.info("Resolving parent path '%s'...", args.path)
            container = self._resolve_and_validate_package(args.path)

        created: List[str] = []
        errors: List[str] = []
        for pkg_attrs in packages_data:
            try:
                name = self._create_single_package(container, pkg_attrs, args.path, is_root=is_root)
                created.append(name)
            except CliExecutionError:
                raise
            except Exception as e:
                pkg_name = pkg_attrs.get("name", "unknown")
                self.logger.error("Failed to create package '%s': %s", pkg_name, e)
                errors.append(pkg_name)

        self._report_results(created, errors, len(packages_data))

    def _create_single_package(self, container: Any, pkg_attrs: Dict[str, Any], parent_path: Any, *, is_root: bool = False) -> str:
        """Create a single package and set its attributes. Returns the package name.

        Args:
            container: The parent container (RPProject for root, RPPackage for nested).
            pkg_attrs: Dictionary of package attributes.
            parent_path: The parent path (for reporting; can be None/empty for root).
            is_root: Whether creating at project root (uses addPackage) vs nested (uses addNestedPackage).
        """
        name = str(pkg_attrs.get("name", ""))
        if not name:
            raise CliExecutionError("'name' is required in attributes")

        unknown = set(pkg_attrs.keys()) - self.VALID_ATTRIBUTES
        if unknown:
            self.logger.warning("Skipping unknown attributes: %s", unknown)

        self.logger.info("Creating package '%s'...", name)

        # Check for duplicates before attempting creation
        self._check_package_not_exists(container, name, is_root)

        try:
            # Call the appropriate creation method based on location
            if is_root:
                package = container.addPackage(name)
            else:
                package = container.addNestedPackage(name)
        except Exception as e:
            error_str = str(e)
            # Check if error indicates the package already exists
            # COM error code -2147221495 (0x80040005) means "DISP_E_EXCEPTION" but typically indicates duplicate
            # Also check for common duplicate/already exists keywords
            if "already" in error_str.lower() or "duplicate" in error_str.lower() or "-2147221495" in error_str or "2147221495" in error_str:
                container_desc = "project root" if is_root else "parent package"
                raise CliExecutionError(f"Package '{name}' already exists in {container_desc}") from e
            # Generic error
            raise CliExecutionError(f"Failed to create package '{name}': {e}") from e

        # Set attributes if any are provided
        if len(pkg_attrs) > 1:  # More than just 'name'
            self.logger.info("Setting attributes for package '%s'...", name)
            try:
                self._set_attributes(package, pkg_attrs)
            except Exception as e:
                # Log that attributes couldn't be set but don't fail - package was created
                self.logger.warning("Failed to set attributes for package '%s': %s", name, e)

        # Build full_path without leading artifacts for root-created packages
        if is_root or not parent_path:
            full_path = name
        else:
            full_path = f"{parent_path}/{name}"

        self.logger.info("Created package: %s", full_path)
        return name

    def _check_package_not_exists(self, container: Any, name: str, is_root: bool) -> None:
        """Check if a package with the given name already exists in the container.

        Args:
            container: RPProject (for root) or RPPackage (for nested)
            name: Package name to check
            is_root: Whether checking at project root or nested

        Raises:
            CliExecutionError: If package with name already exists
        """
        self.logger.info("Checking if package '%s' already exists...", name)

        try:
            if is_root:
                existing_packages = container.getPackages()
                container_desc = "project root"
            else:
                existing_packages = container.getNestedPackages()
                parent_name = container.getName()
                container_desc = f"package '{parent_name}'"

            # Search for duplicate by name
            for pkg in existing_packages:
                pkg_name = pkg.getName()
                if pkg_name == name:
                    raise CliExecutionError(f"Package '{name}' already exists in {container_desc}")
        except CliExecutionError:
            raise
        except Exception as e:
            # If there's an error checking for duplicates, log it but continue
            # The creation attempt itself will fail more gracefully if package exists
            self.logger.debug("Could not enumerate existing packages to check for duplicates: %s", e)

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} packages; all failed")
        if created:
            self.logger.info("Successfully created %d package%s", len(created), "s" if len(created) != 1 else "")
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
        self.logger.info("Starting package deletion...")
        self.logger.info("Resolving package path '%s'...", args.path)
        package = self._resolve_and_validate_package(args.path)

        try:
            self.logger.info("Deleting package '%s'...", args.path)
            package.deleteFromProject()
            self.logger.info("Successfully deleted package '%s'", args.path)
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
        self.logger.info("Starting package view operation...")
        self.logger.info("Resolving package path '%s'...", args.path)
        package = self._resolve_and_validate_package(args.path)

        try:
            self.logger.info("Retrieving package details...")
            data = self._collect_package_data(package)
            output = self._format_output(data, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Writing output to file '%s'", args.output)
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
        self.logger.info("Starting package list operation...")
        self.logger.info("Resolving package path '%s'...", args.path)
        package = self._resolve_and_validate_package(args.path)

        try:
            self.logger.info("Listing nested packages...")
            package_names = self._collect_nested_package_names(package)
            if package_names:
                self.logger.info("Found %d nested package%s", len(package_names), "s" if len(package_names) != 1 else "")
            else:
                self.logger.info("No nested packages found")
            output = self._format_output(package_names, args.format)

            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Writing output to file '%s'", args.output)
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


class PackageUpdateAction(AbstractPackageAction):
    """Update attributes of an existing package.

    SWR_PKG_0016: Package Update Command
    SWR_PKG_0006: External JSON File Support
    SWR_PKG_0007: Stereotype and Tag Support
    """

    VALID_ATTRIBUTES = {
        "name",
        "description",
        "display_name",
        "stereotypes",
        "tags",
        "properties",
    }

    def __init__(self) -> None:
        """Initialize the 'update' action."""
        super().__init__(command_id="update")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        """Register the 'update' subcommand and its arguments."""
        parser = sub_parser.add_parser("update", help="Update attributes of an existing package")
        self.add_path_argument(parser, required=False, help_text="Package path to update")
        parser.add_argument("--guid", default=None, help="GUID of the package to update")
        parser.add_argument("--input", default=None, help="JSON file with package attributes")
        parser.add_argument("attributes", nargs="?", default=None, help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def _resolve_element_by_guid(self, guid: str) -> Any:
        """Resolve element by GUID and validate it's a Package.

        Args:
            guid: GUID of the element to resolve.

        Returns:
            Package COM object.

        Raises:
            CliExecutionError: If GUID not found or element is not a Package.
        """
        project = self._get_active_root()
        element = project.findElementByGUID(guid)
        if element is None:
            raise CliExecutionError(f"GUID '{guid}' not found")
        meta_class = element.getMetaClass()
        if meta_class != "Package":
            raise CliExecutionError(f"GUID '{guid}' does not resolve to a Package (found {meta_class})")
        return element

    def _load_json_data(self, args: Any) -> Dict[str, Any]:
        """Load JSON data from inline string or file.

        SWR_PKG_0006: External JSON File Support

        Args:
            args: Parsed argparse.Namespace with `input` and `attributes`.

        Returns:
            Dictionary of package attributes (empty if neither provided).
        """
        if args.input:
            try:
                with open(args.input, encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                raise CliExecutionError(f"File not found: {args.input}") from None
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}") from e
        elif args.attributes:
            data_str = args.attributes.strip()
            if data_str.startswith("{"):
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}") from e
            else:
                try:
                    with open(data_str, encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    raise CliExecutionError(f"File not found: {data_str}") from None
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}") from e
        return {}

    def _set_attributes(self, package: Any, data: Dict[str, Any]) -> None:
        """Set validated attributes on package (partial update).

        Only fields present in `data` are modified; unknown fields are
        skipped with a warning log.

        Args:
            package: Package COM object to update.
            data: Dictionary of attributes to apply.
        """
        for key, value in data.items():
            if key not in self.VALID_ATTRIBUTES:
                self.logger.warning("Skipping unknown attribute: %s", key)
                continue
            if key == "name":
                package.setName(value)
            elif key == "description":
                package.setDescription(value)
            elif key == "display_name":
                package.setDisplayName(value)
            elif key == "stereotypes":
                for stereotype in value:
                    package.addStereotype(stereotype, "Package")
            elif key == "tags":
                for tag_key, tag_value in value.items():
                    package.setPropertyValue(tag_key, tag_value)
            elif key == "properties":
                for prop_key, prop_value in value.items():
                    package.setPropertyValue(prop_key, prop_value)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute package update.

        Args:
            args: Parsed argparse.Namespace with path/guid and attribute data.
        """
        self.logger.info("Starting package update...")
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid is required")
        if args.guid:
            self.logger.info("Resolving package by GUID '%s'...", args.guid)
            package = self._resolve_element_by_guid(args.guid)
        else:
            self.logger.info("Resolving package path '%s'...", args.path)
            package = self._resolve_and_validate_package(args.path)
        data = self._load_json_data(args)
        self._set_attributes(package, data)
        self.logger.info("Successfully updated package: %s", package.getName())
