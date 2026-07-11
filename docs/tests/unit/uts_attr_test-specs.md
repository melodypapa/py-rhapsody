# Unit Test Specifications - Attribute Command

**Category:** Attribute Command
**Prefix:** UTS_ATTR
**Test Type:** Unit
**Last Validated:** 2026-07-10

---

## UTS_ATTR_00001: Create single attribute with inline JSON

**ID:** UTS_ATTR_00001
**Traces-To:** SWR_ATTR_00001
**Title:** Create single attribute with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single attribute can be created with inline JSON containing name and type.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent classifier exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call AttributeCreateAction with inline JSON
2. Verify attribute created via addAttribute
3. Verify type set via setType
**Expected Result:**
Attribute created successfully with correct name and type.
**Verification Criteria:**
- addAttribute called once with correct name
- setType called with resolved type
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00002: Create multiple attributes from JSON array

**ID:** UTS_ATTR_00002
**Traces-To:** SWR_ATTR_00001, SWR_ATTR_00013
**Title:** Create multiple attributes from JSON array
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of attributes from JSON array.
**Pre-conditions:**
- JSON array with multiple attribute definitions
- Parent classifier exists
**Test Steps:**
1. Call AttributeCreateAction with JSON array
2. Verify addAttribute called for each
**Expected Result:**
All attributes created.
**Verification Criteria:**
- addAttribute called correct number of times
- Logger shows count
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00003: Create with type

**ID:** UTS_ATTR_00003
**Traces-To:** SWR_ATTR_00011
**Title:** Create attribute with type
**Type:** Unit
**Priority:** Medium
**Description:**
Test that type is resolved and set.
**Pre-conditions:**
- JSON contains type field
- Type exists in model
**Test Steps:**
1. Call AttributeCreateAction with type field
2. Verify findNestedClassifierRecursive called
3. Verify setType called
**Expected Result:**
Type resolved and set.
**Verification Criteria:**
- findNestedClassifierRecursive called with type name
- setType called with resolved type
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00004: Create with isStatic flag

**ID:** UTS_ATTR_00004
**Traces-To:** SWR_ATTR_00012
**Title:** Create attribute with isStatic flag
**Type:** Unit
**Priority:** Medium
**Description:**
Test that isStatic flag is applied during creation.
**Pre-conditions:**
- JSON contains isStatic
**Test Steps:**
1. Call AttributeCreateAction with isStatic field
2. Verify setIsStatic called
**Expected Result:**
Flag applied correctly.
**Verification Criteria:**
- setIsStatic(1) called for true
- setIsStatic(0) called for false
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00005: Create skips unknown attributes

**ID:** UTS_ATTR_00005
**Traces-To:** SWR_ATTR_00001
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes are skipped and logged.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call AttributeCreateAction with unknown fields
2. Verify warning logged
**Expected Result:**
Unknown fields skipped.
**Verification Criteria:**
- Logger.warning called
- Attribute still created
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00006: Create fails without name

**ID:** UTS_ATTR_00006
**Traces-To:** SWR_ATTR_00001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name is missing.
**Pre-conditions:**
- JSON does not contain name
**Test Steps:**
1. Call AttributeCreateAction without name
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "name" is required
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00007: Create from external file

**ID:** UTS_ATTR_00007
**Traces-To:** SWR_ATTR_00007
**Title:** Create attributes from external JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test creating attributes from file.
**Pre-conditions:**
- Valid JSON file exists
**Test Steps:**
1. Call AttributeCreateAction with --input
2. Verify file read
3. Verify attributes created
**Expected Result:**
File read and attributes created.
**Verification Criteria:**
- File opened with UTF-8
- addAttribute called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00008: Delete attribute by path and name

**ID:** UTS_ATTR_00008
**Traces-To:** SWR_ATTR_00002
**Title:** Delete attribute by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test deleting attribute via --path and --name.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeDeleteAction with --path and --name
2. Verify deleteAttribute called
**Expected Result:**
Attribute deleted.
**Verification Criteria:**
- findAttribute called
- deleteAttribute called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00009: Delete attribute by GUID

