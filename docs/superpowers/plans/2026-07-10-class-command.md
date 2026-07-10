# Class Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `class` command group with create, delete, view, list, and link subcommands for managing Rhapsody RPClass elements via CLI.

**Architecture:** Mirrors the existing `package` command structure exactly. Uses `AbstractClassAction` base class with two path validation helpers (`_resolve_and_validate_package` for create/list, `_resolve_and_validate_class` for delete/view/link). Adds `--guid` lookup support (via `findElementByGUID`) and a `link` subcommand for generalization relationships. Class create uses `addClass()` + 8 attribute-setting helpers following single responsibility principle.

**Tech Stack:** Python 3.8+, argparse CLI framework, Rhapsody COM API wrapper, pytest for testing.

## Global Constraints

- Python version: 3.8+
- All code must pass: `ruff check src/ tests/`, `black --check src/ tests/`, `mypy src/ tests/`, `pytest tests/unit -v`
- All tests must pass before commit
- Follow existing CLI patterns (PackageCommand, PackageCreateAction, etc.) — see `src/rhapsody_cli/actions/package_action.py` and `src/rhapsody_cli/commands/package_command.py`
- Use existing infrastructure: `PathResolver`, `OutputFormatter`, `ElementManagementAction`, `RhapsodyContext`
- TDD approach: write failing test first, then implementation
- Requirement IDs use 5-digit format: `SWR_CLS_00001` through `SWR_CLS_00015`
- Test case IDs use 5-digit format: `UTS_CLS_00001` through `UTS_CLS_00035`
- Class create accepts path resolving to Package **or Project** (metaClass in `{"Package", "Project"}`) since `RPProject` inherits `addClass`/`getClasses` from `RPPackage`
- `link` subcommand v1 supports only `generalization` type; `--type` flag is reserved for future expansion
- The `view` command's JSON output must round-trip cleanly into `create` (unknown fields `guid`, `isComposite`, `isReactive`, `metaClass`, `fullPath` are skipped during create with a warning)
- `getIsAbstract()` returns `bool`; `getIsActive/Final/Composite/Reactive()` return `int` (0/1) — normalize to `int` in JSON output

---

## File Structure

**New files:**
- `src/rhapsody_cli/actions/class_action.py` — 6 Action classes (`AbstractClassAction` + 5 concrete: Create, Delete, View, List, Link)
- `src/rhapsody_cli/commands/class_command.py` — Command dispatcher
- `tests/unit/actions/test_class_action.py` — Action tests
- `tests/unit/commands/test_class_command.py` — Command dispatcher tests
- `docs/requirements/swr_cls_requirements.md` — SW requirements (SWR_CLS_00001-00013)
- `docs/tests/unit/uts_cls_test-specs.md` — Unit test specs (UTS_CLS_00001-00029)
- `docs/user_guide/working_with_classes.rst` — User documentation

**Modified files:**
- `src/rhapsody_cli/cli/cli.py` — Register `class` command in dispatcher and usage text

---

## Phase 1: SW Requirements Documentation

### Task 1: Document Class Command Requirements

**Files:**
- Create: `docs/requirements/swr_cls_requirements.md`

**Interfaces:**
- Produces: SWR_CLS_00001 through SWR_CLS_00015 (referenced by implementation docstrings and test specs)

- [ ] **Step 1: Create requirements file**

Create `docs/requirements/swr_cls_requirements.md`:

```markdown
# Software Requirements - Class Command

**Category:** Class Command
**Prefix:** SWR_CLS
**Source:** Extracted from spec 2026-07-09-class-command-design.md
**Last Validated:** 2026-07-10

---

## SWR_CLS_00001: Class Create Command

**ID:** SWR_CLS_00001
**Title:** class create command creates one or multiple classes
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class create` command to create one or multiple classes.
- SHALL accept `--path <parent-package-path>` argument (required)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path resolves to Package or Project element (metaClass in {"Package", "Project"})
- SHALL create classes via `parent.addClass(name)`
- SHALL set validated attributes: name, description, isAbstract, isFinal, isActive, stereotypes, tags, operations, attributes, superclasses
- SHALL apply name via `addClass()`, description via `setDescription()`, isAbstract via `setIsAbstract(1/0)`, isFinal via `setIsFinal(1/0)`, isActive via `setIsActive(1/0)`, stereotypes via `addStereotype(name, "Class")`, tags via `setPropertyValue(key, val)`, operations via `addOperation(name)`, attributes via `addAttribute(name)`, superclasses via `addGeneralization(classifier)`
- SHALL resolve superclass names via `findNestedClassifierRecursive(name)` on the parent package
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{` or `[`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00002: Class Delete Command

**ID:** SWR_CLS_00002
**Title:** class delete command deletes a class
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class delete` command to delete a class.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL require exactly one of `--path` or `--guid`
- SHALL validate path/guid resolves to Class element (metaClass == "Class")
- SHALL delete class via `deleteFromProject()`
- SHALL log deletion to stderr
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassDeleteAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00003: Class View Command

**ID:** SWR_CLS_00003
**Title:** class view command displays class details
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class view` command to view class details.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display fields: Name, GUID, Description, IsAbstract, IsActive, IsFinal, IsComposite, IsReactive, MetaClass, FullPath, Operations, Attributes
- SHALL collect Operations via `getOperations()` and `op.getName()` for each
- SHALL collect Attributes via `getAttributes()` and `attr.getName()` for each
- SHALL normalize IsAbstract (bool) to int in JSON output
- SHALL support table (Property|Value layout), JSON (12-key object), CSV (horizontal 12-column) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassViewAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00004: Class List Command

**ID:** SWR_CLS_00004
**Title:** class list command lists classes in a package
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class list` command to list classes in a package.
- SHALL accept `--path <package-path>` argument (required)
- SHALL validate path resolves to Package or Project element (metaClass in {"Package", "Project"})
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list classes via `getClasses()` and collect names via `getName()`
- SHALL support table (single Name column), JSON (array of strings), CSV (1-column horizontal) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassListAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00005: Path Validation

**ID:** SWR_CLS_00005
**Title:** All class commands validate path before execution
**Status:** Planned
**Priority:** High
**Description:**
All class commands
- SHALL validate path before execution.
- SHALL resolve path using PathResolver
- SHALL verify element at path is expected type (Package/Project for create/list; Class for delete/view/link)
- SHALL raise CliExecutionError if path not found
- SHALL raise CliExecutionError if path resolves to wrong type
**Implementation:** src/rhapsody_cli/actions/class_action.py:AbstractClassAction._resolve_and_validate_package, _resolve_and_validate_class
**Last Changed:** 2026-07-10

---

## SWR_CLS_00006: External JSON File Support

**ID:** SWR_CLS_00006
**Title:** Class create supports external JSON files
**Status:** Planned
**Priority:** Medium
**Description:**
Class create command
- SHALL support external JSON files.
- SHALL accept `--input <file>` argument
- SHALL accept file path as positional argument
- SHALL detect inline JSON vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL raise CliExecutionError if file not found
- SHALL raise CliExecutionError if JSON invalid
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction._load_json_data
**Last Changed:** 2026-07-10

---

## SWR_CLS_00007: Stereotype and Tag Support

**ID:** SWR_CLS_00007
**Title:** Class create supports stereotypes and tags
**Status:** Planned
**Priority:** Medium
**Description:**
Class create command
- SHALL support stereotypes and tags.
- SHALL accept `stereotypes` array in JSON
- SHALL apply stereotypes via `addStereotype(name, "Class")`
- SHALL accept `tags` object in JSON
- SHALL set tags via `setPropertyValue(key, val)`
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction._set_stereotypes, _set_properties
**Last Changed:** 2026-07-10

---

## SWR_CLS_00008: Multi-Format Output

**ID:** SWR_CLS_00008
**Title:** Class view and list support multiple output formats
**Status:** Planned
**Priority:** Medium
**Description:**
Class view and list commands
- SHALL support multiple output formats.
- SHALL support table format (default, human-readable)
- SHALL support JSON format (machine-parsable)
- SHALL support CSV format (spreadsheet-friendly)
- SHALL use horizontal layout for CSV (header row + data rows)
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassViewAction._format_output, ClassListAction._format_output
**Last Changed:** 2026-07-10

---

## SWR_CLS_00009: View-to-Create Workflow

**ID:** SWR_CLS_00009
**Title:** Class view JSON output reusable as class create input
**Status:** Planned
**Priority:** Medium
**Description:**
Class view JSON output
- SHALL be reusable as class create input.
- SHALL ignore unknown fields (guid, isComposite, isReactive, metaClass, fullPath) in create with warning
- SHALL only use validated attributes from view output
- SHALL enable class cloning workflow
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction.VALID_ATTRIBUTES
**Last Changed:** 2026-07-10

---

## SWR_CLS_00010: Error Handling and Logging

**ID:** SWR_CLS_00010
**Title:** All class actions follow consistent error handling patterns
**Status:** Planned
**Priority:** High
**Description:**
All class actions
- SHALL follow consistent error handling patterns.
- SHALL use `_handle_execution_error()` for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/class_action.py:AbstractClassAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00011: Class Link Command

**ID:** SWR_CLS_00011
**Title:** class link command adds/removes generalization relationships
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class link` command to manage generalization relationships.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--add <class-name>` argument (optional)
- SHALL accept `--remove <class-name>` argument (optional)
- SHALL require exactly one of `--add` or `--remove`
- SHALL accept `--type <generalization>` argument (optional, default: generalization)
- SHALL validate source class via path/guid resolves to Class element (metaClass == "Class")
- SHALL resolve target class by name via `findNestedClassifierRecursive(name)` on source class
- SHALL add generalization via `addGeneralization(target_classifier)` when `--add` specified
- SHALL remove generalization via `deleteGeneralization(target_classifier)` when `--remove` specified
- SHALL raise CliExecutionError if target name not found
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassLinkAction
**Last Changed:** 2026-07-10

---

## SWR_CLS_00012: Boolean Flag Support

**ID:** SWR_CLS_00012
**Title:** Class create supports boolean flags isAbstract, isFinal, isActive
**Status:** Planned
**Priority:** Medium
**Description:**
Class create command
- SHALL support boolean flags.
- SHALL accept `isAbstract` bool in JSON, set via `setIsAbstract(1/0)`
- SHALL accept `isFinal` bool in JSON, set via `setIsFinal(1/0)`
- SHALL accept `isActive` bool in JSON, set via `setIsActive(1/0)`
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction._set_boolean_flags
**Last Changed:** 2026-07-10

---

## SWR_CLS_00013: GUID Lookup Support

**ID:** SWR_CLS_00013
**Title:** Class view/delete/link support --guid as alternative to --path
**Status:** Planned
**Priority:** Medium
**Description:**
Class view, delete, and link commands
- SHALL support `--guid` as alternative to `--path`.
- SHALL accept `--guid <guid>` argument (format: 12345678-1234-1234-1234-123456789abc)
- SHALL require exactly one of `--path` or `--guid`
- SHALL locate class by GUID via `findElementByGUID(guid)` on the active project
- SHALL validate located element is Class (metaClass == "Class")
- SHALL raise CliExecutionError if GUID not found
**Implementation:** src/rhapsody_cli/actions/class_action.py:AbstractClassAction._resolve_class_by_guid
**Last Changed:** 2026-07-10

---

## SWR_CLS_00014: Class Command Execution Logging

**ID:** SWR_CLS_00014
**Title:** class commands log execution steps at INFO level
**Status:** Planned
**Priority:** Medium
**Description:**
The class commands SHALL emit INFO-level log messages showing execution progress, enabling end-users to understand what the CLI is doing at each stage (mirrors SWR_PKG_0014 for the package command):

**Class Create Logging:**
- SHALL log "Starting class creation..." at operation start
- SHALL log "Resolving parent path 'X'..." before path resolution
- SHALL log "Creating class 'Y'..." for each class being created
- SHALL log "Setting attributes for class 'Y'..." when attributes (beyond name) are being set
- SHALL log "Created class: Z" for each successfully created class
- SHALL log "Successfully created N class(es)" with count summary at completion

**Class Delete Logging:**
- SHALL log "Starting class deletion..." at operation start
- SHALL log "Resolving class path/GUID 'X'..." before path resolution
- SHALL log "Deleting class 'X'..." before deletion
- SHALL log "Successfully deleted class 'X'" after successful deletion

**Class View Logging:**
- SHALL log "Starting class view operation..." at operation start
- SHALL log "Resolving class path/GUID 'X'..." before path resolution
- SHALL log "Retrieving class details..." before data collection
- SHALL log "Writing output to file 'X'" when writing to file (when --output specified)

**Class List Logging:**
- SHALL log "Starting class list operation..." at operation start
- SHALL log "Resolving package path 'X'..." before path resolution
- SHALL log "Listing classes..." before collection
- SHALL log "Found N class(es)" or "No classes found" with count
- SHALL log "Writing output to file 'X'" when writing to file (when --output specified)

**Class Link Logging:**
- SHALL log "Starting class link operation..." at operation start
- SHALL log "Resolving source class path/GUID 'X'..." before path resolution
- SHALL log "Resolving target class 'Y'..." before target lookup
- SHALL log "Adding generalization to 'Y'..." or "Removing generalization from 'Y'..." before the operation
- SHALL log "Successfully updated generalization for class 'X'" after success

**Common Requirements:**
- All execution-step logs SHALL use INFO level (visible by default, not requiring --verbose flag)
- Error logs for operation failures SHALL use ERROR level (already in place per SWR_CLS_00010)
- Logs SHALL be emitted to the standard logger for the class_action module
**Implementation:** src/rhapsody_cli/actions/class_action.py (all 5 action classes)
**Last Changed:** 2026-07-10

---

## SWR_CLS_00015: Class Create Duplicate Detection

**ID:** SWR_CLS_00015
**Title:** class create detects and reports duplicate class names
**Status:** Planned
**Priority:** High
**Description:**
The class CLI (mirrors SWR_PKG_0015 for the package command)
- SHALL detect when a class with the given name already exists in the target parent (Package or Project) before attempting creation
- SHALL report a user-friendly error message when a duplicate class name is detected
- Error message SHALL follow the format: `"Class 'X' already exists in [project root|package 'Y']"`
- Duplicate detection SHALL use case-sensitive name comparison (matching Rhapsody behavior)
- Duplicate detection SHALL be performed by iterating through existing classes via `getClasses()` on the parent
- When a duplicate is detected, SHALL raise `CliExecutionError` with the user-friendly message (not allow COM exception to bubble up)
- Duplicate check SHALL occur before attempting the `addClass()` COM call (fail-fast approach)
- Logging SHALL include "Checking if class 'X' already exists..." before the check
- If the duplicate check itself fails (e.g., `getClasses()` COM error), SHALL log at DEBUG level and continue with creation attempt (duplicate check is a convenience, not a hard blocker)
- SHALL also detect the underlying COM error code (`-2147221495`) as a fallback signal if `addClass()` fails after a duplicate check that could not confirm existence, converting it to the same user-friendly message rather than letting the raw COM exception propagate
- Attribute-setting failures after successful `addClass()` SHALL NOT be treated as creation failures: SHALL wrap attribute-setting calls in try/except, log WARNING on failure, and still report the class as created (mirrors the fix applied to `PackageCreateAction._create_single_package`)
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassCreateAction._check_class_not_exists
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_cls_requirements.md
git commit -m "docs: Add SW requirements for class command (SWR_CLS_00001-00013)"
```

---

## Phase 2: AbstractClassAction Base Class

### Task 2: Create AbstractClassAction Base Class

**Files:**
- Create: `src/rhapsody_cli/actions/class_action.py`
- Test: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `ElementManagementAction` from `src/rhapsody_cli/actions/abstract_action.py`
- Produces:
  - `AbstractClassAction` class with:
    - `_resolve_and_validate_package(path) -> Any` — validates metaClass in `{"Package", "Project"}`
    - `_resolve_and_validate_class(path) -> Any` — validates metaClass == `"Class"`
    - `_resolve_class_by_guid(guid) -> Any` — locates class via `findElementByGUID` on active project, validates metaClass == `"Class"`
  - Module-level `logger = logging.getLogger(__name__)`

- [ ] **Step 1: Write test for AbstractClassAction**

Create `tests/unit/actions/test_class_action.py`:

```python
"""Tests for class actions."""

from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.class_action import AbstractClassAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractClassAction:
    """Test AbstractClassAction base class.

    SWR_CLS_00005: Path Validation
    SWR_CLS_00010: Error Handling and Logging
    SWR_CLS_00013: GUID Lookup Support
    """

    def test_resolve_and_validate_package_success_package(self) -> None:
        """Test successful package resolution for create/list."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_package,
            ):
                result = action._resolve_and_validate_package("Sensors")
                assert result == mock_package

    def test_resolve_and_validate_package_success_project(self) -> None:
        """Test project root accepted as package parent (RPProject inherits addClass)."""
        action = AbstractClassAction()
        mock_project = MagicMock()
        mock_project.getMetaClass.return_value = "Project"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_project,
            ):
                result = action._resolve_and_validate_package("")
                assert result == mock_project

    def test_resolve_and_validate_package_not_package(self) -> None:
        """Test validation fails for non-package element."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_class,
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_package("Sensors/MyClass")

                assert "does not resolve to a Package or Project" in str(exc_info.value)
                assert "found Class" in str(exc_info.value)

    def test_resolve_and_validate_class_success(self) -> None:
        """Test successful class resolution for delete/view/link."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_class,
            ):
                result = action._resolve_and_validate_class("Sensors/TemperatureSensor")
                assert result == mock_class

    def test_resolve_and_validate_class_not_class(self) -> None:
        """Test validation fails for non-class element."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_element",
                return_value=mock_package,
            ):
                with pytest.raises(CliExecutionError) as exc_info:
                    action._resolve_and_validate_class("Sensors")

                assert "does not resolve to a Class" in str(exc_info.value)
                assert "found Package" in str(exc_info.value)

    def test_resolve_class_by_guid_success(self) -> None:
        """Test successful class lookup by GUID."""
        action = AbstractClassAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_project", return_value=MagicMock()) as mock_proj:
            mock_proj.return_value.findElementByGUID.return_value = mock_class

            result = action._resolve_class_by_guid("12345678-1234-1234-1234-123456789abc")
            assert result == mock_class
            mock_proj.return_value.findElementByGUID.assert_called_once_with(
                "12345678-1234-1234-1234-123456789abc"
            )

    def test_resolve_class_by_guid_not_class(self) -> None:
        """Test GUID lookup fails for non-class element."""
        action = AbstractClassAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(ElementManagementAction, "_get_active_project", return_value=MagicMock()) as mock_proj:
            mock_proj.return_value.findElementByGUID.return_value = mock_package

            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_class_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "does not resolve to a Class" in str(exc_info.value)
            assert "found Package" in str(exc_info.value)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/actions/test_class_action.py::TestAbstractClassAction -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.actions.class_action'`

- [ ] **Step 3: Implement AbstractClassAction**

Create `src/rhapsody_cli/actions/class_action.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/actions/test_class_action.py::TestAbstractClassAction -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit base class**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Add AbstractClassAction base class with path and GUID validation"
```

---

## Phase 3: ClassCreateAction Implementation

### Task 3: Implement ClassCreateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction._resolve_and_validate_package(path)`
- Produces: `ClassCreateAction` with:
  - `VALID_ATTRIBUTES` class constant (set of strings)
  - `init_arguments(sub_parser)` — registers `create` subparser with `--path`, `--input`, `attributes`
  - `execute(args)` — creates classes from JSON
  - `_load_json_data(input) -> Any` — loads inline JSON or file (UTF-8)
  - `_set_attributes(cls, attrs)` — orchestrates 8 attribute setters
  - `_set_basic_attributes(cls, attrs)` — description
  - `_set_boolean_flags(cls, attrs)` — isAbstract, isFinal, isActive
  - `_set_properties(cls, attrs)` — tags via `setPropertyValue`
  - `_set_stereotypes(cls, attrs)` — `addStereotype(name, "Class")`
  - `_set_operations(cls, attrs)` — `addOperation(name)`
  - `_set_attributes_list(cls, attrs)` — `addAttribute(name)`
  - `_set_superclasses(cls, parent, cls, attrs)` — resolves names via `parent.findNestedClassifierRecursive(name)`, then `cls.addGeneralization(target)`

- [ ] **Step 1: Write tests for ClassCreateAction**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassCreateAction:
    """Test ClassCreateAction.

    UTS_CLS_00001: Create single class with inline JSON
    UTS_CLS_00002: Create multiple classes from JSON file
    UTS_CLS_00003: Create with stereotypes
    UTS_CLS_00004: Create with tags
    UTS_CLS_00005: Create with boolean flags
    UTS_CLS_00006: Create with operations
    UTS_CLS_00007: Create with attributes
    UTS_CLS_00008: Create with superclasses
    UTS_CLS_00009: Create skips unknown attributes
    UTS_CLS_00010: Create fails without name
    """

    def _make_action_with_parent(self) -> tuple:
        """Helper: build action and mock parent package."""
        from rhapsody_cli.actions.class_action import ClassCreateAction

        action = ClassCreateAction()
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        return action, mock_parent

    def test_create_single_class_inline_json(self) -> None:
        """UTS_CLS_00001: Test creating single class with inline JSON."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TemperatureSensor","description":"Temp sensor"}'

            action.execute(args)

            mock_parent.addClass.assert_called_once_with("TemperatureSensor")
            mock_class.setDescription.assert_called_once_with("Temp sensor")

    def test_create_bulk_classes_from_file(self, tmp_path) -> None:
        """UTS_CLS_00002: Test creating multiple classes from JSON file."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        json_file = tmp_path / "classes.json"
        json_file.write_text(
            '[{"name":"TempSensor"},{"name":"PressureSensor"}]', encoding="utf-8"
        )

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            assert mock_parent.addClass.call_count == 2

    def test_create_with_stereotypes(self) -> None:
        """UTS_CLS_00003: Test stereotypes applied via addStereotype(name, 'Class')."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","stereotypes":["active","boundary"]}'

            action.execute(args)

            assert mock_class.addStereotype.call_count == 2
            mock_class.addStereotype.assert_any_call("active", "Class")
            mock_class.addStereotype.assert_any_call("boundary", "Class")

    def test_create_with_tags(self) -> None:
        """UTS_CLS_00004: Test tags set via setPropertyValue."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","tags":{"status":"active","level":"3"}}'

            action.execute(args)

            assert mock_class.setPropertyValue.call_count == 2
            mock_class.setPropertyValue.assert_any_call("status", "active")
            mock_class.setPropertyValue.assert_any_call("level", "3")

    def test_create_with_boolean_flags(self) -> None:
        """UTS_CLS_00005: Test isAbstract/isFinal/isActive set via setIsX(1/0)."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","isAbstract":true,"isFinal":false,"isActive":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setIsFinal.assert_called_once_with(0)
            mock_class.setIsActive.assert_called_once_with(1)

    def test_create_with_operations(self) -> None:
        """UTS_CLS_00006: Test operations added via addOperation."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","operations":["readValue","setThreshold"]}'

            action.execute(args)

            assert mock_class.addOperation.call_count == 2
            mock_class.addOperation.assert_any_call("readValue")
            mock_class.addOperation.assert_any_call("setThreshold")

    def test_create_with_attributes_list(self) -> None:
        """UTS_CLS_00007: Test attributes added via addAttribute."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","attributes":["threshold","unit"]}'

            action.execute(args)

            assert mock_class.addAttribute.call_count == 2
            mock_class.addAttribute.assert_any_call("threshold")
            mock_class.addAttribute.assert_any_call("unit")

    def test_create_with_superclasses(self) -> None:
        """UTS_CLS_00008: Test superclasses resolved via findNestedClassifierRecursive."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class
        mock_base = MagicMock()
        mock_parent.findNestedClassifierRecursive.return_value = mock_base

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","superclasses":["BaseSensor"]}'

            action.execute(args)

            mock_parent.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_class.addGeneralization.assert_called_once_with(mock_base)

    def test_create_skips_unknown_attributes(self) -> None:
        """UTS_CLS_00009: Test unknown attributes skipped with warning."""
        action, mock_parent = self._make_action_with_parent()
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_warning.assert_called_once()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_create_missing_name_raises_error(self) -> None:
        """UTS_CLS_00010: Test missing name raises CliExecutionError."""
        action, mock_parent = self._make_action_with_parent()

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"description":"No name"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "'name' is required" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassCreateAction -v`
Expected: FAIL with `ImportError: cannot import name 'ClassCreateAction'`

- [ ] **Step 3: Implement ClassCreateAction**

Append to `src/rhapsody_cli/actions/class_action.py`:

```python
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

        SWR_CLS_00006: External JSON File Support
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassCreateAction -v`
Expected: PASS (10 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit ClassCreateAction**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Implement ClassCreateAction with bulk creation and 8 attribute setters"
```

