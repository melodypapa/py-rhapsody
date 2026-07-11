# Integration Test Specifications - Command-Line Interface

**Category:** CLI
**Prefix:** ITS
**Test Type:** Integration
**Last Validated:** 2026-07-07

---

## ITS_CLI_00001: cli group wires --output option to RhapsodyContext.output_format

**ID:** ITS_CLI_00001
**Traces-To:** SWR_CLI_00001, SWR_CLI_00002, SWR_CLI_00003
**Title:** CliRunner invokes the cli group; --output stores the format on ctx.obj.output_format
**Type:** Integration
**Priority:** High
**Description:**
Verifies the integration between the `cli` Click group, the `--output` option, and the
`RhapsodyContext` it constructs. When no context exists, a new `RhapsodyContext` is created and
`ctx.obj.output_format` reflects the `--output` choice (default `"table"`). Confirms the `project`,
`element`, and `io` subgroups are registered as commands of `cli`.
**Pre-conditions:**
- `click.testing.CliRunner` available.
- `rhapsody_cli.cli.main.cli` imported.
- No real Rhapsody connection required (subcommands not invoked).
**Test Steps:**
1. `runner = CliRunner()`.
2. `result = runner.invoke(cli, ["--help"])`.
3. Assert `result.exit_code == 0` and the help text lists `project`, `element`, and `io` as
   subcommands, and `--output` as an option with choices `table`, `json`, `csv`.
4. `result = runner.invoke(cli, ["--output", "json", "--help"])`; assert exit code 0.
5. Use an introspection command (or a stub subcommand) to confirm `ctx.obj.output_format ==
   "json"` after the group callback runs with `--output json`.
6. Confirm the default (`--output` omitted) yields `ctx.obj.output_format == "table"`.
**Expected Result:**
The `cli` group constructs a `RhapsodyContext`, propagates the `--output` choice to
`output_format`, and registers all three subcommand groups.
**Verification Criteria:**
- `--help` output contains `project`, `element`, `io`, and `--output`.
- `--output` choices include `table`, `json`, `csv`.
- `ctx.obj.output_format == "json"` when `--output json` is passed.
- `ctx.obj.output_format == "table"` when `--output` is omitted.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00002: project open command drives context connect and OpenProjectCommand

**ID:** ITS_CLI_00002
**Traces-To:** SWR_CLI_00004, SWR_CLI_00003
**Title:** project open <path> connects via attach, opens the project, and echoes "Opened project: {path}"
**Type:** Integration
**Priority:** High
**Description:**
Verifies end-to-end integration of the `project open` command: it constructs a `RhapsodyContext`,
calls `connect(method="attach")`, calls `open_project(path)`, and echoes `"Opened project: {path}"`.
`RhapsodyContext.open_project` must lazily connect if `app` is None, then delegate to
`RhapsodyApplication.openProject` and store the resulting `RPProject` on `ctx.project`.
**Pre-conditions:**
- `CliRunner` available.
- `RhapsodyApplication.connect` patched to return a `RhapsodyApplication` wrapping a mock COM app
  whose `openProject` returns a mock COM project (`getMetaClass() == "Project"`).
- A real temporary file on disk to satisfy the path-exists validator (content irrelevant).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "open", str(tmp_path)])`.
2. Assert `result.exit_code == 0`.
3. Assert `"Opened project:"` is present in `result.output` and the echoed path matches
   `str(tmp_path)`.
4. Assert (via spy) that `RhapsodyApplication.connect` was called with `method="attach"`.
5. Assert (via spy) that the mock app's `openProject` was called with `str(tmp_path)`.
6. Assert the resulting `RPProject` ended up on `ctx.project` (introspect via a follow-up command
   or a captured context object).
**Expected Result:**
`project open` performs the full connect → open → echo sequence; the wrapped `RPProject` is stored
on the context for subsequent commands.
**Verification Criteria:**
- `result.exit_code == 0`.
- `result.output` contains `Opened project:` and the path.
- `connect` called with `method="attach"`.
- `openProject` called with the supplied path.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00003: project list command formats open projects as a table

**ID:** ITS_CLI_00003
**Traces-To:** SWR_CLI_00005, SWR_CLI_00012, SWR_CLI_00015
**Title:** project list routes open projects through OutputFormatter.table via the format router
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies integration of `ListProjectsCommand.execute` with `RhapsodyContext.connect`,
`RhapsodyApplication.getProjects` (returning an `RPCollection` of `RPProject`), and
`OutputFormatter.table`. The default `--output table` format must produce an ASCII grid table
containing each project's name and path.
**Pre-conditions:**
- `CliRunner` available.
- `RhapsodyApplication.connect` patched to return an app whose `getProjects` returns an
  `RPCollection` of two mock `RPProject` objects with names `"P1"` and `"P2"`.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "list"])`.
