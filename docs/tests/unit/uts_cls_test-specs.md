# Unit Test Specifications - Class Command

**Category:** Class Command
**Prefix:** UTS_CLS
**Test Type:** Unit
**Last Validated:** 2026-07-10

---

## UTS_CLS_00001: Create single class with inline JSON

**ID:** UTS_CLS_00001
**Traces-To:** SWR_CLS_00001
**Title:** Create single class with inline JSON
**Type:** Unit
**Priority:** High
**Description:**
Test that a single class can be created with inline JSON containing name and description.
**Pre-conditions:**
- Rhapsody application is mocked
- Parent package exists at specified path
- Valid inline JSON provided
**Test Steps:**
1. Call ClassCreateAction with inline JSON
2. Verify class created via addClass
3. Verify description set via setDescription
**Expected Result:**
Class created successfully with correct name and description.
**Verification Criteria:**
- addClass called once with correct name
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00002: Create multiple classes from JSON file

**ID:** UTS_CLS_00002
**Traces-To:** SWR_CLS_00001, SWR_CLS_00006
**Title:** Create multiple classes from JSON file
**Type:** Unit
**Priority:** High
**Description:**
Test bulk creation of classes from external JSON file with array of class definitions.
**Pre-conditions:**
- JSON file exists with valid array of class definitions
- Parent package exists
**Test Steps:**
1. Call ClassCreateAction with --input pointing to JSON file
2. Verify file read with UTF-8 encoding
3. Verify all classes created
**Expected Result:**
All classes created, logs show count.
**Verification Criteria:**
- File opened with UTF-8 encoding
- addClass called for each class
- Logger shows total count
**Last Changed:** 2026-07-10

---

## UTS_CLS_00003: Create with stereotypes

**ID:** UTS_CLS_00003
**Traces-To:** SWR_CLS_00007
**Title:** Create class with stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that stereotypes are applied to class during creation.
**Pre-conditions:**
- JSON contains stereotypes array
**Test Steps:**
1. Call ClassCreateAction with JSON containing stereotypes
2. Verify addStereotype called for each stereotype
**Expected Result:**
All stereotypes applied correctly with "Class" type.
**Verification Criteria:**
- addStereotype called once per stereotype
- Correct stereotype name and "Class" type passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00004: Create with tags

**ID:** UTS_CLS_00004
**Traces-To:** SWR_CLS_00007
**Title:** Create class with tags
**Type:** Unit
**Priority:** Medium
**Description:**
Test that tags are set on class during creation.
**Pre-conditions:**
- JSON contains tags object
**Test Steps:**
1. Call ClassCreateAction with JSON containing tags
2. Verify setPropertyValue called for each tag
**Expected Result:**
All tags set correctly.
**Verification Criteria:**
- setPropertyValue called once per tag
- Correct key-value pairs passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00005: Create with boolean flags

**ID:** UTS_CLS_00005
**Traces-To:** SWR_CLS_00012
**Title:** Create class with boolean flags isAbstract, isFinal, isActive
**Type:** Unit
**Priority:** Medium
**Description:**
Test that boolean flags are set on class during creation.
**Pre-conditions:**
- JSON contains isAbstract, isFinal, isActive fields
**Test Steps:**
1. Call ClassCreateAction with JSON containing boolean flags
2. Verify setIsAbstract, setIsFinal, setIsActive called with 1/0
**Expected Result:**
All boolean flags set correctly.
**Verification Criteria:**
- setIsAbstract called with 1 if true, 0 if false
- setIsFinal called with 1/0
- setIsActive called with 1/0
**Last Changed:** 2026-07-10

---

## UTS_CLS_00006: Create with operations

**ID:** UTS_CLS_00006
**Traces-To:** SWR_CLS_00001
**Title:** Create class with operations
**Type:** Unit
**Priority:** Medium
**Description:**
Test that operations are added to class during creation.
**Pre-conditions:**
- JSON contains operations array
**Test Steps:**
1. Call ClassCreateAction with JSON containing operations
2. Verify addOperation called for each operation
**Expected Result:**
All operations added correctly.
**Verification Criteria:**
- addOperation called once per operation
- Correct operation names passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00007: Create with attributes

