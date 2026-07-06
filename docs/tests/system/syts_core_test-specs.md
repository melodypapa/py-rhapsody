# System Test Specifications - Wrapping Machinery

**Category:** CORE
**Prefix:** SYTS
**Test Type:** System
**Last Validated:** 2026-07-07

---

## SYTS_CORE_00001: wrap Dispatch Across a Realistic Fake Model Graph

**ID:** SYTS_CORE_00001
**Traces-To:** SWR_CORE_00005, SWR_CORE_00006, SWR_CORE_00008
**Title:** wrap() dispatches each fake COM node to its registered wrapper class
**Type:** System
**Priority:** High
**Description:**
This test verifies that the `wrap()` factory correctly dispatches a heterogeneous fake
model graph (Project -> Package -> Class -> Attribute/Operation) to the right wrapper
classes, and that unmapped meta classes fall back to the generic `RPModelElement` wrapper
rather than raising. The graph is navigated end-to-end through the wrapper API.
**Pre-conditions:**
- A fake COM model graph where each node returns a distinct `getMetaClass()` string
  ("Project", "Package", "Class", "Attribute", "Operation", and one unknown type
  "FutureThing").
- The `rhapsody_cli.models.elements` package imported so the wrapper registry is
  populated.
- The graph wired so `getPackages()` returns the Package node, the Package's
  `getNestedElements()` (or equivalent) returns Class nodes, and a Class exposes
  `getAttributes()` / `getOperations()` collections.
**Test Steps:**
1. Obtain the fake Project COM object and call `wrap(project_com)`.
2. Assert the result is an `RPProject` instance.
3. Navigate to the package via `getPackages()` and assert each item is an `RPPackage`.
4. Navigate to a class via the package's class collection and assert it is an `RPClass`.
5. Navigate to an attribute and an operation and assert their wrapper types.
6. Navigate to the "FutureThing" node (unmapped meta class) and assert the result is a
   plain `RPModelElement` (the fallback) rather than raising.
**Expected Result:**
- Each node is wrapped as the correct subclass: RPProject, RPPackage, RPClass,
  RPAttribute, RPOperation.
- The unmapped "FutureThing" node is wrapped as a generic `RPModelElement` without
  raising.
- All wrapper instances expose the expected Java-mirrored methods (e.g. `getName()`,
  `getMetaClass()`, `getGUID()`).
**Verification Criteria:**
- Pass if every isinstance assertion holds and no exception is raised for the unmapped
  type.
- Fail if any node is wrapped as the wrong class, or if `wrap()` raises for the unmapped
  meta class.
**Last Changed:** 2026-07-07

---

## SYTS_CORE_00002: RPCollection End-to-End Iteration Over a Populated Fake Project

**ID:** SYTS_CORE_00002
**Traces-To:** SWR_CORE_00003, SWR_CORE_00007
**Title:** RPCollection iterates and indexes a populated fake collection with auto-wrapping
**Type:** System
**Priority:** High
**Description:**
This test verifies that `RPCollection` exposes Pythonic iteration and 1-based indexing
over a populated fake `IRPCollection`, and that items returned by `getItem` and `__iter__`
are auto-wrapped via `_wrap_if_element` into the correct wrapper classes.
**Pre-conditions:**
- A fake `IRPCollection` with `getCount()` returning 3 and `getItem(i)` returning three
  fake model-element COM objects (e.g. two Class nodes and one Attribute node) plus one
  non-element scalar (to confirm pass-through).
- The wrapper registry populated via the elements package import.
- The fake collection's `getItem` returns 1-based indices.
**Test Steps:**
1. Wrap the fake `IRPCollection` in an `RPCollection`.
2. Assert `len(collection) == 3`.
3. Iterate the collection with a `for` loop and collect the wrapped items.
4. Index the collection with `collection[1]`, `collection[2]`, `collection[3]` and assert
   each is wrapped correctly.
5. Confirm that non-element values returned by `getItem` are passed through unchanged.
**Expected Result:**
- `len(collection)` returns 3.
- Iteration yields exactly 3 items, each auto-wrapped to the matching wrapper subclass
  (RPClass, RPClass, RPAttribute).
- 1-based indexing returns the same items in the same order as iteration.
- Non-element scalar values are returned unchanged (not wrapped).
**Verification Criteria:**
- Pass if length, iteration count, indexing, and auto-wrapping all match expectations.
- Fail if `__iter__` yields the wrong number of items, if items are not auto-wrapped, or
  if 1-based indexing is off by one.
**Last Changed:** 2026-07-07

---

## SYTS_CORE_00003: call_com Error Translation End-to-End