**ID:** UTS_ATTR_00009
**Traces-To:** SWR_ATTR_00002, SWR_ATTR_00010
**Title:** Delete attribute by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test deleting attribute via --guid.
**Pre-conditions:**
- Attribute GUID exists
**Test Steps:**
1. Call AttributeDeleteAction with --guid
2. Verify findElementByGUID called
3. Verify deleteAttribute called
**Expected Result:**
Attribute deleted.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated
- deleteAttribute called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00010: Delete GUID wrong type raises error

**ID:** UTS_ATTR_00010
**Traces-To:** SWR_ATTR_00002, SWR_ATTR_00010
**Title:** Delete GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong type via GUID raises error.
**Pre-conditions:**
- GUID resolves to non-attribute
**Test Steps:**
1. Call AttributeDeleteAction with --guid for Class
2. Verify CliExecutionError raised
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to an Attribute"
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00011: View attribute table output

**ID:** UTS_ATTR_00011
**Traces-To:** SWR_ATTR_00003, SWR_ATTR_00008
**Title:** View attribute in table format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing attribute in table format.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeViewAction with format=table
2. Verify table output
**Expected Result:**
Table with all properties.
**Verification Criteria:**
- Table contains Name, GUID, Type, etc.
- OutputFormatter.table called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00012: View attribute JSON output

**ID:** UTS_ATTR_00012
**Traces-To:** SWR_ATTR_00003, SWR_ATTR_00008
**Title:** View attribute in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test viewing attribute in JSON format.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeViewAction with format=json
2. Verify JSON output
**Expected Result:**
JSON with 11 keys.
**Verification Criteria:**
- Output is valid JSON
- Contains all 11 fields
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00013: View attribute CSV output

**ID:** UTS_ATTR_00013
**Traces-To:** SWR_ATTR_00003, SWR_ATTR_00008
**Title:** View attribute in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test viewing attribute in CSV format.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeViewAction with format=csv
2. Verify CSV output
**Expected Result:**
CSV with horizontal layout.
**Verification Criteria:**
- Output has header + data row
- 11 columns
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00014: List attributes on classifier

**ID:** UTS_ATTR_00014
**Traces-To:** SWR_ATTR_00004
**Title:** List attributes on classifier
**Type:** Unit
**Priority:** High
**Description:**
Test listing attributes.
**Pre-conditions:**
- Classifier has attributes
**Test Steps:**
1. Call AttributeListAction with --path
2. Verify attributes listed
**Expected Result:**
List of attribute names.
**Verification Criteria:**
- getAttributes called
- All names shown
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00015: List empty classifier

**ID:** UTS_ATTR_00015
**Traces-To:** SWR_ATTR_00004
**Title:** List attributes on empty classifier
**Type:** Unit
**Priority:** Medium
**Description:**
Test listing when no attributes.
**Pre-conditions:**
- Classifier has no attributes
**Test Steps:**
1. Call AttributeListAction
2. Verify empty output
**Expected Result:**
Empty output.
**Verification Criteria:**
- getAttributes returns empty
- Output is empty
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00016: List JSON output

**ID:** UTS_ATTR_00016
**Traces-To:** SWR_ATTR_00004, SWR_ATTR_00008
**Title:** List attributes in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test listing in JSON format.
**Pre-conditions:**
- Classifier has attributes
**Test Steps:**
1. Call AttributeListAction with format=json
2. Verify JSON array
**Expected Result:**
JSON array of strings.
**Verification Criteria:**
- Output is valid JSON array
- Contains all names
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00017: Update attribute by path and name

