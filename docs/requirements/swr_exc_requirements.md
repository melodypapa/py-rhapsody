# Software Requirements - EXC (Exceptions)

**Category:** EXC
**Prefix:** SWR
**Source:** Extracted from code
**Last Validated:** 2026-07-07

---

## SWR_EXC_00001: RhapsodyRuntimeException

**ID:** SWR_EXC_00001
**Title: RhapsodyRuntimeException mirrors the Java API exception of the same name
**Status:** Implemented
**Priority:** High
**Description:**
`RhapsodyRuntimeException` shall be an `Exception` subclass that mirrors
`com.telelogic.rhapsody.core.RhapsodyRuntimeException` from the Java API. It shall be
raised by wrapper methods when the underlying COM call raises a
`pywintypes.com_error`. The original COM error message/HRESULT text shall be preserved
as the exception message for diagnostics.
**Implementation:** src/rhapsody_cli/exceptions/core.py:RhapsodyRuntimeException
**Last Changed:** 2026-07-07

---

## SWR_EXC_00002: RhapsodyConnectionError

**ID:** SWR_EXC_00002
**Title: RhapsodyConnectionError is raised when attach/launch fails
**Status:** Implemented
**Priority:** High
**Description:**
`RhapsodyConnectionError` shall be an `Exception` subclass specific to `rhapsody_cli`
(not present in the Java API). It shall be raised when `RhapsodyApplication.attach()` or
`RhapsodyApplication.launch()` cannot find or start a Rhapsody instance. The exception
message shall describe the failure (e.g., `"No running Rhapsody instance found: {detail}"`
or `"Failed to launch Rhapsody instance: {detail}"`).
**Implementation:** src/rhapsody_cli/exceptions/core.py:RhapsodyConnectionError
**Last Changed:** 2026-07-07

---

## SWR_EXC_00003: Exceptions Public API

**ID:** SWR_EXC_00003
**Title: exceptions package exports both exception classes
**Status:** Implemented
**Priority:** Medium
**Description:**
The `rhapsody_cli.exceptions` package `__init__.py` shall export `RhapsodyConnectionError`
and `RhapsodyRuntimeException` via `__all__`, and both shall also be re-exported from the
top-level `rhapsody_cli` package so users can import them as
`from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`.
**Implementation:** src/rhapsody_cli/exceptions/__init__.py
**Last Changed:** 2026-07-07

---

## SWR_EXC_00004: COM Error Funneling

**ID:** SWR_EXC_00004
**Title: All wrapper COM calls funnel errors through call_com to RhapsodyRuntimeException
**Status:** Implemented
**Priority:** High
**Description:**
All wrapper method calls that invoke the underlying COM object shall funnel COM errors
through the shared `call_com` helper, which translates `pywintypes.com_error` into
`RhapsodyRuntimeException`. Callers shall never see raw `pywintypes.com_error`.
**Implementation:** src/rhapsody_cli/models/_core.py:call_com
**Last Changed:** 2026-07-07
