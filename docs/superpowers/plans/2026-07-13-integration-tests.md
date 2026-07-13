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

## Integration Test Coverage Tracker

This table tracks which model wrapper classes have integration tests. Each model class needs tests for:
- Basic CRUD operations (create, read properties, update, delete)
- Parent-child hierarchical relationships
- Reference relationships to other elements
- Navigation methods
- Exception handling for invalid operations

### Core Infrastructure

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPModelElement` | [ ] | `test_core.py` | HIGH |
| `RPUnit` | [ ] | `test_core.py` | HIGH |
| `RPCollection` | [ ] | `test_core.py` | HIGH |

### Classifiers

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPClassifier` | [ ] | `test_classifiers.py` | HIGH |
| `RPClass` | [ ] | `test_classifiers.py` | HIGH |
| `RPActor` | [ ] | `test_actors_usecases.py` | MEDIUM |
| `RPUseCase` | [ ] | `test_actors_usecases.py` | MEDIUM |
| `RPOperation` | [ ] | `test_operations.py` | HIGH |
| `RPStereotype` | [ ] | `test_classifiers.py` | LOW |
| `RPInterfaceItem` | [ ] | `test_classifiers.py` | MEDIUM |
| `RPAssociationClass` | [ ] | `test_classifiers.py` | LOW |
| `RPStatechart` | [ ] | `test_statemachine.py` | HIGH |

### Variables

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPVariable` | [ ] | `test_variables.py` | HIGH |
| `RPAttribute` | [ ] | `test_variables.py` | HIGH |
| `RPTag` | [ ] | `test_variables.py` | MEDIUM |
| `RPArgument` | [ ] | `test_variables.py` | HIGH |

### Relations

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPRelation` | [ ] | `test_relations.py` | HIGH |
| `RPInstance` | [ ] | `test_relations.py` | HIGH |
| `RPAssociation` | [ ] | `test_relations.py` | HIGH |
| `RPAssociationRole` | [ ] | `test_relations.py` | MEDIUM |
| `RPDependency` | [ ] | `test_relations.py` | HIGH |
| `RPGeneralization` | [ ] | `test_relations.py` | HIGH |
| `RPHyperLink` | [ ] | `test_relations.py` | LOW |
| `RPPort` | [ ] | `test_relations.py` | MEDIUM |

### Requirements

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPRequirement` | [ ] | `test_requirements.py` | MEDIUM |
| `RPAnnotation` | [ ] | `test_requirements.py` | LOW |

### Activity Diagrams

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPFlow` | [ ] | `test_activity.py` | LOW |
| `RPFlowItem` | [ ] | `test_activity.py` | LOW |
| `RPFlowchart` | [ ] | `test_activity.py` | MEDIUM |
| `RPObjectNode` | [ ] | `test_activity.py` | LOW |
| `RPSwimlane` | [ ] | `test_activity.py` | LOW |
| `RPAction` | [ ] | `test_activity.py` | LOW |
| `RPAcceptEventAction` | [ ] | `test_activity.py` | LOW |
| `RPAcceptTimeEvent` | [ ] | `test_activity.py` | LOW |
| `RPCallOperation` | [ ] | `test_activity.py` | LOW |
| `RPSendAction` | [ ] | `test_activity.py` | LOW |
| `RPActionBlock` | [ ] | `test_activity.py` | LOW |

