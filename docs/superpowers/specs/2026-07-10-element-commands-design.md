# Design Specification: Operation, Attribute, and Port Commands

**Date:** 2026-07-10
**Status:** Draft
**Related:** Class command implementation (2026-07-09-class-command-design.md)

---

## Overview

Create three new CLI command groups for managing operations, attributes, and ports on Rhapsody classifiers (Class, Actor, etc.). These commands replace the generic `element` command with specific element-type commands.

---

## Commands Structure

| Command | Subcommands | Parent Element |
|---------|-------------|----------------|
| `operation` | create, delete, view, list, update | Classifier (Class/Actor) |
| `attribute` | create, delete, view, list, update | Classifier |
| `port` | create, delete, view, list, update | Classifier |

### Common Patterns (inherited from class/package commands)

- **Path format:** `--path <class-path>` identifies the parent classifier
- **Element identification:** `--name <element-name>` for delete/view/update
- **GUID support:** `--guid` for view/delete (optional alternative to path+name)
- **Output formats:** `--format table|json|csv` for view/list (default: table)
- **File output:** `--output <file>` optional
- **JSON input:** Inline JSON or `--input <file>` for create/update
- **Bulk creation:** JSON array support for create

---

## Operation Command

### Subcommands

#### `operation create`

Create one or more operations on a classifier.

**Arguments:**
- `--path <class-path>` (required) - parent classifier path
- `--input <json-file>` (optional) - external JSON file
- `attributes` (positional) - inline JSON or file path

**JSON fields (validated):**
| Field | Type | Setter Method | Notes |
|-------|------|---------------|-------|
| `name` | string | `addOperation(name)` | required |
| `body` | string | `setBody(body)` | optional |
| `isAbstract` | bool | `setIsAbstract(1/0)` | optional |
| `isStatic` | bool | `setIsStatic(1/0)` | optional |
| `isVirtual` | bool | `setIsVirtual(1/0)` | optional |
| `returns` | string | resolve type, set via API | optional, type name |
| `visibility` | string | `setVisibility(val)` | optional, e.g. "public" |
| `arguments` | string | `setArguments(val)` | optional, argument declaration |
| `description` | string | `setDescription(val)` | optional |

**Example:**
```bash
rhapsody-cli operation create --path Sensors/TemperatureSensor '{"name":"readValue","returns":"float","visibility":"public"}'
```

#### `operation delete`

Delete an operation from a classifier.

**Arguments:**
- `--path <class-path>` (optional) - parent classifier path
- `--guid <guid>` (optional) - operation GUID
- `--name <operation-name>` (optional) - operation name within class
- Requires exactly one of `--path` + `--name` OR `--guid`

**Resolution:**
- By GUID: `findElementByGUID(guid)`
- By path+name: resolve class, then `findInterfaceItem(name)` or iterate `getOperations()`

#### `operation view`

Display details of a single operation.

**Arguments:**
- `--path <class-path>` (optional)
- `--guid <guid>` (optional)
- `--name <operation-name>` (optional)
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Display fields:**
- Name, GUID, Description, Body, IsAbstract, IsStatic, IsVirtual, Returns, Visibility, Arguments, MetaClass, FullPath

#### `operation list`

List all operations on a classifier.

**Arguments:**
- `--path <class-path>` (required)
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Output:** List of operation names (table: single column, JSON: array of strings, CSV: 1-column horizontal)

#### `operation update`

Update attributes of an existing operation.

**Arguments:**
- `--path <class-path>` (optional)
- `--guid <guid>` (optional)
- `--name <operation-name>` (optional)
- `--input <json-file>` (optional)
- `attributes` (positional) - inline JSON with fields to update

**Behavior:** Partial update - only specified fields are modified. Same validated fields as create.

---

## Attribute Command

### Subcommands

#### `attribute create`

Create one or more attributes on a classifier.

**Arguments:**
- `--path <class-path>` (required)
- `--input <json-file>` (optional)
- `attributes` (positional) - inline JSON or file path

**JSON fields (validated):**
| Field | Type | Setter Method | Notes |
|-------|------|---------------|-------|
| `name` | string | `addAttribute(name)` | required |
| `type` | string | resolve type, `setType(classifier)` | optional, type name |
| `defaultValue` | string | `setDefaultValue(val)` | optional |
| `multiplicity` | string | `setMultiplicity(val)` | optional, e.g. "1", "0..*" |
| `isStatic` | bool | `setIsStatic(1/0)` | optional |
| `visibility` | string | `setVisibility(val)` | optional, e.g. "private" |
| `declaration` | string | `setDeclaration(val)` | optional, on-the-fly type |
| `description` | string | `setDescription(val)` | optional |

**Example:**
```bash
rhapsody-cli attribute create --path Sensors/TemperatureSensor '{"name":"value","type":"float","visibility":"private"}'
```

#### `attribute delete`

Delete an attribute from a classifier.

**Arguments:**
- `--path <class-path>` (optional)
- `--guid <guid>` (optional)
- `--name <attribute-name>` (optional)
- Requires exactly one of `--path` + `--name` OR `--guid`

**Resolution:**
- By GUID: `findElementByGUID(guid)`
- By path+name: resolve class, then `findAttribute(name)`

#### `attribute view`

Display details of a single attribute.

**Arguments:**
- `--path <class-path>` (optional)
- `--guid <guid>` (optional)
- `--name <attribute-name>` (optional)
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Display fields:**
- Name, GUID, Description, Type, DefaultValue, Multiplicity, IsStatic, Visibility, Declaration, MetaClass, FullPath

#### `attribute list`

List all attributes on a classifier.

