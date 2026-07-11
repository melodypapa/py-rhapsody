# Operation and Attribute Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `operation` and `attribute` commands with create, delete, view, list, and update subcommands for managing Rhapsody operations and attributes on classifiers.

**Architecture:** Mirrors existing class command structure. Uses `AbstractOperationAction` and `AbstractAttributeAction` base classes with path validation helpers. Create uses `addOperation/addAttribute` + setters; delete/view/list/update resolve via path+name or GUID with type validation.

**Tech Stack:** Python 3.8+, argparse CLI framework, Rhapsody COM API wrapper, pytest for testing.

## Global Constraints

- Python version: 3.8+
- All code must pass: `ruff check src/ tests/`, `black --check src/ tests/`, `mypy src/ tests/`, `pytest tests/unit -v`
- All tests must pass before commit
- Follow existing action patterns (ClassCreateAction, PackageCreateAction) — see `src/rhapsody_cli/actions/class_action.py`
- Use existing infrastructure: `PathResolver`, `OutputFormatter`, `ElementManagementAction`, `RhapsodyContext`
- TDD approach: write failing test first, then implementation
- Requirement IDs use 5-digit format: `SWR_OP_00001-...`, `SWR_ATTR_00001-...`
- Test case IDs use 5-digit format: `UTS_OP_00001-...`, `UTS_ATTR_00001-...`
- Parent element for operations/attributes is Classifier (Class/Actor/etc.) - metaClass check not strict, any classifier with `getOperations()/getAttributes()` methods
- Operation resolution via `findInterfaceItem(name)` or iterating `getOperations()`
- Attribute resolution via `findAttribute(name)`
- Type validation for --guid: metaClass must match expected type (Operation/Attribute)

---

## File Structure

**New files:**
- `src/rhapsody_cli/actions/operation_action.py` — AbstractOperationAction + 5 concrete actions
- `src/rhapsody_cli/actions/attribute_action.py` — AbstractAttributeAction + 5 concrete actions
- `src/rhapsody_cli/commands/operation_command.py` — OperationCommand dispatcher
- `src/rhapsody_cli/commands/attribute_command.py` — AttributeCommand dispatcher
- `tests/unit/actions/test_operation_action.py` — Operation action tests
- `tests/unit/actions/test_attribute_action.py` — Attribute action tests
- `tests/unit/commands/test_operation_command.py` — Operation command tests
- `tests/unit/commands/test_attribute_command.py` — Attribute command tests
- `docs/requirements/swr_op_requirements.md` — SW requirements
- `docs/requirements/swr_attr_requirements.md` — SW requirements
- `docs/tests/unit/uts_op_test-specs.md` — Unit test specs
- `docs/tests/unit/uts_attr_test-specs.md` — Unit test specs
- `docs/user_guide/working_with_operations.rst` — User documentation
- `docs/user_guide/working_with_attributes.rst` — User documentation

**Modified files:**
- `src/rhapsody_cli/cli/cli.py` — Register operation and attribute commands

---

## Phase 1: SW Requirements Documentation

### Task 1: Document Operation Command Requirements

**Files:**
- Create: `docs/requirements/swr_op_requirements.md`

**Interfaces:**
- Produces: SWR_OP_00001 through SWR_OP_00013

- [ ] **Step 1: Create requirements file**

```markdown
# Software Requirements - Operation Command

**Category:** Operation Command
**Prefix:** SWR_OP
**Source:** Extracted from spec 2026-07-10-element-commands-design.md
**Last Validated:** 2026-07-10

---

## SWR_OP_00001: Operation Create Command

**ID:** SWR_OP_00001
**Title:** operation create command creates one or multiple operations
**Status:** Planned
**Priority:** High
**Description:**
The operation CLI
- SHALL provide a `operation create` command to create one or multiple operations.
- SHALL accept `--path <class-path>` argument (required) - parent classifier path
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path resolves to Classifier element
- SHALL create operations via `classifier.addOperation(name)`
- SHALL set validated attributes: name, body, isAbstract, isStatic, isVirtual, returns, visibility, arguments, description
- SHALL apply name via `addOperation()`, body via `setBody()`, isAbstract via `setIsAbstract(1/0)`, isStatic via `setIsStatic(1/0)`, isVirtual via `setIsVirtual(1/0)`, visibility via `setVisibility()`, arguments via `setArguments()`, description via `setDescription()`
- SHALL resolve returns type via `findNestedClassifierRecursive(type_name)` on parent classifier's package
- SHALL set returns type via appropriate API method
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{` or `[`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationCreateAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00002: Operation Delete Command