2. Assert `result.exit_code == 0`.
3. Assert `result.output` contains a tabulated grid with both project names `"P1"` and `"P2"`.
4. Assert `OutputFormatter.table` (or the format router) was invoked with headers including
   `Name` (or equivalent) and a rows list of length 2.
**Expected Result:**
The list command retrieves open projects, routes them through `OutputFormatter.table`, and prints
an ASCII grid containing both project entries.
**Verification Criteria:**
- `result.exit_code == 0`.
- `result.output` contains `"P1"` and `"P2"`.
- `result.output` contains a grid-style table (e.g., `+` border characters).
**Last Changed:** 2026-07-07

---

## ITS_CLI_00004: project list with no open projects echoes "No open projects"

**ID:** ITS_CLI_00004
**Traces-To:** SWR_CLI_00005
**Title:** project list prints "No open projects" when getProjects returns an empty collection
**Type:** Integration
**Priority:** Low
**Description:**
Verifies the empty-collection branch of `ListProjectsCommand.execute`: when
`RhapsodyApplication.getProjects()` returns an `RPCollection` of length 0, the command must echo
`"No open projects"` and exit cleanly without invoking the formatter.
**Pre-conditions:**
- `CliRunner` available.
- `RhapsodyApplication.connect` patched to return an app whose `getProjects` returns an
  `RPCollection` with `getCount() == 0`.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "list"])`.
2. Assert `result.exit_code == 0`.
3. Assert `result.output` contains the exact string `"No open projects"`.
4. Assert (via spy) that `OutputFormatter.table` was NOT called (empty branch short-circuits).
**Expected Result:**
The command prints the no-projects message and does not invoke the table formatter.
**Verification Criteria:**
- `result.exit_code == 0`.
- `"No open projects"` substring present in `result.output`.
- `OutputFormatter.table` call count is 0.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00005: Context state transitions connect → open → close → disconnect

**ID:** ITS_CLI_00005
**Traces-To:** SWR_CLI_00003, SWR_CLI_00006
**Title:** RhapsodyContext drives connect, open_project, close_project, and disconnect in sequence
**Type:** Integration
**Priority:** High
**Description:**
Verifies the `RhapsodyContext` state machine integrates correctly with the underlying
`RhapsodyApplication` and `RPProject` lifecycles. After `connect`, `app` is set; after
`open_project`, `project` is set; after `close_project`, `project` is None but `app` remains;
after `disconnect`, both are None and the app's `quit()` was called.
**Pre-conditions:**
- A mock `RhapsodyApplication` whose `openProject` returns a mock `RPProject` whose `close()` is a
  spy.
- `RhapsodyApplication.quit` is a spy.
- `RhapsodyApplication.connect` patched to return the mock app.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `ctx = RhapsodyContext()`.
2. Assert `ctx.app is None` and `ctx.project is None`.
3. `ctx.connect(method="attach")`; assert `ctx.app is mock_app`.
4. `ctx.open_project("model.rpy")`; assert `ctx.project is mock_project` and `mock_app.openProject`
   was called with `"model.rpy"`.
5. `ctx.close_project()`; assert `ctx.project is None`, `ctx.app is mock_app` (still connected),
   and `mock_project.close` was called once.
6. `ctx.disconnect()`; assert `ctx.project is None`, `ctx.app is None`, and `mock_app.quit` was
   called once.
**Expected Result:**
The context transitions through all four states cleanly, delegating to the application and
project wrappers at each step and clearing references on close/disconnect.
**Verification Criteria:**
- After `connect`: `ctx.app is mock_app`.
- After `open_project`: `ctx.project is mock_project`.
- After `close_project`: `ctx.project is None`, `mock_project.close.call_count == 1`.
- After `disconnect`: `ctx.app is None`, `mock_app.quit.call_count == 1`.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00006: element add command dispatches by --type to root creation methods

**ID:** ITS_CLI_00006
**Traces-To:** SWR_CLI_00007, SWR_CLI_00016
**Title:** element add --type {class,actor,package} dispatches to root.createClass/createActor/createPackage
**Type:** Integration
**Priority:** High
**Description:**
Verifies `AddElementCommand.execute` integrates with the active `RPProject`'s root and dispatches
correctly based on `--type`. The class-based command architecture must wire `--type` and `--name`
params to the callback, require an active project, and echo `"Created {type}: {name}"` on success.
Unknown types must abort.
**Pre-conditions:**
- `CliRunner` available.
- A `RhapsodyContext` with `project` set to a mock `RPProject` whose root exposes spies
  `createClass`, `createActor`, `createPackage` (each returning a wrapped new element).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["element", "add", "--type", "class", "--name", "Foo"])`.
