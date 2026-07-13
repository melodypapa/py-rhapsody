# Integration Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comprehensive integration tests that validate every model wrapper method works correctly with real Rhapsody COM API, separate from existing mocked unit tests.

**Architecture:** Session-scoped pytest fixtures manage Rhapsody application lifecycle and temporary test project. Integration tests mirror unit test structure under `tests/integration/models/`, testing actual COM interactions and hierarchical relationships (operations in classes, models under packages). Manual execution only on Windows with Rhapsody installed.

**Tech Stack:** pytest, pywin32, existing rhapsody-cli models, Rhapsody COM API

## Global Constraints

- Platform: Windows only (COM automation requires Windows)
- Python: 3.8+
- All wrapper method names use snake_case (established convention)
- All COM calls must use `call_com(lambda: ...)` wrapper
- All constants use SCREAMING_SNAKE_CASE
- Use string-quoted forward refs or `TYPE_CHECKING` imports (no `from __future__ import annotations`)
- TDD is mandatory — write tests before implementation
- Integration tests use manual execution only (no CI integration)
- Coverage must remain separate from unit tests

---

### Task 1: Create Integration Test Directory Structure

**Files:**
- Create: `tests/integration/__init__.py`
- Create: `tests/integration/models/__init__.py`
- Create: `tests/integration/models/elements/__init__.py`

**Interfaces:**
- Produces: Package structure for integration tests

- [ ] **Step 1: Create integration test package marker**

```python
# tests/integration/__init__.py
"""Integration tests for rhapsody-cli models with real Rhapsody COM API."""
```

- [ ] **Step 2: Create models integration test package marker**

```python
# tests/integration/models/__init__.py
"""Integration tests for model wrapper classes."""
```

- [ ] **Step 3: Create elements integration test package marker**

```python
# tests/integration/models/elements/__init__.py
"""Integration tests for element wrapper classes."""
```

- [ ] **Step 4: Commit directory structure**

```bash
git add tests/integration/__init__.py tests/integration/models/__init__.py tests/integration/models/elements/__init__.py
git commit -m "feat: add integration test directory structure"
```

---

### Task 2: Add Git Ignore Entry for Test Project

**Files:**
- Modify: `.gitignore`

**Interfaces:**
- Produces: Git ignore rule for temporary test project directory

- [ ] **Step 1: Add test project directory to gitignore**

```bash
# Append to .gitignore
echo "" >> .gitignore
echo "# Integration test temporary project" >> .gitignore
echo "demos/test_project/" >> .gitignore
```

- [ ] **Step 2: Verify git ignore entry**

```bash
cat .gitignore | grep -A2 "Integration test"
```
Expected: Output shows the test project ignore entry

- [ ] **Step 3: Commit git ignore changes**

```bash
git add .gitignore
git commit -m "chore: ignore integration test project directory"
```

---

### Task 3: Add Pytest Markers for Test Separation

**Files:**
- Modify: `pyproject.toml`

**Interfaces:**
- Produces: Pytest markers for unit vs integration test separation

- [ ] **Step 1: Add pytest markers to configuration**

Read `pyproject.toml` to find the `[tool.pytest.ini_options]` section and add markers:

```toml
markers = [
    "integration: marks tests as integration tests (require Rhapsody)",
    "unit: marks tests as unit tests (mocked COM)"
]
```

If no `[tool.pytest.ini_options]` section exists, add it:

```toml
[tool.pytest.ini_options]
markers = [
    "integration: marks tests as integration tests (require Rhapsody)",
    "unit: marks tests as unit tests (mocked COM)"
]
```

- [ ] **Step 2: Verify pytest configuration**

```bash
pytest --markers
```
Expected: Output shows `integration` and `unit` markers

- [ ] **Step 3: Commit pytest configuration**

```bash
git add pyproject.toml
git commit -m "test: add pytest markers for unit/integration separation"
```

---

### Task 4: Create Integration Test Fixtures

**Files:**
- Create: `tests/integration/conftest.py`

**Interfaces:**
- Produces: Session-scoped fixtures for Rhapsody app and test project
- Produces: Autouse fixture for skipping tests when Rhapsody unavailable

