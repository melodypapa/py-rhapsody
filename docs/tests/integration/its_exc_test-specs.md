# Integration Test Specifications - Exceptions

**Category:** EXC
**Prefix:** ITS
**Test Type:** Integration
**Last Validated:** 2026-07-07

---

## ITS_EXC_00001: COM error funnels through call_com to RhapsodyRuntimeException

**ID:** ITS_EXC_00001
**Traces-To:** SWR_EXC_00001, SWR_EXC_00004, SWR_CORE_00004
**Title:** A pywintypes.com_error raised by a COM callable surfaces as RhapsodyRuntimeException
**Type:** Integration
**Priority:** High
**Description:**
Verifies the core exception-flow contract that ties together the exceptions module, the
`call_com` helper, and any caller that invokes COM. When a COM-callable raises
`pywintypes.com_error`, `call_com` must catch it and re-raise `RhapsodyRuntimeException` whose
message preserves the original COM error text. The caller must never observe the raw
`pywintypes.com_error`.
**Pre-conditions:**
- `rhapsody_cli.models._core` imported (provides `call_com`).
- `rhapsody_cli.exceptions` imported (provides `RhapsodyRuntimeException`).
- `pywintypes` available (Windows) OR `pywintypes.com_error` patched into the module for the
  test.
- A callable `failing()` that raises `pywintypes.com_error("the message", 0x80004005, None, None)`.
**Test Steps:**
1. Call `call_com(failing)`.
2. Assert `RhapsodyRuntimeException` is raised (use `pytest.raises`).
3. Assert the raised exception is NOT an instance of `pywintypes.com_error`.
4. Assert `str(exc)` contains a substring derived from the original COM message (e.g.,
   `"the message"` or the hresult text `"80004005"`).
5. Call `call_com(lambda: 42)` and assert it returns `42` (no false positives on the success
   path).
**Expected Result:**
The COM error is fully translated to `RhapsodyRuntimeException` with the message preserved; the
success path is unaffected.
**Verification Criteria:**
- `pytest.raises(RhapsodyRuntimeException)` succeeds for `failing`.
- `isinstance(exc, pywintypes.com_error)` is False for the raised exception.
- `str(exc)` contains a recognizable substring from the original COM message.
- Success-path callable returns its value unchanged.
**Last Changed:** 2026-07-07

---

## ITS_EXC_00002: attach failure raises RhapsodyConnectionError consumed by CLI

**ID:** ITS_EXC_00002
**Traces-To:** SWR_EXC_00002, SWR_APP_00001, SWR_CLI_00004
**Title:** attach() raising RhapsodyConnectionError flows through the CLI project open command to click.Abort
**Type:** Integration
**Priority:** High
**Description:**
Verifies a cross-layer exception flow: `RhapsodyApplication.attach` cannot find a running instance
and raises `RhapsodyConnectionError`; the CLI `project open` command catches it, echoes the
message to stderr, and aborts via `click.Abort`. This exercises the application → exceptions →
CLI boundary in a single end-to-end path.
**Pre-conditions:**
- `win32com.client.GetActiveObject` patched to raise `pywintypes.com_error` (simulating no running
  instance).
- `win32com.client.Dispatch` patched to ALSO raise (so `connect` cannot fall back to `launch`).
- `click.testing.CliRunner` available.
- A real temp file on disk to satisfy the path validator.
- `rhapsody_cli.cli.main.cli` and `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "open", str(tmp_path)])`.
2. Assert `result.exit_code != 0`.
3. Assert `result.exception` is `click.Abort` (or `SystemAbort`), NOT a raw
   `RhapsodyConnectionError`.
4. Assert the error message text (e.g., `"No running Rhapsody instance found"` or
   `"Failed to launch Rhapsody instance"`) appears in `result.output` or captured stderr.
5. Assert `RhapsodyApplication.openProject` was never called (connection failed before open).
**Expected Result:**
The `RhapsodyConnectionError` is contained inside the command layer, logged to stderr, and
converted to `click.Abort`; the CLI never leaks the raw exception to the test runner.
**Verification Criteria:**
- `result.exit_code != 0`.
- `result.exception` is `click.Abort` (or its subclass), not `RhapsodyConnectionError`.
- Error message text present in output/stderr.
- `openProject` spy call count is 0.
**Last Changed:** 2026-07-07

---

## ITS_EXC_00003: Top-level package re-exports both exception classes

**ID:** ITS_EXC_00003
**Traces-To:** SWR_EXC_00003
**Title:** from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException succeeds
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the public-API integration between `rhapsody_cli.exceptions.__init__` (which exports both
classes via `__all__`) and the top-level `rhapsody_cli.__init__` (which re-exports them). Users
must be able to import both exception classes directly from the top-level package without
navigating into submodules.
**Pre-conditions:**
- A fresh Python interpreter (or a re-import) so `rhapsody_cli` is loaded from clean state.
**Test Steps:**
1. Execute `from rhapsody_cli import RhapsodyConnectionError, RhapsodyRuntimeException`.
2. Assert `RhapsodyConnectionError` is a class and a subclass of `Exception`.
3. Assert `RhapsodyRuntimeException` is a class and a subclass of `Exception`.
4. Assert `RhapsodyConnectionError is not RhapsodyRuntimeException` (distinct classes).
5. Assert both names appear in `rhapsody_cli.__all__` (or are accessible as attributes of
   `rhapsody_cli`).