**ID:** UTS_CLS_00007
**Traces-To:** SWR_CLS_00001
**Title:** Create class with attributes
**Type:** Unit
**Priority:** Medium
**Description:**
Test that attributes are added to class during creation.
**Pre-conditions:**
- JSON contains attributes array
**Test Steps:**
1. Call ClassCreateAction with JSON containing attributes
2. Verify addAttribute called for each attribute
**Expected Result:**
All attributes added correctly.
**Verification Criteria:**
- addAttribute called once per attribute
- Correct attribute names passed
**Last Changed:** 2026-07-10

---

## UTS_CLS_00008: Create with superclasses

**ID:** UTS_CLS_00008
**Traces-To:** SWR_CLS_00001
**Title:** Create class with superclasses
**Type:** Unit
**Priority:** Medium
**Description:**
Test that superclasses are resolved and generalizations added during creation.
**Pre-conditions:**
- JSON contains superclasses array
- Superclass names exist in parent package
**Test Steps:**
1. Call ClassCreateAction with JSON containing superclasses
2. Verify findNestedClassifierRecursive called for each superclass name
3. Verify addGeneralization called for each resolved target
**Expected Result:**
All generalizations added correctly.
**Verification Criteria:**
- findNestedClassifierRecursive called once per superclass name
- addGeneralization called once per resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00009: Create skips unknown attributes

**ID:** UTS_CLS_00009
**Traces-To:** SWR_CLS_00001, SWR_CLS_00009
**Title:** Unknown attributes are skipped with warning
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown attributes in JSON are skipped and logged as warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call ClassCreateAction with JSON containing unknown fields
2. Verify class still created
3. Verify warning logged
**Expected Result:**
Class created, unknown fields skipped with warning.
**Verification Criteria:**
- Class created successfully
- Logger.warning called with unknown field names
**Last Changed:** 2026-07-10

---

## UTS_CLS_00010: Create fails without name

**ID:** UTS_CLS_00010
**Traces-To:** SWR_CLS_00001
**Title:** Create fails without name field
**Type:** Unit
**Priority:** High
**Description:**
Test that creation fails when name field is missing from JSON.
**Pre-conditions:**
- JSON does not contain name field
**Test Steps:**
1. Call ClassCreateAction with JSON without name
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with appropriate message.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "'name' is required"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00011: Delete class by path

**ID:** UTS_CLS_00011
**Traces-To:** SWR_CLS_00002
**Title:** Delete class by path successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that a class is deleted successfully by path.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassDeleteAction with valid path
2. Verify deleteFromProject called
3. Verify log message shown
**Expected Result:**
Class deleted with log message.
**Verification Criteria:**
- deleteFromProject called once
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00012: Delete class by GUID

**ID:** UTS_CLS_00012
**Traces-To:** SWR_CLS_00002, SWR_CLS_00013
**Title:** Delete class by GUID successfully
**Type:** Unit
**Priority:** High
**Description:**
Test that a class is deleted successfully by GUID.
**Pre-conditions:**
- Class exists with specified GUID
**Test Steps:**
1. Call ClassDeleteAction with --guid parameter
2. Verify findElementByGUID called on project
3. Verify deleteFromProject called
**Expected Result:**
Class deleted with log message.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- deleteFromProject called once
**Last Changed:** 2026-07-10

---

## UTS_CLS_00013: Delete handles COM error

**ID:** UTS_CLS_00013
**Traces-To:** SWR_CLS_00010
**Title:** Delete handles COM error gracefully
**Type:** Unit
**Priority:** High
**Description:**
Test that COM errors during deletion are handled properly.
**Pre-conditions:**
- deleteFromProject raises exception
**Test Steps:**
1. Call ClassDeleteAction
2. Simulate COM error in deleteFromProject
3. Verify error handled
**Expected Result:**
Exception handled, CliExecutionError raised.
**Verification Criteria:**
- CliExecutionError raised
- Error message contains original error
**Last Changed:** 2026-07-10

---

## UTS_CLS_00014: Delete requires path or guid

**ID:** UTS_CLS_00014
**Traces-To:** SWR_CLS_00002, SWR_CLS_00013
**Title:** Delete requires exactly one of path or guid
**Type:** Unit
**Priority:** High
**Description:**
Test that delete raises error when neither or both path and guid are specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassDeleteAction with neither path nor guid
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --path or --guid must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --path or --guid"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00015: View table output

