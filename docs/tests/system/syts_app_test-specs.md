# System Test Specifications - Application Connection Layer

**Category:** APP
**Prefix:** SYTS
**Test Type:** System
**Last Validated:** 2026-07-07

---

## SYTS_APP_00001: Connect with Attach-First Fallback to Launch

**ID:** SYTS_APP_00001
**Traces-To:** SWR_APP_00001, SWR_APP_00002, SWR_APP_00003
**Title:** Connect with attach-first fallback to launch end-to-end
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end connection flow exercised through the CLI stack: when a
running Rhapsody instance is present, `RhapsodyApplication.connect(prefer_attach=True)`
attaches to it; when no running instance is found, the connection layer transparently
falls back to launching a new instance. The fake COM layer simulates both scenarios so the
real `connect()` code path (including the `attach()` -> `launch()` fallback) is exercised.
**Pre-conditions:**
- A fake `win32com.client.GetActiveObject` that raises `pythoncom.com_error` to simulate
  "no running instance", and a fake `win32com.client.Dispatch` that returns a fake
  `Rhapsody.Application` COM object.
- A second configuration where `GetActiveObject` succeeds and returns a fake running
  instance.
- CliRunner from click available to drive the CLI.
**Test Steps:**
1. Configure the fake COM layer so `GetActiveObject` raises a com_error (no running
   instance) and `Dispatch` returns a fake `Rhapsody.Application` object.
2. Invoke the CLI through CliRunner with a command that triggers `connect()` (e.g.
   `project list`) and capture stdout/stderr and the exit code.
3. Reconfigure the fake COM layer so `GetActiveObject` returns a fake running instance.
4. Re-invoke the same CLI command and capture stdout/stderr and the exit code.
**Expected Result:**
- In the fallback scenario, `attach()` fails internally and `launch()` is invoked; the CLI
  command completes successfully (exit code 0) and produces the expected output
  (e.g. "No open projects" or a project listing).
- In the attach-success scenario, `launch()` is NOT invoked and the CLI command completes
  successfully (exit code 0) with the same expected output.
**Verification Criteria:**
- Pass if both scenarios exit with code 0 and produce the expected command output.
- Pass if the fake COM dispatch counters confirm `Dispatch` was called exactly once in the
  fallback scenario and zero times in the attach-success scenario.
- Fail if any `RhapsodyConnectionError` propagates to the user, or if `launch()` is
  invoked when attach already succeeded.
**Last Changed:** 2026-07-07

---

## SYTS_APP_00002: Open Project File End-to-End Lifecycle

**ID:** SYTS_APP_00002
**Traces-To:** SWR_APP_00003, SWR_APP_00004, SWR_APP_00005
**Title:** Open a project file, retrieve active project, and verify wrapped RPProject
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end project lifecycle from the CLI: connecting to a fake
Rhapsody instance, opening a project file from a path, and confirming the active project
matches the one that was opened. It exercises `connect()`, `openProject(filename)`, and
`activeProject()` together.
**Pre-conditions:**
- A fake `Rhapsody.Application` COM object whose `openProject(path)` returns a fake
  `IRPProject` with a known name and GUID.
- A temporary file on disk representing the project path (so the CLI's path-existence
  validation passes).
- CliRunner available.
**Test Steps:**
1. Create a temp file path to serve as `project_path`.
2. Invoke `rhapsody project open <project_path>` through CliRunner.
3. Capture stdout/stderr and exit code.
4. Through the fake COM layer, inspect which COM method was called on the application
   object and which path was passed.
5. Invoke a follow-up command that reads `activeProject()` (e.g. `element query`) and
   capture its output.
**Expected Result:**
- The `project open` command exits with code 0 and echoes "Opened project: {path}".
- The fake application's `openProject` COM method is called exactly once with the
  provided path.
- The follow-up command that reads the active project succeeds and produces output
  consistent with the fake project (e.g. lists its nested elements or packages).
**Verification Criteria:**
- Pass if exit code is 0 for both commands, the success message matches exactly, and the
  fake COM `openProject` call recorder shows the correct path argument.
- Fail if the project fails to open, if the active project is `None` after opening, or if
  the success message is missing from stdout.
**Last Changed:** 2026-07-07

---

## SYTS_APP_00003: Get All Open Projects and Quit Application

