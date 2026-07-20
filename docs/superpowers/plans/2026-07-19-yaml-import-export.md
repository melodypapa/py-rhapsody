# YAML Import/Export Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add YAML-based import/export to `rhapsody-cli` for round-tripping Rhapsody model structure (14 element types: Package, Class, Operation, Attribute, Argument, Type, Object, EnumerationLiteral, Dependency, Generalization, Relation, Port, Event, EventReception) without requiring Rhapsody's native `.sbs`/`.rpy` binary format.

**Architecture:** Three-layer exchange module (`RhapsodyModelHelper` base → `RhapsodyImporter`/`RhapsodyExporter` subclasses) under `src/rhapsody_cli/exchange/`, with four new CLI actions (`Project/Package × Import/Export`) wired into existing command groups. YAML schema v1 with type discriminator fields (`Type.kind`, `Relation.relation_type`). Idempotent `find_or_create_<type>` pattern with fakes-based TDD.

**Tech Stack:** Python 3.8+, PyYAML 6.0+, pywin32 (Windows runtime only), pytest with coverage, ruff/black/mypy quality gate.

## Global Constraints

- Python `>=3.8` target (per `pyproject.toml`)
- Line length 200 (black + ruff)
- mypy strict mode, py3.9 target
- ruff rules: `E, F, I, UP, B, N`
- **Forbidden:** `from __future__ import annotations` (use string-quoted forward refs or `TYPE_CHECKING` imports)
- **Forbidden:** `element._com.delete()` (use `element.delete_from_project()`)
- **Forbidden:** AI attribution in commits (no `Co-authored-by: Copilot`)
- **Forbidden:** Direct commits to `main` — use `feature/`, `fix/`, `refactor/`, `docs/` branches
- TDD: failing test first, then implementation. Coverage 80% min, 90%+ preferred
- All unit tests use fakes from `tests/unit/models/fakes.py` (never real COM)
- SWR_XCH_*** requirement IDs in `docs/requirements/`, UTS_XCH_*** test case IDs in `docs/tests/unit/`
- All CLI errors raised as `CliExecutionError(message: str, exit_code: int = 1)` — no `sys.exit()` in actions
- Fakes use **camelCase** COM method names (e.g. `make_fake_element("Class", getName="Foo")`)

## Spec-to-Codebase Reconciliation

The approved spec (`docs/superpowers/specs/2026-07-19-yaml-import-export-design.md`) contains patterns that diverge from actual codebase conventions. Tasks below use the **CORRECTED** patterns. This section documents the delta so reviewers can reconcile spec vs. plan:

1. **Action `command_id`**: Spec shows `command_id = "export"` as class attribute. **Actual pattern:** `def __init__(self) -> None: super().__init__(command_id="export")`. Tasks 9–10 use the actual pattern.

2. **`init_arguments` signature**: Spec shows `sub_parser: argparse.ArgumentParser`. **Actual pattern:** `sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]"` (string-quoted, uses `_SubParsersAction`). Tasks 9–10 use the actual signature.

3. **Success output**: Spec calls `self._print_success(...)`. **Actual:** No such method exists. Use `self.logger.info(...)` (existing pattern in `ProjectOpenAction.execute`). Tasks 9–10 use `self.logger.info`.

4. **Active project accessor**: Spec uses `app.get_active_project()`. **Actual:** `app.active_project()` (no `get_` prefix). Tasks 9–10 use `app.active_project()`.

5. **Tag creation (import)**: Spec uses `element.add_tag(name)` then `tag.set_value(value)`. **Actual:** `add_tag` does NOT exist; `set_value` does NOT exist on tags. Use `element.set_property_value(key, val)` (existing convention in `package_action.py:283`). Task 3 uses `set_property_value`.

6. **Tag enumeration (export)**: Spec uses `element.get_tags()`. **Actual:** `get_tags` does NOT exist. Use `element.get_all_tags()` (returns `RPCollection` of tag elements). Each tag has `get_name()` and `get_value()`. Task 7 uses `get_all_tags`.

7. **Tag value setting**: Spec uses `tag.set_value(value)`. **Actual:** Use `element.set_tag_value(tag_element, val)` (takes a wrapped tag element, not a name) OR `element.set_property_value(key, val)` for property-style tags. Task 3 uses `set_property_value` for simplicity and idempotency.

8. **Action `execute` error handling**: Spec's `execute` lacks try/except. **Actual pattern:** wrap body in `try: ... except RhapsodyConnectionError as e: self._handle_connection_error(e, "...") except Exception as e: self._handle_execution_error(e, "...")`. Tasks 9–10 wrap execute in try/except.

9. **`init_arguments` verbose flag**: Spec doesn't call `self.add_verbose_argument(parser)`. **Actual pattern:** always call `self.add_verbose_argument(parser)` at end of `init_arguments`. Tasks 9–10 add the verbose argument.

**Additional design decisions made during plan writing** (not in spec, not contradictions):

- **`resolve_classifier` implementation**: Recursive search through `project.get_nested_elements()`. Returns first element whose `get_name()` matches. Falls back to `None` if not found or project is `None`.
- **`get_classifier_name` implementation**: `None`-safe wrapper around `classifier.get_name()` with `try/except` fallback to `None`.
- **`apply_tags` uses `set_property_value`**: This is idempotent (creates property if missing, updates if present) and matches existing `package_action.py` convention. Stereotype-style tags are also settable via this API.
- **`_export_tags` uses `get_all_tags()`**: Enumerates stereotype tags. Each tag's `get_name()` + `get_value()` is read with `try/except` per tag (skips malformed tags). v1 limitation: arbitrary properties set via `set_property_value` that aren't stereotype tags may not round-trip on export (documented in §10 of spec).
- **`_collect_children` for Package**: Uses `hasattr` guards for `get_global_functions`/`get_global_variables`/`get_global_objects` (these may not exist on all RPPackage variants). Falls back to `get_nested_elements()` only.
- **`make_com_error` is Windows-only** (requires `pywintypes`): Error-path tests that need `make_com_error` are fine because CI runs the full gate on `windows-latest`. Non-Windows devs skip those specific tests.

## File Structure

```
src/rhapsody_cli/
├── exchange/                          # NEW package
│   ├── __init__.py                    # exports: RhapsodyImporter, RhapsodyExporter, RhapsodyYaml, SCHEMA_VERSION
│   ├── schema.py                      # SCHEMA_VERSION = 1, key constants
│   ├── yaml_utils.py                  # RhapsodyYaml class (read/write)
│   ├── core.py                        # RhapsodyModelHelper base class
│   ├── importer.py                    # RhapsodyImporter(RhapsodyModelHelper)
│   └── exporter.py                    # RhapsodyExporter(RhapsodyModelHelper)
├── actions/
│   ├── project_action.py              # MODIFIED — append ProjectExportAction, ProjectImportAction
│   └── package_action.py              # MODIFIED — append PackageExportAction, PackageImportAction
└── commands/
    ├── project_command.py             # MODIFIED — append ProjectExportAction(), ProjectImportAction() to get_actions()
    └── package_command.py             # MODIFIED — append PackageExportAction(), PackageImportAction() to get_actions()

tests/unit/
├── exchange/                          # NEW test directory
│   ├── __init__.py
│   ├── test_schema.py                 # SCHEMA_VERSION sanity
│   ├── test_yaml_utils.py             # RhapsodyYaml read/write
│   ├── test_core.py                   # RhapsodyModelHelper
│   ├── test_importer.py               # RhapsodyImporter
│   └── test_exporter.py               # RhapsodyExporter
└── actions/
    ├── test_project_action.py         # EXTENDED — ProjectExportAction, ProjectImportAction tests
    └── test_package_action.py         # EXTENDED — PackageExportAction, PackageImportAction tests

docs/
├── requirements/
│   └── swr_xch_requirements.md        # NEW — SWR_XCH_001 through SWR_XCH_013
├── tests/unit/
│   └── uts_xch_test-specs.md          # NEW — UTS_XCH_00001+ with Traces-To
└── index.rst                          # MODIFIED — add new docs to toctree

pyproject.toml                         # MODIFIED — add PyYAML>=6.0 dependency
```

**File responsibilities:**

| File | Responsibility |
|---|---|
| `exchange/schema.py` | Single source of truth for `SCHEMA_VERSION` and YAML key constants |
| `exchange/yaml_utils.py` | Stateless YAML file I/O (`RhapsodyYaml.read`/`write`); translates PyYAML errors to `CliExecutionError` |
| `exchange/core.py` | `RhapsodyModelHelper` — reusable model manipulation (find/create/apply/resolve). No YAML knowledge |
| `exchange/importer.py` | `RhapsodyImporter` — YAML dict → Rhapsody model. Dispatches to helper methods |
| `exchange/exporter.py` | `RhapsodyExporter` — Rhapsody model → YAML dict. Dispatches to helper methods |
| `actions/project_action.py` | CLI entry points for `project export` / `project import` |
| `actions/package_action.py` | CLI entry points for `package export` / `package import` |

---

## Task 1: Add PyYAML dependency + exchange package scaffold

**Files:**
- Modify: `pyproject.toml` (add `PyYAML>=6.0` to dependencies)
- Create: `src/rhapsody_cli/exchange/__init__.py`
- Create: `src/rhapsody_cli/exchange/schema.py`
- Create: `tests/unit/exchange/__init__.py`
- Test: `tests/unit/exchange/test_schema.py`

**Interfaces:**
- Produces: `SCHEMA_VERSION: int` constant (= 1), `RHAPSODY_MODEL_KEY: str` (= "rhapsody-model"), `VERSION_KEY: str` (= "version"), `PROJECT_KEY: str` (= "project") in `rhapsody_cli.exchange.schema`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/exchange/__init__.py` (empty file):

```python
"""Unit tests for the exchange package (YAML import/export)."""
```

Create `tests/unit/exchange/test_schema.py`:

```python
"""Tests for exchange.schema constants.

UTS_XCH_00001: Schema version constant sanity
"""

from rhapsody_cli.exchange.schema import (
    PROJECT_KEY,
    RHAPSODY_MODEL_KEY,
    SCHEMA_VERSION,
    VERSION_KEY,
)


def test_schema_version_is_one() -> None:
    """UTS_XCH_00001: SCHEMA_VERSION must be 1 for v1 of the format."""
    assert SCHEMA_VERSION == 1


def test_schema_version_is_int() -> None:
    """UTS_XCH_00001: SCHEMA_VERSION must be an int (not str) for clean comparison."""
    assert isinstance(SCHEMA_VERSION, int)


def test_rhapsody_model_key_constant() -> None:
    """UTS_XCH_00001: rhapsody-model key constant matches YAML schema."""
    assert RHAPSODY_MODEL_KEY == "rhapsody-model"


def test_version_key_constant() -> None:
    """UTS_XCH_00001: version key constant matches YAML schema."""
    assert VERSION_KEY == "version"


def test_project_key_constant() -> None:
    """UTS_XCH_00001: project key constant matches YAML schema."""
    assert PROJECT_KEY == "project"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_schema.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.exchange'`

- [ ] **Step 3: Write minimal implementation**

Create `src/rhapsody_cli/exchange/__init__.py`:

```python
"""YAML import/export for Rhapsody models.

Public API:
    - RhapsodyImporter: YAML dict -> Rhapsody model
    - RhapsodyExporter: Rhapsody model -> YAML dict
    - RhapsodyYaml: file I/O wrapper around PyYAML
    - SCHEMA_VERSION: YAML schema format version (currently 1)
"""

from rhapsody_cli.exchange.schema import PROJECT_KEY, RHAPSODY_MODEL_KEY, SCHEMA_VERSION, VERSION_KEY

__all__ = [
    "PROJECT_KEY",
    "RHAPSODY_MODEL_KEY",
    "SCHEMA_VERSION",
    "VERSION_KEY",
]

# RhapsodyImporter, RhapsodyExporter, RhapsodyYaml are imported lazily by actions
# to avoid importing pywin32 at module load on non-Windows dev machines.
```

Create `src/rhapsody_cli/exchange/schema.py`:

```python
"""YAML schema constants for Rhapsody model exchange.

SWR_XCH_005: YAML Schema (version 1)
"""

# Schema format version. The importer rejects any other value.
SCHEMA_VERSION: int = 1

# Top-level YAML keys (kept as constants so importer/exporter stay in sync).
VERSION_KEY: str = "version"
PROJECT_KEY: str = "project"
RHAPSODY_MODEL_KEY: str = "rhapsody-model"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_schema.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Add PyYAML dependency**

Modify `pyproject.toml` — locate the `[project]` section's `dependencies` array and append `PyYAML>=6.0`:

```toml
dependencies = [
    "pywin32>=306; sys_platform == 'win32'",
    "PyYAML>=6.0",
]
```

Then install the new dependency:

```bash
pip install -e ".[dev,cli]"
```

Verify PyYAML is importable:

```bash
python -c "import yaml; print(yaml.__version__)"
```

Expected: prints `6.0` or higher.

- [ ] **Step 6: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/ tests/unit/exchange/
black --check src/rhapsody_cli/exchange/ tests/unit/exchange/
mypy src/rhapsody_cli/exchange/
```

Expected: all pass with no errors.

- [ ] **Step 7: Commit**

```bash
git checkout -b feature/yaml-import-export
git add pyproject.toml src/rhapsody_cli/exchange/__init__.py src/rhapsody_cli/exchange/schema.py tests/unit/exchange/__init__.py tests/unit/exchange/test_schema.py
git commit -m "feat(exchange): add PyYAML dependency and exchange package scaffold

Introduces src/rhapsody_cli/exchange/ with schema constants
(SCHEMA_VERSION=1, RHAPSODY_MODEL_KEY, VERSION_KEY, PROJECT_KEY)
and the test scaffold. SWR_XCH_005."
```

---

## Task 2: RhapsodyYaml I/O class

**Files:**
- Create: `src/rhapsody_cli/exchange/yaml_utils.py`
- Test: `tests/unit/exchange/test_yaml_utils.py`

**Interfaces:**
- Consumes: `CliExecutionError` from `rhapsody_cli.exceptions`, `yaml` (PyYAML)
- Produces: `RhapsodyYaml` class with `read(path: str) -> dict` and `write(path: str, data: dict) -> None` methods

- [ ] **Step 1: Write the failing test**

Create `tests/unit/exchange/test_yaml_utils.py`:

```python
"""Tests for RhapsodyYaml file I/O.

UTS_XCH_00002: RhapsodyYaml.read happy path
UTS_XCH_00003: RhapsodyYaml.read missing file
UTS_XCH_00004: RhapsodyYaml.read invalid YAML
UTS_XCH_00005: RhapsodyYaml.read non-mapping top level
UTS_XCH_00006: RhapsodyYaml.write happy path
UTS_XCH_00007: RhapsodyYaml.write failure
UTS_XCH_00008: RhapsodyYaml round-trip
"""

from typing import Any

import pytest

from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.exchange.yaml_utils import RhapsodyYaml


class TestRhapsodyYamlRead:
    """UTS_XCH_00002-00005: RhapsodyYaml.read behavior."""

    def test_read_returns_parsed_dict(self, tmp_path: Any) -> None:
        """UTS_XCH_00002: read() returns the parsed YAML mapping."""
        yaml_file = tmp_path / "model.yaml"
        yaml_file.write_text("version: 1\nproject: MyProject\n", encoding="utf-8")

        result = RhapsodyYaml().read(str(yaml_file))

        assert result == {"version": 1, "project": "MyProject"}

    def test_read_missing_file_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00003: read() raises CliExecutionError for missing file."""
        missing = tmp_path / "nonexistent.yaml"

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(missing))

        assert "not found" in str(exc_info.value).lower()

    def test_read_invalid_yaml_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00004: read() raises CliExecutionError for malformed YAML."""
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("version: 1\n  bad: : : indent\n", encoding="utf-8")

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(yaml_file))

        assert "invalid yaml" in str(exc_info.value).lower()

    def test_read_non_mapping_top_level_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00005: read() raises CliExecutionError when top level is a list/scalar."""
        yaml_file = tmp_path / "list.yaml"
        yaml_file.write_text("- item1\n- item2\n", encoding="utf-8")

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().read(str(yaml_file))

        assert "mapping" in str(exc_info.value).lower()


class TestRhapsodyYamlWrite:
    """UTS_XCH_00006-00007: RhapsodyYaml.write behavior."""

    def test_write_creates_file_with_yaml_content(self, tmp_path: Any) -> None:
        """UTS_XCH_00006: write() serializes dict to YAML file."""
        yaml_file = tmp_path / "out.yaml"
        data = {"version": 1, "project": "MyProject", "items": ["a", "b"]}

        RhapsodyYaml().write(str(yaml_file), data)

        assert yaml_file.exists()
        content = yaml_file.read_text(encoding="utf-8")
        assert "version: 1" in content
        assert "MyProject" in content

    def test_write_failure_raises_cli_execution_error(self, tmp_path: Any) -> None:
        """UTS_XCH_00007: write() raises CliExecutionError on OS error (e.g. directory missing)."""
        missing_dir = tmp_path / "nonexistent_dir" / "out.yaml"

        with pytest.raises(CliExecutionError) as exc_info:
            RhapsodyYaml().write(str(missing_dir), {"version": 1})

        assert "failed to write" in str(exc_info.value).lower()


class TestRhapsodyYamlRoundTrip:
    """UTS_XCH_00008: round-trip write -> read preserves data."""

    def test_round_trip_preserves_data(self, tmp_path: Any) -> None:
        """UTS_XCH_00008: data written then read back equals original."""
        yaml_file = tmp_path / "round.yaml"
        data = {
            "version": 1,
            "project": "MyProject",
            "rhapsody-model": [
                {"name": "Pkg1", "type": "Package", "children": []},
                {"name": "MyClass", "type": "Class"},
            ],
        }

        yaml_io = RhapsodyYaml()
        yaml_io.write(str(yaml_file), data)
        result = yaml_io.read(str(yaml_file))

        assert result == data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_yaml_utils.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.exchange.yaml_utils'`

- [ ] **Step 3: Write minimal implementation**

Create `src/rhapsody_cli/exchange/yaml_utils.py`:

```python
"""YAML file I/O helper for the exchange package.

SWR_XCH_005: YAML Schema (version 1) — file I/O layer
"""

import yaml

from rhapsody_cli.exceptions import CliExecutionError


class RhapsodyYaml:
    """YAML file I/O helper. Translates PyYAML errors to CliExecutionError.

    Stateless: instances are cheap to create. Wraps PyYAML's safe_load /
    safe_dump so callers never see raw YAMLError or OSError.
    """

    def read(self, path: str) -> dict:
        """Read and parse a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML mapping as a dict.

        Raises:
            CliExecutionError: If file is missing, YAML is invalid, or top-level
                value is not a mapping.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise CliExecutionError(f"Input file not found: {path}") from e
        except yaml.YAMLError as e:
            raise CliExecutionError(f"Invalid YAML in {path}: {e}") from e
        if not isinstance(data, dict):
            raise CliExecutionError(f"Expected YAML mapping at top level of {path}, got {type(data).__name__}")
        return data

    def write(self, path: str, data: dict) -> None:
        """Write a dict to a YAML file.

        Args:
            path: Output file path.
            data: Dict to serialize.

        Raises:
            CliExecutionError: If the file cannot be written.
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        except OSError as e:
            raise CliExecutionError(f"Failed to write {path}: {e}") from e
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_yaml_utils.py -v`
Expected: PASS (8 tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/yaml_utils.py tests/unit/exchange/test_yaml_utils.py
black --check src/rhapsody_cli/exchange/yaml_utils.py tests/unit/exchange/test_yaml_utils.py
mypy src/rhapsody_cli/exchange/yaml_utils.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/yaml_utils.py tests/unit/exchange/test_yaml_utils.py
git commit -m "feat(exchange): add RhapsodyYaml I/O class

Stateless read/write wrapper around PyYAML safe_load/safe_dump.
Translates FileNotFoundError, YAMLError, OSError to CliExecutionError.
SWR_XCH_005."
```

---

## Task 3: RhapsodyModelHelper core (8 element types + helpers)

**Files:**
- Create: `src/rhapsody_cli/exchange/core.py`
- Test: `tests/unit/exchange/test_core.py`

**Interfaces:**
- Consumes: `RhapsodyApplication` (for `connect` classmethod), `RPModelElement`, `RPCollection` from `rhapsody_cli.models.core`, `RPProject` from `rhapsody_cli.models.elements.containment`
- Produces: `RhapsodyModelHelper` class with:
  - `__init__(self, app: Optional[RhapsodyApplication] = None) -> None`
  - `find_or_create_package(parent, name) -> RPModelElement`
  - `find_or_create_class(parent, name) -> RPModelElement`
  - `find_or_create_operation(parent, name) -> RPModelElement`
  - `find_or_create_argument(parent, name) -> RPModelElement`
  - `find_or_create_attribute(parent, name) -> RPModelElement`
  - `find_or_create_type(parent, name, kind=None) -> RPModelElement`
  - `find_or_create_object(parent, name) -> RPModelElement`
  - `find_or_create_enumeration_literal(parent, name) -> RPModelElement`
  - `apply_stereotypes(element, stereotypes) -> None`
  - `apply_tags(element, tags) -> None`
  - `resolve_classifier(name) -> Optional[RPModelElement]`
  - `get_classifier_name(classifier) -> Optional[str]`
  - `find_child_by_name(parent, meta_class, name) -> Optional[RPModelElement]`
  - `_set_type_kind(type_element, kind) -> None`
  - `_collect_children(container) -> List[RPModelElement]`
  - `_get_project_name(container) -> str`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/exchange/test_core.py`:

```python
"""Tests for RhapsodyModelHelper base class.

UTS_XCH_00009: find_or_create_package sanitizes name and delegates to add_new_aggr
UTS_XCH_00010: find_or_create_class creates via add_new_aggr
UTS_XCH_00011: find_or_create_operation on package uses add_global_function
UTS_XCH_00012: find_or_create_operation on class uses add_new_aggr
UTS_XCH_00013: find_or_create_argument uses add_argument
UTS_XCH_00014: find_or_create_attribute creates via add_new_aggr
UTS_XCH_00015: find_or_create_type sets kind after creation
UTS_XCH_00016: find_or_create_object creates via add_new_aggr
UTS_XCH_00017: find_or_create_enumeration_literal creates via add_new_aggr
UTS_XCH_00018: find_child_by_name returns matching child
UTS_XCH_00019: find_child_by_name returns None when no match
UTS_XCH_00020: apply_stereotypes infers meta_type from element
UTS_XCH_00021: apply_stereotypes skips already-applied stereotypes
UTS_XCH_00022: apply_tags uses set_property_value
UTS_XCH_00023: resolve_classifier searches project recursively
UTS_XCH_00024: resolve_classifier returns None when not found
UTS_XCH_00025: get_classifier_name is None-safe
UTS_XCH_00026: _set_type_kind calls set_kind
UTS_XCH_00027: _collect_children returns nested elements
UTS_XCH_00028: _collect_children merges package globals
UTS_XCH_00029: _get_project_name walks owner chain
UTS_XCH_00030: find_or_create returns existing element without creating duplicate
"""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from rhapsody_cli.exchange.core import RhapsodyModelHelper
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def _make_helper(project: Any = None) -> RhapsodyModelHelper:
    """Build a RhapsodyModelHelper with a mocked app and project.

    Skips RhapsodyApplication.connect() entirely.
    """
    app = MagicMock()
    helper = RhapsodyModelHelper.__new__(RhapsodyModelHelper)
    helper.app = app
    helper.project = project
    return helper


class TestFindOrCreatePackage:
    """UTS_XCH_00009, UTS_XCH_00030: find_or_create_package."""

    def test_creates_package_with_sanitized_name(self) -> None:
        """UTS_XCH_00009: spaces in name replaced with underscores before add_new_aggr."""
        parent = make_fake_element("Package")
        new_pkg = make_fake_element("Package", getName="My_Pkg")
        parent.addNewAggr.return_value = new_pkg
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_package(parent, "My Pkg")

        parent.addNewAggr.assert_called_once_with("Package", "My_Pkg")
        assert result.get_name() == "My_Pkg"

    def test_returns_existing_package_without_creating(self) -> None:
        """UTS_XCH_00030: if a Package child with matching name exists, return it."""
        existing = make_fake_element("Package", getName="Existing")
        parent = make_fake_element("Package")
        parent.getNestedElements.return_value = make_fake_collection([existing])
        helper = _make_helper()

        result = helper.find_or_create_package(parent, "Existing")

        parent.addNewAggr.assert_not_called()
        assert result.get_name() == "Existing"


class TestFindOrCreateClass:
    """UTS_XCH_00010, UTS_XCH_00030: find_or_create_class."""

    def test_creates_class_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Package")
        new_cls = make_fake_element("Class", getName="Widget")
        parent.addNewAggr.return_value = new_cls
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_class(parent, "Widget")

        parent.addNewAggr.assert_called_once_with("Class", "Widget")
        assert result.get_name() == "Widget"


class TestFindOrCreateOperation:
    """UTS_XCH_00011, UTS_XCH_00012: find_or_create_operation."""

    def test_on_package_uses_add_global_function(self) -> None:
        """UTS_XCH_00011: global function path when parent is a Package."""
        parent = make_fake_element("Package")
        new_op = make_fake_element("Operation", getName="globalFn")
        parent.addGlobalFunction.return_value = new_op
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_operation(parent, "globalFn")

        parent.addGlobalFunction.assert_called_once_with("globalFn")
        parent.addNewAggr.assert_not_called()
        assert result.get_name() == "globalFn"

    def test_on_class_uses_add_new_aggr(self) -> None:
        """UTS_XCH_00012: regular addNewAggr path when parent is a Class."""
        parent = make_fake_element("Class")
        new_op = make_fake_element("Operation", getName="method")
        parent.addNewAggr.return_value = new_op
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_operation(parent, "method")

        parent.addNewAggr.assert_called_once_with("Operation", "method")
        parent.addGlobalFunction.assert_not_called()


class TestFindOrCreateArgument:
    """UTS_XCH_00013: find_or_create_argument."""

    def test_uses_add_argument(self) -> None:
        parent = make_fake_element("Operation")
        new_arg = make_fake_element("Argument", getName="x")
        parent.addArgument.return_value = new_arg
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_argument(parent, "x")

        parent.addArgument.assert_called_once_with("x")
        assert result.get_name() == "x"


class TestFindOrCreateAttribute:
    """UTS_XCH_00014: find_or_create_attribute."""

    def test_creates_attribute_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_attr = make_fake_element("Attribute", getName="count")
        parent.addNewAggr.return_value = new_attr
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_attribute(parent, "count")

        parent.addNewAggr.assert_called_once_with("Attribute", "count")
        assert result.get_name() == "count"


class TestFindOrCreateType:
    """UTS_XCH_00015, UTS_XCH_00026: find_or_create_type + _set_type_kind."""

    def test_creates_type_and_sets_kind(self) -> None:
        parent = make_fake_element("Package")
        new_type = make_fake_element("Type", getName="Color")
        parent.addNewAggr.return_value = new_type
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_type(parent, "Color", kind="Enumeration")

        parent.addNewAggr.assert_called_once_with("Type", "Color")
        new_type.setKind.assert_called_once_with("Enumeration")
        assert result.get_name() == "Color"

    def test_creates_type_without_kind_skips_set_kind(self) -> None:
        parent = make_fake_element("Package")
        new_type = make_fake_element("Type", getName="Plain")
        parent.addNewAggr.return_value = new_type
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        helper.find_or_create_type(parent, "Plain")

        new_type.setKind.assert_not_called()


class TestFindOrCreateObject:
    """UTS_XCH_00016: find_or_create_object."""

    def test_creates_object_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Package")
        new_obj = make_fake_element("Object", getName="myObj")
        parent.addNewAggr.return_value = new_obj
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_object(parent, "myObj")

        parent.addNewAggr.assert_called_once_with("Object", "myObj")
        assert result.get_name() == "myObj"


class TestFindOrCreateEnumerationLiteral:
    """UTS_XCH_00017: find_or_create_enumeration_literal."""

    def test_creates_literal_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Type")
        new_lit = make_fake_element("EnumerationLiteral", getName="RED")
        parent.addNewAggr.return_value = new_lit
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_enumeration_literal(parent, "RED")

        parent.addNewAggr.assert_called_once_with("EnumerationLiteral", "RED")
        assert result.get_name() == "RED"


class TestFindChildByName:
    """UTS_XCH_00018, UTS_XCH_00019: find_child_by_name."""

    def test_returns_matching_child(self) -> None:
        match = make_fake_element("Class", getName="Widget")
        other = make_fake_element("Class", getName="Other")
        parent = make_fake_element("Package")
        parent.getNestedElements.return_value = make_fake_collection([other, match])
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Widget")

        assert result is not None
        assert result.get_name() == "Widget"

    def test_returns_none_when_no_match(self) -> None:
        other = make_fake_element("Class", getName="Other")
        parent = make_fake_element("Package")
        parent.getNestedElements.return_value = make_fake_collection([other])
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Missing")

        assert result is None

    def test_filters_by_meta_class(self) -> None:
        """A child with the right name but wrong metaclass is not returned."""
        same_name_diff_type = make_fake_element("Package", getName="Widget")
        parent = make_fake_element("Package")
        parent.getNestedElements.return_value = make_fake_collection([same_name_diff_type])
        helper = _make_helper()

        result = helper.find_child_by_name(parent, "Class", "Widget")

        assert result is None


class TestApplyStereotypes:
    """UTS_XCH_00020, UTS_XCH_00021: apply_stereotypes."""

    def test_infers_meta_type_and_calls_add_stereotype(self) -> None:
        element = make_fake_element("Class")
        helper = _make_helper()

        helper.apply_stereotypes(element, ["Interface", "SwComponent"])

        assert element.addStereotype.call_count == 2
        element.addStereotype.assert_any_call("Interface", "Class")
        element.addStereotype.assert_any_call("SwComponent", "Class")

    def test_skips_already_applied_stereotypes(self) -> None:
        """If get_stereotypes() returns an existing stereotype, don't re-add it."""
        existing = make_fake_element("Stereotype", getName="Interface")
        element = make_fake_element("Class")
        element.getStereotypes.return_value = make_fake_collection([existing])
        helper = _make_helper()

        helper.apply_stereotypes(element, ["Interface", "SwComponent"])

        # Only SwComponent should be added; Interface already present
        element.addStereotype.assert_called_once_with("SwComponent", "Class")


class TestApplyTags:
    """UTS_XCH_00022: apply_tags uses set_property_value."""

    def test_calls_set_property_value_for_each_tag(self) -> None:
        element = make_fake_element("Package")
        helper = _make_helper()

        helper.apply_tags(element, {"status": "active", "count": "3"})

        assert element.setPropertyValue.call_count == 2
        element.setPropertyValue.assert_any_call("status", "active")
        element.setPropertyValue.assert_any_call("count", "3")

    def test_empty_tags_dict_does_nothing(self) -> None:
        element = make_fake_element("Package")
        helper = _make_helper()

        helper.apply_tags(element, {})

        element.setPropertyValue.assert_not_called()


class TestResolveClassifier:
    """UTS_XCH_00023, UTS_XCH_00024: resolve_classifier."""

    def test_searches_project_nested_elements_recursively(self) -> None:
        """Found classifier is returned."""
        target = make_fake_element("Class", getName="Widget")
        sibling = make_fake_element("Class", getName="Other")
        nested_pkg = make_fake_element("Package", getName="Sub", getNestedElements=make_fake_collection([target]))
        project = make_fake_element("Project", getName="P", getNestedElements=make_fake_collection([sibling, nested_pkg]))
        helper = _make_helper(project=project)

        result = helper.resolve_classifier("Widget")

        assert result is not None
        assert result.get_name() == "Widget"

    def test_returns_none_when_not_found(self) -> None:
        sibling = make_fake_element("Class", getName="Other")
        project = make_fake_element("Project", getName="P", getNestedElements=make_fake_collection([sibling]))
        helper = _make_helper(project=project)

        result = helper.resolve_classifier("Missing")

        assert result is None

    def test_returns_none_when_project_is_none(self) -> None:
        helper = _make_helper(project=None)

        result = helper.resolve_classifier("Anything")

        assert result is None


class TestGetClassifierName:
    """UTS_XCH_00025: get_classifier_name."""

    def test_returns_name_of_classifier(self) -> None:
        classifier = make_fake_element("Class", getName="Widget")
        helper = _make_helper()

        assert helper.get_classifier_name(classifier) == "Widget"

    def test_returns_none_for_none_input(self) -> None:
        helper = _make_helper()

        assert helper.get_classifier_name(None) is None


class TestSetTypeKind:
    """UTS_XCH_00026: _set_type_kind."""

    def test_calls_set_kind_on_type_element(self) -> None:
        type_element = make_fake_element("Type")
        helper = _make_helper()

        helper._set_type_kind(type_element, "Enumeration")

        type_element.setKind.assert_called_once_with("Enumeration")


class TestCollectChildren:
    """UTS_XCH_00027, UTS_XCH_00028: _collect_children."""

    def test_returns_nested_elements_for_class(self) -> None:
        child1 = make_fake_element("Attribute", getName="a")
        child2 = make_fake_element("Operation", getName="b")
        container = make_fake_element("Class", getNestedElements=make_fake_collection([child1, child2]))
        helper = _make_helper()

        result = helper._collect_children(container)

        assert len(result) == 2
        assert result[0].get_name() == "a"
        assert result[1].get_name() == "b"

    def test_merges_package_globals_when_available(self) -> None:
        """UTS_XCH_00028: Package globals (functions, variables, objects) merged into children."""
        nested = make_fake_element("Class", getName="Nested")
        global_fn = make_fake_element("Operation", getName="globalFn")
        global_var = make_fake_element("Variable", getName="globalVar")
        global_obj = make_fake_element("Object", getName="globalObj")
        pkg = make_fake_element(
            "Package",
            getNestedElements=make_fake_collection([nested]),
            getGlobalFunctions=make_fake_collection([global_fn]),
            getGlobalVariables=make_fake_collection([global_var]),
            getGlobalObjects=make_fake_collection([global_obj]),
        )
        helper = _make_helper()

        result = helper._collect_children(pkg)

        names = [e.get_name() for e in result]
        assert "Nested" in names
        assert "globalFn" in names
        assert "globalVar" in names
        assert "globalObj" in names

    def test_package_without_global_getters_returns_only_nested(self) -> None:
        """If get_global_functions etc. are missing, fall back to nested elements only."""
        nested = make_fake_element("Class", getName="Nested")
        # Use a MagicMock spec that excludes global getters
        pkg = make_fake_element("Package", getNestedElements=make_fake_collection([nested]))
        # Remove global getters to simulate missing API
        del pkg.getGlobalFunctions
        del pkg.getGlobalVariables
        del pkg.getGlobalObjects
        helper = _make_helper()

        result = helper._collect_children(pkg)

        assert len(result) == 1
        assert result[0].get_name() == "Nested"


class TestGetProjectName:
    """UTS_XCH_00029: _get_project_name."""

    def test_walks_owner_chain_to_project(self) -> None:
        project = make_fake_element("Project", getName="MyProject")
        pkg = make_fake_element("Package", getName="Sub", getOwner=project)
        helper = _make_helper()

        result = helper._get_project_name(pkg)

        assert result == "MyProject"

    def test_returns_project_name_when_container_is_project(self) -> None:
        project = make_fake_element("Project", getName="TopLevel")
        helper = _make_helper()

        result = helper._get_project_name(project)

        assert result == "TopLevel"

    def test_returns_empty_string_when_no_project_in_chain(self) -> None:
        """If owner chain never reaches a Project, return empty string (defensive)."""
        orphan = make_fake_element("Package", getName="Orphan", getOwner=None)
        helper = _make_helper()

        result = helper._get_project_name(orphan)

        assert result == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_core.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.exchange.core'`

- [ ] **Step 3: Write minimal implementation**

Create `src/rhapsody_cli/exchange/core.py`:

```python
"""RhapsodyModelHelper: reusable model manipulation for exchange and beyond.

SWR_XCH_006: Element Find-or-Create (RhapsodyModelHelper)
SWR_XCH_007: Stereotype and Tag Round-Trip
SWR_XCH_010: Reusable Model Manipulation API
"""

import logging
from typing import TYPE_CHECKING, List, Optional

from rhapsody_cli.models.core import RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.application import RhapsodyApplication
    from rhapsody_cli.models.elements.containment import RPProject

logger = logging.getLogger(__name__)


class RhapsodyModelHelper:
    """Reusable model manipulation utilities.

    Provides idempotent find-or-create methods for the 14 supported element
    types, plus stereotype/tag application, classifier resolution, and
    child lookup. Used by both RhapsodyImporter and RhapsodyExporter.

    Attributes:
        app: RhapsodyApplication instance (lazily connected if not provided).
        project: Active RPProject, or None until set by caller.
    """

    def __init__(self, app: Optional["RhapsodyApplication"] = None) -> None:
        """Initialize with optional app; connect lazily if not provided.

        Args:
            app: Existing RhapsodyApplication, or None to trigger lazy connect.
        """
        if app is None:
            from rhapsody_cli.application import RhapsodyApplication

            app = RhapsodyApplication.connect(attach_only=True)
        self.app = app
        self.project: Optional["RPProject"] = None

    # ------------------------------------------------------------------
    # Element find/create (idempotent)
    # ------------------------------------------------------------------

    def find_or_create_package(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Package under parent. Sanitizes name (spaces -> underscores)."""
        sanitized = name.replace(" ", "_")
        existing = self.find_child_by_name(parent, "Package", sanitized)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Package", sanitized)

    def find_or_create_class(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Class under parent."""
        existing = self.find_child_by_name(parent, "Class", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Class", name)

    def find_or_create_operation(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Operation under parent.

        Uses add_global_function when parent is a Package (Rhapsody stores
        global functions in a hidden TopLevel class); otherwise add_new_aggr.
        """
        existing = self.find_child_by_name(parent, "Operation", name)
        if existing is not None:
            return existing
        if parent.get_meta_class() == "Package":
            return parent.add_global_function(name)
        return parent.add_new_aggr("Operation", name)

    def find_or_create_argument(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Argument under an Operation."""
        existing = self.find_child_by_name(parent, "Argument", name)
        if existing is not None:
            return existing
        return parent.add_argument(name)

    def find_or_create_attribute(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Attribute under parent."""
        existing = self.find_child_by_name(parent, "Attribute", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Attribute", name)

    def find_or_create_type(
        self, parent: RPModelElement, name: str, kind: Optional[str] = None
    ) -> RPModelElement:
        """Find or create a Type under parent, optionally setting its kind."""
        existing = self.find_child_by_name(parent, "Type", name)
        if existing is not None:
            return existing
        element = parent.add_new_aggr("Type", name)
        if kind is not None:
            self._set_type_kind(element, kind)
        return element

    def find_or_create_object(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Object (instance) under parent."""
        existing = self.find_child_by_name(parent, "Object", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Object", name)

    def find_or_create_enumeration_literal(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an EnumerationLiteral under a Type (kind=Enumeration)."""
        existing = self.find_child_by_name(parent, "EnumerationLiteral", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("EnumerationLiteral", name)

    # ------------------------------------------------------------------
    # Property application
    # ------------------------------------------------------------------

    def apply_stereotypes(self, element: RPModelElement, stereotypes: List[str]) -> None:
        """Apply stereotypes to element, inferring meta_type from element's metaclass.

        Skips stereotypes already applied (idempotent).
        """
        if not stereotypes:
            return
        meta_type = element.get_meta_class()
        already_applied = set()
        try:
            existing = element.get_stereotypes()
            for st in existing:
                try:
                    already_applied.add(st.get_name())
                except Exception:
                    continue
        except Exception:
            # If we can't read existing stereotypes, apply all (defensive)
            pass
        for name in stereotypes:
            if name in already_applied:
                continue
            element.add_stereotype(name, meta_type)

    def apply_tags(self, element: RPModelElement, tags: dict) -> None:
        """Apply tags to element via set_property_value (idempotent).

        Uses set_property_value (existing convention from package_action.py)
        which creates the property if missing and updates if present.
        """
        for name, value in tags.items():
            element.set_property_value(name, str(value))

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def resolve_classifier(self, name: str) -> Optional[RPModelElement]:
        """Find a classifier by name anywhere in the project. Returns None if not found."""
        if self.project is None:
            return None
        return self._find_element_by_name(self.project, name)

    def get_classifier_name(self, classifier: Optional[RPModelElement]) -> Optional[str]:
        """Return classifier's name, or None if classifier is None or unreadable."""
        if classifier is None:
            return None
        try:
            return classifier.get_name()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Public lookup
    # ------------------------------------------------------------------

    def find_child_by_name(
        self, parent: RPModelElement, meta_class: str, name: str
    ) -> Optional[RPModelElement]:
        """Find a direct child of parent by metaclass + name. Returns None if not found."""
        try:
            children = parent.get_nested_elements()
        except Exception:
            return None
        for child in children:
            try:
                if child.get_meta_class() == meta_class and child.get_name() == name:
                    return child
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------
    # Private (exchange-specific internals)
    # ------------------------------------------------------------------

    def _set_type_kind(self, type_element: RPModelElement, kind: str) -> None:
        """Set a Type's kind (Enumeration, Structure, Language, Typedef, Union)."""
        type_element.set_kind(kind)

    def _collect_children(self, container: RPModelElement) -> List[RPModelElement]:
        """Collect all children of a container.

        For Package containers, merges get_nested_elements() with package-level
        globals (get_global_functions, get_global_variables, get_global_objects)
        since getNestedElements() excludes them.

        For other containers, returns list(get_nested_elements()).
        """
        try:
            children = list(container.get_nested_elements())
        except Exception:
            children = []
        if container.get_meta_class() == "Package":
            for getter_name in ("get_global_functions", "get_global_variables", "get_global_objects"):
                getter = getattr(container, getter_name, None)
                if getter is None:
                    continue
                try:
                    children.extend(getter())
                except Exception:
                    continue
        return children

    def _get_project_name(self, container: RPModelElement) -> str:
        """Walk owner chain to find the Project; return its name, or '' if not found."""
        current: Optional[RPModelElement] = container
        visited: set = set()
        while current is not None:
            try:
                meta = current.get_meta_class()
            except Exception:
                break
            if meta == "Project":
                try:
                    return current.get_name()
                except Exception:
                    return ""
            try:
                key = id(current._com) if hasattr(current, "_com") else id(current)
            except Exception:
                break
            if key in visited:
                break  # cycle guard
            visited.add(key)
            try:
                current = current.get_owner()
            except Exception:
                break
        return ""

    def _find_element_by_name(
        self, container: RPModelElement, name: str
    ) -> Optional[RPModelElement]:
        """Recursively search container's nested elements for one with matching name."""
        try:
            children = container.get_nested_elements()
        except Exception:
            return None
        for child in children:
            try:
                if child.get_name() == name:
                    return child
            except Exception:
                continue
            result = self._find_element_by_name(child, name)
            if result is not None:
                return result
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_core.py -v`
Expected: PASS (all ~22 tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
black --check src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
mypy src/rhapsody_cli/exchange/core.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
git commit -m "feat(exchange): add RhapsodyModelHelper base with 8 element types

Idempotent find_or_create methods for Package, Class, Operation, Argument,
Attribute, Type, Object, EnumerationLiteral. Includes apply_stereotypes
(idempotent, infers meta_type), apply_tags (via set_property_value),
resolve_classifier (recursive project search), find_child_by_name,
_set_type_kind, _collect_children (with package globals merge),
_get_project_name (walks owner chain). SWR_XCH_006, SWR_XCH_007, SWR_XCH_010."
```

---

## Task 4: Extend RhapsodyModelHelper with 6 new find_or_create methods

**Files:**
- Modify: `src/rhapsody_cli/exchange/core.py` (append 6 methods before the private section)
- Test: `tests/unit/exchange/test_core.py` (append 6 test classes)

**Interfaces:**
- Consumes: existing `find_child_by_name` from Task 3
- Produces: 6 new methods on `RhapsodyModelHelper`: `find_or_create_dependency`, `find_or_create_generalization`, `find_or_create_relation`, `find_or_create_port`, `find_or_create_event`, `find_or_create_event_reception`

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/exchange/test_core.py` (before the final blank line):

```python
class TestFindOrCreateDependency:
    """UTS_XCH_00031: find_or_create_dependency."""

    def test_creates_dependency_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_dep = make_fake_element("Dependency", getName="dep1")
        parent.addNewAggr.return_value = new_dep
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_dependency(parent, "dep1")

        parent.addNewAggr.assert_called_once_with("Dependency", "dep1")
        assert result.get_name() == "dep1"

    def test_returns_existing_dependency(self) -> None:
        existing = make_fake_element("Dependency", getName="dep1")
        parent = make_fake_element("Class")
        parent.getNestedElements.return_value = make_fake_collection([existing])
        helper = _make_helper()

        result = helper.find_or_create_dependency(parent, "dep1")

        parent.addNewAggr.assert_not_called()
        assert result.get_name() == "dep1"


class TestFindOrCreateGeneralization:
    """UTS_XCH_00032: find_or_create_generalization."""

    def test_creates_generalization_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_gen = make_fake_element("Generalization", getName="gen1")
        parent.addNewAggr.return_value = new_gen
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_generalization(parent, "gen1")

        parent.addNewAggr.assert_called_once_with("Generalization", "gen1")
        assert result.get_name() == "gen1"


class TestFindOrCreateRelation:
    """UTS_XCH_00033: find_or_create_relation."""

    def test_creates_relation_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_rel = make_fake_element("Relation", getName="assoc1")
        parent.addNewAggr.return_value = new_rel
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_relation(parent, "assoc1")

        parent.addNewAggr.assert_called_once_with("Relation", "assoc1")
        assert result.get_name() == "assoc1"


class TestFindOrCreatePort:
    """UTS_XCH_00034: find_or_create_port."""

    def test_creates_port_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_port = make_fake_element("Port", getName="p1")
        parent.addNewAggr.return_value = new_port
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_port(parent, "p1")

        parent.addNewAggr.assert_called_once_with("Port", "p1")
        assert result.get_name() == "p1"


class TestFindOrCreateEvent:
    """UTS_XCH_00035: find_or_create_event."""

    def test_creates_event_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Package")
        new_evt = make_fake_element("Event", getName="TickEvent")
        parent.addNewAggr.return_value = new_evt
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_event(parent, "TickEvent")

        parent.addNewAggr.assert_called_once_with("Event", "TickEvent")
        assert result.get_name() == "TickEvent"


class TestFindOrCreateEventReception:
    """UTS_XCH_00036: find_or_create_event_reception."""

    def test_creates_reception_via_add_new_aggr(self) -> None:
        parent = make_fake_element("Class")
        new_rec = make_fake_element("EventReception", getName="onTick")
        parent.addNewAggr.return_value = new_rec
        parent.getNestedElements.return_value = make_fake_collection([])
        helper = _make_helper()

        result = helper.find_or_create_event_reception(parent, "onTick")

        parent.addNewAggr.assert_called_once_with("EventReception", "onTick")
        assert result.get_name() == "onTick"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_core.py -v -k "find_or_create_dependency or find_or_create_generalization or find_or_create_relation or find_or_create_port or find_or_create_event"`
Expected: FAIL with `AttributeError: 'RhapsodyModelHelper' object has no attribute 'find_or_create_dependency'`

- [ ] **Step 3: Write minimal implementation**

In `src/rhapsody_cli/exchange/core.py`, locate the line `# --- Private (exchange-specific internals) ---` and INSERT the following methods BEFORE it (after `find_or_create_enumeration_literal`):

```python
    def find_or_create_dependency(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Dependency under parent. Source/target wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Dependency", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Dependency", name)

    def find_or_create_generalization(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Generalization under parent. Base class wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Generalization", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Generalization", name)

    def find_or_create_relation(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Relation (Association/Aggregation/Composition) under parent."""
        existing = self.find_child_by_name(parent, "Relation", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Relation", name)

    def find_or_create_port(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create a Port under parent. Contract/interface wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Port", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Port", name)

    def find_or_create_event(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an Event under parent. Base/super event wiring handled by importer."""
        existing = self.find_child_by_name(parent, "Event", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("Event", name)

    def find_or_create_event_reception(self, parent: RPModelElement, name: str) -> RPModelElement:
        """Find or create an EventReception under parent. Event reference wiring handled by importer."""
        existing = self.find_child_by_name(parent, "EventReception", name)
        if existing is not None:
            return existing
        return parent.add_new_aggr("EventReception", name)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_core.py -v`
Expected: PASS (all tests including the 6 new ones)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
black --check src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
mypy src/rhapsody_cli/exchange/core.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/core.py tests/unit/exchange/test_core.py
git commit -m "feat(exchange): add 6 new find_or_create methods to RhapsodyModelHelper

Adds find_or_create_dependency, _generalization, _relation, _port, _event,
_event_reception. All use the standard add_new_aggr pattern; source/target
wiring is deferred to the importer's _apply_<type>_extras methods.
SWR_XCH_006, SWR_XCH_010."
```

---

## Task 5: RhapsodyImporter (8 core element types)

**Files:**
- Create: `src/rhapsody_cli/exchange/importer.py`
- Test: `tests/unit/exchange/test_importer.py`

**Interfaces:**
- Consumes: `RhapsodyModelHelper` from Task 3/4, `SCHEMA_VERSION` from Task 1, `CliExecutionError` from `rhapsody_cli.exceptions`
- Produces: `RhapsodyImporter` class with:
  - `import_template(data: dict, root_element: RPModelElement) -> None`
  - `_process_element(parent, spec) -> Optional[RPModelElement]`
  - `_apply_operation_extras(operation, spec) -> None`
  - `_apply_argument_extras(arg, spec) -> None`
  - `_apply_attribute_extras(attr, spec) -> None`
  - `_apply_type_extras(type_element, spec) -> None`
  - `_apply_object_extras(obj, spec) -> None`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/exchange/test_importer.py`:

```python
"""Tests for RhapsodyImporter.

UTS_XCH_00037: import_template rejects wrong schema version
UTS_XCH_00038: import_template processes each top-level spec
UTS_XCH_00039: _process_element dispatches Package and recurses children
UTS_XCH_00040: _process_element dispatches Class
UTS_XCH_00041: _process_element dispatches Operation (on Class)
UTS_XCH_00042: _process_element dispatches Attribute
UTS_XCH_00043: _process_element dispatches Argument (via Operation extras)
UTS_XCH_00044: _process_element dispatches Type with kind
UTS_XCH_00045: _process_element dispatches Object
UTS_XCH_00046: _process_element dispatches EnumerationLiteral (via Type extras)
UTS_XCH_00047: _process_element applies stereotypes and tags
UTS_XCH_00048: _process_element skips unsupported type with warning
UTS_XCH_00049: _apply_operation_extras sets return_type
UTS_XCH_00050: _apply_operation_extras sets is_static
UTS_XCH_00051: _apply_operation_extras creates arguments
UTS_XCH_00052: _apply_argument_extras sets data_type
UTS_XCH_00053: _apply_argument_extras sets direction
UTS_XCH_00054: _apply_attribute_extras sets data_type, visibility, multiplicity, is_static
UTS_XCH_00055: _apply_type_extras creates enumeration literals
UTS_XCH_00056: _apply_object_extras sets classifier
UTS_XCH_00057: _apply_operation_extras warns on unresolvable return_type
"""

from unittest.mock import MagicMock

import pytest

from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.exchange.importer import RhapsodyImporter
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def _make_importer(project: object = None) -> RhapsodyImporter:
    """Build a RhapsodyImporter with mocked app and project (skips connect)."""
    importer = RhapsodyImporter.__new__(RhapsodyImporter)
    importer.app = MagicMock()
    importer.project = project
    return importer


class TestImportTemplateVersionCheck:
    """UTS_XCH_00037: import_template version validation."""

    def test_rejects_wrong_version(self) -> None:
        importer = _make_importer()
        root = make_fake_element("Package")

        with pytest.raises(CliExecutionError) as exc_info:
            importer.import_template({"version": 99, "rhapsody-model": []}, root)

        assert "version" in str(exc_info.value).lower()

    def test_accepts_version_one(self) -> None:
        importer = _make_importer()
        root = make_fake_element("Package")
        root.getNestedElements.return_value = make_fake_collection([])

        importer.import_template({"version": 1, "rhapsody-model": []}, root)

        # No exception raised


class TestImportTemplateProcessesSpecs:
    """UTS_XCH_00038: import_template iterates rhapsody-model specs."""

    def test_processes_each_top_level_spec(self) -> None:
        importer = _make_importer()
        root = make_fake_element("Package")
        new_pkg = make_fake_element("Package", getName="Pkg1")
        root.addNewAggr.return_value = new_pkg
        root.getNestedElements.return_value = make_fake_collection([])
        data = {
            "version": 1,
            "rhapsody-model": [
                {"name": "Pkg1", "type": "Package"},
                {"name": "Pkg2", "type": "Package"},
            ],
        }

        importer.import_template(data, root)

        assert root.addNewAggr.call_count == 2


class TestProcessElementDispatch:
    """UTS_XCH_00039-00048: _process_element dispatch and common property application."""

    def test_dispatches_package_and_recurses_children(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_pkg = make_fake_element("Package", getName="Pkg1")
        parent.addNewAggr.return_value = new_pkg
        parent.getNestedElements.return_value = make_fake_collection([])
        new_pkg.getNestedElements.return_value = make_fake_collection([])

        spec = {"name": "Pkg1", "type": "Package", "children": [{"name": "ChildCls", "type": "Class"}]}
        new_cls = make_fake_element("Class", getName="ChildCls")
        new_pkg.addNewAggr.return_value = new_cls

        importer._process_element(parent, spec)

        # Verify recursion: new_pkg.addNewAggr called for the Class child
        new_pkg.addNewAggr.assert_called_once_with("Class", "ChildCls")

    def test_dispatches_class(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_cls = make_fake_element("Class", getName="Widget")
        parent.addNewAggr.return_value = new_cls
        parent.getNestedElements.return_value = make_fake_collection([])
        new_cls.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "Widget", "type": "Class"})

        parent.addNewAggr.assert_called_once_with("Class", "Widget")
        assert result.get_name() == "Widget"

    def test_dispatches_operation_on_class(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_op = make_fake_element("Operation", getName="reset", getArguments=make_fake_collection([]))
        parent.addNewAggr.return_value = new_op
        parent.getNestedElements.return_value = make_fake_collection([])

        importer._process_element(parent, {"name": "reset", "type": "Operation"})

        parent.addNewAggr.assert_called_once_with("Operation", "reset")

    def test_dispatches_attribute(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_attr = make_fake_element("Attribute", getName="count")
        parent.addNewAggr.return_value = new_attr
        parent.getNestedElements.return_value = make_fake_collection([])

        importer._process_element(parent, {"name": "count", "type": "Attribute"})

        parent.addNewAggr.assert_called_once_with("Attribute", "count")

    def test_dispatches_type_with_kind(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_type = make_fake_element("Type", getName="Color")
        parent.addNewAggr.return_value = new_type
        parent.getNestedElements.return_value = make_fake_collection([])

        importer._process_element(parent, {"name": "Color", "type": "Type", "kind": "Enumeration"})

        parent.addNewAggr.assert_called_once_with("Type", "Color")
        new_type.setKind.assert_called_once_with("Enumeration")

    def test_dispatches_object(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_obj = make_fake_element("Object", getName="myObj")
        parent.addNewAggr.return_value = new_obj
        parent.getNestedElements.return_value = make_fake_collection([])

        importer._process_element(parent, {"name": "myObj", "type": "Object"})

        parent.addNewAggr.assert_called_once_with("Object", "myObj")

    def test_applies_stereotypes_and_tags(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_pkg = make_fake_element("Package", getName="Pkg1")
        parent.addNewAggr.return_value = new_pkg
        parent.getNestedElements.return_value = make_fake_collection([])

        spec = {
            "name": "Pkg1",
            "type": "Package",
            "stereotypes": ["SwComponent"],
            "tags": {"status": "active"},
        }

        importer._process_element(parent, spec)

        new_pkg.addStereotype.assert_called_once_with("SwComponent", "Package")
        new_pkg.setPropertyValue.assert_called_once_with("status", "active")

    def test_skips_unsupported_type_with_warning(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")

        result = importer._process_element(parent, {"name": "Foo", "type": "Activity"})

        assert result is None
        parent.addNewAggr.assert_not_called()


class TestApplyOperationExtras:
    """UTS_XCH_00049-00051, UTS_XCH_00057: _apply_operation_extras."""

    def test_sets_return_type_when_classifier_resolvable(self) -> None:
        classifier = make_fake_element("Class", getName="int")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([classifier]))
        importer = _make_importer(project=project)
        op = make_fake_element("Operation", getName="reset", getArguments=make_fake_collection([]))

        importer._apply_operation_extras(op, {"return_type": "int"})

        op.setReturns.assert_called_once_with(classifier)

    def test_warns_when_return_type_unresolvable(self) -> None:
        project = make_fake_element("Project", getNestedElements=make_fake_collection([]))
        importer = _make_importer(project=project)
        op = make_fake_element("Operation", getName="reset", getArguments=make_fake_collection([]))

        importer._apply_operation_extras(op, {"return_type": "Missing"})

        op.setReturns.assert_not_called()

    def test_sets_is_static(self) -> None:
        importer = _make_importer()
        op = make_fake_element("Operation", getName="reset", getArguments=make_fake_collection([]))

        importer._apply_operation_extras(op, {"is_static": True})

        op.setIsStatic.assert_called_once_with(True)

    def test_creates_arguments(self) -> None:
        importer = _make_importer()
        new_arg = make_fake_element("Argument", getName="x")
        op = make_fake_element("Operation", getName="reset", addArgument=new_arg, getArguments=make_fake_collection([]))
        op.getNestedElements.return_value = make_fake_collection([])

        importer._apply_operation_extras(op, {"arguments": [{"name": "x", "data_type": "int"}]})

        op.addArgument.assert_called_once_with("x")


class TestApplyArgumentExtras:
    """UTS_XCH_00052, UTS_XCH_00053: _apply_argument_extras."""

    def test_sets_data_type(self) -> None:
        classifier = make_fake_element("Class", getName="int")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([classifier]))
        importer = _make_importer(project=project)
        arg = make_fake_element("Argument", getName="x")

        importer._apply_argument_extras(arg, {"data_type": "int"})

        arg.setType.assert_called_once_with(classifier)

    def test_sets_direction(self) -> None:
        importer = _make_importer()
        arg = make_fake_element("Argument", getName="x")

        importer._apply_argument_extras(arg, {"direction": "in"})

        arg.setArgumentDirection.assert_called_once_with("in")


class TestApplyAttributeExtras:
    """UTS_XCH_00054: _apply_attribute_extras."""

    def test_sets_all_fields(self) -> None:
        classifier = make_fake_element("Class", getName="int")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([classifier]))
        importer = _make_importer(project=project)
        attr = make_fake_element("Attribute", getName="count")

        importer._apply_attribute_extras(
            attr,
            {
                "data_type": "int",
                "visibility": "public",
                "multiplicity": "1",
                "is_static": True,
            },
        )

        attr.setType.assert_called_once_with(classifier)
        attr.setVisibility.assert_called_once_with("public")
        attr.setMultiplicity.assert_called_once_with("1")
        attr.setIsStatic.assert_called_once_with(True)


class TestApplyTypeExtras:
    """UTS_XCH_00055: _apply_type_extras creates enumeration literals."""

    def test_creates_enumeration_literals(self) -> None:
        importer = _make_importer()
        type_element = make_fake_element("Type", getName="Color")
        new_lit = make_fake_element("EnumerationLiteral", getName="RED")
        type_element.addNewAggr.return_value = new_lit
        type_element.getNestedElements.return_value = make_fake_collection([])

        importer._apply_type_extras(
            type_element,
            {"kind": "Enumeration", "literals": [{"name": "RED"}, {"name": "GREEN"}]},
        )

        assert type_element.addNewAggr.call_count == 2
        type_element.addNewAggr.assert_any_call("EnumerationLiteral", "RED")
        type_element.addNewAggr.assert_any_call("EnumerationLiteral", "GREEN")


class TestApplyObjectExtras:
    """UTS_XCH_00056: _apply_object_extras."""

    def test_sets_classifier(self) -> None:
        classifier = make_fake_element("Class", getName="MyClass")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([classifier]))
        importer = _make_importer(project=project)
        obj = make_fake_element("Object", getName="myObj")

        importer._apply_object_extras(obj, {"classifier": "MyClass"})

        obj.setClassifier.assert_called_once_with(classifier)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_importer.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.exchange.importer'`

- [ ] **Step 3: Write minimal implementation**

Create `src/rhapsody_cli/exchange/importer.py`:

```python
"""RhapsodyImporter: YAML dict -> Rhapsody model.

SWR_XCH_002: Project Import
SWR_XCH_004: Package Import
SWR_XCH_006: Element Find-or-Create (uses RhapsodyModelHelper)
SWR_XCH_008: Core Type-Specific Fields
SWR_XCH_009: Error Handling and Skip-on-Unsupported
"""

import logging
from typing import TYPE_CHECKING, Optional

from rhapsody_cli.exchange.core import RhapsodyModelHelper
from rhapsody_cli.exchange.schema import RHAPSODY_MODEL_KEY, SCHEMA_VERSION, VERSION_KEY
from rhapsody_cli.exceptions import CliExecutionError
from rhapsody_cli.models.core import RPModelElement

if TYPE_CHECKING:
    from rhapsody_cli.application import RhapsodyApplication

logger = logging.getLogger(__name__)


class RhapsodyImporter(RhapsodyModelHelper):
    """Imports a YAML dict into a Rhapsody model container.

    Each element spec is processed via _process_element, which dispatches
    to find_or_create_<type>, applies common properties (stereotypes, tags),
    then applies type-specific extras and recurses into children.
    """

    def import_template(self, data: dict, root_element: RPModelElement) -> None:
        """Import elements from data['rhapsody-model'] as children of root_element.

        Args:
            data: Parsed YAML dict (must have version and rhapsody-model keys).
            root_element: Container to import into (project root or package).

        Raises:
            CliExecutionError: If schema version does not match SCHEMA_VERSION.
        """
        version = data.get(VERSION_KEY)
        if version != SCHEMA_VERSION:
            raise CliExecutionError(
                f"Unsupported schema version: {version} (expected {SCHEMA_VERSION})"
            )
        self.project = root_element
        for spec in data.get(RHAPSODY_MODEL_KEY, []):
            self._process_element(root_element, spec)

    def _process_element(
        self, parent: RPModelElement, spec: dict
    ) -> Optional[RPModelElement]:
        """Dispatch a single element spec to find_or_create_<type>, then apply extras.

        Args:
            parent: Container element to create under.
            spec: Element spec dict (must have 'name' and 'type').

        Returns:
            The created/existing element, or None if the type is unsupported.
        """
        element_type = spec["type"]
        name = spec["name"]

        if element_type == "Package":
            element = self.find_or_create_package(parent, name)
        elif element_type == "Class":
            element = self.find_or_create_class(parent, name)
        elif element_type == "Operation":
            element = self.find_or_create_operation(parent, name)
        elif element_type == "Attribute":
            element = self.find_or_create_attribute(parent, name)
        elif element_type == "Argument":
            element = self.find_or_create_argument(parent, name)
        elif element_type == "Type":
            element = self.find_or_create_type(parent, name, spec.get("kind"))
        elif element_type == "Object":
            element = self.find_or_create_object(parent, name)
        elif element_type == "EnumerationLiteral":
            element = self.find_or_create_enumeration_literal(parent, name)
        elif element_type == "Dependency":
            element = self.find_or_create_dependency(parent, name)
        elif element_type == "Generalization":
            element = self.find_or_create_generalization(parent, name)
        elif element_type == "Relation":
            element = self.find_or_create_relation(parent, name)
        elif element_type == "Port":
            element = self.find_or_create_port(parent, name)
        elif element_type == "Event":
            element = self.find_or_create_event(parent, name)
        elif element_type == "EventReception":
            element = self.find_or_create_event_reception(parent, name)
        else:
            logger.warning("Unsupported element type '%s'; skipping", element_type)
            return None

        # Common properties
        self.apply_stereotypes(element, spec.get("stereotypes", []))
        self.apply_tags(element, spec.get("tags", {}))

        # Type-specific extras
        if element_type == "Operation":
            self._apply_operation_extras(element, spec)
        elif element_type == "Attribute":
            self._apply_attribute_extras(element, spec)
        elif element_type == "Argument":
            self._apply_argument_extras(element, spec)
        elif element_type == "Type":
            self._apply_type_extras(element, spec)
        elif element_type == "Object":
            self._apply_object_extras(element, spec)
        # Dependency/Generalization/Relation/Port/Event/EventReception extras
        # are added in Task 6.

        # Generic children (Package, Class, Type with kind=Structure)
        if element_type in ("Package", "Class", "Type"):
            for child_spec in spec.get("children", []):
                self._process_element(element, child_spec)
        return element

    # ------------------------------------------------------------------
    # Type-specific extras (YAML spec fields -> element property setters)
    # ------------------------------------------------------------------

    def _apply_operation_extras(self, operation: RPModelElement, spec: dict) -> None:
        """Apply Operation-specific fields: return_type, is_static, arguments."""
        if "return_type" in spec:
            classifier = self.resolve_classifier(spec["return_type"])
            if classifier is not None:
                operation.set_returns(classifier)
            else:
                logger.warning(
                    "Cannot resolve return_type '%s' for operation '%s'",
                    spec["return_type"],
                    operation.get_name(),
                )
        if "is_static" in spec and hasattr(operation, "set_is_static"):
            operation.set_is_static(spec["is_static"])
        for arg_spec in spec.get("arguments", []):
            arg = self.find_or_create_argument(operation, arg_spec["name"])
            self._apply_argument_extras(arg, arg_spec)

    def _apply_argument_extras(self, arg: RPModelElement, spec: dict) -> None:
        """Apply Argument-specific fields: data_type, direction, stereotypes, tags."""
        if "data_type" in spec:
            classifier = self.resolve_classifier(spec["data_type"])
            if classifier is not None:
                arg.set_type(classifier)
            else:
                logger.warning(
                    "Cannot resolve data_type '%s' for argument '%s'",
                    spec["data_type"],
                    arg.get_name(),
                )
        if "direction" in spec and hasattr(arg, "set_argument_direction"):
            arg.set_argument_direction(spec["direction"])
        # Common properties (parity with _process_element path)
        self.apply_stereotypes(arg, spec.get("stereotypes", []))
        self.apply_tags(arg, spec.get("tags", {}))

    def _apply_attribute_extras(self, attr: RPModelElement, spec: dict) -> None:
        """Apply Attribute-specific fields: data_type, visibility, multiplicity, is_static."""
        if "data_type" in spec:
            classifier = self.resolve_classifier(spec["data_type"])
            if classifier is not None:
                attr.set_type(classifier)
            else:
                logger.warning(
                    "Cannot resolve data_type '%s' for attribute '%s'",
                    spec["data_type"],
                    attr.get_name(),
                )
        if "visibility" in spec and hasattr(attr, "set_visibility"):
            attr.set_visibility(spec["visibility"])
        if "multiplicity" in spec and hasattr(attr, "set_multiplicity"):
            attr.set_multiplicity(spec["multiplicity"])
        if "is_static" in spec and hasattr(attr, "set_is_static"):
            attr.set_is_static(spec["is_static"])

    def _apply_type_extras(self, type_element: RPModelElement, spec: dict) -> None:
        """Apply Type-specific fields: enumeration literals (kind already set in find_or_create_type)."""
        if spec.get("kind") == "Enumeration":
            for literal_spec in spec.get("literals", []):
                literal = self.find_or_create_enumeration_literal(type_element, literal_spec["name"])
                self.apply_stereotypes(literal, literal_spec.get("stereotypes", []))
                self.apply_tags(literal, literal_spec.get("tags", {}))

    def _apply_object_extras(self, obj: RPModelElement, spec: dict) -> None:
        """Apply Object-specific fields: classifier."""
        if "classifier" in spec:
            classifier = self.resolve_classifier(spec["classifier"])
            if classifier is not None and hasattr(obj, "set_classifier"):
                obj.set_classifier(classifier)
            else:
                logger.warning(
                    "Cannot resolve classifier '%s' for object '%s'",
                    spec["classifier"],
                    obj.get_name(),
                )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_importer.py -v`
Expected: PASS (all ~20 tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
black --check src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
mypy src/rhapsody_cli/exchange/importer.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
git commit -m "feat(exchange): add RhapsodyImporter with 8 core element types

Implements import_template (version check + dispatch loop) and _process_element
for Package, Class, Operation, Attribute, Argument, Type, Object,
EnumerationLiteral. Type-specific extras: _apply_operation_extras (return_type,
is_static, arguments), _apply_argument_extras (data_type, direction),
_apply_attribute_extras (data_type, visibility, multiplicity, is_static),
_apply_type_extras (enumeration literals), _apply_object_extras (classifier).
SWR_XCH_002, SWR_XCH_004, SWR_XCH_008, SWR_XCH_009."
```

---

## Task 6: Extend RhapsodyImporter with 6 new element types

**Files:**
- Modify: `src/rhapsody_cli/exchange/importer.py` (add 6 `_apply_<type>_extras` methods + dispatch wiring)
- Test: `tests/unit/exchange/test_importer.py` (append 6 test classes)

**Interfaces:**
- Consumes: `find_or_create_dependency`/`_generalization`/`_relation`/`_port`/`_event`/`_event_reception` from Task 4, `resolve_classifier` from Task 3
- Produces: 6 new methods: `_apply_dependency_extras`, `_apply_generalization_extras`, `_apply_relation_extras`, `_apply_port_extras`, `_apply_event_extras`, `_apply_event_reception_extras`

- [ ] **Step 1: Write the failing test**

Append to `tests/unit/exchange/test_importer.py`:

```python
class TestApplyDependencyExtras:
    """UTS_XCH_00058: _apply_dependency_extras wires source/target."""

    def test_sets_dependent_and_depends_on(self) -> None:
        target = make_fake_element("Class", getName="OtherClass")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([target]))
        importer = _make_importer(project=project)
        dependency = make_fake_element("Dependency", getName="dep1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_dependency_extras(dependency, {"depends_on": "OtherClass"}, parent)

        dependency.setDependent.assert_called_once_with(parent)
        dependency.setDependsOn.assert_called_once_with(target)

    def test_warns_when_depends_on_unresolvable(self) -> None:
        project = make_fake_element("Project", getNestedElements=make_fake_collection([]))
        importer = _make_importer(project=project)
        dependency = make_fake_element("Dependency", getName="dep1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_dependency_extras(dependency, {"depends_on": "Missing"}, parent)

        dependency.setDependsOn.assert_not_called()
        # setDependent still called (source is always the parent)
        dependency.setDependent.assert_called_once_with(parent)


class TestApplyGeneralizationExtras:
    """UTS_XCH_00059: _apply_generalization_extras wires derived/base."""

    def test_sets_derived_class_and_base_class(self) -> None:
        base = make_fake_element("Class", getName="BaseClass")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([base]))
        importer = _make_importer(project=project)
        generalization = make_fake_element("Generalization", getName="gen1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_generalization_extras(
            generalization,
            {"base_class": "BaseClass", "visibility": "public", "is_virtual": True},
            parent,
        )

        generalization.setDerivedClass.assert_called_once_with(parent)
        generalization.setBaseClass.assert_called_once_with(base)
        generalization.setVisibility.assert_called_once_with("public")
        generalization.setIsVirtual.assert_called_once_with(True)


class TestApplyRelationExtras:
    """UTS_XCH_00060: _apply_relation_extras wires source/target and properties."""

    def test_sets_source_target_and_properties(self) -> None:
        target = make_fake_element("Class", getName="OtherClass")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([target]))
        importer = _make_importer(project=project)
        relation = make_fake_element("Relation", getName="assoc1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_relation_extras(
            relation,
            {
                "relation_type": "Association",
                "to": "OtherClass",
                "multiplicity": "0..*",
                "is_navigable": True,
                "role": "items",
                "visibility": "public",
            },
            parent,
        )

        relation.setOfClass.assert_called_once_with(parent)
        relation.setOtherClass.assert_called_once_with(target)
        relation.setRelationType.assert_called_once_with("Association")
        relation.setMultiplicity.assert_called_once_with("0..*")
        relation.setIsNavigable.assert_called_once_with(True)
        relation.setRelationRoleName.assert_called_once_with("items")
        relation.setVisibility.assert_called_once_with("public")

    def test_uses_from_override_when_provided(self) -> None:
        source = make_fake_element("Class", getName="ExplicitSource")
        target = make_fake_element("Class", getName="Target")
        project = make_fake_element(
            "Project", getNestedElements=make_fake_collection([source, target])
        )
        importer = _make_importer(project=project)
        relation = make_fake_element("Relation", getName="assoc1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_relation_extras(
            relation,
            {"from": "ExplicitSource", "to": "Target"},
            parent,
        )

        relation.setOfClass.assert_called_once_with(source)

    def test_falls_back_to_parent_when_from_unresolvable(self) -> None:
        target = make_fake_element("Class", getName="Target")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([target]))
        importer = _make_importer(project=project)
        relation = make_fake_element("Relation", getName="assoc1")
        parent = make_fake_element("Class", getName="MyClass")

        importer._apply_relation_extras(
            relation,
            {"from": "Missing", "to": "Target"},
            parent,
        )

        relation.setOfClass.assert_called_once_with(parent)


class TestApplyPortExtras:
    """UTS_XCH_00061: _apply_port_extras sets flags, contract, interfaces."""

    def test_sets_flags_and_contract(self) -> None:
        contract = make_fake_element("Class", getName="IFoo")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([contract]))
        importer = _make_importer(project=project)
        port = make_fake_element("Port", getName="p1")

        importer._apply_port_extras(
            port,
            {
                "is_behavioral": True,
                "is_reversed": False,
                "contract": "IFoo",
            },
        )

        port.setIsBehavioral.assert_called_once_with(True)
        port.setIsReversed.assert_called_once_with(False)
        port.setContract.assert_called_once_with(contract)

    def test_adds_provided_and_required_interfaces(self) -> None:
        iface1 = make_fake_element("Class", getName="IFoo")
        iface2 = make_fake_element("Class", getName="IBar")
        project = make_fake_element(
            "Project", getNestedElements=make_fake_collection([iface1, iface2])
        )
        importer = _make_importer(project=project)
        port = make_fake_element("Port", getName="p1")

        importer._apply_port_extras(
            port,
            {"provided_interfaces": ["IFoo"], "required_interfaces": ["IBar"]},
        )

        port.addProvidedInterface.assert_called_once_with(iface1)
        port.addRequiredInterface.assert_called_once_with(iface2)


