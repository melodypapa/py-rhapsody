# Design: Temporarily Disable `project` Sub-Command, Attach-Based Element Commands, and CLI Logging

## Context

Users currently open Rhapsody projects manually through the Rhapsody GUI rather than
via `rhapsody-cli project open`. The `project` sub-command group is being temporarily
disabled, and the `element` commands need to work against whatever project is already
active in the running Rhapsody instance instead of requiring `project open` first.
This also introduces basic logging for the CLI.

## Goals

1. Disable the `project` sub-command group without deleting its implementation or tests.
2. `element add` / `element view` / `element query` attach to the running Rhapsody
   instance and operate on its currently active project automatically.
3. Add a lightweight logging setup for the CLI (console + file), controllable via a
   `--verbose` flag.

## Non-Goals

- Removing or rewriting `cli/commands/project.py` or its tests.
- Persisting CLI state across separate process invocations (not possible; each CLI
  invocation is a new process — state can only come from the live Rhapsody instance).
- Log rotation, structured logging, or configurable log file paths.

## Design

### 1. Disable `project` sub-command

- In `src/rhapsody_cli/cli/main.py`, remove the line
  `cli.add_command(project_cmd)` (and its now-unused import) so the `project` group is
  no longer registered on the root `cli` group.
- `src/rhapsody_cli/cli/commands/project.py` and its tests remain unchanged, so
  re-enabling later is a one-line change (re-add the import + `add_command` call).
- Existing tests that assert `project` is invocable via the root CLI must be updated to
  reflect that it's no longer registered (e.g., `cli list-commands` no longer includes
  `project`, invoking `rhapsody-cli project ...` yields a click "no such command" error).

### 2. Element commands attach to the live Rhapsody instance

- `RhapsodyContext` gains a new method:

  ```python
  def get_active_project(self) -> RPProject:
      """Attach to the running Rhapsody instance and return its active project."""
      self.connect("attach")
      assert self.app is not None
      self.project = self.app.activeProject()
      return self.project
  ```

- `cli/commands/element.py`'s `AddElementCommand`, `ViewElementCommand`, and
  `QueryElementCommand` replace their `if ctx.project is None: ...` checks with a call
  to `ctx.get_active_project()` wrapped in a `try/except RhapsodyConnectionError` block.
- On `RhapsodyConnectionError`, the command logs the exception at `ERROR` level and
  prints to the user:
  `"No running Rhapsody instance found. Please open Rhapsody and a project first."`,
  then raises `click.Abort()`.
- All other exception handling in these commands stays as-is (generic `Exception`
  catch-all prints `Error: {e}` and aborts).

### 3. CLI logging

- New module `src/rhapsody_cli/cli/logging_config.py`:

  ```python
  def configure_logging(verbose: bool) -> None:
      """Configure console + file logging for the rhapsody_cli package logger."""
  ```

  - Configures the `rhapsody_cli` logger (parent of all module loggers via
    `logging.getLogger(__name__)` in each module).
  - Level: `logging.INFO` by default, `logging.DEBUG` when `verbose=True`.
  - Two handlers:
    - `logging.StreamHandler()` → stderr.
    - `logging.FileHandler("rhapsody-cli.log", mode="a")` → append to a file in the
      current working directory.
  - Both handlers use the same formatter:
    `"%(asctime)s [%(levelname)s] %(name)s: %(message)s"`.
  - Guards against duplicate handlers being added if `configure_logging` is called more
    than once (e.g., in tests) by clearing existing handlers on the target logger first.

- `src/rhapsody_cli/cli/main.py`: add a `--verbose` / `-v` boolean flag (default
  `False`) to the root `cli` group. In the group callback, call
  `configure_logging(verbose)` before dispatching to subcommands.

- Command modules (`element.py`, and any others touched) obtain a module-level
  `logger = logging.getLogger(__name__)` and log:
  - `INFO`: start/success of key actions (e.g., "Attached to Rhapsody", "Created class
    'Foo'").
  - `ERROR`: caught exceptions before re-raising/aborting.

## Data Flow (element command)

```
CLI invocation (e.g. `rhapsody-cli element add --type class --name Foo`)
    ↓
cli() group callback → configure_logging(verbose)
    ↓
AddElementCommand.execute()
    ↓
ctx.get_active_project()
    ├─ ctx.connect("attach")  → RhapsodyApplication.attach() → COM GetActiveObject
    │      └─ on failure → RhapsodyConnectionError → log ERROR → print user message → click.Abort()
    └─ ctx.app.activeProject() → RPProject wrapping COM activeProject()
    ↓
root = project.getRoot(); root.createClass(name) / createActor(name) / createPackage(name)
    ↓
log INFO "Created {type}: {name}"; click.echo(...)
```

## Error Handling

| Condition | Behavior |
|---|---|
| No running Rhapsody instance (attach fails) | Log `ERROR` with exception detail; print `"No running Rhapsody instance found. Please open Rhapsody and a project first."`; `click.Abort()` |
| Attach succeeds but no active project (COM raises on `activeProject()`) | Caught by existing generic `except Exception` handler → `Error: {e}` printed; `click.Abort()` |
| Unknown element type in `element add` | Unchanged: existing explicit check/message |
| Any other runtime error | Unchanged: existing generic `except Exception` handler |

## Testing

- `tests/cli/test_command_classes.py` (or equivalent): assert `project` group is not a
  subcommand of the root `cli` group; `project.py`'s own unit tests remain and still
  pass in isolation (they construct `ProjectCommandGroup` directly, not via `cli`).
- `tests/cli/test_element_commands.py`: update fakes/tests for `add`/`view`/`query` to
  cover:
  - Successful path: `RhapsodyContext.get_active_project()` returns a fake project via
    fake `RhapsodyApplication.attach()` + `activeProject()`.
  - Failure path: `RhapsodyConnectionError` raised by `connect("attach")` results in the
    expected error message and `click.Abort()`.
- New `tests/cli/test_logging_config.py`: verify `configure_logging` sets the expected
  level for `verbose=True/False`, attaches exactly one `StreamHandler` and one
  `FileHandler` (no duplicates on repeated calls), and that a log record written after
  configuration appears in the log file.
- Run full quality gate: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest`.

## Files Touched

- `src/rhapsody_cli/cli/main.py`
- `src/rhapsody_cli/cli/context.py`
- `src/rhapsody_cli/cli/commands/element.py`
- `src/rhapsody_cli/cli/logging_config.py` (new)
- `tests/cli/test_command_classes.py` (or wherever root CLI registration is tested)
- `tests/cli/test_element_commands.py`
- `tests/cli/test_logging_config.py` (new)

`src/rhapsody_cli/cli/commands/project.py` and its existing tests are **not** modified.
