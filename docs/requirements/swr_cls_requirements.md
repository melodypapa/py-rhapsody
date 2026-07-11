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

## SWR_CLS_00014: Class Update Command

**ID:** SWR_CLS_00014
**Title:** class update command modifies class attributes
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class update` command to modify attributes of an existing class.
- SHALL accept `--path <class-path>` argument (optional) - full path to class (including name, e.g. Sensors/TemperatureSensor)
- SHALL accept `--guid <guid>` argument (optional) - class GUID
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--input <json-file>` argument (optional) - external JSON file
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL validate path/guid resolves to Class element (metaClass == "Class")
- SHALL validate type when using --guid (metaClass == "Class", raise CliExecutionError if mismatch)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, description, isAbstract, isFinal, isActive, stereotypes, tags
- SHALL apply name via `setName(val)`, description via `setDescription(val)`
- SHALL apply boolean flags via `setIsAbstract(1/0)`, `setIsFinal(1/0)`, `setIsActive(1/0)`
- SHALL apply stereotypes via `addStereotype(name, "Class")`
- SHALL apply tags via `setPropertyValue(key, val)`
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL log INFO for successful updates
- SHALL log WARNING for skipped attributes
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassUpdateAction
**Last Changed:** 2026-07-10