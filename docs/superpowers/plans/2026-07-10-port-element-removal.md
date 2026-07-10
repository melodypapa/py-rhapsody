# Port Command and Element Command Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement `port` command with create, delete, view, list, and update subcommands, then remove the deprecated `element` command.

**Architecture:** Mirrors operation/attribute command structure. Uses `AbstractPortAction` base class. Create uses `addPort(name)` + setters. Delete uses `deleteFromProject()`. Port-specific attributes: isBehavioral, isReversed, portContract.

**Tech Stack:** Python 3.8+, argparse CLI framework, Rhapsody COM API wrapper, pytest for testing.

## Global Constraints

- Python version: 3.8+
- All code must pass: `ruff check src/ tests/`, `black --check src/ tests/`, `mypy src/ tests/`, `pytest tests/unit -v`
- All tests must pass before commit
- Follow existing action patterns (OperationCreateAction, ClassCreateAction)
- Use existing infrastructure: `PathResolver`, `OutputFormatter`, `ElementManagementAction`
- TDD approach: write failing test first, then implementation
- Requirement IDs use 5-digit format: `SWR_PORT_00001-...`
- Test case IDs use 5-digit format: `UTS_PORT_00001-...`
- Port resolution via iterating `getPorts()` and matching by name (no findPort method)
- Port deletion via `deleteFromProject()` (no dedicated deletePort method)
- Type validation for --guid: metaClass must be "Port"

---

## File Structure

**New files:**
- `src/rhapsody_cli/actions/port_action.py` — AbstractPortAction + 5 concrete actions
- `src/rhapsody_cli/commands/port_command.py` — PortCommand dispatcher
- `tests/unit/actions/test_port_action.py` — Port action tests
- `tests/unit/commands/test_port_command.py` — Port command tests
- `docs/requirements/swr_port_requirements.md` — SW requirements
- `docs/tests/unit/uts_port_test-specs.md` — Unit test specs
- `docs/user_guide/working_with_ports.rst` — User documentation

**Deleted files:**
- `src/rhapsody_cli/commands/element_command.py`
- `src/rhapsody_cli/actions/element_action.py`
- `tests/unit/commands/test_element_command.py`
- `tests/unit/actions/test_element_action.py`

**Modified files:**
- `src/rhapsody_cli/cli/cli.py` — Register port command, remove element command
- `docs/requirements/swr_elem_requirements.md` — Remove or deprecate
- `docs/tests/unit/uts_elem_test-specs.md` — Remove or deprecate

---

## Part A: Port Command Implementation

## Phase 1: SW Requirements Documentation

### Task 1: Document Port Command Requirements

**Files:**
- Create: `docs/requirements/swr_port_requirements.md`

**Interfaces:**
- Produces: SWR_PORT_00001 through SWR_PORT_00013

- [ ] **Step 1: Create requirements file**

```markdown
# Software Requirements - Port Command

**Category:** Port Command
**Prefix:** SWR_PORT
**Source:** Extracted from spec 2026-07-10-element-commands-design.md
**Last Validated:** 2026-07-10

---

## SWR_PORT_00001: Port Create Command

**ID:** SWR_PORT_00001
**Title:** port create command creates one or multiple ports
**Status:** Planned
**Priority:** High
**Description:**
The port CLI
- SHALL provide a `port create` command to create one or multiple ports.
- SHALL accept `--path <class-path>` argument (required) - parent classifier path
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path resolves to Classifier element
- SHALL create ports via `classifier.addPort(name)`
- SHALL set validated attributes: name, isBehavioral, isReversed, portContract, description
- SHALL apply name via `addPort()`, isBehavioral via `setIsBehavioral(0/1)`, isReversed via `setIsReversed(0/1)`, description via `setDescription()`
- SHALL resolve portContract by name via `findNestedClassifierRecursive()` on parent's package
- SHALL set portContract via `setPortContract(classifier)`
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{` or `[`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortCreateAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00002: Port Delete Command

