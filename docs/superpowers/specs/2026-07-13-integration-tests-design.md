# Integration Tests Design for rhapsody-cli

**Date:** 2026-07-13
**Author:** Designed via brainstorming session
**Status:** Approved

## Overview

This design adds comprehensive integration tests to the rhapsody-cli project that verify model classes work correctly with a real Rhapsody application. Integration tests complement existing mocked unit tests by validating actual COM API interactions and end-to-end workflows.

### Key Requirements

- Validate wrapper methods correctly call the real Rhapsody COM API
- Test end-to-end workflows with live Rhapsody instances
- Execute manually by developers on Windows with Rhapsody installed
- Maintain separate coverage metrics from unit tests
- Use temporary test projects that are cleaned up after test runs

## Architecture

### Directory Structure

Integration tests mirror the unit test structure under `tests/integration/models/`:

```
tests/
├── unit/
│   └── models/
│       ├── test_core.py
│       ├── elements/
│       │   ├── test_classifiers.py
│       │   ├── test_containment.py
│       │   └── ...
│       └── fakes.py
└── integration/
    ├── conftest.py
    └── models/
        ├── test_core.py
        └── elements/
            ├── test_classifiers.py
            ├── test_containment.py
            └── ...
```

### Components

- **`tests/integration/conftest.py`** — Pytest fixtures for Rhapsody lifecycle management
- **Mirrored test modules** — Integration test modules matching unit test structure
- **`demos/test_project/`** — Temporary test project directory (gitignored)
- **Separate coverage configuration** — Distinct coverage artifacts from unit tests

## Test Fixtures and Session Management

### Fixture Architecture (tests/integration/conftest.py)

#### `rhapsody_app` — Session-scoped application fixture

- Connects to Rhapsody via `RhapsodyApplication.connect(prefer_attach=True)`
- Yields the application instance for all tests
- Closes connection in finalizer (even if tests fail)
- Skips gracefully if Rhapsody is unavailable

#### `test_project` — Session-scoped project fixture

- Depends on `rhapsody_app` fixture
- Cleans up `demos/test_project/` before creating new project
- Creates new RPProject at `demos/test_project/TestProject.rpy`
- Yields project instance for tests to use
- Optionally cleans up after session based on behavior/flag

#### `skip_if_no_rhapsody` — Autouse detection fixture

- Detects if Rhapsody is unavailable (not installed, no license, etc.)
- Skips all integration tests gracefully with clear message
- Runs before app/project fixtures

### Coverage Separation

- Integration tests use separate `.coveragerc` or pytest config
- Unit and integration coverage never mix in reports
- Can run `pytest tests/unit/` vs `pytest tests/integration/` with distinct coverage artifacts

## Test Structure and Organization

### Directory Mirroring

Integration tests mirror the unit test directory structure:

- `tests/unit/models/test_core.py` → `tests/integration/models/test_core.py`
- `tests/unit/models/elements/test_classifiers.py` → `tests/integration/models/elements/test_classifiers.py`
- And so forth for all model wrapper classes

### Test Class Patterns

Each integration test class mirrors its unit test counterpart:

```python
class TestRPProjectIntegration:
    def test_get_name(self, test_project):
        """Validate get_name() returns actual project name."""
        pass

    def test_get_nested_elements(self, test_project):
        """Validate element retrieval with real COM objects."""
        pass

    def test_create_element_workflow(self, test_project):
        """End-to-end workflow: create class, add to package."""
        pass
```

### Test Method Patterns

- Tests use `rhapsody_app` and `test_project` fixtures
- Each test validates a specific wrapper method against real COM API
- Tests include both success and failure paths
- Workflow tests validate end-to-end user scenarios

### Separation of Concerns

- **Unit tests:** Mocked COM objects, test wrapper logic in isolation
- **Integration tests:** Real COM API, verify actual Rhapsody behavior
- **No duplication:** Each test suite has distinct purpose and validation strategy

## Implementation Details

### Test Project Creation and Element Building

- Tests use the `test_project` fixture to create elements for validation
- Helper methods in test classes for common element creation patterns
- Tests create packages, classes, diagrams, etc., as needed for validation
- Each test is responsible for setting up its own elements (not shared between tests)

### Error Handling and Validation

- Integration tests catch `RhapsodyRuntimeException` from COM failures
- Validate that error messages and exceptions match expected behavior
- Test both success and failure paths for wrapper methods
- Verify that wrapper methods translate COM errors appropriately

### Test Execution

```bash
# Run only unit tests (fast, no Rhapsody needed)
pytest tests/unit/

# Run only integration tests (requires Rhapsody on Windows)
pytest tests/integration/

# Run with coverage for integration tests only
pytest tests/integration/ --cov=rhapsody_cli --cov-report=html
```

