# Unit Test Specifications - YAML Import/Export

**Category:** YAML Import/Export
**Prefix:** UTS_XCH
**Test Type:** Unit
**Last Validated:** 2026-07-19

---

## UTS_XCH_00001: Schema version constant sanity

**ID:** UTS_XCH_00001
**Traces-To:** SWR_XCH_005
**Title:** SCHEMA_VERSION and key constants are correctly defined
**Type:** Unit
**Priority:** High
**Description:**
Verify `SCHEMA_VERSION = 1` (int), `VERSION_KEY = "version"`, `PROJECT_KEY = "project"`, `RHAPSODY_MODEL_KEY = "rhapsody-model"`.
**Pre-conditions:**
- `exchange/schema.py` importable
**Test Steps:**
1. Import `SCHEMA_VERSION`, `VERSION_KEY`, `PROJECT_KEY`, `RHAPSODY_MODEL_KEY`
2. Assert types and values
**Expected Result:**
Constants have the expected values and types.
**Verification Criteria:**
- `SCHEMA_VERSION == 1` and `isinstance(SCHEMA_VERSION, int)`
- Each key constant equals its string literal
**Last Changed:** 2026-07-19

---

## UTS_XCH_00002: RhapsodyYaml.read happy path

**ID:** UTS_XCH_00002
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml.read returns parsed YAML mapping
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` returns the parsed dict from a valid YAML file.
**Pre-conditions:**
- Temp file contains `key: value` YAML
**Test Steps:**
1. Instantiate `RhapsodyYaml`
2. Call `read(path)` on the temp file
3. Assert returned dict matches expected
**Expected Result:**
Dict equals `{"key": "value"}`.
**Verification Criteria:**
- Returned object is a `dict`
- `result["key"] == "value"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00003: RhapsodyYaml.read missing file

**ID:** UTS_XCH_00003
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError on missing file
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` raises `CliExecutionError` when the file does not exist.
**Pre-conditions:**
- Path points to a non-existent file
**Test Steps:**
1. Call `read(non_existent_path)`
2. Assert `CliExecutionError` is raised
**Expected Result:**
`CliExecutionError` raised with "Input file not found" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains the path
**Last Changed:** 2026-07-19

---

## UTS_XCH_00004: RhapsodyYaml.read invalid YAML

**ID:** UTS_XCH_00004
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError on malformed YAML
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` raises `CliExecutionError` when the YAML is malformed.
**Pre-conditions:**
- Temp file contains invalid YAML (e.g. `: : :`)
**Test Steps:**
1. Call `read(path)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Invalid YAML" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains file path and parser error
**Last Changed:** 2026-07-19

---

## UTS_XCH_00005: RhapsodyYaml.read non-mapping top level

**ID:** UTS_XCH_00005
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError when top level is not a mapping
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `read(path)` raises `CliExecutionError` when top level is a list or scalar.
**Pre-conditions:**
- Temp file contains `- item` (YAML list)
**Test Steps:**
1. Call `read(path)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Expected YAML mapping" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
**Last Changed:** 2026-07-19

---

## UTS_XCH_00006: RhapsodyYaml.write happy path

**ID:** UTS_XCH_00006
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml.write serializes dict to YAML file
**Type:** Unit
**Priority:** High
**Description:**
Verify `write(path, data)` writes a YAML file that can be read back.
**Pre-conditions:**
- Temp output path
- Dict `{"a": 1, "b": [2, 3]}`
**Test Steps:**
1. Call `write(path, data)`
2. Read the file back with PyYAML directly
3. Assert content matches
**Expected Result:**
File contains the YAML serialization of the dict.
**Verification Criteria:**
- File exists after write
- `yaml.safe_load(open(path))` equals input dict
**Last Changed:** 2026-07-19

---

## UTS_XCH_00007: RhapsodyYaml.write failure

