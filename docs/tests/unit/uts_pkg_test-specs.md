# Unit Test Specifications - Package Command

**Category:** Package Command
**Prefix:** UTS_PKG
**Test Type:** Unit
**Last Validated:** 2026-07-09

---

## UTS_PKG_00001: Create single package with inline JSON

**ID:** UTS_PKG_00001
**Traces-To:** SWR_PKG_0001
**Title:** Create single package with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single package can be created with inline JSON containing name and description.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent package exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call PackageCreateAction with inline JSON
2. Verify package created via addNestedPackage
3. Verify description set via setDescription
**Expected Result:**
Package created successfully with correct name and description.
**Verification Criteria:**
- addNestedPackage called once with correct name
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-09

---

## UTS_PKG_00002: Create multiple packages from JSON file

**ID:** UTS_PKG_00002
**Traces-To:** SWR_PKG_0001, SWR_PKG_0006
**Title:** Create multiple packages from JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of packages from external JSON file with array of package definitions.
**Pre-conditions:**
- JSON file exists with valid array of package definitions
- Parent package exists
**Test Steps:**
1. Call PackageCreateAction with --input pointing to JSON file
2. Verify file read with UTF-8 encoding
3. Verify all packages created
**Expected Result:**
All packages created, logs show count.
**Verification Criteria:**
- File opened with UTF-8 encoding
- addNestedPackage called for each package
- Logger shows total count
**Last Changed:** 2026-07-09

---

## UTS_PKG_00003: Create with stereotypes

**ID:** UTS_PKG_00003
**Traces-To:** SWR_PKG_0007
**Title:** Create package with stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that stereotypes are applied to package during creation.
**Pre-conditions:**
- JSON contains stereotypes array
**Test Steps:**
1. Call PackageCreateAction with JSON containing stereotypes
2. Verify addStereotype called for each stereotype
**Expected Result:**
All stereotypes applied correctly.
**Verification Criteria:**
- addStereotype called once per stereotype
- Correct stereotype name and "Package" type passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00004: Create with tags

**ID:** UTS_PKG_00004
**Traces-To:** SWR_PKG_0007
**Title:** Create package with tags
**Type:** Unit
**Priority:** Medium
**Description:**
Test that tags are set on package during creation.
**Pre-conditions:**
- JSON contains tags object
**Test Steps:**
1. Call PackageCreateAction with JSON containing tags
2. Verify setPropertyValue called for each tag
**Expected Result:**
All tags set correctly.
**Verification Criteria:**
- setPropertyValue called once per tag
- Correct key-value pairs passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00005: Create with properties

**ID:** UTS_PKG_00005
**Traces-To:** SWR_PKG_0001
**Title:** Create package with custom properties
**Type:** Unit
**Priority:** Medium
**Description:**
Test that custom properties are set on package during creation.
**Pre-conditions:**
- JSON contains properties object
**Test Steps:**
1. Call PackageCreateAction with JSON containing properties
2. Verify setPropertyValue called for each property
**Expected Result:**
All properties set correctly.
**Verification Criteria:**
- setPropertyValue called once per property
- Correct key-value pairs passed
**Last Changed:** 2026-07-09

---

## UTS_PKG_00006: Create skips unknown attributes

**ID:** UTS_PKG_00006
**Traces-To:** SWR_PKG_0001
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes in JSON are skipped and logged as warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call PackageCreateAction with JSON containing unknown fields
2. Verify package still created
3. Verify warning logged
**Expected Result:**
Package created, unknown fields skipped with warning.
**Verification Criteria:**
- Package created successfully
- Logger.warning called with unknown field names
**Last Changed:** 2026-07-09

---

## UTS_PKG_00007: Create fails without name

**ID:** UTS_PKG_00007
**Traces-To:** SWR_PKG_0001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name field is missing from JSON.
**Pre-conditions:**
- JSON does not contain name field
**Test Steps:**
1. Call PackageCreateAction with JSON without name
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with appropriate message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "'name' is required"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00008: Create from external file

**ID:** UTS_PKG_00008
**Traces-To:** SWR_PKG_0006
**Title:** Create packages from external JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test that packages can be created from external JSON file.
**Pre-conditions:**
- Valid JSON file exists
**Test Steps:**
1. Call PackageCreateAction with --input parameter
2. Verify file read with UTF-8
3. Verify packages created
**Expected Result:**
File read and packages created.
**Verification Criteria:**
- File opened with UTF-8 encoding
- Packages created from file content
**Last Changed:** 2026-07-09

---

## UTS_PKG_00009: Create fails for invalid JSON

