# Software Requirements - Attribute Command

**Category:** Attribute Command
**Prefix:** SWR_ATTR
**Source:** Extracted from spec 2026-07-10-element-commands-design.md
**Last Validated:** 2026-07-10

---

## SWR_ATTR_00001: Attribute Create Command

**ID:** SWR_ATTR_00001
**Title:** attribute create command creates one or multiple attributes
**Status:** Planned
**Priority:** High
**Description:**
The attribute CLI
- SHALL provide a `attribute create` command to create one or multiple attributes.
- SHALL accept `--path <class-path>` argument (required) - parent classifier path
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path resolves to Classifier element
- SHALL create attributes via `classifier.addAttribute(name)`
- SHALL set validated attributes: name, type, defaultValue, multiplicity, isStatic, visibility, declaration, description
- SHALL apply name via `addAttribute()`, type via `setType()`, defaultValue via `setDefaultValue()`, multiplicity via `setMultiplicity()`, isStatic via `setIsStatic(1/0)`, visibility via `setVisibility()`, declaration via `setDeclaration()`, description via `setDescription()`
- SHALL resolve type by name via `findNestedClassifierRecursive(type_name)` on parent classifier's package
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{` or `[`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeCreateAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00002: Attribute Delete Command

**ID:** SWR_ATTR_00002
**Title:** attribute delete command deletes an attribute
**Status:** Planned
**Priority:** High
**Description:**
The attribute CLI
- SHALL provide a `attribute delete` command to delete an attribute.
- SHALL accept `--path <class-path>` argument (optional) - parent classifier path
- SHALL accept `--guid <guid>` argument (optional) - attribute GUID
- SHALL accept `--name <attribute-name>` argument (optional) - attribute name within class
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Attribute", raise CliExecutionError if mismatch)
- SHALL resolve attribute via `findAttribute(name)`
- SHALL delete attribute via `deleteAttribute(attr)`
- SHALL log deletion to stderr
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeDeleteAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00003: Attribute View Command

**ID:** SWR_ATTR_00003
**Title:** attribute view command displays attribute details
**Status:** Planned
**Priority:** High
**Description:**
The attribute CLI
- SHALL provide a `attribute view` command to view attribute details.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <attribute-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Attribute")
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display fields: Name, GUID, Description, Type, DefaultValue, Multiplicity, IsStatic, Visibility, Declaration, MetaClass, FullPath
- SHALL support table (Property|Value layout), JSON (11-key object), CSV (horizontal 11-column) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeViewAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00004: Attribute List Command

**ID:** SWR_ATTR_00004
**Title:** attribute list command lists attributes on a classifier
**Status:** Planned
**Priority:** High
**Description:**
The attribute CLI
- SHALL provide a `attribute list` command to list attributes on a classifier.
- SHALL accept `--path <class-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list attributes via `getAttributes()` and collect names via `getName()`
- SHALL support table (single Name column), JSON (array of strings), CSV (1-column horizontal) output formats
- SHALL write to file if `--output` specified, else stdout
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeListAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00005: Attribute Update Command

**ID:** SWR_ATTR_00005
**Title:** attribute update command modifies attribute attributes
**Status:** Planned
**Priority:** High
**Description:**
The attribute CLI
- SHALL provide a `attribute update` command to modify attributes of an existing attribute.
- SHALL accept `--path <class-path>` argument (optional)
- SHALL accept `--guid <guid>` argument (optional)
- SHALL accept `--name <attribute-name>` argument (optional)
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL validate type when using --guid (metaClass == "Attribute", raise CliExecutionError if mismatch)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, type, defaultValue, multiplicity, isStatic, visibility, declaration, description
- SHALL skip unknown attributes with warning log
- SHALL log INFO for successful updates
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeUpdateAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00006: Path and Name Validation

**ID:** SWR_ATTR_00006
**Title:** All attribute commands validate path and name before execution
**Status:** Planned
**Priority:** High
**Description:**
All attribute commands
- SHALL validate path before execution.
- SHALL resolve classifier path using PathResolver
- SHALL resolve attribute by name within classifier
- SHALL raise CliExecutionError if path not found
- SHALL raise CliExecutionError if attribute name not found in classifier
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AbstractAttributeAction._resolve_classifier, _resolve_attribute
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00007: External JSON File Support

**ID:** SWR_ATTR_00007
**Title:** Attribute create/update supports external JSON files
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute create and update commands
- SHALL support external JSON files.
- SHALL accept `--input <file>` argument
- SHALL accept file path as positional argument
- SHALL detect inline JSON vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL raise CliExecutionError if file not found
- SHALL raise CliExecutionError if JSON invalid
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeCreateAction._load_json_data
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00008: Multi-Format Output

**ID:** SWR_ATTR_00008
**Title:** Attribute view and list support multiple output formats
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute view and list commands
- SHALL support multiple output formats.
- SHALL support table format (default, human-readable)
- SHALL support JSON format (machine-parsable)
- SHALL support CSV format (spreadsheet-friendly)
- SHALL use horizontal layout for CSV (header row + data rows)
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeViewAction._format_output, AttributeListAction._format_output
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00009: Error Handling and Logging

**ID:** SWR_ATTR_00009
**Title:** All attribute actions follow consistent error handling patterns
**Status:** Planned
**Priority:** High
**Description:**
All attribute actions
- SHALL follow consistent error handling patterns.
- SHALL use `_handle_execution_error()` for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AbstractAttributeAction
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00010: GUID Lookup Support

**ID:** SWR_ATTR_00010
**Title:** Attribute view/delete/update support --guid as alternative to --path + --name
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute view, delete, and update commands
- SHALL support `--guid` as alternative to `--path` + `--name`.
- SHALL accept `--guid <guid>` argument
- SHALL require exactly one of `--path` + `--name` OR `--guid`
- SHALL locate attribute by GUID via `findElementByGUID(guid)` on the active project
- SHALL validate located element is Attribute (metaClass == "Attribute")
- SHALL raise CliExecutionError if GUID not found
- SHALL raise CliExecutionError if GUID resolves to wrong type
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AbstractAttributeAction._resolve_attribute_by_guid
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00011: Type Resolution

**ID:** SWR_ATTR_00011
**Title:** Attribute create/update resolves type by name
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute create and update commands
- SHALL resolve attribute type by name.
- SHALL accept `type` field as type name string
- SHALL resolve type via `findNestedClassifierRecursive(type_name)` on parent classifier's package
- SHALL raise CliExecutionError if type name not found
- SHALL set resolved type classifier on attribute via `setType()`
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeCreateAction._resolve_type
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00012: IsStatic Flag Support

**ID:** SWR_ATTR_00012
**Title:** Attribute create/update supports isStatic flag
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute create and update commands
- SHALL support isStatic flag.
- SHALL accept `isStatic` bool in JSON, set via `setIsStatic(1/0)`
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeCreateAction._set_boolean_flags
**Last Changed:** 2026-07-10

---

## SWR_ATTR_00013: Bulk Creation Support

**ID:** SWR_ATTR_00013
**Title:** Attribute create supports bulk creation via JSON array
**Status:** Planned
**Priority:** Medium
**Description:**
Attribute create command
- SHALL support bulk creation.
- SHALL accept JSON array of attribute definitions
- SHALL create each attribute in sequence
- SHALL log INFO with count of created attributes
**Implementation:** src/rhapsody_cli/actions/attribute_action.py:AttributeCreateAction.execute
**Last Changed:** 2026-07-10
