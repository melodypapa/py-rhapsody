# Unit Test Specifications - Command-Line Interface

**Category:** CLI
**Prefix:** UTS
**Test Type:** Unit
**Last Validated:** 2026-07-07

---

## UTS_CLI_00001: cli Group Is the Main Entry Point

**ID:** UTS_CLI_00001
**Traces-To:** SWR_CLI_00001
**Title:** cli group registers the project, element, and io subgroups
**Type:** Unit
**Priority:** High
**Description:**
Verifies that the `cli` Click group is the main entry point and registers the `project`, `element`, and `io` command subgroups as named subcommands.
**Pre-conditions:**
- `rhapsody_cli.cli.main` imported (which triggers `cli.add_command(project_cmd)` etc.).
- `click.testing.CliRunner` available.
**Test Steps:**
1. Import `cli` from `rhapsody_cli.cli.main`.
2. Assert `cli.name == "cli"` and `cli` is a `click.Group`.
3. Inspect `cli.commands` (the registered subcommands).
4. Run `CliRunner().invoke(cli, ["--help"])` and inspect stdout.
**Expected Result:**
`cli.commands` contains the keys `"project"`, `"element"`, and `"io"`. The `--help` output lists all three subcommands.
**Verification Criteria:**
Pass if all three subcommand names are present in `cli.commands` and the help output mentions them.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00002: cli Group Creates RhapsodyContext When None Exists

**ID:** UTS_CLI_00002
**Traces-To:** SWR_CLI_00001
**Title:** cli callback creates a new RhapsodyContext when ctx.obj is None
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when no context object exists, the `cli` callback constructs a new `RhapsodyContext` and assigns it to `ctx.obj`, and sets `output_format` on it.
**Pre-conditions:**
- `RhapsodyContext` patched (or its constructor spied) so the test can observe construction.
- `CliRunner` available.
**Test Steps:**
1. Patch `rhapsody_cli.cli.main.RhapsodyContext` to return a sentinel instance.
2. Invoke `cli` with `["--output","json","--help"]` via `CliRunner`.
3. Inspect the `ctx.obj` produced during invocation (or assert `RhapsodyContext` was instantiated).
**Expected Result:**
A new `RhapsodyContext` is constructed during the invocation and its `output_format` attribute is set to `"json"`.
**Verification Criteria:**
Pass if `RhapsodyContext` was constructed once and the resulting context has `output_format == "json"`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00003: --output Option Accepts table, json, csv

**ID:** UTS_CLI_00003
**Traces-To:** SWR_CLI_00002
**Title:** --output option accepts the three allowed choices and rejects others
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that the `--output` option is a `click.Choice` over `["table", "json", "csv"]`, defaults to `"table"`, and rejects any other value with a Click usage error.
**Pre-conditions:**
- `cli` imported.
- `CliRunner` available.
**Test Steps:**
1. Invoke `cli` with `["--output","json","--help"]` and assert exit code 0.
2. Invoke `cli` with `["--output","csv","--help"]` and assert exit code 0.
3. Invoke `cli` with `["--output","table","--help"]` and assert exit code 0.
4. Invoke `cli` with `["--output","xml","--help"]` and assert a non-zero exit code and an error message mentioning invalid choice.
**Expected Result:**
The three allowed values are accepted; `"xml"` is rejected with a Click `UsageError`-style message.
**Verification Criteria:**
Pass if the first three invocations exit 0 and the fourth exits non-zero with a message containing `"invalid choice"` (or similar) and `"xml"`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00004: --output Default Is table and Stored on ctx.obj

**ID:** UTS_CLI_00004
**Traces-To:** SWR_CLI_00002
**Title:** --output defaults to "table" and is stored on ctx.obj.output_format
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `--output` is omitted, the resulting `RhapsodyContext.output_format` is `"table"`.
**Pre-conditions:**
- `RhapsodyContext` constructor spied or a captured `ctx.obj`.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a real (or sentinel) instance whose `output_format` attribute can be inspected.
2. Invoke `cli` with `["--help"]` (no `--output`).
3. Capture the context that was assigned to `ctx.obj`.
4. Assert `ctx.obj.output_format == "table"`.
**Expected Result:**
The default value of `--output` is `"table"` and it is stored on `ctx.obj.output_format`.
**Verification Criteria:**
Pass if `ctx.obj.output_format == "table"` after the invocation.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00005: RhapsodyContext Initial State

**ID:** UTS_CLI_00005
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext initializes app, project, output_format to defaults
**Type:** Unit
**Priority:** High
**Description:**
Verifies that a freshly constructed `RhapsodyContext` has `app is None`, `project is None`, and `output_format == "table"`.
**Pre-conditions:**
- `RhapsodyContext` importable.
**Test Steps:**
1. Construct `ctx = RhapsodyContext()`.
2. Assert `ctx.app is None`.
3. Assert `ctx.project is None`.
4. Assert `ctx.output_format == "table"`.
**Expected Result:**
All three attributes match their default values.
**Verification Criteria:**
Pass if all three assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00006: RhapsodyContext.connect Lazily Attaches or Launches

