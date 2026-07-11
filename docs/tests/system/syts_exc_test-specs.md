# System Test Specifications - Exceptions

**Category:** EXC
**Prefix:** SYTS
**Test Type:** System
**Last Validated:** 2026-07-07

---

## SYTS_EXC_00001: COM Failure Surfaces as RhapsodyRuntimeException End-to-End

**ID:** SYTS_EXC_00001
**Traces-To:** SWR_EXC_00001, SWR_EXC_00004
**Title:** A COM error raised inside a wrapper method surfaces as RhapsodyRuntimeException
**Type:** System
**Priority:** High
**Description:**
This test verifies end-to-end error propagation: when a wrapper method's underlying COM
call raises `pywintypes.com_error`, the shared `call_com` helper translates it into a
`RhapsodyRuntimeException` whose message preserves the original COM error text. The
caller (CLI or direct wrapper consumer) never sees a raw `pywintypes.com_error`.
**Pre-conditions:**
- A fake `pywintypes.com_error` exception class installed in `sys.modules` (or a stand-in
  matching `call_com`'s except clause).
- A fake COM object whose `getName()` raises `pywintypes.com_error("hresult 0x80004005:
  access denied")`.
- The wrapper registry populated via `rhapsody_cli.models.elements` import.
**Test Steps:**
1. Wrap the failing fake COM object via `wrap()`.
2. Invoke `wrapper.getName()` and assert `RhapsodyRuntimeException` is raised.
3. Assert the exception message contains the original COM error text (e.g. "access
   denied" or the hresult string).
4. Confirm that the raised exception is NOT an instance of `pywintypes.com_error` (the
   caller sees only `RhapsodyRuntimeException`).
5. Repeat the call through a CLI command path (e.g. `element view`) and confirm the CLI
   writes the error to stderr and aborts non-zero rather than leaking a traceback.
**Expected Result:**
- `wrapper.getName()` raises `RhapsodyRuntimeException` with the original COM message
  preserved.
- The raised exception is not a `pywintypes.com_error` instance.
- The CLI path writes the error to stderr and exits non-zero.
**Verification Criteria:**
- Pass if `RhapsodyRuntimeException` is raised with the original message, it is not a
  `com_error` instance, and the CLI aborts non-zero with stderr output.
- Fail if a raw `com_error` propagates, the message is dropped, or the CLI exits 0.
**Last Changed:** 2026-07-07

---

## SYTS_EXC_00002: Connection Failure Surfaces as RhapsodyConnectionError and CLI Aborts

**ID:** SYTS_EXC_00002
**Traces-To:** SWR_EXC_00002, SWR_EXC_00003
**Title:** Attach/launch failure raises RhapsodyConnectionError and CLI aborts non-zero
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end connection-failure path: when both `attach()` and
`launch()` fail against the fake COM layer, `RhapsodyApplication.connect()` raises
`RhapsodyConnectionError` with a descriptive message, and the CLI surfaces this to stderr
and aborts with a non-zero exit code.
**Pre-conditions:**
- A fake `win32com.client.GetActiveObject` that raises `pythoncom.com_error` (no running
  instance).
- A fake `win32com.client.Dispatch` that raises `pythoncom.com_error` (cannot launch).
- CliRunner available; the `cli` entry point importable.
**Test Steps:**
1. Configure the fake COM layer so both `GetActiveObject` and `Dispatch` raise
   com_error.
2. Invoke `rhapsody project open <temp_path>` via CliRunner.
3. Capture stdout, stderr, and exit code.
4. Independently call `RhapsodyApplication.connect()` directly and assert it raises
   `RhapsodyConnectionError`.
5. Assert the exception message describes the failure (contains "No running Rhapsody
   instance found" or "Failed to launch Rhapsody instance").
**Expected Result:**
- The direct `connect()` call raises `RhapsodyConnectionError` with a descriptive
  message.
- The CLI invocation exits non-zero (exit code 1 for `click.Abort`).
- Stderr contains a connection-failure description; stdout has no success message.
**Verification Criteria:**
- Pass if `RhapsodyConnectionError` is raised by `connect()`, the CLI exits non-zero, and
  stderr contains the failure description.
- Fail if the CLI exits 0, no error is written to stderr, or a different exception type
  is raised.
**Last Changed:** 2026-07-07

---

## SYTS_EXC_00003: Exceptions Public API - Importable from Top-Level Package

**ID:** SYTS_EXC_00003
**Traces-To:** SWR_EXC_00003
**Title:** Both exception classes importable from rhapsody_cli top-level and exceptions package
**Type:** System
**Priority:** Medium
**Description:**
This test verifies the public API surface end-to-end: both `RhapsodyConnectionError` and
`RhapsodyRuntimeException` are importable from the top-level `rhapsody_cli` package and
from `rhapsody_cli.exceptions`, and both appear in `rhapsody_cli.exceptions.__all__`. This
is verified by performing the imports in a fresh process-like context.
**Pre-conditions:**
- The `rhapsody_cli` package installed/importable.
- A clean import context (or the test re-imports the package modules).
**Test Steps:**
1. Execute `from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`
   and assert neither import raises.
2. Execute
   `from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException`
   and assert neither import raises.
3. Inspect `rhapsody_cli.exceptions.__all__` and assert it contains both class names.
4. Assert both classes are `Exception` subclasses.
5. Assert the two classes are distinct (not aliases of each other).
**Expected Result:**
- Both imports succeed without error.
- `__all__` contains exactly the two exception class names (at minimum).
- Both classes subclass `Exception`.
- `RhapsodyConnectionError is not RhapsodyRuntimeException`.
**Verification Criteria:**
- Pass if all import and isinstance assertions hold and the two classes are distinct.
- Fail if either import raises `ImportError`, either class is missing from `__all__`, or
  the two classes are the same object.
**Last Changed:** 2026-07-07

---

## SYTS_EXC_00004: All Wrapper COM Calls Funnel Through call_com End-to-End

**ID:** SYTS_EXC_00004
**Traces-To:** SWR_EXC_00004, SWR_EXC_00001
**Title:** Wrapper methods across element types consistently raise RhapsodyRuntimeException
**Type:** System
**Priority:** High
**Description:**
This test verifies that all wrapper methods that invoke the underlying COM object funnel
errors through the shared `call_com` helper, so a `pywintypes.com_error` raised by any
fake COM method consistently surfaces as `RhapsodyRuntimeException`. The test samples
methods across multiple element wrapper types (Project, Package, Class, Attribute,
Operation, Diagram) to confirm consistent funneling.
**Pre-conditions:**
- A fake `pywintypes.com_error` exception class.
- Fake COM objects for each sampled element type whose methods raise
  `pywintypes.com_error` with distinct known messages.
- The wrapper registry populated.
**Test Steps:**
1. For each sampled wrapper type (RPProject, RPPackage, RPClass, RPAttribute,
   RPOperation, RPDiagram), wrap the corresponding failing fake COM object.
2. Invoke at least one COM-delegating method on each wrapper (e.g. `getName()`,
   `getPackages()`, `addAttribute("x")`, `getMultiplicity()`, `getBody()`,
   `closeDiagram()`).
3. For each invocation, assert `RhapsodyRuntimeException` is raised (not
   `pywintypes.com_error`).
4. Assert each exception message preserves the corresponding fake COM error message.
5. Confirm no invocation leaks a raw `pywintypes.com_error` to the caller.
**Expected Result:**
- Every sampled COM-delegating method raises `RhapsodyRuntimeException`.
- Each exception message matches the fake COM error message configured for that method.
- No raw `pywintypes.com_error` instance is visible to the caller across any sampled
  type.
**Verification Criteria:**
- Pass if all sampled methods raise `RhapsodyRuntimeException` with the correct
  preserved message and none leak a raw `com_error`.
- Fail if any sampled method raises `pywintypes.com_error` directly, raises a different
  exception type, or drops the original message.
**Last Changed:** 2026-07-07
