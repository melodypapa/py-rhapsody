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
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from rhapsody_cli.actions.abstract_action import ElementManagementAction
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
        container = self._resolve_container_or_element(
            root, path, resolve_element=False, operation=f"resolve package path '{path}'"
        )

        meta_class = container.getMetaClass()
        if meta_class not in self._PACKAGE_META_CLASSES:
            raise CliExecutionError(
                f"Path '{path}' does not resolve to a Package or Project (found {meta_class})"
            )

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
        element = self._resolve_container_or_element(
            root, path, resolve_element=True, operation=f"resolve class path '{path}'"
        )

        meta_class = element.getMetaClass()
        if meta_class != "Class":
            raise CliExecutionError(
                f"Path '{path}' does not resolve to a Class (found {meta_class})"
            )

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
            element = project.findElementByGUID(guid)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to locate class by GUID '{guid}'")

        if element is None:
            raise CliExecutionError(f"No element found with GUID '{guid}'")

        meta_class = element.getMetaClass()
        if meta_class != "Class":
            raise CliExecutionError(
                f"GUID '{guid}' does not resolve to a Class (found {meta_class})"
            )

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

        cls = parent.addClass(name)
        self._set_attributes(parent, cls, cls_attrs)

        full_path = f"{parent_path}/{name}"
        self.logger.info("Created class: %s", full_path)
        return name

    def _report_results(self, created: List[str], errors: List[str], total: int) -> None:
        """Log summary of creation results."""
        if errors and not created:
            raise CliExecutionError(f"Created 0/{total} classes; all failed")
        if errors:
            self.logger.info(
                "Created %d/%d classes with %d error(s)", len(created), total, len(errors)
            )

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
            cls.setDescription(attrs["description"])

    def _set_boolean_flags(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set boolean flags isAbstract, isFinal, isActive.

        SWR_CLS_00012: Boolean Flag Support
        """
        if "isAbstract" in attrs:
            cls.setIsAbstract(1 if attrs["isAbstract"] else 0)
        if "isFinal" in attrs:
            cls.setIsFinal(1 if attrs["isFinal"] else 0)
        if "isActive" in attrs:
            cls.setIsActive(1 if attrs["isActive"] else 0)

    def _set_properties(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Set custom properties (tags)."""
        if "tags" in attrs:
            for key, val in attrs["tags"].items():
                cls.setPropertyValue(key, val)

    def _set_stereotypes(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Apply stereotypes."""
        if "stereotypes" in attrs:
            for stereotype in attrs["stereotypes"]:
                cls.addStereotype(stereotype, "Class")

    def _set_operations(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add operations."""
        if "operations" in attrs:
            for op_name in attrs["operations"]:
                cls.addOperation(op_name)

    def _set_attributes_list(self, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add attributes."""
        if "attributes" in attrs:
            for attr_name in attrs["attributes"]:
                cls.addAttribute(attr_name)

    def _set_superclasses(self, parent: Any, cls: Any, attrs: Dict[str, Any]) -> None:
        """Add generalization relationships to superclasses.

        SWR_CLS_00001: resolves superclass names via parent.findNestedClassifierRecursive(name).
        """
        if "superclasses" in attrs:
            for name in attrs["superclasses"]:
                target = parent.findNestedClassifierRecursive(name)
                if target is None:
                    raise CliExecutionError(
                        f"Superclass '{name}' not found in package"
                    )
                cls.addGeneralization(target)