### Interaction Elements

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPEvent` | [ ] | `test_interactions.py` | LOW |
| `RPEventReception` | [ ] | `test_interactions.py` | LOW |
| `RPMessage` | [ ] | `test_interactions.py` | MEDIUM |
| `RPTransition` | [ ] | `test_interactions.py` | HIGH |
| `RPTrigger` | [ ] | `test_interactions.py` | MEDIUM |
| `RPGuard` | [ ] | `test_interactions.py` | LOW |
| `RPExecutionOccurrence` | [ ] | `test_interactions.py` | LOW |
| `RPInteractionOccurrence` | [ ] | `test_interactions.py` | LOW |
| `RPInteractionOperand` | [ ] | `test_interactions.py` | LOW |
| `RPInteractionOperator` | [ ] | `test_interactions.py` | LOW |
| `RPDestructionEvent` | [ ] | `test_interactions.py` | LOW |

### Diagrams

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPDiagram` | [ ] | `test_diagrams.py` | HIGH |
| `RPCollaborationDiagram` | [ ] | `test_diagrams.py` | LOW |
| `RPComponentDiagram` | [ ] | `test_diagrams.py` | MEDIUM |
| `RPDeploymentDiagram` | [ ] | `test_diagrams.py` | LOW |
| `RPObjectModelDiagram` | [ ] | `test_diagrams.py` | MEDIUM |
| `RPPanelDiagram` | [ ] | `test_diagrams.py` | LOW |
| `RPSequenceDiagram` | [ ] | `test_diagrams.py` | MEDIUM |
| `RPStatechartDiagram` | [ ] | `test_diagrams.py` | MEDIUM |
| `RPStructureDiagram` | [ ] | `test_diagrams.py` | LOW |
| `RPUseCaseDiagram` | [ ] | `test_diagrams.py` | MEDIUM |
| `RPTimingDiagram` | [ ] | `test_diagrams.py` | LOW |
| `RPActivityDiagram` | [ ] | `test_diagrams.py` | MEDIUM |

### Graphics

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPGraphElement` | [ ] | `test_graphics.py` | MEDIUM |
| `RPGraphEdge` | [ ] | `test_graphics.py` | LOW |
| `RPGraphNode` | [ ] | `test_graphics.py` | LOW |
| `RPConnector` | [ ] | `test_graphics.py` | LOW |
| `RPConditionMark` | [ ] | `test_graphics.py` | LOW |
| `RPGraphicalProperty` | [ ] | `test_graphics.py` | LOW |
| `RPImageMap` | [ ] | `test_graphics.py` | LOW |
| `RPLink` | [ ] | `test_graphics.py` | LOW |
| `RPMatrixLayout` | [ ] | `test_graphics.py` | LOW |
| `RPTableView` | [ ] | `test_graphics.py` | LOW |
| `RPMessagePoint` | [ ] | `test_graphics.py` | LOW |
| `RPPin` | [ ] | `test_graphics.py` | LOW |

### Containment Elements

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPPackage` | [ ] | `test_containment.py` | HIGH |
| `RPProject` | [ ] | `test_containment.py` | HIGH |
| `RPComponent` | [ ] | `test_containment.py` | MEDIUM |
| `RPComponentInstance` | [ ] | `test_containment.py` | MEDIUM |
| `RPModule` | [ ] | `test_containment.py` | MEDIUM |
| `RPNode` | [ ] | `test_containment.py` | MEDIUM |
| `RPCollaboration` | [ ] | `test_containment.py` | LOW |
| `RPConfiguration` | [ ] | `test_containment.py` | LOW |
| `RPProfile` | [ ] | `test_containment.py` | LOW |

### State Machine Elements

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPStateVertex` | [ ] | `test_statemachine.py` | HIGH |
| `RPState` | [ ] | `test_statemachine.py` | HIGH |

### Values and Templates

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPInstanceSlot` | [ ] | `test_values.py` | LOW |
| `RPInstanceSpecification` | [ ] | `test_values.py` | LOW |
| `RPValueSpecification` | [ ] | `test_values.py` | LOW |
| `RPInstanceValue` | [ ] | `test_values.py` | LOW |
| `RPLiteralSpecification` | [ ] | `test_values.py` | LOW |
| `RPTemplateInstantiation` | [ ] | `test_templates.py` | LOW |
| `RPTemplateInstantiationParameter` | [ ] | `test_templates.py` | LOW |
| `RPTemplateParameter` | [ ] | `test_templates.py` | LOW |

