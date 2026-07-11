# System Test Specifications - Command-Line Interface

**Category:** CLI
**Prefix:** SYTS
**Test Type:** System
**Last Validated:** 2026-07-07

---

## SYTS_CLI_00001: Full Project Lifecycle via CLI (Open, List, Close)

**ID:** SYTS_CLI_00001
**Traces-To:** SWR_CLI_00001, SWR_CLI_00003, SWR_CLI_00004, SWR_CLI_00005, SWR_CLI_00006
**Title:** End-to-end project open, list, and close command flow
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end CLI project lifecycle using click's CliRunner against a
fake Rhapsody COM layer: opening a project file, listing open projects (confirming the
opened project appears), and closing the active project. It exercises the `cli` group,
`RhapsodyContext` session management, and the `project open/list/close` commands.
**Pre-conditions:**
- A fake `win32com.client` layer returning a fake `Rhapsody.Application` whose
  `openProject(path)` returns a fake `IRPProject` named "Sample" and whose
  `getProjects()` returns a fake `IRPCollection` containing that project.
- A temp file on disk to satisfy the `project_path` existence validation.
- CliRunner available; the `cli` entry point importable.
**Test Steps:**
1. Invoke `rhapsody project open <temp_path>` via CliRunner and capture stdout/stderr and
   exit code.
2. Invoke `rhapsody project list` via CliRunner and capture output.
3. Invoke `rhapsody project close` via CliRunner and capture output.
4. Invoke `rhapsody project list` again and capture output.
**Expected Result:**
- Step 1 exits 0 and stdout contains "Opened project: <temp_path>".
- Step 2 exits 0 and stdout contains a table including the project name "Sample".
- Step 3 exits 0 and stdout contains "Project closed".
- Step 4 exits 0 and stdout contains "No open projects".
**Verification Criteria:**
- Pass if all four invocations exit 0 and produce the exact expected messages.
- Fail if any command exits non-zero, the success message is missing, or the closed
  project still appears in the second `project list`.
**Last Changed:** 2026-07-07

---

## SYTS_CLI_00002: Element Add, Query, and View CLI Flows

**ID:** SYTS_CLI_00002
**Traces-To:** SWR_CLI_00007, SWR_CLI_00008, SWR_CLI_00009
**Title:** element add, element query, and element view commands end-to-end
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end CLI element flows: adding a new element (class) to the
active project, querying the list of elements (confirming the new element appears), and
viewing an element by path. It exercises `AddElementCommand`, `QueryElementCommand`, and
`ViewElementCommand` through CliRunner.
**Pre-conditions:**
- A fake Rhapsody COM layer with an open fake project whose root exposes
  `createClass(name)`, `createActor(name)`, `createPackage(name)`, and a nested-elements
  collection containing the created class.
- The CLI session pre-configured with an active project (or the test invokes `project
  open` first).
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody element add --type class --name Vehicle` and capture output and exit
   code.
2. Invoke `rhapsody element query` and capture output.
3. Invoke `rhapsody element add --type package --name Domain` and capture output.
4. Invoke `rhapsody element add --type actor --name Driver` and capture output.
5. Invoke `rhapsody element view --path Vehicle` and capture output.
6. Invoke `rhapsody element add --type unknown --name X` and capture output and exit code.
**Expected Result:**
- Steps 1, 3, 4 exit 0 with stdout "Created class: Vehicle", "Created package: Domain",
  "Created actor: Driver" respectively.
- Step 2 exits 0 and the output includes "Vehicle" with type "Class".
- Step 5 exits 0 and emits a JSON object or two-row table containing the path "Vehicle".
- Step 6 exits non-zero with an error message about the unknown type on stderr.
**Verification Criteria:**
- Pass if all success messages match exactly, the query output includes the created
  class, and the unknown-type case aborts with non-zero exit.
- Fail if any success command exits non-zero, the created element is missing from query
  output, or the unknown-type case exits 0.
**Last Changed:** 2026-07-07

---

## SYTS_CLI_00003: IO Import and Export CLI Flows

**ID:** SYTS_CLI_00003
**Traces-To:** SWR_CLI_00010, SWR_CLI_00011
**Title:** io import and io export commands end-to-end
**Type:** System
**Priority:** Low
**Description:**
This test verifies the end-to-end CLI IO flows: importing a model from a source file into
a target package, and exporting a model to an output file in a chosen format. It exercises
`ImportCommand` and `ExportCommand` through CliRunner and confirms the progress messages
and completion markers.
**Pre-conditions:**
- A fake Rhapsody COM layer with an active project.
- A temp source file on disk (for `io import`'s existence validation) and a temp output
  path for export.
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody io import <source_path> --target Root` and capture output and exit
   code.
2. Invoke `rhapsody io export <output_path> --format xmi` and capture output and exit
   code.
3. Invoke `rhapsody io export <output_path> --format json` and capture output.
**Expected Result:**
- Step 1 exits 0 and stdout contains "Importing from <source_path> into Root...", a note
  about format dependency, and "✓ Import completed".
- Step 2 exits 0 and stdout contains "Exporting to <output_path> as xmi...", a format
  dependency note, and "✓ Export completed: <output_path>".
- Step 3 exits 0 with the same pattern but "as json" in the first progress message.
**Verification Criteria:**
- Pass if all three invocations exit 0 and emit the exact progress and completion
  messages with the correct substituted paths/formats.
