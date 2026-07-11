# Acceptance Test Specifications - Command-Line Interface

**Category:** CLI
**Prefix:** ATS
**Test Type:** Acceptance
**Last Validated:** 2026-07-07

---

## ATS_CLI_00001: Open a Project from the CLI

**ID:** ATS_CLI_00001
**Traces-To:** SWR_CLI_00001, SWR_CLI_00003, SWR_CLI_00004
**Title:** Run `rhapsody-cli project open <path>` to open a project
**Type:** Acceptance
**Priority:** High
**Description:**
As a CLI user, I want to open a Rhapsody project from the command line by giving a path,
so that I can bootstrap an automated session against a known project file.
**Acceptance Criteria:**
- Given a valid `.rpyx` project file exists on disk and Rhapsody is available, When I run
  `rhapsody-cli project open <path>`, Then the command connects via `"attach"` (or
  launches if needed), opens the project, and prints `Opened project: <path>` to stdout
  with exit code 0.
- Given the path does not exist on disk, When I run `rhapsody-cli project open <path>`,
  Then the command reports the missing file and exits with a non-zero exit code (path
  validation rejects the argument before any COM call).
- Given Rhapsody cannot be reached (e.g., not installed), When I run
  `rhapsody-cli project open <path>`, Then a `RhapsodyConnectionError` (or other
  exception) is reported to stderr and the command aborts with a non-zero exit code.
- Given the CLI is invoked, When I inspect the registered subcommands, Then `project`,
  `element`, and `io` subgroups are all present on the `cli` group.
**Verification Criteria:**
Run `rhapsody-cli project open <fixture.rpyx>` and assert stdout contains
`Opened project:` and the exit code is 0. Run with a non-existent path and assert a
non-zero exit code and a clear error message (no Python traceback leaked to the user).
With Rhapsody unavailable (or simulating the failure), assert the error is reported to
stderr and the exit code is non-zero. Run `rhapsody-cli --help` and assert `project`,
`element`, and `io` are listed as subcommands.
**Last Changed:** 2026-07-07

---

## ATS_CLI_00002: List and Close Projects

**ID:** ATS_CLI_00002
**Traces-To:** SWR_CLI_00005, SWR_CLI_00006
**Title:** Run `project list` and `project close` to inspect and close open projects
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a CLI user, I want to list the currently open projects and close the active project,
so that I can inspect session state and tear down cleanly.
**Acceptance Criteria:**
- Given one or more projects are open in Rhapsody, When I run `rhapsody-cli project list`,
  Then a table is printed with each project's name and path, and the exit code is 0.
- Given no projects are open, When I run `rhapsody-cli project list`, Then the command
  prints `No open projects` and exits 0.
- Given an active project exists, When I run `rhapsody-cli project close`, Then the
  project is closed via `ctx.close_project()` and the command prints `Project closed`
  with exit code 0.
- Given no active project exists, When I run `rhapsody-cli project close`, Then the
  command prints `No active project` and exits 0 (no error).
- Given any command in this group raises an exception, When the exception propagates, Then
  it is reported to stderr and the command aborts with a non-zero exit code.
**Verification Criteria:**
Open a fixture project via `project open`, then run `project list` and assert the table
output contains the project's name and path. Run `project close` and assert stdout
contains `Project closed`; run `project list` again and assert stdout is
`No open projects`. Run `project close` again and assert stdout is `No active project`
with exit code 0. Force an error (e.g., disconnect Rhapsody mid-session) and assert the
next `project list` exits non-zero with a stderr message.
**Last Changed:** 2026-07-07

---

## ATS_CLI_00003: Add Elements via the CLI

**ID:** ATS_CLI_00003
**Traces-To:** SWR_CLI_00007
**Title:** Run `element add --type <T> --name <N>` to create a class or actor
**Type:** Acceptance
**Priority:** High
**Description:**
As a CLI user, I want to create a new model element from the command line by specifying a
type and name, so that I can script model construction without writing Python.
**Acceptance Criteria:**
- Given an active project is open, When I run
  `rhapsody-cli element add --type class --name Vehicle`, Then `root.addClass("Vehicle")`
  is invoked and the command prints `Created class: Vehicle` with exit code 0.
- Given an active project is open, When I run
  `rhapsody-cli element add --type actor --name Driver`, Then `root.addActor("Driver")`
  is invoked and the command prints `Created actor: Driver` with exit code 0.
- Given no active project is open, When I run `element add ...`, Then the
  command prints an error about the missing active project and aborts with a non-zero exit
  code.
- Given an unknown `--type` (e.g., `--type widget`), When I run the command, Then it
  prints an error about the unknown type and aborts with a non-zero exit code.