**ID:** SWR_PORT_00002
**Title:** port delete command deletes a port
**Status:** Planned
**Priority:** High
**Description:**
The port CLI
- SHALL provide a `port delete` command to delete a port.
- SHALL accept `--path <class-path>` argument (optional) - parent classifier path
- SHALL accept `--guid <guid>` argument (optional) - port GUID
- SHALL accept `--name <port-name>` argument (optional) - port name within class
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Port", raise CliExecutionError if mismatch)
- SHALL resolve port by iterating `getPorts()` and matching by name
- SHALL delete port via `deleteFromProject()`
- SHALL log deletion to stderr
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortDeleteAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00003: Port View Command

**ID:** SWR_PORT_00003
**Title:** port view command displays port details
**Status:** Planned
**Priority:** High
**Description:**
The port CLI
- SHALL provide a `port view` command to view port details.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <port-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Port")
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display fields: Name, GUID, Description, IsBehavioral, IsReversed, PortContract, MetaClass, FullPath
- SHALL support table (Property|Value layout), JSON (8-key object), CSV (horizontal 8-column) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortViewAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00004: Port List Command

**ID:** SWR_PORT_00004
**Title:** port list command lists ports on a classifier
**Status:** Planned
**Priority:** High
**Description:**
The port CLI
- SHALL provide a `port list` command to list ports on a classifier.
- SHALL accept `--path <class-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list ports via `getPorts()` and collect names via `getName()`
- SHALL support table (single Name column), JSON (array of strings), CSV (1-column horizontal) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortListAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00005: Port Update Command

**ID:** SWR_PORT_00005
**Title:** port update command modifies port attributes
**Status:** Planned
**Priority:** High
**Description:**
The port CLI
- SHALL provide a `port update` command to modify attributes of an existing port.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <port-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Port", raise CliExecutionError if mismatch)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, isBehavioral, isReversed, portContract, description
- SHALL skip unknown attributes with warning log
- SHALL log INFO for successful updates
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortUpdateAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00006: Path and Name Validation

**ID:** SWR_PORT_00006
**Title:** All port commands validate path and name before execution
**Status:** Planned
**Priority:** High
**Description:**
All port commands
- SHALL validate path before execution.
- SHALL resolve classifier path using PathResolver
- SHALL resolve port by iterating `getPorts()` and matching by name
- SHALL raise CliExecutionError if path not found
- SHALL raise CliExecutionError if port name not found in classifier
**Implementation:** src/rhapsody_cli/actions/port_action.py:AbstractPortAction._resolve_classifier, _resolve_port
**Last Changed:** 2026-07-10

---

## SWR_PORT_00007: External JSON File Support

**ID:** SWR_PORT_00007
**Title:** Port create/update supports external JSON files
**Status:** Planned
**Priority:** Medium
**Description:**
Port create and update commands
- SHALL support external JSON files.
- SHALL accept `--input <file>` argument
- SHALL detect inline JSON vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL raise CliExecutionError if file not found
- SHALL raise CliExecutionError if JSON invalid
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortCreateAction._load_json_data
**Last Changed:** 2026-07-10

---

## SWR_PORT_00008: Multi-Format Output

**ID:** SWR_PORT_00008
**Title:** Port view and list support multiple output formats
**Status:** Planned
**Priority:** Medium
**Description:**
Port view and list commands
- SHALL support multiple output formats.
- SHALL support table format (default)
- SHALL support JSON format
- SHALL support CSV format
- SHALL use horizontal layout for CSV
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortViewAction._format_output, PortListAction._format_output
**Last Changed:** 2026-07-10

---

## SWR_PORT_00009: Error Handling and Logging

**ID:** SWR_PORT_00009
**Title:** All port actions follow consistent error handling patterns
**Status:** Planned
**Priority:** High
**Description:**
All port actions
- SHALL follow consistent error handling patterns.
- SHALL use `_handle_execution_error()` for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/port_action.py:AbstractPortAction
**Last Changed:** 2026-07-10

---

## SWR_PORT_00010: GUID Lookup Support

**ID:** SWR_PORT_00010
**Title:** Port view/delete/update support --guid as alternative to --path + --name
**Status:** Planned
**Priority:** Medium
**Description:**
Port view, delete, and update commands
- SHALL support `--guid` as alternative to `--path` + `--name`.
- SHALL accept `--guid <guid>` argument
- SHALL locate port by GUID via `findElementByGUID(guid)`
- SHALL validate located element is Port (metaClass == "Port")
- SHALL raise CliExecutionError if GUID not found
- SHALL raise CliExecutionError if GUID resolves to wrong type
**Implementation:** src/rhapsody_cli/actions/port_action.py:AbstractPortAction._resolve_port_by_guid
**Last Changed:** 2026-07-10

---

## SWR_PORT_00011: PortContract Resolution

**ID:** SWR_PORT_00011
**Title:** Port create/update resolves portContract by name
**Status:** Planned
**Priority:** Medium
**Description:**
Port create and update commands
- SHALL resolve portContract by name.
- SHALL accept `portContract` field as class name string
- SHALL resolve class via `findNestedClassifierRecursive(class_name)` on parent's package
- SHALL raise CliExecutionError if class name not found
- SHALL set resolved class via `setPortContract(classifier)`
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortCreateAction._resolve_port_contract
**Last Changed:** 2026-07-10

---

## SWR_PORT_00012: IsBehavioral and IsReversed Support

**ID:** SWR_PORT_00012
**Title:** Port create/update supports isBehavioral and isReversed flags
**Status:** Planned
**Priority:** Medium
**Description:**
Port create and update commands
- SHALL support isBehavioral and isReversed flags.
- SHALL accept `isBehavioral` int (0/1) in JSON, set via `setIsBehavioral(val)`
- SHALL accept `isReversed` int (0/1) in JSON, set via `setIsReversed(val)`
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortCreateAction._set_flags
**Last Changed:** 2026-07-10

---

## SWR_PORT_00013: Bulk Creation Support

**ID:** SWR_PORT_00013
**Title:** Port create supports bulk creation via JSON array
**Status:** Planned
**Priority:** Medium
**Description:**
Port create command
- SHALL support bulk creation.
- SHALL accept JSON array of port definitions
- SHALL create each port in sequence
- SHALL log INFO with count of created ports
**Implementation:** src/rhapsody_cli/actions/port_action.py:PortCreateAction.execute
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_port_requirements.md
git commit -m "docs: Add SW requirements for port command (SWR_PORT_00001-00013)"
```