- Fail if any invocation exits non-zero or any expected message is missing or
  mis-substituted.
**Last Changed:** 2026-07-07

---

## SYTS_CLI_00004: Output Format Selection (json, csv, table)

**ID:** SYTS_CLI_00004
**Traces-To:** SWR_CLI_00002, SWR_CLI_00012, SWR_CLI_00013, SWR_CLI_00014, SWR_CLI_00015
**Title:** --output option routes data to the correct OutputFormatter
**Type:** System
**Priority:** Medium
**Description:**
This test verifies that the `--output` option on the `cli` group correctly selects the
output format and that `OutputFormatter.format` routes to the right formatter. The same
underlying command (e.g. `element query`) is invoked with `--output json`, `--output
csv`, and `--output table`, and the resulting stdout is parsed to confirm format.
**Pre-conditions:**
- A fake Rhapsody COM layer with an active project whose root exposes a nested-elements
  collection with at least two elements (e.g. a Class "A" and a Class "B").
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody --output json element query` and capture stdout.
2. Invoke `rhapsody --output csv element query` and capture stdout.
3. Invoke `rhapsody --output table element query` and capture stdout.
4. Invoke `rhapsody element query` (no --output) and capture stdout.
5. Invoke `rhapsody --output json element view --path A` and confirm a JSON object is
  emitted.
**Expected Result:**
- Step 1: stdout is valid JSON parseable by `json.loads`, containing an `elements` array
  where each element has `name` and `type` keys.
- Step 2: stdout is valid CSV with a header row followed by one row per element.
- Step 3: stdout is an ASCII grid table (tabulate `tablefmt="grid"`) with columns "Name"
  and "Type".
- Step 4: defaults to table format (same as step 3).
- Step 5: stdout is a JSON object representing the element.
**Verification Criteria:**
- Pass if `json.loads` succeeds on JSON output, `csv.reader` parses CSV output, the table
  output contains grid borders, and the default matches table format.
- Fail if any output is not in the selected format, or if the default is not table.
**Last Changed:** 2026-07-07

---

## SYTS_CLI_00005: Error Handling and Exit Codes (click.Abort)

**ID:** SYTS_CLI_00005
**Traces-To:** SWR_CLI_00004, SWR_CLI_00007, SWR_CLI_00016
**Title:** CLI errors echo to stderr and abort with non-zero exit code
**Type:** System
**Priority:** High
**Description:**
This test verifies the CLI's end-to-end error handling: when a command encounters a
`RhapsodyConnectionError` or other exception, it echoes the error to stderr and raises
`click.Abort`, causing CliRunner to report a non-zero exit code. It also confirms the
class-based command architecture surfaces errors consistently across subgroups.
**Pre-conditions:**
- A fake Rhapsody COM layer where `attach()` and `launch()` both fail (raising
  `RhapsodyConnectionError`).
- A scenario where `project open` is invoked without a valid project path (or the open
  fails internally).
- A scenario where `element add` is invoked with no active project.
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody project open <nonexistent_or_failing_path>` with the failing COM layer
   and capture stdout, stderr, and exit code.
2. Invoke `rhapsody element add --type class --name X` with no active project and capture
   stdout, stderr, and exit code.
3. Invoke `rhapsody io export <out>` with no active project and capture stderr and exit
   code.
4. Invoke `rhapsody element query` with no active project and capture stderr and exit
   code.
**Expected Result:**
- All four invocations exit with a non-zero exit code (1 for `click.Abort`).
- Each invocation writes a descriptive error message to stderr.
- Stdout does not contain any success message (e.g. "Opened project:", "Created class:").
**Verification Criteria:**
- Pass if every invocation exits non-zero, stderr is non-empty with a relevant error,
  and stdout has no success message.
- Fail if any invocation exits 0, or if the error is not written to stderr.
**Last Changed:** 2026-07-07

---

## SYTS_CLI_00006: Class-Based Command Architecture - Subgroups Registered

**ID:** SYTS_CLI_00006
**Traces-To:** SWR_CLI_00001, SWR_CLI_00016
**Title:** cli group registers project, element, and io subgroups and their commands
**Type:** System
**Priority:** Medium
**Description:**
This test verifies the class-based command architecture end-to-end: the `cli` group
registers the `project`, `element`, and `io` command subgroups, and each subgroup
registers its commands (`open/list/close`, `add/view/query`, `import/export`). This is
verified by invoking `--help` on each level and confirming the command listing.
**Pre-conditions:**
- The `cli` entry point importable.
- CliRunner available.
**Test Steps:**
1. Invoke `rhapsody --help` and capture stdout.
2. Invoke `rhapsody project --help` and capture stdout.
3. Invoke `rhapsody element --help` and capture stdout.
4. Invoke `rhapsody io --help` and capture stdout.
5. Confirm the `--output` option appears in the top-level help with choices
   `table|json|csv`.
**Expected Result:**
- Step 1: help lists `project`, `element`, and `io` subgroups and the `--output` option.
- Step 2: help lists `open`, `list`, and `close` commands.
- Step 3: help lists `add`, `view`, and `query` commands.
- Step 4: help lists `import` and `export` commands.
- Step 5: the `--output` option help text shows choices `table`, `json`, `csv`.
**Verification Criteria:**
- Pass if every expected subgroup and command name appears in the corresponding help
  output, and the `--output` choices are present.
- Fail if any subgroup or command is missing, or if the `--output` option is absent.
**Last Changed:** 2026-07-07