- [ ] **Step 1: Write the failing fixture test**

```python
# tests/integration/conftest.py
import pytest
import os
import shutil
from pathlib import Path
from rhapsody_cli.application import RhapsodyApplication
from rhapsody_cli.exceptions import RhapsodyConnectionError

def pytest_addoption(parser):
    """Add custom command line options for integration tests."""
    parser.addoption(
        "--keep-test-artifacts",
        action="store_true",
        default=False,
        help="Keep test artifacts after integration test run for debugging"
    )

@pytest.fixture(scope="session")
def rhapsody_app():
    """Session-scoped Rhapsody application fixture."""
    app = None
    try:
        app = RhapsodyApplication.connect(prefer_attach=True)
        yield app
    except RhapsodyConnectionError:
        pytest.skip("Rhapsody not available - skipping integration tests")
    finally:
        if app is not None:
            # Clean up connection if needed
            pass

@pytest.fixture(scope="session")
def test_project(rhapsody_app, request):
    """Session-scoped test project fixture."""
    # Clean up any existing test project
    test_project_path = Path("demos/test_project")
    if test_project_path.exists():
        shutil.rmtree(test_project_path)

    # Create new test project
    test_project_path.mkdir(parents=True, exist_ok=True)
    project_path = test_project_path / "TestProject.rpy"

    # Create project via Rhapsody
    project = rhapsody_app.create_project(str(project_path), "TestProject")

    yield project

    # Cleanup after all tests (unless --keep-test-artifacts flag or RHAPSODY_KEEP_ARTIFACTS is set)
    keep_artifacts = request.config.getoption("--keep-test-artifacts", default=False)
    if not keep_artifacts and not os.getenv("RHAPSODY_KEEP_ARTIFACTS"):
        if test_project_path.exists():
            shutil.rmtree(test_project_path)

@pytest.fixture(scope="session", autouse=True)
def skip_if_no_rhapsody():
    """Autouse fixture to detect Rhapsody availability."""
    try:
        # Try to import pywin32 to check platform availability
        import win32com.client
    except ImportError:
        pytest.skip("pywin32 not available - skipping integration tests")
```

- [ ] **Step 2: Run pytest to verify fixtures load**

```bash
pytest tests/integration/ -v --collect-only
```
Expected: Tests are collected (should be 0 tests since we have no test files yet)

- [ ] **Step 3: Commit fixtures**

```bash
git add tests/integration/conftest.py
git commit -m "test: add integration test fixtures for Rhapsody lifecycle"
```

---

### Task 5: Write Core Model Integration Tests - RPModelElement

**Files:**
- Create: `tests/integration/models/test_core.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest
- Consumes: `rhapsody_app` fixture from conftest

- [ ] **Step 1: Write failing test for RPModelElement basic methods**

```python
# tests/integration/models/test_core.py
import pytest
from rhapsody_cli.models.elements.containment import RPProject
from rhapsody_cli.models.core import RPModelElement

@pytest.mark.integration
class TestRPModelElementIntegration:
    """Integration tests for RPModelElement with real Rhapsody COM API."""

    def test_get_name(self, test_project):
        """Test get_name returns actual project name."""
        # Arrange
        assert isinstance(test_project, RPModelElement)

        # Act
        name = test_project.get_name()

        # Assert
        assert name == "TestProject"
        assert isinstance(name, str)

    def test_set_name(self, test_project):
        """Test set_name changes actual project name."""
        # Arrange
        original_name = test_project.get_name()

        # Act
        test_project.set_name("RenamedProject")
        new_name = test_project.get_name()

        # Assert
        assert new_name == "RenamedProject"
        assert isinstance(new_name, str)

        # Cleanup - restore original name
        test_project.set_name(original_name)

    def test_get_meta_class(self, test_project):
        """Test get_meta_class returns correct metaclass."""
        # Act
        meta_class = test_project.get_meta_class()

        # Assert
        assert meta_class == "Project"
        assert isinstance(meta_class, str)

    def test_get_guid(self, test_project):
        """Test get_guid returns unique identifier."""
        # Act
        guid = test_project.get_guid()

        # Assert
        assert isinstance(guid, str)
        assert len(guid) > 0  # GUIDs should not be empty