**Verification Criteria:**
With a fixture project open, run each of the two valid `element add` invocations and
assert the printed `Created <type>: <name>` line and exit code 0; then verify each element
exists in the model (e.g., via `element query` or by re-opening the project in the GUI).
Run `element add` with no active project and assert a non-zero exit code and an error
message mentioning the missing project. Run `element add --type widget --name X` and
assert a non-zero exit code and an error message about the unknown type.
**Last Changed:** 2026-07-07

---

## ATS_CLI_00004: View and Query Elements

**ID:** ATS_CLI_00004
**Traces-To:** SWR_CLI_00008, SWR_CLI_00009
**Title:** Run `element view --path <P>` and `element query [--filter ...]` to inspect elements
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a CLI user, I want to view details of a single element by path and list elements in the
active project with an optional filter, so that I can explore the model from the shell.
**Acceptance Criteria:**
- Given an active project, When I run `rhapsody-cli element view --path /Package/Class`,
  Then the command prints element details; with `--output json` it prints a JSON object
  containing `path`, `type`, and `properties`; with `--output table` (default) it prints
  a two-row table.
- Given no active project, When I run `element view --path ...`, Then the command aborts
  with a non-zero exit code and an error message.
- Given an active project with nested elements, When I run `rhapsody-cli element query`,
  Then a table with columns `Name` and `Type` is printed (default), or a JSON object with
  an `elements` array (each item having `name` and `type`) is printed with `--output json`.
- Given `element query` is invoked with `--filter`, When the filter is applied, Then only
  matching elements are returned (the filter is honored by the query).
- Given any exception during view/query, When it propagates, Then it is reported to stderr
  and the command aborts with a non-zero exit code.
**Verification Criteria:**
Open a fixture project containing at least one package and class. Run
`element view --path /<Package>/<Class> --output json` and assert the output parses as
JSON and contains the expected `path` and `type` keys. Run the same with `--output table`
and assert a two-row table is printed. Run `element query --output json` and assert the
JSON has an `elements` array whose items each have `name` and `type`. Run
`element query --output table` and assert the table headers are `Name` and `Type`. With no
active project, assert `element view` and `element query` both exit non-zero with an error
message.
**Last Changed:** 2026-07-07

---

## ATS_CLI_00006: Select Output Format and Receive Consistent Errors

**ID:** ATS_CLI_00006
**Traces-To:** SWR_CLI_00002, SWR_CLI_00012, SWR_CLI_00013, SWR_CLI_00014, SWR_CLI_00015, SWR_CLI_00016
**Title:** Choose table/json/csv output, see `(no data)` for empty results, and non-zero exit codes on errors
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a CLI user, I want to select the output format globally, see a sensible placeholder
when there is no data, and rely on non-zero exit codes to detect failures in scripts.
**Acceptance Criteria:**
- Given the `cli` group is invoked, When I pass `--output json` (or `csv`, or `table`),
  Then `ctx.obj.output_format` is set to the chosen value and downstream commands route
  their output through `OutputFormatter.format` accordingly.
- Given `--output` is omitted, When I run any command, Then the default format is `table`.
- Given `--output` is given an invalid value (e.g., `xml`), When I run the command, Then
  Click rejects the choice and exits non-zero before any Rhapsody interaction.
- Given a command produces an empty rows list and `--output table` is selected, When the
  output is formatted, Then `(no data)` is printed (the `table` formatter's empty-rows
  contract).
- Given `--output json`, When `OutputFormatter.json_format` is called with non-serializable
  data, Then the value falls back to its `str()` representation and valid JSON is still
  produced.
- Given `--output csv`, When `OutputFormatter.csv_format` is called, Then a header row
  followed by data rows is produced as CSV text.
- Given any command raises an exception, When it propagates to the CLI, Then the message
  is echoed to stderr and the process exits with a non-zero exit code (Click `Abort`).
- Given the CLI architecture, When I inspect the command classes, Then each command is a
  class extending `click.Command` (or a `BaseProjectCommand`/`BaseElementCommand`
  base) grouped under a `click.Group` subclass.
**Verification Criteria:**
Run `rhapsody-cli --output xml project list` and assert Click rejects `xml` with a non-zero
exit code. Run `rhapsody-cli --output json project list` (with no open projects) and
assert valid JSON is printed. Run `rhapsody-cli --output csv project list` (with at least
one open project) and assert the output starts with a CSV header row. Force an empty
result and `--output table` and assert stdout is exactly `(no data)`. Pass a non-serializable
object (e.g., a `datetime`) through `json_format` indirectly and assert the JSON still
parses with the value stringified. Trigger any command failure (e.g., no Rhapsody
installed) and assert the exit code is non-zero and the error appears on stderr, not
stdout. Confirm via `--help` that the class-based commands are registered under
`project`, `element`, and `io` groups.
**Last Changed:** 2026-07-07
