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

---

## UTS_PKG_00026: Create package at project root when path is None

**ID:** UTS_PKG_00026
**Traces-To:** SWR_PKG_0013
**Title:** Create package with no --path (None) creates at project root
**Type:** Unit
**Priority:** High
**Description:**
Test that when PackageCreateAction.execute() is called with args.path=None, the package is created at the project root using RPProject.addPackage(), not addNestedPackage().
**Pre-conditions:**
- Rhapsody application is mocked
- args.path = None
- args.input = None
- args.attributes = '{"name":"TopLevel"}'
**Test Steps:**
1. Mock _get_active_root() to return a mock root with addPackage() method
2. Call PackageCreateAction.execute(args)
3. Verify root.addPackage("TopLevel") was called exactly once
4. Verify root.addNestedPackage() was NOT called
**Expected Result:**
Package created at project root via addPackage.
**Verification Criteria:**
- root.addPackage called once with correct name
- root.addNestedPackage not called
- Logger shows INFO message with path "TopLevel" (no leading None/)
**Last Changed:** 2026-07-10

---

## UTS_PKG_00027: Create package at project root when path is empty string

**ID:** UTS_PKG_00027
**Traces-To:** SWR_PKG_0013
**Title:** Create package with empty string --path creates at project root
**Type:** Unit
**Priority:** High
**Description:**
Test that when PackageCreateAction.execute() is called with args.path="" (empty string), the package is created at the project root using RPProject.addPackage(), behaving identically to args.path=None.
**Pre-conditions:**
- Rhapsody application is mocked
- args.path = ""
- args.input = None
- args.attributes = '{"name":"TopLevel"}'
**Test Steps:**
1. Mock _get_active_root() to return a mock root with addPackage() method
2. Call PackageCreateAction.execute(args) with args.path=""
3. Verify root.addPackage("TopLevel") was called exactly once
4. Verify root.addNestedPackage() was NOT called
**Expected Result:**
Package created at project root via addPackage (same as None case).
**Verification Criteria:**
- root.addPackage called once with correct name
- root.addNestedPackage not called
- Logger shows INFO message with path "TopLevel" (no leading empty-segment artifact)
**Last Changed:** 2026-07-10

---

## UTS_PKG_00028: Package create logs execution steps

**ID:** UTS_PKG_00028
**Traces-To:** SWR_PKG_0014
**Title:** PackageCreateAction logs execution steps at INFO level
**Type:** Unit
**Priority:** Medium
**Description:**
Test that PackageCreateAction.execute() logs INFO-level messages showing operation progress at each stage.
**Pre-conditions:**
- Logger is captured/mocked in test
- Creating 1 package with --path specified
**Test Steps:**
1. Create PackageCreateAction
2. Mock logger to capture log calls
3. Call execute() with args.path="Sensors" and package attributes
4. Verify log messages in order: "Starting package creation...", "Resolving parent path 'Sensors'...", "Creating package 'X'...", "Created package: Sensors/X", "Successfully created 1 package"
**Expected Result:**
All execution-step messages logged at INFO level in correct sequence.
**Verification Criteria:**
- logger.info() called 5 times with expected messages
- Messages appear in expected order
- No ERROR-level logs for successful operation
**Last Changed:** 2026-07-10

---

## UTS_PKG_00029: Package delete logs execution steps

**ID:** UTS_PKG_00029
**Traces-To:** SWR_PKG_0014
**Title:** PackageDeleteAction logs execution steps at INFO level
**Type:** Unit
**Priority:** Medium
**Description:**
Test that PackageDeleteAction.execute() logs INFO-level messages at each stage: operation start, path resolution, deletion, and success.
**Pre-conditions:**
- Logger is captured/mocked in test
- args.path = "Sensors/OldPackage"
**Test Steps:**
1. Create PackageDeleteAction
2. Mock logger to capture log calls
3. Call execute(args)
4. Verify log messages: "Starting package deletion...", "Resolving package path 'Sensors/OldPackage'...", "Deleting package 'Sensors/OldPackage'...", "Successfully deleted package 'Sensors/OldPackage'"
**Expected Result:**
All execution-step messages logged at INFO level in correct sequence.
**Verification Criteria:**
- logger.info() called 4 times with expected messages
- Messages appear in expected order
**Last Changed:** 2026-07-10