**ID:** UTS_CLI_00006
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.connect attaches/launches only when app is None and caches the result
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `connect(method="attach")` calls `RhapsodyApplication.attach()` when `app is None` and caches the result; `connect(method="launch")` calls `launch()` instead; a second `connect()` call reuses the cached `app` without calling attach/launch again.
**Pre-conditions:**
- `RhapsodyApplication.attach` and `RhapsodyApplication.launch` patched to return sentinels.
- A fresh `RhapsodyContext`.
**Test Steps:**
1. Patch `attach` to return `sentinel_a`; patch `launch` to return `sentinel_l`.
2. Construct `ctx = RhapsodyContext()`.
3. Call `ctx.connect("attach")` and assert the return value is `sentinel_a` and `ctx.app is sentinel_a`.
4. Call `ctx.connect("attach")` again and assert `attach.call_count` is still `1`.
5. Construct a second context; call `ctx2.connect("launch")` and assert the return is `sentinel_l` and `launch.call_count == 1`.
**Expected Result:**
First `connect("attach")` calls `attach()` once and caches; the second call reuses the cache. `connect("launch")` calls `launch()`.
**Verification Criteria:**
Pass if `ctx.app is sentinel_a`, `attach.call_count == 1`, and `ctx2.app is sentinel_l`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00007: RhapsodyContext.open_project Connects If Needed

**ID:** UTS_CLI_00007
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.open_project connects when app is None and stores the opened project
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `open_project(path)` calls `connect()` when `app is None`, then calls `app.openProject(path)`, stores the result in `self.project`, and returns it.
**Pre-conditions:**
- A fake `RhapsodyApplication` whose `openProject` returns a fake `RPProject`.
- `RhapsodyApplication.attach`/`launch` patched to return that fake app.
- A fresh `RhapsodyContext`.
**Test Steps:**
1. Patch `RhapsodyApplication.attach` to return `fake_app` whose `openProject` returns `fake_proj`.
2. Construct `ctx = RhapsodyContext()`.
3. Call `ctx.open_project("C:/m.rpy")`.
4. Assert the return value is `fake_proj`, `ctx.project is fake_proj`, `ctx.app is fake_app`, and `fake_app.openProject.call_args == call("C:/m.rpy")`.
**Expected Result:**
`open_project` connects lazily, opens the project, caches it, and returns it.
**Verification Criteria:**
Pass if all assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00008: RhapsodyContext.open_project Does Not Reconnect If App Exists

**ID:** UTS_CLI_00008
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.open_project skips connect() when app is already set
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `app` is already set, `open_project(path)` does NOT call `connect()` and directly calls `app.openProject(path)`.
**Pre-conditions:**
- A `RhapsodyContext` whose `app` is pre-set to a `fake_app` (whose `openProject` returns `fake_proj`).
- `RhapsodyApplication.attach`/`launch` patched as spies that should not be called.
**Test Steps:**
1. Construct `ctx = RhapsodyContext()`; set `ctx.app = fake_app`.
2. Patch `RhapsodyApplication.attach` and `launch` as mocks.
3. Call `ctx.open_project("C:/m.rpy")`.
4. Assert `attach.call_count == 0` and `launch.call_count == 0`.
5. Assert `ctx.project is fake_proj` and `fake_app.openProject.call_args == call("C:/m.rpy")`.
**Expected Result:**
`connect()` is not invoked; the project is opened via the existing app.
**Verification Criteria:**
Pass if neither `attach` nor `launch` is called and `ctx.project` is the fake project.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00009: RhapsodyContext.close_project Closes and Clears

**ID:** UTS_CLI_00009
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.close_project closes the project and sets it to None
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `close_project()` calls `project.close()` when a project exists and then sets `self.project = None`; when no project exists, it is a no-op.
**Pre-conditions:**
- A `RhapsodyContext` with `project` set to a `MagicMock` fake project exposing `close`.
- A second `RhapsodyContext` with `project = None`.
**Test Steps:**
1. Construct `ctx1` with `ctx1.project = fake_proj` (a `MagicMock`).
2. Call `ctx1.close_project()`.
3. Assert `fake_proj.close.call_count == 1` and `ctx1.project is None`.
4. Construct `ctx2` with `ctx2.project = None`.
5. Call `ctx2.close_project()` and assert no exception is raised and `ctx2.project is None`.
**Expected Result:**
`close_project()` closes the project and clears the reference; calling it with no project is a safe no-op.
**Verification Criteria:**
Pass if `fake_proj.close` was called once, `ctx1.project is None`, and `ctx2.close_project()` did not raise.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00010: RhapsodyContext.disconnect Closes Project and Quits App

