# Unit Test Specifications - Wrapping Machinery

**Category:** CORE
**Prefix:** UTS
**Test Type:** Unit
**Last Validated:** 2026-07-07

---

## UTS_CORE_00001: RPModelElement Stores Exactly One _com Attribute

**ID:** UTS_CORE_00001
**Traces-To:** SWR_CORE_00001
**Title:** RPModelElement.__init__ stores the COM object as _com and nothing else
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RPModelElement(com_obj)` stores `com_obj` as the single attribute `_com` and exposes no other instance-level state beyond what the class defines.
**Pre-conditions:**
- A fake COM object built via `tests.fakes.make_fake_element("Class", getName="Foo")`.
**Test Steps:**
1. Construct `el = RPModelElement(fake)`.
2. Assert `el._com is fake`.
3. Inspect `el.__dict__`.
**Expected Result:**
`el._com is fake` and `el.__dict__` is exactly `{"_com": fake}`.
**Verification Criteria:**
Pass if `_com` is the supplied fake and `__dict__` contains no other keys.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00002: RPModelElement Delegates getName/setName/getMetaClass/getGUID

**ID:** UTS_CORE_00002
**Traces-To:** SWR_CORE_00001
**Title:** RPModelElement accessor methods delegate to the underlying COM object
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `getName()`, `getMetaClass()`, and `getGUID()` return `str(...)` of the COM method results, and `setName(name)` calls the COM `setName` with the given name.
**Pre-conditions:**
- A fake COM object via `tests.fakes.make_fake_element("Class", getName="Foo", getGUID="{abc}")` (the helper already configures `getMetaClass`).
**Test Steps:**
1. Construct `el = RPModelElement(fake)`.
2. Call `el.getName()`, `el.getMetaClass()`, `el.getGUID()`.
3. Call `el.setName("Bar")`.
4. Inspect `fake.getName`, `fake.getMetaClass`, `fake.getGUID`, `fake.setName` call records.
**Expected Result:**
`getName()` returns `"Foo"`; `getMetaClass()` returns `"Class"`; `getGUID()` returns `"{abc}"`; `setName("Bar")` results in `fake.setName` being called once with `"Bar"`.
**Verification Criteria:**
Pass if all returned strings match and `fake.setName.call_args == call("Bar")`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00003: RPModelElement Equality, Hash, and Repr

**ID:** UTS_CORE_00003
**Traces-To:** SWR_CORE_00001
**Title:** RPModelElement __eq__/__hash__/__repr__ behave per COM identity and name
**Type:** Unit
**Priority:** High
**Description:**
Verifies that two `RPModelElement` instances wrapping the same COM object compare equal and have equal hashes; instances wrapping different COM objects are not equal; `__repr__` shows the class name and `getName()` value; equality against a non-`RPModelElement` returns `NotImplemented`.
**Pre-conditions:**
- Two distinct fake COM objects `fake_a` and `fake_b` built via `tests.fakes.make_fake_element("Class", getName="Foo")`.
**Test Steps:**
1. Construct `el1 = RPModelElement(fake_a)` and `el2 = RPModelElement(fake_a)` and `el3 = RPModelElement(fake_b)`.
2. Assert `el1 == el2` and `hash(el1) == hash(el2)`.
3. Assert `el1 != el3`.
4. Assert `repr(el1) == "RPModelElement(name='Foo')"`.
5. Assert `el1.__eq__(42) is NotImplemented`.
**Expected Result:**
Same-COM wrappers are equal with equal hashes; different-COM wrappers are unequal; repr is `"RPModelElement(name='Foo')"`; non-`RPModelElement` comparison returns `NotImplemented`.
**Verification Criteria:**
Pass if all five assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00004: RPUnit Save and File Operations

**ID:** UTS_CORE_00004
**Traces-To:** SWR_CORE_00002
**Title:** RPUnit.save/getFilename/setFilename/isReadOnly/setReadOnly delegate to COM
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RPUnit` exposes `save()`, `getFilename()`, `setFilename(filename)`, `isReadOnly()`, and `setReadOnly(read_only)`, all delegating to the underlying COM object. Verifies `setReadOnly(True)` calls COM with `1` and `setReadOnly(False)` calls COM with `0`.
**Pre-conditions:**
- A fake COM unit built via `tests.fakes.make_fake_element("Unit", getFilename="C:/x.rpy", isReadOnly=1)`.
**Test Steps:**
1. Construct `unit = RPUnit(fake)`.
2. Call `unit.save()`, `unit.getFilename()`, `unit.isReadOnly()`.
3. Call `unit.setFilename("C:/y.rpy")`.
4. Call `unit.setReadOnly(True)` and `unit.setReadOnly(False)`.
5. Inspect call records on `fake.save`, `fake.getFilename`, `fake.isReadOnly`, `fake.setFilename`, `fake.setReadOnly`.
**Expected Result:**
`getFilename()` returns `"C:/x.rpy"`; `isReadOnly()` returns `True` (because `bool(1)` is True); `setReadOnly(True)` calls COM `setReadOnly(1)`; `setReadOnly(False)` calls COM `setReadOnly(0)`; `setFilename("C:/y.rpy")` is forwarded verbatim.
**Verification Criteria:**
Pass if all returned values match and `fake.setReadOnly` was called with `1` then `0`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00005: RPCollection getCount/getItem/addItem Delegate to COM

