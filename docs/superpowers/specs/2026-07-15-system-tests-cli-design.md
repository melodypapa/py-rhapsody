# System Tests for CLI (Subprocess End-to-End) Design

## Overview

Design system tests that invoke the `rhapsody-cli` directly as a subprocess (like a real command line), testing the full stack from argument parsing through COM interaction to output formatting. Tests run against a live Rhapsody instance with a real project, following the same pattern as the model class integration tests.

## Scope

- **All 6 command groups**: `project`, `package`, `class`, `attribute`, `operation`, `port`
- **CRUD lifecycle per group**: `create`, `view`, `list`, `update`, `delete` (plus `link` for class, `open`/`close`/`new` for project)
- **CLI parsing tests**: help, invalid commands, missing arguments, verbose flag (no Rhapsody needed)
- **Error handling**: non-existent paths, invalid JSON input, duplicate names

## Approach: Pure Subprocess

All operations (setup, act, verify, teardown) go through `subprocess.run()` invoking `python -m rhapsody_cli.cli.main`. No Python API imports for test operations.

- **Setup**: `rhapsody-cli project new <dir> <name>` via subprocess
- **Act**: `rhapsody-cli class create --path ... --input ...` via subprocess
- **Verify**: `rhapsody-cli class list --path ... --format json` via subprocess, parse JSON
- **Teardown**: `rhapsody-cli project close` via subprocess

## File Structure

```
tests/system/
├── conftest.py                          # Session-scoped: skip if no Rhapsody, test project dir
├── cli/
│   ├── conftest.py                      # CLI helpers: _run_cli, _run_cli_json, cli_project fixture
│   ├── test_cli_parsing.py              # CLI parsing: help, verbose, invalid commands, missing args
│   ├── test_project_cli.py              # project: new, open, list, close
│   ├── test_package_cli.py              # package: create, delete, view, list, update
│   ├── test_class_cli.py                # class: create, delete, view, list, link, update
│   ├── test_attribute_cli.py            # attribute: create, delete, view, list, update
│   ├── test_operation_cli.py            # operation: create, delete, view, list, update
│   └── test_port_cli.py                 # port: create, delete, view, list, update
```

The existing `tests/system/cli/test_element_cli_subprocess.py` is deleted. Its CLI parsing tests move to `test_cli_parsing.py` with corrected command names (the old file referenced a non-existent `element` command).

## Fixture Strategy

### tests/system/conftest.py

- `rhapsody_app` (session-scoped) — Connects to running Rhapsody via `RhapsodyApplication.connect(attach_only=True)`. Skips entire session if unavailable (same pattern as integration tests).
- `test_project_dir` (session-scoped) — Creates `demos/test_project_system/` temp directory.

### tests/system/cli/conftest.py

- `_run_cli(*args)` helper — Runs `python -m rhapsody_cli.cli.main <args>` via `subprocess.run()` with `capture_output=True`, `text=True`, `timeout=30`. Returns `subprocess.CompletedProcess`.
- `_run_cli_json(*args)` helper — Same as `_run_cli` but appends `--format json` and parses JSON from stdout. Returns parsed Python object.
- `cli_project` (session-scoped) — Creates a test project via `rhapsody-cli project new <dir> <name>`. Cleans up via `rhapsody-cli project close` at session end.

### Per-Test Isolation

- Each test creates unique elements using UUID-suffixed names (e.g., `TestCls_a1b2c3d4`)
- Each test cleans up via CLI `delete` in a `finally` block
- Unique names prevent cross-test interference even if cleanup fails

## Test Cases

### test_cli_parsing.py (No Rhapsody Required)

| Test | Description |
|------|-------------|
| `test_cli_help_command` | `--help` returns 0, shows "Usage:" |
| `test_cli_invalid_command` | Unknown command returns non-zero, shows "invalid choice" |
| `test_cli_verbose_flag` | `--verbose` accepted at subcommand level (no "unrecognized arguments") |
| `test_class_create_missing_arguments` | `class create` without `--path` returns usage error |
| `test_package_delete_missing_arguments` | `package delete` without path returns usage error |
| `test_attribute_create_missing_arguments` | `attribute create` without `--path` returns usage error |
| `test_operation_create_missing_arguments` | `operation create` without `--path` returns usage error |
| `test_port_create_missing_arguments` | `port create` without `--path` returns usage error |
| `test_project_open_missing_arguments` | `project open` without `project_path` returns usage error |
| `test_project_new_missing_arguments` | `project new` without arguments returns usage error |