**ID:** UTS_XCH_00007
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.write raises CliExecutionError on OS error
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `write(path, data)` raises `CliExecutionError` when the path is unwritable.
**Pre-conditions:**
- Path points to a directory that does not exist
**Test Steps:**
1. Call `write(non_existent_dir/file, data)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Failed to write" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains the path
**Last Changed:** 2026-07-19

---

## UTS_XCH_00008: RhapsodyYaml round-trip

**ID:** UTS_XCH_00008
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml write then read preserves data
**Type:** Unit
**Priority:** High
**Description:**
Verify data written via `write` can be read back identically via `read`.
**Pre-conditions:**
- Temp file path
**Test Steps:**
1. Call `write(path, original_dict)`
2. Call `read(path)` → result
3. Assert `result == original_dict`
**Expected Result:**
Round-trip preserves the dict.
**Verification Criteria:**
- `result == original_dict`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00009: find_or_create_package sanitizes name and delegates to add_new_aggr

**ID:** UTS_XCH_00009
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_package creates a Package via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_package` sanitizes the name and calls `parent.add_new_aggr("Package", name)` when the child does not exist.
**Pre-conditions:**
- Fake parent with no matching child
**Test Steps:**
1. Call `helper.find_or_create_package(parent, "My Package")`
2. Assert `parent.add_new_aggr` called with `("Package", "My_Package")`
**Expected Result:**
Package created with sanitized name.
**Verification Criteria:**
- `add_new_aggr` called once with `"Package"` and sanitized name
**Last Changed:** 2026-07-19

---

## UTS_XCH_00010: find_or_create_class creates via add_new_aggr

**ID:** UTS_XCH_00010
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_class creates a Class via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_class` calls `parent.add_new_aggr("Class", name)` when not found.
**Pre-conditions:**
- Fake parent with no matching child
**Test Steps:**
1. Call `helper.find_or_create_class(parent, "MyClass")`
2. Assert `add_new_aggr("Class", "MyClass")` called
**Expected Result:**
Class created.
**Verification Criteria:**
- `add_new_aggr` called once with `("Class", "MyClass")`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00011: find_or_create_operation on package uses add_global_function

**ID:** UTS_XCH_00011
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_operation on a Package delegates to add_global_function
**Type:** Unit
**Priority:** High
**Description:**
Verify that when the parent is a Package, `find_or_create_operation` calls `parent.add_global_function(name)`.
**Pre-conditions:**
- Fake parent whose `get_meta_class()` returns "Package"
**Test Steps:**
1. Call `helper.find_or_create_operation(parent, "myFunc")`
2. Assert `parent.add_global_function` called with `"myFunc"`
**Expected Result:**
Operation created via `add_global_function`.
**Verification Criteria:**
- `add_global_function("myFunc")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00012: find_or_create_operation on class uses add_new_aggr

**ID:** UTS_XCH_00012
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_operation on a Class delegates to add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify that when the parent is a Class, `find_or_create_operation` calls `parent.add_new_aggr("Operation", name)`.
**Pre-conditions:**
- Fake parent whose `get_meta_class()` returns "Class"
**Test Steps:**
1. Call `helper.find_or_create_operation(parent, "myOp")`
2. Assert `add_new_aggr("Operation", "myOp")` called
**Expected Result:**
Operation created via `add_new_aggr`.
**Verification Criteria:**
- `add_new_aggr("Operation", "myOp")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00013: find_or_create_argument uses add_argument

**ID:** UTS_XCH_00013
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_argument delegates to parent.add_argument
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_argument` calls `parent.add_argument(name)`.
**Pre-conditions:**
- Fake parent (Operation)
**Test Steps:**
1. Call `helper.find_or_create_argument(parent, "x")`
2. Assert `add_argument("x")` called
**Expected Result:**
Argument created.
**Verification Criteria:**
- `add_argument("x")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00014: find_or_create_attribute creates via add_new_aggr

**ID:** UTS_XCH_00014
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_attribute creates an Attribute via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_attribute` calls `parent.add_new_aggr("Attribute", name)`.
**Pre-conditions:**
- Fake parent (Class)
**Test Steps:**
1. Call `helper.find_or_create_attribute(parent, "threshold")`
2. Assert `add_new_aggr("Attribute", "threshold")` called
**Expected Result:**
Attribute created.
**Verification Criteria:**
- `add_new_aggr("Attribute", "threshold")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00015: find_or_create_type sets kind after creation

**ID:** UTS_XCH_00015
**Traces-To:** SWR_XCH_006, SWR_XCH_008
**Title:** find_or_create_type creates a Type and sets its kind
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_type` creates via `add_new_aggr("Type", name)` and then calls `_set_type_kind(type_element, kind)`.
**Pre-conditions:**
- Fake parent, kind="Enumeration"
**Test Steps:**
1. Call `helper.find_or_create_type(parent, "Color", "Enumeration")`
2. Assert `add_new_aggr("Type", "Color")` called
3. Assert `set_kind("Enumeration")` called on the new type element
**Expected Result:**
Type created with kind set.
**Verification Criteria:**
- `add_new_aggr` and `set_kind` both called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00016: find_or_create_object creates via add_new_aggr