---

## UTS_PKG_00030: Package view logs execution steps

**ID:** UTS_PKG_00030
**Traces-To:** SWR_PKG_0014
**Title:** PackageViewAction logs execution steps at INFO level
**Type:** Unit
**Priority:** Medium
**Description:**
Test that PackageViewAction.execute() logs INFO-level messages for operation start, path resolution, and details retrieval.
**Pre-conditions:**
- Logger is captured/mocked in test
- args.path = "Sensors"
- args.format = "table"
**Test Steps:**
1. Create PackageViewAction
2. Mock logger to capture log calls
3. Call execute(args) with no --output (stdout only)
4. Verify log messages: "Starting package view operation...", "Resolving package path 'Sensors'...", "Retrieving package details..."
**Expected Result:**
Execution-step messages logged at INFO level; no "Writing output to file" message (since no --output).
**Verification Criteria:**
- logger.info() called 3 times with expected messages
- No "Writing output to file" message when args.output is None
**Last Changed:** 2026-07-10

---

## UTS_PKG_00031: Package list logs execution steps and count

**ID:** UTS_PKG_00031
**Traces-To:** SWR_PKG_0014
**Title:** PackageListAction logs execution steps and nested package count
**Type:** Unit
**Priority:** Medium
**Description:**
Test that PackageListAction.execute() logs INFO-level messages for operation start, path resolution, listing, and nested package count.
**Pre-conditions:**
- Logger is captured/mocked in test
- Mock package returns 3 nested packages
- args.path = "Sensors"
**Test Steps:**
1. Create PackageListAction
2. Mock logger to capture log calls
3. Mock getNestedPackages() to return 3 packages
4. Call execute(args)
5. Verify log messages: "Starting package list operation...", "Resolving package path 'Sensors'...", "Listing nested packages...", "Found 3 nested packages"
**Expected Result:**
Execution-step messages logged with correct package count.
**Verification Criteria:**
- logger.info() called 4 times with expected messages
- Count message shows "3 nested packages" (plural form correct)
**Last Changed:** 2026-07-10

---

## UTS_PKG_00032: Duplicate package detection at project root

**ID:** UTS_PKG_00032
**Traces-To:** SWR_PKG_0015
**Title:** Duplicate package name rejected at project root
**Type:** Unit
**Priority:** High
**Description:**
Test that when PackageCreateAction attempts to create a package at the project root with a name that already exists, it detects the duplicate and raises a user-friendly error instead of allowing COM exception.
**Pre-conditions:**
- Mock root container with `getPackages()` returning existing package named "TopLevel"
- args.path = None (creating at root)
- args.attributes = '{"name":"TopLevel"}'
**Test Steps:**
1. Mock `_get_active_root()` to return mock root
2. Mock root.getPackages() to return collection with package named "TopLevel"
3. Call execute(args)
4. Expect CliExecutionError to be raised
**Expected Result:**
CliExecutionError raised with message: `"Package 'TopLevel' already exists in project root"`
**Verification Criteria:**
- Error message contains "already exists"
- Error message contains "project root"
- addPackage() was NOT called (duplicate detected before creation attempt)
**Last Changed:** 2026-07-10

---

## UTS_PKG_00033: Duplicate package detection in nested package

**ID:** UTS_PKG_00033
**Traces-To:** SWR_PKG_0015
**Title:** Duplicate package name rejected in parent package
**Type:** Unit
**Priority:** High
**Description:**
Test that when PackageCreateAction attempts to create a nested package with a name that already exists in the parent, it detects the duplicate and raises a user-friendly error.
**Pre-conditions:**
- Mock parent package "Sensors"
- Mock parent.getNestedPackages() returning existing package named "Temp"
- args.path = "Sensors"
- args.attributes = '{"name":"Temp"}'
**Test Steps:**
1. Mock `_resolve_and_validate_package()` to return mock parent
2. Mock parent.getNestedPackages() to return collection with package named "Temp"
3. Call execute(args)
4. Expect CliExecutionError to be raised
**Expected Result:**
CliExecutionError raised with message: `"Package 'Temp' already exists in package 'Sensors'"`
**Verification Criteria:**
- Error message contains "already exists"
- Error message contains parent package name "Sensors"
- addNestedPackage() was NOT called
**Last Changed:** 2026-07-10

