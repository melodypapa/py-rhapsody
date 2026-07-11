# Acceptance Test Specifications - Exceptions

**Category:** EXC
**Prefix:** ATS
**Test Type:** Acceptance
**Last Validated:** 2026-07-07

---

## ATS_EXC_00001: See RhapsodyRuntimeException on COM Call Failures

**ID:** ATS_EXC_00001
**Traces-To:** SWR_EXC_00001, SWR_EXC_00004
**Title:** Wrapper COM failures surface as RhapsodyRuntimeException with preserved messages
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want any failure in an underlying COM call made by a wrapper method
to surface as a `RhapsodyRuntimeException` carrying the original COM message, so that I
can catch a single, well-typed exception in my scripts and read the underlying cause.
**Acceptance Criteria:**
- Given a wrapper method (e.g., `openProject`, `addClass`, `getName`) that performs a COM
  call which raises `pywintypes.com_error`, When the call is made, Then the caller
  observes a `RhapsodyRuntimeException` whose message contains the original COM error
  text/HRESULT description.
- Given the same scenario, When I inspect the exception type, Then it is never
  `pywintypes.com_error` (raw COM errors never leak through the public API).
- Given `RhapsodyRuntimeException` is raised, When I catch it with
  `except RhapsodyRuntimeException:`, Then the catch succeeds and the exception is also an
  instance of `Exception` (it is a proper `Exception` subclass).
**Verification Criteria:**
Force a COM failure (e.g., call `openProject` on a non-existent path, or call a method on
an element whose backing COM object has been deleted) and assert the raised exception is
an instance of `RhapsodyRuntimeException`, that `str(exc)` is non-empty and contains the
underlying COM message, and that `isinstance(exc, Exception)` is `True`. Assert that
catching only `RhapsodyRuntimeException` is sufficient (i.e., no `pywintypes.com_error`
escapes). Confirm `RhapsodyRuntimeException` is not raised for non-COM failures (those are
re-raised unchanged).
**Last Changed:** 2026-07-07

---

## ATS_EXC_00002: See RhapsodyConnectionError When Attach or Launch Fails

**ID:** ATS_EXC_00002
**Traces-To:** SWR_EXC_00002
**Title:** Connection failures surface as RhapsodyConnectionError with a descriptive message
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want failures to attach to or launch a Rhapsody instance to surface
as a `RhapsodyConnectionError` with a clear message, so that I can distinguish connection
problems from runtime COM problems in my error handling.
**Acceptance Criteria:**
- Given no Rhapsody instance is running, When I call `RhapsodyApplication.attach()`, Then a
  `RhapsodyConnectionError` is raised whose message describes the attach failure (e.g.,
  contains `"No running Rhapsody instance found"`).
- Given Rhapsody cannot be launched (e.g., not installed or COM Dispatch fails), When I
  call `RhapsodyApplication.launch()`, Then a `RhapsodyConnectionError` is raised whose
  message describes the launch failure (e.g., contains
  `"Failed to launch Rhapsody instance"`).
- Given `RhapsodyConnectionError` is raised, When I catch it with
  `except RhapsodyConnectionError:`, Then the catch succeeds and the exception is also an
  instance of `Exception`.
- Given a `RhapsodyConnectionError` and a `RhapsodyRuntimeException` are both raised in
  different scenarios, When I inspect their types, Then they are distinct classes (a
  connection failure is not confused with a runtime COM failure).
**Verification Criteria:**
With no Rhapsody running, call `attach()` and assert the raised exception is a
`RhapsodyConnectionError` whose message mentions the missing running instance. On a
machine without Rhapsody installed (or with Dispatch failing), call `launch()` and assert
a `RhapsodyConnectionError` is raised whose message mentions the launch failure. Confirm
`isinstance(exc, Exception)` is `True` for both. Confirm that a runtime COM failure (e.g.,
`openProject` on a bad path) raises `RhapsodyRuntimeException`, not
`RhapsodyConnectionError`, so the two exception types are distinguishable.
**Last Changed:** 2026-07-07

---

## ATS_EXC_00003: Import Exceptions from the Top-Level Package

**ID:** ATS_EXC_00003
**Traces-To:** SWR_EXC_00003
**Title:** Both exception classes are importable from `rhapsody_cli` and `rhapsody_cli.exceptions`
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a Python developer, I want to import the rhapsody_cli exception classes from the
top-level package, so that my `try/except` blocks can reference them with a short, stable
import path.
**Acceptance Criteria:**
- Given the `rhapsody_cli` package is installed, When I run
  `from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`, Then both
  names are bound to the exception classes without an `ImportError`.
- Given the `rhapsody_cli.exceptions` package, When I run
  `from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException`,
  Then both names are bound to the same classes.
- Given the `rhapsody_cli.exceptions` package, When I inspect `__all__`, Then it lists
  both `"RhapsodyConnectionError"` and `"RhapsodyRuntimeException"`.
- Given the two import paths, When I compare the classes imported from each, Then they are
  the same class objects (not duplicate definitions).
**Verification Criteria:**
In a fresh Python interpreter, run
`from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException` and assert no
exception. Run `from rhapsody_cli.exceptions import ...` and assert the same. Assert
`"RhapsodyConnectionError" in rhapsody_cli.exceptions.__all__` and
`"RhapsodyRuntimeException" in rhapsody_cli.exceptions.__all__`. Assert
`rhapsody_cli.RhapsodyConnectionError is rhapsody_cli.exceptions.RhapsodyConnectionError`
and likewise for `RhapsodyRuntimeException`. Assert both classes are subclasses of
`Exception`.
**Last Changed:** 2026-07-07

---

## ATS_EXC_00004: No Raw pywintypes.com_error Reaches the Caller

**ID:** ATS_EXC_00004
**Traces-To:** SWR_EXC_00004, SWR_EXC_00001
**Title:** All wrapper COM calls funnel errors through call_com to RhapsodyRuntimeException
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want a guarantee that no wrapper method ever raises a raw
`pywintypes.com_error` to my code, so that I can write portable error handling that does
not depend on `pywintypes` being importable on my platform.
**Acceptance Criteria:**
- Given any wrapper method on any element wrapper (`RPProject`, `RPPackage`, `RPClass`,
  `RPOperation`, `RPAttribute`, etc.) that invokes the underlying COM object, When the COM
  call raises `pywintypes.com_error`, Then the error is funneled through `call_com` and
  the caller observes a `RhapsodyRuntimeException`.
- Given the same scenario, When I grep the public API surface for `pywintypes.com_error`
  in raised exceptions, Then no wrapper method raises it directly.
- Given a non-Windows platform where `pywintypes` is `None`, When a non-COM exception
  occurs inside a `call_com` callable, Then that exception is re-raised unchanged (not
  swallowed, not wrapped).
- Given `call_com` is invoked with a callable that returns normally, When it returns, Then
  the original return value is passed through to the caller unchanged.
**Verification Criteria:**
For each wrapper class, force the underlying COM call to fail (e.g., by deleting the
backing element and then calling a method on the stale wrapper, or by passing invalid
arguments that the COM object rejects) and assert the raised exception is an instance of
`RhapsodyRuntimeException` and not `pywintypes.com_error`. On a non-Windows platform (or
with `pywintypes` patched to `None`), pass a callable to `call_com` that raises
`ValueError("boom")` and assert a `ValueError("boom")` is re-raised unchanged. Pass a
callable that returns `42` to `call_com` and assert `42` is returned unchanged. Confirm
via code inspection (or a representative sample) that wrapper methods route COM calls
through `call_com` rather than calling the COM object directly.
**Last Changed:** 2026-07-07