**ID:** SWR_OP_00002
**Title:** operation delete command deletes an operation
**Status:** Planned
**Priority:** High
**Description:**
The operation CLI
- SHALL provide a `operation delete` command to delete an operation.
- SHALL accept `--path <class-path>` argument (optional) - parent classifier path
- SHALL accept `--guid <guid>` argument (optional) - operation GUID
- SHALL accept `--name <operation-name>` argument (optional) - operation name within class
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Operation", raise CliExecutionError if mismatch)
- SHALL resolve operation via `findInterfaceItem(name)` or iterating `getOperations()`
- SHALL delete operation via `deleteOperation(op)`
- SHALL log deletion to stderr
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationDeleteAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00003: Operation View Command

**ID:** SWR_OP_00003
**Title:** operation view command displays operation details
**Status:** Planned
**Priority:** High
**Description:**
The operation CLI
- SHALL provide a `operation view` command to view operation details.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <operation-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Operation")
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display fields: Name, GUID, Description, Body, IsAbstract, IsStatic, IsVirtual, Returns, Visibility, Arguments, MetaClass, FullPath
- SHALL support table (Property|Value layout), JSON (12-key object), CSV (horizontal 12-column) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationViewAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00004: Operation List Command

**ID:** SWR_OP_00004
**Title:** operation list command lists operations on a classifier
**Status:** Planned
**Priority:** High
**Description:**
The operation CLI
- SHALL provide a `operation list` command to list operations on a classifier.
- SHALL accept `--path <class-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list operations via `getOperations()` and collect names via `getName()`
- SHALL support table (single Name column), JSON (array of strings), CSV (1-column horizontal) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationListAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00005: Operation Update Command

**ID:** SWR_OP_00005
**Title:** operation update command modifies operation attributes
**Status:** Planned
**Priority:** High
**Description:**
The operation CLI
- SHALL provide a `operation update` command to modify attributes of an existing operation.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <operation-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Operation", raise CliExecutionError if mismatch)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, body, isAbstract, isStatic, isVirtual, returns, visibility, arguments, description
- SHALL skip unknown attributes with warning log
- SHALL log INFO for successful updates
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationUpdateAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00006: Path and Name Validation

**ID:** SWR_OP_00006
**Title:** All operation commands validate path and name before execution
**Status:** Planned
**Priority:** High
**Description:**
All operation commands
- SHALL validate path before execution.
- SHALL resolve classifier path using PathResolver
- SHALL resolve operation by name within classifier
- SHALL raise CliExecutionError if path not found
- SHALL raise CliExecutionError if operation name not found in classifier
**Implementation:** src/rhapsody_cli/actions/operation_action.py:AbstractOperationAction._resolve_classifier, _resolve_operation
**Last Changed:** 2026-07-10

---

## SWR_OP_00007: External JSON File Support

**ID:** SWR_OP_00007
**Title:** Operation create/update supports external JSON files
**Status:** Planned
**Priority:** Medium
**Description:**
Operation create and update commands
- SHALL support external JSON files.
- SHALL accept `--input <file>` argument
- SHALL accept file path as positional argument
- SHALL detect inline JSON vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL raise CliExecutionError if file not found
- SHALL raise CliExecutionError if JSON invalid
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationCreateAction._load_json_data
**Last Changed:** 2026-07-10

---

## SWR_OP_00008: Multi-Format Output

**ID:** SWR_OP_00008
**Title:** Operation view and list support multiple output formats
**Status:** Planned
**Priority:** Medium
**Description:**
Operation view and list commands
- SHALL support multiple output formats.
- SHALL support table format (default, human-readable)
- SHALL support JSON format (machine-parsable)
- SHALL support CSV format (spreadsheet-friendly)
- SHALL use horizontal layout for CSV (header row + data rows)
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationViewAction._format_output, OperationListAction._format_output
**Last Changed:** 2026-07-10

---

## SWR_OP_00009: Error Handling and Logging

**ID:** SWR_OP_00009
**Title:** All operation actions follow consistent error handling patterns
**Status:** Planned
**Priority:** High
**Description:**
All operation actions
- SHALL follow consistent error handling patterns.
- SHALL use `_handle_execution_error()` for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/operation_action.py:AbstractOperationAction
**Last Changed:** 2026-07-10

---

## SWR_OP_00010: GUID Lookup Support

**ID:** SWR_OP_00010
**Title:** Operation view/delete/update support --guid as alternative to --path + --name
**Status:** Planned
**Priority:** Medium
**Description:**
Operation view, delete, and update commands
- SHALL support `--guid` as alternative to `--path` + `--name`.
- SHALL accept `--guid <guid>` argument
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL locate operation by GUID via `findElementByGUID(guid)` on the active project
- SHALL validate located element is Operation (metaClass == "Operation")
- SHALL raise CliExecutionError if GUID not found
- SHALL raise CliExecutionError if GUID resolves to wrong type
**Implementation:** src/rhapsody_cli/actions/operation_action.py:AbstractOperationAction._resolve_operation_by_guid
**Last Changed:** 2026-07-10

---

## SWR_OP_00011: Returns Type Resolution

**ID:** SWR_OP_00011
**Title:** Operation create/update resolves returns type by name
**Status:** Planned
**Priority:** Medium
**Description:**
Operation create and update commands
- SHALL resolve returns type by name.
- SHALL accept `returns` field as type name string
- SHALL resolve type via `findNestedClassifierRecursive(type_name)` on parent classifier's package
- SHALL raise CliExecutionError if type name not found
- SHALL set resolved type classifier on operation
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationCreateAction._resolve_type
**Last Changed:** 2026-07-10

---

## SWR_OP_00012: Boolean Flag Support

**ID:** SWR_OP_00012
**Title:** Operation create/update supports boolean flags isAbstract, isStatic, isVirtual
**Status:** Planned
**Priority:** Medium
**Description:**
Operation create and update commands
- SHALL support boolean flags.
- SHALL accept `isAbstract` bool in JSON, set via `setIsAbstract(1/0)`
- SHALL accept `isStatic` bool in JSON, set via `setIsStatic(1/0)`
- SHALL accept `isVirtual` bool in JSON, set via `setIsVirtual(1/0)`
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationCreateAction._set_boolean_flags
**Last Changed:** 2026-07-10

---

## SWR_OP_00013: Bulk Creation Support

**ID:** SWR_OP_00013
**Title:** Operation create supports bulk creation via JSON array
**Status:** Planned
**Priority:** Medium
**Description:**
Operation create command
- SHALL support bulk creation.
- SHALL accept JSON array of operation definitions
- SHALL create each operation in sequence
- SHALL log INFO with count of created operations
**Implementation:** src/rhapsody_cli/actions/operation_action.py:OperationCreateAction.execute
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_op_requirements.md
git commit -m "docs: Add SW requirements for operation command (SWR_OP_00001-00013)"
```