**ID:** SYTS_APP_00003
**Traces-To:** SWR_APP_00006, SWR_APP_00007
**Title:** Retrieve all open projects via RPCollection and quit the application
**Type:** System
**Priority:** Medium
**Description:**
This test verifies that `getProjects()` returns an `RPCollection` of all currently open
projects and that `quit()` terminates the wrapped COM instance. It exercises these
end-to-end via the CLI's `project list` command and an explicit disconnect.
**Pre-conditions:**
- A fake `Rhapsody.Application` COM object whose `getProjects()` returns a fake
  `IRPCollection` containing two fake `IRPProject` objects with distinct names and paths.
- The fake application records calls to `quit()`.
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody project list` through CliRunner.
2. Capture stdout/stderr and exit code.
3. Verify the output contains both project names and paths in table format.
4. Trigger a disconnect (e.g. via a command that calls `ctx.disconnect()` or by directly
   invoking `app.quit()` on the wrapped instance).
5. Inspect the fake COM application's call recorder.
**Expected Result:**
- `project list` exits with code 0 and prints a table with both fake projects.
- After disconnect, the fake application's `quit()` COM method is called exactly once.
**Verification Criteria:**
- Pass if the table output contains both project names, exit code is 0, and the fake
  `quit()` call counter equals 1 after disconnect.
- Fail if either project is missing from the output, or if `quit()` is never called or
  called more than once.
**Last Changed:** 2026-07-07

---

## SYTS_APP_00004: Multiple Independent Application Instances (No Singleton)

**ID:** SYTS_APP_00004
**Traces-To:** SWR_APP_00008, SWR_APP_00009
**Title:** Two RhapsodyApplication instances wrap distinct COM objects independently
**Type:** System
**Priority:** Medium
**Description:**
This test verifies that `RhapsodyApplication` is not a global singleton: two instances can
be created in the same process, each wrapping a distinct fake COM object, and operating on
one does not affect the other. It also confirms the canonical Prog ID
`"Rhapsody.Application"` is used.
**Pre-conditions:**
- A fake `win32com.client.Dispatch` that returns a fresh fake `Rhapsody.Application`
  object on each call, recording the Prog ID passed.
- Two distinct fake projects that can be opened by the two instances.
- CliRunner available (the test may also directly instantiate `RhapsodyApplication`).
**Test Steps:**
1. Create two `RhapsodyApplication` instances via `connect(prefer_attach=False)` so each
   calls `launch()` (Dispatch).
2. Open project A on the first instance and project B on the second.
3. Invoke `project list` against each instance and capture output.
4. Inspect the fake Dispatch recorder to confirm the Prog ID was
   `"Rhapsody.Application"` on both calls.
**Expected Result:**
- Each instance lists only its own opened project, confirming independence.
- The fake Dispatch recorder shows two calls, both with Prog ID
   `"Rhapsody.Application"`.
**Verification Criteria:**
- Pass if instance 1's project list contains only project A and instance 2's contains
  only project B, and both Dispatch calls used the canonical Prog ID.
- Fail if both instances share state (e.g. both lists contain both projects), or if the
  Prog ID differs from `"Rhapsody.Application"`.
**Last Changed:** 2026-07-07

---

## SYTS_APP_00005: Connection Failure Propagates to CLI as Abort

**ID:** SYTS_APP_00005
**Traces-To:** SWR_APP_00001, SWR_APP_00002, SWR_APP_00003
**Title:** Connection failure surfaces as RhapsodyConnectionError and CLI aborts non-zero
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end error path: when both `attach()` and `launch()` fail
against the fake COM layer, the resulting `RhapsodyConnectionError` propagates to the CLI,
which echoes the error to stderr and aborts with a non-zero exit code.
**Pre-conditions:**
- A fake `win32com.client.GetActiveObject` that raises `pythoncom.com_error`.
- A fake `win32com.client.Dispatch` that also raises `pythoncom.com_error` (simulating
  Rhapsody not installed).
- CliRunner available.
**Test Steps:**
1. Configure the fake COM layer so both `GetActiveObject` and `Dispatch` raise com_error.
2. Invoke `rhapsody project open <some_path>` through CliRunner.
3. Capture stdout, stderr, and exit code.
**Expected Result:**
- The CLI exits with a non-zero exit code (CliRunner typically reports exit code 1 for
  `click.Abort`).
- The error message written to stderr mentions the connection failure (e.g. contains
  "RhapsodyConnectionError" or the message "No running Rhapsody instance found" /
  "Failed to launch Rhapsody instance").
- Stdout does NOT contain a success message like "Opened project:".
**Verification Criteria:**
- Pass if exit code is non-zero, stderr contains a connection-failure description, and
  stdout has no success message.
- Fail if the CLI exits 0, if the raw com_error leaks to the user, or if no error is
  written to stderr.
**Last Changed:** 2026-07-07

---