**ID:** UTS_XCH_00016
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_object creates an Object via add_new_aggr
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `find_or_create_object` calls `parent.add_new_aggr("Object", name)`.
**Pre-conditions:**
- Fake parent (Package)
**Test Steps:**
1. Call `helper.find_or_create_object(parent, "myInstance")`
2. Assert `add_new_aggr("Object", "myInstance")` called
**Expected Result:**
Object created.
**Verification Criteria:**
- `add_new_aggr("Object", "myInstance")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00017: find_or_create_enumeration_literal creates via add_new_aggr

**ID:** UTS_XCH_00017
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_enumeration_literal creates via add_new_aggr("LiteralValue", name)
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `find_or_create_enumeration_literal` calls `parent.add_new_aggr("LiteralValue", name)`.
**Pre-conditions:**
- Fake parent (Type with kind=Enumeration)
**Test Steps:**
1. Call `helper.find_or_create_enumeration_literal(parent, "RED")`
2. Assert `add_new_aggr("LiteralValue", "RED")` called
**Expected Result:**
EnumerationLiteral created.
**Verification Criteria:**
- `add_new_aggr("LiteralValue", "RED")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00018: find_child_by_name returns matching child

**ID:** UTS_XCH_00018
**Traces-To:** SWR_XCH_010
**Title:** find_child_by_name returns the child whose name matches
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_child_by_name(parent, name)` iterates `parent.get_nested_elements()` and returns the matching child.
**Pre-conditions:**
- Fake parent with two children named "A" and "B"
**Test Steps:**
1. Call `find_child_by_name(parent, "B")`
2. Assert the second child is returned
**Expected Result:**
Returns the child named "B".
**Verification Criteria:**
- Returned element's `get_name()` == "B"
**Last Changed:** 2026-07-19

---

## UTS_XCH_00019: find_child_by_name returns None when no match

**ID:** UTS_XCH_00019
**Traces-To:** SWR_XCH_010
**Title:** find_child_by_name returns None when no child matches
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_child_by_name` returns `None` when no child has the requested name.
**Pre-conditions:**
- Fake parent with children "A", "B"
**Test Steps:**
1. Call `find_child_by_name(parent, "Z")`
2. Assert result is `None`
**Expected Result:**
Returns `None`.
**Verification Criteria:**
- `result is None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00020: apply_stereotypes infers meta_type from element

**ID:** UTS_XCH_00020
**Traces-To:** SWR_XCH_007
**Title:** apply_stereotypes infers meta_type and calls add_stereotype
**Type:** Unit
**Priority:** High
**Description:**
Verify `apply_stereotypes(element, ["active", "boundary"])` calls `element.add_stereotype(name, meta_type)` for each, with `meta_type` derived from `element.get_meta_class()`.
**Pre-conditions:**
- Fake element with `get_meta_class()` returning "Class"
**Test Steps:**
1. Call `apply_stereotypes(element, ["active", "boundary"])`
2. Assert `add_stereotype` called twice with `("active", "Class")` and `("boundary", "Class")`
**Expected Result:**
Both stereotypes added with correct meta_type.
**Verification Criteria:**
- `add_stereotype.call_count == 2`
- Each call's second arg equals "Class"
**Last Changed:** 2026-07-19

---

## UTS_XCH_00021: apply_stereotypes skips already-applied stereotypes

**ID:** UTS_XCH_00021
**Traces-To:** SWR_XCH_007
**Title:** apply_stereotypes is idempotent — skips already-applied stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `apply_stereotypes` does not call `add_stereotype` for stereotypes the element already has.
**Pre-conditions:**
- Fake element with `get_already_applied_stereotypes` returning "active"
**Test Steps:**
1. Call `apply_stereotypes(element, ["active", "boundary"])`
2. Assert `add_stereotype` called only for "boundary"
**Expected Result:**
Only the missing stereotype is added.
**Verification Criteria:**
- `add_stereotype.call_count == 1`
- `add_stereotype` called with `("boundary", ...)`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00022: apply_tags uses set_property_value

**ID:** UTS_XCH_00022
**Traces-To:** SWR_XCH_007
**Title:** apply_tags calls set_property_value for each key/value pair
**Type:** Unit
**Priority:** High
**Description:**
Verify `apply_tags(element, {"status": "active", "level": "3"})` calls `element.set_property_value(key, val)` for each entry.
**Pre-conditions:**
- Fake element with `set_property_value` mock
**Test Steps:**
1. Call `apply_tags(element, tags_dict)`
2. Assert `set_property_value` called twice
**Expected Result:**
Both tags set.
**Verification Criteria:**
- `set_property_value.call_count == 2`
- Both `("status", "active")` and `("level", "3")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00023: resolve_classifier searches project recursively