**ID:** UTS_CLI_00010
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.disconnect closes the project, quits the app, and clears both
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `disconnect()` calls `close_project()` (which closes the project and clears it) and then calls `app.quit()` and sets `self.app = None`.
**Pre-conditions:**
- A `RhapsodyContext` with `app = fake_app` (a `MagicMock` exposing `quit`) and `project = fake_proj` (a `MagicMock` exposing `close`).
**Test Steps:**
1. Construct `ctx` with `ctx.app = fake_app` and `ctx.project = fake_proj`.
2. Call `ctx.disconnect()`.
3. Assert `fake_proj.close.call_count == 1`.
4. Assert `fake_app.quit.call_count == 1`.
5. Assert `ctx.project is None` and `ctx.app is None`.
**Expected Result:**
`disconnect()` closes the project, quits the app, and clears both references.
**Verification Criteria:**
Pass if both `close` and `quit` were called once and both `ctx.project` and `ctx.app` are `None`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00011: RhapsodyContext.disconnect With No App Is a No-op

**ID:** UTS_CLI_00011
**Traces-To:** SWR_CLI_00003
**Title:** RhapsodyContext.disconnect does not raise when app and project are None
**Type:** Unit
**Priority:** Low
**Description:**
Verifies the boundary case where `disconnect()` is called on a fresh context with no app and no project: it should not raise.
**Pre-conditions:**
- A fresh `RhapsodyContext` with `app is None` and `project is None`.
**Test Steps:**
1. Construct `ctx = RhapsodyContext()`.
2. Call `ctx.disconnect()`.
3. Assert `ctx.app is None` and `ctx.project is None`.
**Expected Result:**
No exception is raised; both attributes remain `None`.
**Verification Criteria:**
Pass if `disconnect()` returns without raising and both attributes are `None`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00012: project open Command Happy Path

**ID:** UTS_CLI_00012
**Traces-To:** SWR_CLI_00004
**Title:** project open opens a project and echoes "Opened project: {path}"
**Type:** Unit
**Priority:** High
**Description:**
Verifies that the `project open` command constructs a `RhapsodyContext`, connects via `"attach"`, opens the supplied project path, and echoes `"Opened project: {path}"` to stdout.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `connect`, `open_project` are no-ops/spies.
- A temporary file path that exists on disk (so `click.Path(exists=True)` passes).
- `CliRunner` available.
**Test Steps:**
1. Patch `rhapsody_cli.cli.commands.project.RhapsodyContext` to return a fake context.
2. Create a temp file (e.g., via `tempfile.NamedTemporaryFile`) to satisfy `exists=True`.
3. Invoke `cli` with `["project","open",temp_path]` via `CliRunner`.
4. Inspect `result.exit_code` and `result.output`.
5. Inspect the fake context's `connect` and `open_project` call args.
**Expected Result:**
`result.exit_code == 0`; `result.output` contains `"Opened project: " + temp_path`; `fake_ctx.connect.call_args == call("attach")`; `fake_ctx.open_project.call_args == call(temp_path)`.
**Verification Criteria:**
Pass if exit code is 0, output contains the expected message, and `connect`/`open_project` were called with the expected arguments.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00013: project open Command Translates RhapsodyConnectionError to Abort

