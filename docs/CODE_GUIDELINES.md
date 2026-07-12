# rhapsody-cli Code Guidelines

> **Core Principle:** Test-first, class-based architecture. Write tests before code. Organize code as classes, not functions.

---

## Naming Conventions

### Constants Must Be UPPERCASE

**All constants must use UPPERCASE with underscores (SCREAMING_SNAKE_CASE).**

Constants are values that:
- Never change after initialization
- Are defined at module or class level
- Apply globally or across multiple methods

**✅ CORRECT: Constants in UPPERCASE**
```python
# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
SUPPORTED_FORMATS = ("json", "csv", "xmi")

# Class-level constants
class RhapsodyContextAction(AbstractAction):
    _NO_ACTIVE_INSTANCE_MESSAGE = "No running Rhapsody instance found. Please open Rhapsody and a project first."
    BUFFER_SIZE = 1024
    REQUIRED_PERMISSIONS = {"read", "write"}
```

**❌ WRONG: Constants not in UPPERCASE**
```python
default_timeout = 30  # ❌ Looks like a variable
maxRetries = 3        # ❌ camelCase for constants
supported_formats = ("json", "csv")  # ❌ Lowercase for constants
```

### Other Naming Rules

- **Classes:** PascalCase (e.g., `ElementAddAction`, `RhapsodyContext`)
- **Functions/Methods:** snake_case (e.g., `add_verbose_argument`, `_get_active_project`)
- **Variables:** snake_case (e.g., `project_path`, `element_name`)
- **Private members:** Prefix with `_` (e.g., `_handle_connection_error`, `_NO_ACTIVE_INSTANCE_MESSAGE`)
- **Dunder methods:** Double underscores (e.g., `__init__`, `__str__`)

---

## Python Compatibility & Imports

### ❌ DO NOT USE: `from __future__ import annotations`

**This import is FORBIDDEN.** Remove it from all files immediately if found.

### Why?

- **Already fixed once:** This issue has been resolved across the entire codebase. Do not reintroduce it.
- **Runtime overhead:** Defers all annotations, causing issues with type checkers and runtime reflection.
- **Unnecessary complexity:** We support Python 3.8+ with explicit type hints—no need to defer evaluation.
- **Breaks mypy strict mode:** Type checking becomes unreliable.

### ❌ WRONG:
```python
from __future__ import annotations

def my_function() -> str:
    return "hello"
```

### ✅ CORRECT:
```python
def my_function() -> str:
    return "hello"
```

### Handling Forward References (When Needed)

If you need forward references to undefined types, use string quotes:

```python
class Node:
    def __init__(self, value: int, next_node: 'Node | None' = None):
        self.value = value
        self.next_node = next_node
```

Or use conditional imports and `TYPE_CHECKING`:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhapsody_cli.cli.context import RhapsodyContext

class MyAction:
    def __init__(self, ctx: 'RhapsodyContext'):
        self.ctx = ctx
```

### Import Order & Organization

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

---

## TDD Methodology

### Principle: Tests First

All code must follow strict Test-Driven Development (TDD):

1. **Write tests BEFORE implementation**
2. **Watch tests fail** (red)
3. **Write minimal code to pass** (green)
4. **Refactor while keeping tests passing** (refactor)

### Why Tests First?

- **Design clarity:** Writing tests forces you to think about interfaces and behavior first
- **Better coverage:** You naturally cover more edge cases and error paths
- **Refactoring confidence:** Changes are safe when tests verify behavior
- **Documentation:** Tests document intended behavior
- **Debugging ease:** Failing tests isolate problems quickly

### Coverage Target

- **Minimum:** 80% code coverage
- **Target:** 90%+ code coverage
- **Exceptions:** Fixtures, setup/teardown code, trivial properties may be excluded

### Test Organization

```
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

### Test Naming Convention

