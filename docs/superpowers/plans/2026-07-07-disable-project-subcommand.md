# Disable Project Sub-Command & Attach-Based Element Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Temporarily disable the `project` CLI sub-command, make `element` commands attach to the already-running Rhapsody instance and operate on its active project, and add class-based console+file logging to the CLI.

**Architecture:** `RhapsodyContext` gains a `get_active_project()` method that attaches to Rhapsody and reads `activeProject()`. `element` commands call it instead of checking a locally-empty `ctx.project`. `cli/main.py` drops the `project` sub-command registration and wires a new `CliLoggingConfigurator` class (in `cli/logging_config.py`) via a `--verbose/-v` flag.

**Tech Stack:** Python 3.8+, Click, Python `logging` stdlib, pytest, unittest.mock.

---

## Task 1: Add `CliLoggingConfigurator` class with tests

**Files:**
- Create: `src/rhapsody_cli/cli/logging_config.py`
- Test: Create `tests/cli/test_logging_config.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/cli/test_logging_config.py`:

```python
"""Tests for CliLoggingConfigurator."""

from __future__ import annotations

import logging

from rhapsody_cli.cli.logging_config import CliLoggingConfigurator


def _reset_logger() -> logging.Logger:
    """Return the rhapsody_cli logger with handlers cleared for a clean test."""
    logger = logging.getLogger("rhapsody_cli")
    logger.handlers.clear()
    return logger


class TestCliLoggingConfigurator:
    """Tests for CliLoggingConfigurator."""

    def test_default_level_is_info(self) -> None:
        """Test: verbose=False sets logger level to INFO."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()
        assert logger.level == logging.INFO

    def test_verbose_level_is_debug(self) -> None:
        """Test: verbose=True sets logger level to DEBUG."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=True).configure()
        assert logger.level == logging.DEBUG

    def test_configure_adds_stream_and_file_handlers(self) -> None:
        """Test: configure() attaches exactly one StreamHandler and one FileHandler."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()

        stream_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

        assert len(stream_handlers) == 1
        assert len(file_handlers) == 1

    def test_configure_is_idempotent(self) -> None:
        """Test: calling configure() twice does not duplicate handlers."""
        logger = _reset_logger()
        CliLoggingConfigurator(verbose=False).configure()
        CliLoggingConfigurator(verbose=False).configure()

        assert len(logger.handlers) == 2

    def test_file_handler_targets_expected_log_file(self, tmp_path, monkeypatch) -> None:
        """Test: FileHandler writes to rhapsody-cli.log in the current working directory."""
        monkeypatch.chdir(tmp_path)
        logger = _reset_logger()

        CliLoggingConfigurator(verbose=False).configure()
        logger.info("hello world")

        for handler in logger.handlers:
            handler.flush()

        log_file = tmp_path / "rhapsody-cli.log"
        assert log_file.exists()
        assert "hello world" in log_file.read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_logging_config.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rhapsody_cli.cli.logging_config'`

- [ ] **Step 3: Write the implementation**

Create `src/rhapsody_cli/cli/logging_config.py`:

```python
"""Class-based logging configuration for the rhapsody_cli CLI."""

from __future__ import annotations

import logging

_LOGGER_NAME = "rhapsody_cli"


class CliLoggingConfigurator:
    """Configures console + file logging for the rhapsody_cli package logger."""

    LOG_FILE_NAME = "rhapsody-cli.log"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    def __init__(self, verbose: bool = False) -> None:
        """Store the desired verbosity for the next configure() call."""
        self.verbose = verbose

    def configure(self) -> None:
        """Apply console + file logging configuration to the rhapsody_cli logger."""
        logger = logging.getLogger(_LOGGER_NAME)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(self.LOG_FORMAT)
        logger.addHandler(self._build_stream_handler(formatter))
        logger.addHandler(self._build_file_handler(formatter))

    def _build_stream_handler(self, formatter: logging.Formatter) -> logging.StreamHandler:
        """Build the stderr console handler."""
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _build_file_handler(self, formatter: logging.Formatter) -> logging.FileHandler:
        """Build the append-mode file handler writing to LOG_FILE_NAME."""
        handler = logging.FileHandler(self.LOG_FILE_NAME, mode="a")
        handler.setFormatter(formatter)
        return handler
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_logging_config.py -v`
Expected: PASS (5 passed)

