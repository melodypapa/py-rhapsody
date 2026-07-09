# Package Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `package` command group with create, delete, view, and list subcommands for managing Rhapsody packages via CLI.

**Architecture:** Follows existing element/project command patterns. Uses AbstractPackageAction base class for common path validation and error handling. Supports bulk operations, external JSON input, and multi-format output.

**Tech Stack:** Python 3.8+, argparse CLI framework, Rhapsody COM API wrapper, pytest for testing.

## Global Constraints

- Python version: 3.8+
- All code must pass: ruff, mypy, pytest
- All tests must pass before commit
- Follow existing CLI patterns (ElementCommand, ProjectCommand)
- Use existing infrastructure: PathResolver, OutputFormatter, logging
- TDD approach: write test first, then implementation

---

## File Structure

**New files:**
- `src/rhapsody_cli/commands/package_command.py` - Command dispatcher
- `src/rhapsody_cli/actions/package_action.py` - 5 Action classes
- `tests/unit/commands/test_package_command.py` - Command tests
- `tests/unit/actions/test_package_action.py` - Action tests
- `docs/user-guide/package-command.rst` - User documentation

**Modified files:**
- `src/rhapsody_cli/cli/main.py` - Register package command
- `docs/requirements.rst` - Add SW requirements
- `docs/api-reference/actions.rst` - Add API docs

---

## Phase 1: SW Requirements Documentation

### Task 1: Document Package Command Requirements

**Files:**
- Create: `docs/requirements/swr_pkg_requirements.md`

**Requirement IDs to add:**

Create `docs/requirements/swr_pkg_requirements.md`:

```markdown
# Software Requirements - Package Command

**Category:** Package Command
**Prefix:** SWR_PKG
**Source:** Extracted from spec
**Last Validated:** 2026-07-09

---

## SWR_PKG_0001: Package Create Command

**ID:** SWR_PKG_0001
**Title:** package create command creates one or multiple packages
**Status:** Planned
**Priority:** High
**Description:**
The CLI 
- SHALL provide a `package create` command to create one or multiple packages.
- SHALL accept `--path <parent-path>` argument (required)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path resolves to Package element
- SHALL create nested packages under parent
- SHALL set validated attributes (name, description, properties, stereotypes, tags)
- SHALL skip unknown attributes with warning log
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction
**Last Changed:** 2026-07-09

---

## SWR_PKG_0002: Package Delete Command

**ID:** SWR_PKG_0002
**Title:** package delete command deletes a package
**Status:** Planned
**Priority:** High
**Description:**
The CLI 
- SHALL provide a `package delete` command to delete a package.
- SHALL accept `--path <package-path>` argument (required)
- SHALL validate path resolves to Package element
- SHALL delete package and all contents
- SHALL log deletion to stderr
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageDeleteAction
**Last Changed:** 2026-07-09

---

## SWR_PKG_0003: Package View Command

**ID:** SWR_PKG_0003
**Title:** package view command displays package details
**Status:** Planned
**Priority:** High
**Description:**
The CLI 
- SHALL provide a `package view` command to view package details.
- SHALL accept `--path <package-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display package properties: name, GUID, description, metaClass, fullPath
- SHALL support table, JSON, and CSV output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageViewAction
**Last Changed:** 2026-07-09

---

## SWR_PKG_0004: Package List Command

**ID:** SWR_PKG_0004
**Title:** package list command lists nested packages
**Status:** Planned
**Priority:** High
**Description:**
The CLI 
- SHALL provide a `package list` command to list nested packages.
- SHALL accept `--path <package-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list all nested packages under parent
- SHALL support table, JSON, and CSV output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageListAction
**Last Changed:** 2026-07-09

---

## SWR_PKG_0005: Path Validation

**ID:** SWR_PKG_0005
**Title:** All package commands validate path before execution
**Status:** Planned
**Priority:** High
**Description:**
All package commands 
- SHALL validate path before execution.
- SHALL resolve path using PathResolver
- SHALL verify element at path is Package type (metaClass == "Package")
- SHALL raise error if path not found
- SHALL raise error if path not Package
**Implementation:** src/rhapsody_cli/actions/package_action.py:AbstractPackageAction._resolve_and_validate_package
**Last Changed:** 2026-07-09

---

## SWR_PKG_0006: External JSON File Support

**ID:** SWR_PKG_0006
**Title:** Package create supports external JSON files
**Status:** Planned
**Priority:** Medium
**Description:**
Package create command 
- SHALL support external JSON files.
- SHALL accept `--input <file>` argument
- SHALL accept file path as positional argument
- SHALL detect inline JSON vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL raise error if file not found
- SHALL raise error if JSON invalid
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction._load_json_data
**Last Changed:** 2026-07-09

---

## SWR_PKG_0007: Stereotype and Tag Support

**ID:** SWR_PKG_0007
**Title:** Package create supports stereotypes and tags
**Status:** Planned
**Priority:** Medium
**Description:**
Package create command 
- SHALL support stereotypes and tags.
- SHALL accept `stereotypes` array in JSON
- SHALL apply stereotypes via addStereotype() method
- SHALL accept `tags` object in JSON
- SHALL set tags via setPropertyValue() method
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction._set_stereotypes,_set_tags
**Last Changed:** 2026-07-09

---

## SWR_PKG_0008: Multi-Format Output

**ID:** SWR_PKG_0008
**Title:** Package view and list support multiple output formats
**Status:** Planned
**Priority:** Medium
**Description:**
Package view and list commands 
- SHALL support multiple output formats.
- SHALL support table format (default, human-readable)
- SHALL support JSON format (machine-parsable)
- SHALL support CSV format (spreadsheet-friendly)
- SHALL use horizontal layout for CSV (header row + data rows)
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageViewAction._format_output,PackageListAction._format_output
**Last Changed:** 2026-07-09

---

## SWR_PKG_0009: View-to-Create Workflow

**ID:** SWR_PKG_0009
**Title:** Package view JSON output reusable as package create input
**Status:** Planned
**Priority:** Medium
**Description:**
Package view JSON output 
- SHALL be reusable as package create input.
- SHALL ignore unknown fields (guid, metaClass, fullPath) in create
- SHALL only use validated attributes from view output
- SHALL enable package cloning workflow
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction.VALID_ATTRIBUTES
**Last Changed:** 2026-07-09

---

## SWR_PKG_0010: Error Handling and Logging

**ID:** SWR_PKG_0010
**Title:** All package actions follow consistent error handling patterns
**Status:** Planned
**Priority:** High
**Description:**
All package actions 
- SHALL follow consistent error handling patterns.
- SHALL use _handle_execution_error() for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/package_action.py:AbstractPackageAction
**Last Changed:** 2026-07-09
```

- [ ] **Step 1: Create requirements file**