### Git Ignore Entry

```
demos/test_project/
```

## Coverage and Reporting

### Coverage Separation Strategy

- **Unit tests:** `tests/unit/` → coverage for wrapper logic with mocked COM
- **Integration tests:** `tests/integration/` → coverage for real COM integration
- Separate coverage configurations via pytest markers or different `.coveragerc` files

### Pytest Configuration

```ini
[tool.pytest.ini_options]
markers = [
    "integration: marks tests as integration tests (require Rhapsody)",
    "unit: marks tests as unit tests (mocked COM)"
]
```

### Running Tests by Type

```bash
# Unit tests only (CI environment)
pytest -m unit

# Integration tests only (local development with Rhapsody)
pytest -m integration

# Integration tests with coverage
pytest -m integration --cov=rhapsody_cli --cov-report=html
```

### CI Configuration

- GitHub Actions continues running only `pytest tests/unit/`
- Integration tests remain manual execution only
- CI coverage reports reflect unit test coverage exclusively

## Test Data Management

### Pre-test Cleanup

- `test_project` fixture cleans `demos/test_project/` before creating new project
- Ensures each test run starts with a clean slate
- No artifacts from previous runs interfere with current tests

### Post-test Cleanup Strategy

- **Default behavior:** Clean up `demos/test_project/` after successful test run
- **Debug mode:** Leave artifacts for inspection if tests fail
- Controlled via `--keep-test-artifacts` pytest flag or `RHAPSODY_KEEP_ARTIFACTS=1` environment variable

### Element Creation Helpers

- Test classes include helper methods for common element creation
- Example: `create_test_class(name, parent_package)` in test classes
- Reduces duplication across tests and ensures consistent test data

### Hierarchical Relationship Testing

- **Mixed approach:** Fixtures provide basic project/package structure, tests create specific hierarchical elements they need
- **Parent-child validation:** Tests verify operations are members of classes, models are under packages, etc.
- **Exception handling:** Invalid hierarchical relationships throw Rhapsody exceptions that tests validate are properly translated
- **Helper methods:** Test classes include helpers like `create_class_with_operations(parent_package, operation_names)` to build hierarchies

### Test Isolation

- Each test creates its own elements within the shared project
- Tests don't depend on elements created by other tests
- Tests clean up their own elements if needed (or leave them for post-run cleanup)

## Test Scope

### Comprehensive Coverage

Integration tests will validate **every wrapper method** in every model class:
- Every method in `RPModelElement` and all its subclasses
- Comprehensive validation of COM API interactions
- Both success and failure paths for each method

### Manual Test Writing

- Each integration test is written manually to match unit test structure
- Tests are organized by model class and method
- Maintains consistency with unit test organization

### Validation Strategy

- **COM API Validation:** Ensure wrapper methods correctly call Rhapsody COM API
- **Workflow Testing:** Validate end-to-end user scenarios
- **Error Handling:** Verify exception translation and error messages
- **Return Types:** Ensure methods return correct wrapper types

## Implementation Plan

### Phase 1: Infrastructure Setup

1. Create `tests/integration/` directory structure
2. Set up `tests/integration/conftest.py` with fixtures
3. Add `demos/test_project/` to `.gitignore`
4. Configure pytest markers and coverage separation

### Phase 2: Core Model Integration Tests

1. Implement `tests/integration/models/test_core.py`
2. Create tests for `RPModelElement` base class methods
3. Create tests for `RPCollection` wrapper
4. Create tests for `RPUnit` wrapper

### Phase 3: Element Wrapper Integration Tests

1. Implement `tests/integration/models/elements/` tests
2. Create tests for containment elements (`RPPackage`, `RPProject`)
3. Create tests for classifiers (`RPClass`, `RPActor`)
4. Create tests for relations, diagrams, requirements, variables

### Phase 4: Workflow and End-to-End Tests

1. Add workflow tests for common user scenarios
2. Add tests for complex multi-step operations
3. Add tests for error handling and edge cases

### Phase 5: Documentation and Validation

1. Update documentation with integration test instructions
2. Verify coverage separation works correctly
3. Validate tests run correctly on Windows with Rhapsody

## Success Criteria

- Integration tests run successfully on Windows with Rhapsody installed
- Integration tests are skipped gracefully on non-Windows or without Rhapsody
- Coverage reports show separate metrics for unit and integration tests
- All wrapper methods have corresponding integration tests
- Tests validate both COM API interactions and end-to-end workflows
- Test data cleanup works reliably in both success and failure cases

## Notes

- Integration tests are for manual execution only by developers
- CI continues to run only unit tests (mocked COM, no Rhapsody required)
- Integration tests validate actual Rhapsody behavior beyond mocked unit tests
- Temporary test projects ensure clean test data for each run