- **Test modules:** `test_<component>.py` (e.g., `test_context.py`)
- **Test classes:** `Test<Component>` (e.g., `TestRhapsodyContext`)
- **Test methods:** `test_<behavior>_<condition>_<result>` (e.g., `test_open_project_with_invalid_path_raises_error`)

### Example: TDD for a New CLI Command

#### Step 1: Write Tests FIRST

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

#### Step 2: Implement Minimal Code

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

#### Step 3: Run Tests

```bash
pytest tests/unit/commands/test_element_command.py::TestElementCommandDispatch -v
```

---

## Class-Based Architecture

### Principle: Classes Over Functions

All code should be organized as classes, not module-level functions:

- **CLI commands** → Command groups (inherit from `AbstractCommand`) and actions (inherit from `AbstractAction`)
- **Utilities** → Utility classes with methods (not static functions)
- **Formatters** → Formatter instances (not static methods)
- **Managers** → Manager classes (not helper functions)

### Why Classes?

- **Encapsulation:** State + behavior together
- **Testability:** Easy to mock and inject dependencies
- **Reusability:** Classes can be extended via inheritance
- **Organization:** Related functions grouped logically
- **Type safety:** Better IDE support and type checking

### Shared Attributes in Base Classes

Base classes should define shared attributes (constants, loggers, utilities) to prevent duplication in subclasses:

**✅ CORRECT: Share common resources in base class**
```python
import logging

class AbstractAction:
    """Base action class with shared logger."""
    
    name: str = ""
    logger: logging.Logger = logging.getLogger(__name__)
    
    def execute(self) -> None:
        self.logger.info("Action started")


class MyAction(AbstractAction):
    name = "myaction"
    
    def execute(self) -> None:
        self.logger.info("MyAction executing")  # Uses inherited logger
```

**❌ WRONG: Duplicate logger in every subclass**
```python
class MyAction(AbstractAction):
    logger = logging.getLogger(__name__)  # Redundant! Already in parent
    
    def execute(self) -> None:
        self.logger.info("MyAction executing")
```

Benefits:
- Single point of configuration
- Consistent behavior across subclasses
- Eliminates boilerplate code
- Easier maintenance

### When to Use Functions

Functions are acceptable only for:
- **Decorators** (e.g., `@pytest.fixture`)
- **Lambdas** in comprehensions (e.g., `map(lambda x: x * 2, items)`)
- **Module-level helpers** (private functions prefixed with `_`) used only within one file

### Anti-Pattern: Static Methods Everywhere

❌ **Avoid:**
```python
class OutputFormatter:
    @staticmethod
    def table(headers, rows):
        ...
    
    @staticmethod
    def json(headers, rows):
        ...
```

✅ **Prefer:**
```python
from typing import Any, List

class OutputFormatter:
    def __init__(self, format_type: str = "table"):
        self.format_type = format_type

    def format(self, headers: List[str], rows: List[List[Any]]) -> str:
        if self.format_type == "table":
            return self._format_table(headers, rows)
        elif self.format_type == "json":
            return self._format_json(headers, rows)

    def _format_table(self, headers, rows):
        ...

    def _format_json(self, headers, rows):
        ...
```

---

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
    except RhapsodyConnectionError as e:
        self._handle_connection_error(e)  # logs and raises CliExecutionError
    except Exception as e:
        self._handle_execution_error(e, "Operation")  # logs and raises CliExecutionError
```

> **Rule: No `print()` for status/error messages; no `sys.exit()` outside `cli.main()`.**
> See "No print()/sys.exit() Rule" under Utility Classes below for the full rationale and pattern.

---

## Utility Classes

### Logger Pattern

All action and utility classes should inherit or use a shared logger from their base class:

```python
class AbstractAction:
    """Base class for CLI actions."""
    
    logger: logging.Logger = logging.getLogger(__name__)
    
    def execute(self, args: argparse.Namespace) -> None:
        self.logger.info("Starting action")
