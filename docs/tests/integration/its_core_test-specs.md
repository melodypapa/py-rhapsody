# Integration Test Specifications - Wrapping Machinery

**Category:** CORE
**Prefix:** ITS
**Test Type:** Integration
**Last Validated:** 2026-07-07

---

## ITS_CORE_00001: wrap dispatches across multiple registered element types

**ID:** ITS_CORE_00001
**Traces-To:** SWR_CORE_00005, SWR_CORE_00006, SWR_ELEM_00013
**Title:** wrap() routes raw COM objects of distinct meta classes to their dedicated wrappers
**Type:** Integration
**Priority:** High
**Description:**
Verifies that the `wrap()` factory integrates correctly with the registry populated by
`register_wrapper` calls in the element modules. A single `wrap()` call site must dispatch to the
correct wrapper class based on each COM object's `getMetaClass()` return value, exercising at
least `Project`, `Package`, `Class`, and `Actor` in the same test.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported (registry populated for all core element types).
- Four mock COM objects, each returning a distinct meta class string from `getMetaClass()`:
  `"Project"`, `"Package"`, `"Class"`, `"Actor"`.
**Test Steps:**
1. Call `wrap(mock_project_com)` and assert the result is an `RPProject`.
2. Call `wrap(mock_package_com)` and assert the result is an `RPPackage`.
3. Call `wrap(mock_class_com)` and assert the result is an `RPClass`.
4. Call `wrap(mock_actor_com)` and assert the result is an `RPActor`.
5. For each result, assert `result._com` is the corresponding input mock.
**Expected Result:**
`wrap()` returns the matching wrapper subclass for each meta class; the underlying COM object is
preserved on `_com` for every dispatch.
**Verification Criteria:**
- All four returned objects are instances of their dedicated wrapper subclasses (not the generic
  `RPModelElement`).
- Each `result._com` is the original mock COM object passed in.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00002: RPCollection iteration auto-wraps mixed element types

**ID:** ITS_CORE_00002
**Traces-To:** SWR_CORE_00003, SWR_CORE_00007
**Title:** Iterating an RPCollection of mixed element types yields properly wrapped instances
**Type:** Integration
**Priority:** High
**Description:**
Verifies integration between `RPCollection.__iter__`, `RPCollection.getItem`, and
`_wrap_if_element`/`wrap`. A collection containing heterogeneous raw COM elements (e.g., a Class,
an Attribute, and an Operation) must iterate as their respective wrapper subclasses without
caller intervention.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
- A mock `IRPCollection` whose `getCount()` returns 3 and `getItem(i)` returns, in order, mock
  COM objects reporting meta classes `"Class"`, `"Attribute"`, `"Operation"`.
**Test Steps:**
1. Construct `coll = RPCollection(mock_irp_collection)`.
2. Iterate `coll` and collect items into a list.
3. Assert the list length is 3.
4. Assert item[0] is an `RPClass`, item[1] is an `RPAttribute`, item[2] is an `RPOperation`.
5. Assert `len(coll) == 3` and `coll[1]._com` is the first mock (1-based COM indexing).
**Expected Result:**
Iteration transparently dispatches each raw element through `wrap()`, producing correctly typed
wrappers; `__len__` and 1-based `__getitem__` agree with `getCount()`/`getItem`.
**Verification Criteria:**
- All three iterated items are instances of the correct wrapper subclasses.
- `len(coll) == mock_irp_collection.getCount()`.
- `coll[1]` corresponds to `getItem(1)` (1-based indexing honored).
**Last Changed:** 2026-07-07

---

## ITS_CORE_00003: call_com translates pywintypes.com_error to RhapsodyRuntimeException

**ID:** ITS_CORE_00003
**Traces-To:** SWR_CORE_00004, SWR_EXC_00001, SWR_EXC_00004
**Title:** call_com funnels a pywintypes.com_error into a RhapsodyRuntimeException preserving the message
**Type:** Integration
**Priority:** High
**Description:**
Verifies the cross-boundary error contract: `call_com` must catch `pywintypes.com_error` raised
by a COM-callable and re-raise it as `RhapsodyRuntimeException` with the original message text
preserved. Callers must never observe the raw `pywintypes.com_error`.
**Pre-conditions:**
- `pywintypes` is importable (Windows) OR the module is patched to provide a `com_error` for the
  test. The test is skipped on platforms where `pywintypes is None`.