**ID:** UTS_ATTR_00017
**Traces-To:** SWR_ATTR_00005
**Title:** Update attribute by path and name
**Type:** Unit
**Priority:** High
**Description:**
Test updating attribute.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeUpdateAction with --path and --name
2. Verify attributes updated
**Expected Result:**
Attribute updated.
**Verification Criteria:**
- setType called
- Logger shows INFO
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00018: Update attribute by GUID

**ID:** UTS_ATTR_00018
**Traces-To:** SWR_ATTR_00005, SWR_ATTR_00010
**Title:** Update attribute by GUID
**Type:** Unit
**Priority:** High
**Description:**
Test updating attribute via GUID.
**Pre-conditions:**
- Attribute GUID exists
**Test Steps:**
1. Call AttributeUpdateAction with --guid
2. Verify type validation
3. Verify attributes updated
**Expected Result:**
Attribute updated.
**Verification Criteria:**
- findElementByGUID called
- metaClass validated
- setType called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00019: Update partial update

**ID:** UTS_ATTR_00019
**Traces-To:** SWR_ATTR_00005
**Title:** Update partial - only specified fields
**Type:** Unit
**Priority:** High
**Description:**
Test partial update.
**Pre-conditions:**
- Attribute exists
**Test Steps:**
1. Call AttributeUpdateAction with only type field
2. Verify only setType called
**Expected Result:**
Only type updated.
**Verification Criteria:**
- setType called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00020: Update skips unknown fields

**ID:** UTS_ATTR_00020
**Traces-To:** SWR_ATTR_00005
**Title:** Update skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test unknown fields skipped.
**Pre-conditions:**
- JSON has unknown fields
**Test Steps:**
1. Call AttributeUpdateAction with unknown field
2. Verify warning logged
**Expected Result:**
Unknown skipped.
**Verification Criteria:**
- Logger.warning called
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00021: Path validation - attribute not found

**ID:** UTS_ATTR_00021
**Traces-To:** SWR_ATTR_00006
**Title:** Attribute name not found raises error
**Type:** Unit
**Priority:** High
**Description:**
Test error when attribute not found.
**Pre-conditions:**
- Attribute name doesn't exist
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

## UTS_ATTR_00022: GUID not found raises error

**ID:** UTS_ATTR_00022
**Traces-To:** SWR_ATTR_00010
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

## UTS_ATTR_00023: AttributeCommand registers all subcommands

**ID:** UTS_ATTR_00023
**Traces-To:** SWR_ATTR_00001, SWR_ATTR_00002, SWR_ATTR_00003, SWR_ATTR_00004, SWR_ATTR_00005
**Title:** AttributeCommand registers 5 subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test command dispatcher.
**Pre-conditions:**
- None
**Test Steps:**
1. Create AttributeCommand
2. Check get_actions()
**Expected Result:**
5 actions registered.
**Verification Criteria:**
- create, delete, view, list, update in command_ids
- len(actions) == 5
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00024: Missing subcommand raises error

**ID:** UTS_ATTR_00024
**Traces-To:** SWR_ATTR_00009
**Title:** Missing subcommand raises error
**Type:** Unit
**Priority:** High
**Description:**
Test missing subcommand.
**Pre-conditions:**
- None
**Test Steps:**
1. Create AttributeCommand with empty args
2. Verify error
**Expected Result:**
Error raised.
**Verification Criteria:**
- CliExecutionError raised
**Last Changed:** 2026-07-10

---

## UTS_ATTR_00025: Create with defaultValue and multiplicity

**ID:** UTS_ATTR_00025
**Traces-To:** SWR_ATTR_00001
**Title:** Create with defaultValue and multiplicity
**Type:** Unit
**Priority:** Medium
**Description:**
Test setting defaultValue and multiplicity.
**Pre-conditions:**
- JSON has defaultValue and multiplicity
**Test Steps:**
1. Call AttributeCreateAction
2. Verify setDefaultValue and setMultiplicity called
**Expected Result:**
Fields set correctly.
**Verification Criteria:**
- setDefaultValue called
- setMultiplicity called
**Last Changed:** 2026-07-10
