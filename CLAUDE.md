# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rhapsody-cli is a Pythonic, object-oriented wrapper around the IBM Rhapsody COM API for Windows. Method names and class hierarchy mirror the Rhapsody Java API (`com.telelogic.rhapsody.core`) exactly, so existing Rhapsody Java API knowledge transfers directly. The project also provides an argparse-based CLI for managing projects, elements, and import/export operations.

- **Platform:** Windows (COM automation is Windows-only); tests run anywhere via fakes
- **Python:** 3.8+
- **Runtime deps:** `pywin32` (core), `tabulate` + `rich` (CLI extras)
- **Entry point:** `rhapsody-cli = "rhapsody_cli.cli.main:main"`

## Common Commands

### Installation

```bash
pip install -e ".[dev,cli]"   # Full dev setup: required to run the full test suite (CLI tests need tabulate/rich)
pip install -e ".[dev]"       # Dev tools only (ruff/black/mypy/pytest); CLI tests will fail to import
pip install -e ".[cli]"       # CLI runtime deps only
pip install -e .              # Core package only (pywin32 on Windows)
```

### Testing

```bash
pytest                                  # All tests
pytest tests/unit/                      # Unit tests only (mocked COM, no Rhapsody needed)
pytest tests/integration/               # Integration tests (requires live Rhapsody instance)
pytest tests/system/                    # End-to-end subprocess tests
pytest tests/unit/models/test_core.py   # Single test module
pytest -k "test_open"                   # Pattern matching
pytest --co                             # List all tests without running
```

**Test structure:**
- `tests/unit/` — Mocked COM objects, no Rhapsody installation required (what CI runs)
- `tests/integration/` — Requires live, licensed Rhapsody instance (auto-skips if unavailable)
- `tests/system/` — End-to-end subprocess tests

Tests run entirely against mocked COM objects (fakes live under `tests/unit/models/fakes.py`). No Rhapsody installation or license is required to run the unit test suite.

### Linting, Formatting, Type Checking

```bash
ruff check src/ tests/       # Lint (E, F, I, UP, B rule sets)
ruff check src/ tests/ --fix # Auto-fix
black --check src/ tests/    # Format check (line-length 200, py38 target)
black src/ tests/            # Auto-format
mypy src/ tests/             # Type checking (strict mode, python 3.9)
```