**ID:** UTS_CLI_00013
**Traces-To:** SWR_CLI_00004
**Title:** project open echoes a connection error to stderr and aborts on RhapsodyConnectionError
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `connect`/`open_project` raises a `RhapsodyConnectionError`, the command echoes `"Connection error: {e}"` to stderr and raises `click.Abort` (non-zero exit code).
**Pre-conditions:**
- `RhapsodyContext` patched so its `connect` raises `RhapsodyConnectionError("no rhapsody")`.
- A temp file path that exists on disk.
- `CliRunner` available (with `mix_stderr=False` if separating stderr).
**Test Steps:**
1. Patch `RhapsodyContext` so `connect` raises `RhapsodyConnectionError("no rhapsody")`.
2. Invoke `cli` with `["project","open",temp_path]` via `CliRunner`.
3. Inspect `result.exit_code` and stderr/output.
**Expected Result:**
`result.exit_code != 0`; the error output contains `"Connection error:"` and `"no rhapsody"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains both `"Connection error:"` and the original message.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00014: project open Command Translates Generic Exception to Abort

**ID:** UTS_CLI_00014
**Traces-To:** SWR_CLI_00004
**Title:** project open echoes a generic error to stderr and aborts on other exceptions
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when an unexpected exception (not `RhapsodyConnectionError`, not `click.Abort`) is raised during execution, the command echoes `"Error: {e}"` to stderr and raises `click.Abort`.
**Pre-conditions:**
- `RhapsodyContext` patched so `open_project` raises `RuntimeError("boom")`.
- A temp file path that exists on disk.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` so `open_project` raises `RuntimeError("boom")`.
2. Invoke `cli` with `["project","open",temp_path]` via `CliRunner`.
3. Inspect `result.exit_code` and error output.
**Expected Result:**
`result.exit_code != 0`; the error output contains `"Error:"` and `"boom"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains both `"Error:"` and `"boom"`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00015: project list Command Happy Path With Projects

**ID:** UTS_CLI_00015
**Traces-To:** SWR_CLI_00005
**Title:** project list echoes a formatted table of open projects
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `project list` connects via `"attach"`, retrieves open projects, and echoes a table (via `OutputFormatter.table`) with columns `Name` and `Path` derived from `proj.getName()` and `proj.getPath()`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `app.getProjects()` returns a fake collection of two fake projects (`getName`/`getPath` configured).
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `app.getProjects()` returning two fake projects.
2. Invoke `cli` with `["project","list"]` via `CliRunner`.
3. Inspect `result.exit_code` and `result.output`.
**Expected Result:**
`result.exit_code == 0`; output is a table containing both projects' names and paths; `fake_ctx.connect.call_args == call("attach")`.
**Verification Criteria:**
Pass if exit code is 0 and the output contains both project names and paths in a tabulated form.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00016: project list Command With No Open Projects

**ID:** UTS_CLI_00016
**Traces-To:** SWR_CLI_00005
**Title:** project list echoes "No open projects" when the collection is empty
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the empty-collection branch: when `getProjects()` returns an empty collection (or a falsy collection), the command echoes exactly `"No open projects"` and does not call `OutputFormatter.table`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `app.getProjects()` returns an empty fake collection (`make_fake_collection([])`).
- `OutputFormatter.table` patched as a spy.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` as above.
2. Patch `rhapsody_cli.cli.commands.project.OutputFormatter.table` as a spy.
3. Invoke `cli` with `["project","list"]` via `CliRunner`.
4. Inspect `result.exit_code` and `result.output`.
**Expected Result:**
`result.exit_code == 0`; `result.output` stripped equals `"No open projects"`; `OutputFormatter.table` was not called.
**Verification Criteria:**
Pass if exit code is 0, the output is exactly the no-projects message, and `OutputFormatter.table.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00017: project list Command Reports Exceptions to stderr

**ID:** UTS_CLI_00017
**Traces-To:** SWR_CLI_00005
**Title:** project list echoes an error and aborts when an exception is raised
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that when `getProjects()` (or any other call) raises an exception, the command echoes `"Error: {e}"` to stderr and aborts with a non-zero exit code.
**Pre-conditions:**
- `RhapsodyContext` patched so `app.getProjects()` raises `RuntimeError("oops")`.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` as above.
2. Invoke `cli` with `["project","list"]` via `CliRunner`.
3. Inspect `result.exit_code` and error output.
**Expected Result:**
`result.exit_code != 0`; the error output contains `"Error:"` and `"oops"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains both substrings.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00018: project close Command With No Active Project

**ID:** UTS_CLI_00018
**Traces-To:** SWR_CLI_00006
**Title:** project close echoes "No active project" when ctx.project is None
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when no active project exists, `project close` echoes `"No active project"` and does not call `close_project()`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `project` is `None` and whose `close_project` is a spy.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `project = None`.
2. Invoke `cli` with `["project","close"]` via `CliRunner`.
3. Inspect `result.exit_code` and `result.output`; inspect `fake_ctx.close_project.call_count`.
**Expected Result:**
`result.exit_code == 0`; `result.output` stripped equals `"No active project"`; `close_project` was not called.
**Verification Criteria:**
Pass if exit code is 0, output is the no-active-project message, and `close_project.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00019: project close Command Happy Path

**ID:** UTS_CLI_00019
**Traces-To:** SWR_CLI_00006
**Title:** project close closes the active project and echoes "Project closed"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when an active project exists, `project close` calls `ctx.close_project()` and echoes `"Project closed"`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `project` is a truthy `MagicMock` and whose `close_project` is a spy.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `project = MagicMock()`.
2. Invoke `cli` with `["project","close"]` via `CliRunner`.
3. Inspect `result.exit_code` and `result.output`; inspect `fake_ctx.close_project.call_count`.
**Expected Result:**
`result.exit_code == 0`; `result.output` stripped equals `"Project closed"`; `close_project` was called once.
**Verification Criteria:**
Pass if exit code is 0, output is `"Project closed"`, and `close_project.call_count == 1`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00020: element add Command Dispatches on Type

