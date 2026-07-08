# Project Review and Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all issues found in the project review: remove the forbidden `from __future__ import annotations` import and rewrite modern type syntax to `typing` equivalents, wrap direct COM calls in `call_com()`, fix the mypy config so type-checking runs, auto-skip integration tests when no Rhapsody instance is available, and rewrite all stale Click references in documentation to reflect the argparse migration.

**Architecture:** The codebase has three layers (core model wrapping, application entry point, argparse-based CLI). The CLI migrated from Click to argparse (PanGu style: `AbstractCommand` groups dispatch to `AbstractAction` subcommands). Code conventions in `docs/CODE_GUIDELINES.md` forbid `from __future__ import annotations` and require Python 3.8 compatibility, so modern PEP 585/604 syntax must be rewritten to `typing.Optional`/`List`/`Dict`/`Union`. All COM calls must go through `call_com(lambda: ...)` in `models/_core.py` so `pywintypes.com_error` becomes `RhapsodyRuntimeException`.

**Tech Stack:** Python 3.8+, pywin32 (COM), argparse (CLI), tabulate + rich (CLI output), pytest/ruff/black/mypy (quality gates).

## Global Constraints

- `requires-python` stays `>=3.8` (do NOT change).
- CI matrix in `.github/workflows/python-package.yml` stays `["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]` (do NOT change).
- `from __future__ import annotations` is FORBIDDEN — remove everywhere in `src/` and `tests/`. The ban in `docs/CODE_GUIDELINES.md` stays in force.
- Do NOT touch historical plan docs under `docs/superpowers/plans/` (they are dated records; their Click/future-import mentions stay as-is). The only file you create in that directory is this plan itself.
- All COM calls go through `call_com(lambda: ...)` from `rhapsody_cli.models._core`.
- Commit style: feature branches only, never commit to `main`. No AI co-author trailers.
- Quality gates must pass at the end: `ruff check src/ tests/`, `black --check src/ tests/`, `mypy src/ tests/`, `pytest`.

---

## File Structure

**Modified (code):**
- `pyproject.toml` — bump mypy `python_version` from `"3.8"` to `"3.9"`.
- `src/rhapsody_cli/commands/abstract_command.py` — remove future import, rewrite `list[...]`/`dict[...]`/`X | None` to `typing` equivalents.
- `src/rhapsody_cli/commands/element_command.py` — remove future import, rewrite `list[...]`.
- `src/rhapsody_cli/commands/io_command.py` — remove future import, rewrite `list[...]`.
- `src/rhapsody_cli/commands/project_command.py` — remove future import, rewrite `list[...]`.
- `src/rhapsody_cli/actions/element_action.py` — wrap direct `._com` calls in `call_com()`.
- 26 test files — remove `from __future__ import annotations` line; rewrite modern syntax in `tests/unit/commands/test_abstract_command.py` and `tests/unit/models/fakes.py`.
- `tests/integration/conftest.py` — add session skip guard for Rhapsody availability (also remove future import).

**Modified (docs):**
- `.github/copilot-instructions.md` — rewrite Click→argparse, fix test paths, update examples.
- `docs/CODE_GUIDELINES.md` — rewrite Click examples to argparse, keep the future-import ban.
- `docs/index.rst` — "Click-based" → "argparse-based"; fix project structure tree.
- `docs/user_guide/installation.rst` — remove `click` from dependency lists.
- `docs/user_guide/cli_tools.rst` — "built using Click" → "built using argparse".
- `docs/requirements/swr_cli_requirements.md` — rewrite Click-group requirement to argparse dispatcher.
- `docs/contributing.rst` — line length 100 → 200; fix stale test paths in examples.
- `CLAUDE.md` — remove the "Note on Stale Documentation" section (no longer accurate after fixes).

---

### Task 1: Fix mypy `python_version` config

The installed mypy no longer supports targeting Python 3.8 (`Python 3.8 is not supported (must be 3.9 or higher)`), so `mypy src/ tests/` fails before checking any code. Bump to 3.9. The code still supports 3.8 at runtime because Task 3 rewrites all annotations to `typing` equivalents (3.8-compatible). mypy targeting 3.9 checks against a 3.9 stdlib surface; the 3.8 CI matrix entry catches any accidental 3.9-only stdlib use at runtime.

**Files:**
- Modify: `pyproject.toml:54`

**Interfaces:**
- Consumes: none.
- Produces: a mypy config that runs successfully on the installed mypy version.

- [ ] **Step 1: Edit pyproject.toml**

Change line 54 in `pyproject.toml` from:

```toml
python_version = "3.8"
```

to:

```toml
python_version = "3.9"
```

Leave `[tool.mypy].strict = true`, `warn_unused_ignores = true`, and the `[[tool.mypy.overrides]]` blocks unchanged.

- [ ] **Step 2: Verify mypy runs (it will still show type errors until Task 3; just confirm it no longer fails with the version error)**

Run: `mypy src/ tests/ 2>&1 | head -5`
Expected: output shows actual type-checking results (not "Python 3.8 is not supported"). It is fine if there are still type errors from the `X | None` syntax — Task 3 fixes those.

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "fix: bump mypy python_version to 3.9 (3.8 unsupported by current mypy)"
```

---

### Task 2: Wrap direct COM calls in `element_action.py`

`src/rhapsody_cli/actions/element_action.py:232-246` calls `._com.delete()`, `._com.deleteClass(...)`, `._com.deleteActor(...)`, `._com.deletePackage(...)` directly, bypassing `call_com()` and therefore `RhapsodyRuntimeException` translation. This is inconsistent with the rest of the codebase.

**Files:**
- Modify: `src/rhapsody_cli/actions/element_action.py:1-10` (imports) and `:232-246` (COM calls)

**Interfaces:**
- Consumes: `call_com` from `rhapsody_cli.models._core` (already exported).
- Produces: `ElementDeleteAction.execute` that translates COM errors consistently.

- [ ] **Step 1: Add the `call_com` import**

In `src/rhapsody_cli/actions/element_action.py`, after the existing imports (lines 3-7), add `call_com` to the import block. Replace:

```python
import argparse
import sys

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
```

with:

```python
import argparse
import sys

from rhapsody_cli.actions.abstract_action import ElementManagementAction
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.models._core import call_com
```

- [ ] **Step 2: Wrap the four direct COM calls**

Replace lines 232-246 (the `if hasattr(element_to_delete._com, "delete"):` block through the `Package` branch):

```python
            # Try direct delete method first (if available)
            if hasattr(element_to_delete._com, "delete"):
                element_to_delete._com.delete()
                deleted = True
            else:
                # Fall back to parent container methods
                if meta_class == "Class":
                    parent._com.deleteClass(element_to_delete._com)
                    deleted = True
                elif meta_class == "Actor":
                    parent._com.deleteActor(element_to_delete._com)
                    deleted = True
                elif meta_class == "Package":
                    parent._com.deletePackage(element_to_delete._com)
                    deleted = True