### Task 2: Document Attribute Command Requirements

**Files:**
- Create: `docs/requirements/swr_attr_requirements.md`

**Interfaces:**
- Produces: SWR_ATTR_00001 through SWR_ATTR_00013

- [ ] **Step 1: Create requirements file** (similar structure to operation, with attribute-specific fields: type, defaultValue, multiplicity, isStatic, visibility, declaration)

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_attr_requirements.md
git commit -m "docs: Add SW requirements for attribute command (SWR_ATTR_00001-00013)"
```

---

## Phase 2: AbstractOperationAction Base Class

### Task 3: Create AbstractOperationAction Base Class

**Files:**
- Create: `src/rhapsody_cli/actions/operation_action.py`
- Create: `tests/unit/actions/test_operation_action.py`

**Interfaces:**
- Consumes: `ElementManagementAction` from `abstract_action.py`
- Produces:
  - `AbstractOperationAction` class with:
    - `_resolve_classifier(path) -> Any` — resolves parent classifier
    - `_resolve_operation(classifier, name) -> Any` — finds operation by name
    - `_resolve_operation_by_guid(guid) -> Any` — locates via GUID, validates metaClass == "Operation"
  - Module-level `logger = logging.getLogger(__name__)`

- [ ] **Step 1: Write tests for AbstractOperationAction**

Create `tests/unit/actions/test_operation_action.py`:

```python
"""Tests for operation actions."""