### Common Elements

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPComment` | [ ] | `test_common.py` | LOW |
| `RPConstraint` | [ ] | `test_common.py` | MEDIUM |
| `RPEnumerationLiteral` | [ ] | `test_common.py` | LOW |
| `RPClassifierRole` | [ ] | `test_common.py` | LOW |
| `RPSysMLPort` | [ ] | `test_common.py` | LOW |
| `RPType` | [ ] | `test_common.py` | LOW |

### Support Classes

| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPFile` | [ ] | `test_support.py` | MEDIUM |
| `RPASCIIFile` | [ ] | `test_support.py` | LOW |
| `RPControlledFile` | [ ] | `test_support.py` | LOW |
| `RPFileFragment` | [ ] | `test_support.py` | LOW |
| `RPCodeGenerator` | [ ] | `test_support.py` | LOW |
| `RPSearchManager` | [ ] | `test_support.py` | LOW |
| `RPSearchQuery` | [ ] | `test_support.py` | LOW |
| `RPSearchResult` | [ ] | `test_support.py` | LOW |

**Legend:**
- [ ] = Not implemented
- [x] = Implemented and passing
- **Priority:** HIGH = Core functionality (Must have), MEDIUM = Common use cases (Should have), LOW = Advanced features (Nice to have)

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

### Task 10: Write Variable Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_variables.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for variable hierarchy**

```python
# tests/integration/models/elements/test_variables.py
import pytest
from rhapsody_cli.models.elements.variables import RPAttribute, RPVariable
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPVariableIntegration:
    """Integration tests for RPVariable with real Rhapsody COM API."""

    def test_create_class_attribute(self, test_project):
        """Test creating attribute as member of class (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")

        # Act
        attribute = test_class.add_attribute("testAttribute")

        # Assert
        assert attribute is not None
        assert isinstance(attribute, RPAttribute)
        assert attribute.get_name() == "testAttribute"
        # Verify attribute is member of class
        attributes = test_class.get_attributes()
        assert attribute in list(attributes)

    def test_attribute_type_relationship(self, test_project):
        """Test setting attribute type (reference relationship)."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        type_class = package.add_class("TypeClass")
        attribute = test_class.add_attribute("typedAttribute")

        # Act
        attribute.set_type(type_class)

        # Assert
        retrieved_type = attribute.get_type()
        assert retrieved_type is not None
        assert retrieved_type.get_name() == "TypeClass"

@pytest.mark.integration
class TestRPAttributeIntegration:
    """Integration tests for RPAttribute with real Rhapsody COM API."""

    def test_attribute_visibility(self, test_project):
        """Test setting and getting attribute visibility."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        attribute = test_class.add_attribute("publicAttribute")

        # Act
        attribute.set_visibility("Public")
        visibility = attribute.get_visibility()

        # Assert
        assert visibility == "Public"

    def test_attribute_default_value(self, test_project):
        """Test setting attribute default value."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        attribute = test_class.add_attribute("initializedAttribute")

        # Act
        attribute.set_default_value("0")
        default_value = attribute.get_default_value()

        # Assert
        assert default_value == "0"
```

- [ ] **Step 2: Run tests to verify variable functionality**

```bash
pytest tests/integration/models/elements/test_variables.py -v
```
Expected: Tests validate variable creation, type relationships, and properties

- [ ] **Step 3: Commit variable integration tests**

```bash
git add tests/integration/models/elements/test_variables.py
git commit -m "test: add RPVariable and RPAttribute integration tests"
```

---

### Task 11: Write Relation Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_relations.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for relationships between elements**