Full quality gate:

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest
```

### Running the CLI

```bash
rhapsody-cli element add --type class --name MyClass
rhapsody-cli element query
rhapsody-cli project open path/to/project.rpy
rhapsody-cli project list
```

**Available command groups:** `element` | `io` | `project`

## Architecture

Three layers, each building on the one below:

### Layer 1 — Core Model Wrapping (`src/rhapsody_cli/models/`)

Base infrastructure in `core.py`:
- `RPModelElement` (`models/core.py:94`) — base class for all wrapped COM objects. Mirrors `IRPModelElement`. Method names match Java API exactly (`getName`, `setName`, `getMetaClass`, `getGUID`).
- `RPUnit` (`models/core.py:1349`) — elements that can be saved as files (`save()`, `getFilename()`, `getNestedElements()`).
- `RPCollection` (`models/core.py:1627`) — iterable/indexable wrapper over `IRPCollection`. 1-based COM indexing is translated to 0-based Python indexing in `__getitem__`.
- `call_com(func)` (`models/core.py:42`) — invokes a COM call, translating `pywintypes.com_error` into `RhapsodyRuntimeException`. **All COM calls must go through `call_com(lambda: ...)`** or through the helper accessors.
- `wrap(com_obj)` (`models/core.py:61`) — factory that dispatches a raw COM object to the correct wrapper subclass using `_WRAPPER_REGISTRY`.
- `register_wrapper(meta_class, cls)` (`models/core.py:37`) — registers a wrapper class for a given `getMetaClass()` string.
- `_get_method_or_property` / `_set_method_or_property` — helpers that prefer Java-style methods (`getName()`) but fall back to bare COM properties (`name`) because different Rhapsody Prog IDs expose attributes differently. The app uses `Rhapsody2.Application.1` (property-style).

Concrete element wrappers live in `models/elements/` and register themselves at import time:
- `containment.py` — `RPPackage`, `RPProject`
- `classifiers.py` — `RPClassifier`, `RPClass`, `RPActor`
- `relations.py`, `diagrams.py`, `requirements.py`, `variables.py`

`models/elements/__init__.py` imports all element submodules so their `register_wrapper()` calls fire on package import. `rhapsody_cli/__init__.py` imports `models` to ensure the registry is populated whenever the public API is used.

### Layer 2 — Application Entry Point (`src/rhapsody_cli/application.py`)

`RhapsodyApplication` wraps `IRPApplication` (the top-level Rhapsody automation object). Three connection modes:
- `attach()` (`application.py:28`) — connect to a running instance via `GetActiveObject`
- `launch()` (`application.py:38`) — start a new instance via `Dispatch`
- `connect(prefer_attach=True)` (`application.py:48`) — try attach, fall back to launch

Prog ID: `Rhapsody2.Application.1` (`application.py:18`). `pywin32` imports are guarded so the module can be imported on non-Windows platforms (e.g. for Sphinx on Read the Docs); the COM calls themselves fail at runtime there.

### Layer 3 — CLI Layer (`src/rhapsody_cli/cli/` + `commands/` + `actions/`)

The CLI uses **argparse** (stdlib) with a class-based, two-tier command/action architecture (recently migrated from Click — see git history). This "PanGu style" pattern is mandatory for all new CLI code.

**Dispatch flow** (`cli/cli.py:16`):
1. `main()` reads `sys.argv[1]` as the command group name (`element` | `io` | `project`)
2. Instantiates the matching `AbstractCommand` subclass with the remaining args
3. The command group constructs an `argparse.ArgumentParser` with one subparser per `AbstractAction`
4. On `execute()`, dispatches to the selected action's `execute(args)`

**Command groups** (`commands/abstract_command.py:11`):
- Subclass `AbstractCommand`, override `get_actions()` to return the list of action instances
- `__init__` builds `{command_id: action}` map and parses args
- `execute()` (`abstract_command.py:62`) looks up the selected action and calls `action.execute(parsed_args)`

**Actions** (`actions/abstract_action.py:12`):
- Each action = one subcommand (e.g. `ElementAddAction` → `element add`)
- Instance attributes: `command_id` (subcommand identifier), `logger` (instance-specific `logging.getLogger(self.__class__.__name__)`)
- Must implement `init_arguments(sub_parser)` (register its own subparser + args) and `execute(args)` (business logic)
- Base hierarchy: `AbstractAction` → `RhapsodyContextAction` (adds connection/error handling) → `ElementManagementAction` (adds `_get_active_project()` helper)

**Support classes:**
- `RhapsodyContextAction` (`actions/abstract_action.py`) — holds per-action Rhapsody connection state directly: `self._app` (a `RhapsodyApplication`, lazily connected via `_connect_app()`), `self._project` (the active `RPProject`), and `self.output_format` (set by `AbstractCommand.execute(output_format=...)` from the global `--format` CLI flag).
- `OutputFormatter` (`cli/formatters.py`) — table/JSON/CSV output rendering
- `CliLoggingConfigurator` (`cli/logging_config.py`) — configures logging; `-v`/`--verbose` enables DEBUG

**Data flow:**

```
CLI argv → main() → AbstractCommand (argparse) → AbstractAction.execute()
    → RhapsodyApplication → call_com() → COM API
    → wrap() dispatches to RPModelElement subclass
    → OutputFormatter (table/json/csv)
```

## Key Conventions

### API Mirroring

Method names and class hierarchy **exactly mirror** the Rhapsody Java API (`com.telelogic.rhapsody.core`). Java `com.telelogic.rhapsody.core.IRPClass` → Python `rhapsody_cli.models.elements.classifiers.RPClass`. Java `getNestedElements()` → Python `getNestedElements()`. Preserve this mirroring when adding wrappers.

### Wrapper Registry Pattern

New element types must register at module import time:

```python
# src/rhapsody_cli/models/elements/myclass.py
from rhapsody_cli.models.core import RPModelElement, AbstractRPModelElement

class RPMyClass(RPModelElement):
    """Wraps IRPMyClass."""
    pass

