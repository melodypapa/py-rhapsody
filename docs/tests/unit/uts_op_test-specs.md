# Unit Test Specifications - Operation Command

**Category:** Operation Command
**Prefix:** UTS_OP
**Test Type:** Unit
**Last Validated:** 2026-07-10

---

## UTS_OP_00001: Create single operation with inline JSON

**ID:** UTS_OP_00001
**Traces-To:** SWR_OP_00001
**Title:** Create single operation with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single operation can be created with inline JSON containing name and body.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent classifier exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call OperationCreateAction with inline JSON
2. Verify operation created via addOperation
3. Verify body set via setBody
**Expected Result:**
Operation created successfully with correct name and body.
**Verification Criteria:**
- addOperation called once with correct name
- setBody called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_OP_00002: Create multiple operations from JSON array

**ID:** UTS_OP_00002
**Traces-To:** SWR_OP_00001, SWR_OP_00013
**Title:** Create multiple operations from JSON array
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of operations from JSON array.
**Pre-conditions:**
- JSON array with multiple operation definitions
- Parent classifier exists
**Test Steps:**
1. Call OperationCreateAction with JSON array
2. Verify addOperation called for each
**Expected Result:**
All operations created.
**Verification Criteria:**
- addOperation called correct number of times
- Logger shows count
**Last Changed:** 2026-07-10

---

## UTS_OP_00003: Create with boolean flags

**ID:** UTS_OP_00003
**Traces-To:** SWR_OP_00012
**Title:** Create operation with isAbstract, isStatic, isVirtual flags
**Type:** Unit
**Priority:** Medium
**Description:**
Test that boolean flags are applied during creation.
**Pre-conditions:**
- JSON contains isAbstract, isStatic, isVirtual
**Test Steps:**
1. Call OperationCreateAction with boolean flags
2. Verify setIsAbstract, setIsStatic, setIsVirtual called
**Expected Result:**
All flags applied correctly.
**Verification Criteria:**
- setIsAbstract(1) called for true
- setIsStatic(0) called for false
- setIsVirtual(1) called for true
**Last Changed:** 2026-07-10

---

## UTS_OP_00004: Create with returns type

**ID:** UTS_OP_00004
**Traces-To:** SWR_OP_00011
**Title:** Create operation with returns type
**Type:** Unit
**Priority:** Medium
**Description:**
Test that returns type is resolved and set.
**Pre-conditions:**
- JSON contains returns field
- Type exists in model
**Test Steps:**
1. Call OperationCreateAction with returns field
2. Verify findNestedClassifierRecursive called
3. Verify setReturns called
**Expected Result:**
Returns type resolved and set.
**Verification Criteria:**
- findNestedClassifierRecursive called with type name
- setReturns called with resolved type
**Last Changed:** 2026-07-10

---

## UTS_OP_00005: Create skips unknown attributes

**ID:** UTS_OP_00005
**Traces-To:** SWR_OP_00001
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes are skipped and logged.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call OperationCreateAction with unknown fields
2. Verify warning logged
**Expected Result:**
Unknown fields skipped.
**Verification Criteria:**
- Logger.warning called
- Operation still created
**Last Changed:** 2026-07-10

---

## UTS_OP_00006: Create fails without name

**ID:** UTS_OP_00006
**Traces-To:** SWR_OP_00001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name is missing.
**Pre-conditions:**
- JSON does not contain name
**Test Steps:**
1. Call OperationCreateAction without name
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "name" is required
**Last Changed:** 2026-07-10

---

## UTS_OP_00007: Create from external file

**ID:** UTS_OP_00007
**Traces-To:** SWR_OP_00007
**Title:** Create operations from external JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test creating operations from file.
**Pre-conditions:**
- Valid JSON file exists
**Test Steps:**
1. Call OperationCreateAction with --input
2. Verify file read
3. Verify operations created
**Expected Result:**
File read and operations created.
**Verification Criteria:**
- File opened with UTF-8
- addOperation called
**Last Changed:** 2026-07-10

---

## UTS_OP_00008: Delete operation by path and name