**ID:** UTS_XCH_00023
**Traces-To:** SWR_XCH_010
**Title:** resolve_classifier walks project.get_nested_elements() to find a classifier by name
**Type:** Unit
**Priority:** High
**Description:**
Verify `resolve_classifier(name)` returns the first classifier whose `get_name()` matches.
**Pre-conditions:**
- Fake project with nested elements containing a Class named "Base"
**Test Steps:**
1. Call `helper.resolve_classifier("Base")`
2. Assert returned element has `get_name() == "Base"`
**Expected Result:**
Returns the matching classifier.
**Verification Criteria:**
- Returned element is not `None`
- `get_name() == "Base"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00024: resolve_classifier returns None when not found

**ID:** UTS_XCH_00024
**Traces-To:** SWR_XCH_010
**Title:** resolve_classifier returns None when no classifier matches
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `resolve_classifier(name)` returns `None` when the name is not found.
**Pre-conditions:**
- Fake project with no classifier named "Missing"
**Test Steps:**
1. Call `helper.resolve_classifier("Missing")`
2. Assert result is `None`
**Expected Result:**
Returns `None`.
**Verification Criteria:**
- `result is None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00025: get_classifier_name is None-safe

**ID:** UTS_XCH_00025
**Traces-To:** SWR_XCH_010
**Title:** get_classifier_name returns None when classifier is None or get_name raises
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `get_classifier_name(None)` returns `None` and that exceptions from `get_name()` are swallowed.
**Pre-conditions:**
- None classifier
- Fake classifier whose `get_name` raises
**Test Steps:**
1. Call `get_classifier_name(None)` → `None`
2. Call `get_classifier_name(broken_classifier)` → `None`
**Expected Result:**
Both return `None`.
**Verification Criteria:**
- Both results are `None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00026: _set_type_kind calls set_kind

**ID:** UTS_XCH_00026
**Traces-To:** SWR_XCH_006, SWR_XCH_008
**Title:** _set_type_kind delegates to type_element.set_kind
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_set_type_kind(type_element, "Enumeration")` calls `type_element.set_kind("Enumeration")`.
**Pre-conditions:**
- Fake type element
**Test Steps:**
1. Call `helper._set_type_kind(type_element, "Enumeration")`
2. Assert `set_kind("Enumeration")` called
**Expected Result:**
Kind set on the type.
**Verification Criteria:**
- `set_kind` called once with `"Enumeration"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00027: _collect_children returns nested elements

**ID:** UTS_XCH_00027
**Traces-To:** SWR_XCH_010
**Title:** _collect_children returns get_nested_elements() contents
**Type:** Unit
**Priority:** High
**Description:**
Verify `_collect_children(container)` returns the contents of `container.get_nested_elements()`.
**Pre-conditions:**
- Fake container with 2 nested elements
**Test Steps:**
1. Call `helper._collect_children(container)`
2. Assert result has 2 items
**Expected Result:**
Returns the 2 nested elements.
**Verification Criteria:**
- `len(result) == 2`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00028: _collect_children merges package globals

**ID:** UTS_XCH_00028
**Traces-To:** SWR_XCH_010
**Title:** _collect_children merges get_global_functions/variables/objects for packages
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_collect_children` on a Package also includes globals from `get_global_functions`, `get_global_variables`, `get_global_objects` (when available).
**Pre-conditions:**
- Fake package with nested elements + global functions/variables/objects
**Test Steps:**
1. Call `helper._collect_children(package)`
2. Assert result contains all 4 sources
**Expected Result:**
Combined list returned.
**Verification Criteria:**
- Result includes items from all 4 sources
**Last Changed:** 2026-07-19