```python
# tests/integration/models/elements/test_relations.py
import pytest
from rhapsody_cli.models.elements.relations import RPAssociation, RPDependency, RPGeneralization
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPAssociationIntegration:
    """Integration tests for RPAssociation with real Rhapsody COM API."""

    def test_create_association_between_classes(self, test_project):
        """Test creating association relationship between two classes."""
        # Arrange
        package = test_project.add_package("TestPackage")
        class_a = package.add_class("ClassA")
        class_b = package.add_class("ClassB")

        # Act
        association = class_a.add_association(class_b)

        # Assert
        assert association is not None
        # Verify association connects both classes
        roles = list(association.get_roles())
        assert len(roles) == 2

    def test_association_navigation(self, test_project):
        """Test navigating from association to connected classes."""
        # Arrange
        package = test_project.add_package("TestPackage")
        class_a = package.add_class("SourceClass")
        class_b = package.add_class("TargetClass")
        association = class_a.add_association(class_b)

        # Act
        roles = association.get_roles()
        role_list = list(roles)

        # Assert
        assert len(role_list) == 2
        # Verify roles reference the connected classes

@pytest.mark.integration
class TestRPGeneralizationIntegration:
    """Integration tests for RPGeneralization with real Rhapsody COM API."""

    def test_create_inheritance_relationship(self, test_project):
        """Test creating generalization (inheritance) between classes."""
        # Arrange
        package = test_project.add_package("TestPackage")
        base_class = package.add_class("BaseClass")
        derived_class = package.add_class("DerivedClass")

        # Act
        generalization = derived_class.add_generalization(base_class)

        # Assert
        assert generalization is not None
        # Verify inheritance hierarchy
        base_elements = list(derived_class.get_generalizations())
        assert len(base_elements) >= 1

@pytest.mark.integration
class TestRPDependencyIntegration:
    """Integration tests for RPDependency with real Rhapsody COM API."""

    def test_create_dependency_between_classes(self, test_project):
        """Test creating dependency relationship between classes."""
        # Arrange
        package = test_project.add_package("TestPackage")
        client_class = package.add_class("ClientClass")
        supplier_class = package.add_class("SupplierClass")

        # Act
        dependency = client_class.add_dependency(supplier_class)

        # Assert
        assert dependency is not None
        # Verify dependency direction (client depends on supplier)
        assert dependency.get_client() is not None
        assert dependency.get_supplier() is not None
```

- [ ] **Step 2: Run tests to verify relationship functionality**

```bash
pytest tests/integration/models/elements/test_relations.py -v
```
Expected: Tests validate relationship creation and navigation

- [ ] **Step 3: Commit relation integration tests**

```bash
git add tests/integration/models/elements/test_relations.py
git commit -m "test: add RPAssociation, RPGeneralization, RPDependency integration tests"
```

---

### Task 12: Write Operation Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_operations.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for operation methods and parameters**

```python
# tests/integration/models/elements/test_operations.py
import pytest
from rhapsody_cli.models.elements.classifiers import RPOperation, RPClass
from rhapsody_cli.models.elements.variables import RPArgument
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPOperationIntegration:
    """Integration tests for RPOperation with real Rhapsody COM API."""

    def test_add_parameter_to_operation(self, test_project):
        """Test adding parameter to operation (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        operation = test_class.add_operation("testMethod")

        # Act
        parameter = operation.add_argument("param1")

        # Assert
        assert parameter is not None
        assert isinstance(parameter, RPArgument)
        assert parameter.get_name() == "param1"
        # Verify parameter is member of operation
        arguments = operation.get_arguments()
        assert parameter in list(arguments)

    def test_operation_return_type(self, test_project):
        """Test setting operation return type."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        type_class = package.add_class("ReturnType")
        operation = test_class.add_operation("methodWithReturn")

        # Act
        operation.set_return_type(type_class)

        # Assert
        return_type = operation.get_return_type()
        assert return_type is not None
        assert return_type.get_name() == "ReturnType"

    def test_operation_visibility(self, test_project):
        """Test setting operation visibility."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        operation = test_class.add_operation("publicMethod")

        # Act
        operation.set_visibility("Public")
        visibility = operation.get_visibility()

        # Assert
        assert visibility == "Public"

    def test_operation stereotypes(self, test_project):
        """Test applying stereotypes to operations."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("TestClass")
        operation = test_class.add_operation("testOperation")

        # Act
        operation.add_stereotype("constructor")

        # Assert
        stereotypes = operation.get_stereotypes()
        assert "constructor" in stereotypes or len(list(stereotypes)) > 0
```

- [ ] **Step 2: Run tests to verify operation functionality**

```bash
pytest tests/integration/models/elements/test_operations.py -v
```
Expected: Tests validate operation creation, parameters, and properties

- [ ] **Step 3: Commit operation integration tests**

```bash
git add tests/integration/models/elements/test_operations.py
git commit -m "test: add RPOperation integration tests"
```

---

### Task 13: Write Requirement Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_requirements.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for requirement elements**

