# Software Requirements - CLI (Command-Line Interface)

**Category:** CLI
**Prefix:** SWR
**Source:** Extracted from code
**Last Validated:** 2026-07-07

---

## SWR_CLI_00001: CLI Entry Point

**ID:** SWR_CLI_00001
**Title: cli group is the main Click entry point for the rhapsody-cli tool
**Status:** Implemented
**Priority:** High
**Description:**
The `cli` Click group shall be the main entry point for the command-line tool. It shall
provide a `--output` option with choices `table`, `json`, `csv` (default `table`) that
sets the output format on the `RhapsodyContext`. If no context object exists, a new
`RhapsodyContext` shall be created. The group shall register the `project`, `element`,
and `io` command subgroups.
**Implementation:** src/rhapsody_cli/cli/main.py:cli
**Last Changed:** 2026-07-07

---

## SWR_CLI_00002: Output Format Option

**ID:** SWR_CLI_00002
**Title: --output option selects table, json, or csv output format
**Status:** Implemented
**Priority:** Medium
**Description:**
The `--output` option on the `cli` group shall accept one of `table`, `json`, or `csv`
(default `table`) and store the selected format string on `ctx.obj.output_format`.
**Implementation:** src/rhapsody_cli/cli/main.py:cli
**Last Changed:** 2026-07-07

---

## SWR_CLI_00003: RhapsodyContext Session Management

**ID:** SWR_CLI_00003
**Title: RhapsodyContext manages CLI session state (app, project, output format)
**Status:** Implemented
**Priority:** High
**Description:**
`RhapsodyContext` shall manage CLI session state with attributes `app`
(`RhapsodyApplication | None`), `project` (`RPProject | None`), and `output_format`
(str, default `"table"`). It shall expose methods: `connect(method="attach")` (lazily
attaches or launches), `open_project(project_path)` (connects if needed, opens project),
`close_project()` (closes and clears project), and `disconnect()` (closes project and
quits app).
**Implementation:** src/rhapsody_cli/cli/context.py:RhapsodyContext
**Last Changed:** 2026-07-07

---

## SWR_CLI_00004: Project Open Command

**ID:** SWR_CLI_00004
**Title: project open command opens a Rhapsody project file
**Status:** Implemented
**Priority:** High
**Description:**
The `project open` command shall accept a `project_path` argument (validated to exist on
disk) and execute `OpenProjectCommand.execute`. It shall create a `RhapsodyContext`,
connect via `"attach"`, open the project, and echo `"Opened project: {path}"`. On
`RhapsodyConnectionError` or other exceptions, it shall echo the error to stderr and
raise `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/project.py:OpenProjectCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00005: Project List Command

**ID:** SWR_CLI_00005
**Title: project list command lists open projects
**Status:** Implemented
**Priority:** Medium
**Description:**
The `project list` command shall execute `ListProjectsCommand.execute`. It shall create a
`RhapsodyContext`, connect via `"attach"`, and retrieve all open projects. If no projects
are open it shall echo `"No open projects"`. Otherwise it shall format the project name
and path as a table via `OutputFormatter.table` and echo the result. Exceptions are
reported to stderr with `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/project.py:ListProjectsCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00006: Project Close Command

**ID:** SWR_CLI_00006
**Title: project close command closes the active project
**Status:** Implemented
**Priority:** Medium
**Description:**
The `project close` command shall execute `CloseProjectCommand.execute`. It shall create a
`RhapsodyContext`; if no active project exists it shall echo `"No active project"`.
Otherwise it shall close the project via `ctx.close_project()` and echo
`"Project closed"`. Exceptions are reported to stderr with `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/project.py:CloseProjectCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00007: Element Add Command

**ID:** SWR_CLI_00007
**Title: element add command creates a new element in the active project
**Status:** Implemented
**Priority:** High
**Description:**
The `element add` command shall accept required `--type` and `--name` options and execute
`AddElementCommand.execute`. It shall require an active project (else echo an error and
abort). It shall fetch the project root and dispatch on `element_type.lower()`:
`"class"` -> `root.createClass(name)`, `"actor"` -> `root.createActor(name)`,
`"package"` -> `root.createPackage(name)`. Unknown types shall echo an error and abort.
On success it shall echo `"Created {type}: {name}"`.
**Implementation:** src/rhapsody_cli/cli/commands/element.py:AddElementCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00008: Element View Command

**ID:** SWR_CLI_00008
**Title: element view command displays element details for a path
**Status:** Implemented
**Priority:** Low
**Description:**
The `element view` command shall accept a required `--path` option and execute
`ViewElementCommand.execute`. It shall require an active project. It shall build a demo
data dict (`path`, `type="unknown"`, properties) and format it as JSON (if
`output_format == "json"`) or as a two-row table otherwise. Exceptions are reported to
stderr with `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/element.py:ViewElementCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00009: Element Query Command