---

## Phase 4: ClassDeleteAction Implementation

### Task 4: Implement ClassDeleteAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction._resolve_and_validate_class(path)` and `_resolve_class_by_guid(guid)`
- Produces: `ClassDeleteAction` with `init_arguments()` and `execute()`; accepts `--path` or `--guid` (exactly one required)

- [ ] **Step 1: Write tests for ClassDeleteAction**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassDeleteAction:
    """Test ClassDeleteAction.

    UTS_CLS_00011: Delete class by path
    UTS_CLS_00012: Delete class by GUID
    UTS_CLS_00013: Delete handles COM error
    UTS_CLS_00014: Delete requires path or guid
    """

    def test_delete_class_by_path_success(self) -> None:
        """UTS_CLS_00011: Test successful class deletion by path."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/OldClass"
            args.guid = None

            action.execute(args)

            mock_class.deleteFromProject.assert_called_once()

    def test_delete_class_by_guid_success(self) -> None:
        """UTS_CLS_00012: Test successful class deletion by GUID."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"

            action.execute(args)

            mock_class.deleteFromProject.assert_called_once()

    def test_delete_class_handles_com_error(self) -> None:
        """UTS_CLS_00013: Test error handling during deletion."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"
        mock_class.deleteFromProject.side_effect = Exception("COM error")

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/OldClass"
            args.guid = None

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "COM error" in str(exc_info.value)

    def test_delete_requires_path_or_guid(self) -> None:
        """UTS_CLS_00014: Test that exactly one of path/guid is required."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        args = MagicMock()
        args.path = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid must be specified" in str(exc_info.value)

    def test_delete_rejects_both_path_and_guid(self) -> None:
        """Test that specifying both path and guid is rejected."""
        from rhapsody_cli.actions.class_action import ClassDeleteAction

        action = ClassDeleteAction()
        args = MagicMock()
        args.path = "Sensors/X"
        args.guid = "12345678-1234-1234-1234-123456789abc"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Only one of --path or --guid" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassDeleteAction -v`
Expected: FAIL with `ImportError: cannot import name 'ClassDeleteAction'`

- [ ] **Step 3: Implement ClassDeleteAction**

Append to `src/rhapsody_cli/actions/class_action.py`:

```python
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
            cls.deleteFromProject()
            self.logger.info("Deleted class: %s", label)
        except Exception as e:
            self._handle_execution_error(e, f"Failed to delete class '{label}'")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassDeleteAction -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit ClassDeleteAction**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Implement ClassDeleteAction with path and GUID lookup"
```

---

## Phase 5: ClassViewAction Implementation

### Task 5: Implement ClassViewAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction._resolve_and_validate_class(path)` and `_resolve_class_by_guid(guid)`
- Produces: `ClassViewAction` with multi-format output (table/JSON/CSV), `--path` or `--guid` lookup, 12 view fields