**ID:** UTS_OP_00008
**Traces-To:** SWR_OP_00002
**Title:** Delete operation by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test deleting operation via --path and --name.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationDeleteAction with --path and --name
2. Verify deleteOperation called
**Expected Result:**
Operation deleted.
**Verification Criteria:**
- findInterfaceItem called
- deleteOperation called
**Last Changed:** 2026-07-10

---

## UTS_OP_00009: Delete operation by GUID

**ID:** UTS_OP_00009
**Traces-To:** SWR_OP_00002, SWR_OP_00010
**Title:** Delete operation by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test deleting operation via --guid.
**Pre-conditions:**
- Operation GUID exists
**Test Steps:**
1. Call OperationDeleteAction with --guid
2. Verify findElementByGUID called
3. Verify deleteOperation called
**Expected Result:**
Operation deleted.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated
- deleteOperation called
**Last Changed:** 2026-07-10

---

## UTS_OP_00010: Delete GUID wrong type raises error

**ID:** UTS_OP_00010
**Traces-To:** SWR_OP_00002, SWR_OP_00010
**Title:** Delete GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong type via GUID raises error.
**Pre-conditions:**
- GUID resolves to non-operation
**Test Steps:**
1. Call OperationDeleteAction with --guid for Class
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to an Operation"
**Last Changed:** 2026-07-10

---

## UTS_OP_00011: View operation table output

**ID:** UTS_OP_00011
**Traces-To:** SWR_OP_00003, SWR_OP_00008
**Title:** View operation in table format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing operation in table format.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationViewAction with format=table
2. Verify table output
**Expected Result:**
Table with all properties.
**Verification Criteria:**
- Table contains Name, GUID, Body, etc.
- OutputFormatter.table called
**Last Changed:** 2026-07-10

---

## UTS_OP_00012: View operation JSON output

**ID:** UTS_OP_00012
**Traces-To:** SWR_OP_00003, SWR_OP_00008
**Title:** View operation in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing operation in JSON format.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationViewAction with format=json
2. Verify JSON output
**Expected Result:**
JSON with 12 keys.
**Verification Criteria:**
- Output is valid JSON
- Contains all 12 fields
**Last Changed:** 2026-07-10

---

## UTS_OP_00013: View operation CSV output

**ID:** UTS_OP_00013
**Traces-To:** SWR_OP_00003, SWR_OP_00008
**Title:** View operation in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test viewing operation in CSV format.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationViewAction with format=csv
2. Verify CSV output
**Expected Result:**
CSV with horizontal layout.
**Verification Criteria:**
- Output has header + data row
- 12 columns
**Last Changed:** 2026-07-10

---

## UTS_OP_00014: List operations on classifier

**ID:** UTS_OP_00014
**Traces-To:** SWR_OP_00004
**Title:** List operations on classifier
**Type:** Unit
**Priority:** High
**Description:**
Test listing operations.
**Pre-conditions:**
- Classifier has operations
**Test Steps:**
1. Call OperationListAction with --path
2. Verify operations listed
**Expected Result:**
List of operation names.
**Verification Criteria:**
- getOperations called
- All names shown
**Last Changed:** 2026-07-10

---

## UTS_OP_00015: List empty classifier

**ID:** UTS_OP_00015
**Traces-To:** SWR_OP_00004
**Title:** List operations on empty classifier
**Type:** Unit
**Priority:** Medium
**Description:**
Test listing when no operations.
**Pre-conditions:**
- Classifier has no operations
**Test Steps:**
1. Call OperationListAction
2. Verify empty output
**Expected Result:**
Empty output.
**Verification Criteria:**
- getOperations returns empty
- Output is empty
**Last Changed:** 2026-07-10

---

## UTS_OP_00016: List JSON output

**ID:** UTS_OP_00016
**Traces-To:** SWR_OP_00004, SWR_OP_00008
**Title:** List operations in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test listing in JSON format.
**Pre-conditions:**
- Classifier has operations
**Test Steps:**
1. Call OperationListAction with format=json
2. Verify JSON array
**Expected Result:**
JSON array of strings.
**Verification Criteria:**
- Output is valid JSON array
- Contains all names
**Last Changed:** 2026-07-10

---

## UTS_OP_00017: Update operation by path and name

