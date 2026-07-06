# Copilot Instructions for py-rhapsody

## Quick Reference

**Language:** Python 3.8+  
**Build System:** setuptools (src-layout)  
**Testing:** pytest with unit tests only (no Rhapsody installation required)  
**Quality Tools:** ruff (linting), black (formatting), mypy (type checking)  
**CLI Framework:** Click with class-based command architecture

---

## Build & Test Commands

### Installation

```bash
pip install -e ".[dev,cli]"  # Full dev setup: required to run the full test suite (CLI tests need click/tabulate/rich)
pip install -e ".[dev]"      # Dev tools only (ruff/black/mypy/pytest) - tests/cli/* will fail to import
pip install -e ".[cli]"      # CLI runtime dependencies only
pip install -e .             # Install package only (pywin32 on Windows)
```

### Testing

```bash
pytest                       # Run all tests
pytest tests/cli/            # Run only CLI tests
pytest tests/elements/       # Run only element tests
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
mypy src/ tests/            # Type checking (Python 3.9 strict mode)
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
git add src/py_rhapsody/models/elements/myclass.py tests/elements/test_myclass.py
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

**py-rhapsody** is a Pythonic wrapper around the IBM Rhapsody COM API. It consists of three layers:

1. **Core Model Wrapping** (`src/py_rhapsody/models/`)
   - Base class `RPModelElement` wraps all Rhapsody COM objects
   - Element subclasses mirror Rhapsody Java API (e.g., `RPClass`, `RPPackage`, `RPAttribute`)
   - Wrapper registry pattern: each element module registers its wrapper class in `_WRAPPER_REGISTRY`
   - `call_com()` translates COM failures to `RhapsodyRuntimeException`

2. **Application Entry Point** (`src/py_rhapsody/application.py`)
   - `RhapsodyApplication` handles Rhapsody connection (attach/launch)
   - Supports three connection modes: `attach()` (existing instance), `launch()` (new instance), `connect()` (try attach then launch)

3. **CLI Layer** (`src/py_rhapsody/cli/`)
   - Click-based command-line interface using class-based architecture
   - Command groups: `project`, `element`, `io`
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
- Java: `com.telelogic.rhapsody.core.IRPClass` → Python: `py_rhapsody.models.elements.class_.RPClass`
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
# ✅ CORRECT: Class-based command
class OpenProjectCommand(click.Command):
    def __init__(self) -> None:
        super().__init__(
            name="open",
            help="Open a Rhapsody project file.",
            callback=self.execute,
            params=[click.Argument(["project_path"], type=click.Path(exists=True))],
        )

    def execute(self, project_path: str) -> None:
        """Business logic here."""
        ...

# ❌ WRONG: Function-based with decorators
@click.command()
@click.argument("project_path")
def open_project(project_path):
    ...
```

**Command groups** inherit from `click.Group` and add subcommands in `__init__`:

```python
class ProjectCommandGroup(click.Group):
    def __init__(self) -> None:
        super().__init__(name="project", help="Project commands")
        self.add_command(OpenProjectCommand())
        self.add_command(ListProjectsCommand())
        ...
```

### Wrapper Registry Pattern

New element types must register themselves with the wrapper registry:

```python
# In src/py_rhapsody/models/elements/myclass.py
from py_rhapsody.models._core import register_wrapper, RPModelElement

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
- CLI commands re-raise `click.Abort` without modification, wrap other errors

```python
try:
    ctx.connect("attach")
except RhapsodyConnectionError as e:
    click.echo(f"Connection error: {e}", err=True)
    raise click.Abort() from e
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
src/py_rhapsody/
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
│       ├── class_.py             # RPClass
│       ├── attribute.py          # RPAttribute
│       └── ...
├── cli/                           # CLI commands (class-based)
│   ├── main.py                   # CLI root group
│   ├── context.py                # RhapsodyContext (state management)
│   ├── formatters.py             # OutputFormatter (table/JSON/CSV)
│   └── commands/
│       ├── __init__.py
│       ├── project.py            # ProjectCommandGroup
│       ├── element.py            # ElementCommandGroup
│       └── io.py                 # IOCommandGroup
└── py.typed                       # PEP 561 marker (type stubs available)

tests/
├── fakes.py                      # Fake COM objects for testing
├── test_application.py           # Tests for RhapsodyApplication
├── test_core.py                  # Tests for wrap(), call_com(), registry
├── cli/
│   ├── test_command_classes.py  # Tests for CLI command classes
│   ├── test_element_commands.py  # Tests for element commands
│   └── test_io_commands.py       # Tests for io commands
└── elements/
    ├── test_class.py            # Tests for RPClass
    ├── test_attribute.py        # Tests for RPAttribute
    └── ...
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
5. **Class-based CLI commands** — never function-based
6. **Type annotations on all functions** — mypy strict mode enforces this
7. **Run quality gates:** `ruff check`, `black --check`, `mypy`, `pytest`

---

## Common Tasks

### Add a new element wrapper

1. Create `src/py_rhapsody/models/elements/myclass.py`
2. Define `RPMyClass(RPModelElement)` with method mirrors
3. Call `register_wrapper("MyClass", RPMyClass)` at module level
4. Write tests in `tests/elements/test_myclass.py` with fakes
5. Add to `src/py_rhapsody/models/elements/__init__.py` exports

### Add a new CLI command

1. Write tests first in appropriate `tests/cli/test_*.py` module
2. Create command class inheriting from `click.Command`
3. Implement `execute()` method with business logic
4. Add to appropriate command group (project/element/io)
5. Verify all CLI tests pass

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

- **Design & Architecture:** `docs/superpowers/specs/2026-07-06-py-rhapsody-com-api-design.md`
- **Code Guidelines (TDD/Classes):** `docs/CODE_GUIDELINES.md`
- **Rhapsody Java API:** https://www.ibm.com/docs/en/rhapsody (method/class reference)
- **Click CLI Documentation:** https://click.palletsprojects.com/
