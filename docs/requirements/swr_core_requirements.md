# Software Requirements - CORE (Wrapping Machinery)

**Category:** CORE
**Prefix:** SWR
**Source:** Extracted from code
**Last Validated:** 2026-07-07

---

## SWR_CORE_00001: RPModelElement Base Class

**ID:** SWR_CORE_00001
**Title:** RPModelElement wraps IRPModelElement as the base for all model elements
**Status:** Implemented
**Priority:** High
**Description:**
`RPModelElement` shall be the base class for every wrapped Rhapsody model element,
mirroring `com.telelogic.rhapsody.core.IRPModelElement`. It shall store exactly one
attribute, `_com`, holding the raw COM object. It shall expose Java-mirrored methods
`getName()`, `setName(name)`, `getMetaClass()`, and `getGUID()` that delegate to the
underlying COM object. It shall implement `__eq__` (COM object equality), `__hash__`
(by COM object identity), and `__repr__` (showing class name and name).
**Implementation:** src/rhapsody_cli/models/_core.py:RPModelElement
**Last Changed:** 2026-07-07

---

## SWR_CORE_00002: RPUnit Save and File Operations

**ID:** SWR_CORE_00002
**Title:** RPUnit wraps IRPUnit for elements that can be saved as separate files
**Status:** Implemented
**Priority:** High
**Description:**
`RPUnit` shall extend `RPModelElement` to wrap `IRPUnit` (model elements that can be
saved as separate files). It shall expose Java-mirrored methods: `save()`,
`getFilename()`, `setFilename(filename)`, `isReadOnly()`, and
`setReadOnly(read_only)`. The `setReadOnly` method shall translate Python booleans to
COM-style integers (1/0).
**Implementation:** src/rhapsody_cli/models/_core.py:RPUnit
**Last Changed:** 2026-07-07

---

## SWR_CORE_00003: RPCollection Iterable Container

**ID:** SWR_CORE_00003
**Title:** RPCollection wraps IRPCollection as an iterable/indexable container
**Status:** Implemented
**Priority:** High
**Description:**
`RPCollection` shall wrap `IRPCollection` and expose Java-mirrored methods `getCount()`,
`getItem(index)`, and `addItem(element)`. It shall also support Python protocols:
`__len__` (returns `getCount()`), `__getitem__` (1-based COM indexing via `getItem`,
raising `IndexError` for negative indices), and `__iter__` (yields each item
auto-wrapped via `wrap()`). Items returned by `getItem` shall be auto-wrapped via
`_wrap_if_element`.
**Implementation:** src/rhapsody_cli/models/_core.py:RPCollection
**Last Changed:** 2026-07-07

---

## SWR_CORE_00004: call_com Error Translation

**ID:** SWR_CORE_00004
**Title:** call_com translates COM errors into RhapsodyRuntimeException
**Status:** Implemented
**Priority:** High
**Description:**
The `call_com(func)` helper shall invoke a COM-callable and return its result. If the
call raises a `pywintypes.com_error`, it shall be re-raised as
`RhapsodyRuntimeException` with the original message preserved. On non-Windows
platforms where `pywintypes` is unavailable, non-COM exceptions shall be re-raised
unchanged. Callers shall never see raw `pywintypes.com_error`.
**Implementation:** src/rhapsody_cli/models/_core.py:call_com
**Last Changed:** 2026-07-07

---

## SWR_CORE_00005: wrap Factory Function

**ID:** SWR_CORE_00005
**Title:** wrap dispatches a raw COM object to its matching wrapper class
**Status:** Implemented
**Priority:** High
**Description:**
The `wrap(com_obj)` factory function shall inspect the underlying Rhapsody element's
runtime type via `getMetaClass()` and return the correct Python wrapper instance. Type
resolution shall be driven by a registry dict mapping Rhapsody type names to wrapper
classes. `wrap()` shall never crash on an unmapped type; unmapped types shall fall back
to a generic `RPModelElement` wrapper.
**Implementation:** src/rhapsody_cli/models/_core.py:wrap
**Last Changed:** 2026-07-07

---

## SWR_CORE_00006: register_wrapper Registry

**ID:** SWR_CORE_00006
**Title:** register_wrapper populates the meta-class to wrapper-class registry
**Status:** Implemented
**Priority:** High
**Description:**
The `register_wrapper(meta_class, wrapper_cls)` function shall register `wrapper_cls`
as the wrapper for COM objects whose `getMetaClass()` returns `meta_class`. Each
element module shall call `register_wrapper` at import time to populate the registry.
Adding support for a new Rhapsody element type shall require only one wrapper class
plus one registry entry, with no changes to `wrap()` itself.
**Implementation:** src/rhapsody_cli/models/_core.py:register_wrapper
**Last Changed:** 2026-07-07

---

## SWR_CORE_00007: _wrap_if_element Helper

**ID:** SWR_CORE_00007
**Title:** _wrap_if_element wraps values that look like Rhapsody model elements
**Status:** Implemented
**Priority:** Medium
**Description:**
The `_wrap_if_element(value)` helper shall return `wrap(value)` if `value` exposes a
`getMetaClass` attribute (i.e., looks like a Rhapsody model element); otherwise it shall
return `value` unchanged. This is used by `RPCollection.getItem` to auto-wrap collection
members.
**Implementation:** src/rhapsody_cli/models/_core.py:_wrap_if_element
**Last Changed:** 2026-07-07

---

## SWR_CORE_00008: Registry Fallback to RPModelElement

**ID:** SWR_CORE_00008
**Title:** Unmapped meta classes fall back to generic RPModelElement wrapper
**Status:** Implemented
**Priority:** Medium
**Description:**
When `wrap()` encounters a COM object whose `getMetaClass()` is not present in the
wrapper registry, it shall return a generic `RPModelElement` instance rather than
raising an error. This guarantees navigation code keeps working for element types that
do not yet have a dedicated wrapper class.
**Implementation:** src/rhapsody_cli/models/_core.py:wrap
**Last Changed:** 2026-07-07

---

## SWR_CORE_00009: Negative Index Rejection

**ID:** SWR_CORE_00009
**Title:** RPCollection rejects negative indices
**Status:** Implemented
**Priority:** Low
**Description:**
`RPCollection.__getitem__` shall raise `IndexError("negative indices are not supported")`
when given a negative index, because COM collection indexing is 1-based and does not
support negative indexing.
**Implementation:** src/rhapsody_cli/models/_core.py:RPCollection.__getitem__
**Last Changed:** 2026-07-07

---

## SWR_CORE_00010: pywintypes Optional Import

**ID:** SWR_CORE_00010
**Title:** pywintypes import is optional on non-Windows platforms
**Status:** Implemented
**Priority:** Low
**Description:**
The `pywintypes` import shall be wrapped in a try/except so that on non-Windows
platforms `pywintypes` is set to `None` rather than raising `ImportError`. This allows
the module to be imported on non-Windows systems (where no live COM connection can
occur) without error.
**Implementation:** src/rhapsody_cli/models/_core.py
**Last Changed:** 2026-07-07