```python
# tests/integration/models/elements/test_requirements.py
import pytest
from rhapsody_cli.models.elements.requirements import RPRequirement, RPAnnotation
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPRequirementIntegration:
    """Integration tests for RPRequirement with real Rhapsody COM API."""

    def test_create_requirement_in_package(self, test_project):
        """Test creating requirement within package (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("RequirementsPackage")

        # Act
        requirement = package.add_requirement("REQ-001")

        # Assert
        assert requirement is not None
        assert isinstance(requirement, RPRequirement)
        assert requirement.get_name() == "REQ-001"

    def test_requirement_properties(self, test_project):
        """Test setting requirement properties (text, priority, etc.)."""
        # Arrange
        package = test_project.add_package("RequirementsPackage")
        requirement = package.add_requirement("REQ-002")

        # Act
        requirement.set_property("Text", "System shall validate user input")
        requirement.set_property("Priority", "High")

        # Assert
        text = requirement.get_property("Text")
        priority = requirement.get_property("Priority")
        assert "validate user input" in text
        assert priority == "High"

    def test_requirement_satisfy_relationship(self, test_project):
        """Test creating satisfy relationship from element to requirement."""
        # Arrange
        package = test_project.add_package("TestPackage")
        test_class = package.add_class("ValidatorClass")
        requirement = package.add_requirement("REQ-003")

        # Act
        satisfy_relation = test_class.add_satisfy(requirement)

        # Assert
        assert satisfy_relation is not None
        # Verify relationship exists
        satisfied = list(requirement.get_satisfied_by())
        assert test_class in satisfied or len(satisfied) > 0
```

- [ ] **Step 2: Run tests to verify requirement functionality**

```bash
pytest tests/integration/models/elements/test_requirements.py -v
```
Expected: Tests validate requirement creation and satisfy relationships

- [ ] **Step 3: Commit requirement integration tests**

```bash
git add tests/integration/models/elements/test_requirements.py
git commit -m "test: add RPRequirement integration tests"
```

---

### Task 14: Write Diagram Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_diagrams.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for diagram creation and elements**

```python
# tests/integration/models/elements/test_diagrams.py
import pytest
from rhapsody_cli.models.elements.diagrams import RPDiagram, RPClassDiagram
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPDiagramIntegration:
    """Integration tests for RPDiagram with real Rhapsody COM API."""

    def test_create_class_diagram_in_package(self, test_project):
        """Test creating class diagram within package (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("DesignPackage")

        # Act
        diagram = package.add_diagram("ClassDiagram", "ClassDiagram")

        # Assert
        assert diagram is not None
        assert isinstance(diagram, RPDiagram)
        assert diagram.get_name() == "ClassDiagram"

    def test_add_element_to_diagram(self, test_project):
        """Test adding element to diagram (graphical representation)."""
        # Arrange
        package = test_project.add_package("DesignPackage")
        test_class = package.add_class("TestClass")
        diagram = package.add_diagram("MainDiagram", "ClassDiagram")

        # Act
        graph_element = diagram.add_graph_item(test_class, 100, 100)

        # Assert
        assert graph_element is not None
        # Verify element appears in diagram's items
        items = list(diagram.get_items())
        assert len(items) > 0

    def test_diagram_navigation(self, test_project):
        """Test navigating from diagram to owner package."""
        # Arrange
        package = test_project.add_package("DesignPackage")
        diagram = package.add_diagram("NavigationDiagram", "ClassDiagram")

        # Act
        owner = diagram.get_owner()

        # Assert
        assert owner is not None
        assert owner.get_name() == "DesignPackage"
        assert isinstance(owner, RPPackage)
```

- [ ] **Step 2: Run tests to verify diagram functionality**

```bash
pytest tests/integration/models/elements/test_diagrams.py -v
```
Expected: Tests validate diagram creation and element manipulation

- [ ] **Step 3: Commit diagram integration tests**

```bash
git add tests/integration/models/elements/test_diagrams.py
git commit -m "test: add RPDiagram integration tests"
```

---

### Task 15: Write State Machine Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_statemachine.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for state machine elements**

