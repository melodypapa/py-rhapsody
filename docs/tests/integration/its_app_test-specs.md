# Integration Test Specifications - Application Connection Layer

**Category:** APP
**Prefix:** ITS
**Test Type:** Integration
**Last Validated:** 2026-07-07

---

## ITS_APP_00001: Connect with attach-first fallback to launch

**ID:** ITS_APP_00001
**Traces-To:** SWR_APP_00001, SWR_APP_00002, SWR_APP_00003
**Title:** connect(prefer_attach=True) falls back from attach() to launch() when no instance is running
**Type:** Integration
**Priority:** High
**Description:**
Verifies the integration between `RhapsodyApplication.attach`, `RhapsodyApplication.launch`, and
`RhapsodyApplication.connect`. When `prefer_attach=True` (default) and no running Rhapsody
instance exists, `attach()` raises `RhapsodyConnectionError`, and `connect()` must catch that
specific exception and fall through to `launch()`, returning a `RhapsodyApplication` whose `_com`
points to the launched instance.
**Pre-conditions:**
- `win32com.client.GetActiveObject` is patched to raise `pywintypes.com_error` (no active instance).
- `win32com.client.Dispatch` is patched to return a mock COM application object.
- `RhapsodyApplication` class is importable from `rhapsody_cli.application`.
**Test Steps:**
1. Call `RhapsodyApplication.connect(prefer_attach=True)`.
2. Assert that `attach()` was attempted first (i.e., `GetActiveObject` was invoked once with `"Rhapsody.Application"`).
3. Assert that the returned object is a `RhapsodyApplication` instance whose `_com` is the mock returned by `Dispatch`.
4. Assert that no `RhapsodyConnectionError` propagated out of `connect()`.
**Expected Result:**
`connect()` swallows the `RhapsodyConnectionError` from the failed `attach()` and returns a
`RhapsodyApplication` wrapping the COM object produced by `launch()`.
**Verification Criteria:**
- Returned object `isinstance` of `RhapsodyApplication`.
- `GetActiveObject` called exactly once before `Dispatch`.
- `Dispatch` called exactly once with `"Rhapsody.Application"`.
- No exception escapes the call.
**Last Changed:** 2026-07-07

---

## ITS_APP_00002: openProject returns wrapped RPProject and translates COM errors

**ID:** ITS_APP_00002
**Traces-To:** SWR_APP_00004, SWR_APP_00009
**Title:** openProject(path) returns an RPProject wrapper; COM failures surface as RhapsodyRuntimeException
**Type:** Integration
**Priority:** High
**Description:**
Verifies the integration between `RhapsodyApplication.openProject`, the `wrap()` factory, and the
`RPProject` wrapper. On success, the raw COM project returned by the underlying
`openProject` call must be passed through `wrap()` and yield an `RPProject` instance. When the
COM call raises `pywintypes.com_error`, the error must cross the `call_com` boundary as a
`RhapsodyRuntimeException` preserving the original message.
**Pre-conditions:**
- A `RhapsodyApplication` instance whose `_com.openProject` is patched.
- `rhapsody_cli.models.elements` is imported so the wrapper registry is populated.
- A mock COM project object whose `getMetaClass()` returns `"Project"`.
**Test Steps:**
1. Patch `_com.openProject` to return the mock COM project; call `app.openProject("model.rpy")`.
2. Assert the return value is an `RPProject` instance and its `_com` is the mock project.
3. Patch `_com.openProject` to raise `pywintypes.com_error("file not found", 0, "missing")`.
4. Call `app.openProject("missing.rpy")` and assert `RhapsodyRuntimeException` is raised.
5. Assert the raised exception's message contains the original COM error text.
**Expected Result:**
Success path yields a properly wrapped `RPProject`; failure path raises
`RhapsodyRuntimeException` (never raw `pywintypes.com_error`) with the COM message preserved.
**Verification Criteria:**
- `isinstance(result, RPProject)` on success.
- `RhapsodyRuntimeException` raised on COM failure; no `pywintypes.com_error` leaks.
- Exception message string contains the original COM detail.
**Last Changed:** 2026-07-07