**ID:** UTS_PKG_00009
**Traces-To:** SWR_PKG_0006
**Title:** Create fails for malformed JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails gracefully for malformed JSON.
**Pre-conditions:**
- Malformed JSON string provided
**Test Steps:**
1. Call PackageCreateAction with malformed JSON
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with JSON parse error.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Invalid JSON"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00010: Create fails for missing file

**ID:** UTS_PKG_00010
**Traces-To:** SWR_PKG_0006
**Title:** Create fails for non-existent file
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails for non-existent file path.
**Pre-conditions:**
- File does not exist
**Test Steps:**
1. Call PackageCreateAction with non-existent file path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with file not found message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "File not found"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00011: Delete package successfully

**ID:** UTS_PKG_00011
**Traces-To:** SWR_PKG_0002
**Title:** Delete package successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that package is deleted successfully.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageDeleteAction with valid path
2. Verify deleteFromProject called
3. Verify log message shown
**Expected Result:**
Package deleted with log message.
**Verification Criteria:**
- deleteFromProject called once
- Logger shows INFO message
**Last Changed:** 2026-07-09

---

## UTS_PKG_00012: Delete handles COM error

**ID:** UTS_PKG_00012
**Traces-To:** SWR_PKG_0010
**Title:** Delete handles COM error gracefully
**Type:** Unit
**Priority:** High
**Description:**
Test that COM errors during deletion are handled properly.
**Pre-conditions:**
- deleteFromProject raises exception
**Test Steps:**
1. Call PackageDeleteAction
2. Simulate COM error in deleteFromProject
3. Verify error handled
**Expected Result:**
Exception handled, error logged.
**Verification Criteria:**
- Exception caught
- _handle_execution_error called
- Error logged
**Last Changed:** 2026-07-09

---

## UTS_PKG_00013: View table output

**ID:** UTS_PKG_00013
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in table format
**Type:** Unit
**Priority:** High
**Description:**
Test that package details are displayed in table format.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageViewAction with format=table
2. Verify table output contains all properties
**Expected Result:**
Table printed to stdout with all package properties.
**Verification Criteria:**
- Table contains Name, GUID, Description, etc.
- OutputFormatter.table called
**Last Changed:** 2026-07-09

---

## UTS_PKG_00014: View JSON output to file

**ID:** UTS_PKG_00014
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in JSON format to file
**Type:** Unit
**Priority:** High
**Description:**
Test that package details are written to JSON file.
**Pre-conditions:**
- Package exists at specified path
- Output file path provided
**Test Steps:**
1. Call PackageViewAction with format=json and --output
2. Verify JSON file created
3. Verify JSON contains all fields
**Expected Result:**
JSON file created with all package details.
**Verification Criteria:**
- File created at specified path
- JSON parseable and contains all fields
**Last Changed:** 2026-07-09

---

## UTS_PKG_00015: View CSV output

**ID:** UTS_PKG_00015
**Traces-To:** SWR_PKG_0003, SWR_PKG_0008
**Title:** View package in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test that package details are displayed in CSV format with horizontal layout.
**Pre-conditions:**
- Package exists at specified path
**Test Steps:**
1. Call PackageViewAction with format=csv
2. Verify CSV output has header + data row
**Expected Result:**
CSV printed with horizontal layout.
**Verification Criteria:**
- Output has exactly 2 lines
- Header row present
- Data row present
**Last Changed:** 2026-07-09

---

## UTS_PKG_00016: List nested packages

**ID:** UTS_PKG_00016
**Traces-To:** SWR_PKG_0004
**Title:** List nested packages
**Type:** Unit
**Priority:** High
**Description:**
Test that nested packages are listed correctly.
**Pre-conditions:**
- Package has nested packages
**Test Steps:**
1. Call PackageListAction with parent package path
2. Verify all nested packages shown
**Expected Result:**
List of nested package names.
**Verification Criteria:**
- getNestedPackages called
- All nested package names shown
**Last Changed:** 2026-07-09

---

## UTS_PKG_00017: List empty package

**ID:** UTS_PKG_00017
**Traces-To:** SWR_PKG_0004
**Title:** List empty package returns empty output
**Type:** Unit
**Priority:** Medium
**Description:**
Test that empty output is shown for package with no nested packages.
**Pre-conditions:**
- Package has no nested packages
**Test Steps:**
1. Call PackageListAction
2. Verify empty output
**Expected Result:**
Empty table/list shown.
**Verification Criteria:**
- getNestedPackages returns empty
- Output is empty or shows "no data"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00018: List JSON output