**ID:** UTS_OP_00017
**Traces-To:** SWR_OP_00005
**Title:** Update operation by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test updating operation.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationUpdateAction with --path and --name
2. Verify attributes updated
**Expected Result:**
Operation updated.
**Verification Criteria:**
- setBody called
- Logger shows INFO
**Last Changed:** 2026-07-10

---

## UTS_OP_00018: Update operation by GUID

**ID:** UTS_OP_00018
**Traces-To:** SWR_OP_00005, SWR_OP_00010
**Title:** Update operation by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test updating operation via GUID.
**Pre-conditions:**
- Operation GUID exists
**Test Steps:**
1. Call OperationUpdateAction with --guid
2. Verify type validation
3. Verify attributes updated
**Expected Result:**
Operation updated.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated
- setBody called
**Last Changed:** 2026-07-10

---

## UTS_OP_00019: Update partial update

**ID:** UTS_OP_00019
**Traces-To:** SWR_OP_00005
**Title:** Update partial - only specified fields
**Type:** Unit
**Priority:** High
**Description:**
Test partial update.
**Pre-conditions:**
- Operation exists
**Test Steps:**
1. Call OperationUpdateAction with only body field
2. Verify only setBody called
**Expected Result:**
Only body updated.
**Verification Criteria:**
- setBody called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_OP_00020: Update skips unknown fields

**ID:** UTS_OP_00020
**Traces-To:** SWR_OP_00005
**Title:** Update skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test unknown fields skipped.
**Pre-conditions:**
- JSON has unknown fields
**Test Steps:**
1. Call OperationUpdateAction with unknown field
2. Verify warning logged
**Expected Result:**
Unknown skipped.
**Verification Criteria:**
- Logger.warning called
**Last Changed:** 2026-07-10

---

## UTS_OP_00021: Path validation - operation not found

**ID:** UTS_OP_00021
**Traces-To:** SWR_OP_00006
**Title:** Operation name not found raises error
**Type:** Unit
**Priority:** High
**Description:**
Test error when operation not found.
**Pre-conditions:**
- Operation name doesn't exist
**Test Steps:**
1. Call action with non-existent name
2. Verify CliExecutionError
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "not found"
**Last Changed:** 2026-07-10

---

## UTS_OP_00022: GUID not found raises error

**ID:** UTS_OP_00022
**Traces-To:** SWR_OP_00010
**Title:** GUID not found raises error
**Type:** Unit
**Priority:** High
**Description:**
Test error when GUID not found.
**Pre-conditions:**
- GUID doesn't exist
**Test Steps:**
1. Call action with non-existent GUID
2. Verify CliExecutionError
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "not found"
**Last Changed:** 2026-07-10

---

## UTS_OP_00023: OperationCommand registers all subcommands

**ID:** UTS_OP_00023
**Traces-To:** SWR_OP_00001, SWR_OP_00002, SWR_OP_00003, SWR_OP_00004, SWR_OP_00005
**Title:** OperationCommand registers 5 subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test command dispatcher.
**Pre-conditions:**
- None
**Test Steps:**
1. Create OperationCommand
2. Check get_actions()
**Expected Result:**
5 actions registered.
**Verification Criteria:**
- create, delete, view, list, update in command_ids
- len(actions) == 5
**Last Changed:** 2026-07-10

---

## UTS_OP_00024: Missing subcommand raises error

**ID:** UTS_OP_00024
**Traces-To:** SWR_OP_00009
**Title:** Missing subcommand raises error
**Type:** Unit
**Priority:** High
**Description:**
Test missing subcommand.
**Pre-conditions:**
- None
**Test Steps:**
1. Create OperationCommand with empty args
2. Verify error
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
**Last Changed:** 2026-07-10

---

## UTS_OP_00025: Create with visibility and arguments

**ID:** UTS_OP_00025
**Traces-To:** SWR_OP_00001
**Title:** Create with visibility and arguments
**Type:** Unit
**Priority:** Medium
**Description:**
Test setting visibility and arguments.
**Pre-conditions:**
- JSON has visibility and arguments
**Test Steps:**
1. Call OperationCreateAction
2. Verify setVisibility and setArguments called
**Expected Result:**
Fields set correctly.
**Verification Criteria:**
- setVisibility called
- setArguments called
**Last Changed:** 2026-07-10