- [ ] **Step 5: Commit**

```bash
git add src/rhapsody_cli/cli/logging_config.py tests/cli/test_logging_config.py
git commit -m "feat: add class-based CLI logging configurator"
```

---

## Task 2: Wire `--verbose` flag into `cli/main.py`

**Files:**
- Modify: `src/rhapsody_cli/cli/main.py`
- Test: Modify `tests/cli/test_core.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/cli/test_core.py` (near `test_cli_output_format_option`):

```python
def test_cli_verbose_flag_configures_debug_logging() -> None:
    """Test --verbose flag configures the rhapsody_cli logger at DEBUG level."""
    import logging

    runner = CliRunner()
    result = runner.invoke(cli, ["--verbose", "--help"])
    assert result.exit_code == 0
    assert logging.getLogger("rhapsody_cli").level == logging.DEBUG


def test_cli_without_verbose_flag_configures_info_logging() -> None:
    """Test omitting --verbose configures the rhapsody_cli logger at INFO level."""
    import logging

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert logging.getLogger("rhapsody_cli").level == logging.INFO
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_core.py -k verbose -v`
Expected: FAIL with `click.exceptions.NoSuchOption` (no `--verbose` option registered yet) or a `logging` level assertion failure.

- [ ] **Step 3: Modify `src/rhapsody_cli/cli/main.py`**

Current content is:

```python
"""Main CLI entry point."""

from __future__ import annotations

import click

from rhapsody_cli.cli.commands.element import element as element_cmd
from rhapsody_cli.cli.commands.io import io as io_cmd
from rhapsody_cli.cli.commands.project import project as project_cmd
from rhapsody_cli.cli.context import RhapsodyContext


@click.group()
@click.option(
    "--output",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format",
)
@click.pass_context
def cli(ctx: click.Context, output: str) -> None:
    """Rhapsody model CLI tool for browsing and managing models."""
    if ctx.obj is None:
        ctx.obj = RhapsodyContext()
    ctx.obj.output_format = output


cli.add_command(project_cmd)
cli.add_command(element_cmd)
cli.add_command(io_cmd)


if __name__ == "__main__":
    cli()
```

Replace it with:

```python
"""Main CLI entry point."""

from __future__ import annotations

import click

from rhapsody_cli.cli.commands.element import element as element_cmd
from rhapsody_cli.cli.commands.io import io as io_cmd
from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.logging_config import CliLoggingConfigurator

# NOTE: The `project` sub-command is temporarily disabled. Users open Rhapsody
# projects manually via the Rhapsody GUI; `element` commands attach to that
# running instance's active project instead. Re-enable by importing
# `project as project_cmd` from `rhapsody_cli.cli.commands.project` and adding
# `cli.add_command(project_cmd)` below.


@click.group()
@click.option(
    "--output",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Enable DEBUG-level logging (default: INFO).",
)
@click.pass_context
def cli(ctx: click.Context, output: str, verbose: bool) -> None:
    """Rhapsody model CLI tool for browsing and managing models."""
    CliLoggingConfigurator(verbose=verbose).configure()
    if ctx.obj is None:
        ctx.obj = RhapsodyContext()
    ctx.obj.output_format = output


cli.add_command(element_cmd)
cli.add_command(io_cmd)


if __name__ == "__main__":
    cli()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_core.py -k verbose -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add src/rhapsody_cli/cli/main.py tests/cli/test_core.py
git commit -m "feat: wire --verbose flag to CliLoggingConfigurator"
```

---

## Task 3: Remove `project` sub-command from CLI registration

**Files:**
- Modify: `tests/cli/test_core.py`

(No further change to `src/rhapsody_cli/cli/main.py` — Task 2 already removed the
`project` import and `add_command` call.)

- [ ] **Step 1: Update the now-outdated `test_project_help` test**

In `tests/cli/test_core.py`, replace:

```python
def test_project_help() -> None:
    """Test project command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["project", "--help"])
    assert result.exit_code == 0
    assert "Manage Rhapsody projects" in result.output
    assert "open" in result.output
    assert "list" in result.output
```

with:

```python
def test_project_command_is_not_registered() -> None:
    """Test: the project sub-command is temporarily disabled on the root CLI."""
    runner = CliRunner()
    result = runner.invoke(cli, ["project", "--help"])
    assert result.exit_code != 0
    assert "No such command" in result.output


def test_cli_help_does_not_list_project_command() -> None:
    """Test: root --help no longer advertises the project sub-command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "project" not in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_core.py -k project -v`