**ID:** UTS_PKG_00018
**Traces-To:** SWR_PKG_0004, SWR_PKG_0008
**Title:** List nested packages in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test that nested packages are listed in JSON array format.
**Pre-conditions:**
- Package has nested packages
**Test Steps:**
1. Call PackageListAction with format=json
2. Verify JSON array output
**Expected Result:**
JSON array of package names.
**Verification Criteria:**
- Output is valid JSON array
- Array contains all package names
**Last Changed:** 2026-07-09

---

## UTS_PKG_00019: Path validation - not found

**ID:** UTS_PKG_00019
**Traces-To:** SWR_PKG_0005
**Title:** Path validation fails for non-existent path
**Type:** Unit
**Priority:** High
**Description:**
Test that path validation raises error for non-existent path.
**Pre-conditions:**
- Path does not exist in model
**Test Steps:**
1. Call any package action with non-existent path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with path not found message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "not found"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00020: Path validation - not package

**ID:** UTS_PKG_00020
**Traces-To:** SWR_PKG_0005
**Title:** Path validation fails for non-package element
**Type:** Unit
**Priority:** High
**Description:**
Test that path validation raises error when path resolves to non-package element.
**Pre-conditions:**
- Path resolves to Class or other non-package element
**Test Steps:**
1. Call any package action with path to Class
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "does not resolve to a Package" message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "does not resolve to a Package"
- Error message shows actual element type
**Last Changed:** 2026-07-09

---

## UTS_PKG_00021: View-to-create workflow

**ID:** UTS_PKG_00021
**Traces-To:** SWR_PKG_0009
**Title:** View output can be reused as create input
**Type:** Unit
**Priority:** High
**Description:**
Test that package view JSON output can be used as package create input.
**Pre-conditions:**
- Package view JSON output available
**Test Steps:**
1. Export package via view --format json
2. Use JSON as create input
3. Verify new package created
**Expected Result:**
New package created with same attributes.
**Verification Criteria:**
- Unknown fields (guid, metaClass) ignored
- Only validated attributes used
- Package created successfully
**Last Changed:** 2026-07-09

---

## UTS_PKG_00022: Bulk creation with errors

**ID:** UTS_PKG_00022
**Traces-To:** SWR_PKG_0001
**Title:** Bulk creation handles partial failures
**Type:** Unit
**Priority:** Medium
**Description:**
Test that bulk creation continues on errors and reports results.
**Pre-conditions:**
- JSON array contains some invalid package definitions
**Test Steps:**
1. Call PackageCreateAction with mixed valid/invalid packages
2. Verify valid packages created
3. Verify errors logged
**Expected Result:**
Valid packages created, errors logged, summary shown.
**Verification Criteria:**
- Valid packages created
- Invalid packages logged as errors
- Summary shows count
**Last Changed:** 2026-07-09

---

## UTS_PKG_00023: File output handling

**ID:** UTS_PKG_00023
**Traces-To:** SWR_PKG_0003, SWR_PKG_0004
**Title:** Output written to file when --output specified
**Type:** Unit
**Priority:** High
**Description:**
Test that output is written to file instead of stdout when --output specified.
**Pre-conditions:**
- --output parameter provided
**Test Steps:**
1. Call view/list action with --output
2. Verify file created
3. Verify content matches expected format
**Expected Result:**
Content written to file, not stdout.
**Verification Criteria:**
- File exists at specified path
- File content matches expected output
- Nothing printed to stdout
**Last Changed:** 2026-07-09

---

## UTS_PKG_00024: File output error handling

**ID:** UTS_PKG_00024
**Traces-To:** SWR_PKG_0010
**Title:** File output handles permission errors
**Type:** Unit
**Priority:** High
**Description:**
Test that file output errors are handled gracefully.
**Pre-conditions:**
- Invalid file path (no write permission)
**Test Steps:**
1. Call view/list action with invalid --output path
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with file write error.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Failed to write"
**Last Changed:** 2026-07-09

---

## UTS_PKG_00025: Register all subcommands

**ID:** UTS_PKG_00025
**Traces-To:** SWR_PKG_0001-00004
**Title:** PackageCommand registers all subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test that PackageCommand registers all 4 subcommands.
**Pre-conditions:**
- PackageCommand initialized
**Test Steps:**
1. Create PackageCommand
2. Call get_actions
3. Verify 4 subcommands registered
**Expected Result:**
All 4 subcommands (create, delete, view, list) registered.
**Verification Criteria:**
- 4 actions returned
- All subcommand names present
**Last Changed:** 2026-07-09