**ID:** UTS_CLI_00020
**Traces-To:** SWR_CLI_00007
**Title:** element add dispatches class/actor to the matching root.addX method
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `element add --type {class|actor} --name N` calls `root.addClass(N)` or `root.addActor(N)` respectively, and echoes `"Created {type}: {name}"`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context whose `project` is a `MagicMock` exposing `getRoot()` returning a fake root with `addClass`/`addActor` spies.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` as above.
2. Invoke `cli` with `["element","add","--type","class","--name","C1"]` and assert `root.addClass.call_args == call("C1")` and output contains `"Created class: C1"`.
3. Invoke `cli` with `["element","add","--type","actor","--name","A1"]` and assert `root.addActor.call_args == call("A1")`.
**Expected Result:**
Each invocation dispatches to the matching `addX` method with the supplied name and echoes the success message.
**Verification Criteria:**
Pass if both add methods are called with the right names and the output contains the success messages.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00021: element add Command Case-Insensitive Type

**ID:** UTS_CLI_00021
**Traces-To:** SWR_CLI_00007
**Title:** element add matches element type case-insensitively
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that the dispatch uses `element_type.lower()`, so `"Class"`, `"CLASS"`, and `"class"` all dispatch to `root.createClass`.
**Pre-conditions:**
- Same fake context as UTS_CLI_00020.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context.
2. Invoke `cli` with `["element","add","--type","Class","--name","X"]` and assert `root.createClass.call_args == call("X")`.
3. Invoke `cli` with `["element","add","--type","CLASS","--name","Y"]` and assert `root.createClass.call_args == call("Y")`.
**Expected Result:**
Both invocations dispatch to `createClass` regardless of case.
**Verification Criteria:**
Pass if `createClass` is called with `"X"` then `"Y"`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00022: element add Command Rejects Unknown Type

**ID:** UTS_CLI_00022
**Traces-To:** SWR_CLI_00007
**Title:** element add aborts with an error for an unknown element type
**Type:** Unit
**Priority:** High
**Description:**
Verifies that an `--type` value other than `class`/`actor` (case-insensitive) echoes `"Error: Unknown element type '{type}'"` to stderr and aborts with a non-zero exit code, without calling any `addX` method.
**Pre-conditions:**
- Same fake context as UTS_CLI_00020.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context.
2. Invoke `cli` with `["element","add","--type","widget","--name","X"]` via `CliRunner`.
3. Inspect `result.exit_code` and error output; inspect call counts on `addClass`/`addActor`.
**Expected Result:**
`result.exit_code != 0`; error output contains `"Error: Unknown element type 'widget'"`; none of the `addX` methods were called.
**Verification Criteria:**
Pass if exit code is non-zero, the error message matches, and no `addX` was called.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00023: element add Command Requires an Active Project

**ID:** UTS_CLI_00023
**Traces-To:** SWR_CLI_00007
**Title:** element add aborts with an error when no active project exists
**Type:** Unit
**Priority:** High
**Description:**
Verifies that when `ctx.project is None`, `element add` echoes `"Error: No active project. Use 'project open' first."` to stderr and aborts without calling any `createX` method.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project = None`.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `project = None`.
2. Invoke `cli` with `["element","add","--type","class","--name","X"]` via `CliRunner`.
3. Inspect `result.exit_code` and error output.
**Expected Result:**
`result.exit_code != 0`; error output contains `"No active project"` and `"project open"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains both substrings.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00024: element view Command Outputs JSON When output_format Is json

**ID:** UTS_CLI_00024
**Traces-To:** SWR_CLI_00008
**Title:** element view emits a JSON object when ctx.output_format == "json"
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that `element view --path P` builds the demo data dict and emits it via `OutputFormatter.json_format` when `output_format == "json"`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project = MagicMock()` (truthy) and `output_format = "json"`.
- `OutputFormatter.json_format` patched as a spy returning a sentinel string.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context with `output_format = "json"`.
2. Patch `rhapsody_cli.cli.commands.element.OutputFormatter.json_format` to return `"{...}"`.
3. Invoke `cli` with `["element","view","--path","Root::C1"]` via `CliRunner`.
4. Inspect `result.exit_code`, `result.output`, and the `json_format` call args.
**Expected Result:**
`result.exit_code == 0`; output is the sentinel string; `json_format` was called with a dict containing `"path": "Root::C1"`, `"type": "unknown"`, and a `"properties"` key.
**Verification Criteria:**
Pass if exit code is 0, `json_format` was called once, and its argument dict contains the expected keys/values.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00025: element view Command Outputs Table Otherwise

**ID:** UTS_CLI_00025
**Traces-To:** SWR_CLI_00008
**Title:** element view emits a two-row table when output_format is not "json"
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that when `output_format != "json"` (e.g., `"table"`), `element view --path P` emits a two-row table via `OutputFormatter.table` with headers `["Property", "Value"]` and rows `[["path", P], ["type", "unknown"]]`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project = MagicMock()` and `output_format = "table"`.
- `OutputFormatter.table` patched as a spy returning a sentinel string.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context with `output_format = "table"`.
2. Patch `rhapsody_cli.cli.commands.element.OutputFormatter.table` to return a sentinel.
3. Invoke `cli` with `["element","view","--path","Root::C1"]` via `CliRunner`.
4. Inspect `result.exit_code` and the `table` call args.
**Expected Result:**
`result.exit_code == 0`; `table` was called with headers `["Property", "Value"]` and rows `[["path", "Root::C1"], ["type", "unknown"]]`.
**Verification Criteria:**
Pass if exit code is 0 and `table` call args match the expected headers/rows.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00026: element view Command Requires an Active Project

**ID:** UTS_CLI_00026
**Traces-To:** SWR_CLI_00008
**Title:** element view aborts with an error when no active project exists
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that when `ctx.project is None`, `element view` echoes `"Error: No active project"` to stderr and aborts.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project = None`.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `project = None`.
2. Invoke `cli` with `["element","view","--path","Root::C1"]` via `CliRunner`.
3. Inspect `result.exit_code` and error output.
**Expected Result:**
`result.exit_code != 0`; error output contains `"No active project"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains the substring.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00027: element query Command Outputs JSON When output_format Is json

**ID:** UTS_CLI_00027
**Traces-To:** SWR_CLI_00009
**Title:** element query emits a JSON object with an elements array when output_format is json
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `element query [--filter F]` fetches `root.getNestedElements()` and, when `output_format == "json"`, emits `{"elements": [{"name": ..., "type": ...}, ...]}` via `OutputFormatter.json_format`.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project` whose `getRoot()` returns a fake root whose `getNestedElements()` returns an iterable of two fake elements (`getName`/`getMetaClass` configured).
- `output_format = "json"` on the fake context.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context.
2. Invoke `cli` with `["element","query"]` via `CliRunner`.
3. Inspect `result.exit_code` and `result.output`; parse the output as JSON.
**Expected Result:**
`result.exit_code == 0`; the parsed JSON has an `"elements"` key whose value is a list of two objects each with `"name"` and `"type"`.
**Verification Criteria:**
Pass if exit code is 0, the output is valid JSON, and the parsed object matches the expected structure with two elements.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00028: element query Command Outputs Table Otherwise

