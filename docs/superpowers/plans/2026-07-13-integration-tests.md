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

### Task 11: Fix CLI Integration Test Isolation

**Files:**
- Modify: `tests/integration/cli/test_package_cli_integration.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest
- Produces: CLI tests that run against the isolated `demos/test_project/` project

**Root Cause:**
The 4 old CLI integration tests (in `tests/integration/cli/test_package_cli_integration.py`) never requested the `test_project` fixture. When pytest collects tests in lexical directory order (`cli/` before `models/`), the CLI tests run first. Since no fixture created a project, `RhapsodyContextAction._get_active_project()` → `app.active_project()` raised `RhapsodyRuntimeException: No active project is open in Rhapsody`.

The earlier relaxation of `_require_rhapsody` (removing the implicit "must have an open project" check) removed the safety net but didn't fix the underlying isolation problem.

**Fix:**
- Add a class-level `@pytest.fixture(autouse=True)` (`_use_test_project`) that requests the `test_project` fixture and caches it as `self.project`. This is **scoped to the test class** (not global), making the dependency explicit without affecting any other test.
- Add model-based assertions via `self.project` (e.g., `self.project.get_packages()`) to verify CLI commands actually created/deleted the expected model elements — going beyond just "the command didn't throw."
- Replace the timestamp-based uniqueness scheme (`int(time.time() * 1000) % 1000000`) with `uuid.uuid4().hex[:8]` to eliminate any theoretical collision risk between parallel test sessions.
- Add `@pytest.mark.integration` to the class for consistency with the registered marker.
- Update docstring to document the fixture dependency.

- [x] **Step 1: Update CLI test file with fixture and model assertions**

Apply the following changes to `tests/integration/cli/test_package_cli_integration.py`:
1. Replace docstring to describe `test_project` fixture dependency
2. `import time` → `import uuid`; add `import pytest`
3. Add `@pytest.mark.integration` to the class
4. Add `_use_test_project` autouse fixture that requests `test_project` → `self.project`
5. Replace `_generate_unique_name` with `uuid.uuid4().hex[:8]`-based version
6. Add model assertions to each test method using `self.project`:
   - Root create: assert `pkg_name` in `self.project.get_packages()`
   - Root duplicate: assert exactly 1 package named `pkg_name` after duplicate rejection
   - Nested create: assert child in `parent.get_nested_packages()`
   - Nested duplicate: assert exactly 1 child with that name after duplicate rejection

- [x] **Step 2: Run integration tests to verify fix**

```bash
pytest tests/integration/ -v
```

Expected: All 11 integration tests pass (4 CLI + 7 containment), regardless of collection order.

- [x] **Step 3: Run unit tests to verify no regressions**

```bash
pytest tests/unit/ -q
```

Expected: All 936 unit tests pass.

- [x] **Step 4: Commit the fix**

```bash
git add tests/integration/cli/test_package_cli_integration.py docs/superpowers/plans/2026-07-13-integration-tests.md
git commit -m "test: wire CLI integration tests to test_project fixture with model assertions"
```

---

## Integration Test Coverage Matrix

### Core Model Classes

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPModelElement** | `tests/integration/models/test_core.py` | get_name, set_name, get_meta_class, get_guid, get_owner, get_project, delete_from_project | 🟡 In Progress | High | None |
| **RPCollection** | `tests/integration/models/test_core.py` | iteration, get_nested_elements (with/without filter), count, indexing | 🟡 In Progress | High | RPModelElement |
| **RPUnit** | `tests/integration/models/test_core.py` | save, get_filename, get_canonical_filename | 🔴 Not Started | Medium | RPModelElement |
| **RPRelations** | `tests/integration/models/test_core.py` | get_relations, add_relation, find_relation | 🔴 Not Started | Medium | RPModelElement |
| **RPGraphics** | `tests/integration/models/test_core.py` | get_graphical_properties, set_graphical_properties | 🔴 Not Started | Low | RPModelElement |

### Containment Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPProject** | `tests/integration/models/elements/test_containment.py` | create_project, get_elements, add_package, save, close | 🟡 In Progress | Critical | None |
| **RPPackage** | `tests/integration/models/elements/test_containment.py` | add_package, get_nested_elements, get_higher_object, get_owner | 🟡 In Progress | Critical | RPProject |
| **RPModule** | `tests/integration/models/elements/test_containment.py` | add_module, get_elements, save | 🔴 Not Started | Medium | RPPackage |
| **RPComponent** | `tests/integration/models/elements/test_containment.py` | add_component, get_elements, get_realizing_classes | 🔴 Not Started | Medium | RPPackage |
| **RPComponentInstance** | `tests/integration/models/elements/test_containment.py` | add_component_instance, get_component, get_master | 🔴 Not Started | Low | RPComponent |
| **RPConfiguration** | `tests/integration/models/elements/test_containment.py` | get_elements, get_current_element, set_current_element | 🔴 Not Started | Low | RPProject |
| **RPCollaboration** | `tests/integration/models/elements/test_containment.py` | add_collaboration, get_roles, get_interactions | 🔴 Not Started | Low | RPPackage |
| **RPNode** | `tests/integration/models/elements/test_containment.py` | add_node, get_elements | 🔴 Not Started | Low | RPPackage |
| **RPProfile** | `tests/integration/models/elements/test_containment.py` | add_profile, get_profile_elements | 🔴 Not Started | Low | RPProject |

### Classifier Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPClassifier** | `tests/integration/models/elements/test_classifiers.py` | get_attributes, get_operations, add_attribute, get_containing_package | 🔴 Not Started | High | RPPackage |
| **RPClass** | `tests/integration/models/elements/test_classifiers.py` | add_class, add_superclass, get_superclasses, get_is_abstract, set_is_abstract, delete_class | 🟡 In Progress | Critical | RPPackage, RPClassifier |
| **RPOperation** | `tests/integration/models/elements/test_classifiers.py` | add_operation, get_parameters, get_owner, get_result, delete_operation | 🔴 Not Started | High | RPClass |
| **RPActor** | `tests/integration/models/elements/test_classifiers.py` | add_actor, get_communications | 🔴 Not Started | Medium | RPPackage |
| **RPUseCase** | `tests/integration/models/elements/test_classifiers.py` | add_usecase, get_actors, get_extensions | 🔴 Not Started | Medium | RPPackage |
| **RPInterfaceItem** | `tests/integration/models/elements/test_classifiers.py` | add_interface_item, get_operations | 🔴 Not Started | Medium | RPClassifier |
| **RPAssociationClass** | `tests/integration/models/elements/test_classifiers.py` | add_association_class, get_association_ends | 🔴 Not Started | Low | RPClass |
| **RPStereotype** | `tests/integration/models/elements/test_classifiers.py` | add_stereotype, get_stereotyped_elements | 🔴 Not Started | Low | RPModelElement |
| **RPStatechart** | `tests/integration/models/elements/test_classifiers.py` | add_statechart, get_states, get_transitions | 🔴 Not Started | Low | RPClass |

### Relation Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPRelation** | `tests/integration/models/elements/test_relations.py` | get_owner, get_other_end, get_name | 🔴 Not Started | High | RPModelElement |
| **RPAssociationRole** | `tests/integration/models/elements/test_relations.py` | add_association_role, get_role_name, get_multiplicity | 🔴 Not Started | High | RPClass |
| **RPDependency** | `tests/integration/models/elements/test_relations.py` | add_dependency, get_client, get_supplier | 🔴 Not Started | Medium | RPModelElement |
| **RPGeneralization** | `tests/integration/models/elements/test_relations.py` | add_generalization, get_super, get_sub | 🔴 Not Started | Medium | RPClassifier |
| **RPHyperlink** | `tests/integration/models/elements/test_relations.py` | add_hyperlink, get_url, get_anchor | 🔴 Not Started | Low | RPModelElement |
| **RPPort** | `tests/integration/models/elements/test_relations.py` | add_port, get_interfaces, get_aggregated | 🔴 Not Started | Medium | RPClass |
| **RPInstance** | `tests/integration/models/elements/test_relations.py` | add_instance, get_classifiers, get_slots | 🔴 Not Started | Low | RPClassifier |

### Activity Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPAction** | `tests/integration/models/elements/test_activity.py` | add_action, get_execution_language, get_body | 🔴 Not Started | Medium | RPClass |
| **RPActivity** | `tests/integration/models/elements/test_activity.py` | add_activity, get_actions, get_preconditions | 🔴 Not Started | Low | RPClassifier |

### Diagram Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPDiagram** | `tests/integration/models/elements/test_diagrams.py` | add_diagram, get_elements, get_name, save | 🔴 Not Started | Low | RPPackage |
| **RPUMLDiagram** | `tests/integration/models/elements/test_diagrams.py` | get_type, get_owned_elements | 🔴 Not Started | Low | RPDiagram |
| **RPActivityDiagram** | `tests/integration/models/elements/test_diagrams.py` | add_activity_diagram, get_activities | 🔴 Not Started | Low | RPClass |
| **RPSequenceDiagram** | `tests/integration/models/elements/test_diagrams.py` | add_sequence_diagram, get_lifelines | 🔴 Not Started | Low | RPClassifier |
| **RPCollaborationDiagram** | `tests/integration/models/elements/test_diagrams.py` | add_collaboration_diagram, get_links | 🔴 Not Started | Low | RPCollaboration |

### Requirement Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPRequirement** | `tests/integration/models/elements/test_requirements.py` | add_requirement, get_id, get_text, get_traces_to | 🔴 Not Started | Medium | RPPackage |
| **RPTrace** | `tests/integration/models/elements/test_requirements.py` | add_trace, get_traced_from, get_traced_to | 🔴 Not Started | Low | RPRequirement |

### Variable and Value Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPAttribute** | `tests/integration/models/elements/test_variables.py` | add_attribute, get_type, get_default_value, delete_attribute | 🔴 Not Started | High | RPClass |
| **RPParameter** | `tests/integration/models/elements/test_variables.py` | add_parameter, get_type, get_default_value | 🔴 Not Started | High | RPOperation |
| **RPVariable** | `tests/integration/models/elements/test_variables.py` | add_variable, get_type, get_scope | 🔴 Not Started | Medium | RPClassifier |
| **RPTypedValue** | `tests/integration/models/elements/test_values.py` | get_type, get_value, set_value | 🔴 Not Started | Low | RPVariable |

### Graphics and Interaction Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPGraphics** | `tests/integration/models/elements/test_graphics.py` | get_position, set_position, get_size, set_size | 🔴 Not Started | Low | RPDiagram |
| **RPLink** | `tests/integration/models/elements/test_graphics.py` | add_link, get_from, get_to | 🔴 Not Started | Low | RPDiagram |
| **RPEventReception** | `tests/integration/models/elements/test_interactions.py` | add_event_reception, get_event, get_operation | 🔴 Not Started | Low | RPClass |
| **RPInteraction** | `tests/integration/models/elements/test_interactions.py` | add_interaction, get_fragments, get_lifelines | 🔴 Not Started | Low | RPClassifier |

### Template and StateMachine Elements

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPTemplate** | `tests/integration/models/elements/test_templates.py` | add_template, get_template_parameters, bind_parameters | 🔴 Not Started | Low | RPClassifier |
| **RPStateMachine** | `tests/integration/models/elements/test_statemachine.py` | add_state_machine, get_states, get_transitions, get_initial_state | 🔴 Not Started | Low | RPClass |

### Support Classes

| Model Class | Integration Test File | Key Methods to Test | Test Status | Priority | Dependencies |
|-------------|----------------------|---------------------|-------------|----------|--------------|
| **RPCodeGen** | `tests/integration/models/support/test_codegen.py` | generate_code, get_codegen_properties | 🔴 Not Started | Low | RPProject |
| **RPFiles** | `tests/integration/models/support/test_files.py` | get_files, import_file, export_file | 🔴 Not Started | Low | RPProject |
| **RPIde** | `tests/integration/models/support/test_ide.py` | get_ide_properties, set_ide_properties | 🔴 Not Started | Low | RhapsodyApplication |

**Legend:**
- 🟢 **Complete** - All methods tested and passing
- 🟡 **In Progress** - Some methods tested, work ongoing
- 🔴 **Not Started** - No integration tests written yet
- **Priority** - Critical > High > Medium > Low
- **Dependencies** - Other model classes that must be tested first

---

## Method-Level Testing Checklist by Class

### RPModelElement (Base Class - Critical)
- [ ] **Core Identity** (Tested in Task 5)
  - [x] get_name() - Returns element name
  - [x] set_name() - Updates element name
  - [x] get_meta_class() - Returns element type
  - [x] get_guid() - Returns unique identifier
  - [ ] get_display_name() - Returns display name with stereotypes
  - [ ] get_full_name() - Returns fully qualified name
- [ ] **Hierarchy Navigation** (Partial in Task 7-8)
  - [x] get_owner() - Returns parent element
  - [ ] get_project() - Returns containing project
  - [ ] get_higher_object() - Returns next higher in containment
  - [ ] get_containing_package() - Returns containing package
- [ ] **Element Management**
  - [ ] delete_from_project() - Removes element from model
  - [ ] is_deleted() - Checks if element was deleted
  - [ ] can_delete() - Validates deletion is allowed
- [ ] **Properties and Metadata**
  - [ ] get_property() - Retrieves named property value
  - [ ] set_property() - Sets named property value
  - [ ] get_properties() - Gets all properties as dictionary
  - [ ] has_property() - Checks if property exists
- [ ] **Relations and Links**
  - [ ] add_link_to_element() - Creates graphical link
  - [ ] get_links() - Gets all links from element
  - [ ] find_element() - Finds nested element by name

### RPClass (Critical)
- [ ] **Creation and Deletion** (Partial in Task 7)
  - [x] package.add_class() - Creates class in package
  - [ ] add_class() - Creates nested class
  - [ ] delete_class() - Removes class from model
  - [ ] can_delete() - Checks if class can be deleted
- [ ] **Inheritance Management**
  - [ ] add_superclass() - Adds parent class
  - [ ] delete_superclass() - Removes parent class
  - [ ] get_superclasses() - Gets all parent classes
  - [ ] get_subclasses() - Gets all child classes
  - [ ] get_all_superclasses() - Gets complete inheritance tree
- [ ] **Class Properties**
  - [ ] get_is_abstract() - Checks if class is abstract
  - [ ] set_is_abstract() - Sets abstract property
  - [ ] get_is_final() - Checks if class is final
  - [ ] set_is_final() - Sets final property
  - [ ] get_is_active() - Checks if class is active
  - [ ] set_is_active() - Sets active property
  - [ ] get_is_composite() - Checks if class is composite
- [ ] **Type Management**
  - [ ] add_type() - Adds type relationship
  - [ ] delete_type() - Removes type relationship
  - [ ] get_types() - Gets all types
- [ ] **Operations**
  - [ ] add_operation() - Creates operation in class
  - [ ] get_operations() - Gets all operations
  - [ ] find_operation() - Finds operation by name
  - [ ] add_constructor() - Creates constructor
  - [ ] add_destructor() - Creates destructor
- [ ] **Attributes**
  - [ ] get_attributes() - Gets all attributes
  - [ ] find_attribute() - Finds attribute by name

### RPPackage (Critical)
- [ ] **Creation and Containment** (Partial in Task 8)
  - [x] project.add_package() - Creates package in project
  - [x] package.add_package() - Creates nested package
  - [ ] delete_package() - Removes package from model
- [ ] **Element Management**
  - [x] get_nested_elements() - Gets child elements
  - [ ] get_nested_elements_by_type() - Gets filtered children
  - [ ] find_element() - Finds element by name
  - [ ] find_nested_element() - Searches recursively
- [ ] **Hierarchy Navigation** (Partial in Task 8)
  - [x] get_owner() - Returns parent package/project
  - [ ] get_higher_object() - Returns next higher level
  - [ ] get_project() - Returns containing project
- [ ] **Package Properties**
  - [ ] get_is_default() - Checks if default package
  - [ ] get_is_library() - Checks if library package
  - [ ] get_is_controlled() - Checks if under version control

### RPProject (Critical)
- [ ] **Project Management** (Partial in Task 8)
  - [x] create_project() - Creates new project file
  - [ ] open_project() - Opens existing project
  - [ ] save_project() - Saves project changes
  - [ ] close_project() - Closes project
  - [ ] delete_project() - Deletes project file
- [ ] **Element Access**
  - [x] get_nested_elements() - Gets top-level elements
  - [ ] get_all_elements() - Gets all elements recursively
  - [ ] find_element() - Finds element by GUID or name
- [ ] **Project Properties**
  - [ ] get_author() - Gets project author
  - [ ] set_author() - Sets project author
  - [ ] get_description() - Gets project description
  - [ ] set_description() - Sets project description
  - [ ] get_default_language() - Gets default code generation language

### RPCollection (High Priority)
- [ ] **Iteration and Access** (Partial in Task 6)
  - [x] iteration support - Iterates over elements
  - [x] get_count() - Returns element count
  - [ ] get_item(index) - Gets element at 0-based index
  - [ ] contains(element) - Checks if element in collection
- [ ] **Filtering**
  - [x] get_nested_elements() - Gets all elements
  - [x] get_nested_elements(metaClass) - Gets filtered elements
  - [ ] find_first(metaClass) - Gets first matching element
  - [ ] find_all(metaClass) - Gets all matching elements

### RPOperation (High Priority)
- [ ] **Creation and Management**
  - [ ] add_operation() - Creates operation in class
  - [ ] delete_operation() - Removes operation
  - [ ] get_result() - Gets return parameter
  - [ ] set_result() - Sets return parameter
- [ ] **Parameters**
  - [ ] add_parameter() - Creates parameter
  - [ ] get_parameters() - Gets all parameters
  - [ ] delete_parameter() - Removes parameter
- [ ] **Operation Properties**
  - [ ] get_is_static() - Checks if static
  - [ ] set_is_static() - Sets static property
  - [ ] get_is_virtual() - Checks if virtual
  - [ ] set_is_virtual() - Sets virtual property
  - [ ] get_visibility() - Gets visibility scope
  - [ ] set_visibility() - Sets visibility scope

### RPAttribute (High Priority)
- [ ] **Creation and Management**
  - [ ] add_attribute() - Creates attribute in class
  - [ ] delete_attribute() - Removes attribute
  - [ ] get_type() - Gets attribute type
  - [ ] set_type() - Sets attribute type
- [ ] **Attribute Properties**
  - [ ] get_default_value() - Gets default value
  - [ ] set_default_value() - Sets default value
  - [ ] get_visibility() - Gets visibility scope
  - [ ] set_visibility() - Sets visibility scope
  - [ ] get_is_static() - Checks if static
  - [ ] set_is_static() - Sets static property
  - [ ] get_is_const() - Checks if constant
  - [ ] set_is_const() - Sets constant property

### RPAssociationRole (High Priority)
- [ ] **Association Management**
  - [ ] add_association_role() - Creates association end
  - [ ] get_other_role() - Gets opposite association end
  - [ ] get_association() - Gets parent association
- [ ] **Role Properties**
  - [ ] get_role_name() - Gets role name
  - [ ] set_role_name() - Sets role name
  - [ ] get_multiplicity() - Gets multiplicity
  - [ ] set_multiplicity() - Sets multiplicity
  - [ ] get_navigability() - Gets navigability
  - [ ] set_navigability() - Sets navigability
  - [ ] get_aggregation() - Gets aggregation type
  - [ ] set_aggregation() - Sets aggregation type

### RPDependency (Medium Priority)
- [ ] **Dependency Management**
  - [ ] add_dependency() - Creates dependency
  - [ ] add_dependency_to() - Creates dependency to target
  - [ ] add_dependency_between() - Creates bidirectional dependency
  - [ ] delete_dependency() - Removes dependency
- [ ] **Dependency Properties**
  - [ ] get_client() - Gets depending element
  - [ ] get_supplier() - Gets depended-on element
  - [ ] get_name() - Gets dependency name
  - [ ] set_name() - Sets dependency name

### RPGeneralization (Medium Priority)
- [ ] **Generalization Management**
  - [ ] add_generalization() - Creates generalization
  - [ ] delete_generalization() - Removes generalization
- [ ] **Generalization Properties**
  - [ ] get_super() - Gets parent classifier
  - [ ] get_sub() - Gets child classifier
  - [ ] get_name() - Gets generalization name

### RPPackage (Medium Priority)
- [ ] **Package Creation** (Partial in Task 8)
  - [x] add_package() - Creates package
  - [ ] delete_package() - Removes package
- [ ] **Package Contents**
  - [x] get_nested_elements() - Gets child elements
  - [ ] get_elements() - Gets direct children
  - [ ] find_element() - Finds element by name
- [ ] **Package Properties**
  - [ ] get_is_default() - Checks if default package
  - [ ] get_is_library() - Checks if library package

### RPDiagram (Low Priority)
- [ ] **Diagram Creation**
  - [ ] add_diagram() - Creates diagram
  - [ ] delete_diagram() - Removes diagram
- [ ] **Diagram Contents**
  - [ ] get_elements() - Gets diagram elements
  - [ ] add_element() - Adds element to diagram
  - [ ] delete_element() - Removes element from diagram
- [ ] **Diagram Properties**
  - [ ] get_name() - Gets diagram name
  - [ ] set_name() - Sets diagram name
  - [ ] get_type() - Gets diagram type
  - [ ] save() - Saves diagram layout

---

## Integration Test Execution Status

### Test Suite Status
- **Total Model Classes:** 50+ classes
- **Integration Test Files Created:** 3/25 planned
- **Test Coverage by Priority:**
  - Critical: 3/6 classes (50%) 🟡
  - High: 0/8 classes (0%) 🔴
  - Medium: 0/12 classes (0%) 🔴
  - Low: 0/24+ classes (0%) 🔴

### Hierarchical Relationship Coverage
- [x] **Package → Class** (Task 7) - Class creation in package
- [x] **Class → Operation** (Task 7) - Operation creation in class
- [x] **Package → Package** (Task 8) - Nested package creation
- [x] **Project → Package** (Task 8) - Top-level package creation
- [ ] **Class → Attribute** - Attribute creation in class
- [ ] **Class → Superclass** - Inheritance relationships
- [ ] **Class → Interface** - Interface realization
- [ ] **Association → Role** - Association ends
- [ ] **Package → Diagram** - Diagram creation
- [ ] **Invalid hierarchy exception handling** (Partial in Task 7)

### Exception Handling Test Coverage
- [x] **Invalid parent-child relationships** (Partial in Task 7)
- [ ] **Deletion of referenced elements**
- [ ] **Duplicate element names**
- [ ] **Invalid type assignments**
- [ ] **Circular dependencies**
- [ ] **Invalid multiplicity values**
- [ ] **COM error translation**

---

## Completion Checklist

- [ ] All Critical priority classes have integration tests (6/6)
- [ ] All High priority classes have integration tests (0/8)
- [ ] 50%+ of Medium priority classes have integration tests (0/12)
- [ ] Core infrastructure tasks (Tasks 1-4) completed
- [ ] Integration tests run on Windows with Rhapsody
- [ ] Integration tests skip gracefully without Rhapsody
- [ ] Unit and integration test coverage are separate
- [ ] Documentation updated with integration test instructions
- [ ] Test project cleanup works correctly
- [ ] Parent-child relationships validated (classes in packages, operations in classes)
- [ ] Exception handling tested for invalid hierarchies
- [ ] All RPModelElement base methods tested (8/20 methods)
- [ ] All RPClass critical methods tested (5/25 methods)
- [ ] All RPPackage critical methods tested (4/15 methods)
- [ ] All RPProject critical methods tested (3/15 methods)

## Success Criteria

- **Coverage:** Integration tests can be run manually on Windows with Rhapsody installed
- **Validation:** Tests validate every wrapper method against real COM API
- **Hierarchy:** Hierarchical relationships (parent-child) are properly tested
- **Exceptions:** Invalid relationships throw appropriate exceptions
- **Separation:** Coverage reports show separate metrics for unit vs integration tests
- **Cleanup:** Test data cleanup works reliably in both success and failure cases
- **Progress:** At least 50% of Critical and High priority classes have integration tests
- **Completeness:** All base RPModelElement methods have integration tests