from unittest.mock import MagicMock, patch
import pytest
from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.actions.operation_action import AbstractOperationAction
from rhapsody_cli.exceptions import CliExecutionError


class TestAbstractOperationAction:
    """Test AbstractOperationAction base class."""

    def test_resolve_classifier_success(self) -> None:
        """Test successful classifier resolution."""
        action = AbstractOperationAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(ElementManagementAction, "_get_active_root", return_value=MagicMock()):
            with patch(
                "rhapsody_cli.actions.abstract_action.PathResolver.resolve_container",
                return_value=mock_class,
            ):
                result = action._resolve_classifier("Sensors/TemperatureSensor")
                assert result == mock_class

    def test_resolve_operation_by_name(self) -> None:
        """Test resolving operation by name within classifier."""
        action = AbstractOperationAction()
        mock_class = MagicMock()
        mock_operation = MagicMock()
        mock_class.findInterfaceItem.return_value = mock_operation

        result = action._resolve_operation(mock_class, "readValue")
        assert result == mock_operation
        mock_class.findInterfaceItem.assert_called_once_with("readValue")

    def test_resolve_operation_by_guid(self) -> None:
        """Test resolving operation by GUID with type validation."""
        action = AbstractOperationAction()
        mock_project = MagicMock()
        mock_operation = MagicMock()
        mock_operation.getMetaClass.return_value = "Operation"
        mock_project.findElementByGUID.return_value = mock_operation

        with patch.object(action, "_get_active_root", return_value=mock_project):
            result = action._resolve_operation_by_guid("12345678-1234-1234-1234-123456789abc")
            assert result == mock_operation

    def test_resolve_operation_by_guid_wrong_type(self) -> None:
        """Test that wrong type via GUID raises error."""
        action = AbstractOperationAction()
        mock_project = MagicMock()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"
        mock_project.findElementByGUID.return_value = mock_class

        with patch.object(action, "_get_active_root", return_value=mock_project):
            with pytest.raises(CliExecutionError) as exc_info:
                action._resolve_operation_by_guid("12345678-1234-1234-1234-123456789abc")

            assert "does not resolve to an Operation" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)

    def test_resolve_operation_name_not_found(self) -> None:
        """Test that operation name not found raises error."""
        action = AbstractOperationAction()
        mock_class = MagicMock()
        mock_class.findInterfaceItem.return_value = None

        with pytest.raises(CliExecutionError) as exc_info:
            action._resolve_operation(mock_class, "nonexistent")

        assert "Operation 'nonexistent' not found" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/unit/actions/test_operation_action.py::TestAbstractOperationAction -v
```

Expected: Import errors (class not yet implemented)

- [ ] **Step 3: Implement AbstractOperationAction**

Create `src/rhapsody_cli/actions/operation_action.py`:

```python
"""Operation command actions.

SWR_OP_00001-00013: Operation Command
"""

import json
import logging
from typing import Any, List

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.path_resolver import PathResolver
from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.commands.abstract_command import AbstractAction