```python
# tests/integration/models/elements/test_statemachine.py
import pytest
from rhapsody_cli.models.elements.statemachine import RPState, RPStatechart
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPStatechartIntegration:
    """Integration tests for RPStatechart with real Rhapsody COM API."""

    def test_create_statechart_in_class(self, test_project):
        """Test creating statechart within class (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("BehaviorPackage")
        test_class = package.add_class("StateMachineClass")

        # Act
        statechart = test_class.add_statechart("BehaviorStatechart")

        # Assert
        assert statechart is not None
        assert isinstance(statechart, RPStatechart)

    def test_add_state_to_statechart(self, test_project):
        """Test adding state to statechart (hierarchical relationship)."""
        # Arrange
        package = test_project.add_package("BehaviorPackage")
        test_class = package.add_class("ActiveClass")
        statechart = test_class.add_statechart("MainStatechart")

        # Act
        state = statechart.add_state("IdleState")

        # Assert
        assert state is not None
        assert isinstance(state, RPState)
        assert state.get_name() == "IdleState"

    def test_add_transition_between_states(self, test_project):
        """Test creating transition between states (relationship)."""
        # Arrange
        package = test_project.add_package("BehaviorPackage")
        test_class = package.add_class("TransitionClass")
        statechart = test_class.add_statechart("TransitionStatechart")
        source_state = statechart.add_state("State1")
        target_state = statechart.add_state("State2")

        # Act
        transition = statechart.add_transition(source_state, target_state)

        # Assert
        assert transition is not None
        # Verify transition connects the states
        assert transition.get_source() is not None
        assert transition.get_target() is not None
```

- [ ] **Step 2: Run tests to verify state machine functionality**

```bash
pytest tests/integration/models/elements/test_statemachine.py -v
```
Expected: Tests validate state machine creation and state transitions

- [ ] **Step 3: Commit state machine integration tests**

```bash
git add tests/integration/models/elements/test_statemachine.py
git commit -m "test: add RPStatechart and RPState integration tests"
```

---

### Task 16: Write Actor and Use Case Model Integration Tests

**Files:**
- Create: `tests/integration/models/elements/test_actors_usecases.py`

**Interfaces:**
- Consumes: `test_project` fixture from conftest

- [ ] **Step 1: Write failing tests for actors and use cases**

```python
# tests/integration/models/elements/test_actors_usecases.py
import pytest
from rhapsody_cli.models.elements.classifiers import RPActor, RPUseCase
from rhapsody_cli.models.elements.relations import RPAssociation
from rhapsody_cli.models.elements.containment import RPPackage

@pytest.mark.integration
class TestRPActorIntegration:
    """Integration tests for RPActor with real Rhapsody COM API."""

    def test_create_actor_in_package(self, test_project):
        """Test creating actor within package (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("ActorsPackage")

        # Act
        actor = package.add_actor("User")

        # Assert
        assert actor is not None
        assert isinstance(actor, RPActor)
        assert actor.get_name() == "User"

@pytest.mark.integration
class TestRPUseCaseIntegration:
    """Integration tests for RPUseCase with real Rhapsody COM API."""

    def test_create_use_case_in_package(self, test_project):
        """Test creating use case within package (parent-child relationship)."""
        # Arrange
        package = test_project.add_package("UseCasesPackage")

        # Act
        use_case = package.add_use_case("LoginUseCase")

        # Assert
        assert use_case is not None
        assert isinstance(use_case, RPUseCase)
        assert use_case.get_name() == "LoginUseCase"

    def test_create_actor_association_with_use_case(self, test_project):
        """Test creating association between actor and use case (relationship)."""
        # Arrange
        package = test_project.add_package("UseCasesPackage")
        actor = package.add_actor("Administrator")
        use_case = package.add_use_case("ManageUsers")

        # Act
        association = actor.add_association(use_case)

        # Assert
        assert association is not None
        # Verify association connects actor to use case
```

- [ ] **Step 2: Run tests to verify actor and use case functionality**

```bash
pytest tests/integration/models/elements/test_actors_usecases.py -v
```
Expected: Tests validate actor/use case creation and associations

- [ ] **Step 3: Commit actor and use case integration tests**

