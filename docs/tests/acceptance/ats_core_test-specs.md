# Acceptance Test Specifications - Wrapping Machinery

**Category:** CORE
**Prefix:** ATS
**Test Type:** Acceptance
**Last Validated:** 2026-07-07

---

## ATS_CORE_00001: Navigate a Model Element via Name, Meta Class, and GUID

**ID:** ATS_CORE_00001
**Traces-To:** SWR_CORE_00001
**Title:** Read identity and metadata of a wrapped model element
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to query a wrapped Rhapsody model element's name, meta class,
and GUID, so that I can identify elements and write navigation logic that branches on
element type.
**Acceptance Criteria:**
- Given any wrapped `RPModelElement` (e.g., an `RPClass` returned from `addClass`), When I
  call `getName()`, Then the string returned matches the name used to create the element.
- Given any wrapped `RPModelElement`, When I call `getMetaClass()`, Then the string
  returned matches the Rhapsody meta-class name (e.g., `"Class"`, `"Package"`,
  `"Operation"`).
- Given any wrapped `RPModelElement`, When I call `getGUID()`, Then a non-empty GUID
  string is returned and is stable across repeated calls for the same element.
- Given two references to the same underlying element, When I compare them with `==`, Then
  they are equal; and `repr(element)` produces a string showing the wrapper class name and
  the element name.
**Verification Criteria:**
Open a fixture project, obtain a class via `package.addClass("Demo")`, and assert
`element.getName() == "Demo"`, `element.getMetaClass() == "Class"`, and that
`element.getGUID()` is a non-empty string equal on two consecutive calls. Re-fetch the
same element via a collection and assert `fetched == element`. Assert
`"Demo" in repr(element)` and `"RPClass" in repr(element)` (or the relevant class name).
**Last Changed:** 2026-07-07

---

## ATS_CORE_00002: Save a Unit and Manage File Metadata

**ID:** ATS_CORE_00002
**Traces-To:** SWR_CORE_00002
**Title:** Save a unit and read/write its file metadata and read-only flag
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to save a unit (project, package, or class that owns its own
file) and inspect or change its filename and read-only state, so that I can persist model
edits and control file-level locking.
**Acceptance Criteria:**
- Given a wrapped `RPUnit` (e.g., an `RPProject` or `RPPackage`), When I call
  `unit.save()`, Then the underlying Rhapsody unit is written to disk and no exception is
  raised.
- Given a wrapped `RPUnit`, When I call `unit.getFilename()`, Then the path string of the
  unit's backing file is returned; and after `setFilename(new_path)` the next
  `getFilename()` returns `new_path`.
- Given a wrapped `RPUnit`, When I call `unit.isReadOnly()`, Then a boolean is returned;
  and after `unit.setReadOnly(True)` the next `isReadOnly()` returns `True` (and
  `setReadOnly(False)` flips it back).
**Verification Criteria:**
Open a writable fixture project, modify a package (e.g., add a class), call
`package.save()`, and assert no exception is raised. Capture
`project.getFilename()` before and after `setFilename` to a new temp path and assert the
value changes. Call `setReadOnly(True)` and assert `isReadOnly()` returns `True`; call
`setReadOnly(False)` and assert it returns `False`. Confirm the bool-to-int translation
happens internally (no `TypeError` from passing a Python `bool`).
**Last Changed:** 2026-07-07

---

## ATS_CORE_00003: Iterate RPCollections Pythonically

**ID:** ATS_CORE_00003
**Traces-To:** SWR_CORE_00003, SWR_CORE_00007
**Title:** Iterate, len, and index Rhapsody collections using Python protocols
**Type:** Acceptance
**Priority:** High
**Description:**
As a Python developer, I want to iterate over an `RPCollection` with a `for` loop, query
its length with `len()`, and index it with `[]`, so that I can write idiomatic Python
navigation code instead of Java-style `getCount`/`getItem` loops.
**Acceptance Criteria:**
- Given an `RPCollection` returned from a method like `package.getNestedElements()`, When
  I write `for x in collection:`, Then each yielded `x` is auto-wrapped (e.g., an
  `RPClass`, `RPPackage`, etc.) and the loop visits every element exactly once.
- Given an `RPCollection` with N items, When I call `len(collection)`, Then the integer
  returned equals N (matching `getCount()`).
- Given an `RPCollection` with at least one item, When I call `collection[1]`, Then the
  first item is returned (1-based COM indexing) and is auto-wrapped via `_wrap_if_element`.
- Given an `RPCollection` containing non-element values (e.g., strings), When I iterate,
  Then those values are returned unchanged (not wrapped), while element-like values are
  wrapped.
**Verification Criteria:**
Add three classes (`A`, `B`, `C`) to a package, then iterate `package.getClasses()` (or
the equivalent nested-elements collection) and assert the collected names are exactly
`{"A", "B", "C"}` with no duplicates. Assert `len(collection) == 3 == collection.getCount()`.
Assert `collection[1].getName() == "A"`. Iterate a second time to confirm the iterator is
reusable. If any non-element value is present in a collection, assert it is returned
verbatim by `_wrap_if_element`.
**Last Changed:** 2026-07-07

