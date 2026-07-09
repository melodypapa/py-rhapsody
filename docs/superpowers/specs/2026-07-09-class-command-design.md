# Class Command Design

**Date:** 2026-07-09
**Status:** Approved
**Author:** User + Assistant

## Overview

Implement a `class` command group for managing Rhapsody RPClass elements via CLI. The design mirrors the existing `package` command structure, with 5 subcommands: create, delete, view, list, and link.

## Architecture

Follows the package command pattern exactly:

### AbstractClassAction (Base Class)

Base class with two path validation methods:

- `_resolve_and_validate_package(path)` - Validates path resolves to Package (metaClass == "Package"). Used by create and list.
- `_resolve_and_validate_class(path)` - Validates path resolves to Class (metaClass == "Class"). Used by delete, view, and link.

Inherits from `ElementManagementAction`.

### 5 Action Classes

1. **ClassCreateAction** - Create classes with bulk JSON support, validated attributes
2. **ClassDeleteAction** - Delete a class via `deleteFromProject()`
3. **ClassViewAction** - View class details in table/JSON/CSV formats
4. **ClassListAction** - List classes in a package via `getClasses()`
5. **ClassLinkAction** - Add/remove relationships between classes (generalization, association, unidirectional)

## Subcommands

### create

Create one or multiple classes under a parent package.

**Arguments:**
- `--path <parent-package-path>` (required) - Parent package path
- `--input <json-file>` (optional) - External JSON file
- `attributes` (positional, optional) - Inline JSON or JSON file path

**Validated Attributes:**

| Attribute | Type | COM Method |
|-----------|------|------------|
| `name` | string (required) | `package.addClass(name)` |
| `description` | string | `setDescription()` |
| `isAbstract` | bool | `setIsAbstract(1/0)` |
| `isFinal` | bool | `setIsFinal(1/0)` |
| `isActive` | bool | `setIsActive(1/0)` |
| `stereotypes` | array of strings | `addStereotype(name, "Class")` |
| `tags` | dict (key-value) | `setPropertyValue(key, val)` |
| `operations` | array of strings | `addOperation(name)` |
| `attributes` | array of strings | `addAttribute(name)` |
| `superclasses` | array of strings | `addGeneralization(class)` (resolved by name lookup) |

**Bulk creation:** Supports JSON array for creating multiple classes at once.

**Unknown attributes:** Skipped with warning log.

**External JSON file support:** Detects inline JSON (starts with `{` or `[`) vs file path automatically. Reads with UTF-8 encoding.

**Example JSON:**
```json
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
```

**Attribute setting methods (following single responsibility principle):**

- `_set_attributes()` - Orchestrates all attribute setting
- `_set_basic_attributes()` - Sets description
- `_set_boolean_flags()` - Sets isAbstract, isFinal, isActive
- `_set_properties()` - Sets custom properties (tags)
- `_set_stereotypes()` - Applies stereotypes
- `_set_operations()` - Adds operations
- `_set_attributes_list()` - Adds attributes
- `_set_superclasses()` - Adds generalization relationships

### delete

Delete a class.

**Arguments:**
- `--path <class-path>` (required) - Class path to delete

**Behavior:** Calls `deleteFromProject()` on the resolved class. Logs deletion to stderr.

### view

View class details.

**Arguments:**
- `--path <class-path>` (required) - Class path to view
- `--format <table|json|csv>` (optional, default: table) - Output format
- `--output <file>` (optional) - Write to file instead of stdout

**View Fields:**

| Field | Source Method |
|-------|---------------|
| Name | `getName()` |
| GUID | `getGUID()` |
| Description | `getDescription()` |
| IsAbstract | `getIsAbstract()` |
| IsActive | `getIsActive()` |
| IsFinal | `getIsFinal()` |
| IsComposite | `getIsComposite()` |
| IsReactive | `getIsReactive()` |
| MetaClass | `getMetaClass()` |
| FullPath | `getFullPathName()` |

**Output Formats:**

**Table format:**
```
Property     | Value
-------------|---------------------
Name         | TemperatureSensor
GUID         | {12345678-...}
Description  | Temperature sensor
IsAbstract   | 0
IsActive     | 1
IsFinal      | 0
IsComposite  | 0
IsReactive   | 0
MetaClass    | Class
FullPath     | Sensors/TemperatureSensor
```

**JSON format:**
```json
{
  "name": "TemperatureSensor",
  "guid": "{12345678-...}",
  "description": "Temperature sensor",
  "isAbstract": 0,
  "isActive": 1,
  "isFinal": 0,
  "isComposite": 0,
  "isReactive": 0,
  "metaClass": "Class",
  "fullPath": "Sensors/TemperatureSensor"
}
```