```

with:

```python
            # Try direct delete method first (if available)
            if hasattr(element_to_delete._com, "delete"):
                call_com(lambda: element_to_delete._com.delete())
                deleted = True
            else:
                # Fall back to parent container methods
                if meta_class == "Class":
                    call_com(lambda: parent._com.deleteClass(element_to_delete._com))
                    deleted = True
                elif meta_class == "Actor":
                    call_com(lambda: parent._com.deleteActor(element_to_delete._com))
                    deleted = True
                elif meta_class == "Package":
                    call_com(lambda: parent._com.deletePackage(element_to_delete._com))
                    deleted = True
```

Leave the `hasattr(element_to_delete._com, "delete")` check as-is — `hasattr` is a pure attribute access, not a COM invocation.

- [ ] **Step 3: Verify lint + format + existing tests pass**

Run: `ruff check src/rhapsody_cli/actions/element_action.py && black --check src/rhapsody_cli/actions/element_action.py && pytest tests/unit/commands/ -q`
Expected: ruff clean, black clean, all unit command tests pass.

- [ ] **Step 4: Commit**

```bash
git add src/rhapsody_cli/actions/element_action.py
git commit -m "fix: wrap direct COM delete calls in call_com for error translation"
```

---

### Task 3: Remove `from __future__ import annotations` and rewrite modern type syntax in `src/`

`docs/CODE_GUIDELINES.md:60-83` forbids `from __future__ import annotations`. Four `src/` command files use it, and `abstract_command.py` uses PEP 585 (`list[str]`, `dict[...]`) and PEP 604 (`str | None`) syntax that requires it on Python 3.8. Rewrite to `typing` equivalents and remove the import.

**Files:**
- Modify: `src/rhapsody_cli/commands/abstract_command.py`
- Modify: `src/rhapsody_cli/commands/element_command.py`
- Modify: `src/rhapsody_cli/commands/io_command.py`
- Modify: `src/rhapsody_cli/commands/project_command.py`

**Interfaces:**
- Consumes: `AbstractAction` from `rhapsody_cli.actions.abstract_action`.
- Produces: command classes with the same public API, but 3.8-compatible annotations (`List[str]`, `List[AbstractAction]`, `Dict[str, AbstractAction]`, `Optional[str]`, `Optional[argparse.Namespace]`).

- [ ] **Step 1: Rewrite `abstract_command.py`**

Replace the entire file content with:

```python
"""Abstract base class for all CLI command groups."""

import argparse
import sys
from typing import Dict, List, Optional

from rhapsody_cli.actions.abstract_action import AbstractAction


