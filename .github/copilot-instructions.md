# Copilot Instructions for rhapsody-cli

## Quick Reference

**Language:** Python 3.8+  
**Build System:** setuptools (src-layout)  
**Testing:** pytest with unit tests only (no Rhapsody installation required)  
**Quality Tools:** ruff (linting), black (formatting), mypy (type checking)  
**CLI Framework:** argparse (stdlib) with class-based command/action architecture

---

## Build & Test Commands

### Installation

```bash
pip install -e ".[dev,cli]"  # Full dev setup: required to run the full test suite (CLI tests need tabulate/rich)
pip install -e ".[dev]"      # Dev tools only (ruff/black/mypy/pytest) - tests that import tabulate/rich will fail
pip install -e ".[cli]"      # CLI runtime dependencies only
pip install -e .             # Install package only (pywin32 on Windows)
```

### Testing

```bash
pytest                       # Run all tests
pytest tests/unit/cli/               # Run only CLI unit tests
pytest tests/unit/models/elements/   # Run only element tests
pytest tests/test_core.py   # Run single test module
pytest -k "test_open"       # Run tests matching pattern
pytest -v                   # Verbose output
pytest --co                 # List all tests without running
```

### Linting & Formatting

```bash
ruff check src/ tests/      # Run linter
ruff check src/ tests/ --fix # Auto-fix issues
black --check src/ tests/   # Check formatting
black src/ tests/           # Auto-format
mypy src/ tests/            # Type checking (strict mode, python_version 3.9)
```

### Running Everything

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest
```

---

## Git Workflow

### Mandatory Rules

**1. Do NOT add Copilot as co-author**

Never include `Co-authored-by: Copilot` in commits. Each commit must be authored by the human developer only:

```bash
# ✅ CORRECT: Human-authored only
git commit -m "feat: add new model element"

# ❌ WRONG: Do not add Copilot trailer
git commit -m "feat: add new model element

Co-authored-by: Copilot <...@users.noreply.github.com>"
```

**2. All changes go to feature branches, NEVER directly to main**

Always work on a feature branch. Main is reserved for tested, production-ready code:

```bash
# ✅ CORRECT: Work on feature branch
git checkout -b feature/add-new-element
# ... make changes ...
git commit -m "feat: add element wrapper for MyClass"
git push -u origin feature/add-new-element

# ❌ WRONG: Never commit directly to main
git checkout main
git commit -m "..."  # ✗ FORBIDDEN
git push origin main
```

### Feature Branch Workflow

```bash
# 1. Create and switch to feature branch
git checkout -b feature/<type>-<short-description>

# 2. Make changes, test, commit (locally on feature branch)
git add src/rhapsody_cli/models/elements/myclass.py tests/elements/test_myclass.py
git commit -m "feat: add RPMyClass element wrapper"

# 3. Push to origin
git push -u origin feature/<type>-<short-description>

# 4. Create pull request on GitHub for review
# (via gh pr create or GitHub web UI)

# 5. After PR approval and merge, delete local branch
git checkout main
git pull origin main
git branch -d feature/<type>-<short-description>
```

### Branch Naming Convention

Use kebab-case with a type prefix:

- `feature/add-element-wrapper` — New functionality
- `fix/connection-error-handling` — Bug fix
- `refactor/class-based-element` — Code reorganization
- `docs/update-guidelines` — Documentation only

---

## Architecture

### High-Level Overview

**rhapsody-cli** is a Pythonic wrapper around the IBM Rhapsody COM API. It consists of three layers:

1. **Core Model Wrapping** (`src/rhapsody_cli/models/`)
   - Base class `RPModelElement` wraps all Rhapsody COM objects
   - Element subclasses mirror Rhapsody Java API (e.g., `RPClass`, `RPPackage`, `RPAttribute`)
   - Wrapper registry pattern: each element module registers its wrapper class in `_WRAPPER_REGISTRY`
   - `call_com()` translates COM failures to `RhapsodyRuntimeException`

2. **Application Entry Point** (`src/rhapsody_cli/application.py`)
   - `RhapsodyApplication` handles Rhapsody connection (attach/launch)
   - Supports three connection modes: `attach()` (existing instance), `launch()` (new instance), `connect()` (try attach then launch)

3. **CLI Layer** (`src/rhapsody_cli/cli/` + `src/rhapsody_cli/commands/` + `src/rhapsody_cli/actions/`)
   - argparse-based (stdlib) CLI using a class-based command/action architecture
   - `main()` dispatches on the first argv token to an `AbstractCommand` subclass
   - Command groups (`ElementCommand`, `ProjectCommand`, `IOCommand`) each own a set of `AbstractAction` subcommands
   - Each action registers its own argparse subparser (`init_arguments`) and owns its execution (`execute`)
   - Context: `RhapsodyContext` manages the current Rhapsody state
   - Formatters: `OutputFormatter` handles table/JSON/CSV output

### Key Data Flow

```
User CLI Input
    ↓
CLI Command (class-based) → RhapsodyContext → RhapsodyApplication
    ↓
COM Call wrapped in call_com()
    ↓
RPModelElement (wrapper class from registry)
    ↓