2. Assert `result.exit_code == 0` and `result.output` contains `"Created class: Foo"`.
3. Assert `root.createClass` was called with `"Foo"`.
4. Repeat with `--type actor --name Bar`; assert `root.createActor` called with `"Bar"`.
5. Repeat with `--type package --name Pkg`; assert `root.createPackage` called with `"Pkg"`.
6. `result = runner.invoke(cli, ["element", "add", "--type", "widget", "--name", "X"])`; assert
   `result.exit_code != 0` and the output mentions an unknown/unsupported type.
7. With no active project (`ctx.project = None`), assert the command echoes an error and aborts.
**Expected Result:**
The command dispatches to the correct root creation method per `--type`, echoes the success
message, rejects unknown types, and aborts when no project is active.
**Verification Criteria:**
- `root.createClass.call_args == (("Foo",),)` for the class case.
- `root.createActor.call_args == (("Bar",),)` for the actor case.
- `root.createPackage.call_args == (("Pkg",),)` for the package case.
- Unknown type and no-project cases produce non-zero exit codes.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00007: --output json routes element query through OutputFormatter.json_format

**ID:** ITS_CLI_00007
**Traces-To:** SWR_CLI_00002, SWR_CLI_00009, SWR_CLI_00013, SWR_CLI_00015
**Title:** element query --output json emits a JSON object with an "elements" array
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the full formatter chain: `--output json` sets `ctx.obj.output_format = "json"`;
`QueryElementCommand.execute` reads this attribute and routes the data through
`OutputFormatter.format(data, "json")`, which delegates to `OutputFormatter.json_format`,
producing `json.dumps(data, indent=2, default=str)`. The emitted JSON must contain an `elements`
array where each element has `name` and `type` keys.
**Pre-conditions:**
- `CliRunner` available.
- A `RhapsodyContext` with `project` set to a mock `RPProject` whose root returns nested elements
  (e.g., two elements named `"A"` and `"B"` of types `"Class"` and `"Actor"`).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["--output", "json", "element", "query"])`.
2. Assert `result.exit_code == 0`.
3. Parse `result.output` as JSON (stripping any non-JSON prefix/suffix if the command mixes
   messages).
4. Assert the parsed object has an `"elements"` key whose value is a list of length 2.
5. Assert each element in the list has `"name"` and `"type"` keys.
6. Assert `OutputFormatter.json_format` was called (via spy) with data containing the two
   elements.
**Expected Result:**
The `--output json` option propagates from the `cli` group through the command to the formatter
router, which selects `json_format` and emits valid indented JSON with the expected schema.
**Verification Criteria:**
- `result.exit_code == 0`.
- `result.output` is parseable as JSON (after stripping any leading log lines).
- Parsed JSON has `elements` array of length 2; each item has `name` and `type`.
- `OutputFormatter.json_format` spy called once.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00008: --output csv routes element query through OutputFormatter.csv_format

**ID:** ITS_CLI_00008
**Traces-To:** SWR_CLI_00002, SWR_CLI_00009, SWR_CLI_00014, SWR_CLI_00015
**Title:** element query --output csv writes a CSV with Name and Type columns
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies the CSV formatter branch: `--output csv` causes `OutputFormatter.format(data, "csv")`
to coerce `data` to a list and delegate to `OutputFormatter.csv_format(headers, rows)`, which uses
`csv.writer` over a `StringIO`. The emitted CSV must start with a header row `Name,Type` followed
by one row per element.
**Pre-conditions:**
- `CliRunner` available.
- A `RhapsodyContext` with `project` set to a mock `RPProject` whose root returns two nested
  elements.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["--output", "csv", "element", "query"])`.
