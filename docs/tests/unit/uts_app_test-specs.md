# Unit Test Specifications - Application Connection Layer

**Category:** APP
**Prefix:** UTS
**Test Type:** Unit
**Last Validated:** 2026-07-07

---

## UTS_APP_00001: Attach to Running Rhapsody Instance Happy Path

**ID:** UTS_APP_00001
**Traces-To:** SWR_APP_00001
**Title:** attach() returns a RhapsodyApplication wrapping the active COM object
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RhapsodyApplication.attach()` calls `win32com.client.GetActiveObject("Rhapsody2.Application.1")` and returns a `RhapsodyApplication` instance whose `_com` is the object returned by the COM call.
**Pre-conditions:**
- `tests.fakes.make_fake_element("Application")` produces a fake COM application object.
- `win32com.client.GetActiveObject` is patched (e.g., via `unittest.mock.patch`) to return that fake object.
**Test Steps:**
1. Patch `rhapsody_cli.application.win32com.client.GetActiveObject` to return the fake COM object.
2. Call `RhapsodyApplication.attach()`.
3. Inspect the returned instance's `_com` attribute.
**Expected Result:**
A `RhapsodyApplication` instance is returned and its `_com` attribute is the fake COM object returned by `GetActiveObject`. `GetActiveObject` is called exactly once with the string `"Rhapsody2.Application.1"`.
**Verification Criteria:**
Pass if the returned object is a `RhapsodyApplication`, `result._com is fake_app`, and `GetActiveObject` was called once with `"Rhapsody2.Application.1"`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00002: Attach Raises RhapsodyConnectionError When No Instance Running

**ID:** UTS_APP_00002
**Traces-To:** SWR_APP_00001
**Title:** attach() raises RhapsodyConnectionError when GetActiveObject fails
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `GetActiveObject` raises a `pywintypes.com_error`, `attach()` translates it into a `RhapsodyConnectionError` whose message starts with `"No running Rhapsody instance found:"` and chains the original exception as `__cause__`.
**Pre-conditions:**
- `tests.fakes.make_com_error("no active object")` produces a `pywintypes.com_error`.
- `win32com.client.GetActiveObject` is patched to raise that error.
**Test Steps:**
1. Patch `GetActiveObject` to raise the `com_error`.
2. Call `RhapsodyApplication.attach()` inside an `assertRaises(RhapsodyConnectionError)` block.
3. Inspect the raised exception's `args[0]` and `__cause__`.
**Expected Result:**
A `RhapsodyConnectionError` is raised; its message begins with `"No running Rhapsody instance found:"` and includes the original error text; `__cause__` is the original `pywintypes.com_error`.
**Verification Criteria:**
Pass if `RhapsodyConnectionError` is raised, the message contains the original COM error text, and `__cause__` is the `com_error`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00003: Launch New Rhapsody Instance Happy Path

**ID:** UTS_APP_00003
**Traces-To:** SWR_APP_00002
**Title:** launch() returns a RhapsodyApplication wrapping a freshly dispatched COM object
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RhapsodyApplication.launch()` calls `win32com.client.Dispatch("Rhapsody2.Application.1")` and returns a `RhapsodyApplication` wrapping the dispatched object.
**Pre-conditions:**
- A fake COM application object built via `tests.fakes.make_fake_element("Application")`.
- `win32com.client.Dispatch` is patched to return that fake object.
**Test Steps:**
1. Patch `rhapsody_cli.application.win32com.client.Dispatch` to return the fake COM object.
2. Call `RhapsodyApplication.launch()`.
3. Inspect the returned instance's `_com` attribute.
**Expected Result:**
A `RhapsodyApplication` is returned whose `_com` is the dispatched fake object. `Dispatch` is called exactly once with `"Rhapsody2.Application.1"`.
**Verification Criteria:**
Pass if `isinstance(result, RhapsodyApplication)`, `result._com is fake_app`, and `Dispatch` call args are `("Rhapsody2.Application.1",)`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00004: Launch Raises RhapsodyConnectionError on Dispatch Failure

