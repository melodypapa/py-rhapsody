# Acceptance Test Specifications - Application Connection Layer

**Category:** APP
**Prefix:** ATS
**Test Type:** Acceptance
**Last Validated:** 2026-07-07

---

## ATS_APP_00001: Attach to a Running Rhapsody Instance

**ID:** ATS_APP_00001
**Traces-To:** SWR_APP_00001, SWR_APP_00009
**Title:** Attach to a running Rhapsody instance via COM GetActiveObject
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to attach to an already-running IBM Rhapsody instance from
rhapsody_cli, so that I can drive an interactive Rhapsody session that is already open
without launching a duplicate process.
**Acceptance Criteria:**
- Given a Rhapsody instance is already running on the machine, When I call
  `RhapsodyApplication.attach()`, Then a `RhapsodyApplication` instance is returned whose
  underlying COM object is the active `"Rhapsody2.Application.1"` instance.
- Given no Rhapsody instance is running, When I call `RhapsodyApplication.attach()`, Then
  a `RhapsodyConnectionError` is raised with a message indicating that no running instance
  was found.
- Given `attach()` succeeds, When I inspect the COM Prog ID used internally, Then it is the
  canonical `"Rhapsody2.Application.1"` Prog ID.
**Verification Criteria:**
Open Task Manager, confirm no `rhapsody.exe` is running, call `attach()` and assert that
`RhapsodyConnectionError` is raised. Launch Rhapsody manually, call `attach()`, and assert
the returned object's `getName()` (or `activeProject()`) call succeeds against the live
instance. Confirm no new `rhapsody.exe` process was created by the attach call.
**Last Changed:** 2026-07-07

---

## ATS_APP_00002: Launch a New Rhapsody Instance

**ID:** ATS_APP_00002
**Traces-To:** SWR_APP_00002, SWR_APP_00009
**Title:** Launch a new Rhapsody instance via COM Dispatch
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to launch a fresh Rhapsody instance from rhapsody_cli, so that
I can run automated model manipulations against a clean, dedicated Rhapsody process.
**Acceptance Criteria:**
- Given no Rhapsody instance needs to be reused, When I call
  `RhapsodyApplication.launch()`, Then a new Rhapsody process is started via COM Dispatch
  and a `RhapsodyApplication` wrapping that process is returned.
- Given the COM Dispatch call fails (e.g., Rhapsody not installed), When I call
  `RhapsodyApplication.launch()`, Then a `RhapsodyConnectionError` is raised with a
  message describing the launch failure.
- Given `launch()` succeeds, When I check running processes, Then a new `rhapsody.exe`
  process exists that was not present before the call.
**Verification Criteria:**
Record the count of `rhapsody.exe` processes before the call, call `launch()`, then
confirm the count increased by exactly one and the returned `RhapsodyApplication` can be
driven (e.g., `getProjects()` returns without error). On a machine without Rhapsody
installed, confirm `RhapsodyConnectionError` is raised and its message contains the
underlying failure detail.
**Last Changed:** 2026-07-07

---

## ATS_APP_00003: Connect with Attach-First Fallback to Launch

**ID:** ATS_APP_00003
**Traces-To:** SWR_APP_00003
**Title:** Connect to Rhapsody using attach-first, falling back to launch
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want a single `connect()` entry point that reuses a running
Rhapsody if possible and otherwise launches a new one, so that I do not have to write
try/except logic at every call site.
**Acceptance Criteria:**
- Given a Rhapsody instance is already running, When I call
  `RhapsodyApplication.connect(prefer_attach=True)`, Then the returned
  `RhapsodyApplication` is attached to that existing instance (no new process started).
- Given no Rhapsody instance is running, When I call
  `RhapsodyApplication.connect(prefer_attach=True)`, Then `attach()` fails silently and a
  new instance is launched; the returned `RhapsodyApplication` wraps the new instance.
- Given `prefer_attach=False`, When I call `RhapsodyApplication.connect(prefer_attach=False)`,
  Then `launch()` is called directly even if a Rhapsody instance is already running.
**Verification Criteria:**
With Rhapsody already open, call `connect()` and verify (via process count) that no new
`rhapsody.exe` was created and the returned object targets the same project that is open
in the GUI. Close Rhapsody, call `connect()` again, and verify a new process is launched.
Call `connect(prefer_attach=False)` while Rhapsody is running and verify that a second
`rhapsody.exe` process is created.
**Last Changed:** 2026-07-07

