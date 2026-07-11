# Unit Test Specifications - Exceptions

**Category:** EXC
**Prefix:** UTS
**Test Type:** Unit
**Last Validated:** 2026-07-07

---

## UTS_EXC_00001: RhapsodyRuntimeException Is an Exception Subclass

**ID:** UTS_EXC_00001
**Traces-To:** SWR_EXC_00001
**Title:** RhapsodyRuntimeException subclasses Exception and can be raised/caught
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RhapsodyRuntimeException` is a subclass of `Exception`, can be raised with a single string argument, and is catchable by `except Exception` and `except RhapsodyRuntimeException`.
**Pre-conditions:**
- `RhapsodyRuntimeException` importable from `rhapsody_cli.exceptions`.
**Test Steps:**
1. Import `RhapsodyRuntimeException`.
2. Assert `issubclass(RhapsodyRuntimeException, Exception)`.
3. Inside a `try` block, `raise RhapsodyRuntimeException("boom")`.
4. Catch with `except RhapsodyRuntimeException as exc` and inspect `str(exc)`.
5. Confirm the same raise is also caught by a bare `except Exception`.
**Expected Result:**
`issubclass` returns `True`; the raised exception's `str()` is `"boom"`; both `except RhapsodyRuntimeException` and `except Exception` catch it.
**Verification Criteria:**
Pass if all assertions hold and `str(exc) == "boom"`.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00002: RhapsodyRuntimeException Preserves the COM Error Message

**ID:** UTS_EXC_00002
**Traces-To:** SWR_EXC_00001
**Title:** RhapsodyRuntimeException carries the original COM error text as its message
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `call_com` translates a `pywintypes.com_error` into a `RhapsodyRuntimeException`, the original COM error message/HRESULT text is preserved as the exception message (i.e., `str(exc)` contains the original error text).
**Pre-conditions:**
- `tests.fakes.make_com_error("HRESULT 0x8...")` produces a `pywintypes.com_error`.
- A callable `failing = MagicMock(side_effect=com_error)`.
**Test Steps:**
1. Call `call_com(failing)` inside `assertRaises(RhapsodyRuntimeException)`.
2. Capture the raised exception.
3. Assert `str(exc)` contains the substring `"HRESULT 0x8..."`.
4. Assert `exc.__cause__ is com_error` (the original error is chained).
**Expected Result:**
The `RhapsodyRuntimeException` message contains the original COM error text; `__cause__` is the original `com_error`.
**Verification Criteria:**
Pass if both the message-substring and `__cause__` assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00003: RhapsodyConnectionError Is an Exception Subclass

**ID:** UTS_EXC_00003
**Traces-To:** SWR_EXC_00002
**Title:** RhapsodyConnectionError subclasses Exception and is distinct from RhapsodyRuntimeException
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RhapsodyConnectionError` is a subclass of `Exception`, can be raised and caught, and is NOT a subclass of `RhapsodyRuntimeException` (the two are independent exception types).
**Pre-conditions:**
- Both exception classes importable from `rhapsody_cli.exceptions`.
**Test Steps:**
1. Import `RhapsodyConnectionError` and `RhapsodyRuntimeException`.
2. Assert `issubclass(RhapsodyConnectionError, Exception)`.
3. Assert `not issubclass(RhapsodyConnectionError, RhapsodyRuntimeException)`.
4. Assert `not issubclass(RhapsodyRuntimeException, RhapsodyConnectionError)`.
5. Inside a `try` block, `raise RhapsodyConnectionError("no instance")`.
6. Catch with `except RhapsodyConnectionError as exc` and assert `str(exc) == "no instance"`.
**Expected Result:**
`RhapsodyConnectionError` is an `Exception` subclass, distinct from `RhapsodyRuntimeException`, and carries its message as `str(exc)`.
**Verification Criteria:**
Pass if all `issubclass`/`not issubclass` assertions hold and the caught exception's message matches.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00004: RhapsodyConnectionError Raised by attach and launch

**ID:** UTS_EXC_00004
**Traces-To:** SWR_EXC_00002
**Title:** attach() and launch() raise RhapsodyConnectionError with descriptive prefixed messages
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `RhapsodyApplication.attach()` fails it raises `RhapsodyConnectionError` with a message beginning `"No running Rhapsody instance found:"`, and when `launch()` fails it raises `RhapsodyConnectionError` with a message beginning `"Failed to launch Rhapsody instance:"`. Both messages include the underlying detail.
**Pre-conditions:**
- `win32com.client.GetActiveObject` patched to raise `tests.fakes.make_com_error("not found")`.
- `win32com.client.Dispatch` patched to raise `tests.fakes.make_com_error("cannot start")`.
**Test Steps:**
1. Patch `GetActiveObject` to raise the `com_error`; call `RhapsodyApplication.attach()` inside `assertRaises(RhapsodyConnectionError)`; capture the exception.
2. Assert `str(exc).startswith("No running Rhapsody instance found:")` and that `"not found"` is in `str(exc)`.
3. Patch `Dispatch` to raise the `com_error`; call `RhapsodyApplication.launch()` inside `assertRaises(RhapsodyConnectionError)`; capture the exception.
4. Assert `str(exc).startswith("Failed to launch Rhapsody instance:")` and that `"cannot start"` is in `str(exc)`.
**Expected Result:**
`attach()` raises `RhapsodyConnectionError` with the attach-specific prefix and the original detail; `launch()` raises `RhapsodyConnectionError` with the launch-specific prefix and the original detail.
**Verification Criteria:**
Pass if all four assertions (two prefix checks and two detail-substring checks) hold.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00005: exceptions Package Exports Both Classes via __all__