**ID:** UTS_APP_00004
**Traces-To:** SWR_APP_00002
**Title:** launch() raises RhapsodyConnectionError when Dispatch fails
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `Dispatch` raises a `pywintypes.com_error`, `launch()` raises `RhapsodyConnectionError` with a message beginning `"Failed to launch Rhapsody instance:"` and chains the original error.
**Pre-conditions:**
- `tests.fakes.make_com_error("dispatch failed")` produces a `pywintypes.com_error`.
- `win32com.client.Dispatch` is patched to raise it.
**Test Steps:**
1. Patch `Dispatch` to raise the `com_error`.
2. Call `RhapsodyApplication.launch()` inside `assertRaises(RhapsodyConnectionError)`.
3. Inspect the raised exception message and `__cause__`.
**Expected Result:**
`RhapsodyConnectionError` is raised; message starts with `"Failed to launch Rhapsody instance:"` and includes `"dispatch failed"`; `__cause__` is the original `com_error`.
**Verification Criteria:**
Pass if the raised exception is a `RhapsodyConnectionError`, message contains the original text, and `__cause__` is the `com_error`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00005: Connect with prefer_attach=True Falls Back to Launch

**ID:** UTS_APP_00005
**Traces-To:** SWR_APP_00003
**Title:** connect(prefer_attach=True) falls back to launch() when attach() fails
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `connect(prefer_attach=True)` (the default) attempts `attach()` first, and if `attach()` raises `RhapsodyConnectionError`, falls back to `launch()` and returns the launched instance.
**Pre-conditions:**
- `RhapsodyApplication.attach` is patched to raise `RhapsodyConnectionError`.
- `RhapsodyApplication.launch` is patched to return a sentinel `RhapsodyApplication` instance.
**Test Steps:**
1. Patch `attach` to raise `RhapsodyConnectionError`; patch `launch` to return the sentinel.
2. Call `RhapsodyApplication.connect()` (default `prefer_attach=True`).
3. Inspect the returned object.
**Expected Result:**
The returned object is the sentinel returned by `launch()`. `attach` was called once; `launch` was called once.
**Verification Criteria:**
Pass if `result is sentinel`, `attach.call_count == 1`, and `launch.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00006: Connect with prefer_attach=True Uses Attach When It Succeeds

**ID:** UTS_APP_00006
**Traces-To:** SWR_APP_00003
**Title:** connect(prefer_attach=True) returns attach result and does not call launch
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `attach()` succeeds, `connect(prefer_attach=True)` returns the attached instance and never calls `launch()`.
**Pre-conditions:**
- `RhapsodyApplication.attach` is patched to return a sentinel instance.
- `RhapsodyApplication.launch` is patched (should not be invoked).
**Test Steps:**
1. Patch `attach` to return the sentinel; patch `launch` as a `MagicMock`.
2. Call `RhapsodyApplication.connect(prefer_attach=True)`.
3. Inspect the returned object and `launch.call_count`.
**Expected Result:**
The returned object is the sentinel from `attach()`. `launch` is never called.
**Verification Criteria:**
Pass if `result is sentinel`, `attach.call_count == 1`, and `launch.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00007: Connect with prefer_attach=False Calls Launch Directly