**ID:** UTS_CLI_00028
**Traces-To:** SWR_CLI_00009
**Title:** element query emits a table with Name/Type columns when output_format is not json
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `output_format != "json"`, `element query` emits a table via `OutputFormatter.table` with headers `["Name", "Type"]` and one row per nested element.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `output_format = "table"` and a fake root returning two fake elements.
- `OutputFormatter.table` patched as a spy.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context with `output_format = "table"`.
2. Patch `rhapsody_cli.cli.commands.element.OutputFormatter.table` as a spy.
3. Invoke `cli` with `["element","query"]` via `CliRunner`.
4. Inspect `result.exit_code` and the `table` call args.
**Expected Result:**
`result.exit_code == 0`; `table` was called with headers `["Name", "Type"]` and a rows list of length 2.
**Verification Criteria:**
Pass if exit code is 0 and `table` call args match the expected headers and row count.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00029: element query Command Accepts Optional --filter

**ID:** UTS_CLI_00029
**Traces-To:** SWR_CLI_00009
**Title:** element query accepts an optional --filter option without error
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that the `--filter` option is optional (default `None`) and that supplying it does not cause a parameter error (the command still runs the happy path).
**Pre-conditions:**
- Same fake context as UTS_CLI_00027.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return the fake context.
2. Invoke `cli` with `["element","query","--filter","Class"]` via `CliRunner`.
3. Inspect `result.exit_code`.
**Expected Result:**
`result.exit_code == 0`; the command accepts the `--filter` option and runs to completion.
**Verification Criteria:**
Pass if exit code is 0 (no Click usage error from a missing/unknown option).
**Last Changed:** 2026-07-07

---

## UTS_CLI_00030: element query Command Requires an Active Project

**ID:** UTS_CLI_00030
**Traces-To:** SWR_CLI_00009
**Title:** element query aborts with an error when no active project exists
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `ctx.project is None`, `element query` echoes `"Error: No active project"` to stderr and aborts.
**Pre-conditions:**
- `RhapsodyContext` patched to return a fake context with `project = None`.
- `CliRunner` available.
**Test Steps:**
1. Patch `RhapsodyContext` to return a fake context with `project = None`.
2. Invoke `cli` with `["element","query"]` via `CliRunner`.
3. Inspect `result.exit_code` and error output.
**Expected Result:**
`result.exit_code != 0`; error output contains `"No active project"`.
**Verification Criteria:**
Pass if exit code is non-zero and the error output contains the substring.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00037: OutputFormatter.table Returns "(no data)" For Empty Rows

**ID:** UTS_CLI_00037
**Traces-To:** SWR_CLI_00012
**Title:** OutputFormatter.table returns "(no data)" when rows is empty
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the empty-rows branch of `OutputFormatter.table`: when `rows` is `[]`, the method returns exactly `"(no data)"` and does not invoke `tabulate`.
**Pre-conditions:**
- `tabulate` patched as a spy (so the test can confirm it is not called).
**Test Steps:**
1. Patch `rhapsody_cli.cli.formatters.tabulate` as a spy.
2. Call `OutputFormatter.table(["Name"], [])`.
3. Inspect the return value and `tabulate.call_count`.
**Expected Result:**
The return value is exactly `"(no data)"`; `tabulate` was not called.
**Verification Criteria:**
Pass if the return value is `"(no data)"` and `tabulate.call_count == 0`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00038: OutputFormatter.table Delegates to tabulate With grid Format

**ID:** UTS_CLI_00038
**Traces-To:** SWR_CLI_00012
**Title:** OutputFormatter.table delegates to tabulate(rows, headers=headers, tablefmt="grid")
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that when `rows` is non-empty, `OutputFormatter.table` calls `tabulate(rows, headers=headers, tablefmt="grid")` and returns `str(...)` of its result.
**Pre-conditions:**
- `tabulate` patched to return a sentinel object (not a str) so `str(...)` is exercised.
**Test Steps:**
1. Patch `rhapsody_cli.cli.formatters.tabulate` to return a sentinel object `Sentinel` whose `str()` is `"<table>"`.
2. Call `OutputFormatter.table(["Name", "Type"], [["C1", "Class"]])`.
3. Inspect the return value and `tabulate` call args.
**Expected Result:**
The return value is `"<table>"` (the `str()` of the sentinel); `tabulate` was called once with `rows=[["C1","Class"]]`, `headers=["Name","Type"]`, `tablefmt="grid"`.
**Verification Criteria:**
Pass if the return value matches `str(sentinel)` and `tabulate.call_args` matches the expected kwargs.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00039: OutputFormatter.json_format Serializes With Indent 2 and default=str