**ID:** UTS_EXC_00005
**Traces-To:** SWR_EXC_00003
**Title:** rhapsody_cli.exceptions.__init__ exports both exception classes via __all__
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that the `rhapsody_cli.exceptions` package `__init__.py` defines `__all__` containing exactly `"RhapsodyConnectionError"` and `"RhapsodyRuntimeException"`, and that both names are attributes of the package.
**Pre-conditions:**
- `rhapsody_cli.exceptions` imported.
**Test Steps:**
1. Import the `rhapsody_cli.exceptions` package.
2. Inspect `rhapsody_cli.exceptions.__all__`.
3. Assert `set(rhapsody_cli.exceptions.__all__) == {"RhapsodyConnectionError", "RhapsodyRuntimeException"}`.
4. Assert `getattr(rhapsody_cli.exceptions, "RhapsodyConnectionError") is RhapsodyConnectionError`.
5. Assert `getattr(rhapsody_cli.exceptions, "RhapsodyRuntimeException") is RhapsodyRuntimeException`.
**Expected Result:**
`__all__` is exactly the two expected names; both are accessible as package attributes pointing at the correct classes.
**Verification Criteria:**
Pass if the `__all__` set equality holds and both `getattr` checks succeed.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00006: Top-Level Package Re-exports Both Exception Classes

**ID:** UTS_EXC_00006
**Traces-To:** SWR_EXC_00003
**Title:** from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException works
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that both exception classes are re-exported from the top-level `rhapsody_cli` package, so users can import them directly as `from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`.
**Pre-conditions:**
- `rhapsody_cli` imported.
**Test Steps:**
1. Execute `from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`.
2. Assert the imported `RhapsodyConnectionError` is the same class as `rhapsody_cli.exceptions.RhapsodyConnectionError`.
3. Assert the imported `RhapsodyRuntimeException` is the same class as `rhapsody_cli.exceptions.RhapsodyRuntimeException`.
4. Assert both are subclasses of `Exception`.
**Expected Result:**
Both names import without error from the top-level package and refer to the same classes as the `exceptions` subpackage.
**Verification Criteria:**
Pass if the import succeeds and both identity and subclass assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00007: call_com Funnels com_error to RhapsodyRuntimeException

**ID:** UTS_EXC_00007
**Traces-To:** SWR_EXC_00004
**Title:** call_com translates pywintypes.com_error into RhapsodyRuntimeException for all callers
**Type:** Unit
**Priority:** High
**Description:**
Verifies the funneling contract: any callable passed to `call_com` that raises a `pywintypes.com_error` results in a `RhapsodyRuntimeException`, and callers never observe a raw `pywintypes.com_error` from `call_com`.
**Pre-conditions:**
- `tests.fakes.make_com_error("funnel fail")` produces a `pywintypes.com_error`.
- A callable `failing = MagicMock(side_effect=com_error)`.
**Test Steps:**
1. Call `call_com(failing)` inside a `try/except`.
2. Catch `RhapsodyRuntimeException` and assert it was raised.
3. Explicitly assert that the raw `pywintypes.com_error` is NOT the raised type (i.e., a separate `except pywintypes.com_error` clause would not catch it).
4. Inspect `exc.__cause__` to confirm the original `com_error` is chained.
**Expected Result:**
`RhapsodyRuntimeException` is raised (not `pywintypes.com_error`); the original `com_error` is preserved as `__cause__`.
**Verification Criteria:**
Pass if `RhapsodyRuntimeException` is the raised type, `pywintypes.com_error` is not caught at the same level, and `exc.__cause__ is com_error`.
**Last Changed:** 2026-07-07

---

## UTS_EXC_00008: Wrapper Methods Funnel COM Errors Through call_com

**ID:** UTS_EXC_00008
**Traces-To:** SWR_EXC_00004
**Title:** Wrapper methods that invoke COM raise RhapsodyRuntimeException on com_error, never raw com_error
**Type:** Unit
**Priority:** High
**Description:**
Verifies the end-to-end funneling contract at the wrapper layer: a representative wrapper method (e.g., `RPModelElement.getName()` or `RPClass.addClass(name)`) raises `RhapsodyRuntimeException` (not `pywintypes.com_error`) when the underlying COM object raises a `pywintypes.com_error`.
**Pre-conditions:**
- A fake COM element built via `tests.fakes.make_fake_element("Class")` with `getName.side_effect = tests.fakes.make_com_error("getName failed")` and `addClass.side_effect = tests.fakes.make_com_error("addClass failed")`.
- An `RPModelElement` and an `RPClass` wrapping that fake.
**Test Steps:**
1. Construct `el = RPModelElement(fake)` and `cls = RPClass(fake)`.
2. Call `el.getName()` inside `assertRaises(RhapsodyRuntimeException)`; assert `"getName failed"` is in `str(exc)`.
3. Call `cls.addClass("X")` inside `assertRaises(RhapsodyRuntimeException)`; assert `"addClass failed"` is in `str(exc)`.
4. In both cases, confirm a parallel `except pywintypes.com_error` clause would NOT have caught the exception.
**Expected Result:**
Both wrapper methods raise `RhapsodyRuntimeException` carrying the original COM error text; no raw `pywintypes.com_error` escapes the wrapper layer.
**Verification Criteria:**
Pass if both `assertRaises(RhapsodyRuntimeException)` blocks trigger, the messages contain the original text, and raw `com_error` is not the raised type.
**Last Changed:** 2026-07-07