**Arguments:**
- `--path <class-path>` (required)
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Output:** List of attribute names

#### `attribute update`

Update attributes of an existing attribute.

**Arguments:**
- Same as operation update
- JSON fields: same validated fields as create (partial update)

---

## Port Command

### Subcommands

#### `port create`

Create one or more ports on a classifier.

**Arguments:**
- `--path <class-path>` (required)
- `--input <json-file>` (optional)
- `attributes` (positional) - inline JSON or file path

**JSON fields (validated):**
| Field | Type | Setter Method | Notes |
|-------|------|---------------|-------|
| `name` | string | `addPort(name)` | required |
| `isBehavioral` | int (0/1) | `setIsBehavioral(val)` | optional |
| `isReversed` | int (0/1) | `setIsReversed(val)` | optional |
| `portContract` | string | resolve class, `setPortContract(class)` | optional, interface class name |
| `description` | string | `setDescription(val)` | optional |

**Example:**
```bash
rhapsody-cli port create --path Sensors/TemperatureSensor '{"name":"inputPort","isBehavioral":1}'
```

#### `port delete`

Delete a port from a classifier.

**Arguments:**
- `--path <class-path>` (optional)
- `--guid <guid>` (optional)
- `--name <port-name>` (optional)
- Requires exactly one of `--path` + `--name` OR `--guid`

**Resolution:**
- By GUID: `findElementByGUID(guid)`
- By path+name: resolve class, iterate `getPorts()` to find by name

**Deletion:** `deleteFromProject()` (no dedicated deletePort method)

#### `port view`

Display details of a single port.

**Arguments:**
- Same pattern as operation/attribute view
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Display fields:**
- Name, GUID, Description, IsBehavioral, IsReversed, PortContract, MetaClass, FullPath

#### `port list`

List all ports on a classifier.

**Arguments:**
- `--path <class-path>` (required)
- `--format table|json|csv` (default: table)
- `--output <file>` (optional)

**Output:** List of port names

#### `port update`

Update attributes of an existing port.

**Arguments:**
- Same pattern as operation/attribute update
- JSON fields: same validated fields as create (partial update)

---

## Implementation Structure

### Files (following class command pattern)

```
src/rhapsody_cli/actions/
  operation_action.py    - AbstractOperationAction + 5 concrete actions
  attribute_action.py    - AbstractAttributeAction + 5 concrete actions
  port_action.py         - AbstractPortAction + 5 concrete actions

src/rhapsody_cli/commands/
  operation_command.py   - OperationCommand dispatcher
  attribute_command.py   - AttributeCommand dispatcher
  port_command.py        - PortCommand dispatcher

tests/unit/actions/
  test_operation_action.py
  test_attribute_action.py
  test_port_action.py

tests/unit/commands/
  test_operation_command.py
  test_attribute_command.py
  test_port_command.py

docs/requirements/
  swr_op_requirements.md   - SW requirements (SWR_OP_00001-...)
  swr_attr_requirements.md - SW requirements (SWR_ATTR_00001-...)
  swr_port_requirements.md - SW requirements (SWR_PORT_00001-...)

docs/tests/unit/
  uts_op_test-specs.md     - Unit test specs
  uts_attr_test-specs.md   - Unit test specs
  uts_port_test-specs.md   - Unit test specs

docs/user_guide/
  working_with_operations.rst
  working_with_attributes.rst
  working_with_ports.rst
```

### Class Structure (mirroring class command)

Each command follows the pattern:
```
AbstractOperationAction(ElementManagementAction)
  - _resolve_and_validate_classifier(path) -> classifier
  - _resolve_operation_by_guid(guid) -> operation
  - _resolve_operation_by_name(classifier, name) -> operation

OperationCreateAction(AbstractOperationAction)
OperationDeleteAction(AbstractOperationAction)
OperationViewAction(AbstractOperationAction)
OperationListAction(AbstractOperationAction)
OperationUpdateAction(AbstractOperationAction)

OperationCommand(AbstractCommand)
  - get_actions() -> [Create, Delete, View, List, Update]
```

---

## Element Command Removal

After creating operation, attribute, and port commands, remove the `element` command:

1. Remove `src/rhapsody_cli/commands/element_command.py`
2. Remove `src/rhapsody_cli/actions/element_action.py`
3. Remove `tests/unit/commands/test_element_command.py`
4. Remove `tests/unit/actions/test_element_action.py`
5. Remove element command registration from `cli.py`
6. Update SW requirements (remove SWR_ELEM references)
7. Update test specs (remove UTS_ELEM references)
8. Update documentation

---

## Error Handling (consistent with existing commands)

- Path not found: CliExecutionError with "not found" message
- Wrong element type: CliExecutionError with expected/found type message
- COM errors: use `_handle_execution_error()` pattern
- Validation failures: CliExecutionError with clear message
- Logging: INFO for success, WARNING for skipped attributes, ERROR for failures

---

## Testing Strategy

Follow TDD approach as used in class command:
1. Write test first, verify failure
2. Implement action/command
3. Verify tests pass
4. Run ruff + mypy + black
5. Commit

Each action class gets unit tests covering:
- Success cases (create, delete, view, list, update)
- Error cases (path not found, wrong type, COM error)
- Output format variations (table, JSON, CSV)
- Bulk operations
- Edge cases (empty list, missing name, etc.)

---

## Success Criteria

- All 3 commands (operation, attribute, port) implemented with 5 subcommands each
- Element command removed
- 624+ tests passing (after adding new tests)
- Ruff + mypy + black passing
- Documentation complete (requirements, test specs, user guides)
- CLI help updated to show new commands