```

**Why:**
- Centralized logger configuration in one place
- Consistent logging across all actions
- Subclasses use `self.logger` without redeclaring
- Reduces code duplication

**DO NOT:** Create duplicate loggers in subclasses
```python
# ❌ WRONG - Duplicate logger in subclass
class MyAction(AbstractAction):
    logger = logging.getLogger(__name__)  # Redundant!
```

**DO:** Use inherited logger
```python
# ✅ CORRECT - Use inherited logger
class MyAction(AbstractAction):
    def execute(self, args: argparse.Namespace) -> None:
        self.logger.info("Action executed")  # Uses parent's logger
```

---

### No `print()` / `sys.exit()` Rule

**Rule:** CLI code (actions, command groups) must not use `print()` for status,
success, or error messages, and must not call `sys.exit()` directly. Use the
logger for messages and raise `CliExecutionError` for fatal errors instead.

**Why:**
- `print()` bypasses log level filtering, verbosity flags (`-v`/`--verbose`),
  and any future log redirection/formatting.
- Scattered `sys.exit()` calls make control flow hard to test and centralize;
  every call site becomes a hard process-exit boundary that tests must trap.
- A single, well-known exception type makes error handling composable and
  testable with plain `pytest.raises(...)`, without needing to inspect
  process-level `SystemExit.code`.

**The pattern:**

```python
from rhapsody_cli.exceptions import CliExecutionError

class MyAction(RhapsodyContextAction):
    def execute(self, args: argparse.Namespace) -> None:
        if not args.name:
            self.logger.error("Missing required --name argument")
            raise CliExecutionError("Missing required --name argument")

        # Status/success messages go through the logger, not print()
        self.logger.info("Created element '%s'", args.name)
```

`_handle_connection_error` / `_handle_execution_error` (on `RhapsodyContextAction`)
already implement this pattern — they log the error and raise
`CliExecutionError`, annotated `-> NoReturn`, so callers never need a
`sys.exit()`/`except SystemExit: raise` fallback afterward.

**The one sanctioned exception:** actual *result/data* output that users pipe
or redirect (e.g. `element view`/`element query` tables or JSON, `project list`
tables) stays on `print()` to stdout. This is deliberate — the logger's
`StreamHandler` writes to stderr and prepends timestamps/levels, which would
break piping (`rhapsody-cli element query --output json > elements.json`).
Mark these call sites with a short `NOTE:` comment explaining why `print()` is
used there.

**`sys.exit()` boundary:** `rhapsody_cli.cli.cli.main()` is the *only* place
that calls `sys.exit()` for our own errors — it catches `CliExecutionError`
and exits with `e.exit_code`:

```python
except CliExecutionError as e:
    logger.error(str(e))
    sys.exit(e.exit_code)
```

Argparse's own `SystemExit` (malformed CLI args) and `KeyboardInterrupt`
handling are framework/boundary behavior and are not subject to this rule.

**DO NOT:**
```python
# ❌ WRONG
print(f"Error: {e}", file=sys.stderr)
sys.exit(1)
```

**DO:**
```python
# ✅ CORRECT
self.logger.error("Error: %s", e)
raise CliExecutionError(f"Error: {e}") from e
```

---

### OutputFormatter Pattern

```python
from typing import Any, List

