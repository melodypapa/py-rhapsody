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
The package CLI
- SHALL provide a `package create` command to create one or multiple packages.
- SHALL accept `--path <parent-path>` argument (optional; defaults to project root when omitted)
- SHALL accept `--input <json-file>` argument (optional)
- SHALL accept positional `attributes` argument (inline JSON or file path)
- SHALL support bulk creation via JSON array
- SHALL validate parent path (when given) resolves to Package element
- SHALL create nested packages under parent (when parent path given) or at project root (when parent path omitted)
- SHALL set validated attributes: name, description, description_html, description_rtf, display_name, display_name_rtf, properties, stereotypes, tags
- SHALL apply name via addNestedPackage() for nested, or addPackage() for root-level
- SHALL apply description via setDescription(), properties via setPropertyValue(), stereotypes via addStereotype(), tags via setPropertyValue()
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{` or `[`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction
**Last Changed:** 2026-07-10

---

## SWR_PKG_0002: Package Delete Command

**ID:** SWR_PKG_0002
**Title:** package delete command deletes a package
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
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
The package CLI
- SHALL provide a `package view` command to view package details.
- SHALL accept `--path <package-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL display package properties: name, GUID, description, metaClass, fullPath
- SHALL support table format with vertical key-value layout (Property | Value columns, 5 rows: Name, GUID, Description, MetaClass, FullPath)
- SHALL support JSON format as a single object: `{"name":"...","guid":"...","description":"...","metaClass":"...","fullPath":"..."}`
- SHALL support CSV format with horizontal layout: header row `Name,GUID,Description,MetaClass,FullPath` followed by one data row
- SHALL write to file if `--output` specified, else stdout
- SHALL output to stdout or file (not logger) for safe use in scripts

**Table format example:**
```
+-----------+--------------------------------------+
| Property  | Value                                |
+-----------+--------------------------------------+
| Name      | TempSensors                          |
| GUID      | {12345678-1234-1234-1234-1234567890} |
| Description| Temperature sensors package         |
| MetaClass | Package                              |
| FullPath  | Sensors/TempSensors                  |
+-----------+--------------------------------------+
```

**JSON format example:**
```json
{
  "name": "TempSensors",
  "guid": "{12345678-1234-1234-1234-1234567890}",
  "description": "Temperature sensors package",
  "metaClass": "Package",
  "fullPath": "Sensors/TempSensors"
}
```

**CSV format example:**
```text
Name,GUID,Description,MetaClass,FullPath
TempSensors,{12345678-1234-1234-1234-1234567890},Temperature sensors package,Package,Sensors/TempSensors
```
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageViewAction
**Last Changed:** 2026-07-09

---

## SWR_PKG_0004: Package List Command

**ID:** SWR_PKG_0004
**Title:** package list command lists nested packages
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package list` command to list nested packages.
- SHALL accept `--path <package-path>` argument (required)
- SHALL accept `--format <format>` argument (table/json/csv, default: table)
- SHALL accept `--output <file>` argument (optional)
- SHALL list all nested packages under parent
- SHALL support table format with single Name column, one row per nested package
- SHALL support JSON format as an array of package name strings: `["TempSensors","PressureSensors","FlowSensors"]`
- SHALL support CSV format with horizontal layout: header row `Name` followed by one data row per package
- SHALL write to file if `--output` specified, else stdout
- SHALL output to stdout or file (not logger) for safe use in scripts
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
- SHALL accept `stereotypes` array in JSON (e.g. `["auto_generated","version_1_0"]`)
- SHALL apply each stereotype via addStereotype(name, "Package") method
- SHALL accept `tags` object in JSON (e.g. `{"status":"active","version":"1.0.0"}`)
- SHALL set each tag via setPropertyValue(key, value) method
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
- SHALL support table format (default, human-readable): vertical key-value layout (Property | Value) for view, single Name column for list
- SHALL support JSON format (machine-parsable): single object with 5 keys (name, guid, description, metaClass, fullPath) for view, array of name strings for list
- SHALL support CSV format (spreadsheet-friendly): horizontal layout with header row + data rows
- SHALL use 5 columns for view CSV: `Name,GUID,Description,MetaClass,FullPath`
- SHALL use 1 column for list CSV: `Name`
- SHALL use horizontal layout for CSV (header row + data rows, not vertical key-value pairs)
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

---

## SWR_PKG_0011: Package View Output Format Examples

**ID:** SWR_PKG_0011
**Title:** Package view output format examples for table, JSON, and CSV
**Status:** Planned
**Priority:** Medium
**Description:**
Package view command
- SHALL produce the following output formats.

Table format (default):
```
+-----------+--------------------------------------+
| Property  | Value                                |
+-----------+--------------------------------------+
| Name      | TempSensors                          |
| GUID      | {12345678-1234-1234-1234-1234567890} |
| Description| Temperature sensors package         |
| MetaClass | Package                              |
| FullPath  | Sensors/TempSensors                  |
+-----------+--------------------------------------+
```

JSON format:
```json
{
  "name": "TempSensors",
  "guid": "{12345678-1234-1234-1234-1234567890}",
  "description": "Temperature sensors package",
  "metaClass": "Package",
  "fullPath": "Sensors/TempSensors"
}
```

CSV format:
```text
Name,GUID,Description,MetaClass,FullPath
TempSensors,{12345678-1234-1234-1234-1234567890},Temperature sensors package,Package,Sensors/TempSensors
```

**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageViewAction._format_output
**Last Changed:** 2026-07-09

---

## SWR_PKG_0012: Package List Output Format Examples

**ID:** SWR_PKG_0012
**Title:** Package list output format examples for table, JSON, and CSV
**Status:** Planned
**Priority:** Medium
**Description:**
Package list command
- SHALL produce the following output formats.

Table format (default):
```
+----------------+
| Name           |
+----------------+
| TempSensors    |
| PressureSensors|
| FlowSensors    |
+----------------+
```

JSON format:
```json
["TempSensors", "PressureSensors", "FlowSensors"]
```

CSV format:
```text
Name
TempSensors
PressureSensors
FlowSensors
```

**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageListAction._format_output
**Last Changed:** 2026-07-09

---

## SWR_PKG_0016: Package Update Command

**ID:** SWR_PKG_0016
**Title:** package update command modifies package attributes
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package update` command to modify attributes of an existing package.
- SHALL accept `--path <package-path>` argument (optional) - full path to package (including name, e.g. Sensors/TempSensors)
- SHALL accept `--guid <guid>` argument (optional) - package GUID
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--input <json-file>` argument (optional) - external JSON file
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL validate path/guid resolves to Package element (metaClass == "Package")
- SHALL validate type when using --guid (metaClass == "Package", raise CliExecutionError if mismatch)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, description, display_name, stereotypes, tags, properties
- SHALL apply name via `setName(val)`, description via `setDescription(val)`, display_name via `setDisplayName(val)`
- SHALL apply stereotypes via `addStereotype(name, "Package")`
- SHALL apply tags and properties via `setPropertyValue(key, val)`
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL log INFO for successful updates
- SHALL log WARNING for skipped attributes
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageUpdateAction
**Last Changed:** 2026-07-10

## SWR_PKG_0013: Package Create with Default Root

**ID:** SWR_PKG_0013
**Title:** package create defaults to project root when --path is omitted
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL allow `--path` argument on `package create` to be optional
- When `--path` is omitted (None or empty string), SHALL create the package directly under the project root
- When creating at project root, SHALL use the `RPProject.addPackage()` method (top-level package creation)
- When creating under an existing package, SHALL use `RPPackage.addNestedPackage()` method (nested package creation)
- Reported/logged full paths for root-level packages SHALL not include leading `None/` or empty-segment artifacts (e.g., `"MyPackage"` not `"None/MyPackage"`)
- All other package attributes, stereotypes, tags, and error handling remain unchanged
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction
**Last Changed:** 2026-07-10

---

## SWR_PKG_0014: Package Command Execution Logging

**ID:** SWR_PKG_0014
**Title:** package commands log execution steps at INFO level
**Status:** Planned
**Priority:** Medium
**Description:**
The package commands SHALL emit INFO-level log messages showing execution progress, enabling end-users to understand what the CLI is doing at each stage:

**Package Create Logging:**
- SHALL log "Starting package creation..." at operation start
- SHALL log "Creating packages at project root..." when --path is omitted
- SHALL log "Resolving parent path 'X'..." when --path is provided
- SHALL log "Creating package 'Y'..." for each package being created
- SHALL log "Setting attributes for package 'Y'..." when attributes (beyond name) are being set
- SHALL log "Created package: Z" for each successfully created package
- SHALL log "Successfully created N package(s)" with count summary at completion

**Package Delete Logging:**
- SHALL log "Starting package deletion..." at operation start
- SHALL log "Resolving package path 'X'..." before path resolution
- SHALL log "Deleting package 'X'..." before deletion
- SHALL log "Successfully deleted package 'X'" after successful deletion

**Package View Logging:**
- SHALL log "Starting package view operation..." at operation start
- SHALL log "Resolving package path 'X'..." before path resolution
- SHALL log "Retrieving package details..." before data collection
- SHALL log "Writing output to file 'X'" when writing to file (when --output specified)

**Package List Logging:**
- SHALL log "Starting package list operation..." at operation start
- SHALL log "Resolving package path 'X'..." before path resolution
- SHALL log "Listing nested packages..." before collection
- SHALL log "Found N nested package(s)" or "No nested packages found" with count of nested packages
- SHALL log "Writing output to file 'X'" when writing to file (when --output specified)

**Common Requirements:**
- All execution-step logs SHALL use INFO level (visible by default, not requiring --verbose flag)
- Error logs for operation failures SHALL use ERROR level (already in place)
- Logs SHALL be emitted to the standard logger for the package_action module
**Implementation:** src/rhapsody_cli/actions/package_action.py (all 4 action classes)
**Last Changed:** 2026-07-10

---

## SWR_PKG_0015: Package Create Duplicate Detection

**ID:** SWR_PKG_0015
**Title:** package create detects and reports duplicate package names
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL detect when a package with the given name already exists in the target container (project root or parent package) before attempting creation
- SHALL report a user-friendly error message when a duplicate package name is detected
- Error message SHALL follow the format: `"Package 'X' already exists in [project root|package 'Y']"`
- Duplicate detection SHALL use case-sensitive name comparison (matching Rhapsody behavior)
- Duplicate detection SHALL be performed by iterating through existing packages via `getPackages()` (for root) or `getNestedPackages()` (for nested)
- When a duplicate is detected, SHALL raise `CliExecutionError` with the user-friendly message (not allow COM exception to bubble up)
- Duplicate check SHALL occur before attempting the `addPackage()` or `addNestedPackage()` COM call (fail-fast approach)
- Logging SHALL include "Checking if package 'X' already exists..." before the check
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageCreateAction._check_package_not_exists
**Last Changed:** 2026-07-10