**ID:** SYTS_CORE_00003
**Traces-To:** SWR_CORE_00004, SWR_CORE_00010
**Title:** COM errors raised by wrapper methods surface as RhapsodyRuntimeException
**Type:** System
**Priority:** High
**Description:**
This test verifies end-to-end that when a wrapper method invokes a fake COM object that
raises `pywintypes.com_error`, the error is translated by `call_com` into a
`RhapsodyRuntimeException` whose message preserves the original COM error text. Callers
never see a raw `pywintypes.com_error`.
**Pre-conditions:**
- A fake `pywintypes` module whose `com_error` is a real exception class (or a stand-in
  configured so `call_com`'s except clause matches).
- A fake COM object whose `getName()` (or similar) raises `pywintypes.com_error` with a
  known message.
- The wrapper registry populated.
**Test Steps:**
1. Wrap the failing fake COM object via `wrap()`.
2. Invoke a wrapper method that delegates to the failing COM method (e.g. `getName()`).
3. Assert that a `RhapsodyRuntimeException` is raised (not `pywintypes.com_error`).
4. Assert the exception message contains the original COM error text.
5. Confirm no raw `pywintypes.com_error` instance escapes the wrapper layer.
**Expected Result:**
- The wrapper method raises `RhapsodyRuntimeException`.
- The exception message preserves the original COM error message.
- No `pywintypes.com_error` instance is visible to the caller.
**Verification Criteria:**
- Pass if `RhapsodyRuntimeException` is raised and its message contains the original COM
  text, and `pytest.raises(RhapsodyRuntimeException)` succeeds while
  `pytest.raises(pywintypes.com_error)` would fail at the wrapper boundary.
- Fail if a raw `com_error` propagates, or if the message is dropped/empty.
**Last Changed:** 2026-07-07

---

## SYTS_CORE_00004: RPModelElement Base Class Equality, Hash, and Repr

**ID:** SYTS_CORE_00004
**Traces-To:** SWR_CORE_00001
**Title:** RPModelElement equality by COM identity, hash, and repr behave correctly
**Type:** System
**Priority:** Medium
**Description:**
This test verifies the `RPModelElement` base class behavior end-to-end through the
wrapper layer: two wrappers around the same COM object compare equal and share a hash;
two wrappers around different COM objects compare unequal; `__repr__` shows the class name
and the element's name. Java-mirrored methods `getName`, `setName`, `getMetaClass`, and
`getGUID` delegate to the COM object.
**Pre-conditions:**
- Two distinct fake COM objects A and B, each returning a known name, meta class, and GUID
  from their respective methods.
- The wrapper registry populated.
**Test Steps:**
1. Wrap COM object A twice (`w1 = wrap(A)`, `w2 = wrap(A)`) and wrap B once (`w3 = wrap(B)`).
2. Assert `w1 == w2` and `hash(w1) == hash(w2)`.
3. Assert `w1 != w3` and `hash(w1) != hash(w3)`.
4. Assert `repr(w1)` contains the wrapper class name and the element's name.
5. Assert `w1.getName()`, `w1.getMetaClass()`, and `w1.getGUID()` return the fake values.
6. Call `w1.setName("new")` and assert the fake COM object's `setName` was called with
   "new".
**Expected Result:**
- Wrappers around the same COM object are equal and hash-equal; wrappers around different
  COM objects are not.
- `repr` includes both the class name and the element name.
- Java-mirrored getters delegate correctly; `setName` delegates to the COM object.
**Verification Criteria:**
- Pass if all equality, hash, repr, and delegation assertions hold.
- Fail if equality falls back to identity of the wrapper (rather than the COM object), or
  if any getter fails to delegate.
**Last Changed:** 2026-07-07

---

## SYTS_CORE_00005: RPUnit Save and File Operations End-to-End

**ID:** SYTS_CORE_00005
**Traces-To:** SWR_CORE_00002
**Title:** RPUnit save, getFilename, setFilename, and readOnly operations translate correctly
**Type:** System
**Priority:** Medium
**Description:**
This test verifies that `RPUnit` exposes save and file operations that delegate to the
fake COM object, and that `setReadOnly` translates Python booleans to COM-style 1/0
integers.
**Pre-conditions:**
- A fake `IRPUnit` COM object with `save()`, `getFilename()`, `setFilename(name)`,
  `isReadOnly()`, and `setReadOnly(int)` methods that record their arguments.
- The wrapper registry populated (Project is an RPUnit subclass).
**Test Steps:**
1. Wrap the fake `IRPUnit` via `wrap()`.
2. Call `getFilename()` and assert it returns the fake's filename.
3. Call `setFilename("new/path.rpy")` and assert the fake received that string.
4. Call `save()` and assert the fake's `save` was called exactly once.
5. Call `setReadOnly(True)` and assert the fake's `setReadOnly` was called with integer 1.
6. Call `setReadOnly(False)` and assert the fake's `setReadOnly` was called with integer 0.
7. Call `isReadOnly()` and assert it returns the fake's stored value.
**Expected Result:**
- All delegations succeed and the fake COM call recorder captures the correct arguments.
- `setReadOnly(True)` -> 1, `setReadOnly(False)` -> 0 (boolean-to-integer translation).
**Verification Criteria:**
- Pass if every call delegates correctly and `setReadOnly` translates booleans to 1/0.
- Fail if any method fails to delegate, or if booleans are passed through untranslated.
**Last Changed:** 2026-07-07

---

## SYTS_CORE_00006: RPCollection Rejects Negative Indices

**ID:** SYTS_CORE_00006
**Traces-To:** SWR_CORE_00009
**Title:** RPCollection raises IndexError for negative indices
**Type:** System
**Priority:** Low
**Description:**
This test verifies that `RPCollection.__getitem__` raises `IndexError` with the message
"negative indices are not supported" when given a negative index, because COM collection
indexing is 1-based and does not support negative indexing.
**Pre-conditions:**
- A fake `IRPCollection` with at least one element.
- An `RPCollection` wrapping it.
**Test Steps:**
1. Wrap the fake collection in an `RPCollection`.
2. Attempt `collection[-1]` and assert `IndexError` is raised.
3. Assert the exception message is exactly "negative indices are not supported".
4. Confirm that a valid positive index (e.g. `collection[1]`) still works after the
   negative-index attempts.
**Expected Result:**
- `collection[-1]` raises `IndexError("negative indices are not supported")`.
- Positive indexing continues to work normally.
**Verification Criteria:**
- Pass if the exact `IndexError` with the specified message is raised for negative
  indices, and positive indexing is unaffected.
- Fail if a negative index returns an element, raises a different exception, or breaks
  subsequent positive indexing.
**Last Changed:** 2026-07-07

---