---

## UTS_PKG_00034: Non-duplicate creation still works

**ID:** UTS_PKG_00034
**Traces-To:** SWR_PKG_0015
**Title:** Package creation succeeds when name is not a duplicate
**Type:** Unit
**Priority:** High
**Description:**
Test that package creation proceeds normally when the duplicate check passes (package name does not exist in container).
**Pre-conditions:**
- Mock parent returns empty package collection (no duplicates)
- args.path = "Sensors"
- args.attributes = '{"name":"Humidity"}'
**Test Steps:**
1. Mock parent.getNestedPackages() to return empty collection
2. Call execute(args)
3. Verify addNestedPackage("Humidity") was called
**Expected Result:**
Package created successfully; no error raised.
**Verification Criteria:**
- addNestedPackage() was called with correct name
- No CliExecutionError raised
- Success logs present
**Last Changed:** 2026-07-10

---

## UTS_PKG_00035: Update package via path

**ID:** UTS_PKG_00035
**Traces-To:** SWR_PKG_0016
**Title:** Update package via path
**Type:** Unit
**Priority:** High
**Description:**
Test that package can be updated via --path argument.
**Pre-conditions:**
- Package exists at specified path
- Valid JSON provided
**Test Steps:**
1. Call PackageUpdateAction with --path
2. Verify attributes updated
**Expected Result:**
Package updated successfully.
**Verification Criteria:**
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_PKG_00036: Update package via GUID with type validation

**ID:** UTS_PKG_00036
**Traces-To:** SWR_PKG_0016
**Title:** Update package via GUID with type validation
**Type:** Unit
**Priority:** High
**Description:**
Test that package can be updated via --guid with type validation.
**Pre-conditions:**
- Package exists with given GUID
**Test Steps:**
1. Call PackageUpdateAction with --guid
2. Verify metaClass validation
3. Verify attributes updated
**Expected Result:**
Package updated, type validated.
**Verification Criteria:**
- findElementByGUID called
- metaClass checked equals "Package"
- setName called with correct value
**Last Changed:** 2026-07-10

---

## UTS_PKG_00037: Update package GUID wrong type raises error

**ID:** UTS_PKG_00037
**Traces-To:** SWR_PKG_0016
**Title:** Update package GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong element type via --guid raises CliExecutionError.
**Pre-conditions:**
- GUID resolves to non-package element (Class)
**Test Steps:**
1. Call PackageUpdateAction with --guid for Class
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError with type mismatch message.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to a Package"
- Error contains "found Class"
**Last Changed:** 2026-07-10

---

## UTS_PKG_00038: Update package partial update

**ID:** UTS_PKG_00038
**Traces-To:** SWR_PKG_0016
**Title:** Update package partial update
**Type:** Unit
**Priority:** High
**Description:**
Test that partial update only modifies specified fields.
**Pre-conditions:**
- Package exists
**Test Steps:**
1. Call PackageUpdateAction with only tags field
2. Verify only setPropertyValue called
3. Verify other setters not called
**Expected Result:**
Only specified field updated.
**Verification Criteria:**
- setPropertyValue called for tags
- setDescription not called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_PKG_00039: Update package skips unknown fields

**ID:** UTS_PKG_00039
**Traces-To:** SWR_PKG_0016
**Title:** Update package skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown fields are skipped with warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call PackageUpdateAction with unknown field
2. Verify warning logged
3. Verify known field still applied
**Expected Result:**
Unknown fields skipped, known fields applied.
**Verification Criteria:**
- Logger.warning called with unknown field name
- Known attribute still applied
**Last Changed:** 2026-07-10