**ID:** UTS_CLI_00039
**Traces-To:** SWR_CLI_00013
**Title:** OutputFormatter.json_format returns json.dumps(data, indent=2, default=str)
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `OutputFormatter.json_format(data)` produces the same output as `json.dumps(data, indent=2, default=str)`, including for non-serializable values that fall back to `str()`.
**Pre-conditions:**
- `json` from the stdlib available for comparison.
- A sample data dict containing a non-serializable value (e.g., a `datetime` or a custom object).
**Test Steps:**
1. Build `data = {"a": 1, "b": [1, 2, 3], "obj": object()}`.
2. Call `OutputFormatter.json_format(data)`.
3. Compute `expected = json.dumps(data, indent=2, default=str)`.
4. Compare the two strings.
5. Confirm the output contains the `str()` representation of the `object()` instance.
**Expected Result:**
The two strings are identical; the non-serializable `object()` was rendered via `str()`.
**Verification Criteria:**
Pass if `result == expected` and the output contains `str(object())`-style text.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00040: OutputFormatter.csv_format Writes Headers Then Rows

**ID:** UTS_CLI_00040
**Traces-To:** SWR_CLI_00014
**Title:** OutputFormatter.csv_format writes the header row followed by all data rows
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `OutputFormatter.csv_format(headers, rows)` writes the header row first, then each data row, using `csv.writer`, and returns the resulting CSV string.
**Pre-conditions:**
- `csv` and `io` from the stdlib available for comparison.
- Sample headers and rows.
**Test Steps:**
1. Call `OutputFormatter.csv_format(["Name", "Type"], [["C1", "Class"], ["A1", "Actor"]])`.
2. Parse the result with `csv.reader(io.StringIO(result))` to obtain a list of rows.
3. Inspect the parsed rows.
**Expected Result:**
The parsed rows are `[["Name", "Type"], ["C1", "Class"], ["A1", "Actor"]]` (header first, then data rows in order).
**Verification Criteria:**
Pass if the parsed rows exactly match the expected list.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00041: OutputFormatter.csv_format Empty Rows Still Writes Header

**ID:** UTS_CLI_00041
**Traces-To:** SWR_CLI_00014
**Title:** OutputFormatter.csv_format writes the header even when rows is empty
**Type:** Unit
**Priority:** Low
**Description:**
Verifies the boundary case: when `rows` is `[]`, `csv_format` still writes the header row and returns a CSV string containing only that header.
**Pre-conditions:**
- `csv` and `io` available for parsing.
**Test Steps:**
1. Call `OutputFormatter.csv_format(["Name", "Type"], [])`.
2. Parse the result with `csv.reader(io.StringIO(result))`.
3. Inspect the parsed rows.
**Expected Result:**
The parsed rows are `[["Name", "Type"]]` (only the header row).
**Verification Criteria:**
Pass if the parsed rows equal `[["Name", "Type"]]`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00042: OutputFormatter.format Routes to json_format

**ID:** UTS_CLI_00042
**Traces-To:** SWR_CLI_00015
**Title:** OutputFormatter.format routes to json_format when format_type == "json"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `OutputFormatter.format(data, "json")` calls `json_format(data)` and returns its result, ignoring the `headers` argument.
**Pre-conditions:**
- `OutputFormatter.json_format` patched as a spy returning a sentinel.
**Test Steps:**
1. Patch `rhapsody_cli.cli.formatters.OutputFormatter.json_format` to return `"<json>"`.
2. Call `OutputFormatter.format({"a": 1}, "json", headers=["A"])`.
3. Inspect the return value and `json_format` call args.
**Expected Result:**
The return value is `"<json>"`; `json_format` was called once with `{"a": 1}`.
**Verification Criteria:**
Pass if the return value is the sentinel and `json_format.call_args == call({"a": 1})`.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00043: OutputFormatter.format Routes to csv_format Coercing Data to List

**ID:** UTS_CLI_00043
**Traces-To:** SWR_CLI_00015
**Title:** OutputFormatter.format routes to csv_format when format_type == "csv" and coerces non-list data
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `OutputFormatter.format(data, "csv", headers=H)` calls `csv_format(H, rows)` where `rows = data if isinstance(data, list) else [data]`. When `headers` is None it defaults to `[]`.
**Pre-conditions:**
- `OutputFormatter.csv_format` patched as a spy returning a sentinel.
- Two sample data inputs: a list and a non-list (e.g., a dict).
**Test Steps:**
1. Patch `csv_format` to return `"<csv>"`.
2. Call `OutputFormatter.format([["a", 1]], "csv", headers=["H1", "H2"])` and inspect call args (rows should be the list as-is).
3. Call `OutputFormatter.format({"a": 1}, "csv", headers=["H1"])` and inspect call args (rows should be `[{"a": 1}]`).
4. Call `OutputFormatter.format({"a": 1}, "csv")` and inspect call args (headers should be `[]`).
**Expected Result:**
For the list input, `csv_format` is called with `(["H1","H2"], [["a", 1]])`. For the dict input, with `(["H1"], [{"a": 1}])`. With no headers, with `([], [{"a": 1}])`.
**Verification Criteria:**
Pass if all three `csv_format` call args match the expected coercion behavior.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00044: OutputFormatter.format Routes to table Coercing Data to List