```

- [ ] **Step 2: Run tests to verify they fail (no implementation yet)**

```bash
pytest tests/integration/models/test_core.py::TestRPModelElementIntegration::test_get_name -v
```
Expected: Tests should run (if Rhapsody available) and validate basic RPModelElement methods

- [ ] **Step 3: Commit core model tests**

```bash
git add tests/integration/models/test_core.py
git commit -m "test: add RPModelElement integration tests"
```

---

### Task 6: Write Core Model Integration Tests - RPCollection

**Files:**
- Modify: `tests/integration/models/test_core.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest
- Consumes: Existing RPModelElement integration test structure

- [ ] **Step 1: Add failing tests for RPCollection wrapper**

```python
# Add to tests/integration/models/test_core.py

@pytest.mark.integration
class TestRPCollectionIntegration:
    """Integration tests for RPCollection with real Rhapsody COM API."""

    def test_get_nested_elements_iteration(self, test_project):
        """Test get_nested_elements returns iterable collection."""
        # Act
        elements = test_project.get_nested_elements()

        # Assert
        assert elements is not None
        # Projects should have at least some nested elements
        assert len(list(elements)) >= 0

    def test_get_nested_elements_filtering(self, test_project):
        """Test get_nested_elements with metaclass filter."""
        # Act
        all_elements = test_project.get_nested_elements()
        packages = test_project.get_nested_elements("Package")

        # Assert
        assert all_elements is not None
        assert packages is not None
        # Filtered result should be subset of all elements
        all_list = list(all_elements)
        package_list = list(packages)
        assert len(package_list) <= len(all_list)
```

- [ ] **Step 2: Run tests to verify collection functionality**

```bash
pytest tests/integration/models/test_core.py::TestRPCollectionIntegration -v
```
Expected: Tests validate RPCollection iteration and filtering

- [ ] **Step 3: Commit RPCollection tests**

```bash
git add tests/integration/models/test_core.py
git commit -m "test: add RPCollection integration tests"
```

---

### Task 7: Write Classifier Integration Tests - Hierarchy Testing

**Files:**
- Create: `tests/integration/models/elements/test_classifiers.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest
- Consumes: `rhapsody_app` fixture from conftest

- [ ] **Step 1: Write failing tests for class hierarchy and operations**

```python
# tests/integration/models/elements/test_classifiers.py
import pytest
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPClassIntegration:
    """Integration tests for RPClass with real Rhapsody COM API."""

    def create_test_package(self, project, name="TestPackage"):
        """Helper to create a test package."""
        package = project.add_package(name)
        assert package is not None
        assert isinstance(package, RPPackage)
        return package

    def test_create_class_in_package(self, test_project):
        """Test creating a class within a package (parent-child relationship)."""
        # Arrange
        package = self.create_test_package(test_project)

        # Act
        test_class = package.add_class("TestClass")

        # Assert
        assert test_class is not None
        assert isinstance(test_class, RPClass)
        assert test_class.get_name() == "TestClass"
        assert test_class.get_meta_class() == "Class"

    def test_class_hierarchy_navigation(self, test_project):
        """Test navigating from class to parent package."""
        # Arrange
        package = self.create_test_package(test_project, "ParentPackage")
        test_class = package.add_class("ChildClass")

        # Act
        parent = test_class.get_owner()

        # Assert
        assert parent is not None
        assert parent.get_name() == "ParentPackage"
        assert isinstance(parent, RPPackage)

    def test_create_operation_in_class(self, test_project):
        """Test creating operation as member of class (hierarchical relationship)."""
        # Arrange
        package = self.create_test_package(test_project)
        test_class = package.add_class("TestClass")

        # Act
        operation = test_class.add_operation("testOperation")

        # Assert
        assert operation is not None
        assert operation.get_name() == "testOperation"
        # Verify operation is member of class
        operations = test_class.get_operations()
        assert operation in list(operations)

    def test_invalid_hierarchy_throws_exception(self, test_project):
        """Test that invalid hierarchical relationships throw Rhapsody exceptions."""
        # Arrange
        package = self.create_test_package(test_project)

        # Act & Assert - attempting invalid operations should throw
        with pytest.raises(Exception):  # Will be translated from COM error
            # Try to add a class to something that doesn't support it
            # This will trigger a Rhapsody COM exception
            invalid_parent = package.get_higher_object()  # Likely Project
            if invalid_parent:
                invalid_parent.add_class("InvalidClass")