class OutputFormatter:
    """Formats output data for CLI display."""

    SUPPORTED_FORMATS = ("table", "json", "csv")

    def __init__(self, format_type: str = "table"):
        if format_type not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format_type}")
        self.format_type = format_type

    def format(self, headers: List[str], rows: List[List[Any]]) -> str:
        """Format data according to configured format type."""
        if self.format_type == "table":
            return self._format_table(headers, rows)
        elif self.format_type == "json":
            return self._format_json(headers, rows)
        elif self.format_type == "csv":
            return self._format_csv(headers, rows)
        else:
            raise ValueError(f"Unknown format: {self.format_type}")

    def _format_table(self, headers: List[str], rows: List[List[Any]]) -> str:
        """Format as ASCII table."""
        if not rows:
            return "(no data)"
        return str(tabulate(rows, headers=headers, tablefmt="grid"))

    def _format_json(self, headers: List[str], rows: List[List[Any]]) -> str:
        """Format as JSON."""
        data = [dict(zip(headers, row)) for row in rows]
        return json.dumps(data, indent=2, default=str)

    def _format_csv(self, headers: List[str], rows: List[List[Any]]) -> str:
        """Format as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()
```

### Context Manager Pattern

```python
from typing import Optional

class RhapsodyContext:
    """Manages session state for CLI commands."""

    def __init__(self):
        self._app: Optional[RhapsodyApplication] = None
        self._project: Optional[RPProject] = None
        self._output_format: str = "table"

    @property
    def app(self) -> Optional[RhapsodyApplication]:
        return self._app

    @property
    def project(self) -> Optional[RPProject]:
        return self._project

    @property
    def output_format(self) -> str:
        return self._output_format

    @output_format.setter
    def output_format(self, value: str) -> None:
        if value not in ("table", "json", "csv"):
            raise ValueError(f"Unknown format: {value}")
        self._output_format = value

    def connect(self, method: str = "attach") -> RhapsodyApplication:
        """Connect to Rhapsody instance."""
        if self._app is None:
            if method == "attach":
                self._app = RhapsodyApplication.attach()
            else:
                self._app = RhapsodyApplication.launch()
        return self._app

    def open_project(self, project_path: str) -> RPProject:
        """Open a project file."""
        if self._app is None:
            self.connect()
        assert self._app is not None
        self._project = self._app.open_project(project_path)
        return self._project

    def close_project(self) -> None:
        """Close active project."""
        if self._project:
            self._project.close()
            self._project = None

    def disconnect(self) -> None:
        """Disconnect from Rhapsody."""
        self.close_project()
        if self._app:
            self._app.quit()
            self._app = None
```

---

## Testing Patterns

### Arrange-Act-Assert Pattern

All tests follow AAA structure:

```python
from typing import Any, List

def test_formatter_handles_empty_rows():
    """Test: Formatter handles empty rows gracefully."""
    # ARRANGE
    formatter = OutputFormatter("table")
    headers = ["Name", "Value"]
    rows: List[List[Any]] = []

    # ACT
    result = formatter.format(headers, rows)

    # ASSERT
    assert result == "(no data)"
```

### Mocking COM Objects

```python
from unittest.mock import Mock, MagicMock

def test_context_open_project_calls_app_open_project():
    """Test: RhapsodyContext.open_project delegates to app."""
    # ARRANGE
    ctx = RhapsodyContext()
    mock_app = Mock(spec=RhapsodyApplication)
    mock_project = Mock(spec=RPProject)
    mock_app.open_project.return_value = mock_project
    ctx._app = mock_app
    
    # ACT
    result = ctx.open_project("/path/to/project.rpy")
    
    # ASSERT
    assert result == mock_project
    mock_app.open_project.assert_called_once_with("/path/to/project.rpy")
```

### CLI Integration Tests

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

### Parameterized Tests

```python
@pytest.mark.parametrize("format_type,expected", [
    ("table", "(no data)"),
    ("json", "[]"),
    ("csv", ""),
])
def test_formatter_handles_empty_rows_for_all_formats(format_type, expected):
    """Test: Formatter handles empty rows for all format types."""
    formatter = OutputFormatter(format_type)
    result = formatter.format([], [])
    assert expected in result or result == expected
```

### Fixtures for Reusable Test Data

```python
@pytest.fixture
def mock_context():
    """Fixture: Create a mock RhapsodyContext for testing."""
    ctx = RhapsodyContext()
    ctx._app = Mock(spec=RhapsodyApplication)
    ctx._project = Mock(spec=RPProject)
    return ctx

@pytest.fixture
def formatter():
    """Fixture: Create an OutputFormatter for testing."""
    return OutputFormatter("table")

def test_something_with_context(mock_context):
    """Test using mock_context fixture."""
    # Use mock_context
    assert mock_context.app is not None
```

---

## Code Review Checklist

All code reviews must verify:

### Python Compatibility
- [ ] **NO `from __future__ import annotations`** (this is forbidden)
- [ ] All imports organized (stdlib → third-party → local)
- [ ] No unused imports?

### TDD Requirements
- [ ] Tests written BEFORE implementation?
- [ ] All new behaviors have corresponding tests?
- [ ] Tests cover happy path?
- [ ] Tests cover error cases?
- [ ] Tests cover edge cases?
- [ ] Code coverage ≥ 80% (preferably 90%+)?

### Class-Based Architecture
- [ ] No module-level functions (except decorators and helpers)?
- [ ] CLI commands use command classes (not decorators)?
- [ ] Utilities implemented as classes with methods?
- [ ] Classes have clear responsibility (single purpose)?
- [ ] Inheritance used appropriately (not overused)?

### Code Quality
- [ ] Type annotations complete?
- [ ] Docstrings present for all public methods?
- [ ] Error handling with `raise ... from e`?
- [ ] Private methods prefixed with `_`?
- [ ] Constants in UPPER_CASE?
- [ ] No unused imports or variables?

### Naming Conventions
- [ ] **CONSTANTS in UPPER_CASE** (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`, `SUPPORTED_FORMATS`)
- [ ] **Classes in PascalCase** (e.g., `ElementAddAction`, `RhapsodyContext`)
- [ ] **Functions/methods in snake_case** (e.g., `add_verbose_argument`, `_get_active_project`)
- [ ] **Variables in snake_case** (e.g., `project_path`, `element_type`)
- [ ] **Private members prefixed with `_`** (e.g., `_NO_ACTIVE_INSTANCE_MESSAGE`, `_handle_error`)
- [ ] No camelCase outside of dunder methods?

### Specific to CLI Commands
- [ ] Action inherits from `AbstractAction` (or `RhapsodyContextAction` / `ElementManagementAction`)?
- [ ] Arguments registered in `init_arguments()` via `sub_parser.add_parser(...)`?
- [ ] Logic in `execute(args: argparse.Namespace)` method?
- [ ] Error handling uses `_handle_connection_error` / `_handle_execution_error`, which log and raise `CliExecutionError` (never `sys.exit()` directly)?
- [ ] Status/success/error messages use `self.logger` (never `print()`)? Result/data output (tables, JSON) may still use `print()` to stdout.

### Specific to Tests
- [ ] Uses Arrange-Act-Assert pattern?
- [ ] Mocks external dependencies (COM, file I/O)?
- [ ] Test name describes behavior?
- [ ] No test interdependencies?
- [ ] Fixtures used for reusable data?

---

## Examples in Codebase

### Current Examples (Refactoring Target)

See the following for before/after refactoring:

- **CLI commands:** `src/rhapsody_cli/commands/`
- **CLI actions:** `src/rhapsody_cli/actions/`
- **Formatters:** `src/rhapsody_cli/cli/formatters.py`
- **Context:** `src/rhapsody_cli/cli/context.py`
- **Tests:** `tests/unit/`

### Future Examples

After refactoring completes, this directory will contain exemplary class-based, test-first code for reference.

---

## Questions?

For clarification on these guidelines, refer to:
- **TDD Resources:** [pytest documentation](https://pytest.org)
- **argparse:** [argparse documentation](https://docs.python.org/3/library/argparse.html)
- **Python OOP:** [Real Python OOP Guide](https://realpython.com/python3-object-oriented-programming/)

---

**Last Updated:** 2024  
**Author:** rhapsody-cli development team  
**Status:** Active - Applied to all new code and ongoing refactoring