**ID:** UTS_CORE_00005
**Traces-To:** SWR_CORE_00003
**Title:** RPCollection.getCount/getItem/addItem delegate to the underlying IRPCollection
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RPCollection` exposes `getCount()`, `getItem(index)`, and `addItem(element)`, with `addItem` unwrapping the supplied `RPModelElement` and passing its `_com` to the COM `addItem`.
**Pre-conditions:**
- A fake collection built via `tests.fakes.make_fake_collection([fake_elem_a, fake_elem_b])` where each `fake_elem_*` is built via `make_fake_element`.
**Test Steps:**
1. Construct `coll = RPCollection(fake_coll)`.
2. Call `coll.getCount()` and assert it returns `2`.
3. Call `coll.getItem(1)` and assert it returns a wrapped element.
4. Construct `wrapper = RPModelElement(fake_elem_c)` and call `coll.addItem(wrapper)`.
5. Inspect `fake_coll.addItem` call args.
**Expected Result:**
`getCount()` returns `2`; `getItem(1)` returns a wrapped `RPModelElement` (auto-wrapped by `_wrap_if_element`) whose `_com` is `fake_elem_a`; `addItem(wrapper)` calls `fake_coll.addItem` with `fake_elem_c` (the unwrapped `_com`).
**Verification Criteria:**
Pass if counts/values match and `fake_coll.addItem.call_args == call(fake_elem_c)`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00006: RPCollection Python Protocols len/getitem/iter

**ID:** UTS_CORE_00006
**Traces-To:** SWR_CORE_00003
**Title:** RPCollection __len__/__getitem__/__iter__ use 1-based COM indexing
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `len(coll)` returns `getCount()`; `coll[i]` translates 0-based Python indices to 1-based COM indices via `getItem(index + 1)`; iterating yields each auto-wrapped item in order.
**Pre-conditions:**
- A fake collection built via `tests.fakes.make_fake_collection([fake_a, fake_b, fake_c])` (three fake elements, each with `getMetaClass` so they auto-wrap).
**Test Steps:**
1. Construct `coll = RPCollection(fake_coll)`.
2. Assert `len(coll) == 3`.
3. Assert `coll[0]._com is fake_a` and `coll[2]._com is fake_c` (0-based Python indexing).
4. Iterate `list(coll)` and assert each yielded item is a wrapped `RPModelElement` whose `_com` matches the order `fake_a, fake_b, fake_c`.
**Expected Result:**
`len` returns `3`; `coll[0]` corresponds to `getItem(1)`; iteration yields the three wrapped items in order.
**Verification Criteria:**
Pass if `len(coll) == 3`, `coll[0]._com is fake_a`, `coll[2]._com is fake_c`, and the iterated list has length 3 with matching `_com` references in order.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00007: RPCollection getitem Wraps Items via _wrap_if_element

**ID:** UTS_CORE_00007
**Traces-To:** SWR_CORE_00003
**Title:** RPCollection.getItem auto-wraps elements that expose getMetaClass
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `getItem` passes its return value through `_wrap_if_element`, so collection members that look like Rhapsody elements come back as wrapped `RPModelElement` instances (or subclasses), while non-element values come back unchanged.
**Pre-conditions:**
- A fake collection built with one element-like object (a `MagicMock` with `getMetaClass`) and one plain value (e.g., the integer `42`).
**Test Steps:**
1. Build `fake_coll = make_fake_collection([fake_elem, 42])`.
2. Construct `coll = RPCollection(fake_coll)`.
3. Call `coll.getItem(1)` and assert the result is an `RPModelElement` subclass instance.
4. Call `coll.getItem(2)` and assert the result is the integer `42` unchanged.
**Expected Result:**
The element-like item is wrapped; the plain integer is returned as-is.
**Verification Criteria:**
Pass if `isinstance(coll.getItem(1), RPModelElement)` and `coll.getItem(2) is 42`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00008: call_com Translates com_error to RhapsodyRuntimeException

**ID:** UTS_CORE_00008
**Traces-To:** SWR_CORE_00004
**Title:** call_com re-raises pywintypes.com_error as RhapsodyRuntimeException preserving the message
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `call_com(func)` invokes `func`, returns its result on success, and on `pywintypes.com_error` re-raises as `RhapsodyRuntimeException` with `str(exc)` of the original error as the message and the original error as `__cause__`.
**Pre-conditions:**
- `tests.fakes.make_com_error("boom")` produces a `pywintypes.com_error`.
- A callable `failing = MagicMock(side_effect=com_error)`.
- A callable `ok = MagicMock(return_value=42)`.
**Test Steps:**
1. Call `call_com(ok)` and assert it returns `42`.
2. Call `call_com(failing)` inside `assertRaises(RhapsodyRuntimeException)`.
3. Inspect the raised exception's message and `__cause__`.
**Expected Result:**
Success path returns `42`. Failure path raises `RhapsodyRuntimeException` whose message contains `"boom"` and whose `__cause__` is the original `com_error`.
**Verification Criteria:**
Pass if `call_com(ok) == 42`, `RhapsodyRuntimeException` is raised on the failing callable, `str(exc)` contains `"boom"`, and `exc.__cause__ is com_error`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00009: call_com Reraises Non-COM Exceptions Unchanged

**ID:** UTS_CORE_00009
**Traces-To:** SWR_CORE_00004
**Title:** call_com re-raises non-COM exceptions unchanged without wrapping
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `func` raises an exception that is not a `pywintypes.com_error` (e.g., a `ValueError`), `call_com` re-raises it unchanged and does NOT translate it into `RhapsodyRuntimeException`.
**Pre-conditions:**
- A callable `failing = MagicMock(side_effect=ValueError("not a com error"))`.
**Test Steps:**
1. Call `call_com(failing)` inside `assertRaises(ValueError)`.
2. Inspect the raised exception type and message.
**Expected Result:**
A `ValueError` (not `RhapsodyRuntimeException`) is raised with message `"not a com error"`.
**Verification Criteria:**
Pass if the raised exception is exactly a `ValueError` (not a `RhapsodyRuntimeException`) and its message is `"not a com error"`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00010: wrap Returns Correct Wrapper for Registered Meta Class

**ID:** UTS_CORE_00010
**Traces-To:** SWR_CORE_00005
**Title:** wrap() returns the wrapper class registered for the COM object's meta class
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `wrap(com_obj)` reads `com_obj.getMetaClass()`, looks up the wrapper class in the registry, and returns an instance of that class wrapping `com_obj`.
**Pre-conditions:**
- A fake COM object via `make_fake_element("Class")` (the `"Class"` meta class is registered to `RPClass` once `rhapsody_cli.models.elements` is imported).
- The `rhapsody_cli.models.elements` package imported so the registry is populated.
**Test Steps:**
1. Import `rhapsody_cli.models.elements` to populate the registry.
2. Build `fake = make_fake_element("Class")`.
3. Call `wrap(fake)`.
4. Inspect the type and `_com` of the result.
**Expected Result:**
The result is an `RPClass` instance whose `_com` is `fake`.
**Verification Criteria:**
Pass if `isinstance(result, RPClass)` and `result._com is fake`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00011: wrap Never Crashes on Unmapped Meta Class

**ID:** UTS_CORE_00011
**Traces-To:** SWR_CORE_00005
**Title:** wrap() returns a generic RPModelElement for an unmapped meta class without raising
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `wrap()` does not raise when given a COM object whose `getMetaClass()` is not in the registry, and instead returns a generic `RPModelElement`.
**Pre-conditions:**
- A fake COM object via `make_fake_element("SomeUnknownType")`.
- (Optional) Save and restore `_WRAPPER_REGISTRY` so the test cannot be polluted by other registrations.
**Test Steps:**
1. Build `fake = make_fake_element("SomeUnknownType")`.
2. Call `wrap(fake)`.
3. Inspect the type and `_com` of the result.
**Expected Result:**
No exception is raised. The result is an `RPModelElement` (exactly that class, not a subclass) whose `_com` is `fake`.
**Verification Criteria:**
Pass if `type(result) is RPModelElement` and `result._com is fake`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00012: register_wrapper Populates the Registry

**ID:** UTS_CORE_00012
**Traces-To:** SWR_CORE_00006
**Title:** register_wrapper(meta_class, wrapper_cls) maps the meta class string to the wrapper class
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `register_wrapper("Foo", FooWrapper)` stores `FooWrapper` under `"Foo"` in `_WRAPPER_REGISTRY`, so a subsequent `wrap()` of a COM object with `getMetaClass() == "Foo"` returns a `FooWrapper`.
**Pre-conditions:**
- A clean or saved snapshot of `_WRAPPER_REGISTRY` to restore after the test.
- A trivial `FooWrapper(RPModelElement)` subclass defined for the test.
**Test Steps:**
1. Save the current `_WRAPPER_REGISTRY` state.
2. Define `class FooWrapper(RPModelElement): pass`.
3. Call `register_wrapper("Foo", FooWrapper)`.
4. Assert `_WRAPPER_REGISTRY["Foo"] is FooWrapper`.
5. Build `fake = make_fake_element("Foo")` and call `wrap(fake)`.
6. Restore the original registry.
**Expected Result:**
After `register_wrapper`, `_WRAPPER_REGISTRY["Foo"] is FooWrapper`, and `wrap(fake)` returns a `FooWrapper` instance whose `_com` is `fake`.
**Verification Criteria:**
Pass if the registry entry is set and `wrap()` returns the registered subclass.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00013: register_wrapper Supports Adding New Types Without Changing wrap

**ID:** UTS_CORE_00013
**Traces-To:** SWR_CORE_00006
**Title:** Adding support for a new element type requires only a wrapper class plus one register_wrapper call
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the extensibility contract: after defining a new wrapper subclass and calling `register_wrapper` once, `wrap()` dispatches to the new class with no other code changes.
**Pre-conditions:**
- A snapshot of `_WRAPPER_REGISTRY` to restore.
- A `FakeNewType` wrapper subclass for the test.
**Test Steps:**
1. Confirm `"NewType"` is not already in `_WRAPPER_REGISTRY`.
2. Define `class FakeNewType(RPModelElement): pass`.
3. Call `register_wrapper("NewType", FakeNewType)`.
4. Build `fake = make_fake_element("NewType")` and call `wrap(fake)`.
5. Restore the original registry.
**Expected Result:**
`wrap(fake)` returns a `FakeNewType` instance. No modification to `wrap` itself was required.
**Verification Criteria:**
Pass if `isinstance(result, FakeNewType)` and `result._com is fake`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00014: _wrap_if_element Wraps Element-Like Values

**ID:** UTS_CORE_00014
**Traces-To:** SWR_CORE_00007
**Title:** _wrap_if_element wraps values exposing getMetaClass and passes through others
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `_wrap_if_element(value)` returns `wrap(value)` when `value` has a `getMetaClass` attribute, and returns `value` unchanged otherwise.
**Pre-conditions:**
- A fake element built via `make_fake_element("Class")`.
- A plain Python value (e.g., the string `"hello"`).
**Test Steps:**
1. Call `_wrap_if_element(fake_elem)` and inspect the type.
2. Call `_wrap_if_element("hello")` and inspect the result.
3. Call `_wrap_if_element(42)` and inspect the result.
**Expected Result:**
The fake element is wrapped into an `RPModelElement` subclass; `"hello"` and `42` are returned unchanged.
**Verification Criteria:**
Pass if `isinstance(_wrap_if_element(fake_elem), RPModelElement)`, `_wrap_if_element("hello") == "hello"`, and `_wrap_if_element(42) == 42`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00015: Registry Fallback Returns RPModelElement for Unmapped Meta Class

**ID:** UTS_CORE_00015
**Traces-To:** SWR_CORE_00008
**Title:** wrap() falls back to RPModelElement when the meta class is absent from the registry
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the navigation-safety guarantee: a COM object whose `getMetaClass()` returns a string not present in `_WRAPPER_REGISTRY` is wrapped as a generic `RPModelElement` (exactly that class), so navigation code keeps working for element types without a dedicated wrapper.
**Pre-conditions:**
- A fake COM object via `make_fake_element("ObscureType")`.
- Confirm `"ObscureType"` is not a key in `_WRAPPER_REGISTRY`.
**Test Steps:**
1. Build `fake = make_fake_element("ObscureType")`.
2. Call `wrap(fake)`.
3. Inspect `type(result)` and `result._com`.
**Expected Result:**
`type(result) is RPModelElement` (the base class, not a subclass) and `result._com is fake`. No exception is raised.
**Verification Criteria:**
Pass if `type(result) is RPModelElement` and `result._com is fake`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00016: RPCollection Rejects Negative Indices

**ID:** UTS_CORE_00016
**Traces-To:** SWR_CORE_00009
**Title:** RPCollection.__getitem__ raises IndexError with a specific message for negative indices
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that `RPCollection.__getitem__(-1)` (and any negative index) raises `IndexError` with the message `"negative indices are not supported"`, because COM collection indexing is 1-based.
**Pre-conditions:**
- A fake collection built via `tests.fakes.make_fake_collection([fake_a])`.
**Test Steps:**
1. Construct `coll = RPCollection(fake_coll)`.
2. Call `coll[-1]` inside `assertRaises(IndexError)`.
3. Inspect the exception message.
4. (Boundary) Call `coll[-100]` and confirm the same `IndexError` is raised.
**Expected Result:**
Both `coll[-1]` and `coll[-100]` raise `IndexError` with message exactly `"negative indices are not supported"`. `fake_coll.getItem` is never called.
**Verification Criteria:**
Pass if `IndexError` is raised for both negative indices, the message equals the expected string, and `fake_coll.getItem.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00017: RPCollection getitem Boundary at Zero Index