```

- [ ] **Step 2: Run tests to verify hierarchy validation**

```bash
pytest tests/integration/models/elements/test_classifiers.py::TestRPClassIntegration -v
```
Expected: Tests validate parent-child relationships and exception handling

- [ ] **Step 3: Commit classifier hierarchy tests**

```bash
git add tests/integration/models/elements/test_classifiers.py
git commit -m "test: add RPClass hierarchy integration tests"
```

---

### Task 8: Write Containment Element Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_containment.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest
- Consumes: Helper methods from test_classifiers for consistency

- [ ] **Step 1: Write failing tests for package and project containment**

```python
# tests/integration/models/elements/test_containment.py
import pytest
from rhapsody_cli.models.elements.containment import RPPackage, RPProject

@pytest.mark.integration
class TestRPPackageIntegration:
    """Integration tests for RPPackage with real Rhapsody COM API."""

    def create_test_package(self, project, name="TestPackage"):
        """Helper to create a test package."""
        package = project.add_package(name)
        assert package is not None
        return package

    def test_create_nested_packages(self, test_project):
        """Test creating packages within packages (hierarchical containment)."""
        # Arrange
        parent_package = self.create_test_package(test_project, "ParentPackage")

        # Act
        child_package = parent_package.add_package("ChildPackage")

        # Assert
        assert child_package is not None
        assert isinstance(child_package, RPPackage)
        assert child_package.get_name() == "ChildPackage"
        # Verify child is contained in parent
        children = parent_package.get_nested_elements("Package")
        assert child_package in list(children)

    def test_package_navigation(self, test_project):
        """Test navigating package hierarchy (parent-child relationships)."""
        # Arrange
        root_package = self.create_test_package(test_project, "RootPackage")
        child_package = root_package.add_package("SubPackage")

        # Act
        parent = child_package.get_owner()

        # Assert
        assert parent is not None
        assert parent.get_name() == "RootPackage"
        assert isinstance(parent, RPPackage)

@pytest.mark.integration
class TestRPProjectIntegration:
    """Integration tests for RPProject with real Rhapsody COM API."""

    def test_project_properties(self, test_project):
        """Test basic RPProject properties and methods."""
        # Act & Assert
        assert test_project.get_name() == "TestProject"
        assert test_project.get_meta_class() == "Project"
        assert test_project.get_guid() is not None

    def test_add_package_to_project(self, test_project):
        """Test adding package to project (top-level containment)."""
        # Act
        new_package = test_project.add_package("ProjectLevelPackage")

        # Assert
        assert new_package is not None
        assert isinstance(new_package, RPPackage)
        assert new_package.get_name() == "ProjectLevelPackage"
        # Verify package is in project's nested elements
        packages = test_project.get_nested_elements("Package")
        assert new_package in list(packages)
```

- [ ] **Step 2: Run tests to verify containment relationships**

```bash
pytest tests/integration/models/elements/test_containment.py -v
```
Expected: Tests validate package/project containment and navigation

- [ ] **Step 3: Commit containment integration tests**

```bash
git add tests/integration/models/elements/test_containment.py
git commit -m "test: add RPPackage and RPProject integration tests"
```

---

### Task 9: Add Integration Test Execution Documentation

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Produces: Documentation for running integration tests
- Consumes: Integration test directory structure

- [ ] **Step 1: Add integration test section to CLAUDE.md**

Add this section to `CLAUDE.md` under the "Testing" section:

```markdown
### Integration Tests

Integration tests validate model wrapper methods against a real Rhapsody application. These tests require:
- Windows platform
- Rhapsody installed and licensed
- pywin32 available