Create `docs/requirements/swr_pkg_requirements.md` with the content above.

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_pkg_requirements.md
git commit -m "docs: Add SW requirements for package command (SWR_PKG_0001-00010)"
```

---

## Phase 2: AbstractPackageAction Base Class

### Task 2: Create AbstractPackageAction Base Class

**Files:**
- Create: `src/rhapsody_cli/actions/package_action.py`
- Test: `tests/unit/actions/test_package_action.py`

**Interfaces:**
- Produces: `AbstractPackageAction` class with:
  - `_resolve_and_validate_package(path)` method
  - `add_path_argument(parser)` method
  - Inherits from `ElementManagementAction`

- [ ] **Step 1: Write test for AbstractPackageAction**

Create `tests/unit/actions/test_package_action.py`:

```python
"""Tests for package actions."""

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.package_action import AbstractPackageAction
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractPackageAction:
    """Test AbstractPackageAction base class."""

    def test_resolve_and_validate_package_success(self):
        """Test successful package resolution."""
        action = AbstractPackageAction()
        action._context = RhapsodyContext()

        # Mock package
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch("rhapsody_cli.actions.package_action.PathResolver") as mock_resolver:
                mock_resolver.resolve_container.return_value = mock_package

                result = action._resolve_and_validate_package("Sensors")
                assert result == mock_package

    def test_resolve_and_validate_package_not_package(self):
        """Test validation fails for non-package element."""
        action = AbstractPackageAction()
        action._context = RhapsodyContext()

        # Mock class (not package)
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch("rhapsody_cli.actions.package_action.PathResolver") as mock_resolver:
                mock_resolver.resolve_container.return_value = mock_class

                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_package("Sensors/MyClass")

                assert "does not resolve to a Package" in str(exc_info.value)
                assert "found Class" in str(exc_info.value)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/actions/test_package_action.py -v`
Expected: FAIL with "No module named 'rhapsody_cli.actions.package_action'"

- [ ] **Step 3: Implement AbstractPackageAction**

Create `src/rhapsody_cli/actions/package_action.py`:

```python
"""Package-related CLI actions."""

import logging
from pathlib import Path
from typing import Any

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.path_resolver import PathResolver
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class AbstractPackageAction(ElementManagementAction):
    """Base class for package actions with common validation logic.

    SWR_PKG_0005: Path Validation
    SWR_PKG_00010: Error Handling and Logging
    """

    def _resolve_and_validate_package(self, path: str) -> Any:
        """Resolve path and validate it's a Package element.

        Args:
            path: Package path to resolve

        Returns:
            Package COM object

        Raises:
            CliExecutionError: If path not found or not a Package
        """
        try:
            project = self._get_active_project()
            root = project.getRoot()
            container = PathResolver.resolve_container(root, path)

            # Validate it's a Package
            meta_class = container.getMetaClass()
            if meta_class != "Package":
                raise CliExecutionError(
                    f"Path '{path}' does not resolve to a Package (found {meta_class})"
                )

            return container

        except Exception as e:
            logger.error("Path resolution failed: %s", e)
            raise CliExecutionError(str(e)) from e

    def add_path_argument(self, parser):
        """Add --path argument to parser."""
        parser.add_argument("--path", required=True, help="Package path")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/actions/test_package_action.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit base class**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Add AbstractPackageAction base class with path validation"
```

---

## Phase 3: PackageCreateAction Implementation

### Task 3: Implement PackageCreateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py`
- Modify: `tests/unit/actions/test_package_action.py`

**Interfaces:**
- Consumes: AbstractPackageAction base class
- Produces: `PackageCreateAction` with:
  - `init_arguments()` - defines CLI arguments
  - `execute()` - creates packages from JSON
  - `_load_json_data()` - loads JSON from file or inline
  - `_set_attributes()` - sets validated attributes
  - VALID_ATTRIBUTES constant

- [ ] **Step 1: Write tests for PackageCreateAction**

Add to `tests/unit/actions/test_package_action.py`:

```python
class TestPackageCreateAction:
    """Test PackageCreateAction.

    UTS_PKG_00001: Create single package with inline JSON
    UTS_PKG_00002: Create multiple packages from JSON file
    UTS_PKG_00003: Create with stereotypes
    UTS_PKG_00004: Create with tags
    UTS_PKG_00006: Create skips unknown attributes
    UTS_PKG_00007: Create fails without name
    """

    def test_create_single_package_inline_json(self, tmp_path):
        """UTS_PKG_00001: Test creating single package with inline JSON."""
        from rhapsody_cli.actions.package_action import PackageCreateAction

        action = PackageCreateAction()
        action._context = RhapsodyContext()

        # Mock parent package
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"

        # Mock created package
        mock_package = MagicMock()
        mock_package.getName.return_value = "TempSensors"
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
                mock_resolve.return_value = mock_parent

                args = MagicMock()
                args.path = "Sensors"
                args.input = None
                args.attributes = '{"name":"TempSensors","description":"Temperature sensors"}'
                args.verbose = False

                action.execute(args)

                mock_parent.addNestedPackage.assert_called_once_with("TempSensors")
                mock_package.setDescription.assert_called_once_with("Temperature sensors")

    def test_create_bulk_packages_from_file(self, tmp_path):
        """Test creating multiple packages from JSON file."""
        from rhapsody_cli.actions.package_action import PackageCreateAction

        action = PackageCreateAction()
        action._context = RhapsodyContext()

        # Create JSON file
        json_file = tmp_path / "packages.json"
        json_file.write_text('''[
            {"name": "TempSensors", "description": "Temperature"},
            {"name": "PressureSensors", "description": "Pressure"}
        ]''')

        # Mock parent package
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
                mock_resolve.return_value = mock_parent

                args = MagicMock()
                args.path = "Sensors"
                args.input = str(json_file)
                args.attributes = None
                args.verbose = False

                action.execute(args)

                assert mock_parent.addNestedPackage.call_count == 2

    def test_create_with_stereotypes_and_tags(self, tmp_path):
        """Test creating package with stereotypes and tags."""
        from rhapsody_cli.actions.package_action import PackageCreateAction

        action = PackageCreateAction()
        action._context = RhapsodyContext()

        # Mock parent and package
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
                mock_resolve.return_value = mock_parent

                args = MagicMock()
                args.path = "Sensors"
                args.input = None
                args.attributes = '''{
                    "name": "TempSensors",
                    "stereotypes": ["auto_generated"],
                    "tags": {"status": "active"}
                }'''
                args.verbose = False

                action.execute(args)

                mock_package.addStereotype.assert_called_once_with("auto_generated", "Package")
                mock_package.setPropertyValue.assert_called_once_with("status", "active")

    def test_create_skips_unknown_attributes(self, tmp_path):
        """Test that unknown attributes are skipped with warning."""
        from rhapsody_cli.actions.package_action import PackageCreateAction

        action = PackageCreateAction()
        action._context = RhapsodyContext()

        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        mock_package = MagicMock()
        mock_parent.addNestedPackage.return_value = mock_package

        with patch.object(action, "_get_active_project") as mock_project:
            mock_root = MagicMock()
            mock_project.return_value.getRoot.return_value = mock_root

            with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
                mock_resolve.return_value = mock_parent

                args = MagicMock()
                args.path = "Sensors"
                args.input = None
                args.attributes = '{"name":"TempSensors","unknown_field":"value"}'
                args.verbose = False

                # Capture warning log
                with patch.object(action.logger, "warning") as mock_warning:
                    action.execute(args)

                    mock_warning.assert_called_once()
                    assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self, tmp_path):
        """Test that missing name raises error."""
        from rhapsody_cli.actions.package_action import PackageCreateAction

        action = PackageCreateAction()
        action._context = RhapsodyContext()

        args = MagicMock()
        args.path = "Sensors"
        args.input = None
        args.attributes = '{"description":"No name"}'
        args.verbose = False

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "'name' is required" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageCreateAction -v`
Expected: FAIL with "PackageCreateAction not defined"