---

## ATS_APP_00004: Open, Query, and Select Projects

**ID:** ATS_APP_00004
**Traces-To:** SWR_APP_00004, SWR_APP_00005, SWR_APP_00006
**Title:** Open a project from a path and query open/active projects
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to open a Rhapsody project from a file path and retrieve the
set of open projects and the active project, so that I can script model-level operations
against a known target.
**Acceptance Criteria:**
- Given a connected `RhapsodyApplication` and a valid `.rpyx` project path on disk, When I
  call `app.openProject(path)`, Then an `RPProject` wrapping the opened project is
  returned and the project appears in the Rhapsody GUI.
- Given `openProject` is called with a path whose COM open call fails, When the COM error
  is propagated, Then a `RhapsodyRuntimeException` (not a raw `pywintypes.com_error`) is
  raised with the original COM message preserved.
- Given one or more projects are open, When I call `app.getProjects()`, Then an
  `RPCollection` is returned whose length equals the number of open projects and whose
  items are wrapped `RPProject` instances.
- Given a project has been opened and made active, When I call `app.activeProject()`, Then
  the returned `RPProject` matches the project most recently made active.
**Verification Criteria:**
Connect to Rhapsody, call `openProject` on a known-good fixture project, and assert the
returned object's `getName()` matches the project file name. Call `getProjects()` and
assert `len(...) >= 1` and that iterating yields `RPProject` instances. Call
`activeProject()` and assert its name is among the open projects. Repeat `openProject`
with a non-existent path and assert that `RhapsodyRuntimeException` is raised and its
message is a non-empty string.
**Last Changed:** 2026-07-07

---

## ATS_APP_00005: Quit the Wrapped Rhapsody Instance

**ID:** ATS_APP_00005
**Traces-To:** SWR_APP_00007
**Title:** Terminate the wrapped Rhapsody instance via quit
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a test engineer, I want to terminate the Rhapsody instance wrapped by a
`RhapsodyApplication`, so that automated runs leave no orphaned Rhapsody process behind.
**Acceptance Criteria:**
- Given a `RhapsodyApplication` that was launched via `launch()` or `connect()`, When I
  call `app.quit()`, Then the underlying Rhapsody process terminates and the COM object is
  no longer usable.
- Given the `RhapsodyApplication` was obtained via `attach()` to an externally launched
  instance, When I call `app.quit()`, Then the attached Rhapsody process is also
  terminated (the wrapper does not distinguish attach vs. launch for quit behavior).
**Verification Criteria:**
Launch a Rhapsody via `connect(prefer_attach=False)`, record the PID of the new
`rhapsody.exe` process, call `quit()`, and assert within a few seconds that the PID no
longer exists in the process list. Calling any method on the wrapped COM object after
`quit()` should raise an exception (COM object no longer valid).
**Last Changed:** 2026-07-07

---

## ATS_APP_00006: Run Multiple RhapsodyApplication Instances Side by Side

**ID:** ATS_APP_00006
**Traces-To:** SWR_APP_00008
**Title:** Manage multiple independent RhapsodyApplication instances in one process
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a test engineer, I want to create multiple `RhapsodyApplication` instances in the same
Python process, so that I can compare or migrate models between two Rhapsody sessions
simultaneously.
**Acceptance Criteria:**
- Given `RhapsodyApplication` is not a singleton, When I create two instances via
  `launch()` (or a mix of `attach()` and `launch()`), Then each instance wraps a distinct
  COM object and the two instances do not share state.
- Given two `RhapsodyApplication` instances `app_a` and `app_b`, When I open project A in
  `app_a` and project B in `app_b`, Then `app_a.activeProject()` returns project A and
  `app_b.activeProject()` returns project B, and calling `quit()` on one does not affect
  the other.
**Verification Criteria:**
Call `launch()` twice to obtain `app_a` and `app_b`; assert `app_a._com is not app_b._com`.
Open two different fixture projects, one in each app, and assert
`app_a.activeProject().getName() != app_b.activeProject().getName()`. Call `app_a.quit()`,
then assert `app_b.activeProject()` still returns the expected project (i.e., `app_b` is
unaffected). Finally call `app_b.quit()` to clean up.
**Last Changed:** 2026-07-07