---

## ITS_APP_00003: activeProject returns wrapped RPProject from current selection

**ID:** ITS_APP_00003
**Traces-To:** SWR_APP_00005, SWR_APP_00009
**Title:** activeProject() returns the currently active project as a wrapped RPProject
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies that `RhapsodyApplication.activeProject` reads `_com.activeProject` and routes the result
through `wrap()`, producing an `RPProject` wrapper. Confirms the application layer integrates with
the wrapping machinery rather than returning raw COM objects to callers.
**Pre-conditions:**
- A `RhapsodyApplication` instance whose `_com.activeProject` is patched to return a mock COM
  project with `getMetaClass() == "Project"`.
- `rhapsody_cli.models.elements` imported (registry populated).
**Test Steps:**
1. Patch `_com.activeProject` to return the mock COM project.
2. Call `app.activeProject()`.
3. Assert the returned object is an `RPProject`.
4. Assert the wrapper's `_com` attribute is the same mock project returned by the COM property.
**Expected Result:**
`activeProject()` returns a fully wrapped `RPProject`; the underlying COM object is preserved on
the wrapper's `_com`.
**Verification Criteria:**
- `isinstance(result, RPProject)` is True.
- `result._com is mock_project` is True.
**Last Changed:** 2026-07-07

---

## ITS_APP_00004: getProjects returns RPCollection of wrapped RPProject items

**ID:** ITS_APP_00004
**Traces-To:** SWR_APP_00006, SWR_CORE_00003, SWR_CORE_00007
**Title:** getProjects() returns an RPCollection whose iteration yields RPProject wrappers
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies integration between `RhapsodyApplication.getProjects`, `RPCollection`, and `wrap()`/
`_wrap_if_element`. The COM collection returned by `_com.getProjects()` must be wrapped as an
`RPCollection`, and iterating it must auto-wrap each raw COM project as an `RPProject`.
**Pre-conditions:**
- A `RhapsodyApplication` whose `_com.getProjects` is patched to return a mock `IRPCollection`.
- The mock collection's `getCount()` returns 2 and `getItem(i)` returns two distinct mock COM
  project objects whose `getMetaClass()` returns `"Project"`.
- `rhapsody_cli.models.elements` imported (registry populated).
**Test Steps:**
1. Call `app.getProjects()`.
2. Assert the return value is an `RPCollection`.
3. Iterate the result and collect items into a list.
4. Assert the list has length 2 and every item is an `RPProject`.
5. Assert each item's `_com` matches the corresponding mock returned by `getItem`.
**Expected Result:**
`getProjects()` returns an `RPCollection`; iteration transparently wraps each raw COM project as
`RPProject` via `_wrap_if_element`/`wrap`.
**Verification Criteria:**
- `isinstance(result, RPCollection)` is True.
- `len(result) == 2`.
- All iterated items are `RPProject` instances.
- Order of `_com` matches `getItem(1)`, `getItem(2)`.
**Last Changed:** 2026-07-07

---

## ITS_APP_00005: Multiple RhapsodyApplication instances manage separate COM objects

**ID:** ITS_APP_00005
**Traces-To:** SWR_APP_00008, SWR_APP_00002
**Title:** Two RhapsodyApplication instances wrap independent COM objects without global singleton coupling
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the no-singleton requirement by constructing two `RhapsodyApplication` instances from
two distinct mock COM objects and confirming that operations on one (e.g., `quit`) do not affect
the other, and that `openProject` on each routes to its own `_com`.
**Pre-conditions:**
- Two independent mock COM application objects `mock_a` and `mock_b`, each with its own
  `openProject` and `quit` spies.