_LOGGER_NAME = "rhapsody_cli.actions.operation_action"
logger = logging.getLogger(_LOGGER_NAME)


class AbstractOperationAction(ElementManagementAction):
    """Base class for operation actions with common validation helpers."""

    def _resolve_classifier(self, path: str) -> Any:
        """Resolve classifier path and return classifier object."""
        root = self._get_active_root()
        classifier = PathResolver.resolve_container(root, path)
        if classifier is None:
            raise CliExecutionError(f"Classifier path '{path}' not found")
        return classifier

    def _resolve_operation(self, classifier: Any, name: str) -> Any:
        """Resolve operation by name within classifier."""
        operation = classifier.findInterfaceItem(name)
        if operation is None:
            raise CliExecutionError(f"Operation '{name}' not found in classifier")
        return operation

    def _resolve_operation_by_guid(self, guid: str) -> Any:
        """Resolve operation by GUID and validate type."""
        project = self._get_active_root()
        element = project.findElementByGUID(guid)
        if element is None:
            raise CliExecutionError(f"GUID '{guid}' not found")
        meta_class = element.getMetaClass()
        if meta_class != "Operation":
            raise CliExecutionError(
                f"GUID '{guid}' does not resolve to an Operation (found {meta_class})"
            )
        return element
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/unit/actions/test_operation_action.py::TestAbstractOperationAction -v
```

Expected: All 5 tests pass

- [ ] **Step 5: Commit**

```bash
git add src/rhapsody_cli/actions/operation_action.py tests/unit/actions/test_operation_action.py
git commit -m "feat: Add AbstractOperationAction base class (SWR_OP_00006, SWR_OP_00010)"
```

---

## Phase 3: OperationCreateAction

### Task 4: Write OperationCreateAction Tests

**Files:**
- Modify: `tests/unit/actions/test_operation_action.py`

**Interfaces:**
- Consumes: `AbstractOperationAction`
- Produces: Test class for create action

- [ ] **Step 1: Add TestOperationCreateAction class**

Append to test file with tests for:
- Single operation creation
- Bulk creation from array
- Setting boolean flags (isAbstract, isStatic, isVirtual)
- Setting body, visibility, arguments
- Returns type resolution
- Skipping unknown fields
- Missing name raises error

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/unit/actions/test_operation_action.py::TestOperationCreateAction -v
```

### Task 5: Implement OperationCreateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/operation_action.py`

**Interfaces:**
- Consumes: `AbstractOperationAction`, existing patterns
- Produces: `OperationCreateAction` class

- [ ] **Step 1: Add OperationCreateAction class**

Add class with:
- `command_id = "create"`
- `help_text = "Create operations on a classifier"`
- `VALID_ATTRIBUTES = {"name", "body", "isAbstract", "isStatic", "isVirtual", "returns", "visibility", "arguments", "description"}`
- `_load_json_data(args) -> dict`
- `_resolve_type(classifier, type_name) -> Any`
- `_set_attributes(operation, data)`
- `execute(args)`

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationCreateAction (SWR_OP_00001)"
```

---

## Phase 4: OperationDeleteAction

### Task 6: Write OperationDeleteAction Tests

**Files:**
- Modify: `tests/unit/actions/test_operation_action.py`

- [ ] **Step 1: Add TestOperationDeleteAction class**

Tests for:
- Delete by path+name
- Delete by GUID
- GUID wrong type raises error
- Requires path+name or GUID

- [ ] **Step 2: Run tests to verify they fail**

### Task 7: Implement OperationDeleteAction

**Files:**
- Modify: `src/rhapsody_cli/actions/operation_action.py`

- [ ] **Step 1: Add OperationDeleteAction class**

Add class with:
- `command_id = "delete"`
- `execute(args)` — resolves by path+name or GUID, calls `deleteOperation(op)`

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationDeleteAction (SWR_OP_00002)"
```

---

## Phase 5: OperationViewAction

### Task 8: Write OperationViewAction Tests

