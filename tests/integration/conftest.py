"""Integration test configuration."""

import sys
from pathlib import Path

import pytest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError, RhapsodyRuntimeException
from rhapsody_cli.models.elements.containment import RPProject

# Add unit directory to Python path so imports from unit tests work
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))


@pytest.fixture(scope="session")
def rhapsody_app() -> RhapsodyApplication:
    """Session-scoped Rhapsody application fixture."""
    app = RhapsodyApplication.connect(attach_only=True)
    return app


@pytest.fixture(scope="session", autouse=True)
def _require_rhapsody(rhapsody_app: RhapsodyApplication) -> None:
    """Skip the entire integration session if no Rhapsody with an open project is available."""
    try:
        rhapsody_app.active_project()
    except (RhapsodyConnectionError, RhapsodyRuntimeException) as exc:
        pytest.skip(f"No running Rhapsody with an open project: {exc}", allow_module_level=False)


@pytest.fixture(scope="session")
def test_project(rhapsody_app: RhapsodyApplication) -> RPProject:
    """Session-scoped test project fixture — returns the currently active project."""
    return rhapsody_app.active_project()