Expected: These two new tests PASS already (main.py was updated in Task 2), replacing
the old `test_project_help` which would now FAIL if left in place. Confirm the old
test is gone and the file has no reference to `"Manage Rhapsody projects"`.

Run: `grep -n "Manage Rhapsody projects" tests/cli/test_core.py`
Expected: no output (no matches).

- [ ] **Step 3: Run full CLI test file to confirm nothing else broke**

Run: `pytest tests/cli/test_core.py -v`
Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/cli/test_core.py
git commit -m "test: replace project-enabled CLI help test with disabled-command assertions"
```

---

## Task 4: Add `RhapsodyContext.get_active_project()`

**Files:**
- Modify: `src/rhapsody_cli/cli/context.py`
- Test: Modify `tests/cli/test_core.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/cli/test_core.py`:

```python
def test_context_get_active_project_attaches_and_returns_active_project() -> None:
    """Test get_active_project() attaches to Rhapsody and returns activeProject()."""
    ctx = RhapsodyContext()
    fake_app = MagicMock(name="FakeApplication")
    fake_project = MagicMock(name="FakeProject")
    fake_app.activeProject.return_value = fake_project

    def fake_connect(method: str = "attach") -> MagicMock:
        ctx.app = fake_app
        return fake_app

    with patch.object(ctx, "connect", side_effect=fake_connect) as mock_connect:
        result = ctx.get_active_project()

    mock_connect.assert_called_once_with("attach")
    fake_app.activeProject.assert_called_once_with()
    assert result is fake_project
    assert ctx.project is fake_project


def test_context_get_active_project_propagates_connection_error() -> None:
    """Test get_active_project() lets RhapsodyConnectionError from connect() propagate."""
    from rhapsody_cli.exceptions import RhapsodyConnectionError

    ctx = RhapsodyContext()
    with patch.object(
        ctx, "connect", side_effect=RhapsodyConnectionError("no running instance")
    ):
        with pytest.raises(RhapsodyConnectionError):
            ctx.get_active_project()
```

Add `import pytest` to the top of `tests/cli/test_core.py` alongside the existing
imports (it currently has no `pytest` import).

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_core.py -k get_active_project -v`
Expected: FAIL with `AttributeError: 'RhapsodyContext' object has no attribute 'get_active_project'`

- [ ] **Step 3: Modify `src/rhapsody_cli/cli/context.py`**

Add this method to the `RhapsodyContext` class, placed after `open_project` and
before `create_project`:

```python
    def get_active_project(self) -> RPProject:
        """Attach to the running Rhapsody instance and return its active project.

        Raises:
            RhapsodyConnectionError: if no running Rhapsody instance can be
                attached to (propagated from connect()).
        """
        self.connect("attach")
        assert self.app is not None  # For mypy type narrowing
        self.project = self.app.activeProject()
        return self.project
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_core.py -k get_active_project -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add src/rhapsody_cli/cli/context.py tests/cli/test_core.py
git commit -m "feat: add RhapsodyContext.get_active_project()"
```

---

## Task 5: Update element commands to attach + use active project

**Files:**
- Modify: `src/rhapsody_cli/cli/commands/element.py`
- Test: Modify `tests/cli/test_element_commands.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/cli/test_element_commands.py` (add these imports at the top:
`from unittest.mock import MagicMock, patch`, `from click.testing import CliRunner`,
`from rhapsody_cli.cli.context import RhapsodyContext`,
`from rhapsody_cli.exceptions import RhapsodyConnectionError`):