- [ ] **Step 1: Write tests for ClassViewAction**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassViewAction:
    """Test ClassViewAction.

    UTS_CLS_00015: View table output
    UTS_CLS_00016: View JSON output to file
    UTS_CLS_00017: View CSV output
    UTS_CLS_00018: View by GUID
    UTS_CLS_00019: View requires path or guid
    UTS_CLS_00020: View normalizes IsAbstract to int in JSON
    """

    def _make_mock_class(self) -> MagicMock:
        """Helper: build a fully-populated mock class."""
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"
        mock_class.getName.return_value = "TemperatureSensor"
        mock_class.getGUID.return_value = "12345678-1234-1234-1234-123456789abc"
        mock_class.getDescription.return_value = "Temperature sensor"
        mock_class.getIsAbstract.return_value = True  # bool
        mock_class.getIsActive.return_value = 1
        mock_class.getIsFinal.return_value = 0
        mock_class.getIsComposite.return_value = 0
        mock_class.getIsReactive.return_value = 0
        mock_class.getFullPathName.return_value = "Sensors/TemperatureSensor"

        op1 = MagicMock()
        op1.getName.return_value = "readValue"
        op2 = MagicMock()
        op2.getName.return_value = "setThreshold"
        mock_class.getOperations.return_value = [op1, op2]

        attr1 = MagicMock()
        attr1.getName.return_value = "threshold"
        attr2 = MagicMock()
        attr2.getName.return_value = "unit"
        mock_class.getAttributes.return_value = [attr1, attr2]

        return mock_class

    def test_view_table_output(self, capsys) -> None:
        """UTS_CLS_00015: Test table format output."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out
            assert "Property" in captured.out
            assert "readValue, setThreshold" in captured.out

    def test_view_json_output_to_file(self, tmp_path) -> None:
        """UTS_CLS_00016: Test JSON output to file with int-normalized IsAbstract."""
        from rhapsody_cli.actions.class_action import ClassViewAction
        import json as json_module

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            output_file = tmp_path / "class.json"
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "json"
            args.output = str(output_file)

            action.execute(args)

            data = json_module.loads(output_file.read_text())
            assert data["name"] == "TemperatureSensor"
            assert data["guid"] == "12345678-1234-1234-1234-123456789abc"
            assert data["isAbstract"] == 1  # bool True normalized to int
            assert data["isActive"] == 1
            assert data["isFinal"] == 0
            assert data["operations"] == ["readValue", "setThreshold"]
            assert data["attributes"] == ["threshold", "unit"]

    def test_view_csv_output(self, capsys) -> None:
        """UTS_CLS_00017: Test CSV format output."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.format = "csv"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            lines = captured.out.strip().split("\n")
            assert len(lines) == 2
            assert "Name,GUID" in lines[0]
            assert "TemperatureSensor" in lines[1]

    def test_view_by_guid(self, capsys) -> None:
        """UTS_CLS_00018: Test viewing class by GUID."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        mock_class = self._make_mock_class()

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out

    def test_view_requires_path_or_guid(self) -> None:
        """UTS_CLS_00019: Test that exactly one of path/guid is required."""
        from rhapsody_cli.actions.class_action import ClassViewAction

        action = ClassViewAction()
        args = MagicMock()
        args.path = None
        args.guid = None

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid must be specified" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassViewAction -v`
Expected: FAIL with `ImportError: cannot import name 'ClassViewAction'`

- [ ] **Step 3: Implement ClassViewAction**

Append to `src/rhapsody_cli/actions/class_action.py`:

```python
class ClassViewAction(AbstractClassAction):
    """View class details.

    SWR_CLS_00003: Class View Command
    SWR_CLS_00008: Multi-Format Output
    SWR_CLS_00013: GUID Lookup Support
    """

    _VIEW_HEADERS = [
        "Name", "GUID", "Description",
        "IsAbstract", "IsActive", "IsFinal",
        "IsComposite", "IsReactive", "MetaClass", "FullPath",
        "Operations", "Attributes",
    ]
    _VIEW_KEYS = [
        "name", "guid", "description",
        "isAbstract", "isActive", "isFinal",
        "isComposite", "isReactive", "metaClass", "fullPath",
        "operations", "attributes",
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
        operations = cls.getOperations()
        attributes = cls.getAttributes()
        return {
            "name": cls.getName(),
            "guid": cls.getGUID(),
            "description": cls.getDescription(),
            "isAbstract": int(cls.getIsAbstract()),
            "isActive": int(cls.getIsActive()),
            "isFinal": int(cls.getIsFinal()),
            "isComposite": int(cls.getIsComposite()),
            "isReactive": int(cls.getIsReactive()),
            "metaClass": cls.getMetaClass(),
            "fullPath": cls.getFullPathName(),
            "operations": [op.getName() for op in operations],
            "attributes": [attr.getName() for attr in attributes],
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassViewAction -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit ClassViewAction**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Implement ClassViewAction with 12-field multi-format output"
```

---

## Phase 6: ClassListAction Implementation

### Task 6: Implement ClassListAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction._resolve_and_validate_package(path)`
- Produces: `ClassListAction` listing class names via `getClasses()` and `getName()`

- [ ] **Step 1: Write tests for ClassListAction**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassListAction:
    """Test ClassListAction.

    UTS_CLS_00021: List classes in package
    UTS_CLS_00022: List empty package
    UTS_CLS_00023: List JSON output
    """

    def test_list_classes(self, capsys) -> None:
        """UTS_CLS_00021: Test listing classes in a package."""
        from rhapsody_cli.actions.class_action import ClassListAction

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        cls1 = MagicMock()
        cls1.getName.return_value = "TemperatureSensor"
        cls2 = MagicMock()
        cls2.getName.return_value = "PressureSensor"
        mock_package.getClasses.return_value = [cls1, cls2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            assert "TemperatureSensor" in captured.out
            assert "PressureSensor" in captured.out

    def test_list_empty_package(self, capsys) -> None:
        """UTS_CLS_00022: Test listing empty package."""
        from rhapsody_cli.actions.class_action import ClassListAction

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        mock_package.getClasses.return_value = []

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "EmptyPackage"
            args.format = "table"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            # Should produce empty table (no data)

    def test_list_json_output(self, capsys) -> None:
        """UTS_CLS_00023: Test JSON output format."""
        from rhapsody_cli.actions.class_action import ClassListAction
        import json as json_module

        action = ClassListAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"
        cls1 = MagicMock()
        cls1.getName.return_value = "TemperatureSensor"
        cls2 = MagicMock()
        cls2.getName.return_value = "PressureSensor"
        mock_package.getClasses.return_value = [cls1, cls2]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors"
            args.format = "json"
            args.output = None

            action.execute(args)

            captured = capsys.readouterr()
            data = json_module.loads(captured.out)
            assert data == ["TemperatureSensor", "PressureSensor"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassListAction -v`
Expected: FAIL with `ImportError: cannot import name 'ClassListAction'`

- [ ] **Step 3: Implement ClassListAction**

Append to `src/rhapsody_cli/actions/class_action.py`:

```python
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
        classes = package.getClasses()
        return [cls.getName() for cls in classes]

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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassListAction -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit ClassListAction**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Implement ClassListAction for listing classes in a package"
```

---

## Phase 7: ClassLinkAction Implementation

### Task 7: Implement ClassLinkAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction._resolve_and_validate_class(path)` and `_resolve_class_by_guid(guid)`
- Produces: `ClassLinkAction` with:
  - `init_arguments()` — registers `--path`/`--guid` (one required), `--add`/`--remove` (one required), `--type` (default generalization)
  - `execute()` — resolves source class, resolves target via `findNestedClassifierRecursive(name)`, calls `addGeneralization` or `deleteGeneralization`

- [ ] **Step 1: Write tests for ClassLinkAction**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassLinkAction:
    """Test ClassLinkAction.

    UTS_CLS_00024: Add generalization by name
    UTS_CLS_00025: Remove generalization by name
    UTS_CLS_00026: Link requires add or remove
    UTS_CLS_00027: Link target not found raises error
    UTS_CLS_00028: Link by GUID
    """

    def test_add_generalization_by_path(self) -> None:
        """UTS_CLS_00024: Test adding generalization by name."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.add = "BaseSensor"
            args.remove = None
            args.type = "generalization"

            action.execute(args)

            mock_source.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_source.addGeneralization.assert_called_once_with(mock_target)

    def test_remove_generalization_by_path(self) -> None:
        """UTS_CLS_00025: Test removing generalization by name."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.add = None
            args.remove = "BaseSensor"
            args.type = "generalization"

            action.execute(args)

            mock_source.findNestedClassifierRecursive.assert_called_once_with("BaseSensor")
            mock_source.deleteGeneralization.assert_called_once_with(mock_target)

    def test_link_requires_add_or_remove(self) -> None:
        """UTS_CLS_00026: Test that exactly one of add/remove is required."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        args = MagicMock()
        args.path = "Sensors/X"
        args.guid = None
        args.add = None
        args.remove = None
        args.type = "generalization"

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --add or --remove must be specified" in str(exc_info.value)

    def test_link_target_not_found_raises_error(self) -> None:
        """UTS_CLS_00027: Test that missing target raises error."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_source.findNestedClassifierRecursive.return_value = None

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_source):
            args = MagicMock()
            args.path = "Sensors/X"
            args.guid = None
            args.add = "NonExistent"
            args.remove = None
            args.type = "generalization"

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "Class 'NonExistent' not found" in str(exc_info.value)

    def test_link_by_guid(self) -> None:
        """UTS_CLS_00028: Test linking class by GUID."""
        from rhapsody_cli.actions.class_action import ClassLinkAction

        action = ClassLinkAction()
        mock_source = MagicMock()
        mock_source.getMetaClass.return_value = "Class"
        mock_target = MagicMock()

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_source):
            mock_source.findNestedClassifierRecursive.return_value = mock_target

            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.add = "BaseSensor"
            args.remove = None
            args.type = "generalization"

            action.execute(args)

            mock_source.addGeneralization.assert_called_once_with(mock_target)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassLinkAction -v`
Expected: FAIL with `ImportError: cannot import name 'ClassLinkAction'`

- [ ] **Step 3: Implement ClassLinkAction**

Append to `src/rhapsody_cli/actions/class_action.py`:

```python
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
        target = source.findNestedClassifierRecursive(target_name)
        if target is None:
            raise CliExecutionError(
                f"Class '{target_name}' not found"
            )

        try:
            if args.add:
                source.addGeneralization(target)
                self.logger.info(
                    "Added generalization: %s -> %s",
                    args.path or args.guid,
                    target_name,
                )
            else:
                source.deleteGeneralization(target)
                self.logger.info(
                    "Removed generalization: %s -/-> %s",
                    args.path or args.guid,
                    target_name,
                )
        except Exception as e:
            self._handle_execution_error(
                e, f"Failed to modify generalization for class '{args.path or args.guid}'"
            )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassLinkAction -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit ClassLinkAction**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Implement ClassLinkAction for generalization relationships"
```

---

## Phase 8: ClassCommand Dispatcher

### Task 8: Implement ClassCommand Dispatcher

**Files:**
- Create: `src/rhapsody_cli/commands/class_command.py`
- Create: `tests/unit/commands/test_class_command.py`
- Modify: `src/rhapsody_cli/cli/cli.py`

**Interfaces:**
- Consumes: 5 Action classes (`ClassCreateAction`, `ClassDeleteAction`, `ClassViewAction`, `ClassListAction`, `ClassLinkAction`)
- Produces: `ClassCommand` class extending `AbstractCommand` with `get_actions()` returning the 5 actions

- [ ] **Step 1: Write test for ClassCommand**

Create `tests/unit/commands/test_class_command.py`:

```python
"""Tests for ClassCommand dispatcher.