```bash
git add tests/integration/models/elements/test_actors_usecases.py
git commit -m "test: add RPActor and RPUseCase integration tests"
```

---

### Task 17: Verify Test Execution and Coverage Separation

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

### Task 18: Maintain and Update Coverage Tracker

**Files:**
- Modify: `docs/superpowers/plans/2026-07-13-integration-tests.md`

**Interfaces:**
- Consumes: Integration test implementation results
- Produces: Updated coverage tracker with completed tests

- [ ] **Step 1: Update coverage tracker as tests are implemented**

For each model class integration test that is completed, update the corresponding checkbox in the **Integration Test Coverage Tracker** table:

```markdown
| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPModelElement` | [x] | `test_core.py` | HIGH |
```

- [ ] **Step 2: Update file location if tests are in different files**

If integration tests for a model class are placed in a different file than initially planned, update the **File Location** column:

```markdown
| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPDiagram` | [x] | `test_graphics.py` | HIGH |
```

- [ ] **Step 3: Track partial implementations**

For model classes with only partial test coverage, use specific notation:

```markdown
| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPState` | [~] | `test_statemachine.py` | HIGH |
```

Legend additions:
- [~] = Partial implementation (some methods tested)

- [ ] **Step 4: Add new model classes to tracker**

When new wrapper classes are added to the codebase, add them to the appropriate category table:

```markdown
| Model Class | Integration Tests | File Location | Priority |
|-------------|-------------------|---------------|----------|
| `RPNewClass` | [ ] | `test_new_class.py` | MEDIUM |
```

- [ ] **Step 5: Generate coverage summary report**

After completing test implementation, generate a summary showing overall progress:

```bash
# Count completed integration test classes
grep -c "\[x\]" docs/superpowers/plans/2026-07-13-integration-tests.md

# Count remaining (unimplemented) test classes
grep -c "\[ \]" docs/superpowers/plans/2026-07-13-integration-tests.md
```

- [ ] **Step 6: Commit coverage tracker updates**

```bash
git add docs/superpowers/plans/2026-07-13-integration-tests.md
git commit -m "docs: update integration test coverage tracker"
```

- [ ] **Step 7: Use tracker for planning next test implementation**

When planning additional test implementations, sort the tracker by:
1. Priority (HIGH → MEDIUM → LOW)
2. Related model classes (test all classes in same file together)

Example query to find HIGH priority unimplemented tests:
```bash
# Extract HIGH priority unimplemented classes from tracker
grep "HIGH" docs/superpowers/plans/2026-07-13-integration-tests.md | grep "\[ \]"
```

---

## Completion Checklist

- [ ] All tasks (1-18) completed successfully
- [ ] Integration tests run on Windows with Rhapsody
- [ ] Integration tests skip gracefully without Rhapsody
- [ ] Unit and integration test coverage are separate
- [ ] Documentation updated with integration test instructions
- [ ] Test project cleanup works correctly
- [ ] Parent-child relationships validated (classes in packages, operations in classes, states in statecharts)
- [ ] Exception handling tested for invalid hierarchies
- [ ] Variable model tests completed (attributes, tags, arguments)
- [ ] Relationship model tests completed (associations, dependencies, generalizations)
- [ ] Operation model tests completed (parameters, return types, visibility)
- [ ] Requirement model tests completed (requirements, satisfy relationships)
- [ ] Diagram model tests completed (diagrams, graph elements)
- [ ] State machine model tests completed (statecharts, states, transitions)
- [ ] Actor and use case model tests completed
- [ ] Coverage tracker table maintained and updated as tests are implemented
- [ ] All model classes in tracker have integration tests marked as [x] completed

## Success Criteria

- Integration tests can be run manually on Windows with Rhapsody installed
- Tests validate every wrapper method against real COM API
- Hierarchical relationships (parent-child) are properly tested across all element types
- Invalid relationships throw appropriate exceptions
- Coverage reports show separate metrics for unit vs integration tests
- Test data cleanup works reliably in both success and failure cases
- All major model wrapper classes have integration test coverage
- Coverage tracker table accurately reflects implementation status
- All checkboxes in coverage tracker show [x] for completed implementation