---

## UTS_XCH_00029: _get_project_name walks owner chain

**ID:** UTS_XCH_00029
**Traces-To:** SWR_XCH_010
**Title:** _get_project_name walks the owner chain to find the Project's name
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_get_project_name(element)` returns the name of the Project ancestor.
**Pre-conditions:**
- Fake element whose owner chain leads to a project named "MyProject"
**Test Steps:**
1. Call `helper._get_project_name(element)`
2. Assert result equals "MyProject"
**Expected Result:**
Returns "MyProject".
**Verification Criteria:**
- `result == "MyProject"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00030 through UTS_XCH_00045: RhapsodyImporter core element dispatch (Task 5)

These 16 test cases cover `RhapsodyImporter.import_template` (version check, dispatch) and `_process_element` / `_apply_<type>_extras` for the 8 core element types (Package, Class, Operation, Argument, Attribute, Type, Object, EnumerationLiteral).

**Traces-To:** SWR_XCH_002, SWR_XCH_004, SWR_XCH_008, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

Each entry in this range follows the same template:
- **UTS_XCH_00030:** import_template raises CliExecutionError on version mismatch (SWR_XCH_009)
- **UTS_XCH_00031:** import_template dispatches each spec to _process_element (SWR_XCH_002)
- **UTS_XCH_00032:** _process_element creates Package and recurses into children (SWR_XCH_006, SWR_XCH_008)
- **UTS_XCH_00033:** _process_element creates Class and applies is_abstract/is_active (SWR_XCH_008)
- **UTS_XCH_00034:** _process_element creates Operation and applies return_type/visibility/is_static (SWR_XCH_008)
- **UTS_XCH_00035:** _apply_operation_extras creates Arguments and sets direction/type (SWR_XCH_008)
- **UTS_XCH_00036:** _process_element creates Argument and applies direction/type (SWR_XCH_008)
- **UTS_XCH_00037:** _process_element creates Attribute and applies type/visibility/multiplicity (SWR_XCH_008)
- **UTS_XCH_00038:** _process_element creates Type with kind and processes literals (SWR_XCH_008)
- **UTS_XCH_00039:** _process_element creates Object and sets classifier (SWR_XCH_008)
- **UTS_XCH_00040:** _process_element creates EnumerationLiteral with stereotypes/tags (SWR_XCH_007, SWR_XCH_008)
- **UTS_XCH_00041:** _process_element applies stereotypes to all element types (SWR_XCH_007)
- **UTS_XCH_00042:** _process_element applies tags to all element types (SWR_XCH_007)
- **UTS_XCH_00043:** _process_element skips unsupported type with warning (SWR_XCH_009)
- **UTS_XCH_00044:** _process_element skips missing type reference with warning (SWR_XCH_009)
- **UTS_XCH_00045:** _process_element recurses into Package children (SWR_XCH_006)