- [ ] **Step 3: Implement PackageCreateAction**

Add to `src/rhapsody_cli/actions/package_action.py`:

```python
import json
import logging
from pathlib import Path
from typing import Any

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.path_resolver import PathResolver
from rhapsody_cli.exceptions import CliExecutionError

logger = logging.getLogger(__name__)


class PackageCreateAction(AbstractPackageAction):
    """Create one or multiple packages.

    SWR_PKG_0001: Package Create Command
    SWR_PKG_0006: External JSON File Support
    SWR_PKG_0007: Stereotype and Tag Support
    SWR_PKG_00009: View-to-Create Workflow
    """

    VALID_ATTRIBUTES = {
        "name", "description", "description_html", "description_rtf",
        "display_name", "display_name_rtf", "properties",
        "stereotypes", "tags"
    }

    def init_arguments(self, sub_parser):
        """Define CLI arguments."""
        parser = sub_parser.add_parser("create", help="Create a package")
        parser.add_argument("--path", required=True, help="Parent package path")
        parser.add_argument("--input", help="JSON file with package attributes")
        parser.add_argument("attributes", nargs="?", help="Inline JSON or JSON file path")
        self.add_verbose_argument(parser)

    def execute(self, args):
        """Execute package creation."""
        # Load JSON data
        if args.input:
            data = self._load_json_data(args.input)
        elif args.attributes:
            data = self._load_json_data(args.attributes)
        else:
            raise CliExecutionError("Either --input or attributes argument must be provided")

        # Support both single hash and array
        packages_data = data if isinstance(data, list) else [data]

        # Resolve and validate parent package
        container = self._resolve_and_validate_package(args.path)

        # Create packages
        created = []
        errors = []
        for pkg_attrs in packages_data:
            try:
                name = pkg_attrs.get("name")
                if not name:
                    raise CliExecutionError("'name' is required in attributes")

                # Filter unknown attributes
                unknown = set(pkg_attrs.keys()) - self.VALID_ATTRIBUTES
                if unknown:
                    self.logger.warning("Skipping unknown attributes: %s", unknown)

                # Create package
                package = container.addNestedPackage(name)

                # Set validated attributes
                self._set_attributes(package, pkg_attrs)

                full_path = f"{args.path}/{name}"
                self.logger.info("Created package: %s", full_path)
                created.append(name)

            except Exception as e:
                self.logger.error("Failed to create package '%s': %s", pkg_attrs.get("name", "unknown"), e)
                errors.append((pkg_attrs.get("name", "unknown"), str(e)))

        # Report results
        if errors and not created:
            raise CliExecutionError(f"Created 0/{len(packages_data)} packages; all failed")
        elif errors:
            self.logger.info("Created %d/%d packages with %d error(s)", len(created), len(packages_data), len(errors))

    def _load_json_data(self, attributes_input: str) -> Any:
        """Load JSON data from inline string or external file."""
        # Check if inline JSON
        if attributes_input.startswith("{") or attributes_input.startswith("["):
            try:
                return json.loads(attributes_input)
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}")

        # Otherwise treat as file path
        if not Path(attributes_input).exists():
            raise CliExecutionError(f"File not found: {attributes_input}")

        try:
            with open(attributes_input, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise CliExecutionError(f"Invalid JSON in file: {e}")
        except OSError as e:
            raise CliExecutionError(f"Failed to read file: {e}")

    def _set_attributes(self, package, attrs):
        """Set validated attributes on package."""
        self._set_basic_attributes(package, attrs)
        self._set_properties(package, attrs)
        self._set_stereotypes(package, attrs)
        self._set_tags(package, attrs)

    def _set_basic_attributes(self, package, attrs):
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

    def _set_properties(self, package, attrs):
        """Set custom properties."""
        if "properties" in attrs:
            for key, val in attrs["properties"].items():
                package.setPropertyValue(key, val)

    def _set_stereotypes(self, package, attrs):
        """Apply stereotypes."""
        if "stereotypes" in attrs:
            for stereotype in attrs["stereotypes"]:
                package.addStereotype(stereotype, "Package")

    def _set_tags(self, package, attrs):
        """Set tags."""
        if "tags" in attrs:
            for key, val in attrs["tags"].items():
                package.setPropertyValue(key, val)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageCreateAction -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit PackageCreateAction**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Implement PackageCreateAction with bulk creation and validation"
```

---

## Phase 4: PackageDeleteAction Implementation

### Task 4: Implement PackageDeleteAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py`
- Modify: `tests/unit/actions/test_package_action.py`

**Interfaces:**
- Consumes: AbstractPackageAction._resolve_and_validate_package()
- Produces: `PackageDeleteAction` with init_arguments() and execute()

- [ ] **Step 1: Write tests for PackageDeleteAction**

Add to `tests/unit/actions/test_package_action.py`:

```python
class TestPackageDeleteAction:
    """Test PackageDeleteAction."""

    def test_delete_package_success(self):
        """Test successful package deletion."""
        from rhapsody_cli.actions.package_action import PackageDeleteAction

        action = PackageDeleteAction()
        action._context = RhapsodyContext()

        # Mock package
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.deleteFromProject = MagicMock()

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_package

            args = MagicMock()
            args.path = "Sensors/OldPackage"
            args.verbose = False

            action.execute(args)

            mock_package.deleteFromProject.assert_called_once()

    def test_delete_package_handles_error(self):
        """Test error handling during deletion."""
        from rhapsody_cli.actions.package_action import PackageDeleteAction

        action = PackageDeleteAction()
        action._context = RhapsodyContext()

        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.deleteFromProject.side_effect = Exception("COM error")

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_package

            args = MagicMock()
            args.path = "Sensors/OldPackage"
            args.verbose = False

            with pytest.raises(Exception) as exc_info:
                action.execute(args)

            assert "COM error" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageDeleteAction -v`
Expected: FAIL with "PackageDeleteAction not defined"