---

## Phase 2-7: Port Command Implementation

Follow the same TDD pattern as operation/attribute commands:

- **Phase 2:** AbstractPortAction (Task 2-3) — `_resolve_port(classifier, name)` iterates `getPorts()`, `_resolve_port_by_guid(guid)`
- **Phase 3:** PortCreateAction (Task 4-5) — `addPort(name)`, setIsBehavioral, setIsReversed, setPortContract
- **Phase 4:** PortDeleteAction (Task 6-7) — `deleteFromProject()`
- **Phase 5:** PortViewAction (Task 8-9) — display fields: Name, GUID, Description, IsBehavioral, IsReversed, PortContract, MetaClass, FullPath
- **Phase 6:** PortListAction (Task 10-11) — via `getPorts()`
- **Phase 7:** PortUpdateAction (Task 12-13) — partial update
- **Phase 8:** PortCommand dispatcher (Task 14-15)

Each phase: write tests → verify failure → implement → verify pass → commit.

---

## Phase 9: CLI Registration

### Task 16: Register Port Command in CLI

**Files:**
- Modify: `src/rhapsody_cli/cli/cli.py`

- [ ] **Step 1: Import and register PortCommand**

```python
from rhapsody_cli.commands.port_command import PortCommand

dispatcher.register(PortCommand)
```

- [ ] **Step 2: Update usage text**

Add "port" to usage text.

- [ ] **Step 3: Verify CLI help**

```bash
python -m rhapsody_cli.cli --help
python -m rhapsody_cli.cli port --help
```

- [ ] **Step 4: Commit**

```bash
git commit -m "feat: Register port command in CLI"
```

---

## Phase 10: Documentation

### Task 17: Add Port Test Specs

**Files:**
- Create: `docs/tests/unit/uts_port_test-specs.md`

- [ ] **Step 1: Create test specs**

Document test specs for all port actions (UTS_PORT_00001-00035).

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add unit test specs for port command (UTS_PORT_00001-00035)"
```

### Task 18: Create Port User Guide

**Files:**
- Create: `docs/user_guide/working_with_ports.rst`

- [ ] **Step 1: Create user guide**

Document all port subcommands with usage, arguments, examples.

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Add user guide for port command"
```

---

## Part B: Element Command Removal