**ID:** UTS_APP_00007
**Traces-To:** SWR_APP_00003
**Title:** connect(prefer_attach=False) calls launch() directly without attach()
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `prefer_attach=False`, `connect()` calls `launch()` directly and never attempts `attach()`.
**Pre-conditions:**
- `RhapsodyApplication.attach` is patched (should not be invoked).
- `RhapsodyApplication.launch` is patched to return a sentinel instance.
**Test Steps:**
1. Patch `attach` and `launch` as above.
2. Call `RhapsodyApplication.connect(prefer_attach=False)`.
3. Inspect the returned object and call counts.
**Expected Result:**
The returned object is the sentinel from `launch()`. `attach` is never called; `launch` is called once.
**Verification Criteria:**
Pass if `result is sentinel`, `attach.call_count == 0`, and `launch.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00008: Open Project File Returns Wrapped RPProject

**ID:** UTS_APP_00008
**Traces-To:** SWR_APP_00004
**Title:** openProject(filename) delegates to COM and returns a wrapped RPProject
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `openProject(filename)` calls `self._com.openProject(filename)` and returns an `RPProject` wrapping the returned COM project object.
**Pre-conditions:**
- A fake COM application object whose `openProject` method returns a fake project COM object (built via `tests.fakes.make_fake_element("Project")`).
- A `RhapsodyApplication` constructed directly with that fake COM object.
**Test Steps:**
1. Build a `RhapsodyApplication(fake_app)`.
2. Call `app.openProject("C:/models/sample.rpy")`.
3. Inspect the type and `_com` of the result.
4. Inspect `fake_app.openProject` call args.
**Expected Result:**
The result is an `RPProject` instance whose `_com` is the fake project COM object. `fake_app.openProject` was called once with `"C:/models/sample.rpy"`.
**Verification Criteria:**
Pass if `isinstance(result, RPProject)`, `result._com is fake_project`, and `fake_app.openProject.call_args == call("C:/models/sample.rpy")`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00009: Open Project Translates COM Error to RhapsodyRuntimeException

**ID:** UTS_APP_00009
**Traces-To:** SWR_APP_00004
**Title:** openProject translates a com_error from the COM call into RhapsodyRuntimeException
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when the underlying `self._com.openProject(...)` raises a `pywintypes.com_error`, `openProject` re-raises it as `RhapsodyRuntimeException` (via `call_com`) and never returns a partial result.
**Pre-conditions:**
- A fake COM application object whose `openProject` side effect is `tests.fakes.make_com_error("file not found")`.
- A `RhapsodyApplication` constructed with that fake object.
**Test Steps:**
1. Build `RhapsodyApplication(fake_app)` with `openProject` raising the `com_error`.
2. Call `app.openProject("missing.rpy")` inside `assertRaises(RhapsodyRuntimeException)`.
3. Inspect the exception message.
**Expected Result:**
`RhapsodyRuntimeException` is raised; its message contains the original COM error text. No `RPProject` is returned.
**Verification Criteria:**
Pass if `RhapsodyRuntimeException` is raised and its `str()` contains `"file not found"`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00010: Get Active Project Returns Wrapped RPProject

**ID:** UTS_APP_00010
**Traces-To:** SWR_APP_00005
**Title:** activeProject() delegates to COM and returns a wrapped RPProject
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `activeProject()` calls `self._com.activeProject()` and returns an `RPProject` wrapping the returned COM object.
**Pre-conditions:**
- A fake COM application whose `activeProject` returns a fake project COM object (built via `tests.fakes.make_fake_element("Project")`).
- A `RhapsodyApplication` constructed with that fake object.
**Test Steps:**
1. Build `RhapsodyApplication(fake_app)`.
2. Call `app.activeProject()`.
3. Inspect the type and `_com` of the result.
4. Verify `fake_app.activeProject` was called once with no arguments.
**Expected Result:**
The result is an `RPProject` whose `_com` is the fake project COM object. `fake_app.activeProject` was called once.
**Verification Criteria:**
Pass if `isinstance(result, RPProject)`, `result._com is fake_project`, and `fake_app.activeProject.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00011: Get All Open Projects Returns RPCollection

**ID:** UTS_APP_00011
**Traces-To:** SWR_APP_00006
**Title:** getProjects() delegates to COM and returns an RPCollection
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `getProjects()` calls `self._com.getProjects()` and returns an `RPCollection` wrapping the returned COM collection object.
**Pre-conditions:**
- A fake COM collection built via `tests.fakes.make_fake_collection([])` (empty is fine for this test).
- A fake COM application whose `getProjects` returns that fake collection.
- A `RhapsodyApplication` constructed with that fake object.
**Test Steps:**
1. Build `RhapsodyApplication(fake_app)`.
2. Call `app.getProjects()`.
3. Inspect the type and `_com` of the result.
4. Verify `fake_app.getProjects` was called once with no arguments.
**Expected Result:**
The result is an `RPCollection` whose `_com` is the fake collection. `fake_app.getProjects` was called once.
**Verification Criteria:**
Pass if `isinstance(result, RPCollection)`, `result._com is fake_collection`, and `fake_app.getProjects.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00012: Quit Application Calls COM quit

**ID:** UTS_APP_00012
**Traces-To:** SWR_APP_00007
**Title:** quit() calls quit() on the underlying COM object
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `quit()` calls `self._com.quit()` exactly once and returns `None`.
**Pre-conditions:**
- A fake COM application object (a `MagicMock`) whose `quit` is a mock method.
- A `RhapsodyApplication` constructed with that fake object.
**Test Steps:**
1. Build `RhapsodyApplication(fake_app)`.
2. Call `app.quit()`.
3. Inspect the return value and `fake_app.quit.call_count`.
**Expected Result:**
`quit()` returns `None` and `fake_app.quit` was called exactly once with no arguments.
**Verification Criteria:**
Pass if `result is None` and `fake_app.quit.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00013: Quit Translates COM Error to RhapsodyRuntimeException