- [ ] **Step 3: Implement PackageDeleteAction**

Add to `src/rhapsody_cli/actions/package_action.py`:

```python
class PackageDeleteAction(AbstractPackageAction):
    """Delete a package.

    SWR_PKG_0002: Package Delete Command
    """

    def init_arguments(self, sub_parser):
        """Define CLI arguments."""
        parser = sub_parser.add_parser("delete", help="Delete a package")
        parser.add_argument("--path", required=True, help="Package path to delete")
        self.add_verbose_argument(parser)

    def execute(self, args):
        """Execute package deletion."""
        package = self._resolve_and_validate_package(args.path)

        try:
            package.deleteFromProject()
            self.logger.info("Deleted package: %s", args.path)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete package '{args.path}'")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageDeleteAction -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit PackageDeleteAction**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Implement PackageDeleteAction with path validation"
```

---

## Phase 5: PackageViewAction Implementation

### Task 5: Implement PackageViewAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py`
- Modify: `tests/unit/actions/test_package_action.py`

**Interfaces:**
- Consumes: AbstractPackageAction._resolve_and_validate_package()
- Produces: `PackageViewAction` with multi-format output and file support

- [ ] **Step 1: Write tests for PackageViewAction**

Add to `tests/unit/actions/test_package_action.py`:

```python
class TestPackageViewAction:
    """Test PackageViewAction."""

    def test_view_table_output(self, capsys):
        """Test table format output."""
        from rhapsody_cli.actions.package_action import PackageViewAction

        action = PackageViewAction()
        action._context = RhapsodyContext()
        action._context.output_format = "table"

        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.getName.return_value = "TempSensors"
        mock_package.getGUID.return_value = "{12345}"
        mock_package.getDescription.return_value = "Temperature sensors"
        mock_package.getFullPathName.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_package

            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "table"
            args.output = None
            args.verbose = False

            action.execute(args)

            captured = capsys.readouterr()
            assert "TempSensors" in captured.out
            assert "{12345}" in captured.out

    def test_view_json_output_to_file(self, tmp_path):
        """Test JSON output to file."""
        from rhapsody_cli.actions.package_action import PackageViewAction
        import json

        action = PackageViewAction()
        action._context = RhapsodyContext()
        action._context.output_format = "json"

        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.getName.return_value = "TempSensors"
        mock_package.getGUID.return_value = "{12345}"
        mock_package.getDescription.return_value = "Temperature sensors"
        mock_package.getFullPathName.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_package

            output_file = tmp_path / "package.json"
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "json"
            args.output = str(output_file)
            args.verbose = False

            action.execute(args)

            # Verify file created and contains valid JSON
            data = json.loads(output_file.read_text())
            assert data["name"] == "TempSensors"
            assert data["guid"] == "{12345}"

    def test_view_csv_output(self, capsys):
        """Test CSV format output."""
        from rhapsody_cli.actions.package_action import PackageViewAction

        action = PackageViewAction()
        action._context = RhapsodyContext()
        action._context.output_format = "csv"

        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.getName.return_value = "TempSensors"
        mock_package.getGUID.return_value = "{12345}"
        mock_package.getDescription.return_value = "Temperature sensors"
        mock_package.getFullPathName.return_value = "Sensors/TempSensors"

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_package

            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.format = "csv"
            args.output = None
            args.verbose = False

            action.execute(args)

            captured = capsys.readouterr()
            # CSV should have header + data row
            lines = captured.out.strip().split("\n")
            assert len(lines) == 2
            assert "Name,GUID" in lines[0]
            assert "TempSensors,{12345}" in lines[1]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageViewAction -v`
Expected: FAIL with "PackageViewAction not defined"

- [ ] **Step 3: Implement PackageViewAction**

Add to `src/rhapsody_cli/actions/package_action.py`:

```python
from rhapsody_cli.cli.formatters import OutputFormatter


class PackageViewAction(AbstractPackageAction):
    """View package details.

    SWR_PKG_0003: Package View Command
    SWR_PKG_0008: Multi-Format Output
    """

    def init_arguments(self, sub_parser):
        """Define CLI arguments."""
        parser = sub_parser.add_parser("view", help="View package details")
        parser.add_argument("--path", required=True, help="Package path to view")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args):
        """Execute package view."""
        package = self._resolve_and_validate_package(args.path)

        try:
            # Get package details
            name = package.getName()
            guid = package.getGUID()
            description = package.getDescription()
            meta_class = package.getMetaClass()
            full_path = package.getFullPathName()

            # Prepare data
            data = {
                "name": name,
                "guid": guid,
                "description": description,
                "metaClass": meta_class,
                "fullPath": full_path,
            }

            table_rows = [
                ["Name", name],
                ["GUID", guid],
                ["Description", description],
                ["MetaClass", meta_class],
                ["FullPath", full_path],
            ]

            # Format output
            output = self._format_output(data, table_rows, args.format)

            # Write to file or stdout
            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote package details to: %s", args.output)
            else:
                print(output)

        except Exception as e:
            self._handle_execution_error(e, f"Failed to view package '{args.path}'")

    def _format_output(self, data, table_rows, format_type):
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(data)
        elif format_type == "csv":
            # CSV: header row + data row
            headers = ["Name", "GUID", "Description", "MetaClass", "FullPath"]
            data_row = [data["name"], data["guid"], data["description"], data["metaClass"], data["fullPath"]]
            return OutputFormatter.csv_format(headers, [data_row])
        else:
            return OutputFormatter.table(["Property", "Value"], table_rows)

    def _write_to_file(self, file_path, content):
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageViewAction -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit PackageViewAction**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Implement PackageViewAction with multi-format output"
```

---

## Phase 6: PackageListAction Implementation

### Task 6: Implement PackageListAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py`
- Modify: `tests/unit/actions/test_package_action.py`

**Interfaces:**
- Consumes: AbstractPackageAction._resolve_and_validate_package()
- Produces: `PackageListAction` with nested package listing

- [ ] **Step 1: Write tests for PackageListAction**

Add to `tests/unit/actions/test_package_action.py`:

```python
class TestPackageListAction:
    """Test PackageListAction."""

    def test_list_nested_packages(self, capsys):
        """Test listing nested packages."""
        from rhapsody_cli.actions.package_action import PackageListAction

        action = PackageListAction()
        action._context = RhapsodyContext()
        action._context.output_format = "table"

        # Mock parent package
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"

        # Mock nested packages
        pkg1 = MagicMock()
        pkg1.getName.return_value = "TempSensors"
        pkg2 = MagicMock()
        pkg2.getName.return_value = "PressureSensors"

        mock_parent.getNestedPackages.return_value = [pkg1, pkg2]

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_parent

            args = MagicMock()
            args.path = "Sensors"
            args.format = "table"
            args.output = None
            args.verbose = False

            action.execute(args)

            captured = capsys.readouterr()
            assert "TempSensors" in captured.out
            assert "PressureSensors" in captured.out

    def test_list_empty_package(self, capsys):
        """Test listing empty package."""
        from rhapsody_cli.actions.package_action import PackageListAction

        action = PackageListAction()
        action._context = RhapsodyContext()

        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        mock_parent.getNestedPackages.return_value = []

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_parent

            args = MagicMock()
            args.path = "EmptyPackage"
            args.format = "table"
            args.output = None
            args.verbose = False

            action.execute(args)

            captured = capsys.readouterr()
            # Should show empty table

    def test_list_json_output(self, capsys):
        """Test JSON output format."""
        from rhapsody_cli.actions.package_action import PackageListAction
        import json

        action = PackageListAction()
        action._context = RhapsodyContext()

        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"

        pkg1 = MagicMock()
        pkg1.getName.return_value = "TempSensors"
        pkg2 = MagicMock()
        pkg2.getName.return_value = "PressureSensors"

        mock_parent.getNestedPackages.return_value = [pkg1, pkg2]

        with patch.object(action, "_resolve_and_validate_package") as mock_resolve:
            mock_resolve.return_value = mock_parent

            args = MagicMock()
            args.path = "Sensors"
            args.format = "json"
            args.output = None
            args.verbose = False

            action.execute(args)

            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert data == ["TempSensors", "PressureSensors"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageListAction -v`
Expected: FAIL with "PackageListAction not defined"

- [ ] **Step 3: Implement PackageListAction**

Add to `src/rhapsody_cli/actions/package_action.py`:

```python
class PackageListAction(AbstractPackageAction):
    """List nested packages.

    SWR_PKG_0004: Package List Command
    SWR_PKG_0008: Multi-Format Output
    """

    def init_arguments(self, sub_parser):
        """Define CLI arguments."""
        parser = sub_parser.add_parser("list", help="List nested packages")
        parser.add_argument("--path", required=True, help="Package path")
        parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
        parser.add_argument("--output", help="Write output to file")
        self.add_verbose_argument(parser)

    def execute(self, args):
        """Execute package list."""
        package = self._resolve_and_validate_package(args.path)

        try:
            # Get nested packages
            nested_packages = package.getNestedPackages()
            package_names = [pkg.getName() for pkg in nested_packages]

            # Prepare table rows
            table_rows = [[name] for name in package_names]

            # Format output
            output = self._format_output(package_names, table_rows, args.format)

            # Write to file or stdout
            if args.output:
                self._write_to_file(args.output, output)
                self.logger.info("Wrote %d packages to: %s", len(package_names), args.output)
            else:
                print(output)

        except Exception as e:
            self._handle_execution_error(e, f"Failed to list packages in '{args.path}'")

    def _format_output(self, package_names, table_rows, format_type):
        """Format output based on format parameter."""
        if format_type == "json":
            return OutputFormatter.json_format(package_names)
        elif format_type == "csv":
            return OutputFormatter.csv_format(["Name"], table_rows)
        else:
            return OutputFormatter.table(["Name"], table_rows)

    def _write_to_file(self, file_path, content):
        """Write content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            raise CliExecutionError(f"Failed to write file '{file_path}': {e}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageListAction -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit PackageListAction**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Implement PackageListAction for nested package listing"
```

---

## Phase 7: PackageCommand Dispatcher

### Task 7: Implement PackageCommand Dispatcher

**Files:**
- Create: `src/rhapsody_cli/commands/package_command.py`
- Create: `tests/unit/commands/test_package_command.py`
- Modify: `src/rhapsody_cli/cli/main.py`

**Interfaces:**
- Consumes: 4 Action classes
- Produces: `PackageCommand` class that registers subcommands

- [ ] **Step 1: Write test for PackageCommand**

Create `tests/unit/commands/test_package_command.py`:

```python
"""Tests for PackageCommand."""

from unittest.mock import MagicMock

from rhapsody_cli.commands.package_command import PackageCommand


class TestPackageCommand:
    """Test PackageCommand dispatcher."""

    def test_register_subcommands(self):
        """Test that all subcommands are registered."""
        command = PackageCommand()
        mock_subparsers = MagicMock()

        command.register_subcommands(mock_subparsers)

        # Should register 4 subcommands
        assert mock_subparsers.add_parser.call_count == 4

        # Check each subcommand
        calls = mock_subparsers.add_parser.call_args_list
        command_names = [call[0][0] for call in calls]

        assert "create" in command_names
        assert "delete" in command_names
        assert "view" in command_names
        assert "list" in command_names
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/commands/test_package_command.py -v`
Expected: FAIL with "No module named 'rhapsody_cli.commands.package_command'"

- [ ] **Step 3: Implement PackageCommand**

Create `src/rhapsody_cli/commands/package_command.py`:

```python
"""Package command dispatcher."""

from rhapsody_cli.actions.package_action import (
    PackageCreateAction,
    PackageDeleteAction,
    PackageViewAction,
    PackageListAction,
)
from rhapsody_cli.commands.abstract_command import Command


class PackageCommand(Command):
    """Package command dispatcher."""

    def register_subcommands(self, sub_parser):
        """Register package subcommands."""
        # Register create action
        create_action = PackageCreateAction()
        create_action.init_arguments(sub_parser)

        # Register delete action
        delete_action = PackageDeleteAction()
        delete_action.init_arguments(sub_parser)

        # Register view action
        view_action = PackageViewAction()
        view_action.init_arguments(sub_parser)

        # Register list action
        list_action = PackageListAction()
        list_action.init_arguments(sub_parser)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/commands/test_package_command.py -v`
Expected: PASS

- [ ] **Step 5: Register in main CLI**

Modify `src/rhapsody_cli/cli/main.py` to add:

```python
from rhapsody_cli.commands.package_command import PackageCommand

# In register_commands():
package_cmd = PackageCommand()
package_cmd.register_subcommands(subparsers)
```

- [ ] **Step 6: Commit PackageCommand**

```bash
git add src/rhapsody_cli/commands/package_command.py tests/unit/commands/test_package_command.py src/rhapsody_cli/cli/main.py
git commit -m "feat: Add PackageCommand dispatcher and register in CLI"
```

---

## Phase 8: Sphinx Documentation

### Task 8: Write User Guide Documentation

**Files:**
- Create: `docs/user-guide/package-command.rst`
- Modify: `docs/user-guide/index.rst`

**Sphinx content to add:**

- [ ] **Step 1: Create package-command.rst**

Create `docs/user-guide/package-command.rst`:

```restructuredtext
Package Command
===============

The ``package`` command provides operations for managing Rhapsody packages via CLI.

Synopsis
--------

::

   rhapsody-cli package <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple packages

delete
   Delete a package

view
   View package details

list
   List nested packages

package create
--------------

Create one or multiple packages with validated attributes.

**Usage:**

::

   rhapsody-cli package create --path <parent-path> [options] [attributes]

**Arguments:**

- ``--path <parent-path>`` - Parent package path (required)
- ``--input <json-file>`` - JSON file with package attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single package with inline JSON::

   rhapsody-cli package create --path Sensors '{"name":"TempSensors","description":"Temperature sensors"}'

Create multiple packages from file::

   rhapsody-cli package create --path Sensors --input packages.json

Reuse exported package::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output package.json
   rhapsody-cli package create --path NewSensors package.json

**JSON Format:**

Single package::

   {
     "name": "TempSensors",
     "description": "Temperature sensors package",
     "stereotypes": ["auto_generated"],
     "tags": {"status": "active"}
   }

Multiple packages::

   [
     {"name": "TempSensors", "description": "Temperature"},
     {"name": "PressureSensors", "description": "Pressure"}
   ]

**Validated Attributes:**

- ``name`` (required) - Package name
- ``description`` - Plain text description
- ``description_html`` - HTML description
- ``properties`` - Custom properties object
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Tag name-value pairs

package delete
--------------

Delete a package and all its contents.

**Usage:**

::

   rhapsody-cli package delete --path <package-path>

**Example:**

::

   rhapsody-cli package delete --path Sensors/OldPackage

package view
------------

View package details in various formats.

**Usage:**

::

   rhapsody-cli package view --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Examples:**

View in table format::

   rhapsody-cli package view --path Sensors/TempSensors

Export to JSON file::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output package.json

Export to CSV::

   rhapsody-cli package view --path Sensors/TempSensors --format csv --output package.csv

**Output Formats:**

Table::

   +-----------+--------------------------------------+
   | Property  | Value                                |
   +-----------+--------------------------------------+
   | Name      | TempSensors                          |
   | GUID      | {12345678-1234-1234-1234-1234567890} |
   | Desc      | Temperature sensors package          |
   | MetaClass | Package                              |
   | FullPath  | Sensors/TempSensors                  |
   +-----------+--------------------------------------+

JSON::

   {
     "name": "TempSensors",
     "guid": "{12345678-1234-1234-1234-1234567890}",
     "description": "Temperature sensors package",
     "metaClass": "Package",
     "fullPath": "Sensors/TempSensors"
   }

CSV::

   Name,GUID,Description,MetaClass,FullPath
   TempSensors,{12345678-1234-1234-1234-1234567890},Temperature sensors package,Package,Sensors/TempSensors

package list
------------

List nested packages under a parent package.

**Usage:**

::

   rhapsody-cli package list --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Examples:**

List nested packages::

   rhapsody-cli package list --path Sensors

Export to JSON::

   rhapsody-cli package list --path Sensors --format json --output packages.json

**Output Formats:**

Table::

   +----------------+
   | Name           |
   +----------------+
   | TempSensors    |
   | PressureSensors|
   | FlowSensors    |
   +----------------+

JSON::

   ["TempSensors", "PressureSensors", "FlowSensors"]

CSV::

   Name
   TempSensors
   PressureSensors
   FlowSensors

Workflow: Package Cloning
-------------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export package to JSON::

   rhapsody-cli package view --path Sensors/TempSensors --format json --output template.json

**Step 2:** Edit template.json (modify name, description, etc.)

**Step 3:** Create new package from template::

   rhapsody-cli package create --path NewSensors template.json

Error Handling
--------------

All commands validate the path before execution:

- Path must exist in the model
- Path must resolve to a Package element (not Class, Actor, etc.)
- Invalid path raises ``CliExecutionError``

Examples of errors::

   Path 'Sensors/Invalid' not found
   Path 'Sensors/MyClass' does not resolve to a Package (found Class)

See Also
--------

- :doc:`element-command` - Generic element operations
- :doc:`project-command` - Project management operations
```

- [ ] **Step 2: Add to user guide index**

Modify `docs/user-guide/index.rst` to add:

```restructuredtext
.. toctree::
   :maxdepth: 2

   package-command
```

- [ ] **Step 3: Build Sphinx documentation**

Run: `cd docs && make html`
Expected: No errors, package-command.html generated

- [ ] **Step 4: Commit documentation**

```bash
git add docs/user-guide/package-command.rst docs/user-guide/index.rst
git commit -m "docs: Add comprehensive user guide for package command"
```

---

## Phase 9: Test Case Documentation

### Task 9: Document Test Cases

**Files:**
- Create: `docs/tests/unit/uts_pkg_test-specs.md`

**Test case IDs to add:**

- [ ] **Step 1: Create test spec file**

Create `docs/tests/unit/uts_pkg_test-specs.md`:

```markdown
# Unit Test Specifications - Package Command

**Category:** Package Command
**Prefix:** UTS_PKG
**Source:** SWR_PKG Requirements
**Last Updated:** 2026-07-09

---

## UTS_PKG_00001: Create single package with inline JSON

**ID:** UTS_PKG_00001
**Traces-To:** SWR_PKG_0001
**Title:** Create single package with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single package can be created with inline JSON containing name and description.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent package exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call PackageCreateAction with inline JSON
2. Verify package created via addNestedPackage
3. Verify description set via setDescription
**Expected Result:**
Package created successfully with correct name and description.
**Verification Criteria:**
- addNestedPackage called once with correct name
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-09

---

## UTS_PKG_00002: Create multiple packages from JSON file

**ID:** UTS_PKG_00002
**Traces-To:** SWR_PKG_0001, SWR_PKG_0006
**Title:** Create multiple packages from JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of packages from external JSON file with array of package definitions.
**Pre-conditions:**
- JSON file exists with valid array of package definitions
- Parent package exists
**Test Steps:**
1. Call PackageCreateAction with --input pointing to JSON file
2. Verify file read with UTF-8 encoding
3. Verify all packages created
**Expected Result:**
All packages created, logs show count.
**Verification Criteria:**
- File opened with UTF-8 encoding
- addNestedPackage called for each package
- Logger shows total count
**Last Changed:** 2026-07-09

---

## UTS_PKG_00003: Create with stereotypes

**ID:** UTS_PKG_00003
**Traces-To:** SWR_PKG_0007
**Title:** Create package with stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that stereotypes are applied to package during creation.
**Pre-conditions:**
- JSON contains stereotypes array
**Test Steps:**
1. Call PackageCreateAction with JSON containing stereotypes
2. Verify addStereotype called for each stereotype
**Expected Result:**
All stereotypes applied correctly.
**Verification Criteria:**
- addStereotype called once per stereotype
- Correct stereotype name and "Package" type passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00004: Create with tags

**ID:** UTS_PKG_00004
**Traces-To:** SWR_PKG_0007
**Title:** Create package with tags
**Type:** Unit
**Priority:** Medium
**Description:**
Test that tags are set on package during creation.
**Pre-conditions:**
- JSON contains tags object
**Test Steps:**
1. Call PackageCreateAction with JSON containing tags
2. Verify setPropertyValue called for each tag
**Expected Result:**
All tags set correctly.
**Verification Criteria:**
- setPropertyValue called once per tag
- Correct key-value pairs passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00005: Create with properties

**ID:** UTS_PKG_00005
**Traces-To:** SWR_PKG_0001
**Title:** Create package with custom properties
**Type:** Unit
**Priority:** Medium
**Description:**
Test that custom properties are set on package during creation.
**Pre-conditions:**
- JSON contains properties object
**Test Steps:**
1. Call PackageCreateAction with JSON containing properties
2. Verify setPropertyValue called for each property
**Expected Result:**
All properties set correctly.
**Verification Criteria:**
- setPropertyValue called once per property
- Correct key-value pairs passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00006: Create skips unknown attributes

**ID:** UTS_PKG_00006
**Traces-To:** SWR_PKG_0001
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes in JSON are skipped and logged as warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call PackageCreateAction with JSON containing unknown fields
2. Verify package still created
3. Verify warning logged
**Expected Result:**
Package created, unknown fields skipped with warning.
**Verification Criteria:**
- Package created successfully
- Logger.warning called with unknown field names
**Last Changed:** 2026-07-09

---

## UTS_PKG_00007: Create fails without name

**ID:** UTS_PKG_00007
**Traces-To:** SWR_PKG_0001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name field is missing from JSON.
**Pre-conditions:**
- JSON does not contain name field
**Test Steps:**
1. Call PackageCreateAction with JSON without name
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with appropriate message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "'name' is required"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00008: Create from external file

**ID:** UTS_PKG_00008
**Traces-To:** SWR_PKG_0006
**Title:** Create packages from external JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test that packages can be created from external JSON file.
**Pre-conditions:**
- Valid JSON file exists
**Test Steps:**
1. Call PackageCreateAction with --input parameter
2. Verify file read with UTF-8
3. Verify packages created
**Expected Result:**
File read and packages created.
**Verification Criteria:**
- File opened with UTF-8 encoding
- Packages created from file content
**Last Changed:** 2026-07-09

---

## UTS_PKG_00009: Create fails for invalid JSON

**ID:** UTS_PKG_00009
**Traces-To:** SWR_PKG_0006
**Title:** Create fails for malformed JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails gracefully for malformed JSON.
**Pre-conditions:**
- Malformed JSON string provided
**Test Steps:**
1. Call PackageCreateAction with malformed JSON
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with JSON parse error.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Invalid JSON"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00010: Create fails for missing file

**ID:** UTS_PKG_00010
**Traces-To:** SWR_PKG_0006
**Title:** Create fails for non-existent file
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails for non-existent file path.
**Pre-conditions:**
- File does not exist
**Test Steps:**
1. Call PackageCreateAction with non-existent file path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with file not found message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "File not found"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00011: Delete package successfully

**ID:** UTS_PKG_00011
**Traces-To:** SWR_PKG_0002
**Title:** Delete package successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that package is deleted successfully.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageDeleteAction with valid path
2. Verify deleteFromProject called
3. Verify log message shown
**Expected Result:**
Package deleted with log message.
**Verification Criteria:**
- deleteFromProject called once
- Logger shows INFO message
**Last Changed:** 2026-07-09

---

## UTS_PKG_00012: Delete handles COM error

**ID:** UTS_PKG_00012
**Traces-To:** SWR_PKG_00010
**Title:** Delete handles COM error gracefully
**Type:** Unit
**Priority:** High
**Description:**
Test that COM errors during deletion are handled properly.
**Pre-conditions:**
- deleteFromProject raises exception
**Test Steps:**
1. Call PackageDeleteAction
2. Simulate COM error in deleteFromProject
3. Verify error handled
**Expected Result:**
Exception handled, error logged.
**Verification Criteria:**
- Exception caught
- _handle_execution_error called
- Error logged
**Last Changed:** 2026-07-09

---

## UTS_PKG_00013: View table output

**ID:** UTS_PKG_00013
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in table format
**Type:** Unit
**Priority:** High
**Description:**
Test that package details are displayed in table format.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageViewAction with format=table
2. Verify table output contains all properties
**Expected Result:**
Table printed to stdout with all package properties.
**Verification Criteria:**
- Table contains Name, GUID, Description, etc.
- OutputFormatter.table called
**Last Changed:** 2026-07-09

---

## UTS_PKG_00014: View JSON output to file

**ID:** UTS_PKG_00014
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in JSON format to file
**Type:** Unit
**Priority:** High
**Description:**
Test that package details are written to JSON file.
**Pre-conditions:**
- Package exists at specified path
- Output file path provided
**Test Steps:**
1. Call PackageViewAction with format=json and --output
2. Verify JSON file created
3. Verify JSON contains all fields
**Expected Result:**
JSON file created with all package details.
**Verification Criteria:**
- File created at specified path
- JSON parseable and contains all fields
**Last Changed:** 2026-07-09

---

## UTS_PKG_00015: View CSV output

**ID:** UTS_PKG_00015
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test that package details are displayed in CSV format with horizontal layout.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageViewAction with format=csv
2. Verify CSV output has header + data row
**Expected Result:**
CSV printed with horizontal layout.
**Verification Criteria:**
- Output has exactly 2 lines
- Header row present
- Data row present
**Last Changed:** 2026-07-09

---

## UTS_PKG_00016: List nested packages

**ID:** UTS_PKG_00016
**Traces-To:** SWR_PKG_0004
**Title:** List nested packages
**Type:** Unit
**Priority:** High
**Description:**
Test that nested packages are listed correctly.
**Pre-conditions:**
- Package has nested packages
**Test Steps:**
1. Call PackageListAction with parent package path
2. Verify all nested packages shown
**Expected Result:**
List of nested package names.
**Verification Criteria:**
- getNestedPackages called
- All nested package names shown
**Last Changed:** 2026-07-09

---

## UTS_PKG_00017: List empty package

**ID:** UTS_PKG_00017
**Traces-To:** SWR_PKG_0004
**Title:** List empty package returns empty output
**Type:** Unit
**Priority:** Medium
**Description:**
Test that empty output is shown for package with no nested packages.
**Pre-conditions:**
- Package has no nested packages
**Test Steps:**
1. Call PackageListAction
2. Verify empty output
**Expected Result:**
Empty table/list shown.
**Verification Criteria:**
- getNestedPackages returns empty
- Output is empty
**Last Changed:** 2026-07-09

---

## UTS_PKG_00018: List JSON output

**ID:** UTS_PKG_00018
**Traces-To:** SWR_PKG_0004, SWR_PKG_0008
**Title:** List nested packages in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test that nested packages are listed in JSON array format.
**Pre-conditions:**
- Package has nested packages
**Test Steps:**
1. Call PackageListAction with format=json
2. Verify JSON array output
**Expected Result:**
JSON array of package names.
**Verification Criteria:**
- Output is valid JSON array
- Array contains all package names
**Last Changed:** 2026-07-09

---

## UTS_PKG_00019: Path validation - not found

**ID:** UTS_PKG_00019
**Traces-To:** SWR_PKG_0005
**Title:** Path validation fails for non-existent path
**Type:** Unit
**Priority:** High
**Description:**
Test that path validation raises error for non-existent path.
**Pre-conditions:**
- Path does not exist in model
**Test Steps:**
1. Call any package action with non-existent path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with path not found message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "not found"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00020: Path validation - not package

**ID:** UTS_PKG_00020
**Traces-To:** SWR_PKG_0005
**Title:** Path validation fails for non-package element
**Type:** Unit
**Priority:** High
**Description:**
Test that path validation raises error when path resolves to non-package element.
**Pre-conditions:**
- Path resolves to Class or other non-package element
**Test Steps:**
1. Call any package action with path to Class
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "does not resolve to a Package" message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "does not resolve to a Package"
- Error message shows actual element type
**Last Changed:** 2026-07-09

---

## UTS_PKG_00021: View-to-create workflow

**ID:** UTS_PKG_00021
**Traces-To:** SWR_PKG_00009
**Title:** View output can be reused as create input
**Type:** Unit
**Priority:** High
**Description:**
Test that package view JSON output can be used as package create input.
**Pre-conditions:**
- Package view JSON output available
**Test Steps:**
1. Export package via view --format json
2. Use JSON as create input
3. Verify new package created
**Expected Result:**
New package created with same attributes.
**Verification Criteria:**
- Unknown fields (guid, metaClass) ignored
- Only validated attributes used
- Package created successfully
**Last Changed:** 2026-07-09

---

## UTS_PKG_00022: Bulk creation with errors

**ID:** UTS_PKG_00022
**Traces-To:** SWR_PKG_0001
**Title:** Bulk creation handles partial failures
**Type:** Unit
**Priority:** Medium
**Description:**
Test that bulk creation continues on errors and reports results.
**Pre-conditions:**
- JSON array contains some invalid package definitions
**Test Steps:**
1. Call PackageCreateAction with mixed valid/invalid packages
2. Verify valid packages created
3. Verify errors logged
**Expected Result:**
Valid packages created, errors logged, summary shown.
**Verification Criteria:**
- Valid packages created
- Invalid packages logged as errors
- Summary shows count
**Last Changed:** 2026-07-09

---

## UTS_PKG_00023: File output handling

**ID:** UTS_PKG_00023
**Traces-To:** SWR_PKG_0003, SWR_PKG_0004
**Title:** Output written to file when --output specified
**Type:** Unit
**Priority:** High
**Description:**
Test that output is written to file instead of stdout when --output specified.
**Pre-conditions:**
- --output parameter provided
**Test Steps:**
1. Call view/list action with --output
2. Verify file created
3. Verify content matches expected format
**Expected Result:**
Content written to file, not stdout.
**Verification Criteria:**
- File exists at specified path
- File content matches expected output
- Nothing printed to stdout
**Last Changed:** 2026-07-09

---

## UTS_PKG_00024: File output error handling

**ID:** UTS_PKG_00024
**Traces-To:** SWR_PKG_00010
**Title:** File output handles permission errors
**Type:** Unit
**Priority:** High
**Description:**
Test that file output errors are handled gracefully.
**Pre-conditions:**
- Invalid file path (no write permission)
**Test Steps:**
1. Call view/list action with invalid --output path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with file write error.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Failed to write"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00025: Register all subcommands

**ID:** UTS_PKG_00025
**Traces-To:** SWR_PKG_0001-00004
**Title:** PackageCommand registers all subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test that PackageCommand registers all 4 subcommands.
**Pre-conditions:**
- PackageCommand initialized
**Test Steps:**
1. Create PackageCommand
2. Call register_subcommands
3. Verify 4 subcommands registered
**Expected Result:**
All 4 subcommands (create, delete, view, list) registered.
**Verification Criteria:**
- subparser.add_parser called 4 times
- All subcommand names present
**Last Changed:** 2026-07-09
```