**ID:** UTS_CLI_00044
**Traces-To:** SWR_CLI_00015
**Title:** OutputFormatter.format routes to table for any other format_type and coerces non-list data
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that for any `format_type` not equal to `"json"` or `"csv"` (including `"table"` and unknown values), `OutputFormatter.format` routes to `table(headers, rows)` with the same list-coercion as the csv branch.
**Pre-conditions:**
- `OutputFormatter.table` patched as a spy returning a sentinel.
**Test Steps:**
1. Patch `table` to return `"<table>"`.
2. Call `OutputFormatter.format([["a", 1]], "table", headers=["H1", "H2"])` and inspect call args.
3. Call `OutputFormatter.format({"a": 1}, "table", headers=["H1"])` and inspect call args (rows should be `[{"a": 1}]`).
4. Call `OutputFormatter.format({"a": 1}, "weird-unknown", headers=["H1"])` and inspect call args (still routes to `table`).
**Expected Result:**
All three invocations route to `table` with the expected coercion: list input passed as-is, non-list input wrapped in a list.
**Verification Criteria:**
Pass if `table` is called three times with the expected headers/rows in each case.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00045: Class-Based Command Architecture Inheritance

**ID:** UTS_CLI_00045
**Traces-To:** SWR_CLI_00016
**Title:** Each command class extends click.Command (or a project/element/io base) which extends click.Command
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that every concrete command class (`OpenProjectCommand`, `ListProjectsCommand`, `CloseProjectCommand`, `AddElementCommand`, `ViewElementCommand`, `QueryElementCommand`) is a subclass of `click.Command` (directly or via `BaseProjectCommand`/`BaseElementCommand`), and that those base classes themselves subclass `click.Command`.
**Pre-conditions:**
- All command modules imported.
**Test Steps:**
1. Import each command class and the two base classes.
2. Assert `issubclass(BaseProjectCommand, click.Command)`, `issubclass(BaseElementCommand, click.Command)`.
3. Assert each of the six concrete command classes is a subclass of `click.Command` (and the appropriate base).
**Expected Result:**
All base classes subclass `click.Command`; all concrete commands subclass their respective base (and transitively `click.Command`).
**Verification Criteria:**
Pass if all `issubclass` assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00046: Class-Based Command Architecture __init__ Configuration

**ID:** UTS_CLI_00046
**Traces-To:** SWR_CLI_00016
**Title:** Each command __init__ configures name, help, callback=self.execute, and params
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that each command's `__init__` calls `super().__init__` with `name`, `help`, `callback=self.execute`, and a non-empty `params` list (or empty list where appropriate). Verifies that `callback is instance.execute`.
**Pre-conditions:**
- All command classes imported.
**Test Steps:**
1. Instantiate each command class (e.g., `OpenProjectCommand()`).
2. For each instance, assert `cmd.name` matches the expected short name (e.g., `"open"`, `"list"`, `"close"`, `"add"`, `"view"`, `"query"`, `"import"`, `"export"`).
3. Assert `cmd.help` is a non-empty string.
4. Assert `cmd.callback == cmd.execute` (the bound method).
5. Assert `cmd.params` is a list of `click.Parameter` instances matching the expected count for that command.
**Expected Result:**
Each command is configured with the correct name, help, callback bound to `self.execute`, and the expected parameters.
**Verification Criteria:**
Pass if every name/help/callback/params assertion holds for all eight command classes.
**Last Changed:** 2026-07-07

---

## UTS_CLI_00047: Command Group Subclasses click.Group and Registers Commands

**ID:** UTS_CLI_00047
**Traces-To:** SWR_CLI_00016
**Title:** ProjectCommandGroup/ElementCommandGroup/IOCommandGroup subclass click.Group and register their commands
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `ProjectCommandGroup`, `ElementCommandGroup`, and `IOCommandGroup` each subclass `click.Group`, set the expected `name` (`project`/`element`/`io`), and register their respective subcommands in `__init__`.
**Pre-conditions:**
- All command modules imported.
**Test Steps:**
1. Instantiate `ProjectCommandGroup()`, `ElementCommandGroup()`, `IOCommandGroup()` (or use the module-level singletons `project`, `element`, `io`).
2. For each, assert `isinstance(group, click.Group)`.
3. Assert `group.name` is `"project"`/`"element"`/`"io"`.
4. Assert `group.commands` contains the expected subcommand names: project -> `{"open","list","close"}`, element -> `{"add","view","query"}`, io -> `{"import","export"}`.
**Expected Result:**
All three groups are `click.Group` subclasses with the right names and the right registered subcommands.
**Verification Criteria:**
Pass if all type/name/subcommand assertions hold.
**Last Changed:** 2026-07-07