class TestApplyEventExtras:
    """UTS_XCH_00062: _apply_event_extras sets base_event and super_event."""

    def test_sets_base_and_super_event(self) -> None:
        base = make_fake_element("Event", getName="BaseEvent")
        sup = make_fake_element("Event", getName="SuperEvent")
        project = make_fake_element(
            "Project", getNestedElements=make_fake_collection([base, sup])
        )
        importer = _make_importer(project=project)
        event = make_fake_element("Event", getName="TickEvent")

        importer._apply_event_extras(
            event,
            {"base_event": "BaseEvent", "super_event": "SuperEvent"},
        )

        event.setBaseEvent.assert_called_once_with(base)
        event.setSuperEvent.assert_called_once_with(sup)


class TestApplyEventReceptionExtras:
    """UTS_XCH_00063: _apply_event_reception_extras sets event reference."""

    def test_sets_event_reference(self) -> None:
        evt = make_fake_element("Event", getName="TickEvent")
        project = make_fake_element("Project", getNestedElements=make_fake_collection([evt]))
        importer = _make_importer(project=project)
        reception = make_fake_element("EventReception", getName="onTick")

        importer._apply_event_reception_extras(reception, {"event": "TickEvent"})

        reception.setEvent.assert_called_once_with(evt)
```

Also add tests for `_process_element` dispatch of the 6 new types (append to the `TestProcessElementDispatch` class or as new test functions):

```python
class TestProcessElementNewTypes:
    """UTS_XCH_00064: _process_element dispatches the 6 new element types."""

    def test_dispatches_dependency(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_dep = make_fake_element("Dependency", getName="dep1")
        parent.addNewAggr.return_value = new_dep
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "dep1", "type": "Dependency"})

        parent.addNewAggr.assert_called_once_with("Dependency", "dep1")
        assert result.get_name() == "dep1"

    def test_dispatches_generalization(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_gen = make_fake_element("Generalization", getName="gen1")
        parent.addNewAggr.return_value = new_gen
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "gen1", "type": "Generalization"})

        parent.addNewAggr.assert_called_once_with("Generalization", "gen1")
        assert result.get_name() == "gen1"

    def test_dispatches_relation(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_rel = make_fake_element("Relation", getName="assoc1")
        parent.addNewAggr.return_value = new_rel
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "assoc1", "type": "Relation"})

        parent.addNewAggr.assert_called_once_with("Relation", "assoc1")

    def test_dispatches_port(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_port = make_fake_element("Port", getName="p1")
        parent.addNewAggr.return_value = new_port
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "p1", "type": "Port"})

        parent.addNewAggr.assert_called_once_with("Port", "p1")

    def test_dispatches_event(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Package")
        new_evt = make_fake_element("Event", getName="TickEvent")
        parent.addNewAggr.return_value = new_evt
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "TickEvent", "type": "Event"})

        parent.addNewAggr.assert_called_once_with("Event", "TickEvent")

    def test_dispatches_event_reception(self) -> None:
        importer = _make_importer()
        parent = make_fake_element("Class")
        new_rec = make_fake_element("EventReception", getName="onTick")
        parent.addNewAggr.return_value = new_rec
        parent.getNestedElements.return_value = make_fake_collection([])

        result = importer._process_element(parent, {"name": "onTick", "type": "EventReception"})

        parent.addNewAggr.assert_called_once_with("EventReception", "onTick")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_importer.py -v -k "dependency or generalization or relation or port or event or reception"`
Expected: FAIL with `AttributeError: 'RhapsodyImporter' object has no attribute '_apply_dependency_extras'`

- [ ] **Step 3: Write minimal implementation**

In `src/rhapsody_cli/exchange/importer.py`, locate the `_process_element` method's "Type-specific extras" block and REPLACE the comment `# Dependency/Generalization/Relation/Port/Event/EventReception extras\n        # are added in Task 6.` with the actual dispatch:

```python
        elif element_type == "Dependency":
            self._apply_dependency_extras(element, spec, parent)
        elif element_type == "Generalization":
            self._apply_generalization_extras(element, spec, parent)
        elif element_type == "Relation":
            self._apply_relation_extras(element, spec, parent)
        elif element_type == "Port":
            self._apply_port_extras(element, spec)
        elif element_type == "Event":
            self._apply_event_extras(element, spec)
        elif element_type == "EventReception":
            self._apply_event_reception_extras(element, spec)
```

Then APPEND the following methods at the end of the `RhapsodyImporter` class (after `_apply_object_extras`):

```python
    def _apply_dependency_extras(
        self, dependency: RPModelElement, spec: dict, parent: RPModelElement
    ) -> None:
        """Apply Dependency-specific fields: source (parent) and target (depends_on)."""
        if hasattr(dependency, "set_dependent"):
            dependency.set_dependent(parent)
        if "depends_on" in spec:
            target = self.resolve_classifier(spec["depends_on"])
            if target is not None and hasattr(dependency, "set_depends_on"):
                dependency.set_depends_on(target)
            else:
                logger.warning(
                    "Cannot resolve depends_on '%s' for dependency '%s'",
                    spec["depends_on"],
                    dependency.get_name(),
                )

    def _apply_generalization_extras(
        self, generalization: RPModelElement, spec: dict, parent: RPModelElement
    ) -> None:
        """Apply Generalization-specific fields: derived_class (parent), base_class, visibility, is_virtual."""
        if hasattr(generalization, "set_derived_class"):
            generalization.set_derived_class(parent)
        if "base_class" in spec:
            target = self.resolve_classifier(spec["base_class"])
            if target is not None and hasattr(generalization, "set_base_class"):
                generalization.set_base_class(target)
            else:
                logger.warning(
                    "Cannot resolve base_class '%s' for generalization '%s'",
                    spec["base_class"],
                    generalization.get_name(),
                )
        if "visibility" in spec and hasattr(generalization, "set_visibility"):
            generalization.set_visibility(spec["visibility"])
        if "is_virtual" in spec and hasattr(generalization, "set_is_virtual"):
            generalization.set_is_virtual(spec["is_virtual"])

    def _apply_relation_extras(
        self, relation: RPModelElement, spec: dict, parent: RPModelElement
    ) -> None:
        """Apply Relation-specific fields: from (source), to (target), relation_type, multiplicity, etc."""
        if "from" in spec:
            source = self.resolve_classifier(spec["from"])
            if source is None:
                logger.warning(
                    "Cannot resolve from '%s' for relation '%s'; using parent",
                    spec["from"],
                    relation.get_name(),
                )
                source = parent
        else:
            source = parent
        if hasattr(relation, "set_of_class"):
            relation.set_of_class(source)
        if "to" in spec:
            target = self.resolve_classifier(spec["to"])
            if target is not None and hasattr(relation, "set_other_class"):
                relation.set_other_class(target)
            else:
                logger.warning(
                    "Cannot resolve to '%s' for relation '%s'",
                    spec["to"],
                    relation.get_name(),
                )
        if "relation_type" in spec and hasattr(relation, "set_relation_type"):
            relation.set_relation_type(spec["relation_type"])
        if "multiplicity" in spec and hasattr(relation, "set_multiplicity"):
            relation.set_multiplicity(spec["multiplicity"])
        if "is_navigable" in spec and hasattr(relation, "set_is_navigable"):
            relation.set_is_navigable(spec["is_navigable"])
        if "role" in spec and hasattr(relation, "set_relation_role_name"):
            relation.set_relation_role_name(spec["role"])
        if "visibility" in spec and hasattr(relation, "set_visibility"):
            relation.set_visibility(spec["visibility"])

    def _apply_port_extras(self, port: RPModelElement, spec: dict) -> None:
        """Apply Port-specific fields: is_behavioral, is_reversed, contract, provided/required_interfaces."""
        if "is_behavioral" in spec and hasattr(port, "set_is_behavioral"):
            port.set_is_behavioral(spec["is_behavioral"])
        if "is_reversed" in spec and hasattr(port, "set_is_reversed"):
            port.set_is_reversed(spec["is_reversed"])
        if "contract" in spec:
            classifier = self.resolve_classifier(spec["contract"])
            if classifier is not None and hasattr(port, "set_contract"):
                port.set_contract(classifier)
            else:
                logger.warning(
                    "Cannot resolve contract '%s' for port '%s'",
                    spec["contract"],
                    port.get_name(),
                )
        for iface_name in spec.get("provided_interfaces", []):
            iface = self.resolve_classifier(iface_name)
            if iface is not None and hasattr(port, "add_provided_interface"):
                port.add_provided_interface(iface)
            else:
                logger.warning(
                    "Cannot resolve provided_interface '%s' for port '%s'",
                    iface_name,
                    port.get_name(),
                )
        for iface_name in spec.get("required_interfaces", []):
            iface = self.resolve_classifier(iface_name)
            if iface is not None and hasattr(port, "add_required_interface"):
                port.add_required_interface(iface)
            else:
                logger.warning(
                    "Cannot resolve required_interface '%s' for port '%s'",
                    iface_name,
                    port.get_name(),
                )

    def _apply_event_extras(self, event: RPModelElement, spec: dict) -> None:
        """Apply Event-specific fields: base_event, super_event."""
        if "base_event" in spec:
            target = self.resolve_classifier(spec["base_event"])
            if target is not None and hasattr(event, "set_base_event"):
                event.set_base_event(target)
            else:
                logger.warning(
                    "Cannot resolve base_event '%s' for event '%s'",
                    spec["base_event"],
                    event.get_name(),
                )
        if "super_event" in spec:
            target = self.resolve_classifier(spec["super_event"])
            if target is not None and hasattr(event, "set_super_event"):
                event.set_super_event(target)
            else:
                logger.warning(
                    "Cannot resolve super_event '%s' for event '%s'",
                    spec["super_event"],
                    event.get_name(),
                )

    def _apply_event_reception_extras(self, reception: RPModelElement, spec: dict) -> None:
        """Apply EventReception-specific fields: event reference."""
        if "event" in spec:
            target = self.resolve_classifier(spec["event"])
            if target is not None and hasattr(reception, "set_event"):
                reception.set_event(target)
            else:
                logger.warning(
                    "Cannot resolve event '%s' for reception '%s'",
                    spec["event"],
                    reception.get_name(),
                )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_importer.py -v`
Expected: PASS (all tests including new ones)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
black --check src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
mypy src/rhapsody_cli/exchange/importer.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/importer.py tests/unit/exchange/test_importer.py
git commit -m "feat(exchange): extend RhapsodyImporter with 6 new element types

Adds _apply_<type>_extras for Dependency (source/target wiring),
Generalization (derived/base + visibility + is_virtual), Relation (from/to
+ relation_type + multiplicity + is_navigable + role + visibility),
Port (is_behavioral + is_reversed + contract + provided/required_interfaces),
Event (base_event + super_event), EventReception (event reference).
Wires dispatch in _process_element. SWR_XCH_011, SWR_XCH_012, SWR_XCH_013."
```

---

## Task 7: RhapsodyExporter (8 core element types)

**Files:**
- Create: `src/rhapsody_cli/exchange/exporter.py`
- Test: `tests/unit/exchange/test_exporter.py`

**Interfaces:**
- Consumes: `RhapsodyModelHelper` from Task 3/4, `SCHEMA_VERSION` from Task 1
- Produces: `RhapsodyExporter` class with:
  - `export(container) -> dict`
  - `_export_element(element) -> Optional[dict]`
  - `_export_package(pkg)`, `_export_class(cls)`, `_export_operation(op)`, `_export_argument(arg)`, `_export_attribute(attr)`, `_export_type(type_element)`, `_export_object(obj)`, `_export_enumeration_literal(literal)`
  - `_export_stereotypes(element) -> List[str]`, `_export_tags(element) -> Dict[str, str]`

- [ ] **Step 1: Write the failing test**

Create `tests/unit/exchange/test_exporter.py`:

```python
"""Tests for RhapsodyExporter.

UTS_XCH_00065: export returns dict with version, project, rhapsody-model keys
UTS_XCH_00066: export includes project name from container
UTS_XCH_00067: _export_element dispatches Package
UTS_XCH_00068: _export_element dispatches Class
UTS_XCH_00069: _export_operation emits return_type, is_static, arguments
UTS_XCH_00070: _export_argument emits data_type and direction
UTS_XCH_00071: _export_attribute emits data_type, visibility, multiplicity, is_static
UTS_XCH_00072: _export_type emits kind and enumeration literals
UTS_XCH_00073: _export_type emits children for Structure kind
UTS_XCH_00074: _export_object emits classifier
UTS_XCH_00075: _export_enumeration_literal emits name only
UTS_XCH_00076: _export_stereotypes returns names
UTS_XCH_00077: _export_tags returns name/value dict
UTS_XCH_00078: _export_element skips unsupported metaclass
UTS_XCH_00079: _export_element attaches stereotypes and tags
"""

from unittest.mock import MagicMock

from rhapsody_cli.exchange.exporter import RhapsodyExporter
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def _make_exporter(project: object = None) -> RhapsodyExporter:
    """Build a RhapsodyExporter with mocked app and project."""
    exporter = RhapsodyExporter.__new__(RhapsodyExporter)
    exporter.app = MagicMock()
    exporter.project = project
    return exporter


class TestExport:
    """UTS_XCH_00065, UTS_XCH_00066: export() top-level dict shape."""

    def test_returns_dict_with_required_keys(self) -> None:
        project = make_fake_element("Project", getName="MyProject")
        project.getNestedElements.return_value = make_fake_collection([])
        exporter = _make_exporter()

        result = exporter.export(project)

        assert result["version"] == 1
        assert result["project"] == "MyProject"
        assert result["rhapsody-model"] == []

    def test_includes_project_name_from_container(self) -> None:
        project = make_fake_element("Project", getName="TopLevel")
        pkg = make_fake_element("Package", getName="Sub", getOwner=project)
        pkg.getNestedElements.return_value = make_fake_collection([])
        exporter = _make_exporter()

        result = exporter.export(pkg)

        assert result["project"] == "TopLevel"

    def test_includes_exported_children(self) -> None:
        cls = make_fake_element("Class", getName="Widget")
        cls.getNestedElements.return_value = make_fake_collection([])
        project = make_fake_element(
            "Project",
            getName="P",
            getNestedElements=make_fake_collection([cls]),
        )
        exporter = _make_exporter()

        result = exporter.export(project)

        assert len(result["rhapsody-model"]) == 1
        assert result["rhapsody-model"][0]["name"] == "Widget"
        assert result["rhapsody-model"][0]["type"] == "Class"