UTS_CLS_00029: ClassCommand registers all subcommands
"""

import pytest

from rhapsody_cli.commands.class_command import ClassCommand
from rhapsody_cli.exceptions import CliExecutionError


class TestClassCommand:
    """Test ClassCommand dispatcher."""

    def test_command_id_is_class(self) -> None:
        """Test that command name is 'class'."""
        cmd = ClassCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        assert cmd._subcommand == "create"

    def test_missing_subcommand_raises_error(self) -> None:
        """Test that missing subcommand raises error."""
        with pytest.raises(CliExecutionError):
            ClassCommand([])

    def test_registers_all_five_subcommands(self) -> None:
        """UTS_CLS_00029: Test that all 5 subcommands are registered."""
        cmd = ClassCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "link" in command_ids
        assert len(actions) == 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/commands/test_class_command.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.commands.class_command'`

- [ ] **Step 3: Implement ClassCommand**

Create `src/rhapsody_cli/commands/class_command.py`:

```python
"""Class command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.class_action import (
    ClassCreateAction,
    ClassDeleteAction,
    ClassLinkAction,
    ClassListAction,
    ClassViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ClassCommand(AbstractCommand):
    """Class command group - handles class subcommands (create, delete, view, list, link)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize ClassCommand and parse class subcommands.

        Args:
            args: Arguments after 'class' command
                (e.g., ['create', '--path', 'Sensors', '{"name":"Temp"}'])
        """
        super().__init__("class", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the class subcommand actions."""
        return [
            ClassCreateAction(),
            ClassDeleteAction(),
            ClassViewAction(),
            ClassListAction(),
            ClassLinkAction(),
        ]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/commands/test_class_command.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Register in main CLI**

Modify `src/rhapsody_cli/cli/cli.py` to add the class command. Add the import after the package_command import:

```python
from rhapsody_cli.commands.class_command import ClassCommand
```

Add the dispatch branch after the `package` branch:

```python
elif command_name == "class":
    cmd = ClassCommand(command_args)
```

Update the usage text in `_usage()`:

```python
commands_text = "Commands:\n  element    Manage model elements\n"
commands_text += "  package    Manage packages\n  project    Manage projects\n"
commands_text += "  class      Manage classes\n"
```

- [ ] **Step 6: Run all tests to verify nothing broke**

Run: `pytest tests/unit -v`
Expected: All existing tests + new tests pass

- [ ] **Step 7: Run linters**

Run: `ruff check src/ tests/ ; mypy src/`
Expected: No errors

- [ ] **Step 8: Commit ClassCommand**

```bash
git add src/rhapsody_cli/commands/class_command.py tests/unit/commands/test_class_command.py src/rhapsody_cli/cli/cli.py
git commit -m "feat: Add ClassCommand dispatcher and register in CLI"
```

---

## Phase 9: User Guide Documentation

### Task 9: Write User Guide Documentation

**Files:**
- Create: `docs/user_guide/working_with_classes.rst`

- [ ] **Step 1: Create working_with_classes.rst**

Create `docs/user_guide/working_with_classes.rst`:

```restructuredtext
Working with Classes
====================

The ``class`` command provides operations for managing Rhapsody class elements
via CLI. It mirrors the ``package`` command structure and adds support for
class-specific features like boolean flags, operations, attributes, and
generalization relationships.

Synopsis
--------

::

   rhapsody-cli class <subcommand> [options]

Subcommands
-----------

create
   Create one or multiple classes

delete
   Delete a class

view
   View class details

list
   List classes in a package

link
   Add or remove generalization relationships

class create
------------

Create one or multiple classes with validated attributes.

**Usage:**

::

   rhapsody-cli class create --path <parent-package-path> [options] [attributes]

**Arguments:**

- ``--path <parent-package-path>`` - Parent package path (required). Accepts
  package or project root.
- ``--input <json-file>`` - JSON file with class attributes (optional)
- ``attributes`` - Inline JSON or file path (required if --input not specified)

**Examples:**

Create single class with inline JSON::

   rhapsody-cli class create --path Sensors '{"name":"TemperatureSensor","description":"Temp sensor"}'

Create multiple classes from file::

   rhapsody-cli class create --path Sensors --input classes.json

**JSON Format (single class):**

::

   {
     "name": "TemperatureSensor",
     "description": "Temperature sensor class",
     "isAbstract": false,
     "isFinal": false,
     "isActive": false,
     "stereotypes": ["active"],
     "tags": {"status": "active"},
     "operations": ["readValue", "setThreshold"],
     "attributes": ["threshold", "unit"],
     "superclasses": ["BaseSensor"]
   }

**Validated Attributes:**

- ``name`` (required) - Class name
- ``description`` - Plain text description
- ``isAbstract`` - Boolean, sets via setIsAbstract(1/0)
- ``isFinal`` - Boolean, sets via setIsFinal(1/0)
- ``isActive`` - Boolean, sets via setIsActive(1/0)
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Object of key-value pairs
- ``operations`` - Array of operation names
- ``attributes`` - Array of attribute names
- ``superclasses`` - Array of superclass names (resolved via findNestedClassifierRecursive)

class delete
------------

Delete a class by path or GUID.

**Usage:**

::

   rhapsody-cli class delete --path <class-path>
   rhapsody-cli class delete --guid <guid>

**Arguments:**

- ``--path <class-path>`` - Class path to delete (optional)
- ``--guid <guid>`` - Class GUID to delete (format: 12345678-1234-1234-1234-123456789abc)

Exactly one of ``--path`` or ``--guid`` must be specified.

**Example:**

::

   rhapsody-cli class delete --path Sensors/OldClass
   rhapsody-cli class delete --guid 12345678-1234-1234-1234-123456789abc

class view
----------

View class details in various formats.

**Usage:**

::

   rhapsody-cli class view --path <class-path> [options]
   rhapsody-cli class view --guid <guid> [options]

**Arguments:**

- ``--path <class-path>`` - Class path to view (optional)
- ``--guid <guid>`` - Class GUID to view (optional)
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

Exactly one of ``--path`` or ``--guid`` must be specified.

**View Fields:**

Name, GUID, Description, IsAbstract, IsActive, IsFinal, IsComposite,
IsReactive, MetaClass, FullPath, Operations, Attributes

**Output Formats:**

Table (default)::

   Property     | Value
   -------------|---------------------
   Name         | TemperatureSensor
   GUID         | 12345678-...
   IsAbstract   | 0
   Operations   | readValue, setThreshold
   Attributes   | threshold, unit

JSON::

   {
     "name": "TemperatureSensor",
     "guid": "12345678-...",
     "isAbstract": 0,
     "operations": ["readValue", "setThreshold"],
     "attributes": ["threshold", "unit"]
   }

CSV (horizontal)::

   Name,GUID,Description,IsAbstract,...,Operations,Attributes
   TemperatureSensor,12345678-...,Temp sensor,0,...,"readValue,setThreshold","threshold,unit"

class list
----------

List classes in a package.

**Usage:**

::

   rhapsody-cli class list --path <package-path> [options]

**Arguments:**

- ``--path <package-path>`` - Package path (required). Accepts package or project root.
- ``--format <format>`` - Output format: table, json, csv (default: table)
- ``--output <file>`` - Write to file instead of stdout (optional)

**Output Formats:**

Table::

   +--------------------+
   | Name               |
   +--------------------+
   | TemperatureSensor  |
   | PressureSensor     |
   +--------------------+

JSON::

   ["TemperatureSensor", "PressureSensor"]

CSV::

   Name
   TemperatureSensor
   PressureSensor

class link
----------

Add or remove generalization relationships between classes.

**Usage:**

::

   rhapsody-cli class link --path <class-path> --add <target-name>
   rhapsody-cli class link --path <class-path> --remove <target-name>
   rhapsody-cli class link --guid <guid> --add <target-name>

**Arguments:**

- ``--path <class-path>`` - Source class path (optional)
- ``--guid <guid>`` - Source class GUID (optional)
- ``--add <class-name>`` - Add a generalization to target class by name
- ``--remove <class-name>`` - Remove a generalization to target class by name
- ``--type <generalization>`` - Relationship type (default: generalization;
  v1 supports only generalization)

Exactly one of ``--path`` or ``--guid`` must be specified. Exactly one of
``--add`` or ``--remove`` must be specified.

**Examples:**

::

   # Add generalization
   rhapsody-cli class link --path Sensors/TemperatureSensor --add BaseSensor

   # Remove generalization
   rhapsody-cli class link --path Sensors/TemperatureSensor --remove BaseSensor

   # Using GUID
   rhapsody-cli class link --guid 12345678-1234-1234-1234-123456789abc --add BaseSensor

Workflow: Class Cloning
-----------------------

The ``view`` command's JSON output can be reused as ``create`` command input:

**Step 1:** Export class to JSON::

   rhapsody-cli class view --path Sensors/TemperatureSensor --format json --output template.json

**Step 2:** Edit template.json (modify name, description, etc.)

**Step 3:** Create new class from template::

   rhapsody-cli class create --path NewSensors template.json

Unknown fields (``guid``, ``isComposite``, ``isReactive``, ``metaClass``,
``fullPath``) are skipped during create with a warning. All other fields
round-trip cleanly.

Error Handling
--------------

All commands validate the path before execution:

- Path must exist in the model
- Path must resolve to the expected element type (Package/Project for create/list;
  Class for delete/view/link)
- Invalid path raises ``CliExecutionError``

See Also
--------

- :doc:`working_with_packages` - Package management operations
- :doc:`working_with_elements` - Generic element operations
```

- [ ] **Step 2: Commit documentation**

```bash
git add docs/user_guide/working_with_classes.rst
git commit -m "docs: Add user guide for class command"
```

---

## Phase 10: Unit Test Specifications Documentation

### Task 10: Document Unit Test Specs

**Files:**
- Create: `docs/tests/unit/uts_cls_test-specs.md`

- [ ] **Step 1: Create test spec file**

Create `docs/tests/unit/uts_cls_test-specs.md`:

```markdown
# Unit Test Specifications - Class Command

**Category:** Class Command
**Prefix:** UTS_CLS
**Test Type:** Unit
**Last Validated:** 2026-07-10

---

## UTS_CLS_00001: Create single class with inline JSON

**ID:** UTS_CLS_00001
**Traces-To:** SWR_CLS_00001
**Title:** Create single class with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single class can be created with inline JSON containing name and description.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent package exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call ClassCreateAction with inline JSON
2. Verify class created via addClass
3. Verify description set via setDescription
**Expected Result:**
Class created successfully with correct name and description.
**Verification Criteria:**
- addClass called once with correct name
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00002: Create multiple classes from JSON file

**ID:** UTS_CLS_00002
**Traces-To:** SWR_CLS_00001, SWR_CLS_00006
**Title:** Create multiple classes from JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of classes from external JSON file with array of class definitions.
**Pre-conditions:**
- JSON file exists with valid array of class definitions
- Parent package exists
**Test Steps:**
1. Call ClassCreateAction with --input pointing to JSON file
2. Verify file read with UTF-8 encoding
3. Verify all classes created
**Expected Result:**
All classes created, logs show count.
**Verification Criteria:**
- File opened with UTF-8 encoding
- addClass called for each class
- Logger shows total count
**Last Changed:** 2026-07-10

---

## UTS_CLS_00003: Create with stereotypes

**ID:** UTS_CLS_00003
**Traces-To:** SWR_CLS_00007
**Title:** Create class with stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that stereotypes are applied to class during creation.
**Pre-conditions:**
- JSON contains stereotypes array
**Test Steps:**
1. Call ClassCreateAction with JSON containing stereotypes
2. Verify addStereotype called for each stereotype
**Expected Result:**
All stereotypes applied correctly with "Class" type.
**Verification Criteria:**
- addStereotype called once per stereotype
- Correct stereotype name and "Class" type passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00004: Create with tags

**ID:** UTS_CLS_00004
**Traces-To:** SWR_CLS_00007
**Title:** Create class with tags
**Type:** Unit
**Priority:** Medium
**Description:**
Test that tags are set on class during creation.
**Pre-conditions:**
- JSON contains tags object
**Test Steps:**
1. Call ClassCreateAction with JSON containing tags
2. Verify setPropertyValue called for each tag
**Expected Result:**
All tags set correctly.
**Verification Criteria:**
- setPropertyValue called once per tag
- Correct key-value pairs passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00005: Create with boolean flags

**ID:** UTS_CLS_00005
**Traces-To:** SWR_CLS_00012
**Title:** Create class with boolean flags isAbstract, isFinal, isActive
**Type:** Unit
**Priority:** Medium
**Description:**
Test that boolean flags are set on class during creation.
**Pre-conditions:**
- JSON contains isAbstract, isFinal, isActive fields
**Test Steps:**
1. Call ClassCreateAction with JSON containing boolean flags
2. Verify setIsAbstract, setIsFinal, setIsActive called with 1/0
**Expected Result:**
All boolean flags set correctly.
**Verification Criteria:**
- setIsAbstract called with 1 if true, 0 if false
- setIsFinal called with 1/0
- setIsActive called with 1/0
**Last Changed:** 2026-07-10

---

## UTS_CLS_00006: Create with operations

**ID:** UTS_CLS_00006
**Traces-To:** SWR_CLS_00001
**Title:** Create class with operations
**Type:** Unit
**Priority:** Medium
**Description:**
Test that operations are added to class during creation.
**Pre-conditions:**
- JSON contains operations array
**Test Steps:**
1. Call ClassCreateAction with JSON containing operations
2. Verify addOperation called for each operation
**Expected Result:**
All operations added correctly.
**Verification Criteria:**
- addOperation called once per operation
- Correct operation names passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00007: Create with attributes

**ID:** UTS_CLS_00007
**Traces-To:** SWR_CLS_00001
**Title:** Create class with attributes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that attributes are added to class during creation.
**Pre-conditions:**
- JSON contains attributes array
**Test Steps:**
1. Call ClassCreateAction with JSON containing attributes
2. Verify addAttribute called for each attribute
**Expected Result:**
All attributes added correctly.
**Verification Criteria:**
- addAttribute called once per attribute
- Correct attribute names passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00008: Create with superclasses

**ID:** UTS_CLS_00008
**Traces-To:** SWR_CLS_00001
**Title:** Create class with superclasses
**Type:** Unit
**Priority:** Medium
**Description:**
Test that superclasses are resolved and generalizations added during creation.
**Pre-conditions:**
- JSON contains superclasses array
- Superclass names exist in parent package
**Test Steps:**
1. Call ClassCreateAction with JSON containing superclasses
2. Verify findNestedClassifierRecursive called for each superclass name
3. Verify addGeneralization called for each resolved target
**Expected Result:**
All generalizations added correctly.
**Verification Criteria:**
- findNestedClassifierRecursive called once per superclass name
- addGeneralization called once per resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00009: Create skips unknown attributes

**ID:** UTS_CLS_00009
**Traces-To:** SWR_CLS_00001, SWR_CLS_00009
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes in JSON are skipped and logged as warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call ClassCreateAction with JSON containing unknown fields
2. Verify class still created
3. Verify warning logged
**Expected Result:**
Class created, unknown fields skipped with warning.
**Verification Criteria:**
- Class created successfully
- Logger.warning called with unknown field names
**Last Changed:** 2026-07-10

---

## UTS_CLS_00010: Create fails without name

**ID:** UTS_CLS_00010
**Traces-To:** SWR_CLS_00001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name field is missing from JSON.
**Pre-conditions:**
- JSON does not contain name field
**Test Steps:**
1. Call ClassCreateAction with JSON without name
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with appropriate message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "'name' is required"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00011: Delete class by path

**ID:** UTS_CLS_00011
**Traces-To:** SWR_CLS_00002
**Title:** Delete class by path successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that a class is deleted successfully by path.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassDeleteAction with valid path
2. Verify deleteFromProject called
3. Verify log message shown
**Expected Result:**
Class deleted with log message.
**Verification Criteria:**
- deleteFromProject called once
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00012: Delete class by GUID

**ID:** UTS_CLS_00012
**Traces-To:** SWR_CLS_00002, SWR_CLS_00013
**Title:** Delete class by GUID successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that a class is deleted successfully by GUID.
**Pre-conditions:**
- Class exists with specified GUID
**Test Steps:**
1. Call ClassDeleteAction with --guid parameter
2. Verify findElementByGUID called on project
3. Verify deleteFromProject called
**Expected Result:**
Class deleted with log message.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- deleteFromProject called once
**Last Changed:** 2026-07-10

---

## UTS_CLS_00013: Delete handles COM error

**ID:** UTS_CLS_00013
**Traces-To:** SWR_CLS_00010
**Title:** Delete handles COM error gracefully
**Type:** Unit
**Priority:** High
**Description:**
Test that COM errors during deletion are handled properly.
**Pre-conditions:**
- deleteFromProject raises exception
**Test Steps:**
1. Call ClassDeleteAction
2. Simulate COM error in deleteFromProject
3. Verify error handled
**Expected Result:**
Exception handled, CliExecutionError raised.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains original error
**Last Changed:** 2026-07-10

---

## UTS_CLS_00014: Delete requires path or guid

**ID:** UTS_CLS_00014
**Traces-To:** SWR_CLS_00002, SWR_CLS_00013
**Title:** Delete requires exactly one of path or guid
**Type:** Unit
**Priority:** High
**Description:**
Test that delete raises error when neither or both path and guid are specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassDeleteAction with neither path nor guid
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --path or --guid must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --path or --guid"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00015: View table output

**ID:** UTS_CLS_00015
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in table format
**Type:** Unit
**Priority:** High
**Description:**
Test that class details are displayed in table format with all 12 fields.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassViewAction with format=table
2. Verify table output contains all properties
**Expected Result:**
Table printed to stdout with all class properties.
**Verification Criteria:**
- Table contains Name, GUID, Description, IsAbstract, etc.
- Operations and Attributes shown as comma-separated
**Last Changed:** 2026-07-10

---

## UTS_CLS_00016: View JSON output to file

**ID:** UTS_CLS_00016
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in JSON format to file
**Type:** Unit
**Priority:** High
**Description:**
Test that class details are written to JSON file with int-normalized IsAbstract.
**Pre-conditions:**
- Class exists at specified path
- Output file path provided
**Test Steps:**
1. Call ClassViewAction with format=json and --output
2. Verify JSON file created
3. Verify JSON contains all 12 fields
4. Verify isAbstract is int (not bool)
**Expected Result:**
JSON file created with all class details, IsAbstract normalized to int.
**Verification Criteria:**
- File created at specified path
- JSON parseable and contains all fields
- isAbstract is 0 or 1 (not true/false)
**Last Changed:** 2026-07-10

---

## UTS_CLS_00017: View CSV output

**ID:** UTS_CLS_00017
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test that class details are displayed in CSV format with horizontal layout.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassViewAction with format=csv
2. Verify CSV output has header + data row
**Expected Result:**
CSV printed with horizontal layout (12 columns).
**Verification Criteria:**
- Output has exactly 2 lines
- Header row contains all 12 column names
- Data row present
**Last Changed:** 2026-07-10

---

## UTS_CLS_00018: View by GUID

**ID:** UTS_CLS_00018
**Traces-To:** SWR_CLS_00003, SWR_CLS_00013
**Title:** View class by GUID
**Type:** Unit
**Priority:** Medium
**Description:**
Test that class details can be viewed by GUID.
**Pre-conditions:**
- Class exists with specified GUID
**Test Steps:**
1. Call ClassViewAction with --guid parameter
2. Verify findElementByGUID called
3. Verify class details displayed
**Expected Result:**
Class details displayed.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- Output contains class name
**Last Changed:** 2026-07-10

---

## UTS_CLS_00019: View requires path or guid

**ID:** UTS_CLS_00019
**Traces-To:** SWR_CLS_00003, SWR_CLS_00013
**Title:** View requires exactly one of path or guid
**Type:** Unit
**Priority:** High
**Description:**
Test that view raises error when neither path nor guid is specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassViewAction with neither path nor guid
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --path or --guid must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --path or --guid"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00020: View normalizes IsAbstract to int in JSON

**ID:** UTS_CLS_00020
**Traces-To:** SWR_CLS_00003, SWR_CLS_00009
**Title:** View JSON normalizes IsAbstract bool to int
**Type:** Unit
**Priority:** Medium
**Description:**
Test that getIsAbstract() (which returns bool) is normalized to int in JSON output.
**Pre-conditions:**
- Class exists with IsAbstract=True
**Test Steps:**
1. Call ClassViewAction with format=json
2. Verify JSON output
3. Verify isAbstract field is 1 (not true)
**Expected Result:**
JSON output has isAbstract as 1, not true.
**Verification Criteria:**
- JSON parseable
- isAbstract is int (0 or 1)
- Round-trips cleanly with create's isAbstract input
**Last Changed:** 2026-07-10

---

## UTS_CLS_00021: List classes in package

**ID:** UTS_CLS_00021
**Traces-To:** SWR_CLS_00004
**Title:** List classes in a package
**Type:** Unit
**Priority:** High
**Description:**
Test that classes are listed correctly.
**Pre-conditions:**
- Package has classes
**Test Steps:**
1. Call ClassListAction with parent package path
2. Verify all class names shown
**Expected Result:**
List of class names.
**Verification Criteria:**
- getClasses called
- All class names shown
**Last Changed:** 2026-07-10

---

## UTS_CLS_00022: List empty package

**ID:** UTS_CLS_00022
**Traces-To:** SWR_CLS_00004
**Title:** List empty package returns empty output
**Type:** Unit
**Priority:** Medium
**Description:**
Test that empty output is shown for package with no classes.
**Pre-conditions:**
- Package has no classes
**Test Steps:**
1. Call ClassListAction
2. Verify empty output
**Expected Result:**
Empty table/list shown.
**Verification Criteria:**
- getClasses returns empty
- Output is empty
**Last Changed:** 2026-07-10

---

## UTS_CLS_00023: List JSON output

**ID:** UTS_CLS_00023
**Traces-To:** SWR_CLS_00004, SWR_CLS_00008
**Title:** List classes in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test that classes are listed in JSON array format.
**Pre-conditions:**
- Package has classes
**Test Steps:**
1. Call ClassListAction with format=json
2. Verify JSON array output
**Expected Result:**
JSON array of class names.
**Verification Criteria:**
- Output is valid JSON array
- Array contains all class names
**Last Changed:** 2026-07-10

---

## UTS_CLS_00024: Add generalization by name

**ID:** UTS_CLS_00024
**Traces-To:** SWR_CLS_00011
**Title:** Add generalization relationship by class name
**Type:** Unit
**Priority:** High
**Description:**
Test that a generalization is added by resolving target class name.
**Pre-conditions:**
- Source class exists
- Target class exists in same package
**Test Steps:**
1. Call ClassLinkAction with --add parameter
2. Verify findNestedClassifierRecursive called
3. Verify addGeneralization called
**Expected Result:**
Generalization added.
**Verification Criteria:**
- findNestedClassifierRecursive called once with correct name
- addGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00025: Remove generalization by name

**ID:** UTS_CLS_00025
**Traces-To:** SWR_CLS_00011
**Title:** Remove generalization relationship by class name
**Type:** Unit
**Priority:** High
**Description:**
Test that a generalization is removed by resolving target class name.
**Pre-conditions:**
- Source class exists with existing generalization
- Target class exists
**Test Steps:**
1. Call ClassLinkAction with --remove parameter
2. Verify findNestedClassifierRecursive called
3. Verify deleteGeneralization called
**Expected Result:**
Generalization removed.
**Verification Criteria:**
- findNestedClassifierRecursive called once with correct name
- deleteGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00026: Link requires add or remove

**ID:** UTS_CLS_00026
**Traces-To:** SWR_CLS_00011
**Title:** Link requires exactly one of add or remove
**Type:** Unit
**Priority:** High
**Description:**
Test that link raises error when neither or both add and remove are specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassLinkAction with neither add nor remove
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --add or --remove must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --add or --remove"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00027: Link target not found raises error

**ID:** UTS_CLS_00027
**Traces-To:** SWR_CLS_00011
**Title:** Link raises error when target class not found
**Type:** Unit
**Priority:** High
**Description:**
Test that CliExecutionError is raised when target class name not found.
**Pre-conditions:**
- Source class exists
- Target class name does not exist
**Test Steps:**
1. Call ClassLinkAction with --add pointing to non-existent class
2. Verify findNestedClassifierRecursive returns None
3. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Class '<name>' not found".
**Verification Criteria:**
- findNestedClassifierRecursive called once
- CliExecutionError raised
- Error message contains class name
**Last Changed:** 2026-07-10

---

## UTS_CLS_00028: Link by GUID

**ID:** UTS_CLS_00028
**Traces-To:** SWR_CLS_00011, SWR_CLS_00013
**Title:** Link class by source GUID
**Type:** Unit
**Priority:** Medium
**Description:**
Test that source class can be identified by GUID for link operations.
**Pre-conditions:**
- Source class exists with specified GUID
- Target class exists
**Test Steps:**
1. Call ClassLinkAction with --guid parameter
2. Verify findElementByGUID called
3. Verify addGeneralization called
**Expected Result:**
Generalization added via GUID-identified source.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- addGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00029: ClassCommand registers all subcommands

**ID:** UTS_CLS_00029
**Traces-To:** SWR_CLS_00001-00004, SWR_CLS_00011
**Title:** ClassCommand registers all 5 subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test that ClassCommand registers all 5 subcommands.
**Pre-conditions:**
- ClassCommand initialized
**Test Steps:**
1. Create ClassCommand
2. Call get_actions
3. Verify 5 subcommands registered
**Expected Result:**
All 5 subcommands (create, delete, view, list, link) registered.
**Verification Criteria:**
- get_actions returns 5 actions
- All subcommand names present
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit test spec**

```bash
git add docs/tests/unit/uts_cls_test-specs.md
git commit -m "docs: Add unit test specifications for class command (UTS_CLS_00001-00029)"
```

---

## Phase 11: Parity Enhancements (Execution Logging & Duplicate Detection)

### Task 12: Add Execution-Step Logging to All Class Actions

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `self.logger` (already present via `AbstractAction`/`ElementManagementAction`)
- Produces: INFO-level log calls at each execution stage in `ClassCreateAction`, `ClassDeleteAction`, `ClassViewAction`, `ClassListAction`, `ClassLinkAction` (mirrors `package_action.py` pattern)

- [ ] **Step 1: Write failing tests for execution-step logging**

Add to `tests/unit/actions/test_class_action.py` (one test per action, using `caplog` at INFO level), e.g.:

```python
class TestClassActionLogging:
    """Test execution-step logging across class actions.

    UTS_CLS_00030: ClassCreateAction logs execution steps
    UTS_CLS_00031: ClassDeleteAction logs execution steps
    UTS_CLS_00032: ClassViewAction logs execution steps
    UTS_CLS_00033: ClassListAction logs execution steps
    UTS_CLS_00034: ClassLinkAction logs execution steps
    """

    def test_create_logs_execution_steps(self, caplog) -> None:
        """UTS_CLS_00030: create logs start/resolve/create/success at INFO."""
        import logging

        from rhapsody_cli.actions.class_action import ClassCreateAction

        action = ClassCreateAction()
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        mock_parent.getClasses.return_value = []
        mock_class = MagicMock()
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            with caplog.at_level(logging.INFO):
                args = MagicMock()
                args.path = "Sensors"
                args.input = None
                args.attributes = '{"name":"TemperatureSensor"}'
                action.execute(args)

        messages = [r.message for r in caplog.records]
        assert any("Starting class creation" in m for m in messages)
        assert any("Creating class 'TemperatureSensor'" in m for m in messages)
        assert any("Created class" in m for m in messages)

    # Similar tests for delete/view/list/link follow the same pattern used in
    # test_package_action.py's logging test class.
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassActionLogging -v`
Expected: FAIL (logging not yet implemented)

- [ ] **Step 3: Implement execution-step logging**

Add `self.logger.info(...)` calls at each stage described in SWR_CLS_00014, in `execute()` of each of the 5 action classes. Follow `package_action.py`'s exact placement pattern:
- Log "Starting X operation..." as the first line of `execute()`
- Log "Resolving ... path 'X'..." immediately before calling `_resolve_and_validate_package`/`_resolve_and_validate_class`/`_resolve_class_by_guid`
- Log stage-specific messages (creating/deleting/retrieving/listing/linking) before the corresponding COM call
- Log success/summary message after the operation completes

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassActionLogging -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Run linters**

Run: `ruff check src/rhapsody_cli/actions/class_action.py ; mypy src/rhapsody_cli/actions/class_action.py`
Expected: No errors

- [ ] **Step 6: Commit logging enhancement**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Add execution-step logging to class command (SWR_CLS_00014)"
```

---

### Task 13: Add Duplicate Class-Name Detection

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`
- Modify: `tests/unit/actions/test_class_action.py`
- Create: `tests/integration/cli/test_class_cli_integration.py` (live-Rhapsody verification, mirrors `test_package_cli_integration.py`)

**Interfaces:**
- Produces:
  - `ClassCreateAction._check_class_not_exists(parent, name) -> None` — raises `CliExecutionError` if a class named `name` already exists among `parent.getClasses()`
  - Updated `ClassCreateAction._create_single_class()` — calls `_check_class_not_exists()` before `addClass()`; wraps `addClass()` in try/except detecting COM error code `-2147221495` as a duplicate fallback signal; wraps attribute-setting in try/except that logs WARNING instead of failing the whole operation

- [ ] **Step 1: Write failing unit tests for duplicate detection**

Add to `tests/unit/actions/test_class_action.py`:

```python
class TestClassCreateDuplicateDetection:
    """Test duplicate class-name detection.

    UTS_CLS_00035: Create duplicate class raises user-friendly error
    """

    def test_create_duplicate_class_raises_error(self) -> None:
        """UTS_CLS_00035: Duplicate class name raises CliExecutionError with friendly message."""
        from rhapsody_cli.actions.class_action import ClassCreateAction
        from rhapsody_cli.exceptions import CliExecutionError

        action = ClassCreateAction()
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"

        existing_class = MagicMock()
        existing_class.getName.return_value = "TemperatureSensor"
        mock_parent.getClasses.return_value = [existing_class]

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"TemperatureSensor"}'

            with pytest.raises(CliExecutionError, match="already exists"):
                action.execute(args)

            mock_parent.addClass.assert_not_called()

    def test_create_attribute_failure_does_not_undo_creation(self) -> None:
        """Attribute-setting failure after successful addClass() is logged as WARNING, not fatal."""
        from rhapsody_cli.actions.class_action import ClassCreateAction

        action = ClassCreateAction()
        mock_parent = MagicMock()
        mock_parent.getMetaClass.return_value = "Package"
        mock_parent.getClasses.return_value = []
        mock_class = MagicMock()
        mock_class.setDescription.side_effect = Exception("COM failure")
        mock_parent.addClass.return_value = mock_class

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_parent):
            args = MagicMock()
            args.path = "Sensors"
            args.input = None
            args.attributes = '{"name":"X","description":"desc"}'

            # Should not raise; class was created successfully
            action.execute(args)
            mock_parent.addClass.assert_called_once_with("X")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_class_action.py::TestClassCreateDuplicateDetection -v`
Expected: FAIL

- [ ] **Step 3: Implement `_check_class_not_exists` and safe attribute-setting**

In `class_action.py`, add to `ClassCreateAction`:

```python
def _check_class_not_exists(self, parent: Any, name: str) -> None:
    """Check if a class with the given name already exists in the parent.

    SWR_CLS_00015: Duplicate detection.
    """
    self.logger.info("Checking if class '%s' already exists...", name)
    try:
        existing_classes = parent.getClasses()
        parent_desc = "project root" if parent.getMetaClass() == "Project" else f"package '{parent.getName()}'"
        for cls in existing_classes:
            if cls.getName() == name:
                raise CliExecutionError(f"Class '{name}' already exists in {parent_desc}")
    except CliExecutionError:
        raise
    except Exception as e:
        self.logger.debug("Could not enumerate existing classes to check for duplicates: %s", e)
```

Update `_create_single_class()`:
- Call `self._check_class_not_exists(parent, name)` before `parent.addClass(name)`
- Wrap `parent.addClass(name)` in try/except; on failure, check if the error string contains `"already"`, `"duplicate"`, or the COM code `-2147221495`/`2147221495` and raise the friendly `CliExecutionError` message; otherwise raise a generic `CliExecutionError` with context
- Wrap the `self._set_attributes(parent, cls, cls_attrs)` call in try/except that logs `self.logger.warning(...)` on failure instead of propagating (class is already created)

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_class_action.py -v`
Expected: All pass

- [ ] **Step 5: Add live-Rhapsody integration tests**

Create `tests/integration/cli/test_class_cli_integration.py` mirroring `test_package_cli_integration.py`:
- `test_create_and_delete_class_workflow` — create then delete a class under `integration_test_pkg`
- `test_duplicate_class_detection_with_friendly_error` — create a class, attempt to create the same name again, assert `CliExecutionError` message contains "already exists" and does NOT contain `-2147` or "Exception occurred"

- [ ] **Step 6: Run linters and full test suite**

Run: `ruff check src/ tests/ ; black --check src/ tests/ ; mypy src/ tests/ ; pytest tests/unit -v`
Expected: No errors, all tests pass

- [ ] **Step 7: Commit duplicate detection enhancement**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py tests/integration/cli/test_class_cli_integration.py
git commit -m "feat: Add duplicate class-name detection with user-friendly errors (SWR_CLS_00015)"
```

---

## Phase 12: Final Integration and Verification

### Task 14: Final Integration and Verification

**Files:**
- All files from previous tasks

- [ ] **Step 1: Run all tests**

Run: `pytest tests/unit -v`
Expected: All tests pass (existing + new class command tests)

- [ ] **Step 2: Run all linters**

Run: `ruff check src/ tests/ ; black --check src/ tests/ ; mypy src/`
Expected: No errors

- [ ] **Step 3: Verify CLI registration**

Run: `python -m rhapsody_cli --help`
Expected: Usage text lists `class` command alongside element, package, project

- [ ] **Step 4: Verify class subcommand help**

Run: `python -m rhapsody_cli class --help`
Expected: Help text lists create, delete, view, list, link subcommands

- [ ] **Step 5: Final commit (if any cleanup needed)**

```bash
git status
# If clean, no commit needed. If changes, commit them.
```

---

## Summary

**Implementation complete!** The class command provides:

- SW Requirements (SWR_CLS_00001-00015)
- Test Cases (UTS_CLS_00001-00035)
- 5 Subcommands (create, delete, view, list, link)
- Bulk creation with 8 attribute setters
- External JSON file support
- Multi-format output (table, JSON, CSV)
- File output support
- Path validation (Package/Project for create/list; Class for delete/view/link)
- GUID lookup support for delete/view/link
- Generalization relationship management (link)
- View-to-Create workflow (round-trip JSON)
- Execution-step INFO logging across all 5 actions (parity with package command, SWR_CLS_00014)
- Duplicate class-name detection with user-friendly errors (parity with package command, SWR_CLS_00015)
- Comprehensive test coverage (unit + live-Rhapsody integration)
- User documentation

**Files created:**
- 2 implementation files (class_command.py, class_action.py)
- 3 test files (test_class_command.py, test_class_action.py, test_class_cli_integration.py)
- 3 documentation files (swr_cls_requirements.md, uts_cls_test-specs.md, working_with_classes.rst)

**Test coverage:** 35 test cases covering all functionality

**Note on scope decision:** Unlike the package command's SWR_PKG_0013 (root-default `--path`), no equivalent enhancement was added for class create — `_resolve_and_validate_package` already accepts both `Package` and `Project` metaClasses for `--path` (SWR_CLS_00001), so root-level class creation is already reachable via `--path <ProjectRootName>` without needing a default-to-root branch.