6. Assert the same objects are accessible via `rhapsody_cli.exceptions.RhapsodyConnectionError`
   (identity, not a duplicate definition).
**Expected Result:**
Both exception classes are reachable from the top-level package and refer to the same class
objects as the ones in `rhapsody_cli.exceptions`.
**Verification Criteria:**
- Top-level import succeeds without `ImportError`.
- Both classes are `Exception` subclasses.
- `rhapsody_cli.RhapsodyConnectionError is rhapsody_cli.exceptions.RhapsodyConnectionError`.
- `rhapsody_cli.RhapsodyRuntimeException is rhapsody_cli.exceptions.RhapsodyRuntimeException`.
**Last Changed:** 2026-07-07

---

## ITS_EXC_00004: Full exception flow from COM error to CLI stderr output

**ID:** ITS_EXC_00004
**Traces-To:** SWR_EXC_00004, SWR_EXC_00001, SWR_CLI_00004, SWR_CORE_00004
**Title:** A COM error during openProject surfaces as RhapsodyRuntimeException and is reported by the CLI
**Type:** Integration
**Priority:** High
**Description:**
Verifies the complete exception pipeline end to end: a `pywintypes.com_error` raised by the
underlying COM `openProject` call is caught by `call_com` and re-raised as
`RhapsodyRuntimeException`; the `RhapsodyApplication.openProject` wrapper does not swallow it; the
CLI `project open` command catches the `RhapsodyRuntimeException`, writes its message to stderr,
and raises `click.Abort`. This is the canonical "wrapper COM calls funnel through call_com" path
exercised through the CLI surface.
**Pre-conditions:**
- `win32com.client.GetActiveObject` patched to return a mock COM app (so `attach` succeeds and
  `connect` does not fall back).
- The mock COM app's `openProject` patched to raise
  `pywintypes.com_error("project corrupted", 0x8000FFFF, None, None)`.
- `click.testing.CliRunner` available.
- A real temp file on disk for the path validator.
- `rhapsody_cli.cli.main.cli` and `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "open", str(tmp_path)])`.
2. Assert `result.exit_code != 0`.
3. Assert `result.exception` is `click.Abort` (or `SystemAbort`), NOT a raw
   `RhapsodyRuntimeException` and NOT a `pywintypes.com_error`.
4. Assert the original COM message text (e.g., `"project corrupted"`) appears in `result.output`
   or captured stderr (proving message preservation across the boundary).
5. Assert (via spy) that `RhapsodyApplication.openProject` was called once with the supplied path.
6. Assert no `RPProject` was constructed (the COM call failed before `wrap()` ran).
**Expected Result:**
The COM error is translated to `RhapsodyRuntimeException` by `call_com`, propagated through
`openProject` unmodified, then caught by the CLI command and reported via `click.Abort` with the
original message intact.
**Verification Criteria:**
- `result.exit_code != 0`.
- `result.exception` is `click.Abort` (or subclass); NOT `RhapsodyRuntimeException` and NOT
  `pywintypes.com_error`.
- Original COM message text present in output/stderr.
- `openProject` spy called exactly once.
**Last Changed:** 2026-07-07

---

## ITS_EXC_00005: launch failure raises RhapsodyConnectionError and connect does not silently retry

**ID:** ITS_EXC_00005
**Traces-To:** SWR_EXC_00002, SWR_APP_00002, SWR_APP_00003
**Title:** When launch() fails, connect() raises RhapsodyConnectionError rather than retrying indefinitely
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the negative path of the connection fallback integration. When `prefer_attach=False` and
`launch()` raises `RhapsodyConnectionError`, `connect()` must propagate that exception to the
caller rather than retrying, falling back further, or returning a partially-constructed
application. Also confirms `prefer_attach=False` skips `attach()` entirely (no `GetActiveObject`
call).
**Pre-conditions:**
- `win32com.client.GetActiveObject` is a spy (to assert non-invocation).
- `win32com.client.Dispatch` patched to raise `pywintypes.com_error` (simulating Rhapsody not
  installed).
- `RhapsodyApplication` imported.
**Test Steps:**
1. Call `RhapsodyApplication.connect(prefer_attach=False)`.
2. Assert `RhapsodyConnectionError` is raised.
3. Assert the exception message contains a substring like `"Failed to launch Rhapsody instance"`.
4. Assert `GetActiveObject` was NOT called (attach was skipped because `prefer_attach=False`).
5. Assert `Dispatch` was called exactly once with `"Rhapsody2.Application.1"`.
6. Assert no `RhapsodyApplication` instance was returned (the exception propagated).
**Expected Result:**
`connect(prefer_attach=False)` attempts only `launch()`; on failure it raises
`RhapsodyConnectionError` with a descriptive message and does not retry or fall back.
**Verification Criteria:**
- `pytest.raises(RhapsodyConnectionError)` succeeds.
- `GetActiveObject.call_count == 0`.
- `Dispatch.call_count == 1` with arg `"Rhapsody2.Application.1"`.
- Exception message contains `"Failed to launch Rhapsody instance"`.
**Last Changed:** 2026-07-07