**Files:**
- Modify: `tests/unit/actions/test_operation_action.py`

- [ ] **Step 1: Add TestOperationViewAction class**

Tests for:
- View by path+name
- View by GUID with type validation
- Table output format
- JSON output format
- CSV output format
- Write to file

- [ ] **Step 2: Run tests to verify they fail**

### Task 9: Implement OperationViewAction

**Files:**
- Modify: `src/rhapsody_cli/actions/operation_action.py`

- [ ] **Step 1: Add OperationViewAction class**

Add class with:
- `command_id = "view"`
- `_collect_operation_data(operation) -> dict`
- `_format_output(data, format) -> str`
- `execute(args)`

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationViewAction (SWR_OP_00003)"
```

---

## Phase 6: OperationListAction

### Task 10: Write OperationListAction Tests

**Files:**
- Modify: `tests/unit/actions/test_operation_action.py`

- [ ] **Step 1: Add TestOperationListAction class**

Tests for:
- List operations on classifier
- Empty list (no operations)
- Table format
- JSON format (array of strings)
- CSV format
- Write to file

- [ ] **Step 2: Run tests to verify they fail**

### Task 11: Implement OperationListAction

**Files:**
- Modify: `src/rhapsody_cli/actions/operation_action.py`

- [ ] **Step 1: Add OperationListAction class**

Add class with:
- `command_id = "list"`
- `_collect_operation_names(classifier) -> List[str]`
- `_format_output(names, format) -> str`
- `execute(args)`

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationListAction (SWR_OP_00004)"
```

---

## Phase 7: OperationUpdateAction

### Task 12: Write OperationUpdateAction Tests

**Files:**
- Modify: `tests/unit/actions/test_operation_action.py`

- [ ] **Step 1: Add TestOperationUpdateAction class**

Tests for:
- Update by path+name
- Update by GUID with type validation
- Partial update
- Boolean flags update
- Skip unknown fields

- [ ] **Step 2: Run tests to verify they fail**

### Task 13: Implement OperationUpdateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/operation_action.py`

- [ ] **Step 1: Add OperationUpdateAction class**

Add class with:
- `command_id = "update"`
- `VALID_ATTRIBUTES` (same as create)
- `_load_json_data(args) -> dict`
- `_set_attributes(operation, data)` — partial update
- `execute(args)`

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationUpdateAction (SWR_OP_00005)"
```

---

## Phase 8: OperationCommand Dispatcher

### Task 14: Write OperationCommand Tests

**Files:**
- Create: `tests/unit/commands/test_operation_command.py`

- [ ] **Step 1: Write tests for OperationCommand**

Tests for:
- Command ID is "operation"
- Missing subcommand raises error
- Registers all 5 subcommands (create, delete, view, list, update)

- [ ] **Step 2: Run tests to verify they fail**

### Task 15: Implement OperationCommand

**Files:**
- Create: `src/rhapsody_cli/commands/operation_command.py`

- [ ] **Step 1: Create OperationCommand class**

```python
"""Operation command dispatcher."""

from typing import List
from rhapsody_cli.commands.abstract_command import AbstractCommand, AbstractAction
from rhapsody_cli.actions.operation_action import (
    OperationCreateAction,
    OperationDeleteAction,
    OperationViewAction,
    OperationListAction,
    OperationUpdateAction,
)


class OperationCommand(AbstractCommand):
    """Operation command dispatcher."""

    _PROG_ID = "operation"

    def get_actions(self) -> List[AbstractAction]:
        return [
            OperationCreateAction(),
            OperationDeleteAction(),
            OperationViewAction(),
            OperationListAction(),
            OperationUpdateAction(),
        ]

    def _setup_subparsers(self) -> None:
        # Setup subparsers for create, delete, view, list, update
        # (implementation details for argparse setup)
        ...
