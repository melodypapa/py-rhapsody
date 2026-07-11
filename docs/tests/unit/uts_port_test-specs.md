# Unit Test Specifications - Port Command

**Category:** Port Command
**Prefix:** UTS_PORT
**Test Type:** Unit
**Last Validated:** 2026-07-11

---

## UTS_PORT_00001: Create single port with inline JSON

**ID:** UTS_PORT_00001
**Traces-To:** SWR_PORT_00001
**Title:** Create single port with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single port can be created with inline JSON containing name.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent classifier exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call PortCreateAction with inline JSON
2. Verify port created via addPort
3. Verify name set via setName
**Expected Result:**
Port created successfully with correct name.
**Verification Criteria:**
- addPort called once with correct name
- Logger shows INFO message
**Last Changed:** 2026-07-11

---

## UTS_PORT_00002: Create multiple ports from JSON array

**ID:** UTS_PORT_00002
**Traces-To:** SWR_PORT_00001, SWR_PORT_00013
**Title:** Create multiple ports from JSON array
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of ports from JSON array.
**Pre-conditions:**
- JSON array with multiple port definitions
- Parent classifier exists
**Test Steps:**
1. Call PortCreateAction with JSON array
2. Verify addPort called for each
**Expected Result:**
All ports created.
**Verification Criteria:**
- addPort called correct number of times
- Logger shows count
**Last Changed:** 2026-07-11

---

## UTS_PORT_00003: Create with isBehavioral flag

**ID:** UTS_PORT_00003
**Traces-To:** SWR_PORT_00001, SWR_PORT_00012
**Title:** Create port with isBehavioral flag
**Type:** Unit
**Priority:** Medium
**Description:**
Test that isBehavioral flag is applied during creation.
**Pre-conditions:**
- JSON contains isBehavioral field
**Test Steps:**
1. Call PortCreateAction with isBehavioral=true
2. Verify setIsBehavioral called
**Expected Result:**
isBehavioral flag applied correctly.
**Verification Criteria:**
- setIsBehavioral(1) called for true
- setIsBehavioral(0) called for false
**Last Changed:** 2026-07-11

---

## UTS_PORT_00004: Create with isReversed flag

**ID:** UTS_PORT_00004
**Traces-To:** SWR_PORT_00001, SWR_PORT_00012
**Title:** Create port with isReversed flag
**Type:** Unit
**Priority:** Medium
**Description:**
Test that isReversed flag is applied during creation.
**Pre-conditions:**
- JSON contains isReversed field
**Test Steps:**
1. Call PortCreateAction with isReversed=true
2. Verify setIsReversed called
**Expected Result:**
isReversed flag applied correctly.
**Verification Criteria:**
- setIsReversed(1) called for true
- setIsReversed(0) called for false
**Last Changed:** 2026-07-11

---

## UTS_PORT_00005: Create with portContract resolution

**ID:** UTS_PORT_00005
**Traces-To:** SWR_PORT_00001, SWR_PORT_00011
**Title:** Create port with portContract resolution
**Type:** Unit
**Priority:** High
**Description:**
Test that portContract is resolved and set.
**Pre-conditions:**
- JSON contains portContract field
- Interface/Class exists in model
**Test Steps:**
1. Call PortCreateAction with portContract field
2. Verify findNestedClassifierRecursive called
3. Verify setPortContract called
**Expected Result:**
portContract resolved and set.
**Verification Criteria:**
- findNestedClassifierRecursive called with contract name
- setPortContract called with resolved interface
**Last Changed:** 2026-07-11

---

## UTS_PORT_00006: Create skips unknown attributes

**ID:** UTS_PORT_00006
**Traces-To:** SWR_PORT_00001
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes are skipped and logged.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call PortCreateAction with unknown fields
2. Verify warning logged
**Expected Result:**
Unknown fields skipped.
**Verification Criteria:**
- Logger.warning called
- Port still created
**Last Changed:** 2026-07-11

---

## UTS_PORT_00007: Create fails without name

**ID:** UTS_PORT_00007
**Traces-To:** SWR_PORT_00001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name is missing.
**Pre-conditions:**
- JSON does not contain name
**Test Steps:**
1. Call PortCreateAction without name
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "name" is required
**Last Changed:** 2026-07-11