```python
class TestAddElementCommandAttachBehavior:
    """Tests for AddElementCommand attaching to the live Rhapsody instance."""

    def test_add_command_creates_class_on_active_project(self) -> None:
        """Test: add --type class calls createClass on the active project's root."""
        runner = CliRunner()
        group = ElementCommandGroup()

        fake_root = MagicMock(name="FakeRoot")
        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            result = runner.invoke(group, ["add", "--type", "class", "--name", "Foo"])

        assert result.exit_code == 0
        fake_root.createClass.assert_called_once_with("Foo")
        assert "Created class: Foo" in result.output

    def test_add_command_reports_no_running_instance(self) -> None:
        """Test: add command reports a clear message when no Rhapsody is running."""
        runner = CliRunner()
        group = ElementCommandGroup()

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            result = runner.invoke(group, ["add", "--type", "class", "--name", "Foo"])

        assert result.exit_code != 0
        assert (
            "No running Rhapsody instance found. Please open Rhapsody and a project first."
            in result.output
        )


class TestQueryElementCommandAttachBehavior:
    """Tests for QueryElementCommand attaching to the live Rhapsody instance."""

    def test_query_command_lists_elements_from_active_project(self) -> None:
        """Test: query command lists elements from the active project's root."""
        runner = CliRunner()
        group = ElementCommandGroup()

        fake_element = MagicMock(name="FakeElement")
        fake_element.getName.return_value = "MyClass"
        fake_element.getMetaClass.return_value = "Class"

        fake_root = MagicMock(name="FakeRoot")
        fake_root.getNestedElements.return_value = [fake_element]

        fake_project = MagicMock(name="FakeProject")
        fake_project.getRoot.return_value = fake_root

        def fake_get_active_project(self: RhapsodyContext) -> MagicMock:
            self.project = fake_project
            return fake_project

        with patch.object(RhapsodyContext, "get_active_project", fake_get_active_project):
            result = runner.invoke(group, ["query"])

        assert result.exit_code == 0
        assert "MyClass" in result.output

    def test_query_command_reports_no_running_instance(self) -> None:
        """Test: query command reports a clear message when no Rhapsody is running."""
        runner = CliRunner()
        group = ElementCommandGroup()

        with patch.object(
            RhapsodyContext,
            "get_active_project",
            side_effect=RhapsodyConnectionError("No running Rhapsody instance found"),
        ):
            result = runner.invoke(group, ["query"])

        assert result.exit_code != 0
        assert (
            "No running Rhapsody instance found. Please open Rhapsody and a project first."
            in result.output
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_element_commands.py -v`
Expected: FAIL — the new tests fail because `AddElementCommand`/`QueryElementCommand`
still check `ctx.project is None` and print `"Use 'project open' first."` instead of
calling `ctx.get_active_project()`.

- [ ] **Step 3: Modify `src/rhapsody_cli/cli/commands/element.py`**

Replace the full file content with:

```python
"""Element-related CLI commands using class-based architecture."""

from __future__ import annotations

import logging

import click

from rhapsody_cli.cli.context import RhapsodyContext
from rhapsody_cli.cli.formatters import OutputFormatter
from rhapsody_cli.exceptions import RhapsodyConnectionError

logger = logging.getLogger(__name__)

_NO_ACTIVE_INSTANCE_MESSAGE = (
    "No running Rhapsody instance found. Please open Rhapsody and a project first."
)


class BaseElementCommand(click.Command):
    """Base class for element commands."""

    pass


class AddElementCommand(BaseElementCommand):
    """Command: Add a new element to the project."""

    def __init__(self) -> None:
        super().__init__(
            name="add",
            help="Add a new element to the project.",
            callback=self.execute,
            params=[
                click.Option(
                    ["--type"],
                    "element_type",
                    required=True,
                    help="Element type (class, actor, etc)",
                ),
                click.Option(["--name"], required=True, help="Element name"),
            ],
        )

    def execute(self, element_type: str, name: str) -> None:
        """Execute the add command."""
        ctx = RhapsodyContext()
        try:
            project = ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            click.echo(_NO_ACTIVE_INSTANCE_MESSAGE, err=True)
            raise click.Abort() from e

        try:
            root = project.getRoot()  # type: ignore[attr-defined]
            if element_type.lower() == "class":
                root.createClass(name)
            elif element_type.lower() == "actor":
                root.createActor(name)
            elif element_type.lower() == "package":
                root.createPackage(name)
            else:
                click.echo(f"Error: Unknown element type '{element_type}'", err=True)
                raise click.Abort()

            logger.info("Created %s: %s", element_type, name)
            click.echo(f"Created {element_type}: {name}")
        except click.Abort:
            raise
        except Exception as e:
            logger.error("Failed to create %s '%s': %s", element_type, name, e)
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class ViewElementCommand(BaseElementCommand):
    """Command: View element details."""

    def __init__(self) -> None:
        super().__init__(
            name="view",
            help="View element details.",
            callback=self.execute,
            params=[
                click.Option(["--path"], required=True, help="Element path (e.g., Root::MyClass)"),
            ],
        )

    def execute(self, path: str) -> None:
        """Execute the view command."""
        ctx = RhapsodyContext()
        try:
            ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            click.echo(_NO_ACTIVE_INSTANCE_MESSAGE, err=True)
            raise click.Abort() from e

        try:
            data = {
                "path": path,
                "type": "unknown",
                "properties": {"status": "read-only for demo"},
            }

            if ctx.output_format == "json":
                output = OutputFormatter.json_format(data)
            else:
                rows = [["path", path], ["type", "unknown"]]
                output = OutputFormatter.table(["Property", "Value"], rows)

            click.echo(output)
        except click.Abort:
            raise
        except Exception as e:
            logger.error("Failed to view element '%s': %s", path, e)
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class QueryElementCommand(BaseElementCommand):
    """Command: Query elements in active project."""

    def __init__(self) -> None:
        super().__init__(
            name="query",
            help="Query elements in active project.",
            callback=self.execute,
            params=[
                click.Option(["--filter"], default=None, help="Filter by type or name"),
            ],
        )

    def execute(self, filter: str) -> None:
        """Execute the query command."""
        ctx = RhapsodyContext()
        try:
            project = ctx.get_active_project()
        except RhapsodyConnectionError as e:
            logger.error("Failed to attach to Rhapsody: %s", e)
            click.echo(_NO_ACTIVE_INSTANCE_MESSAGE, err=True)
            raise click.Abort() from e

        try:
            root = project.getRoot()  # type: ignore[attr-defined]
            elements = root.getNestedElements()

            if ctx.output_format == "json":
                data = {
                    "elements": [
                        {
                            "name": elem.getName(),
                            "type": elem.getMetaClass(),
                        }
                        for elem in elements
                    ]
                }
                output = OutputFormatter.json_format(data)
            else:
                rows = [[elem.getName(), elem.getMetaClass()] for elem in elements]
                output = OutputFormatter.table(["Name", "Type"], rows)

            click.echo(output)
        except click.Abort:
            raise
        except Exception as e:
            logger.error("Failed to query elements: %s", e)
            click.echo(f"Error: {e}", err=True)
            raise click.Abort() from e


class ElementCommandGroup(click.Group):
    """Command group for element operations."""

    def __init__(self) -> None:
        super().__init__(
            name="element",
            help="Manage model elements.",
            invoke_without_command=False,
        )
        self.add_command(AddElementCommand())
        self.add_command(ViewElementCommand())
        self.add_command(QueryElementCommand())


element = ElementCommandGroup()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_element_commands.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/rhapsody_cli/cli/commands/element.py tests/cli/test_element_commands.py
git commit -m "feat: attach to live Rhapsody instance in element commands"
```

---

## Task 6: Full quality gate and final verification

**Files:** none (verification only)

- [ ] **Step 1: Run the full test suite**

Run: `pytest -v`
Expected: all tests PASS (no failures, no errors). Confirm `tests/cli/test_command_classes.py`
(which constructs `ProjectCommandGroup()` directly, not via `cli`) still passes unchanged.

- [ ] **Step 2: Run lint, format check, and type check**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: no errors. If `black --check` fails on modified files, run
`black src/ tests/` and re-run `git diff` to confirm only expected formatting changed,
then re-run the full gate.

- [ ] **Step 3: Manual smoke check of removed command**

Run: `python -m rhapsody_cli.cli.main project --help`
Expected: non-zero exit, output containing `No such command 'project'`.

- [ ] **Step 4: Commit any formatting fixes (if Step 2 required `black` changes)**

```bash
git add -A
git commit -m "chore: apply black formatting fixes"
```

(Skip this step if Step 2 required no changes.)

---

## Notes for Re-Enabling `project` Later

`src/rhapsody_cli/cli/commands/project.py` and `tests/cli/test_command_classes.py` are
untouched by this plan. To re-enable:
1. In `src/rhapsody_cli/cli/main.py`, re-add
   `from rhapsody_cli.cli.commands.project import project as project_cmd` and
   `cli.add_command(project_cmd)`.
2. Revert/update the `test_project_command_is_not_registered` and
   `test_cli_help_does_not_list_project_command` tests in `tests/cli/test_core.py`
   back to asserting the command IS registered.