```

- [ ] **Step 2: Run tests to verify they pass**

- [ ] **Step 3: Commit**

```bash
git commit -m "feat: Add OperationCommand dispatcher"
```

---

## Phase 9-14: Attribute Command (Mirroring Operation)

The attribute command follows the exact same structure as operation:

- **Phase 9:** SW Requirements (Task 16-17)
- **Phase 10:** AbstractAttributeAction (Task 18-19)
- **Phase 11:** AttributeCreateAction (Task 20-21) — fields: name, type, defaultValue, multiplicity, isStatic, visibility, declaration, description
- **Phase 12:** AttributeDeleteAction (Task 22-23) — uses `findAttribute(name)`, `deleteAttribute(attr)`
- **Phase 13:** AttributeViewAction (Task 24-25) — display fields: Name, GUID, Description, Type, DefaultValue, Multiplicity, IsStatic, Visibility, Declaration, MetaClass, FullPath
- **Phase 14:** AttributeListAction (Task 26-27) — via `getAttributes()`
- **Phase 15:** AttributeUpdateAction (Task 28-29) — partial update
- **Phase 16:** AttributeCommand dispatcher (Task 30-31)

Each phase follows the TDD pattern: write tests, verify failure, implement, verify pass, commit.

---

## Phase 17: CLI Registration

### Task 32: Register Commands in CLI

**Files:**
- Modify: `src/rhapsody_cli/cli/cli.py`

- [ ] **Step 1: Import and register OperationCommand**

Add to imports and command registration in cli.py:

```python
from rhapsody_cli.commands.operation_command import OperationCommand
from rhapsody_cli.commands.attribute_command import AttributeCommand

# In dispatcher setup:
dispatcher.register(OperationCommand)
dispatcher.register(AttributeCommand)
```

- [ ] **Step 2: Update usage text**

Add operation and attribute to usage text.

- [ ] **Step 3: Verify CLI help**

```bash
python -m rhapsody_cli.cli --help
python -m rhapsody_cli.cli operation --help
python -m rhapsody_cli.cli attribute --help
```

- [ ] **Step 4: Commit**

```bash
git commit -m "feat: Register operation and attribute commands in CLI"
```

---

## Phase 18: Test Specs Documentation

### Task 33: Add Operation Test Specs

**Files:**
- Create: `docs/tests/unit/uts_op_test-specs.md`

- [ ] **Step 1: Create test specs file**

Document test specs for all operation actions (UTS_OP_00001-00035).

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add unit test specs for operation command (UTS_OP_00001-00035)"
```

### Task 34: Add Attribute Test Specs

**Files:**
- Create: `docs/tests/unit/uts_attr_test-specs.md`

- [ ] **Step 1: Create test specs file**

Document test specs for all attribute actions (UTS_ATTR_00001-00035).

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add unit test specs for attribute command (UTS_ATTR_00001-00035)"
```

---

## Phase 19: User Guide Documentation

### Task 35: Create Operation User Guide

**Files:**
- Create: `docs/user_guide/working_with_operations.rst`

- [ ] **Step 1: Create user guide**

Document all operation subcommands with usage, arguments, examples.

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add user guide for operation command"
```

### Task 36: Create Attribute User Guide

**Files:**
- Create: `docs/user_guide/working_with_attributes.rst`

- [ ] **Step 1: Create user guide**

Document all attribute subcommands.

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add user guide for attribute command"
```

---

## Phase 20: Final Verification

### Task 37: Run Full Test Suite and Quality Gates

- [ ] **Step 1: Run pytest**

```bash
pytest tests/unit -v
```

Expected: All tests pass (operation and attribute tests included)

- [ ] **Step 2: Run ruff**

```bash
ruff check src/ tests/
```

- [ ] **Step 3: Run black**

```bash
black --check src/ tests/
```

- [ ] **Step 4: Run mypy**

```bash
mypy src/
```

- [ ] **Step 5: Final commit**

---

## Summary

**Completed:**
- Operation command: 5 subcommands (create, delete, view, list, update)
- Attribute command: 5 subcommands
- Tests: ~35 tests per command
- Quality gates passing
- Documentation complete

**Next Plan:** Port Command + Element Command Removal (Plan 3)