---

## UTS_PORT_00008: Create from external file

**ID:** UTS_PORT_00008
**Traces-To:** SWR_PORT_00007
**Title:** Create ports from external JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test creating ports from file.
**Pre-conditions:**
- Valid JSON file exists
**Test Steps:**
1. Call PortCreateAction with --input
2. Verify file read
3. Verify ports created
**Expected Result:**
File read and ports created.
**Verification Criteria:**
- File opened with UTF-8
- addPort called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00009: Delete port by path and name

**ID:** UTS_PORT_00009
**Traces-To:** SWR_PORT_00002
**Title:** Delete port by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test deleting port via --path and --name.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortDeleteAction with --path and --name
2. Verify deleteFromProject called
**Expected Result:**
Port deleted.
**Verification Criteria:**
- getPorts called to find port
- deleteFromProject called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00010: Delete port by GUID

**ID:** UTS_PORT_00010
**Traces-To:** SWR_PORT_00002, SWR_PORT_00010
**Title:** Delete port by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test deleting port via --guid.
**Pre-conditions:**
- Port GUID exists
**Test Steps:**
1. Call PortDeleteAction with --guid
2. Verify findElementByGUID called
3. Verify deleteFromProject called
**Expected Result:**
Port deleted.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated as Port
- deleteFromProject called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00011: Delete GUID wrong type raises error

**ID:** UTS_PORT_00011
**Traces-To:** SWR_PORT_00002, SWR_PORT_00010
**Title:** Delete GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong type via GUID raises error.
**Pre-conditions:**
- GUID resolves to non-port
**Test Steps:**
1. Call PortDeleteAction with --guid for Class
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to a Port"
**Last Changed:** 2026-07-11

---

## UTS_PORT_00012: View port table output

**ID:** UTS_PORT_00012
**Traces-To:** SWR_PORT_00003, SWR_PORT_00008
**Title:** View port in table format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing port in table format.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortViewAction with format=table
2. Verify table output
**Expected Result:**
Table with all properties.
**Verification Criteria:**
- Table contains Name, GUID, Description, etc.
- OutputFormatter.table called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00013: View port JSON output

**ID:** UTS_PORT_00013
**Traces-To:** SWR_PORT_00003, SWR_PORT_00008
**Title:** View port in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing port in JSON format.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortViewAction with format=json
2. Verify JSON output
**Expected Result:**
JSON with 8 keys.
**Verification Criteria:**
- Output is valid JSON
- Contains all 8 fields: name, guid, description, isBehavioral, isReversed, portContract, metaClass, fullPath
**Last Changed:** 2026-07-11

---

## UTS_PORT_00014: View port CSV output

**ID:** UTS_PORT_00014
**Traces-To:** SWR_PORT_00003, SWR_PORT_00008
**Title:** View port in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test viewing port in CSV format.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortViewAction with format=csv
2. Verify CSV output
**Expected Result:**
CSV with horizontal layout.
**Verification Criteria:**
- Output has header + data row
- 8 columns
**Last Changed:** 2026-07-11

---

## UTS_PORT_00015: List ports on classifier

**ID:** UTS_PORT_00015
**Traces-To:** SWR_PORT_00004
**Title:** List ports on classifier
**Type:** Unit
**Priority:** High
**Description:**
Test listing ports.
**Pre-conditions:**
- Classifier has ports
**Test Steps:**
1. Call PortListAction with --path
2. Verify ports listed
**Expected Result:**
List of port names.
**Verification Criteria:**
- getPorts called
- All names shown
**Last Changed:** 2026-07-11

---

## UTS_PORT_00016: List empty classifier

**ID:** UTS_PORT_00016
**Traces-To:** SWR_PORT_00004
**Title:** List ports on empty classifier
**Type:** Unit
**Priority:** Medium
**Description:**
Test listing when no ports.
**Pre-conditions:**
- Classifier has no ports
**Test Steps:**
1. Call PortListAction
2. Verify empty output
**Expected Result:**
Empty output.
**Verification Criteria:**
- getPorts returns empty
- Output is empty
**Last Changed:** 2026-07-11

