# rhapsody-cli Code Guidelines

> **Core Principle:** Test-first, class-based architecture. Write tests before code. Organize code as classes, not functions.

## Table of Contents

1. [TDD Methodology](#tdd-methodology)
2. [Class-Based Architecture](#class-based-architecture)
3. [CLI Commands](#cli-commands)
4. [Utility Classes](#utility-classes)
5. [Testing Patterns](#testing-patterns)
6. [Code Review Checklist](#code-review-checklist)

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

### Test Naming Convention

- **Test modules:** `test_<component>.py` (e.g., `test_context.py`)
- **Test classes:** `Test<Component>` (e.g., `TestRhapsodyContext`)
- **Test methods:** `test_<behavior>_<condition>_<result>` (e.g., `test_open_project_with_invalid_path_raises_error`)

### Example: TDD for a New CLI Command

#### Step 1: Write Tests FIRST

```python
# tests/cli/test_commands.py
import pytest
from click.testing import CliRunner
from rhapsody_cli.cli.commands.project import OpenProjectCommand
from rhapsody_cli.cli.context import RhapsodyContext

class TestOpenProjectCommand:
    def test_open_project_with_valid_path_succeeds(self):
        """Test: OpenProjectCommand opens project with valid path."""
        runner = CliRunner()
        cmd = OpenProjectCommand()
        
        # Mock context
        ctx = RhapsodyContext()
        
        result = runner.invoke(cmd, ["valid_project.rpy"])
        assert result.exit_code == 0
        assert "Opened project" in result.output
    
    def test_open_project_with_invalid_path_fails(self):
        """Test: OpenProjectCommand fails with non-existent path."""
        runner = CliRunner()
        cmd = OpenProjectCommand()
        
        result = runner.invoke(cmd, ["nonexistent.rpy"])
        assert result.exit_code != 0
        assert "Error" in result.output
    
    def test_open_project_with_connection_error_shows_message(self):
        """Test: OpenProjectCommand displays connection error gracefully."""
        runner = CliRunner()
        cmd = OpenProjectCommand()
        
        # Test error handling
        result = runner.invoke(cmd, ["project.rpy"])
        # Should show helpful error, not traceback
        assert "Connection error" not in result.output or "traceback" not in result.output.lower()
```

#### Step 2: Implement Minimal Code

```python
# src/rhapsody_cli/cli/commands/project.py
class OpenProjectCommand(click.Command):
    def __init__(self):
        super().__init__(
            name="open",
            help="Open a Rhapsody project file.",
            callback=self.execute,
            params=[
                click.Argument(["project_path"], type=click.Path(exists=True)),
            ],
        )
    
    def execute(self, project_path: str) -> None:
        try:
            ctx = RhapsodyContext()
            ctx.connect("attach")
            ctx.open_project(project_path)
            click.echo(f"Opened project: {project_path}")
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e
```

#### Step 3: Run Tests

```bash
pytest tests/cli/test_commands.py::TestOpenProjectCommand -v
```

---

## Class-Based Architecture

### Principle: Classes Over Functions

All code should be organized as classes, not module-level functions:

- **CLI commands** → Command classes (inherit from `click.Command`)
- **Utilities** → Utility classes with methods (not static functions)
- **Formatters** → Formatter instances (not static methods)
- **Managers** → Manager classes (not helper functions)

### Why Classes?

- **Encapsulation:** State + behavior together
- **Testability:** Easy to mock and inject dependencies
- **Reusability:** Classes can be extended via inheritance
- **Organization:** Related functions grouped logically
- **Type safety:** Better IDE support and type checking

### When to Use Functions

Functions are acceptable only for:
- **Decorators** (e.g., `@pytest.fixture`, `@click.pass_context`)
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
class OutputFormatter:
    def __init__(self, format_type: str = "table"):
        self.format_type = format_type
    
    def format(self, headers: list[str], rows: list[list[Any]]) -> str:
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

### Command Class Pattern

All Click commands must use command classes, not decorators:

#### Structure

```python
class BaseCommand(click.Command):
    """Base class for all CLI commands."""
    
    def __init__(self, name: str, help: str, callback, params):
        super().__init__(name=name, help=help, callback=callback, params=params)
    
    def execute(self, **kwargs) -> None:
        """Override in subclasses to implement command logic."""
        raise NotImplementedError


class MyCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="mycommand",
            help="Description of my command.",
            callback=self.execute,
            params=[
                click.Argument(["arg_name"], type=str),
                click.Option(["--option"], type=str, default="default"),
            ],
        )
    
    def execute(self, arg_name: str, option: str) -> None:
        """Execute the command."""
        try:
            # Implementation
            click.echo(f"Executed with {arg_name} and {option}")
        except click.Abort:
            raise
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e
```

#### Command Group Pattern

```python
class ProjectCommandGroup(click.Group):
    """Command group for project operations."""
    
    def __init__(self):
        super().__init__(
            name="project",
            help="Manage Rhapsody projects.",
            invoke_without_command=False,
        )
        self.add_command(OpenProjectCommand())
        self.add_command(ListProjectsCommand())
        self.add_command(CloseProjectCommand())


class OpenProjectCommand(click.Command):
    def __init__(self):
        super().__init__(
            name="open",
            help="Open a Rhapsody project file.",
            callback=self.execute,
            params=[
                click.Argument(["project_path"], type=click.Path(exists=True)),
            ],
        )
    
    def execute(self, project_path: str) -> None:
        # Implementation
        ...
```

#### Error Handling in Commands

```python
def execute(self) -> None:
    try:
        # Implementation
        ...
    except click.Abort:
        # User cancelled, don't re-wrap
        raise
    except SpecificError as e:
        # Catch specific errors first
        click.echo(f"Specific error: {e}", err=True)
        raise click.Abort() from e
    except Exception as e:
        # Generic error handler last
        click.echo(f"Unexpected error: {e}", err=True)
        raise click.Abort() from e
```

---

## Utility Classes

### OutputFormatter Pattern

```python
class OutputFormatter:
    """Formats output data for CLI display."""
    
    SUPPORTED_FORMATS = ("table", "json", "csv")
    
    def __init__(self, format_type: str = "table"):
        if format_type not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format_type}")
        self.format_type = format_type
    
    def format(self, headers: list[str], rows: list[list[Any]]) -> str:
        """Format data according to configured format type."""
        if self.format_type == "table":
            return self._format_table(headers, rows)
        elif self.format_type == "json":
            return self._format_json(headers, rows)
        elif self.format_type == "csv":
            return self._format_csv(headers, rows)
        else:
            raise ValueError(f"Unknown format: {self.format_type}")
    
    def _format_table(self, headers: list[str], rows: list[list[Any]]) -> str:
        """Format as ASCII table."""
        if not rows:
            return "(no data)"
        return str(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def _format_json(self, headers: list[str], rows: list[list[Any]]) -> str:
        """Format as JSON."""
        data = [dict(zip(headers, row)) for row in rows]
        return json.dumps(data, indent=2, default=str)
    
    def _format_csv(self, headers: list[str], rows: list[list[Any]]) -> str:
        """Format as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()
```

### Context Manager Pattern

```python
class RhapsodyContext:
    """Manages session state for CLI commands."""
    
    def __init__(self):
        self._app: RhapsodyApplication | None = None
        self._project: RPProject | None = None
        self._output_format: str = "table"
    
    @property
    def app(self) -> RhapsodyApplication | None:
        return self._app
    
    @property
    def project(self) -> RPProject | None:
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
        self._project = self._app.openProject(project_path)
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
def test_formatter_handles_empty_rows():
    """Test: Formatter handles empty rows gracefully."""
    # ARRANGE
    formatter = OutputFormatter("table")
    headers = ["Name", "Value"]
    rows: list[list[Any]] = []
    
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
    mock_app.openProject.return_value = mock_project
    ctx._app = mock_app
    
    # ACT
    result = ctx.open_project("/path/to/project.rpy")
    
    # ASSERT
    assert result == mock_project
    mock_app.openProject.assert_called_once_with("/path/to/project.rpy")
```

### CLI Integration Tests

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

### Specific to CLI Commands
- [ ] Command inherits from `click.Command` or group?
- [ ] Parameters defined in `__init__`?
- [ ] Logic in `execute()` method?
- [ ] Error handling includes `click.Abort`?
- [ ] User-facing messages in `click.echo()`?

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

- **CLI commands:** `src/rhapsody_cli/cli/commands/`
- **Formatters:** `src/rhapsody_cli/cli/formatters.py`
- **Context:** `src/rhapsody_cli/cli/context.py`
- **Tests:** `tests/test_cli.py`

### Future Examples

After refactoring completes, this directory will contain exemplary class-based, test-first code for reference.

---

## Questions?

For clarification on these guidelines, refer to:
- **TDD Resources:** [pytest documentation](https://pytest.org)
- **Click Commands:** [Click documentation](https://click.palletsprojects.com)
- **Python OOP:** [Real Python OOP Guide](https://realpython.com/python3-object-oriented-programming/)

---

**Last Updated:** 2024  
**Author:** rhapsody-cli development team  
**Status:** Active - Applied to all new code and ongoing refactoring