## Phase 11: Remove Element Command Files

### Task 19: Delete Element Command Implementation

**Files:**
- Delete: `src/rhapsody_cli/commands/element_command.py`
- Delete: `src/rhapsody_cli/actions/element_action.py`

- [ ] **Step 1: Remove element command files**

```bash
git rm src/rhapsody_cli/commands/element_command.py
git rm src/rhapsody_cli/actions/element_action.py
```

- [ ] **Step 2: Commit deletion**

```bash
git commit -m "refactor: Remove element command implementation"
```

### Task 20: Delete Element Command Tests

**Files:**
- Delete: `tests/unit/commands/test_element_command.py`
- Delete: `tests/unit/actions/test_element_action.py`

- [ ] **Step 1: Remove element test files**

```bash
git rm tests/unit/commands/test_element_command.py
git rm tests/unit/actions/test_element_action.py
```

- [ ] **Step 2: Commit deletion**

```bash
git commit -m "refactor: Remove element command tests"
```

### Task 21: Remove Element Command Registration

**Files:**
- Modify: `src/rhapsody_cli/cli/cli.py`

- [ ] **Step 1: Remove element command import and registration**

Remove from cli.py:
```python
# Remove this import
from rhapsody_cli.commands.element_command import ElementCommand

# Remove this registration
dispatcher.register(ElementCommand)
```

- [ ] **Step 2: Update usage text**

Remove "element" from usage text.

- [ ] **Step 3: Verify CLI help**

```bash
python -m rhapsody_cli.cli --help
```

Expected: No "element" command shown

- [ ] **Step 4: Commit**

```bash
git commit -m "refactor: Remove element command registration from CLI"
```

---

## Phase 12: Clean Up Documentation

### Task 22: Update or Remove Element Requirements

**Files:**
- Modify or delete: `docs/requirements/swr_elem_requirements.md`

- [ ] **Step 1: Decide on element requirements**

Either:
1. Delete the file entirely, or
2. Add a "Deprecated" notice at the top

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Deprecate element command requirements"
```

### Task 23: Update or Remove Element Test Specs

**Files:**
- Modify or delete: `docs/tests/unit/uts_elem_test-specs.md`

- [ ] **Step 1: Decide on element test specs**

Add deprecation notice or delete.

- [ ] **Step 2: Commit**

```bash
git commit -m "docs: Deprecate element command test specs"
```

### Task 24: Update Any Other Documentation

**Files:**
- Search for references to element command in docs

- [ ] **Step 1: Search for element command references**

```bash
grep -r "element" docs/
```

- [ ] **Step 2: Update or remove references**

Update any documentation that mentions the element command.

- [ ] **Step 3: Commit**

```bash
git commit -m "docs: Remove element command references from documentation"
```

---

## Phase 13: Final Verification

### Task 25: Run Full Test Suite and Quality Gates

- [ ] **Step 1: Run pytest**

```bash
pytest tests/unit -v
```

Expected: All tests pass (port tests included, element tests removed)

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

- [ ] **Step 5: Verify all 5 commands work**

```bash
python -m rhapsody_cli.cli package --help
python -m rhapsody_cli.cli class --help
python -m rhapsody_cli.cli operation --help
python -m rhapsody_cli.cli attribute --help
python -m rhapsody_cli.cli port --help
```

Expected: All 5 commands show help with their subcommands

- [ ] **Step 6: Verify element command removed**

```bash
python -m rhapsody_cli.cli element --help
```

Expected: Error - unknown command 'element'

- [ ] **Step 7: Final commit**

---

## Summary

**Completed:**
- Port command: 5 subcommands (create, delete, view, list, update)
- Element command removed: implementation, tests, registration, documentation
- Tests passing for all commands
- Quality gates passing
- All 5 element-specific commands working (package, class, operation, attribute, port)

**Total Implementation Summary (All 3 Plans):**

| Command | Subcommands | Status |
|---------|-------------|--------|
| `package` | create, delete, view, list, **update** | ✅ |
| `class` | create, delete, view, list, link, **update** | ✅ |
| `operation` | create, delete, view, list, update | ✅ |
| `attribute` | create, delete, view, list, update | ✅ |
| `port` | create, delete, view, list, update | ✅ |
| `element` | — | ❌ Removed |