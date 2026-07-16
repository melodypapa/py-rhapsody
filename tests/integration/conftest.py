"""Integration test configuration."""

import os
import shutil
import sys
import time
from pathlib import Path
from typing import Generator

import pytest
from pytest import Config, FixtureRequest

from rhapsody_cli import RhapsodyApplication
from rhapsody_cli.models.elements.containment import RPProject

# Add unit directory to Python path so imports from unit tests work
sys.path.insert(0, str(Path(__file__).parent.parent / "unit"))

TEST_PROJECT_DIR = Path(__file__).parent.parent.parent / "demos" / "test_project"
TEST_PROJECT_NAME = "TestProject"


def pytest_addoption(parser: Config) -> None:
    """Add custom command line options for integration tests."""
    parser.addoption(
        "--keep-test-artifacts",
        action="store_true",
        default=False,
        help="Keep test artifacts after integration test run for debugging",
    )


def _safe_cleanup_test_project(app: RhapsodyApplication, project_dir: Path) -> None:
    """Safely clean up test project with proper file handle management.

    This function implements proper cleanup sequence to avoid file lock issues:
    1. Close all projects to release COM file handles
    2. Wait for Windows file system to release locks
    3. Delete the project directory

    Note: Auto-save is now enabled when projects are created/opened,
    so saves are handled automatically without explicit save calls.

    Args:
        app: The Rhapsody application instance
        project_dir: Path to the project directory to clean up
    """
    try:
        # Close all projects first to release COM file handles
        app.close_all_projects()

        # Wait a moment for file handles to be released (Windows file system latency)
        time.sleep(0.5)

        # Now safe to delete directory
        if project_dir.exists():
            shutil.rmtree(project_dir)

    except Exception as e:
        print(f"Warning: Could not fully clean up test project: {e}")
        # Try to at least remove files we can individually
        if project_dir.exists():
            try:
                for item in project_dir.iterdir():
                    if item.is_file():
                        try:
                            item.unlink()
                        except Exception:
                            # Skip files that are still locked
                            pass
            except Exception:
                # If we can't clean up files, at least we tried
                pass


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
def test_project(rhapsody_app: RhapsodyApplication, request: FixtureRequest) -> Generator[RPProject, None, None]:
    """Session-scoped test project fixture — creates an isolated project in ``demos/test_project/``.

    The project is created with auto-save enabled to ensure automatic persistence
    during cleanup operations without explicit save calls.
    """
    # Clean up any existing test project using safe cleanup
    if TEST_PROJECT_DIR.exists():
        _safe_cleanup_test_project(rhapsody_app, TEST_PROJECT_DIR)

    TEST_PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    # Create a new test project
    project = rhapsody_app.create_new_project(str(TEST_PROJECT_DIR), TEST_PROJECT_NAME)

    # Enable auto-save on the project at creation to ensure automatic persistence
    project.allow_auto_save(1)

    yield project

    # Enhanced cleanup after all tests
    keep = request.config.getoption("--keep-test-artifacts", default=False)
    if not keep and not os.getenv("RHAPSODY_KEEP_ARTIFACTS"):
        _safe_cleanup_test_project(rhapsody_app, TEST_PROJECT_DIR)


@pytest.fixture(scope="session")
def test_stereotypes(test_project: RPProject) -> None:
    """Set up test stereotypes with tag definitions for integration tests.

    This fixture creates a stereotype with tag definitions that are required
    for various stereotype-related tests. It runs once per test session.

    The fixture will skip tests that require stereotypes if the setup fails,
    allowing the test suite to continue gracefully.

    Note: The test_project fixture already has auto-save enabled, so changes
    are automatically persisted.
    """
    try:
        # Create a stereotype with tag definition for testing
        stereo = test_project.add_stereotype("TestStereotype")  # type: ignore[call-arg]
        if stereo is not None:
            # Add a tag definition to the stereotype
            stereo.add_tag_definition("TestTag", "String")  # type: ignore[attr-defined]

            # Save the project to persist the stereotype setup
            test_project.save(with_subs=1)
    except Exception as e:
        # If stereotype setup fails, tests that require it will be skipped
        print(f"Warning: Could not set up test stereotypes: {e}")


@pytest.fixture(scope="function")
def second_test_project(rhapsody_app: RhapsodyApplication, request: FixtureRequest) -> Generator[RPProject, None, None]:
    """Function-scoped second test project for cross-project testing.

    This fixture creates a temporary second project for testing cross-project
    operations like copy, move, and reference functionality.

    The project is created with auto-save enabled to ensure automatic persistence
    during cleanup operations without explicit save calls.

    The project is automatically cleaned up after each test using the safe
    cleanup logic to avoid file lock issues.

    Args:
        rhapsody_app: The Rhapsody application instance
        request: pytest request object for accessing test configuration

    Returns:
        RPProject: A temporary second test project
    """
    import tempfile

    # Create a temporary directory for the second project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir) / "SecondTestProject"
        project_path.mkdir(parents=True, exist_ok=True)

        try:
            # Create the second test project
            second_project = rhapsody_app.create_new_project(str(project_path), "SecondTestProject")

            # Enable auto-save on the project at creation to ensure automatic persistence
            second_project.allow_auto_save(1)

            yield second_project

        finally:
            # Clean up the second project
            try:
                second_project.close()
            except Exception:
                pass  # Don't let cleanup failures break tests