---

## UTS_XCH_00046 through UTS_XCH_00059: RhapsodyImporter extension (Task 6)

These 14 test cases cover `_apply_<type>_extras` for the 6 new element types (Dependency, Generalization, Relation, Port, Event, EventReception) and the dispatch wiring in `_process_element`.

**Traces-To:** SWR_XCH_011, SWR_XCH_012, SWR_XCH_013, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00046:** _apply_dependency_extras wires from/to via resolve_classifier (SWR_XCH_011)
- **UTS_XCH_00047:** _apply_dependency_extras skips missing target with warning (SWR_XCH_009, SWR_XCH_011)
- **UTS_XCH_00048:** _apply_generalization_extras wires subtype/superclass (SWR_XCH_011)
- **UTS_XCH_00049:** _apply_generalization_extras skips missing superclass (SWR_XCH_009)
- **UTS_XCH_00050:** _apply_relation_extras wires from/to and sets relation_type (SWR_XCH_011)
- **UTS_XCH_00051:** _apply_relation_extras sets multiplicity/role/visibility/is_navigable/is_virtual (SWR_XCH_011)
- **UTS_XCH_00052:** _apply_port_extras sets is_behavioral/is_reversed (SWR_XCH_012)
- **UTS_XCH_00053:** _apply_port_extras sets contract via resolve_classifier (SWR_XCH_012)
- **UTS_XCH_00054:** _apply_port_extras adds provided_interfaces (SWR_XCH_012)
- **UTS_XCH_00055:** _apply_port_extras adds required_interfaces (SWR_XCH_012)
- **UTS_XCH_00056:** _apply_port_extras skips missing contract with warning (SWR_XCH_009, SWR_XCH_012)
- **UTS_XCH_00057:** _apply_event_extras sets base_event/super_event (SWR_XCH_013)
- **UTS_XCH_00058:** _apply_event_reception_extras sets event reference (SWR_XCH_013)
- **UTS_XCH_00059:** _process_element dispatch table includes all 14 types (SWR_XCH_006)

---

## UTS_XCH_00060 through UTS_XCH_00075: RhapsodyExporter core element dispatch (Task 7)

These 16 test cases cover `RhapsodyExporter.export` (top-level dict shape, version/project/rhapsody-model keys) and `_export_<type>` for the 8 core element types plus `_export_stereotypes`, `_export_tags`, and skip-on-unsupported behavior.

**Traces-To:** SWR_XCH_001, SWR_XCH_003, SWR_XCH_005, SWR_XCH_007, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00060:** export returns dict with version=1, project name, rhapsody-model list (SWR_XCH_005)
- **UTS_XCH_00061:** export skips None children (SWR_XCH_009)
- **UTS_XCH_00062:** _export_element dispatches Package to _export_package (SWR_XCH_001)
- **UTS_XCH_00063:** _export_package emits children list (SWR_XCH_008)
- **UTS_XCH_00064:** _export_class emits is_abstract/is_active (SWR_XCH_008)
- **UTS_XCH_00065:** _export_operation emits return_type and arguments (SWR_XCH_008)
- **UTS_XCH_00066:** _export_argument emits direction and type (SWR_XCH_008)
- **UTS_XCH_00067:** _export_attribute emits type/visibility/multiplicity (SWR_XCH_008)
- **UTS_XCH_00068:** _export_type emits kind and literals (SWR_XCH_008)
- **UTS_XCH_00069:** _export_object emits classifier name (SWR_XCH_008)
- **UTS_XCH_00070:** _export_enumeration_literal emits name only (SWR_XCH_008)
- **UTS_XCH_00071:** _export_stereotypes returns list of names (SWR_XCH_007)
- **UTS_XCH_00072:** _export_tags returns dict of name→value (SWR_XCH_007)
- **UTS_XCH_00073:** _export_tags skips malformed tags (SWR_XCH_007, SWR_XCH_009)
- **UTS_XCH_00074:** _export_element returns None for unknown metaclass (SWR_XCH_009)
- **UTS_XCH_00075:** _export_element returns None for None input (SWR_XCH_009)