- [ ] **Step 2: Commit test spec**

```bash
git add docs/tests/unit/uts_pkg_test-specs.md
git commit -m "docs: Add unit test specifications for package command (UTS_PKG_00001-00025)"
```
--------------------------------
**Input:** --output parameter with valid path
**Expected:** Content written to file, not stdout
**Verification:** Check file exists, contains output

TC-PKG-024: File output error handling
--------------------------------------
**Input:** --output parameter with invalid path (no permission)
**Expected:** CliExecutionError raised
**Verification:** Check error message contains "Failed to write"

TC-PKG-025: Register all subcommands
------------------------------------
**Input:** PackageCommand initialization
**Expected:** All 4 subcommands registered
**Verification:** Check subparser.add_parser called 4 times
```

- [ ] **Step 2: Commit test cases**

```bash
git add docs/requirements.rst
git commit -m "docs: Add comprehensive test cases for package command (TC-PKG-001 to TC-PKG-025)"
```

---

## Phase 10: Final Integration

### Task 10: Final Integration and Verification

**Files:**
- All files from previous tasks

**Final verification steps:**

- [ ] **Step 1: Run all tests**

Run: `pytest tests/ -v --cov=src/rhapsody_cli`
Expected: All tests pass, coverage > 90%

- [ ] **Step 2: Run all linters**

Run: `ruff check src/ tests/ && mypy src/ tests/`
Expected: No errors

- [ ] **Step 3: Build documentation**

Run: `cd docs && make html`
Expected: No warnings, all pages generated

- [ ] **Step 4: Test CLI manually**

Test each subcommand:

```bash
# Test create
rhapsody-cli package create --path Sensors '{"name":"TestPackage"}'

# Test view
rhapsody-cli package view --path Sensors/TestPackage

# Test list
rhapsody-cli package list --path Sensors

# Test delete
rhapsody-cli package delete --path Sensors/TestPackage
```

Expected: All commands work without errors

- [ ] **Step 5: Final commit**

```bash
git add .
git commit -m "feat: Complete package command implementation with full test coverage and documentation"
```

---

## Summary

**Implementation complete!** The package command now provides:

- ✅ SW Requirements (REQ-PKG-001 to REQ-PKG-010)
- ✅ Test Cases (TC-PKG-001 to TC-PKG-025)
- ✅ 4 Subcommands (create, delete, view, list)
- ✅ Bulk creation with validation
- ✅ External JSON file support
- ✅ Multi-format output (table, JSON, CSV)
- ✅ File output support
- ✅ Path validation
- ✅ Comprehensive test coverage
- ✅ User documentation
- ✅ API documentation

**Files created:**
- 2 implementation files (package_command.py, package_action.py)
- 2 test files (test_package_command.py, test_package_action.py)
- 1 documentation file (package-command.rst)

**Test coverage:** 25 test cases covering all functionality