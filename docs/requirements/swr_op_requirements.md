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