**ID:** UTS_APP_00013
**Traces-To:** SWR_APP_00007
**Title:** quit() translates a com_error from COM quit into RhapsodyRuntimeException
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that when the underlying `self._com.quit()` raises a `pywintypes.com_error`, `quit()` re-raises it as `RhapsodyRuntimeException` (via `call_com`).
**Pre-conditions:**
- A fake COM application whose `quit` side effect is `tests.fakes.make_com_error("already closed")`.
- A `RhapsodyApplication` constructed with that fake object.
**Test Steps:**
1. Build `RhapsodyApplication(fake_app)` with `quit` raising the `com_error`.
2. Call `app.quit()` inside `assertRaises(RhapsodyRuntimeException)`.
3. Inspect the exception message.
**Expected Result:**
`RhapsodyRuntimeException` is raised and its message contains `"already closed"`.
**Verification Criteria:**
Pass if `RhapsodyRuntimeException` is raised and `"already closed"` is in `str(exc)`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00014: Each RhapsodyApplication Instance Wraps Its Own COM Object

**ID:** UTS_APP_00014
**Traces-To:** SWR_APP_00008
**Title:** Two RhapsodyApplication instances wrap two distinct COM objects independently
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `RhapsodyApplication` is not a singleton: two instances constructed with two distinct fake COM objects each hold their own `_com` and operate independently.
**Pre-conditions:**
- Two distinct fake COM application objects, `fake_app_a` and `fake_app_b`.
**Test Steps:**
1. Construct `app_a = RhapsodyApplication(fake_app_a)`.
2. Construct `app_b = RhapsodyApplication(fake_app_b)`.
3. Assert `app_a._com is fake_app_a` and `app_b._com is fake_app_b`.
4. Assert `app_a is not app_b`.
5. Call `app_a.quit()` and verify `fake_app_b.quit` was NOT called.
**Expected Result:**
Each instance holds its own COM object. Calling `quit()` on one does not affect the other.
**Verification Criteria:**
Pass if `app_a._com is fake_app_a`, `app_b._com is fake_app_b`, `app_a is not app_b`, and after `app_a.quit()`, `fake_app_a.quit.call_count == 1` while `fake_app_b.quit.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_APP_00015: Prog ID Constant Equals Rhapsody2.Application.1

**ID:** UTS_APP_00015
**Traces-To:** SWR_APP_00009
**Title:** _PROG_ID module constant is the canonical Rhapsody2.Application.1 Prog ID
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that the `_PROG_ID` module-level constant in `rhapsody_cli.application` equals `"Rhapsody2.Application.1"` and that `attach()`/`launch()` pass that exact string to `GetActiveObject`/`Dispatch`.
**Pre-conditions:**
- Import access to `rhapsody_cli.application._PROG_ID`.
- `GetActiveObject` and `Dispatch` patched to capture call args.
**Test Steps:**
1. Import `_PROG_ID` from `rhapsody_cli.application`.
2. Assert `_PROG_ID == "Rhapsody2.Application.1"`.
3. Patch `GetActiveObject` to return a fake; call `attach()`; capture the call argument.
4. Patch `Dispatch` to return a fake; call `launch()`; capture the call argument.
**Expected Result:**
`_PROG_ID` is `"Rhapsody2.Application.1"`. Both `GetActiveObject` and `Dispatch` are called with exactly that string.
**Verification Criteria:**
Pass if `_PROG_ID == "Rhapsody2.Application.1"`, and the captured call args for both `GetActiveObject` and `Dispatch` equal `("Rhapsody2.Application.1",)`.
**Last Changed:** 2026-07-07
