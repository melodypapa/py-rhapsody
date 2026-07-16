"""System test configuration.

System tests invoke the CLI as a real subprocess. Tests requiring
Rhapsody auto-skip when no instance is available.
"""

import shutil
import sys
from pathlib import Path

import pytest

from rhapsody_cli import RhapsodyApplication

# Add unit directory to Python path so imports from unit tests work
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))

TEST_PROJECT_DIR = Path(__file__).parent.parent.parent / "demos" / "test_project_system"
TEST_PROJECT_NAME = "SystemTestProject"


@pytest.fixture(scope="session")
def rhapsody_available() -> bool:
    """Check if a running Rhapsody instance is available."""
    try:
        app = RhapsodyApplication.connect(attach_only=True)
        app.get_is_hidden_ui()
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def _require_rhapsody(rhapsody_available: bool) -> None:
    """Skip tests that require Rhapsody when no instance is available.

    Not autouse — test classes that need Rhapsody must request this fixture
    explicitly (typically via an autouse=True wrapper in the class). This allows
    CLI parsing tests to run without Rhapsody.
    """
    if not rhapsody_available:
        pytest.skip("No running Rhapsody available — skipping system tests", allow_module_level=False)


@pytest.fixture(scope="session")
def test_project_dir() -> Path:
    """Session-scoped test project directory."""
    if TEST_PROJECT_DIR.exists():
        shutil.rmtree(TEST_PROJECT_DIR)
    TEST_PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    return TEST_PROJECT_DIR