---

## UTS_PORT_00017: List JSON output

**ID:** UTS_PORT_00017
**Traces-To:** SWR_PORT_00004, SWR_PORT_00008
**Title:** List ports in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test listing in JSON format.
**Pre-conditions:**
- Classifier has ports
**Test Steps:**
1. Call PortListAction with format=json
2. Verify JSON array
**Expected Result:**
JSON array of strings.
**Verification Criteria:**
- Output is valid JSON array
- Contains all names
**Last Changed:** 2026-07-11

---

## UTS_PORT_00018: List CSV output

**ID:** UTS_PORT_00018
**Traces-To:** SWR_PORT_00004, SWR_PORT_00008
**Title:** List ports in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test listing in CSV format.
**Pre-conditions:**
- Classifier has ports
**Test Steps:**
1. Call PortListAction with format=csv
2. Verify CSV output
**Expected Result:**
CSV with Name column.
**Verification Criteria:**
- Output has header row
- Contains all port names
**Last Changed:** 2026-07-11

---

## UTS_PORT_00019: Update port by path and name

**ID:** UTS_PORT_00019
**Traces-To:** SWR_PORT_00005
**Title:** Update port by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test updating port.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortUpdateAction with --path and --name
2. Verify attributes updated
**Expected Result:**
Port updated.
**Verification Criteria:**
- setDescription called
- Logger shows INFO
**Last Changed:** 2026-07-11

---

## UTS_PORT_00020: Update port by GUID

**ID:** UTS_PORT_00020
**Traces-To:** SWR_PORT_00005, SWR_PORT_00010
**Title:** Update port by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test updating port via GUID.
**Pre-conditions:**
- Port GUID exists
**Test Steps:**
1. Call PortUpdateAction with --guid
2. Verify type validation
3. Verify attributes updated
**Expected Result:**
Port updated.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated
- setDescription called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00021: Update partial update

**ID:** UTS_PORT_00021
**Traces-To:** SWR_PORT_00005
**Title:** Update partial - only specified fields
**Type:** Unit
**Priority:** High
**Description:**
Test partial update.
**Pre-conditions:**
- Port exists
**Test Steps:**
1. Call PortUpdateAction with only description field
2. Verify only setDescription called
**Expected Result:**
Only description updated.
**Verification Criteria:**
- setDescription called
- setName not called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00022: Update skips unknown fields

**ID:** UTS_PORT_00022
**Traces-To:** SWR_PORT_00005
**Title:** Update skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test unknown fields skipped.
**Pre-conditions:**
- JSON has unknown fields
**Test Steps:**
1. Call PortUpdateAction with unknown field
2. Verify warning logged
**Expected Result:**
Unknown skipped.
**Verification Criteria:**
- Logger.warning called
**Last Changed:** 2026-07-11

---

## UTS_PORT_00023: Path validation - port not found

**ID:** UTS_PORT_00023
**Traces-To:** SWR_PORT_00006
**Title:** Port name not found raises error
**Type:** Unit
**Priority:** High
**Description:**
Test error when port not found.
**Pre-conditions:**
- Port name doesn't exist
**Test Steps:**
1. Call action with non-existent name
2. Verify CliExecutionError
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "not found"
**Last Changed:** 2026-07-11

---

## UTS_PORT_00024: GUID not found raises error

**ID:** UTS_PORT_00024
**Traces-To:** SWR_PORT_00010
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
**Last Changed:** 2026-07-11

---

## UTS_PORT_00025: PortCommand registers all subcommands

**ID:** UTS_PORT_00025
**Traces-To:** SWR_PORT_00001, SWR_PORT_00002, SWR_PORT_00003, SWR_PORT_00004, SWR_PORT_00005
**Title:** PortCommand registers 5 subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test command dispatcher.
**Pre-conditions:**
- None
**Test Steps:**
1. Create PortCommand
2. Check get_actions()
**Expected Result:**
5 actions registered.
**Verification Criteria:**
- create, delete, view, list, update in command_ids
- len(actions) == 5
**Last Changed:** 2026-07-11