2. Assert `result.exit_code == 0`.
3. Split `result.output` into lines and parse with `csv.reader`.
4. Assert the first row is `["Name", "Type"]`.
5. Assert there are exactly two data rows, each with two columns.
6. Assert `OutputFormatter.csv_format` was called (via spy) with headers `["Name", "Type"]` and a
   rows list of length 2.
**Expected Result:**
The CSV formatter is selected by `--output csv`; the output is valid CSV with the expected header
and one row per element.
**Verification Criteria:**
- `result.exit_code == 0`.
- First CSV row is `["Name", "Type"]`.
- Exactly two data rows follow, each with two columns.
- `OutputFormatter.csv_format` spy called once with the expected headers and rows count.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00009: io export command echoes progress and success messages

**ID:** ITS_CLI_00009
**Traces-To:** SWR_CLI_00011
**Title:** io export <output> --format xmi prints progress lines and "✓ Export completed: {output}"
**Type:** Integration
**Priority:** Low
**Description:**
Verifies `ExportCommand.execute` integrates with the active project requirement and emits the
documented progress messages: `"Exporting to {output} as {format}..."`, a format-dependency note,
and `"✓ Export completed: {output}"`. Confirms the `--format` default is `"xmi"`.
**Pre-conditions:**
- `CliRunner` available.
- A `RhapsodyContext` with `project` set (active project present).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `result = runner.invoke(cli, ["io", "export", "out.xmi"])`.
2. Assert `result.exit_code == 0`.
3. Assert `result.output` contains `"Exporting to out.xmi as xmi..."`.
4. Assert `result.output` contains `"✓ Export completed: out.xmi"`.
5. `result = runner.invoke(cli, ["io", "export", "out.json", "--format", "json"])`; assert the
   progress line says `"as json"`.
6. With no active project, assert the command echoes an error and aborts (non-zero exit).
**Expected Result:**
The export command prints the expected progress messages with the correct `--format` substitution
and aborts when no project is active.
**Verification Criteria:**
- `result.exit_code == 0` when a project is active.
- `result.output` contains `"Exporting to out.xmi as xmi..."` (default format).
- `result.output` contains `"✓ Export completed: out.xmi"`.
- `--format json` produces `"as json"` in the progress line.
- No-project case: non-zero exit code.
**Last Changed:** 2026-07-07

---

## ITS_CLI_00010: Connection error during project open propagates to click.Abort

**ID:** ITS_CLI_00010
**Traces-To:** SWR_CLI_00004, SWR_EXC_00002
**Title:** RhapsodyConnectionError from connect() is caught by project open and surfaced as click.Abort
**Type:** Integration
**Priority:** High
**Description:**
Verifies cross-layer error integration: when `RhapsodyContext.connect` raises
`RhapsodyConnectionError` (because `attach()` and `launch()` both fail), the `project open`
command must catch it, echo the error message to stderr, and raise `click.Abort`, producing a
non-zero exit code from `CliRunner`. No raw `RhapsodyConnectionError` or
`pywintypes.com_error` should escape to the test runner.
**Pre-conditions:**
- `CliRunner` available.
- `RhapsodyApplication.connect` patched to raise
  `RhapsodyConnectionError("No running Rhapsody instance found: test")`.
- A real temp file on disk for the path validator.
**Test Steps:**
1. `result = runner.invoke(cli, ["project", "open", str(tmp_path)])`.
2. Assert `result.exit_code != 0`.
3. Assert the error text (e.g., `"No running Rhapsody instance found"`) appears in `result.output`
   or the captured stderr.
4. Assert `RhapsodyApplication.openProject` was NOT called (connect failed before open).
5. Assert `result.exception` is `click.Abort` (or `SystemAbort`) — NOT a raw
   `RhapsodyConnectionError`.
**Expected Result:**
The connection error is contained within the command layer: it is logged to stderr and converted
to `click.Abort`; `CliRunner` reports a non-zero exit code.
**Verification Criteria:**
- `result.exit_code != 0`.
- Error message text present in output/stderr.
- `result.exception` is `click.Abort` (or its `SystemAbort` subclass), not
  `RhapsodyConnectionError`.
- `openProject` spy call count is 0.
**Last Changed:** 2026-07-07