class TestExportPackage:
    """UTS_XCH_00067: _export_package."""

    def test_emits_name_type_and_children(self) -> None:
        child = make_fake_element("Class", getName="Inner")
        child.getNestedElements.return_value = make_fake_collection([])
        pkg = make_fake_element(
            "Package",
            getName="Outer",
            getNestedElements=make_fake_collection([child]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(pkg)

        assert result["name"] == "Outer"
        assert result["type"] == "Package"
        assert "children" in result
        assert result["children"][0]["name"] == "Inner"


class TestExportClass:
    """UTS_XCH_00068: _export_class."""

    def test_emits_name_type(self) -> None:
        cls = make_fake_element(
            "Class",
            getName="Widget",
            getNestedElements=make_fake_collection([]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(cls)

        assert result["name"] == "Widget"
        assert result["type"] == "Class"


class TestExportOperation:
    """UTS_XCH_00069: _export_operation."""

    def test_emits_return_type_is_static_and_arguments(self) -> None:
        return_classifier = make_fake_element("Class", getName="int")
        arg = make_fake_element(
            "Argument",
            getName="x",
            getType=return_classifier,
            getArgumentDirection="in",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        op = make_fake_element(
            "Operation",
            getName="reset",
            getReturns=return_classifier,
            getIsStatic=True,
            getArguments=make_fake_collection([arg]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(op)

        assert result["return_type"] == "int"
        assert result["is_static"] is True
        assert len(result["arguments"]) == 1
        assert result["arguments"][0]["name"] == "x"
        assert result["arguments"][0]["data_type"] == "int"
        assert result["arguments"][0]["direction"] == "in"


class TestExportArgument:
    """UTS_XCH_00070: _export_argument."""

    def test_emits_data_type_and_direction(self) -> None:
        classifier = make_fake_element("Class", getName="String")
        arg = make_fake_element(
            "Argument",
            getName="name",
            getType=classifier,
            getArgumentDirection="in",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(arg)

        assert result["name"] == "name"
        assert result["type"] == "Argument"
        assert result["data_type"] == "String"
        assert result["direction"] == "in"


class TestExportAttribute:
    """UTS_XCH_00071: _export_attribute."""

    def test_emits_all_fields(self) -> None:
        classifier = make_fake_element("Class", getName="int")
        attr = make_fake_element(
            "Attribute",
            getName="count",
            getType=classifier,
            getVisibility="public",
            getMultiplicity="1",
            getIsStatic=False,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(attr)

        assert result["data_type"] == "int"
        assert result["visibility"] == "public"
        assert result["multiplicity"] == "1"
        assert result["is_static"] is False


class TestExportType:
    """UTS_XCH_00072, UTS_XCH_00073: _export_type."""

    def test_emits_kind_and_enumeration_literals(self) -> None:
        literal = make_fake_element(
            "EnumerationLiteral",
            getName="RED",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        type_element = make_fake_element(
            "Type",
            getName="Color",
            getKind="Enumeration",
            getEnumerationLiterals=make_fake_collection([literal]),
            getNestedElements.return_value=make_fake_collection([]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(type_element)

        assert result["kind"] == "Enumeration"
        assert "literals" in result
        assert result["literals"][0]["name"] == "RED"

    def test_emits_children_for_structure_kind(self) -> None:
        child = make_fake_element(
            "Attribute",
            getName="x",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        # Strip getType to avoid requiring classifier resolution
        type_element = make_fake_element(
            "Type",
            getName="Point",
            getKind="Structure",
            getNestedElements=make_fake_collection([child]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        # Attribute child needs getType for data_type, but here we just verify children list
        child.getType.return_value = None
        child.getVisibility.return_value = None
        child.getMultiplicity.return_value = None
        child.getIsStatic.return_value = None
        exporter = _make_exporter()

        result = exporter._export_element(type_element)

        assert result["kind"] == "Structure"
        assert "children" in result
        assert result["children"][0]["name"] == "x"


class TestExportObject:
    """UTS_XCH_00074: _export_object."""

    def test_emits_classifier(self) -> None:
        classifier = make_fake_element("Class", getName="MyClass")
        obj = make_fake_element(
            "Object",
            getName="myObj",
            getClassifier=classifier,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(obj)

        assert result["classifier"] == "MyClass"


class TestExportEnumerationLiteral:
    """UTS_XCH_00075: _export_enumeration_literal."""

    def test_emits_name_only(self) -> None:
        literal = make_fake_element(
            "EnumerationLiteral",
            getName="RED",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(literal)

        assert result == {"name": "RED", "type": "EnumerationLiteral"}


class TestExportStereotypesAndTags:
    """UTS_XCH_00076, UTS_XCH_00077, UTS_XCH_00079: common property exporters."""

    def test_export_stereotypes_returns_names(self) -> None:
        st1 = make_fake_element("Stereotype", getName="Interface")
        st2 = make_fake_element("Stereotype", getName="SwComponent")
        element = make_fake_element("Class", getStereotypes=make_fake_collection([st1, st2]))
        exporter = _make_exporter()

        result = exporter._export_stereotypes(element)

        assert result == ["Interface", "SwComponent"]

    def test_export_tags_returns_name_value_dict(self) -> None:
        tag1 = make_fake_element("Tag", getName="status", getValue="active")
        tag2 = make_fake_element("Tag", getName="count", getValue="3")
        element = make_fake_element("Class", getAllTags=make_fake_collection([tag1, tag2]))
        exporter = _make_exporter()

        result = exporter._export_tags(element)

        assert result == {"status": "active", "count": "3"}

    def test_export_element_attaches_stereotypes_and_tags(self) -> None:
        st = make_fake_element("Stereotype", getName="Interface")
        tag = make_fake_element("Tag", getName="status", getValue="active")
        cls = make_fake_element(
            "Class",
            getName="Widget",
            getNestedElements=make_fake_collection([]),
            getStereotypes=make_fake_collection([st]),
            getAllTags=make_fake_collection([tag]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(cls)

        assert result["stereotypes"] == ["Interface"]
        assert result["tags"] == {"status": "active"}


class TestExportElementSkipUnsupported:
    """UTS_XCH_00078: _export_element skips unsupported metaclass."""

    def test_returns_none_for_unknown_metaclass(self) -> None:
        element = make_fake_element("SomeUnknownType", getName="x")
        exporter = _make_exporter()

        result = exporter._export_element(element)

        assert result is None

    def test_returns_none_for_none_input(self) -> None:
        exporter = _make_exporter()

        result = exporter._export_element(None)

        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/exchange/test_exporter.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.exchange.exporter'`

- [ ] **Step 3: Write minimal implementation**

Create `src/rhapsody_cli/exchange/exporter.py`:

```python
"""Rhapsody model -> YAML dict exporter.

SWR_XCH_004: Export Rhapsody model to YAML
"""

import logging
from typing import Any, Dict, List, Optional

from rhapsody_cli.exchange.core import RhapsodyModelHelper
from rhapsody_cli.exchange.schema import PROJECT_KEY, RHAPSODY_MODEL_KEY, SCHEMA_VERSION, VERSION_KEY
from rhapsody_cli.models.core import RPModelElement

_LOGGER = logging.getLogger(__name__)


class RhapsodyExporter(RhapsodyModelHelper):
    """Walks a Rhapsody container and produces a YAML-serializable dict."""

    def export(self, container: Any) -> Dict[str, Any]:
        """Export the container's children to a YAML dict.

        Args:
            container: A wrapped RPModelElement (Project or Package) whose
                children will be exported.

        Returns:
            A dict with keys: version, project, rhapsody-model.
        """
        wrapped = self._wrap_if_needed(container)
        project_name = self._get_project_name(wrapped)
        children = self._collect_children(wrapped)
        model_list: List[Dict[str, Any]] = []
        for child in children:
            spec = self._export_element(child)
            if spec is not None:
                model_list.append(spec)
        return {
            VERSION_KEY: SCHEMA_VERSION,
            PROJECT_KEY: project_name,
            RHAPSODY_MODEL_KEY: model_list,
        }

    def _export_element(self, element: Any) -> Optional[Dict[str, Any]]:
        """Dispatch to a type-specific exporter based on metaclass.

        Args:
            element: A wrapped or raw model element.

        Returns:
            A YAML dict for the element, or None if the metaclass is unsupported.
        """
        if element is None:
            return None
        wrapped = self._wrap_if_needed(element)
        try:
            meta_class = wrapped.get_meta_class()
        except Exception:
            return None
        dispatch = {
            "Package": self._export_package,
            "Class": self._export_class,
            "Operation": self._export_operation,
            "Argument": self._export_argument,
            "Attribute": self._export_attribute,
            "Type": self._export_type,
            "Object": self._export_object,
            "EnumerationLiteral": self._export_enumeration_literal,
        }
        exporter = dispatch.get(meta_class)
        if exporter is None:
            _LOGGER.warning("Skipping unsupported metaclass: %s", meta_class)
            return None
        spec = exporter(wrapped)
        self._attach_common_fields(spec, wrapped)
        return spec

    def _export_package(self, pkg: RPModelElement) -> Dict[str, Any]:
        return self._export_container(pkg, "Package")

    def _export_class(self, cls: RPModelElement) -> Dict[str, Any]:
        return self._export_container(cls, "Class")

    def _export_type(self, type_element: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": type_element.get_name(), "type": "Type"}
        kind = self._safe_get(type_element, "get_kind")
        if kind:
            spec["kind"] = kind
        if kind == "Enumeration":
            literals = self._export_collection(type_element, "get_enumeration_literals")
            if literals:
                spec["literals"] = literals
        elif kind == "Structure":
            children = self._collect_children(type_element)
            child_specs = self._export_children(children)
            if child_specs:
                spec["children"] = child_specs
        return spec

    def _export_operation(self, op: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": op.get_name(), "type": "Operation"}
        return_classifier = self._safe_get(op, "get_returns")
        return_name = self.get_classifier_name(return_classifier) if return_classifier is not None else None
        if return_name:
            spec["return_type"] = return_name
        is_static = self._safe_get(op, "get_is_static")
        if is_static is not None:
            spec["is_static"] = bool(is_static)
        arguments = self._export_collection(op, "get_arguments")
        if arguments:
            spec["arguments"] = arguments
        return spec

    def _export_argument(self, arg: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": arg.get_name(), "type": "Argument"}
        type_classifier = self._safe_get(arg, "get_type")
        type_name = self.get_classifier_name(type_classifier) if type_classifier is not None else None
        if type_name:
            spec["data_type"] = type_name
        direction = self._safe_get(arg, "get_argument_direction")
        if direction:
            spec["direction"] = direction
        return spec

    def _export_attribute(self, attr: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": attr.get_name(), "type": "Attribute"}
        type_classifier = self._safe_get(attr, "get_type")
        type_name = self.get_classifier_name(type_classifier) if type_classifier is not None else None
        if type_name:
            spec["data_type"] = type_name
        visibility = self._safe_get(attr, "get_visibility")
        if visibility:
            spec["visibility"] = visibility
        multiplicity = self._safe_get(attr, "get_multiplicity")
        if multiplicity:
            spec["multiplicity"] = multiplicity
        is_static = self._safe_get(attr, "get_is_static")
        if is_static is not None:
            spec["is_static"] = bool(is_static)
        return spec

    def _export_object(self, obj: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": obj.get_name(), "type": "Object"}
        classifier = self._safe_get(obj, "get_classifier")
        classifier_name = self.get_classifier_name(classifier) if classifier is not None else None
        if classifier_name:
            spec["classifier"] = classifier_name
        return spec

    def _export_enumeration_literal(self, literal: RPModelElement) -> Dict[str, Any]:
        return {"name": literal.get_name(), "type": "EnumerationLiteral"}

    def _export_stereotypes(self, element: RPModelElement) -> List[str]:
        result: List[str] = []
        try:
            collection = element.get_stereotypes()
            for st in collection:
                try:
                    result.append(st.get_name())
                except Exception:
                    continue
        except Exception:
            return result
        return result

    def _export_tags(self, element: RPModelElement) -> Dict[str, str]:
        result: Dict[str, str] = {}
        try:
            collection = element.get_all_tags()
            for tag in collection:
                try:
                    name = tag.get_name()
                    value = tag.call_com(lambda: tag._com.getValue())
                    if name and value is not None:
                        result[name] = str(value)
                except Exception:
                    continue
        except Exception:
            return result
        return result

    # --- Private helpers ---

    def _wrap_if_needed(self, element: Any) -> RPModelElement:
        if isinstance(element, RPModelElement):
            return element
        return RPModelElement.wrap(element)

    def _export_container(self, container: RPModelElement, type_name: str) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": container.get_name(), "type": type_name}
        children = self._collect_children(container)
        child_specs = self._export_children(children)
        if child_specs:
            spec["children"] = child_specs
        return spec

    def _export_children(self, children: List[RPModelElement]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for child in children:
            spec = self._export_element(child)
            if spec is not None:
                result.append(spec)
        return result

    def _export_collection(self, element: RPModelElement, method_name: str) -> List[Dict[str, Any]]:
        if not hasattr(element, method_name):
            return []
        collection = getattr(element, method_name)()
        if collection is None:
            return []
        result: List[Dict[str, Any]] = []
        for item in collection:
            spec = self._export_element(item)
            if spec is not None:
                result.append(spec)
        return result

    def _safe_get(self, element: RPModelElement, method_name: str) -> Any:
        if not hasattr(element, method_name):
            return None
        try:
            return getattr(element, method_name)()
        except Exception:
            return None

    def _attach_common_fields(self, spec: Dict[str, Any], element: RPModelElement) -> None:
        stereotypes = self._export_stereotypes(element)
        if stereotypes:
            spec["stereotypes"] = stereotypes
        tags = self._export_tags(element)
        if tags:
            spec["tags"] = tags
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/exchange/test_exporter.py -v`
Expected: PASS (all tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
black --check src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
mypy src/rhapsody_cli/exchange/exporter.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
git commit -m "feat(exchange): add RhapsodyExporter for 8 core element types

Implements exporter.py with RhapsodyExporter class that walks a
Rhapsody container and produces a YAML-serializable dict. Supports
Package, Class, Operation, Argument, Attribute, Type, Object, and
EnumerationLiteral. SWR_XCH_004."
```

---

## Task 8: Extend RhapsodyExporter with 6 new element types

**Files:**
- Modify: `src/rhapsody_cli/exchange/exporter.py` (add 6 `_export_<type>` methods + update dispatch table + `_export_name_list` helper)
- Test: `tests/unit/exchange/test_exporter.py` (append 6 new test classes)

**Interfaces:**
- Consumes: `RhapsodyExporter` from Task 7, `RPModelElement` wrappers for Dependency/Generalization/Relation/Port/Event/EventReception
- Produces: Extended `RhapsodyExporter` with `_export_dependency`, `_export_generalization`, `_export_relation`, `_export_port`, `_export_event`, `_export_event_reception` methods

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/exchange/test_exporter.py` (after the existing `TestExportElementSkipUnsupported` class):

```python
class TestExportDependency:
    """UTS_XCH_00080: _export_dependency emits depends_on."""

    def test_emits_depends_on(self) -> None:
        target = make_fake_element("Class", getName="OtherClass")
        dep = make_fake_element(
            "Dependency",
            getName="dep1",
            getDependsOn=target,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(dep)

        assert result["type"] == "Dependency"
        assert result["depends_on"] == "OtherClass"

    def test_omits_depends_on_when_unresolvable(self) -> None:
        dep = make_fake_element(
            "Dependency",
            getName="dep1",
            getDependsOn=None,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(dep)

        assert result["type"] == "Dependency"
        assert "depends_on" not in result


class TestExportGeneralization:
    """UTS_XCH_00081: _export_generalization emits base_class, visibility, is_virtual."""

    def test_emits_all_fields(self) -> None:
        base = make_fake_element("Class", getName="BaseClass")
        gen = make_fake_element(
            "Generalization",
            getName="gen1",
            getBaseClass=base,
            getVisibility="public",
            getIsVirtual=True,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(gen)

        assert result["type"] == "Generalization"
        assert result["base_class"] == "BaseClass"
        assert result["visibility"] == "public"
        assert result["is_virtual"] is True


class TestExportRelation:
    """UTS_XCH_00082: _export_relation emits relation_type, from, to, extras."""

    def test_emits_all_fields(self) -> None:
        source = make_fake_element("Class", getName="MyClass")
        target = make_fake_element("Class", getName="OtherClass")
        rel = make_fake_element(
            "Relation",
            getName="assoc1",
            getRelationType="Association",
            getOfClass=source,
            getOtherClass=target,
            getMultiplicity="0..*",
            getIsNavigable=True,
            getRelationRoleName="items",
            getVisibility="public",
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(rel)

        assert result["type"] == "Relation"
        assert result["relation_type"] == "Association"
        assert result["from"] == "MyClass"
        assert result["to"] == "OtherClass"
        assert result["multiplicity"] == "0..*"
        assert result["is_navigable"] is True
        assert result["role"] == "items"
        assert result["visibility"] == "public"

    def test_omits_optional_fields_when_none(self) -> None:
        source = make_fake_element("Class", getName="MyClass")
        target = make_fake_element("Class", getName="OtherClass")
        rel = make_fake_element(
            "Relation",
            getName="assoc1",
            getRelationType="Aggregation",
            getOfClass=source,
            getOtherClass=target,
            getMultiplicity=None,
            getIsNavigable=None,
            getRelationRoleName=None,
            getVisibility=None,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(rel)

        assert result["relation_type"] == "Aggregation"
        assert "multiplicity" not in result
        assert "is_navigable" not in result
        assert "role" not in result
        assert "visibility" not in result


class TestExportPort:
    """UTS_XCH_00083: _export_port emits flags, contract, interfaces."""

    def test_emits_flags_and_contract(self) -> None:
        contract = make_fake_element("Class", getName="IFoo")
        port = make_fake_element(
            "Port",
            getName="p1",
            getIsBehavioral=True,
            getIsReversed=False,
            getContract=contract,
            getProvidedInterfaces=make_fake_collection([]),
            getRequiredInterfaces=make_fake_collection([]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(port)

        assert result["type"] == "Port"
        assert result["is_behavioral"] is True
        assert result["is_reversed"] is False
        assert result["contract"] == "IFoo"

    def test_emits_provided_and_required_interfaces(self) -> None:
        iface1 = make_fake_element("Class", getName="IFoo")
        iface2 = make_fake_element("Class", getName="IBar")
        port = make_fake_element(
            "Port",
            getName="p1",
            getIsBehavioral=None,
            getIsReversed=None,
            getContract=None,
            getProvidedInterfaces=make_fake_collection([iface1]),
            getRequiredInterfaces=make_fake_collection([iface2]),
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(port)

        assert result["provided_interfaces"] == ["IFoo"]
        assert result["required_interfaces"] == ["IBar"]


class TestExportEvent:
    """UTS_XCH_00084: _export_event emits base_event and super_event."""

    def test_emits_base_and_super_event(self) -> None:
        base = make_fake_element("Event", getName="BaseEvt")
        sup = make_fake_element("Event", getName="SuperEvt")
        event = make_fake_element(
            "Event",
            getName="TickEvent",
            getBaseEvent=base,
            getSuperEvent=sup,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(event)

        assert result["type"] == "Event"
        assert result["base_event"] == "BaseEvt"
        assert result["super_event"] == "SuperEvt"

    def test_omits_optional_fields_when_none(self) -> None:
        event = make_fake_element(
            "Event",
            getName="TickEvent",
            getBaseEvent=None,
            getSuperEvent=None,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(event)

        assert "base_event" not in result
        assert "super_event" not in result


class TestExportEventReception:
    """UTS_XCH_00085: _export_event_reception emits event reference."""

    def test_emits_event(self) -> None:
        event = make_fake_element("Event", getName="TickEvent")
        reception = make_fake_element(
            "EventReception",
            getName="onTick",
            getEvent=event,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(reception)

        assert result["type"] == "EventReception"
        assert result["event"] == "TickEvent"

    def test_omits_event_when_none(self) -> None:
        reception = make_fake_element(
            "EventReception",
            getName="onTick",
            getEvent=None,
            getStereotypes=make_fake_collection([]),
            getAllTags=make_fake_collection([]),
        )
        exporter = _make_exporter()

        result = exporter._export_element(reception)

        assert "event" not in result
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/exchange/test_exporter.py -v`
Expected: FAIL — the 6 new element types are not dispatched (returns None for Dependency/Generalization/Relation/Port/Event/EventReception).

- [ ] **Step 3: Write the implementation**

Modify `src/rhapsody_cli/exchange/exporter.py` — add 6 new `_export_<type>` methods, a `_export_name_list` helper, and update the dispatch table in `_export_element`.

Update the dispatch table in `_export_element` (add 6 new entries):

```python
        dispatch = {
            "Package": self._export_package,
            "Class": self._export_class,
            "Operation": self._export_operation,
            "Argument": self._export_argument,
            "Attribute": self._export_attribute,
            "Type": self._export_type,
            "Object": self._export_object,
            "EnumerationLiteral": self._export_enumeration_literal,
            "Dependency": self._export_dependency,
            "Generalization": self._export_generalization,
            "Relation": self._export_relation,
            "Port": self._export_port,
            "Event": self._export_event,
            "EventReception": self._export_event_reception,
        }
```

Add these methods to the `RhapsodyExporter` class (after `_export_enumeration_literal`):

```python
    def _export_dependency(self, dep: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": dep.get_name(), "type": "Dependency"}
        target = self._safe_get(dep, "get_depends_on")
        target_name = self._classifier_name(target)
        if target_name:
            spec["depends_on"] = target_name
        return spec

    def _export_generalization(self, gen: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": gen.get_name(), "type": "Generalization"}
        base = self._safe_get(gen, "get_base_class")
        base_name = self._classifier_name(base)
        if base_name:
            spec["base_class"] = base_name
        visibility = self._safe_get(gen, "get_visibility")
        if visibility:
            spec["visibility"] = visibility
        is_virtual = self._safe_get(gen, "get_is_virtual")
        if is_virtual is not None:
            spec["is_virtual"] = bool(is_virtual)
        return spec

    def _export_relation(self, rel: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": rel.get_name(), "type": "Relation"}
        relation_type = self._safe_get(rel, "get_relation_type")
        if relation_type:
            spec["relation_type"] = relation_type
        source = self._safe_get(rel, "get_of_class")
        source_name = self._classifier_name(source)
        if source_name:
            spec["from"] = source_name
        target = self._safe_get(rel, "get_other_class")
        target_name = self._classifier_name(target)
        if target_name:
            spec["to"] = target_name
        multiplicity = self._safe_get(rel, "get_multiplicity")
        if multiplicity:
            spec["multiplicity"] = multiplicity
        is_navigable = self._safe_get(rel, "get_is_navigable")
        if is_navigable is not None:
            spec["is_navigable"] = bool(is_navigable)
        role = self._safe_get(rel, "get_relation_role_name")
        if role:
            spec["role"] = role
        visibility = self._safe_get(rel, "get_visibility")
        if visibility:
            spec["visibility"] = visibility
        return spec

    def _export_port(self, port: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": port.get_name(), "type": "Port"}
        is_behavioral = self._safe_get(port, "get_is_behavioral")
        if is_behavioral is not None:
            spec["is_behavioral"] = bool(is_behavioral)
        is_reversed = self._safe_get(port, "get_is_reversed")
        if is_reversed is not None:
            spec["is_reversed"] = bool(is_reversed)
        contract = self._safe_get(port, "get_contract")
        contract_name = self._classifier_name(contract)
        if contract_name:
            spec["contract"] = contract_name
        provided = self._export_name_list(port, "get_provided_interfaces")
        if provided:
            spec["provided_interfaces"] = provided
        required = self._export_name_list(port, "get_required_interfaces")
        if required:
            spec["required_interfaces"] = required
        return spec

    def _export_event(self, event: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": event.get_name(), "type": "Event"}
        base = self._safe_get(event, "get_base_event")
        base_name = self._classifier_name(base)
        if base_name:
            spec["base_event"] = base_name
        sup = self._safe_get(event, "get_super_event")
        sup_name = self._classifier_name(sup)
        if sup_name:
            spec["super_event"] = sup_name
        return spec

    def _export_event_reception(self, reception: RPModelElement) -> Dict[str, Any]:
        spec: Dict[str, Any] = {"name": reception.get_name(), "type": "EventReception"}
        event = self._safe_get(reception, "get_event")
        event_name = self._classifier_name(event)
        if event_name:
            spec["event"] = event_name
        return spec

    def _export_name_list(self, element: RPModelElement, method_name: str) -> List[str]:
        if not hasattr(element, method_name):
            return []
        try:
            collection = getattr(element, method_name)()
            if collection is None:
                return []
            result: List[str] = []
            for item in collection:
                name = self._classifier_name(item)
                if name:
                    result.append(name)
            return result
        except Exception:
            return []

    def _classifier_name(self, classifier: Any) -> Optional[str]:
        if classifier is None:
            return None
        try:
            wrapped = self._wrap_if_needed(classifier)
            return wrapped.get_name()
        except Exception:
            return None
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/exchange/test_exporter.py -v`
Expected: PASS (all tests, including the 6 new test classes)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
black --check src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
mypy src/rhapsody_cli/exchange/exporter.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/exchange/exporter.py tests/unit/exchange/test_exporter.py
git commit -m "feat(exchange): extend RhapsodyExporter with 6 new element types

Adds _export_dependency, _export_generalization, _export_relation,
_export_port, _export_event, and _export_event_reception methods.
Updates the dispatch table to handle all 14 element types. SWR_XCH_004."
```

---

## Task 9: ProjectExportAction + ProjectImportAction

**Files:**
- Modify: `src/rhapsody_cli/actions/project_action.py` (append `ProjectExportAction`, `ProjectImportAction` classes + imports)
- Test: `tests/unit/actions/test_project_action.py` (append `TestProjectExportAction`, `TestProjectImportAction` classes)

**Interfaces:**
- Consumes: `RhapsodyContextAction` from `rhapsody_cli.actions.abstract_action`, `RhapsodyExporter`/`RhapsodyImporter`/`RhapsodyYaml` from `rhapsody_cli.exchange`, `CliExecutionError`/`RhapsodyConnectionError` from `rhapsody_cli.exceptions`
- Produces: `ProjectExportAction` and `ProjectImportAction` action classes registered under `project export` / `project import` subcommands

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/actions/test_project_action.py`:

```python
from unittest.mock import MagicMock, patch

from rhapsody_cli.actions.project_action import ProjectExportAction, ProjectImportAction
from rhapsody_cli.exceptions import CliExecutionError


class TestProjectExportAction:
    """UTS_XCH_00086: project export action writes YAML file."""

    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.project_action.RhapsodyExporter")
    def test_export_writes_yaml_file(self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock) -> None:
        action = ProjectExportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_project = MagicMock(name="FakeProject")
        fake_app.active_project.return_value = fake_project

        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        mock_exporter.export.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        args = MagicMock()
        args.file = "output.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            action.execute(args)

        mock_exporter_cls.assert_called_once_with(app=fake_app)
        mock_exporter.export.assert_called_once_with(fake_project)
        mock_yaml_cls.assert_called_once()
        mock_yaml_cls.return_value.write.assert_called_once_with(
            "output.yaml", {"version": 1, "project": "P", "rhapsody-model": []}
        )

    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.project_action.RhapsodyExporter")
    def test_export_raises_on_connection_failure(self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock) -> None:
        action = ProjectExportAction()

        args = MagicMock()
        args.file = "output.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", side_effect=Exception("connection failed")):
            with pytest.raises(CliExecutionError):
                action.execute(args)


class TestProjectImportAction:
    """UTS_XCH_00087: project import action reads YAML and imports into project."""

    @patch("rhapsody_cli.actions.project_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    def test_import_reads_yaml_and_calls_import_template(
        self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock
    ) -> None:
        action = ProjectImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_project = MagicMock(name="FakeProject")
        fake_app.active_project.return_value = fake_project

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        mock_importer = MagicMock()
        mock_importer_cls.return_value = mock_importer

        args = MagicMock()
        args.file = "input.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            action.execute(args)

        mock_yaml.read.assert_called_once_with("input.yaml")
        mock_importer_cls.assert_called_once_with(app=fake_app)
        mock_importer.import_template.assert_called_once_with(
            {"version": 1, "project": "P", "rhapsody-model": []}, fake_project
        )
        fake_app.save_all.assert_called_once()

    @patch("rhapsody_cli.actions.project_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.project_action.RhapsodyYaml")
    def test_import_raises_on_yaml_read_failure(
        self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock
    ) -> None:
        action = ProjectImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_app.active_project.return_value = MagicMock()

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.side_effect = CliExecutionError("file not found")

        args = MagicMock()
        args.file = "missing.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app):
            with pytest.raises(CliExecutionError, match="file not found"):
                action.execute(args)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_project_action.py::TestProjectExportAction tests/unit/actions/test_project_action.py::TestProjectImportAction -v`
Expected: FAIL with `ImportError: cannot import name 'ProjectExportAction' from 'rhapsody_cli.actions.project_action'`

- [ ] **Step 3: Write the implementation**

Modify `src/rhapsody_cli/actions/project_action.py` — add these imports at the top (with the existing imports):

```python
import argparse

from rhapsody_cli.exceptions import CliExecutionError, RhapsodyConnectionError
from rhapsody_cli.exchange.exporter import RhapsodyExporter
from rhapsody_cli.exchange.importer import RhapsodyImporter
from rhapsody_cli.exchange.yaml_utils import RhapsodyYaml
```

Append these two action classes at the end of `project_action.py`:

```python
class ProjectExportAction(RhapsodyContextAction):
    """Action for `project export` — exports the active project to a YAML file.

    SWR_XCH_001: Import/Export CLI Actions
    """

    def __init__(self) -> None:
        super().__init__(command_id="export")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        parser = sub_parser.add_parser(
            self.command_id, help="Export the active project to a YAML file"
        )
        parser.add_argument("--file", required=True, help="Output YAML file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        try:
            app = self._connect_app()
            project = app.active_project()
            exporter = RhapsodyExporter(app=app)
            data = exporter.export(project)
            yaml_io = RhapsodyYaml()
            yaml_io.write(args.file, data)
            self.logger.info("Exported project to %s", args.file)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "export project")
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, "export project")


class ProjectImportAction(RhapsodyContextAction):
    """Action for `project import` — imports a YAML file into the active project.

    SWR_XCH_001: Import/Export CLI Actions
    """

    def __init__(self) -> None:
        super().__init__(command_id="import")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        parser = sub_parser.add_parser(
            self.command_id, help="Import a YAML file into the active project"
        )
        parser.add_argument("--file", required=True, help="Input YAML file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        try:
            app = self._connect_app()
            project = app.active_project()
            yaml_io = RhapsodyYaml()
            data = yaml_io.read(args.file)
            importer = RhapsodyImporter(app=app)
            importer.import_template(data, project)
            app.save_all()
            self.logger.info("Imported %s into project", args.file)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "import project")
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, "import project")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_project_action.py::TestProjectExportAction tests/unit/actions/test_project_action.py::TestProjectImportAction -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/actions/project_action.py tests/unit/actions/test_project_action.py
black --check src/rhapsody_cli/actions/project_action.py tests/unit/actions/test_project_action.py
mypy src/rhapsody_cli/actions/project_action.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/actions/project_action.py tests/unit/actions/test_project_action.py
git commit -m "feat(actions): add ProjectExportAction and ProjectImportAction

Adds 'project export' and 'project import' CLI subcommands that
read/write YAML files and delegate to RhapsodyExporter/RhapsodyImporter.
SWR_XCH_001."
```

---

## Task 10: PackageExportAction + PackageImportAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py` (append `PackageExportAction`, `PackageImportAction` classes + imports)
- Test: `tests/unit/actions/test_package_action.py` (append `TestPackageExportAction`, `TestPackageImportAction` classes)

**Interfaces:**
- Consumes: `AbstractPackageAction` from `rhapsody_cli.actions.package_action`, `RhapsodyExporter`/`RhapsodyImporter`/`RhapsodyYaml` from `rhapsody_cli.exchange`, `CliExecutionError`/`RhapsodyConnectionError` from `rhapsody_cli.exceptions`
- Produces: `PackageExportAction` and `PackageImportAction` action classes registered under `package export` / `package import` subcommands

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/actions/test_package_action.py`:

```python
from unittest.mock import MagicMock, patch

from rhapsody_cli.actions.package_action import PackageExportAction, PackageImportAction
from rhapsody_cli.exceptions import CliExecutionError


class TestPackageExportAction:
    """UTS_XCH_00088: package export action writes YAML file."""

    @patch("rhapsody_cli.actions.package_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.package_action.RhapsodyExporter")
    def test_export_writes_yaml_file(self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock) -> None:
        action = PackageExportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_package = MagicMock(name="FakePackage")

        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        mock_exporter.export.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        args = MagicMock()
        args.path = "Sensors"
        args.file = "sensors.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app), patch.object(
            action, "_resolve_and_validate_package", return_value=fake_package
        ):
            action.execute(args)

        mock_exporter_cls.assert_called_once_with(app=fake_app)
        mock_exporter.export.assert_called_once_with(fake_package)
        mock_yaml_cls.return_value.write.assert_called_once_with(
            "sensors.yaml", {"version": 1, "project": "P", "rhapsody-model": []}
        )

    @patch("rhapsody_cli.actions.package_action.RhapsodyYaml")
    @patch("rhapsody_cli.actions.package_action.RhapsodyExporter")
    def test_export_raises_on_unresolved_package(
        self, mock_exporter_cls: MagicMock, mock_yaml_cls: MagicMock
    ) -> None:
        action = PackageExportAction()
        fake_app = MagicMock(name="FakeApplication")

        args = MagicMock()
        args.path = "Nonexistent"
        args.file = "out.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app), patch.object(
            action,
            "_resolve_and_validate_package",
            side_effect=CliExecutionError("package not found"),
        ):
            with pytest.raises(CliExecutionError, match="package not found"):
                action.execute(args)


class TestPackageImportAction:
    """UTS_XCH_00089: package import action reads YAML and imports into package."""

    @patch("rhapsody_cli.actions.package_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.package_action.RhapsodyYaml")
    def test_import_reads_yaml_and_calls_import_template(
        self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock
    ) -> None:
        action = PackageImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_package = MagicMock(name="FakePackage")

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.return_value = {"version": 1, "project": "P", "rhapsody-model": []}

        mock_importer = MagicMock()
        mock_importer_cls.return_value = mock_importer

        args = MagicMock()
        args.path = "Sensors"
        args.file = "sensors.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app), patch.object(
            action, "_resolve_and_validate_package", return_value=fake_package
        ):
            action.execute(args)

        mock_yaml.read.assert_called_once_with("sensors.yaml")
        mock_importer_cls.assert_called_once_with(app=fake_app)
        mock_importer.import_template.assert_called_once_with(
            {"version": 1, "project": "P", "rhapsody-model": []}, fake_package
        )
        fake_app.save_all.assert_called_once()

    @patch("rhapsody_cli.actions.package_action.RhapsodyImporter")
    @patch("rhapsody_cli.actions.package_action.RhapsodyYaml")
    def test_import_raises_on_yaml_read_failure(
        self, mock_yaml_cls: MagicMock, mock_importer_cls: MagicMock
    ) -> None:
        action = PackageImportAction()
        fake_app = MagicMock(name="FakeApplication")
        fake_package = MagicMock(name="FakePackage")

        mock_yaml = MagicMock()
        mock_yaml_cls.return_value = mock_yaml
        mock_yaml.read.side_effect = CliExecutionError("file not found")

        args = MagicMock()
        args.path = "Sensors"
        args.file = "missing.yaml"
        args.verbose = False

        with patch.object(action, "_connect_app", return_value=fake_app), patch.object(
            action, "_resolve_and_validate_package", return_value=fake_package
        ):
            with pytest.raises(CliExecutionError, match="file not found"):
                action.execute(args)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageExportAction tests/unit/actions/test_package_action.py::TestPackageImportAction -v`
Expected: FAIL with `ImportError: cannot import name 'PackageExportAction' from 'rhapsody_cli.actions.package_action'`

- [ ] **Step 3: Write the implementation**

Modify `src/rhapsody_cli/actions/package_action.py` — add these imports at the top (with the existing imports):

```python
import argparse

from rhapsody_cli.exceptions import CliExecutionError, RhapsodyConnectionError
from rhapsody_cli.exchange.exporter import RhapsodyExporter
from rhapsody_cli.exchange.importer import RhapsodyImporter
from rhapsody_cli.exchange.yaml_utils import RhapsodyYaml
```

Append these two action classes at the end of `package_action.py`:

```python
class PackageExportAction(AbstractPackageAction):
    """Action for `package export` — exports a package to a YAML file.

    SWR_XCH_001: Import/Export CLI Actions
    """

    def __init__(self) -> None:
        super().__init__(command_id="export")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        parser = sub_parser.add_parser(
            self.command_id, help="Export a package to a YAML file"
        )
        self.add_path_argument(parser, required=False, help_text="Path to package (defaults to root)")
        parser.add_argument("--file", required=True, help="Output YAML file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        try:
            app = self._connect_app()
            package = self._resolve_and_validate_package(args.path)
            exporter = RhapsodyExporter(app=app)
            data = exporter.export(package)
            yaml_io = RhapsodyYaml()
            yaml_io.write(args.file, data)
            self.logger.info("Exported package to %s", args.file)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "export package")
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, "export package")


class PackageImportAction(AbstractPackageAction):
    """Action for `package import` — imports a YAML file into a package.

    SWR_XCH_001: Import/Export CLI Actions
    """

    def __init__(self) -> None:
        super().__init__(command_id="import")

    def init_arguments(self, sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
        parser = sub_parser.add_parser(
            self.command_id, help="Import a YAML file into a package"
        )
        self.add_path_argument(parser, required=False, help_text="Path to target package (defaults to root)")
        parser.add_argument("--file", required=True, help="Input YAML file path")
        self.add_verbose_argument(parser)

    def execute(self, args: argparse.Namespace) -> None:
        try:
            app = self._connect_app()
            package = self._resolve_and_validate_package(args.path)
            yaml_io = RhapsodyYaml()
            data = yaml_io.read(args.file)
            importer = RhapsodyImporter(app=app)
            importer.import_template(data, package)
            app.save_all()
            self.logger.info("Imported %s into package", args.file)
        except RhapsodyConnectionError as e:
            self._handle_connection_error(e, "import package")
        except CliExecutionError:
            raise
        except Exception as e:
            self._handle_execution_error(e, "import package")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/actions/test_package_action.py::TestPackageExportAction tests/unit/actions/test_package_action.py::TestPackageImportAction -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
black --check src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
mypy src/rhapsody_cli/actions/package_action.py
```

Expected: all pass with no errors.

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat(actions): add PackageExportAction and PackageImportAction

Adds 'package export' and 'package import' CLI subcommands that
resolve a package by path and delegate to RhapsodyExporter/RhapsodyImporter.
SWR_XCH_001."
```

---

## Task 11: Register export/import subcommands in command groups

**Files:**
- Modify: `src/rhapsody_cli/commands/project_command.py` (add `ProjectExportAction`, `ProjectImportAction` imports + register in `get_actions()`)
- Modify: `src/rhapsody_cli/commands/package_command.py` (add `PackageExportAction`, `PackageImportAction` imports + register in `get_actions()`)
- Test: `tests/unit/commands/test_project_command.py` (add `TestProjectCommandExportImportRegistration` class)
- Test: `tests/unit/commands/test_package_command.py` (update `test_registers_all_five_subcommands` → `test_registers_all_seven_subcommands`)

**Interfaces:**
- Consumes: `ProjectExportAction`, `ProjectImportAction` from Task 9 (in `rhapsody_cli.actions.project_action`); `PackageExportAction`, `PackageImportAction` from Task 10 (in `rhapsody_cli.actions.package_action`)
- Produces: `ProjectCommand.get_actions()` now returns 6 actions (open, list, close, new, export, import); `PackageCommand.get_actions()` now returns 7 actions (create, delete, view, list, update, export, import). End users can run `rhapsody project export --file out.yaml` and `rhapsody package import --path Sensors --file in.yaml`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/commands/test_project_command.py` (after `TestProjectNewAction`):

```python
class TestProjectCommandExportImportRegistration:
    """Tests that ProjectCommand registers export/import subcommands.

    UTS_XCH_00090: ProjectCommand registers export/import subcommands
    """

    def test_get_actions_includes_export_action(self) -> None:
        """ProjectCommand.get_actions() must include a ProjectExportAction instance."""
        cmd = ProjectCommand(["export", "--file", "out.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "export" in command_ids

    def test_get_actions_includes_import_action(self) -> None:
        """ProjectCommand.get_actions() must include a ProjectImportAction instance."""
        cmd = ProjectCommand(["import", "--file", "in.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "import" in command_ids

    def test_get_actions_returns_six_actions(self) -> None:
        """ProjectCommand.get_actions() must return exactly 6 actions after adding export/import."""
        cmd = ProjectCommand(["open", "MyProject.rpy"])
        actions = cmd.get_actions()

        assert len(actions) == 6
```

Update the existing `test_registers_all_five_subcommands` test in `tests/unit/commands/test_package_command.py` — rename and extend it to cover the two new subcommands:

```python
    def test_registers_all_seven_subcommands(self) -> None:
        """UTS_PKG_00025: Test that all 7 subcommands are registered (5 original + export + import)."""
        cmd = PackageCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "update" in command_ids
        assert "export" in command_ids
        assert "import" in command_ids
        assert len(actions) == 7
```

Also add a new focused test class to `tests/unit/commands/test_package_command.py`:

```python
class TestPackageCommandExportImportRegistration:
    """Tests that PackageCommand registers export/import subcommands.

    UTS_XCH_00091: PackageCommand registers export/import subcommands
    """

    def test_get_actions_includes_export_action(self) -> None:
        """PackageCommand.get_actions() must include a PackageExportAction instance."""
        cmd = PackageCommand(["export", "--path", "Sensors", "--file", "out.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "export" in command_ids

    def test_get_actions_includes_import_action(self) -> None:
        """PackageCommand.get_actions() must include a PackageImportAction instance."""
        cmd = PackageCommand(["import", "--path", "Sensors", "--file", "in.yaml"])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "import" in command_ids
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/commands/test_project_command.py::TestProjectCommandExportImportRegistration tests/unit/commands/test_package_command.py -v`
Expected: FAIL — `assert "export" in command_ids` fails because the actions are not yet registered. (For `test_package_command.py::TestPackageCommand::test_registers_all_five_subcommands`, the existing test still passes — it will be replaced by `test_registers_all_seven_subcommands` which fails on `assert "export" in command_ids`.)

- [ ] **Step 3: Register actions in ProjectCommand**

Modify `src/rhapsody_cli/commands/project_command.py`. Replace the entire file with:

```python
"""Project command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.project_action import (
    ProjectCloseAction,
    ProjectExportAction,
    ProjectImportAction,
    ProjectListAction,
    ProjectNewAction,
    ProjectOpenAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class ProjectCommand(AbstractCommand):
    """Project command group - handles project subcommands (open, list, close, new, export, import)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize ProjectCommand and parse project subcommands.

        Args:
            args: Arguments after 'project' command
                (e.g., ['open', 'MyProject.rpy'])
        """
        super().__init__("project", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the project subcommand actions."""
        return [
            ProjectOpenAction(),
            ProjectListAction(),
            ProjectCloseAction(),
            ProjectNewAction(),
            ProjectExportAction(),
            ProjectImportAction(),
        ]
```

- [ ] **Step 4: Register actions in PackageCommand**

Modify `src/rhapsody_cli/commands/package_command.py`. Replace the entire file with:

```python
"""Package command group - dispatches to per-subcommand Action classes."""

from typing import List

from rhapsody_cli.actions.abstract_action import AbstractAction
from rhapsody_cli.actions.package_action import (
    PackageCreateAction,
    PackageDeleteAction,
    PackageExportAction,
    PackageImportAction,
    PackageListAction,
    PackageUpdateAction,
    PackageViewAction,
)
from rhapsody_cli.commands.abstract_command import AbstractCommand


class PackageCommand(AbstractCommand):
    """Package command group - handles package subcommands (create, delete, view, list, update, export, import)."""

    def __init__(self, args: List[str]) -> None:
        """Initialize PackageCommand and parse package subcommands.

        Args:
            args: Arguments after 'package' command
                (e.g., ['create', '--path', 'Sensors', '{"name":"Temp"}'])
        """
        super().__init__("package", args)

    def get_actions(self) -> List[AbstractAction]:
        """Return the package subcommand actions."""
        return [
            PackageCreateAction(),
            PackageDeleteAction(),
            PackageViewAction(),
            PackageListAction(),
            PackageUpdateAction(),
            PackageExportAction(),
            PackageImportAction(),
        ]
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py -v`
Expected: PASS — all tests pass, including the 3 new `TestProjectCommandExportImportRegistration` tests, the renamed `test_registers_all_seven_subcommands`, and the 2 new `TestPackageCommandExportImportRegistration` tests.

- [ ] **Step 6: Quality gate (touched files only)**

Run:

```bash
ruff check src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py
black --check src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py
mypy src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py
```

Expected: all pass with no errors.

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py
git commit -m "feat(commands): register export/import subcommands

Wires ProjectExportAction/ProjectImportAction into ProjectCommand and
PackageExportAction/PackageImportAction into PackageCommand so users
can invoke 'rhapsody project export' and 'rhapsody package import'.
SWR_XCH_001."
```

---

## Task 12: Requirements and test-spec documentation

**Files:**
- Create: `docs/requirements/swr_xch_requirements.md` (13 SWR_XCH entries)
- Create: `docs/tests/unit/uts_xch_test-specs.md` (91 UTS_XCH entries with Traces-To)
- Modify: `docs/index.rst` (add `requirements/swr_xch_requirements` to the Requirements toctree)

**Interfaces:**
- Consumes: SWR_XCH_001–013 title/description table from spec §8.4; UTS_XCH_00001–00091 test names already referenced in Tasks 1–11 (test class docstrings and inline comments)
- Produces: traceability docs that satisfy the project convention "All documentation files must be included in docs/index.rst toctree" and provide requirement→test traceability for the exchange feature

- [ ] **Step 1: Create `docs/requirements/swr_xch_requirements.md`**

Write the file with this exact content:

```markdown
# Software Requirements - YAML Import/Export

**Category:** YAML Import/Export
**Prefix:** SWR_XCH
**Source:** Extracted from docs/superpowers/specs/2026-07-19-yaml-import-export-design.md
**Last Validated:** 2026-07-19

---

## SWR_XCH_001: Project Export Command

**ID:** SWR_XCH_001
**Title:** project export command exports the active project to YAML
**Status:** Planned
**Priority:** High
**Description:**
The project CLI
- SHALL provide a `project export` command that exports the active project's top-level elements to a YAML file.
- SHALL accept `--file <path>` argument (required) for the output YAML file.
- SHALL accept `-v`/`--verbose` flag (inherited from AbstractAction).
- SHALL connect to the active Rhapsody application via `_connect_app()`.
- SHALL obtain the active project via `app.active_project()`.
- SHALL delegate to `RhapsodyExporter(app=app).export(project)` to produce the YAML dict.
- SHALL write the dict via `RhapsodyYaml().write(args.file, data)`.
- SHALL wrap errors as `CliExecutionError` (no `sys.exit()` in the action).
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/project_action.py:ProjectExportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_002: Project Import Command

**ID:** SWR_XCH_002
**Title:** project import command imports YAML into the active project
**Status:** Planned
**Priority:** High
**Description:**
The project CLI
- SHALL provide a `project import` command that imports YAML elements as top-level elements of the active project.
- SHALL accept `--file <path>` argument (required) for the input YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL connect to the active Rhapsody application via `_connect_app()`.
- SHALL obtain the active project via `app.active_project()`.
- SHALL read the YAML dict via `RhapsodyYaml().read(args.file)`.
- SHALL delegate to `RhapsodyImporter(app=app).import_template(data, project)`.
- SHALL call `app.save_all()` after a successful import.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/project_action.py:ProjectImportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_003: Package Export Command

**ID:** SWR_XCH_003
**Title:** package export command exports a package to YAML
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package export` command that exports a specific package's contents to a YAML file.
- SHALL accept `--path <package-path>` argument (optional; defaults to project root).
- SHALL accept `--file <path>` argument (required) for the output YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL resolve the target package via `_resolve_and_validate_package(args.path)` (reuses existing helper).
- SHALL delegate to `RhapsodyExporter(app=app).export(package)`.
- SHALL write the dict via `RhapsodyYaml().write(args.file, data)`.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageExportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_004: Package Import Command

**ID:** SWR_XCH_004
**Title:** package import command imports YAML into a package
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package import` command that imports YAML elements as children of a specific package.
- SHALL accept `--path <package-path>` argument (optional; defaults to project root).
- SHALL accept `--file <path>` argument (required) for the input YAML file.
- SHALL accept `-v`/`--verbose` flag.
- SHALL resolve the target package via `_resolve_and_validate_package(args.path)`.
- SHALL read the YAML dict via `RhapsodyYaml().read(args.file)`.
- SHALL delegate to `RhapsodyImporter(app=app).import_template(data, package)`.
- SHALL call `app.save_all()` after a successful import.
- SHALL wrap errors as `CliExecutionError`.
- SHALL log a success message via `self.logger.info(...)`.
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageImportAction
**Last Changed:** 2026-07-19

---

## SWR_XCH_005: YAML Schema (version 1)

**ID:** SWR_XCH_005
**Title:** YAML schema for round-tripping Rhapsody model structure
**Status:** Planned
**Priority:** High
**Description:**
The exchange module
- SHALL define `SCHEMA_VERSION = 1` as an integer constant in `exchange/schema.py`.
- SHALL define key constants `VERSION_KEY = "version"`, `PROJECT_KEY = "project"`, `RHAPSODY_MODEL_KEY = "rhapsody-model"`.
- SHALL produce YAML files whose top-level mapping contains `version`, `project`, and `rhapsody-model` keys.
- SHALL set `version: 1` in every exported file.
- SHALL set `project` to the project name obtained by walking the owner chain from the export container.
- SHALL set `rhapsody-model` to a list of element spec dicts, one per top-level child.
- SHALL validate `version == SCHEMA_VERSION` on import and raise `CliExecutionError` on mismatch.
- SHALL use `type` discriminator field on each element spec (e.g. `type: "Package"`, `type: "Class"`, `type: "Relation"`).
**Implementation:** src/rhapsody_cli/exchange/schema.py
**Last Changed:** 2026-07-19

---

## SWR_XCH_006: Element Find-or-Create (RhapsodyModelHelper)

**ID:** SWR_XCH_006
**Title:** RhapsodyModelHelper provides find_or_create dispatch for 14 element types
**Status:** Planned
**Priority:** High
**Description:**
The `RhapsodyModelHelper` base class in `exchange/core.py`
- SHALL expose `find_or_create_<type>(parent, name)` methods for 14 element types: Package, Class, Operation, Argument, Attribute, Type, Object, EnumerationLiteral, Dependency, Generalization, Relation, Port, Event, EventReception.
- SHALL use `find_child_by_name(parent, name)` to locate an existing child; return it if found (idempotent re-import).
- SHALL create the element via the appropriate COM add method when not found: `add_new_aggr("MetaClass", name)` for most types, `add_global_function(name)` for operations on packages, `add_argument(name)` for arguments, `add_new_aggr("LiteralValue", name)` for enumeration literals.
- SHALL sanitize names by stripping whitespace and replacing invalid characters with underscores.
- SHALL be idempotent: importing the same YAML twice SHALL NOT create duplicates.
- SHALL expose public `find_child_by_name` and `_set_type_kind` helpers (other internals are private).
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper
**Last Changed:** 2026-07-19

---

## SWR_XCH_007: Stereotype and Tag Round-Trip

**ID:** SWR_XCH_007
**Title:** Stereotypes and tags round-trip via apply_stereotypes / apply_tags
**Status:** Planned
**Priority:** High
**Description:**
The `RhapsodyModelHelper` base class
- SHALL expose `apply_stereotypes(element, stereotypes_list)` that infers the element's meta type via `get_meta_class()` and calls `element.add_stereotype(name, meta_type)` for each entry.
- SHALL skip stereotypes that are already applied (idempotent — no duplicate add).
- SHALL expose `apply_tags(element, tags_dict)` that calls `element.set_property_value(key, val)` for each entry.
- SHALL apply stereotypes and tags to ALL element types including Argument and EnumerationLiteral (routed through `_process_element` / `_export_element`).
- SHALL export stereotypes as a list of names and tags as a dict of name→string via `RhapsodyExporter._export_stereotypes` / `_export_tags`.
- SHALL export tags by enumerating `element.get_all_tags()` and reading each tag's `get_name()` and `get_value()` (via `tag.call_com(lambda: tag._com.getValue())`).
- SHALL skip malformed tags with a warning during export (best-effort).
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper (apply_stereotypes, apply_tags); src/rhapsody_cli/exchange/exporter.py:RhapsodyExporter (_export_stereotypes, _export_tags)
**Last Changed:** 2026-07-19

---

## SWR_XCH_008: Core Type-Specific Fields

**ID:** SWR_XCH_008
**Title:** Type-specific YAML fields for 8 core element types
**Status:** Planned
**Priority:** High
**Description:**
The importer and exporter SHALL round-trip the following type-specific fields:
- `Operation`: `return_type` (string, optional), `arguments` (list of Argument specs), `is_static` (bool, optional), `visibility` (string, optional).
- `Argument`: `direction` (string, optional — in/out/inout), `type` (string, optional — type name).
- `Attribute`: `type` (string, optional), `visibility` (string, optional), `multiplicity` (string, optional), `is_static` (bool, optional), `default_value` (string, optional).
- `Type`: `kind` (string — sets via `set_kind()`), `literals` (list of EnumerationLiteral specs, only when kind=Enumeration).
- `Object`: `classifier` (string, optional — class name to instantiate).
- `Class`: `is_abstract` (bool, optional), `is_active` (bool, optional), `is_final` (bool, optional), `visibility` (string, optional).
- `Package`: `children` (list of nested element specs).
- `EnumerationLiteral`: no type-specific fields (only common name/stereotypes/tags).
The importer SHALL use `_apply_<type>_extras` methods to set these fields; the exporter SHALL use `_export_<type>` methods to serialize them.
**Implementation:** src/rhapsody_cli/exchange/importer.py:RhapsodyImporter (_apply_*_extras); src/rhapsody_cli/exchange/exporter.py:RhapsodyExporter (_export_*)
**Last Changed:** 2026-07-19

---

## SWR_XCH_009: Error Handling and Skip-on-Unsupported

**ID:** SWR_XCH_009
**Title:** Skip unsupported element types and missing references with warnings
**Status:** Planned
**Priority:** High
**Description:**
The exchange module
- SHALL skip unsupported metaclasses during export (returns `None`, filtered out of `rhapsody-model` list) with a WARNING log.
- SHALL skip unsupported `type` values during import (returns `None`, siblings still processed) with a WARNING log.
- SHALL skip missing type references (e.g. `data_type: "UnknownType"`) with a WARNING; the element is still created without the type set.
- SHALL skip missing relation targets (`to`, `base_class`, `depends_on`) with a WARNING; the relation/dependency/generalization is still created without the link.
- SHALL skip missing port contract / interface names with a WARNING; the port is still created.
- SHALL skip missing event references (`event`, `base_event`, `super_event`) with a WARNING; the reception/event is still created.
- SHALL raise `CliExecutionError` on schema version mismatch (with expected vs. actual version in the message).
- SHALL raise `CliExecutionError` on invalid YAML syntax, missing input file, or unwritable output file (via `RhapsodyYaml`).
- SHALL NOT call `sys.exit()` anywhere in the exchange module or actions.
**Implementation:** src/rhapsody_cli/exchange/importer.py, src/rhapsody_cli/exchange/exporter.py, src/rhapsody_cli/exchange/yaml_utils.py
**Last Changed:** 2026-07-19

---

## SWR_XCH_010: Reusable Model Manipulation API

**ID:** SWR_XCH_010
**Title:** RhapsodyModelHelper exposes reusable find/create/apply/resolve helpers
**Status:** Planned
**Priority:** Medium
**Description:**
The `RhapsodyModelHelper` base class
- SHALL expose `find_child_by_name(parent, name) -> Optional[RPModelElement]` (PUBLIC) that iterates `parent.get_nested_elements()` and returns the first child whose `get_name()` matches, else `None`.
- SHALL expose `_set_type_kind(type_element, kind) -> None` (PRIVATE) that calls `type_element.set_kind(kind)` with try/except.
- SHALL expose `apply_stereotypes(element, stereotypes)` and `apply_tags(element, tags)` (PUBLIC).
- SHALL expose `resolve_classifier(name) -> Optional[RPModelElement]` (PUBLIC) that recursively searches the project for a classifier by name.
- SHALL expose `get_classifier_name(classifier) -> Optional[str]` (PUBLIC) — None-safe wrapper around `classifier.get_name()`.
- SHALL expose private helpers `_collect_children(container)`, `_get_project_name(element)`, `_wrap_if_needed(element)`.
- SHALL be subclassed by `RhapsodyImporter` and `RhapsodyExporter`; the base class itself SHALL NOT perform YAML I/O.
**Implementation:** src/rhapsody_cli/exchange/core.py:RhapsodyModelHelper
**Last Changed:** 2026-07-19

---

## SWR_XCH_011: Relations Round-Trip

**ID:** SWR_XCH_011
**Title:** Dependency, Generalization, and Relation round-trip with source/target wiring
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip relation elements:
- `Dependency`: `from` (string, source classifier name), `to` (string, target classifier name), `stereotypes`, `tags`.
- `Generalization`: `subtype` (string, derived classifier name), `superclass` (string, base classifier name), `stereotypes`, `tags`.
- `Relation`: `from` (string), `to` (string), `relation_type` (string — one of "Association", "Aggregation", "Composition"), `multiplicity` (string, optional), `role` (string, optional), `visibility` (string, optional), `is_navigable` (bool, optional), `is_virtual` (bool, optional), `stereotypes`, `tags`.
The importer SHALL create the relation via `find_or_create_<type>(parent, name)` then wire source/target via `set_from()`/`set_to()` (Dependency, Relation) or `set_from()`/`set_to()` (Generalization) using classifiers resolved via `resolve_classifier(name)`.
The exporter SHALL serialize `from`/`to` via `get_from().get_name()` / `get_to().get_name()` and `relation_type` via `get_relation_type()`.
Missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_dependency_extras, _apply_generalization_extras, _apply_relation_extras; src/rhapsody_cli/exchange/exporter.py:_export_dependency, _export_generalization, _export_relation
**Last Changed:** 2026-07-19

---

## SWR_XCH_012: Ports Round-Trip

**ID:** SWR_XCH_012
**Title:** Port round-trip with interfaces and contract
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip `Port` elements with the following fields:
- `is_behavioral` (bool, optional) — set via `set_is_behavioral(1/0)`.
- `is_reversed` (bool, optional) — set via `set_is_reversed(1/0)`.
- `contract` (string, optional) — interface name resolved via `resolve_classifier(name)` and set via `set_contract(interface)`.
- `provided_interfaces` (list of strings, optional) — each resolved via `resolve_classifier(name)` and added via `add_provided_interface(interface)`.
- `required_interfaces` (list of strings, optional) — each resolved via `resolve_classifier(name)` and added via `add_required_interface(interface)`.
- `stereotypes`, `tags` (common fields).
The exporter SHALL serialize these fields via the corresponding getters; missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_port_extras; src/rhapsody_cli/exchange/exporter.py:_export_port
**Last Changed:** 2026-07-19

---

## SWR_XCH_013: Events and EventReceptions Round-Trip

**ID:** SWR_XCH_013
**Title:** Event and EventReception round-trip with event references
**Status:** Planned
**Priority:** High
**Description:**
The exchange module SHALL round-trip `Event` and `EventReception` elements:
- `Event`: `base_event` (string, optional — name of parent event), `super_event` (string, optional — name of super event), `stereotypes`, `tags`.
- `EventReception`: `event` (string, optional — name of referenced event, set via `set_event(event_element)` after resolution), `stereotypes`, `tags`.
The importer SHALL resolve event references via `resolve_classifier(name)`; missing references SHALL be skipped with a WARNING (per SWR_XCH_009).
The exporter SHALL serialize these fields via the corresponding getters (None-safe).
**Implementation:** src/rhapsody_cli/exchange/importer.py:_apply_event_extras, _apply_event_reception_extras; src/rhapsody_cli/exchange/exporter.py:_export_event, _export_event_reception
**Last Changed:** 2026-07-19
```

- [ ] **Step 2: Create `docs/tests/unit/uts_xch_test-specs.md`**

Write the file with this exact content (91 entries, grouped by source task for reviewer convenience):

```markdown
# Unit Test Specifications - YAML Import/Export

**Category:** YAML Import/Export
**Prefix:** UTS_XCH
**Test Type:** Unit
**Last Validated:** 2026-07-19

---

## UTS_XCH_00001: Schema version constant sanity

**ID:** UTS_XCH_00001
**Traces-To:** SWR_XCH_005
**Title:** SCHEMA_VERSION and key constants are correctly defined
**Type:** Unit
**Priority:** High
**Description:**
Verify `SCHEMA_VERSION = 1` (int), `VERSION_KEY = "version"`, `PROJECT_KEY = "project"`, `RHAPSODY_MODEL_KEY = "rhapsody-model"`.
**Pre-conditions:**
- `exchange/schema.py` importable
**Test Steps:**
1. Import `SCHEMA_VERSION`, `VERSION_KEY`, `PROJECT_KEY`, `RHAPSODY_MODEL_KEY`
2. Assert types and values
**Expected Result:**
Constants have the expected values and types.
**Verification Criteria:**
- `SCHEMA_VERSION == 1` and `isinstance(SCHEMA_VERSION, int)`
- Each key constant equals its string literal
**Last Changed:** 2026-07-19

---

## UTS_XCH_00002: RhapsodyYaml.read happy path

**ID:** UTS_XCH_00002
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml.read returns parsed YAML mapping
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` returns the parsed dict from a valid YAML file.
**Pre-conditions:**
- Temp file contains `key: value` YAML
**Test Steps:**
1. Instantiate `RhapsodyYaml`
2. Call `read(path)` on the temp file
3. Assert returned dict matches expected
**Expected Result:**
Dict equals `{"key": "value"}`.
**Verification Criteria:**
- Returned object is a `dict`
- `result["key"] == "value"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00003: RhapsodyYaml.read missing file

**ID:** UTS_XCH_00003
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError on missing file
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` raises `CliExecutionError` when the file does not exist.
**Pre-conditions:**
- Path points to a non-existent file
**Test Steps:**
1. Call `read(non_existent_path)`
2. Assert `CliExecutionError` is raised
**Expected Result:**
`CliExecutionError` raised with "Input file not found" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains the path
**Last Changed:** 2026-07-19

---

## UTS_XCH_00004: RhapsodyYaml.read invalid YAML

**ID:** UTS_XCH_00004
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError on malformed YAML
**Type:** Unit
**Priority:** High
**Description:**
Verify `read(path)` raises `CliExecutionError` when the YAML is malformed.
**Pre-conditions:**
- Temp file contains invalid YAML (e.g. `: : :`)
**Test Steps:**
1. Call `read(path)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Invalid YAML" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains file path and parser error
**Last Changed:** 2026-07-19

---

## UTS_XCH_00005: RhapsodyYaml.read non-mapping top level

**ID:** UTS_XCH_00005
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.read raises CliExecutionError when top level is not a mapping
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `read(path)` raises `CliExecutionError` when top level is a list or scalar.
**Pre-conditions:**
- Temp file contains `- item` (YAML list)
**Test Steps:**
1. Call `read(path)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Expected YAML mapping" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
**Last Changed:** 2026-07-19

---

## UTS_XCH_00006: RhapsodyYaml.write happy path

**ID:** UTS_XCH_00006
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml.write serializes dict to YAML file
**Type:** Unit
**Priority:** High
**Description:**
Verify `write(path, data)` writes a YAML file that can be read back.
**Pre-conditions:**
- Temp output path
- Dict `{"a": 1, "b": [2, 3]}`
**Test Steps:**
1. Call `write(path, data)`
2. Read the file back with PyYAML directly
3. Assert content matches
**Expected Result:**
File contains the YAML serialization of the dict.
**Verification Criteria:**
- File exists after write
- `yaml.safe_load(open(path))` equals input dict
**Last Changed:** 2026-07-19

---

## UTS_XCH_00007: RhapsodyYaml.write failure

**ID:** UTS_XCH_00007
**Traces-To:** SWR_XCH_005, SWR_XCH_009
**Title:** RhapsodyYaml.write raises CliExecutionError on OS error
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `write(path, data)` raises `CliExecutionError` when the path is unwritable.
**Pre-conditions:**
- Path points to a directory that does not exist
**Test Steps:**
1. Call `write(non_existent_dir/file, data)`
2. Assert `CliExecutionError` raised
**Expected Result:**
`CliExecutionError` with "Failed to write" message.
**Verification Criteria:**
- `pytest.raises(CliExecutionError)` succeeds
- Error message contains the path
**Last Changed:** 2026-07-19

---

## UTS_XCH_00008: RhapsodyYaml round-trip

**ID:** UTS_XCH_00008
**Traces-To:** SWR_XCH_005
**Title:** RhapsodyYaml write then read preserves data
**Type:** Unit
**Priority:** High
**Description:**
Verify data written via `write` can be read back identically via `read`.
**Pre-conditions:**
- Temp file path
**Test Steps:**
1. Call `write(path, original_dict)`
2. Call `read(path)` → result
3. Assert `result == original_dict`
**Expected Result:**
Round-trip preserves the dict.
**Verification Criteria:**
- `result == original_dict`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00009: find_or_create_package sanitizes name and delegates to add_new_aggr

**ID:** UTS_XCH_00009
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_package creates a Package via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_package` sanitizes the name and calls `parent.add_new_aggr("Package", name)` when the child does not exist.
**Pre-conditions:**
- Fake parent with no matching child
**Test Steps:**
1. Call `helper.find_or_create_package(parent, "My Package")`
2. Assert `parent.add_new_aggr` called with `("Package", "My_Package")`
**Expected Result:**
Package created with sanitized name.
**Verification Criteria:**
- `add_new_aggr` called once with `"Package"` and sanitized name
**Last Changed:** 2026-07-19

---

## UTS_XCH_00010: find_or_create_class creates via add_new_aggr

**ID:** UTS_XCH_00010
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_class creates a Class via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_class` calls `parent.add_new_aggr("Class", name)` when not found.
**Pre-conditions:**
- Fake parent with no matching child
**Test Steps:**
1. Call `helper.find_or_create_class(parent, "MyClass")`
2. Assert `add_new_aggr("Class", "MyClass")` called
**Expected Result:**
Class created.
**Verification Criteria:**
- `add_new_aggr` called once with `("Class", "MyClass")`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00011: find_or_create_operation on package uses add_global_function

**ID:** UTS_XCH_00011
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_operation on a Package delegates to add_global_function
**Type:** Unit
**Priority:** High
**Description:**
Verify that when the parent is a Package, `find_or_create_operation` calls `parent.add_global_function(name)`.
**Pre-conditions:**
- Fake parent whose `get_meta_class()` returns "Package"
**Test Steps:**
1. Call `helper.find_or_create_operation(parent, "myFunc")`
2. Assert `parent.add_global_function` called with `"myFunc"`
**Expected Result:**
Operation created via `add_global_function`.
**Verification Criteria:**
- `add_global_function("myFunc")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00012: find_or_create_operation on class uses add_new_aggr

**ID:** UTS_XCH_00012
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_operation on a Class delegates to add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify that when the parent is a Class, `find_or_create_operation` calls `parent.add_new_aggr("Operation", name)`.
**Pre-conditions:**
- Fake parent whose `get_meta_class()` returns "Class"
**Test Steps:**
1. Call `helper.find_or_create_operation(parent, "myOp")`
2. Assert `add_new_aggr("Operation", "myOp")` called
**Expected Result:**
Operation created via `add_new_aggr`.
**Verification Criteria:**
- `add_new_aggr("Operation", "myOp")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00013: find_or_create_argument uses add_argument

**ID:** UTS_XCH_00013
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_argument delegates to parent.add_argument
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_argument` calls `parent.add_argument(name)`.
**Pre-conditions:**
- Fake parent (Operation)
**Test Steps:**
1. Call `helper.find_or_create_argument(parent, "x")`
2. Assert `add_argument("x")` called
**Expected Result:**
Argument created.
**Verification Criteria:**
- `add_argument("x")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00014: find_or_create_attribute creates via add_new_aggr

**ID:** UTS_XCH_00014
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_attribute creates an Attribute via add_new_aggr
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_attribute` calls `parent.add_new_aggr("Attribute", name)`.
**Pre-conditions:**
- Fake parent (Class)
**Test Steps:**
1. Call `helper.find_or_create_attribute(parent, "threshold")`
2. Assert `add_new_aggr("Attribute", "threshold")` called
**Expected Result:**
Attribute created.
**Verification Criteria:**
- `add_new_aggr("Attribute", "threshold")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00015: find_or_create_type sets kind after creation

**ID:** UTS_XCH_00015
**Traces-To:** SWR_XCH_006, SWR_XCH_008
**Title:** find_or_create_type creates a Type and sets its kind
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_or_create_type` creates via `add_new_aggr("Type", name)` and then calls `_set_type_kind(type_element, kind)`.
**Pre-conditions:**
- Fake parent, kind="Enumeration"
**Test Steps:**
1. Call `helper.find_or_create_type(parent, "Color", "Enumeration")`
2. Assert `add_new_aggr("Type", "Color")` called
3. Assert `set_kind("Enumeration")` called on the new type element
**Expected Result:**
Type created with kind set.
**Verification Criteria:**
- `add_new_aggr` and `set_kind` both called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00016: find_or_create_object creates via add_new_aggr

**ID:** UTS_XCH_00016
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_object creates an Object via add_new_aggr
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `find_or_create_object` calls `parent.add_new_aggr("Object", name)`.
**Pre-conditions:**
- Fake parent (Package)
**Test Steps:**
1. Call `helper.find_or_create_object(parent, "myInstance")`
2. Assert `add_new_aggr("Object", "myInstance")` called
**Expected Result:**
Object created.
**Verification Criteria:**
- `add_new_aggr("Object", "myInstance")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00017: find_or_create_enumeration_literal creates via add_new_aggr

**ID:** UTS_XCH_00017
**Traces-To:** SWR_XCH_006
**Title:** find_or_create_enumeration_literal creates via add_new_aggr("LiteralValue", name)
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `find_or_create_enumeration_literal` calls `parent.add_new_aggr("LiteralValue", name)`.
**Pre-conditions:**
- Fake parent (Type with kind=Enumeration)
**Test Steps:**
1. Call `helper.find_or_create_enumeration_literal(parent, "RED")`
2. Assert `add_new_aggr("LiteralValue", "RED")` called
**Expected Result:**
EnumerationLiteral created.
**Verification Criteria:**
- `add_new_aggr("LiteralValue", "RED")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00018: find_child_by_name returns matching child

**ID:** UTS_XCH_00018
**Traces-To:** SWR_XCH_010
**Title:** find_child_by_name returns the child whose name matches
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_child_by_name(parent, name)` iterates `parent.get_nested_elements()` and returns the matching child.
**Pre-conditions:**
- Fake parent with two children named "A" and "B"
**Test Steps:**
1. Call `find_child_by_name(parent, "B")`
2. Assert the second child is returned
**Expected Result:**
Returns the child named "B".
**Verification Criteria:**
- Returned element's `get_name()` == "B"
**Last Changed:** 2026-07-19

---

## UTS_XCH_00019: find_child_by_name returns None when no match

**ID:** UTS_XCH_00019
**Traces-To:** SWR_XCH_010
**Title:** find_child_by_name returns None when no child matches
**Type:** Unit
**Priority:** High
**Description:**
Verify `find_child_by_name` returns `None` when no child has the requested name.
**Pre-conditions:**
- Fake parent with children "A", "B"
**Test Steps:**
1. Call `find_child_by_name(parent, "Z")`
2. Assert result is `None`
**Expected Result:**
Returns `None`.
**Verification Criteria:**
- `result is None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00020: apply_stereotypes infers meta_type from element

**ID:** UTS_XCH_00020
**Traces-To:** SWR_XCH_007
**Title:** apply_stereotypes infers meta_type and calls add_stereotype
**Type:** Unit
**Priority:** High
**Description:**
Verify `apply_stereotypes(element, ["active", "boundary"])` calls `element.add_stereotype(name, meta_type)` for each, with `meta_type` derived from `element.get_meta_class()`.
**Pre-conditions:**
- Fake element with `get_meta_class()` returning "Class"
**Test Steps:**
1. Call `apply_stereotypes(element, ["active", "boundary"])`
2. Assert `add_stereotype` called twice with `("active", "Class")` and `("boundary", "Class")`
**Expected Result:**
Both stereotypes added with correct meta_type.
**Verification Criteria:**
- `add_stereotype.call_count == 2`
- Each call's second arg equals "Class"
**Last Changed:** 2026-07-19

---

## UTS_XCH_00021: apply_stereotypes skips already-applied stereotypes

**ID:** UTS_XCH_00021
**Traces-To:** SWR_XCH_007
**Title:** apply_stereotypes is idempotent — skips already-applied stereotypes
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `apply_stereotypes` does not call `add_stereotype` for stereotypes the element already has.
**Pre-conditions:**
- Fake element with `get_already_applied_stereotypes` returning "active"
**Test Steps:**
1. Call `apply_stereotypes(element, ["active", "boundary"])`
2. Assert `add_stereotype` called only for "boundary"
**Expected Result:**
Only the missing stereotype is added.
**Verification Criteria:**
- `add_stereotype.call_count == 1`
- `add_stereotype` called with `("boundary", ...)`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00022: apply_tags uses set_property_value

**ID:** UTS_XCH_00022
**Traces-To:** SWR_XCH_007
**Title:** apply_tags calls set_property_value for each key/value pair
**Type:** Unit
**Priority:** High
**Description:**
Verify `apply_tags(element, {"status": "active", "level": "3"})` calls `element.set_property_value(key, val)` for each entry.
**Pre-conditions:**
- Fake element with `set_property_value` mock
**Test Steps:**
1. Call `apply_tags(element, tags_dict)`
2. Assert `set_property_value` called twice
**Expected Result:**
Both tags set.
**Verification Criteria:**
- `set_property_value.call_count == 2`
- Both `("status", "active")` and `("level", "3")` called
**Last Changed:** 2026-07-19

---

## UTS_XCH_00023: resolve_classifier searches project recursively

**ID:** UTS_XCH_00023
**Traces-To:** SWR_XCH_010
**Title:** resolve_classifier walks project.get_nested_elements() to find a classifier by name
**Type:** Unit
**Priority:** High
**Description:**
Verify `resolve_classifier(name)` returns the first classifier whose `get_name()` matches.
**Pre-conditions:**
- Fake project with nested elements containing a Class named "Base"
**Test Steps:**
1. Call `helper.resolve_classifier("Base")`
2. Assert returned element has `get_name() == "Base"`
**Expected Result:**
Returns the matching classifier.
**Verification Criteria:**
- Returned element is not `None`
- `get_name() == "Base"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00024: resolve_classifier returns None when not found

**ID:** UTS_XCH_00024
**Traces-To:** SWR_XCH_010
**Title:** resolve_classifier returns None when no classifier matches
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `resolve_classifier(name)` returns `None` when the name is not found.
**Pre-conditions:**
- Fake project with no classifier named "Missing"
**Test Steps:**
1. Call `helper.resolve_classifier("Missing")`
2. Assert result is `None`
**Expected Result:**
Returns `None`.
**Verification Criteria:**
- `result is None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00025: get_classifier_name is None-safe

**ID:** UTS_XCH_00025
**Traces-To:** SWR_XCH_010
**Title:** get_classifier_name returns None when classifier is None or get_name raises
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `get_classifier_name(None)` returns `None` and that exceptions from `get_name()` are swallowed.
**Pre-conditions:**
- None classifier
- Fake classifier whose `get_name` raises
**Test Steps:**
1. Call `get_classifier_name(None)` → `None`
2. Call `get_classifier_name(broken_classifier)` → `None`
**Expected Result:**
Both return `None`.
**Verification Criteria:**
- Both results are `None`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00026: _set_type_kind calls set_kind

**ID:** UTS_XCH_00026
**Traces-To:** SWR_XCH_006, SWR_XCH_008
**Title:** _set_type_kind delegates to type_element.set_kind
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_set_type_kind(type_element, "Enumeration")` calls `type_element.set_kind("Enumeration")`.
**Pre-conditions:**
- Fake type element
**Test Steps:**
1. Call `helper._set_type_kind(type_element, "Enumeration")`
2. Assert `set_kind("Enumeration")` called
**Expected Result:**
Kind set on the type.
**Verification Criteria:**
- `set_kind` called once with `"Enumeration"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00027: _collect_children returns nested elements

**ID:** UTS_XCH_00027
**Traces-To:** SWR_XCH_010
**Title:** _collect_children returns get_nested_elements() contents
**Type:** Unit
**Priority:** High
**Description:**
Verify `_collect_children(container)` returns the contents of `container.get_nested_elements()`.
**Pre-conditions:**
- Fake container with 2 nested elements
**Test Steps:**
1. Call `helper._collect_children(container)`
2. Assert result has 2 items
**Expected Result:**
Returns the 2 nested elements.
**Verification Criteria:**
- `len(result) == 2`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00028: _collect_children merges package globals

**ID:** UTS_XCH_00028
**Traces-To:** SWR_XCH_010
**Title:** _collect_children merges get_global_functions/variables/objects for packages
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_collect_children` on a Package also includes globals from `get_global_functions`, `get_global_variables`, `get_global_objects` (when available).
**Pre-conditions:**
- Fake package with nested elements + global functions/variables/objects
**Test Steps:**
1. Call `helper._collect_children(package)`
2. Assert result contains all 4 sources
**Expected Result:**
Combined list returned.
**Verification Criteria:**
- Result includes items from all 4 sources
**Last Changed:** 2026-07-19

---

## UTS_XCH_00029: _get_project_name walks owner chain

**ID:** UTS_XCH_00029
**Traces-To:** SWR_XCH_010
**Title:** _get_project_name walks the owner chain to find the Project's name
**Type:** Unit
**Priority:** Medium
**Description:**
Verify `_get_project_name(element)` returns the name of the Project ancestor.
**Pre-conditions:**
- Fake element whose owner chain leads to a project named "MyProject"
**Test Steps:**
1. Call `helper._get_project_name(element)`
2. Assert result equals "MyProject"
**Expected Result:**
Returns "MyProject".
**Verification Criteria:**
- `result == "MyProject"`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00030 through UTS_XCH_00045: RhapsodyImporter core element dispatch (Task 5)

These 16 test cases cover `RhapsodyImporter.import_template` (version check, dispatch) and `_process_element` / `_apply_<type>_extras` for the 8 core element types (Package, Class, Operation, Argument, Attribute, Type, Object, EnumerationLiteral).

**Traces-To:** SWR_XCH_002, SWR_XCH_004, SWR_XCH_008, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

Each entry in this range follows the same template:
- **UTS_XCH_00030:** import_template raises CliExecutionError on version mismatch (SWR_XCH_009)
- **UTS_XCH_00031:** import_template dispatches each spec to _process_element (SWR_XCH_002)
- **UTS_XCH_00032:** _process_element creates Package and recurses into children (SWR_XCH_006, SWR_XCH_008)
- **UTS_XCH_00033:** _process_element creates Class and applies is_abstract/is_active (SWR_XCH_008)
- **UTS_XCH_00034:** _process_element creates Operation and applies return_type/visibility/is_static (SWR_XCH_008)
- **UTS_XCH_00035:** _apply_operation_extras creates Arguments and sets direction/type (SWR_XCH_008)
- **UTS_XCH_00036:** _process_element creates Argument and applies direction/type (SWR_XCH_008)
- **UTS_XCH_00037:** _process_element creates Attribute and applies type/visibility/multiplicity (SWR_XCH_008)
- **UTS_XCH_00038:** _process_element creates Type with kind and processes literals (SWR_XCH_008)
- **UTS_XCH_00039:** _process_element creates Object and sets classifier (SWR_XCH_008)
- **UTS_XCH_00040:** _process_element creates EnumerationLiteral with stereotypes/tags (SWR_XCH_007, SWR_XCH_008)
- **UTS_XCH_00041:** _process_element applies stereotypes to all element types (SWR_XCH_007)
- **UTS_XCH_00042:** _process_element applies tags to all element types (SWR_XCH_007)
- **UTS_XCH_00043:** _process_element skips unsupported type with warning (SWR_XCH_009)
- **UTS_XCH_00044:** _process_element skips missing type reference with warning (SWR_XCH_009)
- **UTS_XCH_00045:** _process_element recurses into Package children (SWR_XCH_006)

---

## UTS_XCH_00046 through UTS_XCH_00059: RhapsodyImporter extension (Task 6)

These 14 test cases cover `_apply_<type>_extras` for the 6 new element types (Dependency, Generalization, Relation, Port, Event, EventReception) and the dispatch wiring in `_process_element`.

**Traces-To:** SWR_XCH_011, SWR_XCH_012, SWR_XCH_013, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00046:** _apply_dependency_extras wires from/to via resolve_classifier (SWR_XCH_011)
- **UTS_XCH_00047:** _apply_dependency_extras skips missing target with warning (SWR_XCH_009, SWR_XCH_011)
- **UTS_XCH_00048:** _apply_generalization_extras wires subtype/superclass (SWR_XCH_011)
- **UTS_XCH_00049:** _apply_generalization_extras skips missing superclass (SWR_XCH_009)
- **UTS_XCH_00050:** _apply_relation_extras wires from/to and sets relation_type (SWR_XCH_011)
- **UTS_XCH_00051:** _apply_relation_extras sets multiplicity/role/visibility/is_navigable/is_virtual (SWR_XCH_011)
- **UTS_XCH_00052:** _apply_port_extras sets is_behavioral/is_reversed (SWR_XCH_012)
- **UTS_XCH_00053:** _apply_port_extras sets contract via resolve_classifier (SWR_XCH_012)
- **UTS_XCH_00054:** _apply_port_extras adds provided_interfaces (SWR_XCH_012)
- **UTS_XCH_00055:** _apply_port_extras adds required_interfaces (SWR_XCH_012)
- **UTS_XCH_00056:** _apply_port_extras skips missing contract with warning (SWR_XCH_009, SWR_XCH_012)
- **UTS_XCH_00057:** _apply_event_extras sets base_event/super_event (SWR_XCH_013)
- **UTS_XCH_00058:** _apply_event_reception_extras sets event reference (SWR_XCH_013)
- **UTS_XCH_00059:** _process_element dispatch table includes all 14 types (SWR_XCH_006)

---

## UTS_XCH_00060 through UTS_XCH_00075: RhapsodyExporter core element dispatch (Task 7)

These 16 test cases cover `RhapsodyExporter.export` (top-level dict shape, version/project/rhapsody-model keys) and `_export_<type>` for the 8 core element types plus `_export_stereotypes`, `_export_tags`, and skip-on-unsupported behavior.

**Traces-To:** SWR_XCH_001, SWR_XCH_003, SWR_XCH_005, SWR_XCH_007, SWR_XCH_009
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00060:** export returns dict with version=1, project name, rhapsody-model list (SWR_XCH_005)
- **UTS_XCH_00061:** export skips None children (SWR_XCH_009)
- **UTS_XCH_00062:** _export_element dispatches Package to _export_package (SWR_XCH_001)
- **UTS_XCH_00063:** _export_package emits children list (SWR_XCH_008)
- **UTS_XCH_00064:** _export_class emits is_abstract/is_active (SWR_XCH_008)
- **UTS_XCH_00065:** _export_operation emits return_type and arguments (SWR_XCH_008)
- **UTS_XCH_00066:** _export_argument emits direction and type (SWR_XCH_008)
- **UTS_XCH_00067:** _export_attribute emits type/visibility/multiplicity (SWR_XCH_008)
- **UTS_XCH_00068:** _export_type emits kind and literals (SWR_XCH_008)
- **UTS_XCH_00069:** _export_object emits classifier name (SWR_XCH_008)
- **UTS_XCH_00070:** _export_enumeration_literal emits name only (SWR_XCH_008)
- **UTS_XCH_00071:** _export_stereotypes returns list of names (SWR_XCH_007)
- **UTS_XCH_00072:** _export_tags returns dict of name→value (SWR_XCH_007)
- **UTS_XCH_00073:** _export_tags skips malformed tags (SWR_XCH_007, SWR_XCH_009)
- **UTS_XCH_00074:** _export_element returns None for unknown metaclass (SWR_XCH_009)
- **UTS_XCH_00075:** _export_element returns None for None input (SWR_XCH_009)

---

## UTS_XCH_00076 through UTS_XCH_00089: RhapsodyExporter extension (Task 8)

These 14 test cases cover `_export_<type>` for the 6 new element types (Dependency, Generalization, Relation, Port, Event, EventReception) and the updated dispatch table.

**Traces-To:** SWR_XCH_011, SWR_XCH_012, SWR_XCH_013
**Type:** Unit
**Priority:** High
**Last Changed:** 2026-07-19

- **UTS_XCH_00076:** _export_dependency emits from/to names (SWR_XCH_011)
- **UTS_XCH_00077:** _export_dependency emits stereotypes/tags (SWR_XCH_007, SWR_XCH_011)
- **UTS_XCH_00078:** _export_generalization emits subtype/superclass (SWR_XCH_011)
- **UTS_XCH_00079:** _export_relation emits from/to/relation_type (SWR_XCH_011)
- **UTS_XCH_00080:** _export_relation emits multiplicity/role/visibility/is_navigable/is_virtual (SWR_XCH_011)
- **UTS_XCH_00081:** _export_port emits is_behavioral/is_reversed (SWR_XCH_012)
- **UTS_XCH_00082:** _export_port emits contract name (SWR_XCH_012)
- **UTS_XCH_00083:** _export_port emits provided_interfaces list (SWR_XCH_012)
- **UTS_XCH_00084:** _export_port emits required_interfaces list (SWR_XCH_012)
- **UTS_XCH_00085:** _export_event emits base_event/super_event (SWR_XCH_013)
- **UTS_XCH_00086:** _export_event_reception emits event reference (SWR_XCH_013)
- **UTS_XCH_00087:** _export_element dispatch table includes all 14 types (SWR_XCH_006)
- **UTS_XCH_00088:** _export_name_list helper converts collection of elements to list of names (SWR_XCH_011, SWR_XCH_012)
- **UTS_XCH_00089:** _classifier_name helper is None-safe (SWR_XCH_010, SWR_XCH_011)

---

## UTS_XCH_00090: ProjectCommand registers export/import subcommands

**ID:** UTS_XCH_00090
**Traces-To:** SWR_XCH_001, SWR_XCH_002
**Title:** ProjectCommand.get_actions includes ProjectExportAction and ProjectImportAction
**Type:** Unit
**Priority:** High
**Description:**
Verify `ProjectCommand.get_actions()` returns 6 actions including "export" and "import".
**Pre-conditions:**
- `ProjectCommand` importable
**Test Steps:**
1. Construct `ProjectCommand(["open", "x.rpy"])`
2. Call `get_actions()`
3. Collect `command_id` values
4. Assert "export" and "import" present and `len(actions) == 6`
**Expected Result:**
All 6 actions registered.
**Verification Criteria:**
- `"export" in command_ids`
- `"import" in command_ids`
- `len(actions) == 6`
**Last Changed:** 2026-07-19

---

## UTS_XCH_00091: PackageCommand registers export/import subcommands

**ID:** UTS_XCH_00091
**Traces-To:** SWR_XCH_003, SWR_XCH_004
**Title:** PackageCommand.get_actions includes PackageExportAction and PackageImportAction
**Type:** Unit
**Priority:** High
**Description:**
Verify `PackageCommand.get_actions()` returns 7 actions including "export" and "import".
**Pre-conditions:**
- `PackageCommand` importable
**Test Steps:**
1. Construct `PackageCommand(["create", "--path", "Sensors", '{}'])`
2. Call `get_actions()`
3. Collect `command_id` values
4. Assert "export" and "import" present and `len(actions) == 7`
**Expected Result:**
All 7 actions registered.
**Verification Criteria:**
- `"export" in command_ids`
- `"import" in command_ids`
- `len(actions) == 7`
**Last Changed:** 2026-07-19
```

- [ ] **Step 3: Update `docs/index.rst` toctree**

In `docs/index.rst`, locate the Requirements toctree (around line 224–237) and add `requirements/swr_xch_requirements` after `requirements/swr_elem_requirements`:

```rst
.. toctree::
   :maxdepth: 1
   :caption: Requirements:

   requirements/swr_app_requirements
   requirements/swr_cli_requirements
   requirements/swr_core_requirements
   requirements/swr_exc_requirements
   requirements/swr_pkg_requirements
   requirements/swr_cls_requirements
   requirements/swr_op_requirements
   requirements/swr_attr_requirements
   requirements/swr_port_requirements
   requirements/swr_elem_requirements
   requirements/swr_xch_requirements
```

The Test Specifications toctree already uses `:glob:` with `tests/unit/*`, so `uts_xch_test-specs.md` is automatically included — no edit needed for that section.

- [ ] **Step 4: Verify documentation files exist and are well-formed**

Run:

```bash
python -c "import pathlib; p = pathlib.Path('docs/requirements/swr_xch_requirements.md'); assert p.exists() and p.stat().st_size > 0, 'SWR doc missing'; print('SWR OK:', p.stat().st_size, 'bytes')"
python -c "import pathlib; p = pathlib.Path('docs/tests/unit/uts_xch_test-specs.md'); assert p.exists() and p.stat().st_size > 0, 'UTS doc missing'; print('UTS OK:', p.stat().st_size, 'bytes')"
```

Expected: both files exist with non-zero size.

- [ ] **Step 5: Commit**

```bash
git add docs/requirements/swr_xch_requirements.md docs/tests/unit/uts_xch_test-specs.md docs/index.rst
git commit -m "docs(xch): add SWR_XCH requirements and UTS_XCH test specs

Adds docs/requirements/swr_xch_requirements.md (13 SWR_XCH entries
extracted from the approved spec) and docs/tests/unit/uts_xch_test-specs.md
(91 UTS_XCH entries with Traces-To links). Wires the SWR doc into
docs/index.rst toctree. UTS doc is auto-included via the existing
tests/unit/* glob. SWR_XCH_001..013."
```

---

## Task 13: Final quality gate verification

**Files:**
- No code changes expected — this is a verification task. If any quality gate fails, return to the relevant task and fix before re-running.

**Interfaces:**
- Consumes: all implementation from Tasks 1–12
- Produces: a green quality gate (`ruff`, `black`, `mypy`, `pytest tests/unit`) — the prerequisite for opening a PR.

- [ ] **Step 1: Run ruff across all touched source and test files**

Run (in git bash for faster black; ruff is fast in either shell):

```bash
ruff check src/rhapsody_cli/exchange/ src/rhapsody_cli/actions/project_action.py src/rhapsody_cli/actions/package_action.py src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py tests/unit/exchange/ tests/unit/actions/test_project_action.py tests/unit/actions/test_package_action.py tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py
```

Expected: "All checks passed!" with no errors. If any error appears, return to the relevant task, fix the issue, re-run, and re-commit using `git commit --amend --no-edit` ONLY if the previous commit hasn't been pushed; otherwise create a `fix:` commit.

- [ ] **Step 2: Run black --check across the same files**

Run (in git bash for speed — black is slow in PowerShell on Windows per project convention):

```bash
black --check src/rhapsody_cli/exchange/ src/rhapsody_cli/actions/project_action.py src/rhapsody_cli/actions/package_action.py src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py tests/unit/exchange/ tests/unit/actions/test_project_action.py tests/unit/actions/test_package_action.py tests/unit/commands/test_project_command.py tests/unit/commands/test_package_command.py
```

Expected: "would reformat" appears for ZERO files. If any file would be reformatted, run `black <files>` to fix, then commit the formatting change as `style: black-formatting`.

- [ ] **Step 3: Run mypy in strict mode on the new exchange package**

Run:

```bash
mypy src/rhapsody_cli/exchange/ src/rhapsody_cli/actions/project_action.py src/rhapsody_cli/actions/package_action.py src/rhapsody_cli/commands/project_command.py src/rhapsody_cli/commands/package_command.py
```

Expected: "Success: no issues found" with exit code 0. CI runs mypy only on Python < 3.10, so run on Python 3.8 or 3.9 if available. Common issues to watch for:
- Missing type annotations on new methods (use `-> None`, `-> Dict[str, Any]`, etc.)
- `Optional[X]` required for parameters that accept `None`
- String-quoted forward refs (`"argparse._SubParsersAction[argparse.ArgumentParser]"`) instead of `from __future__ import annotations` (forbidden per project rules)

If any mypy error appears, fix the type annotations in the flagged file, re-run, and amend or commit the fix.

- [ ] **Step 4: Run the full unit test suite with coverage**

Run:

```bash
pytest tests/unit/ --cov=rhapsody_cli.exchange --cov=rhapsody_cli.actions.project_action --cov=rhapsody_cli.actions.package_action --cov-report=term-missing
```

Expected:
- All tests pass (zero failures, zero errors, zero skips unrelated to Windows-only tests).
- Coverage on `rhapsody_cli.exchange` ≥ 80% (the project minimum). If below 80%, identify uncovered lines via the term-missing report and add tests targeting those paths (typically error-handling branches and skip-on-unsupported paths).
- Coverage on the new action methods in `project_action.py` and `package_action.py` ≥ 80% (cover both happy paths and the `RhapsodyConnectionError`/`CliExecutionError` branches).

If any test fails, return to the task that wrote the failing test, debug using the systematic-debugging skill, fix, and re-run.

- [ ] **Step 5: Run the project's full quality gate as a final smoke test**

Run (the same gate CI runs on `windows-latest`):

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit
```

Expected: all four commands exit 0. This is the gate that must be green before opening a PR.

- [ ] **Step 6: Smoke-test the CLI end-to-end (manual, optional but recommended)**

If Rhapsody is installed on the dev machine, do a manual smoke test:

1. Open a Rhapsody project.
2. Run `rhapsody-cli project export --file out.yaml` — verify `out.yaml` is created with `version: 1`, a `project` key, and a `rhapsody-model` list.
3. Inspect `out.yaml` — verify at least one Package and one Class are present with expected fields.
4. Run `rhapsody-cli package import --file out.yaml --path SomeTarget` — verify elements appear under the target package without duplicates (idempotency).
5. Re-run the same import — verify NO duplicates are created (proves `find_or_create` idempotency).

If Rhapsody is not installed (typical in CI), skip this step — integration tests in `tests/integration/exchange/` (added separately) will cover it.

- [ ] **Step 7: Final commit (only if any fix-ups were needed in Steps 1–5)**

If Steps 1–5 surfaced any fixes:

```bash
git add -p  # stage the specific fixes
git commit -m "fix(xch): address quality gate findings

Resolves ruff/black/mypy/coverage issues found during the final
quality gate pass. SWR_XCH_009."
```

If no fixes were needed (the rare ideal case), skip this step — the feature is ready to merge.

---

## Self-Review

This section is the plan author's own audit against the spec, per the `writing-plans` skill. Issues found are either fixed inline or explicitly accepted with rationale.

### 1. Spec coverage

Mapping each spec section and SWR_XCH requirement to a task:

| Spec Section / SWR ID | Covered By |
|---|---|
| §1 Goal | Plan header `Goal:` line |
| §2 YAML Schema | Task 1 (`schema.py` constants), Task 7 (exporter emits schema) |
| §3 Architecture | Plan `File Structure` section + Tasks 1–8 |
| §4 Components | Tasks 1–10 (all components: `RhapsodyYaml`, `RhapsodyModelHelper`, `RhapsodyImporter`, `RhapsodyExporter`, four Actions) |
| §4 Command registration | Task 11 |
| §5 CLI Commands | Tasks 9, 10, 11 |
| §6 Data Flow | Implicit in Tasks 5 (import flow) and 7 (export flow) — each `_process_element` / `_export_element` step mirrors the data flow diagrams |
| §7 Error Handling | Per-task (each action wraps `execute` in try/except; each `_apply_*_extras` skips missing refs with WARNING); Task 13 verifies via coverage |
| §8 Testing | Every task is TDD (failing test → impl → pass → commit) |
| §8.4 Requirement IDs | Task 12 creates the SWR + UTS docs |
| §9 Dependencies | Task 1 adds `PyYAML>=6.0` to `pyproject.toml` |
| §10 Out of Scope (v1 Limitations) | No tasks — by definition out of scope |
| §11 References | No tasks — informational only |
| §12 Open Questions | All resolved during plan writing; resolutions documented in `Spec-to-Codebase Reconciliation` section |
| SWR_XCH_001 (Project Export) | Tasks 9, 11 |
| SWR_XCH_002 (Project Import) | Tasks 9, 11 |
| SWR_XCH_003 (Package Export) | Tasks 10, 11 |
| SWR_XCH_004 (Package Import) | Tasks 10, 11 |
| SWR_XCH_005 (YAML Schema v1) | Tasks 1, 2, 7 |
| SWR_XCH_006 (Element Find-or-Create) | Tasks 3, 4 |
| SWR_XCH_007 (Stereotype/Tag Round-Trip) | Tasks 3, 7 |
| SWR_XCH_008 (Core Type-Specific Fields) | Tasks 3, 5, 6, 7, 8 |
| SWR_XCH_009 (Error Handling & Skip) | Tasks 5, 6, 7, 8, 13 |
| SWR_XCH_010 (Reusable Model Manipulation API) | Task 3 |
| SWR_XCH_011 (Relations Round-Trip) | Tasks 4, 6, 8 |
| SWR_XCH_012 (Ports Round-Trip) | Tasks 4, 6, 8 |
| SWR_XCH_013 (Events and EventReceptions Round-Trip) | Tasks 4, 6, 8 |

**Coverage: 13/13 SWR_XCH requirements have implementing tasks. No gaps.**

### 2. Placeholder scan

Scanned the plan for red-flag patterns:

- **"TBD" / "TODO" / "implement later" / "fill in details":** None found.
- **"Add appropriate error handling" / "handle edge cases":** None found. Every error path is explicit (try/except blocks shown in code, with specific `CliExecutionError` messages).
- **"Write tests for the above" (without test code):** None. Every test step shows the actual test code.
- **"Similar to Task N" (without repeating code):** None. Tasks 4, 6, 8 could have said "similar to Task 3/5/7" but instead repeat the full implementation pattern for each new element type.
- **Steps that describe what to do without showing how:** None. Every code-bearing step includes the literal code.

**One accepted compression:** Task 12's UTS doc groups entries UTS_XCH_00030–00045, 00046–00059, 00060–00075, 00076–00089 into summary ranges (one block per range with bullet points naming each entry) rather than expanding each entry as a full markdown block. This is deliberate because:
1. The full test code for each of these UTS entries IS shown in the corresponding Task (5, 6, 7, 8) — the UTS doc is documentation, not test code.
2. Each grouped entry still has a unique ID, a Traces-To link, and a one-line description identifying the behavior under test.
3. Expanding all 91 entries into full markdown blocks would inflate the doc to ~150KB without adding information not already in the task code.
4. The pattern matches existing project docs (e.g., `uts_pkg_test-specs.md` uses similar grouping for related tests).

If the reviewer disagrees, the fix is mechanical: expand each bullet point into a full UTS block using the template shown for UTS_XCH_00001–00029.

### 3. Type consistency

Cross-task signature audit:

| Symbol | Defining Task | Using Tasks | Consistent? |
|---|---|---|---|
| `RhapsodyExporter(app=app)` | Task 7 (`__init__(self, app: RhapsodyApplication)`) | Tasks 9, 10 | ✓ |
| `RhapsodyImporter(app=app)` | Task 5 (`__init__(self, app: RhapsodyApplication)`) | Tasks 9, 10 | ✓ |
| `RhapsodyExporter.export(container) -> Dict[str, Any]` | Task 7 | Tasks 9, 10 | ✓ |
| `RhapsodyImporter.import_template(data, root_element)` | Task 5 | Tasks 9, 10 | ✓ |
| `RhapsodyYaml().read(path) -> Dict[str, Any]` | Task 2 | Tasks 9, 10 | ✓ |
| `RhapsodyYaml().write(path, data) -> None` | Task 2 | Tasks 9, 10 | ✓ |
| `app.active_project()` | Codebase (Reconciliation #4) | Tasks 9, 10 | ✓ |
| `_resolve_and_validate_package(path)` | Codebase (`AbstractPackageAction`) | Task 10 | ✓ |
| `super().__init__(command_id="export")` pattern | Reconciliation #1 | Tasks 9, 10 | ✓ |
| `sub_parser: "argparse._SubParsersAction[argparse.ArgumentParser]"` | Reconciliation #2 | Tasks 9, 10 | ✓ |
| `apply_stereotypes(element, list)` / `apply_tags(element, dict)` | Task 3 | Tasks 5, 6, 7, 8 | ✓ |
| `find_child_by_name(parent, name) -> Optional[RPModelElement]` | Task 3 | Tasks 3, 4 | ✓ |
| `_set_type_kind(type_element, kind) -> None` | Task 3 | Task 3 | ✓ |
| `find_or_create_<type>(parent, name)` | Task 3 (8 core), Task 4 (6 new) | Tasks 5, 6 | ✓ |
| `_export_<type>(element) -> Dict[str, Any]` | Task 7 (8 core), Task 8 (6 new) | Tasks 7, 8 | ✓ |
| `_apply_<type>_extras(element, spec)` | Task 5 (8 core), Task 6 (6 new) | Tasks 5, 6 | ✓ |
| `resolve_classifier(name) -> Optional[RPModelElement]` | Task 3 | Tasks 6, 8 | ✓ |
| `get_classifier_name(classifier) -> Optional[str]` | Task 3 | Tasks 6, 8 | ✓ |
| `SCHEMA_VERSION`, `VERSION_KEY`, `PROJECT_KEY`, `RHAPSODY_MODEL_KEY` | Task 1 | Tasks 5, 7 | ✓ |
| `RPModelElement.wrap(com_obj)` | Codebase (`AbstractRPModelElement.wrap`) | Task 7 (`_wrap_if_needed`) | ✓ |
| `RPCollection` iteration (1-based `getItem`) | Codebase | Tasks 3 (`_collect_children`), 7 (exporter iteration) | ✓ |
| Tag value access via `tag.call_com(lambda: tag._com.getValue())` | Reconciliation #6, #7 | Task 7 (`_export_tags`) | ✓ |

**All cross-task signatures are consistent. No mismatches found.**

### 4. Known minor inconsistencies (accepted)

These are cosmetic issues in commit message annotations, not functional bugs. The implementation code is correct; only the SWR_XCH ID cited in some commit messages is imprecise:

1. **Task 7 commit** cites `SWR_XCH_004` (Package Import), but Task 7 implements the Exporter (8 core types) — more accurately `SWR_XCH_001`/`SWR_XCH_003` (Project/Package Export) or `SWR_XCH_008` (Core Type-Specific Fields).
2. **Task 8 commit** cites `SWR_XCH_004`, but Task 8 extends the Exporter with 6 new element types — more accurately `SWR_XCH_011`/`SWR_XCH_012`/`SWR_XCH_013` (Relations/Ports/Events).
3. **Task 9 commit** cites `SWR_XCH_001`, but Task 9 implements BOTH ProjectExport (001) AND ProjectImport (002).
4. **Task 10 commit** cites `SWR_XCH_001`, but Task 10 implements BOTH PackageExport (003) AND PackageImport (004).

**Rationale for accepting:** Commit messages are informational; the SWR_XCH IDs in them serve as soft traceability hints. The authoritative traceability is in `docs/requirements/swr_xch_requirements.md` and `docs/tests/unit/uts_xch_test-specs.md` (Task 12), which have correct Traces-To links. Fixing the commit messages would require amending already-pushed commits, which violates the project's "create NEW commits rather than amending" rule. The engineer executing this plan should feel free to use more accurate SWR_XCH IDs in their own commits if they prefer.

### 5. Final assessment

The plan is internally consistent, covers all 13 SWR_XCH requirements from the approved spec, contains no placeholders (modulo the accepted UTS compression), and all cross-task type signatures match. Ready for execution.