**ID:** UTS_CLS_00015
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in table format
**Type:** Unit
**Priority:** High
**Description:**
Test that class details are displayed in table format with all 12 fields.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassViewAction with format=table
2. Verify table output contains all properties
**Expected Result:**
Table printed to stdout with all class properties.
**Verification Criteria:**
- Table contains Name, GUID, Description, IsAbstract, etc.
- Operations and Attributes shown as comma-separated
**Last Changed:** 2026-07-10

---

## UTS_CLS_00016: View JSON output to file

**ID:** UTS_CLS_00016
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in JSON format to file
**Type:** Unit
**Priority:** High
**Description:**
Test that class details are written to JSON file with int-normalized IsAbstract.
**Pre-conditions:**
- Class exists at specified path
- Output file path provided
**Test Steps:**
1. Call ClassViewAction with format=json and --output
2. Verify JSON file created
3. Verify JSON contains all 12 fields
4. Verify isAbstract is int (not bool)
**Expected Result:**
JSON file created with all class details, IsAbstract normalized to int.
**Verification Criteria:**
- File created at specified path
- JSON parseable and contains all fields
- isAbstract is 0 or 1 (not true/false)
**Last Changed:** 2026-07-10

---

## UTS_CLS_00017: View CSV output

**ID:** UTS_CLS_00017
**Traces-To:** SWR_CLS_00003, SWR_CLS_00008
**Title:** View class in CSV format
**Type:** Unit
**Priority:** Medium
**Description:**
Test that class details are displayed in CSV format with horizontal layout.
**Pre-conditions:**
- Class exists at specified path
**Test Steps:**
1. Call ClassViewAction with format=csv
2. Verify CSV output has header + data row
**Expected Result:**
CSV printed with horizontal layout (12 columns).
**Verification Criteria:**
- Output has exactly 2 lines
- Header row contains all 12 column names
- Data row present
**Last Changed:** 2026-07-10

---

## UTS_CLS_00018: View by GUID

**ID:** UTS_CLS_00018
**Traces-To:** SWR_CLS_00003, SWR_CLS_00013
**Title:** View class by GUID
**Type:** Unit
**Priority:** Medium
**Description:**
Test that class details can be viewed by GUID.
**Pre-conditions:**
- Class exists with specified GUID
**Test Steps:**
1. Call ClassViewAction with --guid parameter
2. Verify findElementByGUID called
3. Verify class details displayed
**Expected Result:**
Class details displayed.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- Output contains class name
**Last Changed:** 2026-07-10

---

## UTS_CLS_00019: View requires path or guid

**ID:** UTS_CLS_00019
**Traces-To:** SWR_CLS_00003, SWR_CLS_00013
**Title:** View requires exactly one of path or guid
**Type:** Unit
**Priority:** High
**Description:**
Test that view raises error when neither path nor guid is specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassViewAction with neither path nor guid
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --path or --guid must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --path or --guid"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00020: View normalizes IsAbstract to int in JSON

**ID:** UTS_CLS_00020
**Traces-To:** SWR_CLS_00003, SWR_CLS_00009
**Title:** View JSON normalizes IsAbstract bool to int
**Type:** Unit
**Priority:** Medium
**Description:**
Test that getIsAbstract() (which returns bool) is normalized to int in JSON output.
**Pre-conditions:**
- Class exists with IsAbstract=True
**Test Steps:**
1. Call ClassViewAction with format=json
2. Verify JSON output
3. Verify isAbstract field is 1 (not true)
**Expected Result:**
JSON output has isAbstract as 1, not true.
**Verification Criteria:**
- JSON parseable
- isAbstract is int (0 or 1)
- Round-trips cleanly with create's isAbstract input
**Last Changed:** 2026-07-10

---

## UTS_CLS_00021: List classes in package

**ID:** UTS_CLS_00021
**Traces-To:** SWR_CLS_00004
**Title:** List classes in a package
**Type:** Unit
**Priority:** High
**Description:**
Test that classes are listed correctly.
**Pre-conditions:**
- Package has classes
**Test Steps:**
1. Call ClassListAction with parent package path
2. Verify all class names shown
**Expected Result:**
List of class names.
**Verification Criteria:**
- getClasses called
- All class names shown
**Last Changed:** 2026-07-10