---

## UTS_XCH_00076 through UTS_XCH_00089: RhapsodyExporter extension (Task 8)

These 14 test cases cover `_export_<type>` for the 6 new element types (Dependency, Generalization, Relation, Port, Event, EventReception) and the updated dispatch table.

**Traces-To:** SWR_XCH_011, SWR_XCH_012, SWR_XCH_013
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00076:** _export_dependency emits from/to names (SWR_XCH_011)
- **UTS_XCH_00077:** _export_dependency emits stereotypes/tags (SWR_XCH_007, SWR_XCH_011)
- **UTS_XCH_00078:** _export_generalization emits subtype/superclass (SWR_XCH_011)
- **UTS_XCH_00079:** _export_relation emits from/to/relation_type (SWR_XCH_011)
- **UTS_XCH_00080:** _export_relation emits multiplicity/role/visibility/is_navigable/is_virtual (SWR_XCH_011)
- **UTS_XCH_00081:** _export_port emits is_behavioral/is_reversed (SWR_XCH_012)
- **UTS_XCH_00082:** _export_port emits contract name (SWR_XCH_012)
- **UTS_XCH_00083:** _export_port emits provided_interfaces list (SWR_XCH_012)
- **UTS_XCH_00084:** _export_port emits required_interfaces list (SWR_XCH_012)
- **UTS_XCH_00085:** _export_event emits base_event/super_event (SWR_XCH_013)
- **UTS_XCH_00086:** _export_event_reception emits event reference (SWR_XCH_013)
- **UTS_XCH_00087:** _export_element dispatch table includes all 14 types (SWR_XCH_006)
- **UTS_XCH_00088:** _export_name_list helper converts collection of elements to list of names (SWR_XCH_011, SWR_XCH_012)
- **UTS_XCH_00089:** _classifier_name helper is None-safe (SWR_XCH_010, SWR_XCH_011)

---

## UTS_XCH_00090: ProjectCommand registers export/import subcommands

**ID:** UTS_XCH_00090
**Traces-To:** SWR_XCH_001, SWR_XCH_002
**Title:** ProjectCommand.get_actions includes ProjectExportAction and ProjectImportAction
**Type:** Unit
**Priority:** High
**Description:**
Verify `ProjectCommand.get_actions()` returns 6 actions including "export" and "import".
**Pre-conditions:**
- `ProjectCommand` importable
**Test Steps:**
1. Construct `ProjectCommand(["open", "x.rpy"])`
2. Call `get_actions()`
3. Collect `command_id` values
4. Assert "export" and "import" present and `len(actions) == 6`
**Expected Result:**
All 6 actions registered.
**Verification Criteria:**
- `"export" in command_ids`
- `"import" in command_ids`
- `len(actions) == 6`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00091: PackageCommand registers export/import subcommands

**ID:** UTS_XCH_00091
**Traces-To:** SWR_XCH_003, SWR_XCH_004
**Title:** PackageCommand.get_actions includes PackageExportAction and PackageImportAction
**Type:** Unit
**Priority:** High
**Description:**
Verify `PackageCommand.get_actions()` returns 7 actions including "export" and "import".
**Pre-conditions:**
- `PackageCommand` importable
**Test Steps:**
1. Construct `PackageCommand(["create", "--path", "Sensors", '{}'])`
2. Call `get_actions()`
3. Collect `command_id` values
4. Assert "export" and "import" present and `len(actions) == 7`
**Expected Result:**
All 7 actions registered.
**Verification Criteria:**
- `"export" in command_ids`
- `"import" in command_ids`
- `len(actions) == 7`
**Last Changed:** 2026-07-19