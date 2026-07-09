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
The CLI SHALL provide a `package create` command to create one or multiple packages.

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
The CLI SHALL provide a `package delete` command to delete a package.

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
The CLI SHALL provide a `package view` command to view package details.

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
The CLI SHALL provide a `package list` command to list nested packages.

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
All package commands SHALL validate path before execution.

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
Package create command SHALL support external JSON files.

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
Package create command SHALL support stereotypes and tags.

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
Package view and list commands SHALL support multiple output formats.

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
Package view JSON output SHALL be reusable as package create input.

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
All package actions SHALL follow consistent error handling patterns.

- SHALL use _handle_execution_error() for COM errors
- SHALL raise CliExecutionError for validation failures
- SHALL log INFO for successful operations
- SHALL log WARNING for skipped attributes
- SHALL log ERROR for failures
**Implementation:** src/rhapsody_cli/actions/package_action.py:AbstractPackageAction
**Last Changed:** 2026-07-09