---

## UTS_CLS_00022: List empty package

**ID:** UTS_CLS_00022
**Traces-To:** SWR_CLS_00004
**Title:** List empty package returns empty output
**Type:** Unit
**Priority:** Medium
**Description:**
Test that empty output is shown for package with no classes.
**Pre-conditions:**
- Package has no classes
**Test Steps:**
1. Call ClassListAction
2. Verify empty output
**Expected Result:**
Empty table/list shown.
**Verification Criteria:**
- getClasses returns empty
- Output is empty
**Last Changed:** 2026-07-10

---

## UTS_CLS_00023: List JSON output

**ID:** UTS_CLS_00023
**Traces-To:** SWR_CLS_00004, SWR_CLS_00008
**Title:** List classes in JSON format
**Type:** Unit
**Priority:** High
**Description:**
Test that classes are listed in JSON array format.
**Pre-conditions:**
- Package has classes
**Test Steps:**
1. Call ClassListAction with format=json
2. Verify JSON array output
**Expected Result:**
JSON array of class names.
**Verification Criteria:**
- Output is valid JSON array
- Array contains all class names
**Last Changed:** 2026-07-10

---

## UTS_CLS_00024: Add generalization by name

**ID:** UTS_CLS_00024
**Traces-To:** SWR_CLS_00011
**Title:** Add generalization relationship by class name
**Type:** Unit
**Priority:** High
**Description:**
Test that a generalization is added by resolving target class name.
**Pre-conditions:**
- Source class exists
- Target class exists in same package
**Test Steps:**
1. Call ClassLinkAction with --add parameter
2. Verify findNestedClassifierRecursive called
3. Verify addGeneralization called
**Expected Result:**
Generalization added.
**Verification Criteria:**
- findNestedClassifierRecursive called once with correct name
- addGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00025: Remove generalization by name

**ID:** UTS_CLS_00025
**Traces-To:** SWR_CLS_00011
**Title:** Remove generalization relationship by class name
**Type:** Unit
**Priority:** High
**Description:**
Test that a generalization is removed by resolving target class name.
**Pre-conditions:**
- Source class exists with existing generalization
- Target class exists
**Test Steps:**
1. Call ClassLinkAction with --remove parameter
2. Verify findNestedClassifierRecursive called
3. Verify deleteGeneralization called
**Expected Result:**
Generalization removed.
**Verification Criteria:**
- findNestedClassifierRecursive called once with correct name
- deleteGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00026: Link requires add or remove

**ID:** UTS_CLS_00026
**Traces-To:** SWR_CLS_00011
**Title:** Link requires exactly one of add or remove
**Type:** Unit
**Priority:** High
**Description:**
Test that link raises error when neither or both add and remove are specified.
**Pre-conditions:**
- None
**Test Steps:**
1. Call ClassLinkAction with neither add nor remove
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Either --add or --remove must be specified".
**Verification Criteria:**
- CliExecutionError raised
- Error message contains "Either --add or --remove"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00027: Link target not found raises error

**ID:** UTS_CLS_00027
**Traces-To:** SWR_CLS_00011
**Title:** Link raises error when target class not found
**Type:** Unit
**Priority:** High
**Description:**
Test that CliExecutionError is raised when target class name not found.
**Pre-conditions:**
- Source class exists
- Target class name does not exist
**Test Steps:**
1. Call ClassLinkAction with --add pointing to non-existent class
2. Verify findNestedClassifierRecursive returns None
3. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError raised with "Class '<name>' not found".
**Verification Criteria:**
- findNestedClassifierRecursive called once
- CliExecutionError raised
- Error message contains class name
**Last Changed:** 2026-07-10

---

## UTS_CLS_00028: Link by GUID

**ID:** UTS_CLS_00028
**Traces-To:** SWR_CLS_00011, SWR_CLS_00013
**Title:** Link class by source GUID
**Type:** Unit
**Priority:** Medium
**Description:**
Test that source class can be identified by GUID for link operations.
**Pre-conditions:**
- Source class exists with specified GUID
- Target class exists
**Test Steps:**
1. Call ClassLinkAction with --guid parameter
2. Verify findElementByGUID called
3. Verify addGeneralization called
**Expected Result:**
Generalization added via GUID-identified source.
**Verification Criteria:**
- findElementByGUID called once with correct GUID
- addGeneralization called once with resolved target
**Last Changed:** 2026-07-10