**CSV format (horizontal):**
```
Name,GUID,Description,IsAbstract,IsActive,IsFinal,IsComposite,IsReactive,MetaClass,FullPath
TemperatureSensor,{12345678-...},Temperature sensor,0,1,0,0,0,Class,Sensors/TemperatureSensor
```

**View-to-Create Workflow:** The JSON output from `view` can be used as input to `create`. Unknown fields (guid, isComposite, isReactive, metaClass, fullPath) are skipped during create with a warning.

### list

List classes in a package.

**Arguments:**
- `--path <package-path>` (required) - Package path
- `--format <table|json|csv>` (optional, default: table) - Output format
- `--output <file>` (optional) - Write to file instead of stdout

**Output Formats:**

**Table format:**
```
Name
--------------------
TemperatureSensor
PressureSensor
HumiditySensor
```

**JSON format:**
```json
["TemperatureSensor", "PressureSensor", "HumiditySensor"]
```

**CSV format (horizontal):**
```
Name
TemperatureSensor
PressureSensor
HumiditySensor
```

### link

Manage relationships between classes on an existing class.

**Arguments:**
- `--path <class-path>` (required) - Class path to modify
- `--add <class-name>` (optional) - Add a relationship to target class by name
- `--remove <class-name>` (optional) - Remove a relationship to target class by name
- `--type <generalization|association|unidirectional>` (optional, default: generalization) - Relationship type

**Relationship Types:**

| Type | COM Method (add) | COM Method (remove) |
|------|-------------------|---------------------|
| `generalization` | `addGeneralization(target)` | `deleteGeneralization(target)` |
| `association` | `addRelation(target)` | `deleteRelation(target)` |
| `unidirectional` | `addUnidirectionalRelation(target)` | `deleteRelation(target)` |

**Behavior:**
- `--add`: Resolves the target class by name in the same package, calls the appropriate add method based on `--type`
- `--remove`: Resolves the target class by name, calls the appropriate delete method based on `--type`
- Exactly one of `--add` or `--remove` must be specified

**Example:**
```
rhapsody-cli class link --path Sensors/TemperatureSensor --add BaseSensor
rhapsody-cli class link --path Sensors/TemperatureSensor --add SensorInterface --type association
rhapsody-cli class link --path Sensors/TemperatureSensor --remove BaseSensor
```

## Path Validation

All commands validate path before execution (SWR_CLS_0005):

- **create, list**: Path must resolve to Package (metaClass == "Package")
- **delete, view, link**: Path must resolve to Class (metaClass == "Class")
- Path resolution uses PathResolver for multi-level navigation
- Errors raised via CliExecutionError with descriptive message

## Error Handling and Logging

All class actions follow consistent error handling patterns (SWR_CLS_0010):

- Use `_handle_execution_error()` for COM errors
- Raise `CliExecutionError` for validation failures
- Log INFO for successful operations
- Log WARNING for skipped attributes
- Log ERROR for failures

## File Structure

**New files:**
- `src/rhapsody_cli/actions/class_action.py` - 6 Action classes (AbstractClassAction + 5 concrete)
- `src/rhapsody_cli/commands/class_command.py` - Command dispatcher
- `tests/unit/actions/test_class_action.py` - Action tests
- `tests/unit/commands/test_class_command.py` - Command tests
- `docs/requirements/swr_cls_requirements.md` - SW requirements
- `docs/tests/unit/uts_cls_test-specs.md` - Unit test specs
- `docs/user_guide/working_with_classes.rst` - User documentation

**Modified files:**
- `src/rhapsody_cli/cli/cli.py` - Register `class` command

## SW Requirements IDs

- SWR_CLS_0001: Class Create Command
- SWR_CLS_0002: Class Delete Command
- SWR_CLS_0003: Class View Command
- SWR_CLS_0004: Class List Command
- SWR_CLS_0005: Path Validation
- SWR_CLS_0006: External JSON File Support
- SWR_CLS_0007: Stereotype and Tag Support
- SWR_CLS_0008: Multi-Format Output
- SWR_CLS_0009: View-to-Create Workflow
- SWR_CLS_0010: Error Handling and Logging
- SWR_CLS_0011: Class Link Command
- SWR_CLS_0012: Boolean Flag Support

## Test Case IDs

- UTS_CLS_00001 - UTS_CLS_00030 (estimated)