Formatted Output (table/JSON/CSV)
```

### API Mirroring

Method names and class hierarchy **exactly mirror** the Rhapsody Java API (`com.telelogic.rhapsody.core`):
- Java: `com.telelogic.rhapsody.core.IRPClass` → Python: `rhapsody_cli.models.elements.class_.RPClass`
- Java: `getNestedElements()` → Python: `getNestedElements()`
- COM errors become `RhapsodyRuntimeException` for consistent error handling

---

## Key Conventions

### Test-Driven Development (TDD)

**Mandatory:** All code changes must follow strict TDD:

1. Write tests **BEFORE** implementation
2. Watch tests fail (red phase)
3. Write minimal code to pass (green phase)
4. Refactor while keeping tests passing (refactor phase)

**Coverage targets:** 80% minimum, 90%+ preferred. See `docs/CODE_GUIDELINES.md` for full details.

### Class-Based Architecture

**Mandatory for CLI:** All CLI commands must be class-based (not function-based with decorators):

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

### Wrapper Registry Pattern

New element types must register themselves with the wrapper registry:

```python
# In src/rhapsody_cli/models/elements/myclass.py
from rhapsody_cli.models._core import register_wrapper, RPModelElement

class RPMyClass(RPModelElement):
    """Wraps IRPMyClass."""
    pass

register_wrapper("MyClass", RPMyClass)
```

This enables automatic dispatch: `wrap(com_object)` returns the correct subclass.

### Error Handling

- Use `call_com(lambda: ...)` to wrap all COM calls
- Catch `RhapsodyConnectionError` for connection issues
- Catch `RhapsodyRuntimeException` for COM API failures
- CLI actions use `sys.exit(1)` for errors after logging via `_handle_connection_error` / `_handle_execution_error`

```python
try:
    ctx.connect("attach")
except RhapsodyConnectionError as e:
    self._handle_connection_error(e)
    sys.exit(1)
```

### Type Annotations

- **Python 3.8 compatibility:** Use `from __future__ import annotations` for forward refs
- **mypy strict mode:** All functions must have return type annotations (`-> None`, `-> int`, etc.)
- **COM API:** Use `# type: ignore[attr-defined]` sparingly for win32com/pywintypes lacking stubs

```python
from __future__ import annotations

def open_project(path: str) -> None:  # ✅ Required return annotation
    com_obj = call_com(lambda: self._com.openProject(path))  # ✅ COM call wrapped
```

### Testing with Fakes

All unit tests use fake COM objects (see `tests/fakes.py`). Never use real COM calls in tests:

```python
from tests.fakes import make_fake_element, make_fake_collection

# Create fake Class element with name
fake_class = make_fake_element("Class", getName="MyClass")

# Create fake collection
fake_items = make_fake_collection([fake_class])
```

No Rhapsody installation or license is required to run the full test suite.

### Code Layout

```
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

### GitHub Actions CI/CD

- **CI:** `python-package.yml` runs tests, linting, formatting, type checking on push/PR
- **CD:** `python-publish.yml` auto-publishes to PyPI on GitHub release
- Tests run across Python 3.8-3.13 matrix

---

## When Adding Features

1. **Read `docs/CODE_GUIDELINES.md`** — comprehensive TDD and architecture patterns
2. **Write tests first** — then implementation
3. **Use `call_com(lambda: ...)`** for all COM calls
4. **Register new element wrappers** in the wrapper registry
5. **Class-based CLI actions** — never function-based or Click-decorator-based
6. **Type annotations on all functions** — mypy strict mode enforces this
7. **Run quality gates:** `ruff check`, `black --check`, `mypy`, `pytest`

---

## Common Tasks

### Add a new element wrapper

1. Create `src/rhapsody_cli/models/elements/myclass.py`
2. Define `RPMyClass(RPModelElement)` with method mirrors
3. Call `register_wrapper("MyClass", RPMyClass)` at module level
4. Write tests in `tests/unit/models/elements/test_myclass.py` with fakes
5. Add to `src/rhapsody_cli/models/elements/__init__.py` exports

### Add a new CLI command

1. Write tests first in appropriate tests/unit/cli/ or tests/unit/commands/ module
2. Create an action class inheriting from AbstractAction (or RhapsodyContextAction / ElementManagementAction)
3. Implement init_arguments() to register the subparser and execute() for business logic
4. Register the action in the appropriate command group's get_actions() (element/project/io)
5. Verify all unit tests pass

### Fix a type checking error

mypy strict mode can be strict. Common patterns:

```python
# ✅ Optional handling
if value is not None:
    use_value(value)

# ✅ Type narrowing
if isinstance(obj, MyClass):
    obj.my_method()

# ✅ Explicit cast when necessary
from typing import cast
result = cast(str, com_call())
```

---

## References

- **Design & Architecture:** `docs/superpowers/specs/2026-07-06-rhapsody-cli-com-api-design.md`
- **Code Guidelines (TDD/Classes):** `docs/CODE_GUIDELINES.md`
- **Rhapsody Java API:** https://www.ibm.com/docs/en/rhapsody (method/class reference)
- **argparse documentation:** https://docs.python.org/3/library/argparse.html