- A callable that raises `pywintypes.com_error("RPC server unavailable", 0x800401E3, None, None)`.
**Test Steps:**
1. Call `call_com(failing_callable)`.
2. Assert `RhapsodyRuntimeException` is raised (not `pywintypes.com_error`).
3. Assert the exception message contains the original COM error text (e.g., the
   `RPC server unavailable` substring or the hresult string).
4. Call `call_com(lambda: "ok")` and assert the result is `"ok"` (no false positives).
**Expected Result:**
On a COM error, `call_com` raises `RhapsodyRuntimeException` with the original message; on
success it returns the value unchanged.
**Verification Criteria:**
- `pytest.raises(RhapsodyRuntimeException)` succeeds for the failing callable.
- The exception's `str()` contains a substring derived from the original COM message.
- The success-path callable returns its value verbatim.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00004: wrap falls back to RPModelElement for unmapped meta class

**ID:** ITS_CORE_00004
**Traces-To:** SWR_CORE_00005, SWR_CORE_00008
**Title:** wrap() returns a generic RPModelElement when the meta class is not in the registry
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the registry fallback integration: when a COM object's `getMetaClass()` returns a string
that has no entry in the wrapper registry (e.g., a hypothetical `"FancyNewElement"`), `wrap()`
must return a plain `RPModelElement` rather than raising. This guarantees navigation code keeps
working for element types without dedicated wrappers.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
- A mock COM object whose `getMetaClass()` returns `"FancyNewElement"` (an unmapped type).
- The mock also exposes `getName()` returning `"someName"`.
**Test Steps:**
1. Call `wrap(mock_unmapped_com)`.
2. Assert the result is an `RPModelElement` instance.
3. Assert the result is NOT an instance of any registered subclass (RPProject, RPPackage, RPClass,
   RPActor, etc.).
4. Assert `result._com is mock_unmapped_com`.
5. Assert `result.getName() == "someName"` (delegation still works on the fallback wrapper).
**Expected Result:**
Unmapped types yield a generic `RPModelElement` whose COM delegation methods still function.
**Verification Criteria:**
- `isinstance(result, RPModelElement)` is True.
- `type(result) is RPModelElement` (exact class, not a subclass).
- `result.getName()` returns the mock's name.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00005: RPCollection rejects negative indices with IndexError

**ID:** ITS_CORE_00005
**Traces-To:** SWR_CORE_00003, SWR_CORE_00009
**Title:** RPCollection.__getitem__ raises IndexError("negative indices are not supported") for negatives
**Type:** Integration
**Priority:** Low
**Description:**
Verifies that the Python protocol layer on `RPCollection` integrates safely with the 1-based COM
indexing model: negative indices (Python-style from-end access) must be rejected with a specific
`IndexError` message rather than being passed to `getItem`, which would misbehave.
**Pre-conditions:**
- A mock `IRPCollection` whose `getCount()` returns 3 and `getItem(i)` returns a mock element.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Construct `coll = RPCollection(mock_irp_collection)`.
2. Assert `coll[-1]` raises `IndexError` with message `"negative indices are not supported"`.
3. Assert `coll[-100]` raises the same `IndexError`.
4. Assert `mock_irp_collection.getItem` was NOT called for either negative-index attempt.
5. Assert `coll[1]` still succeeds (positive indexing unaffected).
**Expected Result:**
Negative indices are rejected before reaching the COM layer; positive 1-based indexing continues
to work.
**Verification Criteria:**
- `pytest.raises(IndexError, match="negative indices are not supported")` for both negative
  attempts.
- `mock_irp_collection.getItem.call_count == 0` after the negative-index attempts.
- `coll[1]` returns a wrapped element.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00006: Importing elements package registers all core wrappers with wrap()

**ID:** ITS_CORE_00006
**Traces-To:** SWR_CORE_00006, SWR_ELEM_00013
**Title:** After importing rhapsody_cli.models.elements, wrap() resolves all core meta classes
**Type:** Integration
**Priority:** High
**Description:**
Verifies that the side-effecting `register_wrapper` calls performed at element-module import time
correctly populate the shared registry that `wrap()` consults. After importing the elements
package, `wrap()` must resolve every core meta class to its dedicated wrapper class without
requiring any explicit registration call from the user.
**Pre-conditions:**
- A fresh interpreter state (or a re-import) of `rhapsody_cli.models.elements`.
- Mock COM objects for each of the registered meta classes: `Project`, `Package`, `Class`,
  `Actor`, `Operation`, `Attribute`, `ActivityDiagram`, `Instance`, `Requirement`, `Statechart`,
  `UseCase`.
