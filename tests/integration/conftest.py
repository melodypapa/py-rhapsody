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