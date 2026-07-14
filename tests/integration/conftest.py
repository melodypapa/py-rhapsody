"""Integration test configuration."""

import os
import shutil
import sys
from pathlib import Path

import pytest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.models.elements.containment import RPProject

# Add unit directory to Python path so imports from unit tests work
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))

TEST_PROJECT_DIR = Path(__file__).parent.parent.parent / "demos" / "test_project"
TEST_PROJECT_NAME = "TestProject"


def pytest_addoption(parser):
    """Add custom command line options for integration tests."""
    parser.addoption(
        "--keep-test-artifacts",
        action="store_true",
        default=False,
        help="Keep test artifacts after integration test run for debugging",
    )


@pytest.fixture(scope="session")
def rhapsody_app() -> RhapsodyApplication:
    """Session-scoped Rhapsody application fixture."""
    app = RhapsodyApplication.connect(attach_only=True)
    return app


@pytest.fixture(scope="session", autouse=True)
def _require_rhapsody(rhapsody_app: RhapsodyApplication) -> None:
    """Skip the entire integration session if no Rhapsody instance is available."""
    try:
        rhapsody_app.get_is_hidden_ui()
    except Exception as exc:
        pytest.skip(f"No running Rhapsody available: {exc}", allow_module_level=False)


@pytest.fixture(scope="session")
def test_project(rhapsody_app: RhapsodyApplication, request) -> RPProject:
    """Session-scoped test project fixture — creates an isolated project in ``demos/test_project/``."""
    # Clean up any existing test project
    if TEST_PROJECT_DIR.exists():
        shutil.rmtree(TEST_PROJECT_DIR)
    TEST_PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    # Create a new test project
    project = rhapsody_app.create_new_project(str(TEST_PROJECT_DIR), TEST_PROJECT_NAME)

    yield project

    # Cleanup after all tests
    keep = request.config.getoption("--keep-test-artifacts", default=False)
    if not keep and not os.getenv("RHAPSODY_KEEP_ARTIFACTS"):
        try:
            project.close()
        except Exception:
            pass
        if TEST_PROJECT_DIR.exists():
            shutil.rmtree(TEST_PROJECT_DIR)