**ID:** SWR_CLI_00009
**Title: element query command lists elements in the active project
**Status:** Implemented
**Priority:** Medium
**Description:**
The `element query` command shall accept an optional `--filter` option and execute
`QueryElementCommand.execute`. It shall require an active project, fetch the project root,
and retrieve nested elements. When `output_format == "json"` it shall emit a JSON object
with an `elements` array (each element having `name` and `type`). Otherwise it shall emit
a table with columns `Name` and `Type`. Exceptions are reported to stderr with
`click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/element.py:QueryElementCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00010: IO Import Command

**ID:** SWR_CLI_00010
**Title: io import command imports a model from a file
**Status:** Implemented
**Priority:** Low
**Description:**
The `io import` command shall accept a `source` argument (validated to exist) and a
`--target` option (default `"Root"`) and execute `ImportCommand.execute`. It shall
require an active project. It shall echo progress messages
(`"Importing from {source} into {target}..."`, a note about format dependency, and
`"✓ Import completed"`). Exceptions are reported to stderr with `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/io.py:ImportCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00011: IO Export Command

**ID:** SWR_CLI_00011
**Title: io export command exports a model to a file
**Status:** Implemented
**Priority:** Low
**Description:**
The `io export` command shall accept an `output` argument (path) and a `--format` option
(default `"xmi"`, help mentions `xmi, json`) and execute `ExportCommand.execute`. It
shall require an active project. It shall echo progress messages
(`"Exporting to {output} as {format}..."`, a note about format dependency, and
`"✓ Export completed: {output}"`). Exceptions are reported to stderr with `click.Abort`.
**Implementation:** src/rhapsody_cli/cli/commands/io.py:ExportCommand
**Last Changed:** 2026-07-07

---

## SWR_CLI_00012: OutputFormatter Table Format

**ID:** SWR_CLI_00012
**Title: OutputFormatter.table formats rows as an ASCII grid table
**Status:** Implemented
**Priority:** Medium
**Description:**
`OutputFormatter.table(headers, rows)` shall return `"(no data)"` when `rows` is empty.
Otherwise it shall return the result of `tabulate(rows, headers=headers, tablefmt="grid")`
as a string.
**Implementation:** src/rhapsody_cli/cli/formatters.py:OutputFormatter.table
**Last Changed:** 2026-07-07

---

## SWR_CLI_00013: OutputFormatter JSON Format

**ID:** SWR_CLI_00013
**Title: OutputFormatter.json_format serializes data as indented JSON
**Status:** Implemented
**Priority:** Medium
**Description:**
`OutputFormatter.json_format(data)` shall return `json.dumps(data, indent=2, default=str)`
so that non-serializable values fall back to their `str()` representation.
**Implementation:** src/rhapsody_cli/cli/formatters.py:OutputFormatter.json_format
**Last Changed:** 2026-07-07

---

## SWR_CLI_00014: OutputFormatter CSV Format

**ID:** SWR_CLI_00014
**Title: OutputFormatter.csv_format writes headers and rows as CSV
**Status:** Implemented
**Priority:** Medium
**Description:**
`OutputFormatter.csv_format(headers, rows)` shall write the header row followed by all
data rows to an in-memory `StringIO` using `csv.writer` and return the resulting string.
**Implementation:** src/rhapsody_cli/cli/formatters.py:OutputFormatter.csv_format
**Last Changed:** 2026-07-07

---

## SWR_CLI_00015: OutputFormatter Format Router

**ID:** SWR_CLI_00015
**Title: OutputFormatter.format routes data to the chosen formatter
**Status:** Implemented
**Priority:** Medium
**Description:**
`OutputFormatter.format(data, format_type, headers=None)` shall route to `json_format`
when `format_type == "json"`, to `csv_format` (coercing `data` to a list) when
`format_type == "csv"`, and to `table` (same coercion) otherwise.
**Implementation:** src/rhapsody_cli/cli/formatters.py:OutputFormatter.format
**Last Changed:** 2026-07-07

---

## SWR_CLI_00016: Class-Based Command Architecture

**ID:** SWR_CLI_00016
**Title: CLI commands use a class-based Click command architecture
**Status:** Implemented
**Priority:** Medium
**Description:**
Each CLI command shall be implemented as a class extending `click.Command` (or a
project/element/io-specific base like `BaseProjectCommand`, `BaseElementCommand`,
`BaseIOCommand`). The command's `__init__` shall configure name, help, callback
(`self.execute`), and params. Commands shall be grouped under a `click.Group` subclass
(`ProjectCommandGroup`, `ElementCommandGroup`, `IOCommandGroup`) that registers the
commands in its own `__init__`.
**Implementation:** src/rhapsody_cli/cli/commands/project.py:BaseProjectCommand
**Last Changed:** 2026-07-07