- `RhapsodyApplication` imported.
**Test Steps:**
1. Construct `app_a = RhapsodyApplication(mock_a)` and `app_b = RhapsodyApplication(mock_b)`.
2. Patch `mock_a.openProject` to return a mock project; call `app_a.openProject("a.rpy")`.
3. Assert `mock_b.openProject` was NOT called.
4. Call `app_b.quit()`; assert `mock_b.quit` was called once and `mock_a.quit` was NOT called.
5. Assert `app_a._com is mock_a` and `app_b._com is mock_b` (distinct COM objects).
**Expected Result:**
Each `RhapsodyApplication` instance wraps exactly one COM object independently; calls on one
instance never bleed into the other.
**Verification Criteria:**
- `app_a._com is not app_b._com`.
- `mock_a.openProject` called exactly once; `mock_b.openProject` never called.
- `mock_b.quit` called exactly once; `mock_a.quit` never called.
**Last Changed:** 2026-07-07

---

## ITS_APP_00006: attach failure raises RhapsodyConnectionError consumed by CLI flow

**ID:** ITS_APP_00006
**Traces-To:** SWR_APP_00001, SWR_EXC_00002, SWR_CLI_00004
**Title:** attach() raising RhapsodyConnectionError is observable to CLI project open flow
**Type:** Integration
**Priority:** High
**Description:**
Verifies cross-layer integration: when `attach()` cannot find a running instance it raises
`RhapsodyConnectionError`; the CLI's `project open` command (when configured NOT to fall back to
launch) must observe this exception, write the message to stderr, and abort. This bridges the
application layer, the exceptions module, and the CLI command layer.
**Pre-conditions:**
- `win32com.client.GetActiveObject` patched to raise `pywintypes.com_error`.
- `win32com.client.Dispatch` patched to ALSO raise (simulate no Rhapsody installed).
- A `click.testing.CliRunner` instance.
- The `project open` CLI command wired with a context whose `connect` uses attach-only.
**Test Steps:**
1. Invoke `project open` with `project_path` pointing to a real temp file via `CliRunner.invoke`.
2. Capture the `Result` object's `output` and `exit_code`.
3. Assert `exit_code != 0` (aborted).
4. Assert stderr/stdout contains the `RhapsodyConnectionError` message text.
5. Assert no `RPProject` was constructed (i.e., `openProject` was never reached).
**Expected Result:**
The attach failure surfaces as `RhapsodyConnectionError`, the CLI command catches it, writes the
message to stderr, and aborts with a non-zero exit code. No raw `pywintypes.com_error` reaches
the CLI surface.
**Verification Criteria:**
- `result.exit_code != 0`.
- Error message text present in `result.output` or captured stderr.
- `RhapsodyApplication.openProject` never invoked.
**Last Changed:** 2026-07-07

---

## ITS_APP_00007: quit() terminates the wrapped COM instance

**ID:** ITS_APP_00007
**Traces-To:** SWR_APP_00007
**Title:** quit() delegates to the underlying COM object's quit method exactly once
**Type:** Integration
**Priority:** Low
**Description:**
Verifies that `RhapsodyApplication.quit` invokes `quit()` on the wrapped COM object exactly once,
completing the application lifecycle integration. After `quit()`, the `RhapsodyApplication`
instance may still hold a reference to the (now-terminated) COM object but must not re-invoke
`quit` on subsequent accidental calls unless explicitly re-driven.
**Pre-conditions:**
- A `RhapsodyApplication` whose `_com.quit` is a spy that records call count.
**Test Steps:**
1. Call `app.quit()`.
2. Assert `_com.quit` was called exactly once.
3. (Optional) Call `app.quit()` a second time and assert the spy count increments to 2 (pure
   delegation, no idempotency guard required by spec).
**Expected Result:**
`quit()` is a thin delegation to `_com.quit`; each call to the wrapper produces exactly one call
on the underlying COM object.
**Verification Criteria:**
- After first `quit()`: `_com.quit.call_count == 1`.
- After second `quit()`: `_com.quit.call_count == 2`.
**Last Changed:** 2026-07-07

---