### test_project_cli.py (Requires Rhapsody)

| Test | Description |
|------|-------------|
| `test_project_new_creates_project` | `project new <dir> <name>` returns 0, project appears in `project list` |
| `test_project_list_shows_open_project` | After creating, `project list` output contains project name |
| `test_project_close_removes_from_list` | After `project close`, project disappears from `project list` |
| `test_project_open_existing_project` | `project open <path>` opens previously created project, appears in list |
| `test_project_list_empty_when_no_project` | When no project open, `project list` reports "No open projects" |

### test_package_cli.py (Requires Rhapsody)

| Test | Description |
|------|-------------|
| `test_package_create_at_root` | `package create --path TestProject --input ...` returns 0, package appears in `package list` |
| `test_package_create_nested` | Create package under another package, verify path in `package view` |
| `test_package_view_existing` | `package view --path TestProject::PkgName` returns 0, shows package details |
| `test_package_view_nonexistent` | `package view --path TestProject::NonExistent` returns non-zero, error message |
| `test_package_list_in_project` | `package list --path TestProject` returns 0, lists packages |
| `test_package_delete_existing` | `package delete --path TestProject::PkgName` returns 0, package gone from `package list` |
| `test_package_delete_nonexistent` | `package delete --path TestProject::NonExistent` returns non-zero, error message |
| `test_package_update_name` | `package update --path ... --name NewName` returns 0, verify via `package view` |

### test_class_cli.py (Requires Rhapsody)

| Test | Description |
|------|-------------|
| `test_class_create_under_package` | `class create --path TestProject::Pkg --input ...` returns 0, class appears in `class list` |
| `test_class_view_existing` | `class view --path TestProject::Pkg::ClsName` returns 0, shows class details |
| `test_class_view_nonexistent` | `class view --path TestProject::Pkg::NonExistent` returns non-zero |
| `test_class_list_in_package` | `class list --path TestProject::Pkg` returns 0, lists classes |
| `test_class_delete_existing` | `class delete --path TestProject::Pkg::ClsName` returns 0, gone from `class list` |
| `test_class_delete_nonexistent` | `class delete --path TestProject::Pkg::NonExistent` returns non-zero |
| `test_class_update_name` | `class update --path ... --name NewName` returns 0, verify via `class view` |
| `test_class_link` | `class link --path ... --target ...` returns 0 (if link subcommand exists) |

### test_attribute_cli.py, test_operation_cli.py, test_port_cli.py

Same pattern as `test_class_cli.py`, adapted for each element type:
- `create` — create element under a class/package, verify via `list`
- `view` — view existing and non-existent element by path
- `list` — list elements in parent container
- `delete` — delete existing and non-existent element
- `update` — update element properties

## Output Verification Strategy

### Return Code Checks

- Success: `result.returncode == 0`
- Usage errors: `result.returncode != 0` and `"usage:" in result.stderr.lower()`
- Runtime errors: `result.returncode != 0` and error message in `result.stderr`

### Output Parsing

- Prefer `--format json` for verification assertions (structured, robust)
- Parse JSON from stdout: `data = json.loads(result.stdout)`
- Assert on structured data: `assert any(item["name"] == expected_name for item in data)`
- For commands that don't support JSON (e.g., `project list`), check for element name/path in stdout text

### Timeout

- Default 30-second timeout per subprocess (matches existing pattern)
- Rhapsody operations should complete well within this

## Error Handling Tests (Per Command File)

Each command group test file includes:

- **Non-existent path**: Command with invalid path returns non-zero, proper error message in stderr
- **Invalid JSON input**: `create` with malformed JSON returns non-zero, error message about JSON parsing
- **Duplicate element name**: `create` with name that already exists returns non-zero (or handles gracefully per CLI behavior)

## Test Markers

- `@pytest.mark.system` — All system tests marked with this
- System tests auto-skip in CI (no Rhapsody available)
- System tests run locally with: `pytest tests/system/ -v`

## Dependencies

- Existing CLI implementation (no changes needed to source code)
- Live Rhapsody instance (same requirement as integration tests)
- `demos/` directory for test project artifacts (same pattern as integration tests)