**ID:** UTS_CORE_00017
**Traces-To:** SWR_CORE_00009
**Title:** RPCollection.__getitem__(0) translates to COM getItem(1) and does not raise
**Type:** Unit
**Priority:** Low
**Description:**
Verifies the boundary between negative-index rejection (covered by SWR_CORE_00009) and valid 0-based indexing: index `0` is treated as the first element (translated to COM `getItem(1)`) rather than rejected as a negative index.
**Pre-conditions:**
- A fake collection built via `tests.fakes.make_fake_collection([fake_a, fake_b])`.
**Test Steps:**
1. Construct `coll = RPCollection(fake_coll)`.
2. Call `coll[0]` and inspect the result and the recorded call to `fake_coll.getItem`.
**Expected Result:**
`coll[0]._com is fake_a` and `fake_coll.getItem` was called once with the integer `1`.
**Verification Criteria:**
Pass if `coll[0]._com is fake_a` and `fake_coll.getItem.call_args == call(1)`.
**Last Changed:** 2026-07-07

---

## UTS_CORE_00018: pywintypes Optional Import Does Not Break Module Import

**ID:** UTS_CORE_00018
**Traces-To:** SWR_CORE_00010
**Title:** The _core module sets pywintypes to None when the import fails and remains importable
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that the `pywintypes` import is wrapped in try/except so the module remains importable when `pywintypes` is unavailable, in which case `pywintypes` is bound to `None` at module scope.
**Pre-conditions:**
- The test patches `sys.modules` (or uses `importlib`) so that importing `pywintypes` raises `ImportError`, simulating a non-Windows platform.
- Access to `rhapsody_cli.models._core` after a forced re-import.
**Test Steps:**
1. Block the `pywintypes` module (e.g., insert a finder that raises `ImportError` for `pywintypes`).
2. Force a re-import of `rhapsody_cli.models._core`.
3. Inspect the `pywintypes` attribute on the re-imported module.
4. Confirm that `call_com` on a callable raising a non-COM `ValueError` still re-raises the `ValueError` unchanged (no `AttributeError` from `pywintypes is None`).
**Expected Result:**
The module imports without error; `_core.pywintypes is None`; `call_com` on a `ValueError`-raising callable re-raises the `ValueError` unchanged.
**Verification Criteria:**
Pass if the re-import succeeds, `_core.pywintypes is None`, and a non-COM exception is re-raised unchanged.
**Last Changed:** 2026-07-07

---