**Running integration tests:**

```bash
# Run only integration tests
pytest tests/integration/

# Run integration tests with coverage
pytest tests/integration/ --cov=rhapsody_cli --cov-report=html

# Run only unit tests (no Rhapsody required)
pytest tests/unit/

# Run by marker
pytest -m integration  # Integration tests only
pytest -m unit         # Unit tests only
```

**Integration test behavior:**
- Tests create a temporary project at `demos/test_project/TestProject.rpy`
- Project is cleaned up before each test run
- Artifacts are preserved on failure for debugging
- Set `RHAPSODY_KEEP_ARTIFACTS=1` or use `--keep-test-artifacts` to preserve artifacts

**Test structure:**
- `tests/integration/conftest.py` — Session-scoped fixtures for Rhapsody lifecycle
- `tests/integration/models/` — Mirrors unit test structure
- Tests validate both COM API interactions and hierarchical relationships
```

- [ ] **Step 2: Verify documentation is clear**

```bash
cat CLAUDE.md | grep -A30 "### Integration Tests"
```
Expected: Documentation shows commands and behavior

- [ ] **Step 3: Commit documentation**

```bash
git add CLAUDE.md
git commit -m "docs: add integration test execution documentation"
```

---

### Task 10: Verify Test Execution and Coverage Separation

**Files:**
- Test: `tests/integration/` (all integration test files)
- Test: `tests/unit/` (existing unit tests)

**Interfaces:**
- Consumes: All integration test fixtures and tests
- Produces: Verification that tests run correctly and coverage is separate

- [ ] **Step 1: Run unit tests to ensure they still work**

```bash
pytest tests/unit/ -v
```
Expected: Unit tests pass (no Rhapsody required)

- [ ] **Step 2: Run integration tests (requires Rhapsody on Windows)**

```bash
pytest tests/integration/ -v
```
Expected: Integration tests pass if Rhapsody is available, skip gracefully otherwise

- [ ] **Step 3: Verify pytest markers work correctly**

```bash
pytest -m unit --collect-only
pytest -m integration --collect-only
```
Expected: First command shows only unit tests, second shows only integration tests

- [ ] **Step 4: Verify coverage separation**

```bash
# Unit test coverage
pytest tests/unit/ --cov=rhapsody_cli --cov-report=term --cov-report=html --cov-config=.coveragerc.unit

# Integration test coverage (if Rhapsody available)
pytest tests/integration/ --cov=rhapsody_cli --cov-report=term --cov-report=html --cov-config=.coveragerc.integration
```

Expected: Both generate separate coverage reports

- [ ] **Step 5: Create coverage configuration files**

Create `.coveragerc.unit`:

```ini
[run]
omit =
    tests/integration/*
    */tests/integration/*
```

Create `.coveragerc.integration`:

```ini
[run]
omit =
    tests/unit/*
    */tests/unit/*
```

- [ ] **Step 6: Commit coverage configuration**

```bash
git add .coveragerc.unit .coveragerc.integration
git commit -m "test: add separate coverage configs for unit/integration tests"
```

- [ ] **Step 7: Final verification test run**

```bash
# Full test suite execution
pytest tests/ -v

# Verify test project cleanup works
ls demos/test_project/
```
Expected: All tests pass, `demos/test_project/` is cleaned up after successful run

---

## Completion Checklist

- [ ] All tasks completed successfully
- [ ] Integration tests run on Windows with Rhapsody
- [ ] Integration tests skip gracefully without Rhapsody
- [ ] Unit and integration test coverage are separate
- [ ] Documentation updated with integration test instructions
- [ ] Test project cleanup works correctly
- [ ] Parent-child relationships validated (classes in packages, operations in classes)
- [ ] Exception handling tested for invalid hierarchies

## Success Criteria

- Integration tests can be run manually on Windows with Rhapsody installed
- Tests validate every wrapper method against real COM API
- Hierarchical relationships (parent-child) are properly tested
- Invalid relationships throw appropriate exceptions
- Coverage reports show separate metrics for unit vs integration tests
- Test data cleanup works reliably in both success and failure cases