class AbstractCommand:
    """Base class for all CLI command groups.

    Subclasses provide their own set of AbstractAction instances via
    get_actions(). Each action registers its own subparser/arguments and
    owns its own execution logic - the command group itself only owns
    top-level parsing and dispatch to the selected action.
    """

    def __init__(self, command: str, args: List[str]) -> None:
        """Initialize the command group and parse its subcommand arguments.

        Args:
            command: Name of the command group (e.g. "element", "io", "project")
            args: Raw command-line arguments after the command group name
        """
        self._args = args
        self._subcommand: Optional[str] = None
        self._parsed_args: Optional[argparse.Namespace] = None

        parser = argparse.ArgumentParser(
            prog=f"rhapsody-cli {command}",
            description=f"Manage {command}s",
            add_help=True,
        )

        actions = self.get_actions()
        self._sub_commands: Dict[str, AbstractAction] = {action.command_id: action for action in actions}

        sub_parsers = parser.add_subparsers(dest="subcommand", help=f"{command.capitalize()} operations")
        for action in actions:
            action.init_arguments(sub_parsers)

        try:
            self._parsed_args = parser.parse_args(args)
            self._subcommand = self._parsed_args.subcommand
        except SystemExit:
            # argparse calls sys.exit on error, we want to propagate that
            raise

        if not self._subcommand:
            parser.print_help()
            sys.exit(2)

    def get_actions(self) -> List[AbstractAction]:
        """Return the list of actions (subcommands) for this command group.

        Subclasses must override this to register their own actions.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.get_actions() must be implemented")

    def execute(self, **kwargs: object) -> None:
        """Dispatch execution to the action matching the parsed subcommand."""
        action = self._sub_commands.get(self._subcommand) if self._subcommand else None
        if action is None or self._parsed_args is None:
            print(f"Error: Unknown subcommand '{self._subcommand}'", file=sys.stderr)
            sys.exit(2)
        action.execute(self._parsed_args)

    def usage(self, error: str = "") -> None:
        """Print usage message and exit.

        Args:
            error: Optional error message to display before usage
        """
        if error:
            print(error)
        print(f"\nUsage: rhapsody-cli {self._command_name()} [options]")
        sys.exit(2)

    def _command_name(self) -> str:
        """Get the command name (lowercase class name)."""
        return self.__class__.__name__.replace("Command", "").lower()
```

- [ ] **Step 2: Rewrite `element_command.py`**

Replace the entire file content with:

```python
"""Element command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.element_action import (
    ElementAddAction,
    ElementDeleteAction,
    ElementQueryAction,
    ElementViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ElementCommand(AbstractCommand):
    """Element command group - handles element subcommands (add, view, query, delete)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize ElementCommand and parse element subcommands.

        Args:
            args: Arguments after 'element' command
                (e.g., ['add', '--type', 'class', '--name', 'MyClass'])
        """
        super().__init__("element", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the element subcommand actions."""
        return [
            ElementAddAction(),
            ElementViewAction(),
            ElementQueryAction(),
            ElementDeleteAction(),
        ]
```

- [ ] **Step 3: Rewrite `io_command.py`**

First read the current file to preserve its exact action imports, then apply the same pattern: remove `from __future__ import annotations`, change `list[str]` → `List[str]` and `list[AbstractAction]` → `List[AbstractAction]`, add `from typing import List`.

Run: read `src/rhapsody_cli/commands/io_command.py` to see current contents, then replace the `from __future__ import annotations` line (delete it) and the two annotations:
- `def __init__(self, args: list[str]) -> None:` → `def __init__(self, args: List[str]) -> None:`
- `def get_actions(self) -> list[AbstractAction]:` → `def get_actions(self) -> List[AbstractAction]:`
- Add `from typing import List` after the docstring, before the first local import.

- [ ] **Step 4: Rewrite `project_command.py`**

Same pattern as Step 3, applied to `src/rhapsody_cli/commands/project_command.py`:
- Delete `from __future__ import annotations`.
- `def __init__(self, args: list[str]) -> None:` → `def __init__(self, args: List[str]) -> None:`
- `def get_actions(self) -> list[AbstractAction]:` → `def get_actions(self) -> List[AbstractAction]:`
- Add `from typing import List` after the docstring, before the first local import.

- [ ] **Step 5: Verify no future import or modern syntax remains in src/commands/**

Run: `grep -rn "from __future__ import annotations" src/ && grep -rn "list\[\|dict\[\|tuple\[\|set\[\| | None\| | str" src/rhapsody_cli/commands/`
Expected: the first grep returns no matches in `src/`; the second returns no matches in `src/rhapsody_cli/commands/`.

- [ ] **Step 6: Verify quality gates on the changed files**

Run: `ruff check src/rhapsody_cli/commands/ && black --check src/rhapsody_cli/commands/ && mypy src/rhapsody_cli/commands/`
Expected: all clean, no type errors.

- [ ] **Step 7: Run the unit test suite**

Run: `pytest tests/unit/ -q`
Expected: all unit tests pass (the command tests exercise these classes).

- [ ] **Step 8: Commit**

```bash
git add src/rhapsody_cli/commands/
git commit -m "refactor: remove forbidden from __future__ import annotations and use typing generics in commands"
```

---

### Task 4: Remove `from __future__ import annotations` from all test files and rewrite modern type syntax

26 test files use the forbidden import. Most have no modern syntax (only the import line needs removal). Two files (`tests/unit/commands/test_abstract_command.py` and `tests/unit/models/fakes.py`) also use `list[...]` / `X | None` syntax that must be rewritten to `typing` equivalents.

**Files:**
- Modify (import-only removal): every file listed below under "Import-only files".
- Modify (import + syntax rewrite): `tests/unit/commands/test_abstract_command.py`, `tests/unit/models/fakes.py`.

**Interfaces:**
- Consumes: none.
- Produces: test suite with no `from __future__ import annotations` and 3.8-compatible annotations.

Import-only files (delete the single `from __future__ import annotations` line from each; no other changes):
- `tests/unit/conftest.py`
- `tests/unit/test_application.py`
- `tests/unit/test_public_api.py`
- `tests/unit/cli/test_core.py`
- `tests/unit/cli/test_logging_config.py`
- `tests/unit/models/test_core.py`
- `tests/unit/models/elements/test_actor.py`
- `tests/unit/models/elements/test_annotation.py`
- `tests/unit/models/elements/test_attribute.py`
- `tests/unit/models/elements/test_class.py`
- `tests/unit/models/elements/test_classifier.py`
- `tests/unit/models/elements/test_diagram.py`
- `tests/unit/models/elements/test_instance.py`
- `tests/unit/models/elements/test_interface_item.py`
- `tests/unit/models/elements/test_operation.py`
- `tests/unit/models/elements/test_package.py`
- `tests/unit/models/elements/test_project.py`
- `tests/unit/models/elements/test_relation.py`
- `tests/unit/models/elements/test_requirement.py`
- `tests/unit/models/elements/test_statechart.py`
- `tests/unit/models/elements/test_usecase.py`
- `tests/unit/models/elements/test_variable.py`
- `tests/unit/exceptions/test_core.py`
- `tests/integration/conftest.py`
- `tests/integration/cli/test_element_cli_integration.py`
- `tests/system/conftest.py`
- `tests/system/cli/test_element_cli_subprocess.py`

- [ ] **Step 1: Delete the `from __future__ import annotations` line from every import-only file**

For each file in the import-only list above, remove the line `from __future__ import annotations` (and the blank line that follows it if it leaves a double blank at the top, to keep black happy).

- [ ] **Step 2: Rewrite `tests/unit/commands/test_abstract_command.py`**

Remove `from __future__ import annotations` (line 3). Then fix the two modern-syntax annotations:
- Line 18: `self.executed_with: argparse.Namespace | None = None` → `self.executed_with: Optional[argparse.Namespace] = None`
- Line 33: `def __init__(self, args: list[str], action: AbstractAction) -> None:` → `def __init__(self, args: List[str], action: AbstractAction) -> None:`
- Add `from typing import List, Optional` to the stdlib import block near the top of the file (after `import argparse` or wherever the existing stdlib imports are, maintaining import order: stdlib → third-party → local).

- [ ] **Step 3: Rewrite `tests/unit/models/fakes.py`**

Remove `from __future__ import annotations` (line 7). Then fix:
- Line 33: `def make_fake_collection(items: list[Any]) -> MagicMock:` → `def make_fake_collection(items: List[Any]) -> MagicMock:`
- Add `from typing import Any, List` to the stdlib import block (the file already imports `Any` from `typing` somewhere — merge `List` into that same import line, e.g. `from typing import Any, List`).

- [ ] **Step 4: Scan all test files for any remaining modern syntax**

Run: `grep -rn "list\[\|dict\[\|tuple\[\|set\[\| | None\| | str\| | int\| | bool" tests/`
Expected: no matches in `tests/` (ignore any matches inside string literals that are not annotations; if any appear, judge case-by-case, but none are expected).

- [ ] **Step 5: Verify no future import remains in tests/**

Run: `grep -rn "from __future__ import annotations" tests/`
Expected: no matches.

- [ ] **Step 6: Run the full quality gates**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit/ tests/system/ -q`
Expected: all clean, all tests pass (integration tests are addressed in Task 5; run them separately there).

- [ ] **Step 7: Commit**

```bash
git add tests/
git commit -m "refactor: remove from __future__ import annotations from tests and use typing generics"
```

---

### Task 5: Add integration-test skip guard for Rhapsody availability

Two integration tests in `tests/integration/cli/test_element_cli_integration.py` fail with `RhapsodyConnectionError` when no Rhapsody COM instance is running. Add a session-scoped autouse fixture in `tests/integration/conftest.py` that probes for a usable Rhapsody (attach + active project) and skips the whole integration session if unavailable. Also check whether the system tests need the same guard.

**Files:**
- Modify: `tests/integration/conftest.py`
- Possibly modify: `tests/system/conftest.py` (if system tests exhibit the same failure)

**Interfaces:**
- Consumes: `RhapsodyApplication` from `rhapsody_cli`, `RhapsodyConnectionError` and `RhapsodyRuntimeException` from `rhapsody_cli.exceptions`.
- Produces: a pytest fixture `_require_rhapsody` that skips integration tests when Rhapsody is unavailable.

- [ ] **Step 1: First, run the system tests to see if they also fail without Rhapsody**

Run: `pytest tests/system/ -q 2>&1 | tail -20`
Expected: observe whether system tests fail with `RhapsodyConnectionError` (same root cause) or pass/skip on their own. Note the result for Step 3.

- [ ] **Step 2: Add the skip fixture to `tests/integration/conftest.py`**

The file currently contains (after Task 4 removed the future import):

```python
"""Integration test configuration."""

import sys
from pathlib import Path

# Add unit directory to Python path so imports from unit tests work
unit_dir = Path(__file__).parent.parent / "unit"
sys.path.insert(0, str(unit_dir))
```

Replace the entire file with:

```python
"""Integration test configuration."""

import sys
from pathlib import Path

import pytest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException

# Add unit directory to Python path so imports from unit tests work
unit_dir = Path(__file__).parent.parent / "unit"
sys.path.insert(0, str(unit_dir))


@pytest.fixture(scope="session", autouse=True)
def _require_rhapsody() -> None:
    """Skip the entire integration session if no Rhapsody with an open project is available."""
    try:
        app = RhapsodyApplication.attach()
        app.activeProject()
    except (RhapsodyConnectionError, RhapsodyRuntimeException) as exc:
        pytest.skip(f"No running Rhapsody with an open project: {exc}", allow_module_level=False)
```

- [ ] **Step 3: Add the same guard to `tests/system/conftest.py` if Step 1 showed failures**

If the system tests in Step 1 failed with `RhapsodyConnectionError`, apply the same fixture pattern to `tests/system/conftest.py`. First read the current file, then add the `pytest`, `RhapsodyApplication`, and exception imports, plus the same `_require_rhapsody` fixture. Preserve any existing content (e.g., the `sys.path` manipulation that mirrors the integration conftest).

If the system tests passed or already skip on their own, do not modify `tests/system/conftest.py`.

- [ ] **Step 4: Run the integration tests and confirm they SKIP (not fail)**

Run: `pytest tests/integration/ -v 2>&1 | tail -20`
Expected: `2 skipped` (with the skip reason shown), `0 failed`.

- [ ] **Step 5: Run the full test suite and confirm everything is green/skipped**

Run: `pytest -q`
Expected: `260 passed, 2 skipped, 0 failed` (or similar with system tests included).

- [ ] **Step 6: Commit**

```bash
git add tests/integration/conftest.py tests/system/conftest.py
git commit -m "test: skip integration tests when no Rhapsody instance is available"
```

(Only add `tests/system/conftest.py` to the commit if Step 3 modified it.)

---

### Task 6: Fix stale Click references in `.github/copilot-instructions.md`

This developer-onboarding doc still describes the Click-based architecture and wrong test paths (`tests/cli/`, `tests/elements/`) from before the argparse migration. Rewrite it to reflect the current argparse `AbstractCommand`/`AbstractAction` pattern and the real `tests/unit/`, `tests/integration/`, `tests/system/` structure.

**Files:**
- Modify: `.github/copilot-instructions.md` (rewrite multiple sections)

**Interfaces:**
- Consumes: the architecture facts gathered during review.
- Produces: an accurate developer-reference doc.

- [ ] **Step 1: Fix the "Quick Reference" header (line 9)**

Change:

```text
**CLI Framework:** Click with class-based command architecture
```

to:

```text
**CLI Framework:** argparse (stdlib) with class-based command/action architecture
```

- [ ] **Step 2: Fix the installation comments (lines 18-19)**

Change:

```bash
pip install -e ".[dev,cli]"  # Full dev setup: required to run the full test suite (CLI tests need click/tabulate/rich)
pip install -e ".[dev]"      # Dev tools only (ruff/black/mypy/pytest) - tests/cli/* will fail to import
```

to:

```bash
pip install -e ".[dev,cli]"  # Full dev setup: required to run the full test suite (CLI tests need tabulate/rich)
pip install -e ".[dev]"      # Dev tools only (ruff/black/mypy/pytest) - tests that import tabulate/rich will fail
```

- [ ] **Step 3: Fix the testing section (lines 28-29)**

Change:

```bash
pytest tests/cli/            # Run only CLI tests
pytest tests/elements/       # Run only element tests
```

to:

```bash
pytest tests/unit/cli/               # Run only CLI unit tests
pytest tests/unit/models/elements/   # Run only element tests
```

- [ ] **Step 4: Fix the type-checking note (line 43)**

Change:

```bash
mypy src/ tests/            # Type checking (Python 3.9 strict mode)
```

to:

```bash
mypy src/ tests/            # Type checking (strict mode, python_version 3.9)
```

- [ ] **Step 5: Rewrite the "Architecture > CLI Layer" bullet (lines 138-143)**

Change:

```text
3. **CLI Layer** (`src/rhapsody_cli/cli/`)
   - Click-based command-line interface using class-based architecture
   - Command groups: `project`, `element`, `io`
   - Context: `RhapsodyContext` manages the current Rhapsody state
   - Formatters: `OutputFormatter` handles table/JSON/CSV output
```

to:

```text
3. **CLI Layer** (`src/rhapsody_cli/cli/` + `src/rhapsody_cli/commands/` + `src/rhapsody_cli/actions/`)
   - argparse-based (stdlib) CLI using a class-based command/action architecture
   - `main()` dispatches on the first argv token to an `AbstractCommand` subclass
   - Command groups (`ElementCommand`, `ProjectCommand`, `IOCommand`) each own a set of `AbstractAction` subcommands
   - Each action registers its own argparse subparser (`init_arguments`) and owns its execution (`execute`)
   - Context: `RhapsodyContext` manages the current Rhapsody state
   - Formatters: `OutputFormatter` handles table/JSON/CSV output
```

- [ ] **Step 6: Replace the class-based command examples (lines 183-215)**

Replace the entire Click example block (the `class OpenProjectCommand(click.Command):` ... `class ProjectCommandGroup(click.Group):` ... code) with the argparse equivalent:

```python
# ✅ CORRECT: Class-based action (argparse)
class ElementAddAction(ElementManagementAction):
    def __init__(self) -> None:
        super().__init__(command_id="add")

    def init_arguments(self, sub_parser) -> None:
        add_parser = sub_parser.add_parser("add", help="Add a new element")
        add_parser.add_argument("--type", required=True)
        add_parser.add_argument("--name", required=True)

    def execute(self, args: argparse.Namespace) -> None:
        # Business logic here
        ...

# Command groups inherit from AbstractCommand and register actions in get_actions():
class ElementCommand(AbstractCommand):
    def __init__(self, args: List[str]) -> None:
        super().__init__("element", args)

    def get_actions(self) -> List[AbstractAction]:
        return [ElementAddAction(), ElementViewAction(), ElementQueryAction(), ElementDeleteAction()]

# ❌ WRONG: Function-based with decorators (Click style) — not used in this project
```

- [ ] **Step 7: Fix the error-handling example (lines 234-247)**

Change the Click-based `click.echo` / `click.Abort` example:

```python
try:
    ctx.connect("attach")
except RhapsodyConnectionError as e:
    click.echo(f"Connection error: {e}", err=True)
    raise click.Abort() from e
```

to the argparse equivalent used by the actual actions:

```python
try:
    ctx.connect("attach")
except RhapsodyConnectionError as e:
    self._handle_connection_error(e)
    sys.exit(1)
```

- [ ] **Step 8: Fix the code-layout tree (lines 280-318)**

Replace the `src/rhapsody_cli/` tree (which shows `cli/commands/project.py` containing `ProjectCommandGroup`) with the actual structure:

```text
src/rhapsody_cli/
├── __init__.py                    # Public API exports
├── application.py                 # RhapsodyApplication entry point
├── exceptions/                    # Exception types
│   ├── __init__.py
│   └── core.py                   # RhapsodyConnectionError, RhapsodyRuntimeException
├── models/                        # Element wrappers
│   ├── __init__.py
│   ├── _core.py                  # RPModelElement, wrap(), call_com(), registry
│   └── elements/                 # Specific element types
│       ├── __init__.py
│       ├── classifiers.py        # RPClass, RPClassifier, RPActor
│       ├── containment.py        # RPPackage, RPProject
│       └── ...                   # Other element types
├── commands/                      # CLI command groups (argparse, class-based)
│   ├── __init__.py
│   ├── abstract_command.py       # AbstractCommand base class
│   ├── element_command.py        # ElementCommand
│   ├── project_command.py        # ProjectCommand
│   └── io_command.py             # IOCommand
├── actions/                       # CLI subcommand actions (argparse, class-based)
│   ├── __init__.py
│   ├── abstract_action.py        # AbstractAction, RhapsodyContextAction, ElementManagementAction
│   ├── element_action.py         # ElementAddAction, ElementViewAction, ElementQueryAction, ElementDeleteAction
│   ├── project_action.py         # Project subcommand actions
│   └── io_action.py              # Import/export actions
├── cli/                           # CLI entry point and support
│   ├── main.py                   # Entry point (re-exports cli.main)
│   ├── cli.py                    # main() dispatcher
│   ├── context.py                # RhapsodyContext (state management)
│   ├── formatters.py             # OutputFormatter (table/JSON/CSV)
│   └── logging_config.py         # CliLoggingConfigurator
└── py.typed                       # PEP 561 marker (type stubs available)

tests/
├── unit/                          # Unit tests (mocked COM, no Rhapsody needed)
│   ├── conftest.py
│   ├── models/fakes.py            # Fake COM objects for testing
│   ├── cli/                       # CLI unit tests
│   ├── commands/                  # Command-group unit tests
│   ├── models/elements/           # Element wrapper tests
│   └── exceptions/                # Exception tests
├── integration/                   # Integration tests (require live Rhapsody)
└── system/                        # End-to-end subprocess tests
```

- [ ] **Step 9: Fix "When Adding Features" and "Common Tasks" (lines 328-357)**

Change line 334 `**Class-based CLI commands** — never function-based` to `**Class-based CLI actions** — never function-based or Click-decorator-based`.

Change the "Add a new CLI command" section (lines 350-356) to:

```text
1. Write tests first in appropriate tests/unit/cli/ or tests/unit/commands/ module
2. Create an action class inheriting from AbstractAction (or RhapsodyContextAction / ElementManagementAction)
3. Implement init_arguments() to register the subparser and execute() for business logic
4. Register the action in the appropriate command group's get_actions() (element/project/io)
5. Verify all unit tests pass
```

- [ ] **Step 10: Fix the references (line 383)**

Change:

```text
- **Click CLI Documentation:** https://click.palletsprojects.com/
```

to:

```text
- **argparse documentation:** https://docs.python.org/3/library/argparse.html
```

- [ ] **Step 11: Verify the file has no remaining Click references**

Run: `grep -n "click\|Click" .github/copilot-instructions.md`
Expected: no matches (or only the word "click" inside a URL/identifier that is genuinely not about the Click framework — there should be none).

- [ ] **Step 12: Commit**

```bash
git add .github/copilot-instructions.md
git commit -m "docs: update copilot-instructions for argparse migration and correct test paths"
```

---

### Task 7: Fix stale Click references in `docs/CODE_GUIDELINES.md`

This is the primary development-reference doc. It contains extensive Click examples (import order, TDD example, command-class pattern, integration-test example, code-review checklist). Rewrite all to argparse. Keep the `from __future__ import annotations` ban (lines 60-83) unchanged — it is correct per the project decision.

**Files:**
- Modify: `docs/CODE_GUIDELINES.md`

**Interfaces:**
- Consumes: the argparse action pattern from the actual source.
- Produces: an accurate, Click-free development guideline.

- [ ] **Step 1: Fix the import-order example (lines 111-126)**

Replace:

```python
# 1. Standard library
import sys
import argparse
import logging
from pathlib import Path

# 2. Third-party
import click
from tabulate import tabulate

# 3. Local application
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.exceptions import RhapsodyConnectionError
from rhapsody_cli.models.elements.class_ import RPClass
```

with:

```python
# 1. Standard library
import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

# 2. Third-party
from tabulate import tabulate

# 3. Local application
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.exceptions import RhapsodyConnectionError
from rhapsody_cli.models.elements.classifiers import RPClass
```

(Note: the actual element module is `classifiers`, not `class_` — fix that stale path too.)

- [ ] **Step 2: Fix the test organization tree (lines 155-166)**

Replace:

```text
tests/
├── cli/
│   ├── __init__.py
│   ├── test_commands.py       # Command class tests
│   ├── test_formatters.py     # Formatter tests
│   ├── test_context.py        # Context management tests
│   └── test_integration.py    # End-to-end CLI tests
├── test_application.py        # Application tests
├── test_core.py               # Core infrastructure tests
└── test_elements_*.py         # Element wrapper tests
```

with:

```text
tests/
├── unit/                      # Unit tests (mocked COM, no Rhapsody needed)
│   ├── conftest.py
│   ├── test_application.py    # Application tests
│   ├── test_public_api.py     # Public API tests
│   ├── cli/                   # CLI support tests (formatters, context, logging)
│   ├── commands/              # Command-group tests
│   ├── models/                # Core infrastructure + element wrapper tests
│   │   ├── test_core.py
│   │   ├── fakes.py           # Fake COM objects
│   │   └── elements/
│   └── exceptions/            # Exception tests
├── integration/               # Integration tests (require live Rhapsody)
└── system/                    # End-to-end subprocess tests
```

- [ ] **Step 3: Rewrite the TDD example (lines 174-244)**

Replace the entire "Example: TDD for a New CLI Command" block (Step 1 tests + Step 2 implementation) with an argparse-based version:

```python
# tests/unit/commands/test_element_command.py
import argparse
import pytest
from unittest.mock import MagicMock

from rhapsody_cli.commands.element_command import ElementCommand
from rhapsody_cli.actions.abstract_action import AbstractAction


class FakeAction(AbstractAction):
    def __init__(self) -> None:
        super().__init__(command_id="fake")

    def init_arguments(self, sub_parser) -> None:
        p = sub_parser.add_parser("fake", help="A fake action")
        p.add_argument("--name", required=True)

    def execute(self, args: argparse.Namespace) -> None:
        # Called by the command during dispatch in a real test
        ...


class TestElementCommandDispatch:
    def test_element_command_dispatches_to_selected_action(self) -> None:
        """Test: ElementCommand parses argv and dispatches to the matching action."""
        # ARRANGE
        action = FakeAction()
        # ACT / ASSERT via constructing the command and invoking execute
        # (Use a fake action that records its calls in a real test.)
        ...

    def test_element_command_with_unknown_subcommand_exits(self) -> None:
        """Test: ElementCommand exits with code 2 for an unknown subcommand."""
        with pytest.raises(SystemExit) as exc_info:
            ElementCommand(["nonexistent"])
        assert exc_info.value.code == 2
```

```python
# src/rhapsody_cli/commands/element_command.py
from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.element_action import (
    ElementAddAction,
    ElementDeleteAction,
    ElementQueryAction,
    ElementViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ElementCommand(AbstractCommand):
    """Element command group - handles element subcommands (add, view, query, delete)."""

    def __init__(self, args: List[str]) -> None:
        super().__init__("element", args)

    def get_actions(self) -> List[AbstractAction]:
        return [
            ElementAddAction(),
            ElementViewAction(),
            ElementQueryAction(),
            ElementDeleteAction(),
        ]
```

- [ ] **Step 4: Fix the "Run Tests" command under the TDD example (line 248-250)**

Change:

```bash
pytest tests/cli/test_commands.py::TestOpenProjectCommand -v
```

to:

```bash
pytest tests/unit/commands/test_element_command.py::TestElementCommandDispatch -v
```

- [ ] **Step 5: Fix "Class-Based Architecture" bullet (line 260)**

Change:

```text
- **CLI commands** → Command classes (inherit from `click.Command`)
```

to:

```text
- **CLI commands** → Command groups (inherit from `AbstractCommand`) and actions (inherit from `AbstractAction`)
```

- [ ] **Step 6: Replace the "CLI Commands" section (lines 355-450)**

Replace the entire "## CLI Commands" section (from `### Command Class Pattern` through the error-handling example) with an argparse-based version:

````markdown
## CLI Commands

### Action Class Pattern

All CLI subcommands use class-based actions, not Click decorators:

#### Structure

```python
class AbstractAction:
    """Base class for a single subcommand action."""

    def __init__(self, command_id: str = "") -> None:
        self.command_id = command_id
        self.logger = logging.getLogger(self.__class__.__name__)

    def init_arguments(self, sub_parser) -> None:
        raise NotImplementedError

    def execute(self, args: argparse.Namespace) -> None:
        raise NotImplementedError


class ElementAddAction(ElementManagementAction):
    def __init__(self) -> None:
        super().__init__(command_id="add")

    def init_arguments(self, sub_parser) -> None:
        add_parser = sub_parser.add_parser("add", help="Add a new element")
        add_parser.add_argument("--type", required=True)
        add_parser.add_argument("--name", required=True)
        self.add_verbose_argument(add_parser)

    def execute(self, args: argparse.Namespace) -> None:
        # Implementation
        ...
```

#### Command Group Pattern

```python
class ElementCommand(AbstractCommand):
    """Command group for element operations."""

    def __init__(self, args: List[str]) -> None:
        super().__init__("element", args)

    def get_actions(self) -> List[AbstractAction]:
        return [
            ElementAddAction(),
            ElementViewAction(),
            ElementQueryAction(),
            ElementDeleteAction(),
        ]
```

#### Error Handling in Actions

```python
def execute(self, args: argparse.Namespace) -> None:
    try:
        # Implementation
        ...
    except SystemExit:
        raise
    except RhapsodyConnectionError as e:
        self._handle_connection_error(e)
        sys.exit(1)
    except Exception as e:
        self._handle_execution_error(e, "Operation")
        sys.exit(1)
```
````

- [ ] **Step 7: Fix the OutputFormatter example annotations (lines 340, 508, 519, 525, 530)**

These examples use `list[str]` / `list[list[Any]]` annotations. Replace each with the `typing` equivalents to match the project's 3.8-compatible style:
- `def format(self, headers: list[str], rows: list[list[Any]]) -> str:` → `def format(self, headers: List[str], rows: List[List[Any]]) -> str:`
- `def _format_table(self, headers: list[str], rows: list[list[Any]]) -> str:` → `def _format_table(self, headers: List[str], rows: List[List[Any]]) -> str:`
- `def _format_json(self, headers: list[str], rows: list[list[Any]]) -> str:` → `def _format_json(self, headers: List[str], rows: List[List[Any]]) -> str:`
- `def _format_csv(self, headers: list[str], rows: list[list[Any]]) -> str:` → `def _format_csv(self, headers: List[str], rows: List[List[Any]]) -> str:`
- Add `from typing import Any, List` to the top of that example block.

- [ ] **Step 8: Fix the Context Manager example (lines 542-597)**

This example uses `RhapsodyApplication | None` and `RPProject | None` annotations. Replace with `Optional[...]`:
- `self._app: RhapsodyApplication | None = None` → `self._app: Optional[RhapsodyApplication] = None`
- `self._project: RPProject | None = None` → `self._project: Optional[RPProject] = None`
- `def app(self) -> RhapsodyApplication | None:` → `def app(self) -> Optional[RhapsodyApplication]:`
- `def project(self) -> RPProject | None:` → `def project(self) -> Optional[RPProject]:`
- Add `from typing import Optional` to the example imports.

- [ ] **Step 9: Fix the "CLI Integration Tests" example (lines 644-664)**

Replace the Click `CliRunner` example:

```python
def test_project_open_command_end_to_end():
    """Test: 'project open' command works end-to-end."""
    from click.testing import CliRunner
    from rhapsody_cli.cli.commands.project import ProjectCommandGroup

    runner = CliRunner()
    group = ProjectCommandGroup()

    with runner.isolated_filesystem():
        # Create a test project file
        Path("test.rpy").write_text("mock project content")

        # Run command
        result = runner.invoke(group, ["open", "test.rpy"])

        # Assert
        assert result.exit_code == 0
```

with the argparse-style subprocess pattern actually used by the system tests:

```python
def test_project_open_command_end_to_end():
    """Test: 'rhapsody-cli project open' works end-to-end via subprocess."""
    import subprocess
    import sys

    # Create a test project file (mock)
    Path("test.rpy").write_text("mock project content")

    # Run the CLI as a subprocess
    result = subprocess.run(
        [sys.executable, "-m", "rhapsody_cli.cli.main", "project", "open", "test.rpy"],
        capture_output=True,
        text=True,
    )

    # Assert (exact assertions depend on the mocked environment)
    assert result.returncode == 0
```

- [ ] **Step 10: Fix the code-review checklist (lines 745-750)**

Change:

```text
### Specific to CLI Commands
- [ ] Command inherits from `click.Command` or group?
- [ ] Parameters defined in `__init__`?
- [ ] Logic in `execute()` method?
- [ ] Error handling includes `click.Abort`?
- [ ] User-facing messages in `click.echo()`?
```

to:

```text
### Specific to CLI Commands
- [ ] Action inherits from `AbstractAction` (or `RhapsodyContextAction` / `ElementManagementAction`)?
- [ ] Arguments registered in `init_arguments()` via `sub_parser.add_parser(...)`?
- [ ] Logic in `execute(args: argparse.Namespace)` method?
- [ ] Error handling uses `_handle_connection_error` / `_handle_execution_error` and `sys.exit(1)`?
- [ ] User-facing messages use `print(..., file=sys.stderr)` for errors?
```

- [ ] **Step 11: Fix the references (lines 780-783)**

Change:

```text
- **Click Commands:** [Click documentation](https://click.palletsprojects.com)
```

to:

```text
- **argparse:** [argparse documentation](https://docs.python.org/3/library/argparse.html)
```

- [ ] **Step 12: Verify no Click references remain in the guidelines**

Run: `grep -n "click\|Click\|CliRunner" docs/CODE_GUIDELINES.md`
Expected: no matches.

- [ ] **Step 13: Commit**

```bash
git add docs/CODE_GUIDELINES.md
git commit -m "docs: rewrite CODE_GUIDELINES Click examples to argparse and fix type syntax"
```

---

### Task 8: Fix stale Click references in remaining docs (`index.rst`, `installation.rst`, `cli_tools.rst`, `swr_cli_requirements.md`, `contributing.rst`)

These doc files each have a small number of Click references or wrong values that need correcting.

**Files:**
- Modify: `docs/index.rst:66,222-230`
- Modify: `docs/user_guide/installation.rst:36-38,65`
- Modify: `docs/user_guide/cli_tools.rst:7`
- Modify: `docs/requirements/swr_cli_requirements.md:13,17-21,34-36,70,87,103,138,156,173,190,257-267`
- Modify: `docs/contributing.rst:40,76`

**Interfaces:**
- Consumes: the argparse architecture facts.
- Produces: Click-free, accurate user/requirements docs.

- [ ] **Step 1: Fix `docs/index.rst`**

Line 66 — change:

```text
   - Click-based command-line interface
```

to:

```text
   - argparse-based command-line interface
```

Lines 222-230 (the project-structure tree) — replace the `cli/` subtree that shows `commands/project.py` containing `ProjectCommandGroup` with the real structure:

```text
   └── cli/                           # CLI entry point and support
       ├── main.py                   # CLI entry point (re-exports cli.main)
       ├── cli.py                    # main() dispatcher
       ├── context.py                # RhapsodyContext (state management)
       ├── formatters.py             # OutputFormatter (table/JSON/CSV)
       └── logging_config.py         # CliLoggingConfigurator
```

And after the `cli/` block, the `commands/` and `actions/` packages are separate top-level packages under `src/rhapsody_cli/` (not nested under `cli/`). If the tree in `index.rst` does not show them, leave the tree as the corrected `cli/` block above — do not invent structure. (The authoritative structure is in Task 6 Step 8's tree.)

- [ ] **Step 2: Fix `docs/user_guide/installation.rst`**

Lines 36-38 — change:

```text
This adds:

* **click** - CLI framework
* **tabulate** - Table formatting
* **rich** - Rich terminal output
```

to:

```text
This adds:

* **tabulate** - Table formatting
* **rich** - Rich terminal output
```

Line 65 — change:

```text
* CLI tools: click, tabulate, rich
```

to:

```text
* CLI tools: tabulate, rich
```

- [ ] **Step 3: Fix `docs/user_guide/cli_tools.rst`**

Line 7 — change:

```text
rhapsody-cli provides a command-line interface for common Rhapsody operations. The CLI is built using Click and supports multiple output formats.
```

to:

```text
rhapsody-cli provides a command-line interface for common Rhapsody operations. The CLI is built using Python's standard-library argparse and supports multiple output formats.
```

- [ ] **Step 4: Fix `docs/requirements/swr_cli_requirements.md`**

This file describes the CLI as a "Click group" in multiple requirements. Rewrite the Click-specific language to argparse-language:

Line 13 — change:

```text
**Title: cli group is the main Click entry point for the rhapsody-cli tool
```

to:

```text
**Title: main() is the main argparse entry point for the rhapsody-cli tool
```

Lines 17-21 — change:

```text
The `cli` Click group shall be the main entry point for the command-line tool. It shall
provide a `--output` option with choices `table`, `json`, `csv` (default `table`) that
sets the output format on the `RhapsodyContext`. If no context object exists, a new
`RhapsodyContext` shall be created. The group shall register the `project`, `element`,
and `io` command subgroups.
**Implementation:** src/rhapsody_cli/cli/main.py:cli
```

to:

```text
The `main()` function in `src/rhapsody_cli/cli/cli.py` shall be the main entry point for
the command-line tool. It shall read a `--output` option with choices `table`, `json`,
`csv` (default `table`) and set the output format on a `RhapsodyContext`. It shall
dispatch the first positional argument to one of the `AbstractCommand` subclasses:
`ElementCommand`, `ProjectCommand`, or `IOCommand`.
**Implementation:** src/rhapsody_cli/cli/cli.py:main
```

Lines 34-36 — change the `--output` description from "on the `cli` group" / `ctx.obj.output_format` to:

```text
The `--output` option shall accept one of `table`, `json`, or `csv` (default `table`) and
store the selected format string on `ctx.output_format` (where `ctx` is the `RhapsodyContext`).
**Implementation:** src/rhapsody_cli/cli/cli.py:main
```

For the per-command requirements (SWR_CLI_00004 through SWR_CLI_00011), replace each `click.Abort` reference with `sys.exit(1)` and each "execute `XCommand.execute`" with "execute the action's `execute(args)` method". Specifically, in each of those requirement bodies, make these substitutions:
- `raise \`click.Abort\`` → `call \`sys.exit(1)\``
- `echo the error to stderr and raise \`click.Abort\`` → `print the error to stderr and call \`sys.exit(1)\``
- `Exceptions are reported to stderr with \`click.Abort\`` → `Exceptions are reported to stderr via \`sys.exit(1)\``

And update the `**Implementation:**` lines to point at the actual action files:
- SWR_CLI_00004: `src/rhapsody_cli/actions/project_action.py:ProjectOpenAction`
- SWR_CLI_00005: `src/rhapsody_cli/actions/project_action.py:ProjectListAction`
- SWR_CLI_00006: `src/rhapsody_cli/actions/project_action.py:ProjectCloseAction`
- SWR_CLI_00007: `src/rhapsody_cli/actions/element_action.py:ElementAddAction`
- SWR_CLI_00008: `src/rhapsody_cli/actions/element_action.py:ElementViewAction`
- SWR_CLI_00009: `src/rhapsody_cli/actions/element_action.py:ElementQueryAction`
- SWR_CLI_00010: `src/rhapsody_cli/actions/io_action.py:IOImportAction`
- SWR_CLI_00011: `src/rhapsody_cli/actions/io_action.py:IOExportAction`

(Verified class names: `ProjectOpenAction`, `ProjectListAction`, `ProjectCloseAction`, `ProjectNewAction` in `project_action.py`; `IOImportAction`, `IOExportAction` in `io_action.py`; `ElementAddAction`, `ElementViewAction`, `ElementQueryAction`, `ElementDeleteAction` in `element_action.py`.)

Lines 257-267 (SWR_CLI_00016, the class-based architecture requirement) — change:

```text
**Title: CLI commands use a class-based Click command architecture
...
Each CLI command shall be implemented as a class extending `click.Command` (or a
project/element/io-specific base like `BaseProjectCommand`, `BaseElementCommand`,
`BaseIOCommand`). The command's `__init__` shall configure name, help, callback
(`self.execute`), and params. Commands shall be grouped under a `click.Group` subclass
(`ProjectCommandGroup`, `ElementCommandGroup`, `IOCommandGroup`) that registers the
commands in its own `__init__`.
**Implementation:** src/rhapsody_cli/cli/commands/project.py:BaseProjectCommand
```

to:

```text
**Title: CLI uses a class-based argparse command/action architecture
...
Each CLI subcommand shall be implemented as a class extending `AbstractAction` (or a
specialized base like `RhapsodyContextAction`, `ElementManagementAction`). Each action
registers its own argparse subparser in `init_arguments()` and owns its execution in
`execute(args)`. Actions shall be grouped under an `AbstractCommand` subclass
(`ElementCommand`, `ProjectCommand`, `IOCommand`) that returns its actions from
`get_actions()`.
**Implementation:** src/rhapsody_cli/actions/abstract_action.py:AbstractAction
```

- [ ] **Step 5: Fix `docs/contributing.rst`**

Line 40 — change:

```text
* Maximum line length: 100 characters
```

to:

```text
* Maximum line length: 200 characters
```

Line 76 — change:

```text
   pytest tests/test_application.py
```

to:

```text
   pytest tests/unit/test_application.py
```

- [ ] **Step 6: Verify no Click references remain in active docs**

Run: `grep -rn "click\|Click\|CliRunner" docs/ .github/`
Expected: no matches except inside `docs/superpowers/plans/` (historical plan docs — intentionally left unchanged). If any active doc still matches, fix it.

- [ ] **Step 7: Commit**

```bash
git add docs/index.rst docs/user_guide/installation.rst docs/user_guide/cli_tools.rst docs/requirements/swr_cli_requirements.md docs/contributing.rst
git commit -m "docs: replace stale Click references with argparse across user/requirements docs"
```

---

### Task 9: Update `CLAUDE.md` to remove the now-inaccurate "stale docs" note

The `CLAUDE.md` created earlier contains a "Note on Stale Documentation" section flagging that `.github/copilot-instructions.md` is outdated and that `from __future__ import annotations` is used inconsistently. After Tasks 3-8, both issues are resolved, so that section is itself now stale.

**Files:**
- Modify: `CLAUDE.md` (the "Note on Stale Documentation" section near the end)

**Interfaces:**
- Consumes: the corrected state from Tasks 3-8.
- Produces: an accurate `CLAUDE.md`.

- [ ] **Step 1: Read the current `CLAUDE.md` "Note on Stale Documentation" section**

Run: read the end of `CLAUDE.md` to locate the section (search for "Note on Stale Documentation").

- [ ] **Step 2: Replace the section**

Replace the entire "## Note on Stale Documentation" section (the heading and its two paragraphs about copilot-instructions.md and the future-import discrepancy) with:

```markdown
## Documentation Status

All developer documentation (`.github/copilot-instructions.md`, `docs/CODE_GUIDELINES.md`, and the user/requirements `.rst`/`.md` files) has been updated to reflect the argparse-based CLI architecture. Historical plan docs under `docs/superpowers/plans/` are dated records and are intentionally not updated.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md to reflect corrected documentation state"
```

---

### Task 10: Final verification

Run the complete quality gate and confirm everything passes after all prior tasks.

**Files:**
- None modified (verification only).

- [ ] **Step 1: Confirm no forbidden import remains in code**

Run: `grep -rn "from __future__ import annotations" src/ tests/`
Expected: no matches. (Matches inside `docs/superpowers/plans/` and `CLAUDE.md`'s discussion are acceptable and not in scope.)

- [ ] **Step 2: Confirm no Click references remain in active code or docs**

Run: `grep -rn "import click\|click\.\|@click\|CliRunner" src/ tests/ docs/ .github/`
Expected: no matches in `src/`, `tests/`, or active `docs/` and `.github/` files. (Historical `docs/superpowers/plans/` files may match — those are out of scope.)

- [ ] **Step 3: Run all quality gates**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: all clean, no errors.

- [ ] **Step 4: Run the full test suite**

Run: `pytest -q`
Expected: `260 passed, 2 skipped, 0 failed` (the 2 integration tests skip because no Rhapsody is running).

- [ ] **Step 5: Confirm the CLI entry point still works**

Run: `python -c "import rhapsody_cli; print('import OK')"` and `python -m rhapsody_cli.cli.main -h`
Expected: import OK; help message printed (exit code 0).

- [ ] **Step 6: Confirm a subcommand help still parses**

Run: `python -m rhapsody_cli.cli.main element --help`
Expected: element subcommand help printed (argparse help, exit code 0).

- [ ] **Step 7: Final commit (if any verification step surfaced a fix)**

If any step above surfaced an issue that required a fix, commit it:

```bash
git add -A
git commit -m "fix: address final verification findings"
```

Otherwise, no commit needed — the work is complete.