AbstractRPModelElement.register_wrapper("MyClass", RPMyClass)
```

Then add the import to `models/elements/__init__.py` so registration fires on package import.

### TDD is Mandatory

Write tests **before** implementation (red → green → refactor). Coverage target: 80% minimum, 90%+ preferred. Tests use fake COM objects from `tests/unit/models/fakes.py` (`make_fake_element`, `make_fake_collection`); never use real COM calls in tests.

### Constants

All constants use `SCREAMING_SNAKE_CASE` (module-level and class-level). See `docs/CODE_GUIDELINES.md` for the full naming rules.

### Type Annotations

- **Do NOT use `from __future__ import annotations`** — it is forbidden in this codebase (see `docs/CODE_GUIDELINES.md`). Use string-quoted forward refs or `TYPE_CHECKING` imports instead.
- mypy runs in strict mode; all functions need return type annotations.
- Use `# type: ignore[attr-defined]` sparingly for `win32com`/`pywintypes` (they lack stubs; overrides in `pyproject.toml` already ignore missing imports for those modules).

### Error Handling

- Wrap all COM calls in `call_com(lambda: ...)` so `pywintypes.com_error` becomes `RhapsodyRuntimeException`.
- `RhapsodyConnectionError` — connection failures (no running instance, pywin32 missing).
- `RhapsodyRuntimeException` — COM API failures.
- CLI actions use the helpers on `RhapsodyContextAction` (`_handle_connection_error`, `_handle_execution_error`) for consistent logging + stderr output.

### Element Deletion

When deleting elements, always call the wrapped `element.deleteFromProject()` method. Never call `element._com.delete()` directly — the raw COM object does not expose a `delete()` method.

## Git Workflow

- **All changes go on feature branches, never directly to `main`.** Branch naming: `feature/<short-description>`, `fix/<...>`, `refactor/<...>`, `docs/<...>` (kebab-case with type prefix).
- Commits are human-authored only; do not add `Co-authored-by: Copilot` (or similar AI co-author) trailers.
- Open a PR for review; delete the local branch after merge.

## CI/CD

- `.github/workflows/python-package.yml` — runs `ruff check`, `black --check`, `mypy` (Python < 3.10 only), and `pytest tests/unit -v --cov` across Python 3.8–3.13 on `windows-latest`. Integration/system tests are not run in CI (they require a live Rhapsody instance).
- `.github/workflows/python-publish.yml` — auto-publishes to PyPI on GitHub release.

## Common Tasks

### Add a new element wrapper

1. Create `src/rhapsody_cli/models/elements/<subpackage>/model_myclass.py` (choose subpackage based on element type: `classifiers/`, `containment/`, `relations/`, etc.)
2. Define `RPMyClass(RPModelElement)` with methods mirroring the Java API
3. Call `AbstractRPModelElement.register_wrapper("MyClass", RPMyClass)` at module level
4. Write tests in `tests/unit/models/elements/test_myclass.py` using fakes from `tests/unit/models/fakes.py`
5. Add the import to the subpackage's `__init__.py` so registration fires on import

### Add a new CLI subcommand

1. Write tests first in appropriate `tests/unit/cli/`, `tests/unit/commands/`, or `tests/unit/actions/` module
2. Create an action class inheriting from `AbstractAction` (or `RhapsodyContextAction` / `ElementManagementAction`)
3. Implement `init_arguments(sub_parser)` to register the subparser and `execute(args)` for business logic
4. Register the action in the appropriate command group's `get_actions()` method (`ElementCommand`, `ProjectCommand`, etc.)
5. Verify unit tests pass and run the full quality gate

## Documentation

- `docs/CODE_GUIDELINES.md` — comprehensive TDD and architecture rules (naming, class-based patterns, testing). Read this before adding features.
- `docs/superpowers/specs/2026-07-06-rhapsody-cli-com-api-design.md` — full architecture and design rationale.
- `docs/requirements/` — requirements specifications; `docs/tests/` — test specifications.
- `docs/traceability_matrix.md` — requirements-to-code traceability.

## Documentation Status

All developer documentation (`.github/copilot-instructions.md`, `docs/CODE_GUIDELINES.md`, and the user/requirements `.rst`/`.md` files) has been updated to reflect the argparse-based CLI architecture. Historical plan docs under `docs/superpowers/plans/` are dated records and are intentionally not updated.