**Test Steps:**
1. `import rhapsody_cli.models.elements` (if not already imported).
2. For each (meta_class, expected_wrapper) pair, construct a mock COM object whose
   `getMetaClass()` returns `meta_class`.
3. Call `wrap(mock)` for each and assert the result `isinstance` of the expected wrapper class.
4. Assert the registry contains entries for all 11 listed meta classes.
**Expected Result:**
A single import of the elements package is sufficient to make `wrap()` dispatch correctly to all
core wrapper classes; no additional user-side registration is required.
**Verification Criteria:**
- All 11 mock objects are wrapped to instances of their expected wrapper subclasses.
- The registry dict contains at least the 11 listed meta-class keys.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00007: RPUnit save and filename flow integrates with call_com

**ID:** ITS_CORE_00007
**Traces-To:** SWR_CORE_00002, SWR_CORE_00004
**Title:** RPUnit.save / setFilename / setReadOnly route through call_com and translate failures
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies that `RPUnit`'s file-operation methods integrate with the shared `call_com` helper
rather than calling COM directly. Success path returns normally; failure path surfaces as
`RhapsodyRuntimeException`. Also confirms `setReadOnly(True)` translates to the integer `1` on the
COM side.
**Pre-conditions:**
- A mock COM unit object exposing `save()`, `getFilename()`, `setFilename(name)`, `isReadOnly()`,
  `setReadOnly(int)`.
- `rhapsody_cli.models._core` imported (so `RPUnit`, `call_com`, `RhapsodyRuntimeException` are
  available).
- `pywintypes.com_error` available or patched.
**Test Steps:**
1. Construct `unit = RPUnit(mock_com_unit)`.
2. Call `unit.save()`; assert `mock_com_unit.save` was called once.
3. Call `unit.setFilename("new.rpy")`; assert `mock_com_unit.setFilename` was called with
   `"new.rpy"`.
4. Call `unit.setReadOnly(True)`; assert `mock_com_unit.setReadOnly` was called with `1` (not
   `True`).
5. Patch `mock_com_unit.save` to raise `pywintypes.com_error("disk full", 0, None, None)`.
6. Call `unit.save()` and assert `RhapsodyRuntimeException` is raised with the original message.
**Expected Result:**
`RPUnit` file operations delegate through `call_com`; boolean→integer translation is applied; COM
errors are translated to `RhapsodyRuntimeException`.
**Verification Criteria:**
- `mock_com_unit.save.call_count == 1` after step 2.
- `mock_com_unit.setReadOnly` last call arg is `1` after step 4.
- `pytest.raises(RhapsodyRuntimeException)` succeeds for step 6.
**Last Changed:** 2026-07-07

---

## ITS_CORE_00008: RPModelElement equality, hash, and repr integrate across wrappers

**ID:** ITS_CORE_00008
**Traces-To:** SWR_CORE_00001, SWR_CORE_00005
**Title:** Two wrappers around the same COM object are equal, hash identically, and repr consistently
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies that `RPModelElement.__eq__`, `__hash__`, and `__repr__` integrate with the `wrap()`
factory such that two independently wrapped references to the same underlying COM object are
interchangeable in sets/dicts and produce useful debug output. This is foundational for using
wrappers as dict keys and for de-duplicating collections.
**Pre-conditions:**
- A single mock COM object `mock_com` exposing `getName()` -> `"Foo"` and `getMetaClass()` ->
  `"Class"`.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `a = wrap(mock_com)`; `b = wrap(mock_com)`.
2. Assert `a == b` is True (COM object equality).
3. Assert `hash(a) == hash(b)`.
4. Assert `len({a, b}) == 1` (set deduplication).
5. Assert `repr(a)` contains both the class name (`RPClass`) and the element name (`Foo`).
6. Construct a second distinct mock `mock_com2` with the same name; `c = wrap(mock_com2)`; assert
   `a != c`.
**Expected Result:**
Wrappers of the same COM object are equal and hash-equal; wrappers of distinct COM objects are
not equal even if their names match. `repr` exposes both class and name.
**Verification Criteria:**
- `a == b` is True; `a != c` is True.
- `hash(a) == hash(b)`.
- `len({a, b}) == 1`.
- `repr(a)` contains `"RPClass"` and `"Foo"`.
**Last Changed:** 2026-07-07

---