---

## UTS_CLS_00029: ClassCommand registers all subcommands

**ID:** UTS_CLS_00029
**Traces-To:** SWR_CLS_00001-00004, SWR_CLS_00011
**Title:** ClassCommand registers all 5 subcommands
**Type:** Unit
**Priority:** High
**Description:**
Test that ClassCommand registers all 5 subcommands.
**Pre-conditions:**
- ClassCommand initialized
**Test Steps:**
1. Create ClassCommand
2. Call get_actions
3. Verify 5 subcommands registered
**Expected Result:**
All 5 subcommands (create, delete, view, list, link) registered.
**Verification Criteria:**
- get_actions returns 5 actions
- All subcommand names present
**Last Changed:** 2026-07-10

---

## UTS_CLS_00030: Update class via path

**ID:** UTS_CLS_00030
**Traces-To:** SWR_CLS_00014
**Title:** Update class via path
**Type:** Unit
**Priority:** High
**Description:**
Test that class can be updated via --path argument.
**Pre-conditions:**
- Class exists at specified path
- Valid JSON provided
**Test Steps:**
1. Call ClassUpdateAction with --path
2. Verify attributes updated
**Expected Result:**
Class updated successfully.
**Verification Criteria:**
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00031: Update class via GUID with type validation

**ID:** UTS_CLS_00031
**Traces-To:** SWR_CLS_00014
**Title:** Update class via GUID with type validation
**Type:** Unit
**Priority:** High
**Description:**
Test that class can be updated via --guid with type validation.
**Pre-conditions:**
- Class exists with given GUID
**Test Steps:**
1. Call ClassUpdateAction with --guid
2. Verify metaClass validation
3. Verify attributes updated
**Expected Result:**
Class updated, type validated.
**Verification Criteria:**
- findElementByGUID called
- metaClass checked equals "Class"
- setIsAbstract called with correct value
**Last Changed:** 2026-07-10

---

## UTS_CLS_00032: Update class GUID wrong type raises error

**ID:** UTS_CLS_00032
**Traces-To:** SWR_CLS_00014
**Title:** Update class GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong element type via --guid raises CliExecutionError.
**Pre-conditions:**
- GUID resolves to non-class element (Package)
**Test Steps:**
1. Call ClassUpdateAction with --guid for Package
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError with type mismatch message.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to a Class"
- Error contains "found Package"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00033: Update class boolean flags

**ID:** UTS_CLS_00033
**Traces-To:** SWR_CLS_00014
**Title:** Update class boolean flags
**Type:** Unit
**Priority:** High
**Description:**
Test updating boolean flags isAbstract, isFinal, isActive.
**Pre-conditions:**
- Class exists
**Test Steps:**
1. Call ClassUpdateAction with boolean flags
2. Verify setIsAbstract, setIsFinal, setIsActive called
**Expected Result:**
Boolean flags updated correctly.
**Verification Criteria:**
- setIsAbstract(1) called for true
- setIsFinal(0) called for false
- setIsActive(1) called for true
**Last Changed:** 2026-07-10

---

## UTS_CLS_00034: Update class partial update

**ID:** UTS_CLS_00034
**Traces-To:** SWR_CLS_00014
**Title:** Update class partial update
**Type:** Unit
**Priority:** High
**Description:**
Test that partial update only modifies specified fields.
**Pre-conditions:**
- Class exists
**Test Steps:**
1. Call ClassUpdateAction with only isAbstract field
2. Verify only setIsAbstract called
3. Verify other setters not called
**Expected Result:**
Only specified field updated.
**Verification Criteria:**
- setIsAbstract called
- setDescription not called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_CLS_00035: Update class skips unknown fields

**ID:** UTS_CLS_00035
**Traces-To:** SWR_CLS_00014
**Title:** Update class skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown fields are skipped with warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call ClassUpdateAction with unknown field
2. Verify warning logged
3. Verify known field still applied
**Expected Result:**
Unknown fields skipped, known fields applied.
**Verification Criteria:**
- Logger.warning called with unknown field name
- Known attribute still applied
**Last Changed:** 2026-07-10