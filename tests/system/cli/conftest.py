"""CLI system test helpers and fixtures.

Provides subprocess CLI invocation helpers and a session-scoped
test project created via the CLI itself.
"""

import json
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

import pytest


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI as a subprocess.

    Args:
        *args: CLI arguments (e.g., "class", "create", "--path", "Pkg")

    Returns:
        CompletedProcess with stdout, stderr, returncode.
    """
    cmd = [sys.executable, "-m", "rhapsody_cli.cli.main", *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _run_cli_json(*args: str) -> Any:
    """Run the CLI with --format json and parse the JSON output.

    Args:
        *args: CLI arguments (without --format json, which is added automatically)

    Returns:
        Parsed JSON data from stdout.

    Raises:
        AssertionError: If the process exits non-zero or JSON parsing fails.
    """
    result = _run_cli(*args, "--format", "json")
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    return json.loads(result.stdout)


def _unique_name(prefix: str = "Test") -> str:
    """Generate a unique element name with UUID suffix.

    Args:
        prefix: Prefix for the name (e.g., "Cls", "Pkg")

    Returns:
        A unique name like "TestCls_a1b2c3d4".
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def cli_project(test_project_dir: Path) -> str:
    """Session-scoped test project created via CLI.

    Creates a new project using `rhapsody-cli project new` and yields
    the project name. The project stays open for the duration of the session
    (the `project close` CLI command is a no-op in subprocess mode — it
    checks `self._project` which is always None in a fresh process, rather
    than calling `app.active_project()`).

    Returns:
        The project name string.
    """
    project_name = "SystemTestProject"

    # Create project via CLI
    result = _run_cli("project", "new", str(test_project_dir), project_name)
    assert result.returncode == 0, f"Failed to create project: {result.stderr}"

    yield project_name

    # NOTE: project close is a no-op in subprocess mode (CLI bug).
    # The project remains open in the Rhapsody instance after the session.
    _run_cli("project", "close")