---

## ATS_CORE_00004: See RhapsodyRuntimeException (Not Raw COM Errors) on COM Failures

**ID:** ATS_CORE_00004
**Traces-To:** SWR_CORE_00004, SWR_CORE_00010
**Title:** COM errors are translated to RhapsodyRuntimeException with preserved messages
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want any failure in an underlying COM call to surface as a
`RhapsodyRuntimeException` carrying the original COM message, so that I can catch a
single, well-typed exception instead of leaking `pywintypes.com_error` into my code.
**Acceptance Criteria:**
- Given a wrapper method that performs a COM call which fails, When the failure is a
  `pywintypes.com_error`, Then the caller observes a `RhapsodyRuntimeException` whose
  message contains the original COM error text.
- Given the same scenario, When I inspect the exception type, Then it is never
  `pywintypes.com_error` (raw COM errors are never raised through the public API).
- Given a non-Windows platform where `pywintypes` is unavailable, When the module is
  imported, Then the import succeeds (no `ImportError`) and non-COM exceptions are
  re-raised unchanged.
**Verification Criteria:**
Force a COM failure (e.g., call `openProject` on a non-existent file, or call a method on
an element whose backing COM object has been deleted) and assert the raised exception is
an instance of `RhapsodyRuntimeException` and not `pywintypes.com_error`, and that
`str(exc)` contains the underlying COM message. On a non-Windows platform (or with
`pywintypes` made unavailable), assert `import rhapsody_cli.models._core` succeeds and
that a non-COM exception (e.g., `ValueError`) raised inside a `call_com` callable is
re-raised unchanged.
**Last Changed:** 2026-07-07

---

## ATS_CORE_00005: Wrap Dispatches Correctly and Falls Back for Unmapped Types

**ID:** ATS_CORE_00005
**Traces-To:** SWR_CORE_00005, SWR_CORE_00006, SWR_CORE_00008
**Title:** wrap() returns the correct wrapper class, or a generic RPModelElement for unmapped types
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want `wrap()` to hand me the most specific Python wrapper for any
Rhapsody COM object, and to never crash on element types that do not yet have a dedicated
wrapper, so that navigation code keeps working across the whole model.
**Acceptance Criteria:**
- Given a raw COM object whose `getMetaClass()` returns `"Class"`, When I call
  `wrap(com_obj)`, Then an `RPClass` instance is returned.
- Given a raw COM object whose `getMetaClass()` returns `"Package"`, When I call
  `wrap(com_obj)`, Then an `RPPackage` instance is returned.
- Given a raw COM object whose `getMetaClass()` returns a value not present in the wrapper
  registry (e.g., an obscure or future element type), When I call `wrap(com_obj)`, Then a
  generic `RPModelElement` is returned (no exception raised) and the caller can still call
  `getName()`, `getMetaClass()`, and `getGUID()` on it.
- Given a new wrapper class and a single `register_wrapper("Foo", RPFoo)` call, When I
  subsequently call `wrap()` on a COM object whose meta class is `"Foo"`, Then an `RPFoo`
  is returned (extensibility without modifying `wrap()` itself).
**Verification Criteria:**
After importing `rhapsody_cli.models.elements`, obtain raw COM objects of known types
(`Class`, `Package`, `Operation`) and assert `wrap()` returns instances of the
corresponding wrapper classes. Construct or obtain a COM object whose meta class is
guaranteed not to be in the registry (e.g., a rarely-used type, or a mock whose
`getMetaClass()` returns `"__test_unknown__"`) and assert `wrap()` returns an
`RPModelElement` instance without raising. Then call
`register_wrapper("__test_unknown__", RPModelElement)` and assert `wrap()` returns the
newly registered class.
**Last Changed:** 2026-07-07

---

## ATS_CORE_00006: Negative Indexing of RPCollections Is Rejected

**ID:** ATS_CORE_00006
**Traces-To:** SWR_CORE_00009
**Title:** RPCollection raises IndexError for negative indices
**Type:** Acceptance
**Priority:** Low
**Description:**
As a Python developer, I want `RPCollection` to reject negative indices with a clear
`IndexError`, so that I am not silently surprised by the mismatch between Python's
negative indexing and COM's 1-based indexing.
**Acceptance Criteria:**
- Given a non-empty `RPCollection`, When I call `collection[-1]`, Then an `IndexError` is
  raised whose message is `"negative indices are not supported"`.
- Given a non-empty `RPCollection`, When I call `collection[-N]` for any negative N, Then
  the same `IndexError` is raised (regardless of magnitude).
- Given a non-empty `RPCollection` with N items, When I call `collection[1]` and
  `collection[N]`, Then valid positive indices still work as expected (1-based).
**Verification Criteria:**
Obtain an `RPCollection` with at least one element. Assert that `collection[-1]` raises
`IndexError` with the exact message `"negative indices are not supported"`. Assert that
`collection[-999]` raises the same `IndexError`. Assert that `collection[1]` returns the
first item and (if the collection has N >= 2 items) `collection[N]` returns the last item,
confirming positive indexing still works after the negative-index guard.
**Last Changed:** 2026-07-07
