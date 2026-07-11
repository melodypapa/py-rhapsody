# Package/Class Update Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `update` subcommands to existing `package` and `class` commands, enabling partial attribute modification via JSON input with --path or --guid support.

**Architecture:** Mirrors existing create/view patterns. `PackageUpdateAction` and `ClassUpdateAction` use same validated attributes as create, with partial update behavior. Type validation when using --guid ensures element matches expected metaClass.

**Tech Stack:** Python 3.8+, argparse CLI framework, Rhapsody COM API wrapper, pytest for testing.

## Global Constraints

- Python version: 3.8+
- All code must pass: `ruff check src/ tests/`, `black --check src/ tests/`, `mypy src/ tests/`, `pytest tests/unit -v`
- All tests must pass before commit
- Follow existing action patterns (PackageCreateAction, ClassCreateAction) — see `src/rhapsody_cli/actions/package_action.py` and `src/rhapsody_cli/actions/class_action.py`
- Use existing infrastructure: `PathResolver`, `OutputFormatter`, `ElementManagementAction`, `RhapsodyContext`
- TDD approach: write failing test first, then implementation
- Requirement IDs use existing 5-digit format
- Type validation for --guid: metaClass must match expected type (Package/Class), raise CliExecutionError if mismatch

---

## File Structure

**Modified files:**
- `src/rhapsody_cli/actions/package_action.py` — ADD: `PackageUpdateAction` (6 actions total after this)
- `src/rhapsody_cli/actions/class_action.py` — ADD: `ClassUpdateAction` (6 actions total after this)
- `src/rhapsody_cli/commands/package_command.py` — UPDATE: register update subcommand (5 actions)
- `src/rhapsody_cli/commands/class_command.py` — UPDATE: register update subcommand (6 actions)
- `tests/unit/actions/test_package_action.py` — ADD: `TestPackageUpdateAction` class
- `tests/unit/actions/test_class_action.py` — ADD: `TestClassUpdateAction` class
- `tests/unit/commands/test_package_command.py` — UPDATE: verify 5 subcommands
- `tests/unit/commands/test_class_command.py` — UPDATE: verify 6 subcommands
- `docs/requirements/swr_pkg_requirements.md` — ADD: SWR_PKG_0013
- `docs/requirements/swr_cls_requirements.md` — ADD: SWR_CLS_00014
- `docs/tests/unit/uts_pkg_test-specs.md` — ADD: test specs for update
- `docs/tests/unit/uts_cls_test-specs.md` — ADD: test specs for update
- `docs/user_guide/working_with_packages.rst` — UPDATE: add update subcommand docs
- `docs/user_guide/working_with_classes.rst` — UPDATE: add update subcommand docs

---

## Phase 1: SW Requirements Documentation

### Task 1: Document Package Update Requirement

**Files:**
- Modify: `docs/requirements/swr_pkg_requirements.md`

**Interfaces:**
- Produces: SWR_PKG_0013 (referenced by implementation docstrings and test specs)

- [ ] **Step 1: Add SWR_PKG_0013 to requirements file**

Append to `docs/requirements/swr_pkg_requirements.md` after SWR_PKG_0012:

```markdown
---

## SWR_PKG_0013: Package Update Command

**ID:** SWR_PKG_0013
**Title:** package update command modifies package attributes
**Status:** Planned
**Priority:** High
**Description:**
The package CLI
- SHALL provide a `package update` command to modify attributes of an existing package.
- SHALL accept `--path <package-path>` argument (optional) - full path to package (including name, e.g. Sensors/TempSensors)
- SHALL accept `--guid <guid>` argument (optional) - package GUID
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--input <json-file>` argument (optional) - external JSON file
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL validate path/guid resolves to Package element (metaClass == "Package")
- SHALL validate type when using --guid (metaClass == "Package", raise CliExecutionError if mismatch)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, description, display_name, stereotypes, tags, properties
- SHALL apply name via `setName(val)`, description via `setDescription(val)`, display_name via `setDisplayName(val)`
- SHALL apply stereotypes via `addStereotype(name, "Package")`
- SHALL apply tags and properties via `setPropertyValue(key, val)`
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL log INFO for successful updates
- SHALL log WARNING for skipped attributes
**Implementation:** src/rhapsody_cli/actions/package_action.py:PackageUpdateAction
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_pkg_requirements.md
git commit -m "docs: Add SWR_PKG_0013 Package Update requirement"
```

### Task 2: Document Class Update Requirement

**Files:**
- Modify: `docs/requirements/swr_cls_requirements.md`

**Interfaces:**
- Produces: SWR_CLS_00014 (referenced by implementation docstrings and test specs)

- [ ] **Step 1: Add SWR_CLS_00014 to requirements file**

Append to `docs/requirements/swr_cls_requirements.md` after SWR_CLS_00013:

```markdown
---

## SWR_CLS_00014: Class Update Command

**ID:** SWR_CLS_00014
**Title:** class update command modifies class attributes
**Status:** Planned
**Priority:** High
**Description:**
The class CLI
- SHALL provide a `class update` command to modify attributes of an existing class.
- SHALL accept `--path <class-path>` argument (optional) - full path to class (including name, e.g. Sensors/TemperatureSensor)
- SHALL accept `--guid <guid>` argument (optional) - class GUID
- SHALL require exactly one of `--path` or `--guid`
- SHALL accept `--input <json-file>` argument (optional) - external JSON file
- SHALL accept positional `attributes` argument (inline JSON with fields to update)
- SHALL validate path/guid resolves to Class element (metaClass == "Class")
- SHALL validate type when using --guid (metaClass == "Class", raise CliExecutionError if mismatch)
- SHALL perform partial update - only specified fields are modified
- SHALL support validated attributes: name, description, isAbstract, isFinal, isActive, stereotypes, tags
- SHALL apply name via `setName(val)`, description via `setDescription(val)`
- SHALL apply boolean flags via `setIsAbstract(1/0)`, `setIsFinal(1/0)`, `setIsActive(1/0)`
- SHALL apply stereotypes via `addStereotype(name, "Class")`
- SHALL apply tags via `setPropertyValue(key, val)`
- SHALL skip unknown attributes with warning log
- SHALL detect inline JSON (starts with `{`) vs file path automatically
- SHALL parse JSON file with UTF-8 encoding
- SHALL log INFO for successful updates
- SHALL log WARNING for skipped attributes
**Implementation:** src/rhapsody_cli/actions/class_action.py:ClassUpdateAction
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit requirements**

```bash
git add docs/requirements/swr_cls_requirements.md
git commit -m "docs: Add SWR_CLS_00014 Class Update requirement"
```

---

## Phase 2: PackageUpdateAction

### Task 3: Write PackageUpdateAction Tests

**Files:**
- Create: `tests/unit/actions/test_package_action.py` (add TestPackageUpdateAction class)

**Interfaces:**
- Consumes: `AbstractPackageAction` from `package_action.py`, existing test patterns
- Produces: Test class for TDD verification

- [ ] **Step 1: Add TestPackageUpdateAction class to test file**

Append to `tests/unit/actions/test_package_action.py`:

```python


class TestPackageUpdateAction:
    """Test PackageUpdateAction.

    SWR_PKG_0013: Package Update Command
    """

    def test_update_package_with_path(self) -> None:
        """Test updating package via --path."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated description"}'

            action.execute(args)

            mock_package.setDescription.assert_called_once_with("Updated description")

    def test_update_package_with_guid(self) -> None:
        """Test updating package via --guid with type validation."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(
            action, "_resolve_element_by_guid", return_value=mock_package
        ):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"name":"NewName"}'

            action.execute(args)

            mock_package.setName.assert_called_once_with("NewName")

    def test_update_package_guid_wrong_type(self) -> None:
        """Test that wrong type via --guid raises error."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_element_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"description":"Updated"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "does not resolve to a Package" in str(exc_info.value)
            assert "found Class" in str(exc_info.value)

    def test_update_package_partial_update(self) -> None:
        """Test that partial update only modifies specified fields."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.guid = None
            args.input = None
            args.attributes = '{"tags":{"version":"2.0"}}'

            action.execute(args)

            # Only setPropertyValue called, not setDescription or setName
            mock_package.setPropertyValue.assert_called_once_with("version", "2.0")
            mock_package.setDescription.assert_not_called()
            mock_package.setName.assert_not_called()

    def test_update_package_skips_unknown_fields(self) -> None:
        """Test that unknown fields are skipped with warning."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_package.setDescription.assert_called_once_with("Updated")
                mock_warning.assert_called()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_update_package_from_file(self, tmp_path: Any) -> None:
        """Test updating package from external JSON file."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        json_file = tmp_path / "update.json"
        json_file.write_text('{"description":"From file"}')

        action = PackageUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_resolve_and_validate_package", return_value=mock_package):
            args = MagicMock()
            args.path = "Sensors/TempSensors"
            args.guid = None
            args.input = str(json_file)
            args.attributes = None

            action.execute(args)

            mock_package.setDescription.assert_called_once_with("From file")

    def test_update_package_requires_path_or_guid(self) -> None:
        """Test that update requires either --path or --guid."""
        from rhapsody_cli.actions.package_action import PackageUpdateAction

        action = PackageUpdateAction()

        args = MagicMock()
        args.path = None
        args.guid = None
        args.input = None
        args.attributes = '{"description":"Updated"}'

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid is required" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/unit/actions/test_package_action.py::TestPackageUpdateAction -v
```

Expected: Import errors or test failures (class not yet implemented)

---

### Task 4: Implement PackageUpdateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/package_action.py`

**Interfaces:**
- Consumes: `AbstractPackageAction`, existing patterns from PackageCreateAction
- Produces: `PackageUpdateAction` class with:
  - `VALID_ATTRIBUTES = {"name", "description", "display_name", "stereotypes", "tags", "properties"}`
  - `_load_json_data(args) -> dict`
  - `_set_attributes(package, data)`
  - `execute(args)` — main entry point

- [ ] **Step 1: Add PackageUpdateAction class**

Add to `src/rhapsody_cli/actions/package_action.py` after existing action classes:

```python


class PackageUpdateAction(AbstractPackageAction):
    """Update attributes of an existing package.

    SWR_PKG_0013: Package Update Command
    """

    command_id = "update"
    help_text = "Update attributes of an existing package"
    VALID_ATTRIBUTES = {
        "name",
        "description",
        "display_name",
        "stereotypes",
        "tags",
        "properties",
    }

    def _resolve_element_by_guid(self, guid: str) -> Any:
        """Resolve element by GUID and validate it's a Package."""
        project = self._get_active_root()
        element = project.findElementByGUID(guid)
        if element is None:
            raise CliExecutionError(f"GUID '{guid}' not found")
        meta_class = element.getMetaClass()
        if meta_class != "Package":
            raise CliExecutionError(
                f"GUID '{guid}' does not resolve to a Package (found {meta_class})"
            )
        return element

    def _load_json_data(self, args: Any) -> dict:
        """Load JSON data from inline string or file."""
        if args.input:
            try:
                with open(args.input, encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                raise CliExecutionError(f"File not found: {args.input}")
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}")
        elif args.attributes:
            data_str = args.attributes.strip()
            if data_str.startswith("{"):
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}")
            else:
                # Treat as file path
                try:
                    with open(data_str, encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    raise CliExecutionError(f"File not found: {data_str}")
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}")
        return {}

    def _set_attributes(self, package: Any, data: dict) -> None:
        """Set validated attributes on package (partial update)."""
        for key, value in data.items():
            if key not in self.VALID_ATTRIBUTES:
                self.logger.warning(f"Skipping unknown attribute: {key}")
                continue

            if key == "name":
                package.setName(value)
            elif key == "description":
                package.setDescription(value)
            elif key == "display_name":
                package.setDisplayName(value)
            elif key == "stereotypes":
                for stereotype in value:
                    package.addStereotype(stereotype, "Package")
            elif key == "tags":
                for tag_key, tag_value in value.items():
                    package.setPropertyValue(tag_key, tag_value)
            elif key == "properties":
                for prop_key, prop_value in value.items():
                    package.setPropertyValue(prop_key, prop_value)

    def execute(self, args: Any) -> None:
        """Execute package update."""
        self.logger.info("Starting package update...")

        # Require either path or guid
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid is required")

        # Resolve package
        if args.guid:
            self.logger.info(f"Resolving package by GUID '{args.guid}'...")
            package = self._resolve_element_by_guid(args.guid)
        else:
            self.logger.info(f"Resolving package path '{args.path}'...")
            package = self._resolve_and_validate_package(args.path)

        # Load and apply attributes
        data = self._load_json_data(args)
        self._set_attributes(package, data)

        self.logger.info(f"Successfully updated package: {package.getName()}")
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/unit/actions/test_package_action.py::TestPackageUpdateAction -v
```

Expected: All 7 tests pass

- [ ] **Step 3: Commit implementation**

```bash
git add src/rhapsody_cli/actions/package_action.py tests/unit/actions/test_package_action.py
git commit -m "feat: Add PackageUpdateAction (SWR_PKG_0013)"
```

---

### Task 5: Register Package Update Subcommand

**Files:**
- Modify: `src/rhapsody_cli/commands/package_command.py`
- Modify: `tests/unit/commands/test_package_command.py`

**Interfaces:**
- Consumes: `PackageUpdateAction` from `package_action.py`
- Produces: Updated PackageCommand with 5 registered actions

- [ ] **Step 1: Update PackageCommand imports and get_actions**

Modify `src/rhapsody_cli/commands/package_command.py`:

```python
from rhapsody_cli.actions.package_action import (
    PackageCreateAction,
    PackageDeleteAction,
    PackageListAction,
    PackageUpdateAction,  # ADD
    PackageViewAction,
)


class PackageCommand(AbstractCommand):
    """Package command dispatcher."""

    _PROG_ID = "package"

    def get_actions(self) -> List[AbstractAction]:
        return [
            PackageCreateAction(),
            PackageDeleteAction(),
            PackageViewAction(),
            PackageListAction(),
            PackageUpdateAction(),  # ADD
        ]

    def _setup_subparsers(self) -> None:
        # ... existing setup for create, delete, view, list ...

        # ADD: update subparser
        update_parser = self._subparsers.add_parser(
            "update", help="Update attributes of an existing package"
        )
        update_parser.add_argument(
            "--path", help="Full path to package (including name)"
        )
        update_parser.add_argument("--guid", help="Package GUID")
        update_parser.add_argument("--input", help="External JSON file")
        update_parser.add_argument(
            "attributes",
            nargs="?",
            help="Inline JSON with attributes to update",
        )
        update_parser.set_defaults(action="update")
```

- [ ] **Step 2: Update test to verify 5 subcommands**

Modify `tests/unit/commands/test_package_command.py`:

```python
    def test_registers_all_five_subcommands(self) -> None:
        """UTS_PKG_00025: Test that all 5 subcommands are registered."""
        cmd = PackageCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "update" in command_ids
        assert len(actions) == 5
```

- [ ] **Step 3: Run tests to verify**

```bash
pytest tests/unit/commands/test_package_command.py -v
pytest tests/unit/actions/test_package_action.py::TestPackageUpdateAction -v
```

Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add src/rhapsody_cli/commands/package_command.py tests/unit/commands/test_package_command.py
git commit -m "feat: Register package update subcommand (SWR_PKG_0013)"
```

---

## Phase 3: ClassUpdateAction

### Task 6: Write ClassUpdateAction Tests

**Files:**
- Modify: `tests/unit/actions/test_class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction`, existing test patterns
- Produces: Test class for TDD verification

- [ ] **Step 1: Add TestClassUpdateAction class**

Append to `tests/unit/actions/test_class_action.py`:

```python


class TestClassUpdateAction:
    """Test ClassUpdateAction.

    SWR_CLS_00014: Class Update Command
    """

    def test_update_class_with_path(self) -> None:
        """Test updating class via --path."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated description"}'

            action.execute(args)

            mock_class.setDescription.assert_called_once_with("Updated description")

    def test_update_class_with_guid(self) -> None:
        """Test updating class via --guid with type validation."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_class):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"isAbstract":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)

    def test_update_class_guid_wrong_type(self) -> None:
        """Test that wrong type via --guid raises error."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_package = MagicMock()
        mock_package.getMetaClass.return_value = "Package"

        with patch.object(action, "_resolve_class_by_guid", return_value=mock_package):
            args = MagicMock()
            args.path = None
            args.guid = "12345678-1234-1234-1234-123456789abc"
            args.input = None
            args.attributes = '{"description":"Updated"}'

            with pytest.raises(CliExecutionError) as exc_info:
                action.execute(args)

            assert "does not resolve to a Class" in str(exc_info.value)
            assert "found Package" in str(exc_info.value)

    def test_update_class_partial_update(self) -> None:
        """Test that partial update only modifies specified fields."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.input = None
            args.attributes = '{"isAbstract":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setDescription.assert_not_called()
            mock_class.setName.assert_not_called()

    def test_update_class_boolean_flags(self) -> None:
        """Test updating boolean flags."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.input = None
            args.attributes = '{"isAbstract":true,"isFinal":false,"isActive":true}'

            action.execute(args)

            mock_class.setIsAbstract.assert_called_once_with(1)
            mock_class.setIsFinal.assert_called_once_with(0)
            mock_class.setIsActive.assert_called_once_with(1)

    def test_update_class_skips_unknown_fields(self) -> None:
        """Test that unknown fields are skipped with warning."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()
        mock_class = MagicMock()
        mock_class.getMetaClass.return_value = "Class"

        with patch.object(action, "_resolve_and_validate_class", return_value=mock_class):
            args = MagicMock()
            args.path = "Sensors/TemperatureSensor"
            args.guid = None
            args.input = None
            args.attributes = '{"description":"Updated","unknown_field":"value"}'

            with patch.object(action.logger, "warning") as mock_warning:
                action.execute(args)

                mock_class.setDescription.assert_called_once_with("Updated")
                mock_warning.assert_called()
                assert "unknown_field" in str(mock_warning.call_args)

    def test_update_class_requires_path_or_guid(self) -> None:
        """Test that update requires either --path or --guid."""
        from rhapsody_cli.actions.class_action import ClassUpdateAction

        action = ClassUpdateAction()

        args = MagicMock()
        args.path = None
        args.guid = None
        args.input = None
        args.attributes = '{"description":"Updated"}'

        with pytest.raises(CliExecutionError) as exc_info:
            action.execute(args)

        assert "Either --path or --guid is required" in str(exc_info.value)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/unit/actions/test_class_action.py::TestClassUpdateAction -v
```

Expected: Import errors or test failures (class not yet implemented)

---

### Task 7: Implement ClassUpdateAction

**Files:**
- Modify: `src/rhapsody_cli/actions/class_action.py`

**Interfaces:**
- Consumes: `AbstractClassAction`, existing patterns from ClassCreateAction
- Produces: `ClassUpdateAction` class with:
  - `VALID_ATTRIBUTES = {"name", "description", "isAbstract", "isFinal", "isActive", "stereotypes", "tags"}`
  - `_load_json_data(args) -> dict`
  - `_set_attributes(classifier, data)`
  - `execute(args)` — main entry point

- [ ] **Step 1: Add ClassUpdateAction class**

Add to `src/rhapsody_cli/actions/class_action.py` after ClassLinkAction:

```python


class ClassUpdateAction(AbstractClassAction):
    """Update attributes of an existing class.

    SWR_CLS_00014: Class Update Command
    """

    command_id = "update"
    help_text = "Update attributes of an existing class"
    VALID_ATTRIBUTES = {
        "name",
        "description",
        "isAbstract",
        "isFinal",
        "isActive",
        "stereotypes",
        "tags",
    }

    def _load_json_data(self, args: Any) -> dict:
        """Load JSON data from inline string or file."""
        if args.input:
            try:
                with open(args.input, encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                raise CliExecutionError(f"File not found: {args.input}")
            except json.JSONDecodeError as e:
                raise CliExecutionError(f"Invalid JSON: {e}")
        elif args.attributes:
            data_str = args.attributes.strip()
            if data_str.startswith("{"):
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}")
            else:
                # Treat as file path
                try:
                    with open(data_str, encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    raise CliExecutionError(f"File not found: {data_str}")
                except json.JSONDecodeError as e:
                    raise CliExecutionError(f"Invalid JSON: {e}")
        return {}

    def _set_attributes(self, classifier: Any, data: dict) -> None:
        """Set validated attributes on class (partial update)."""
        for key, value in data.items():
            if key not in self.VALID_ATTRIBUTES:
                self.logger.warning(f"Skipping unknown attribute: {key}")
                continue

            if key == "name":
                classifier.setName(value)
            elif key == "description":
                classifier.setDescription(value)
            elif key == "isAbstract":
                classifier.setIsAbstract(1 if value else 0)
            elif key == "isFinal":
                classifier.setIsFinal(1 if value else 0)
            elif key == "isActive":
                classifier.setIsActive(1 if value else 0)
            elif key == "stereotypes":
                for stereotype in value:
                    classifier.addStereotype(stereotype, "Class")
            elif key == "tags":
                for tag_key, tag_value in value.items():
                    classifier.setPropertyValue(tag_key, tag_value)

    def execute(self, args: Any) -> None:
        """Execute class update."""
        self.logger.info("Starting class update...")

        # Require either path or guid
        if not args.path and not args.guid:
            raise CliExecutionError("Either --path or --guid is required")

        # Resolve class
        if args.guid:
            self.logger.info(f"Resolving class by GUID '{args.guid}'...")
            classifier = self._resolve_class_by_guid(args.guid)
        else:
            self.logger.info(f"Resolving class path '{args.path}'...")
            classifier = self._resolve_and_validate_class(args.path)

        # Load and apply attributes
        data = self._load_json_data(args)
        self._set_attributes(classifier, data)

        self.logger.info(f"Successfully updated class: {classifier.getName()}")
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/unit/actions/test_class_action.py::TestClassUpdateAction -v
```

Expected: All 8 tests pass

- [ ] **Step 3: Commit implementation**

```bash
git add src/rhapsody_cli/actions/class_action.py tests/unit/actions/test_class_action.py
git commit -m "feat: Add ClassUpdateAction (SWR_CLS_00014)"
```

---

### Task 8: Register Class Update Subcommand

**Files:**
- Modify: `src/rhapsody_cli/commands/class_command.py`
- Modify: `tests/unit/commands/test_class_command.py`

**Interfaces:**
- Consumes: `ClassUpdateAction` from `class_action.py`
- Produces: Updated ClassCommand with 6 registered actions

- [ ] **Step 1: Update ClassCommand imports and get_actions**

Modify `src/rhapsody_cli/commands/class_command.py`:

```python
from rhapsody_cli.actions.class_action import (
    ClassCreateAction,
    ClassDeleteAction,
    ClassLinkAction,
    ClassListAction,
    ClassUpdateAction,  # ADD
    ClassViewAction,
)


class ClassCommand(AbstractCommand):
    """Class command dispatcher."""

    _PROG_ID = "class"

    def get_actions(self) -> List[AbstractAction]:
        return [
            ClassCreateAction(),
            ClassDeleteAction(),
            ClassViewAction(),
            ClassListAction(),
            ClassLinkAction(),
            ClassUpdateAction(),  # ADD
        ]

    def _setup_subparsers(self) -> None:
        # ... existing setup for create, delete, view, list, link ...

        # ADD: update subparser
        update_parser = self._subparsers.add_parser(
            "update", help="Update attributes of an existing class"
        )
        update_parser.add_argument(
            "--path", help="Full path to class (including name)"
        )
        update_parser.add_argument("--guid", help="Class GUID")
        update_parser.add_argument("--input", help="External JSON file")
        update_parser.add_argument(
            "attributes",
            nargs="?",
            help="Inline JSON with attributes to update",
        )
        update_parser.set_defaults(action="update")
```

- [ ] **Step 2: Update test to verify 6 subcommands**

Modify `tests/unit/commands/test_class_command.py`:

```python
    def test_registers_all_six_subcommands(self) -> None:
        """UTS_CLS_00029: Test that all 6 subcommands are registered."""
        cmd = ClassCommand(["create", "--path", "Sensors", '{"name":"Test"}'])
        actions = cmd.get_actions()
        command_ids = [a.command_id for a in actions]

        assert "create" in command_ids
        assert "delete" in command_ids
        assert "view" in command_ids
        assert "list" in command_ids
        assert "link" in command_ids
        assert "update" in command_ids
        assert len(actions) == 6
```

- [ ] **Step 3: Run tests to verify**

```bash
pytest tests/unit/commands/test_class_command.py -v
pytest tests/unit/actions/test_class_action.py::TestClassUpdateAction -v
```

Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add src/rhapsody_cli/commands/class_command.py tests/unit/commands/test_class_command.py
git commit -m "feat: Register class update subcommand (SWR_CLS_00014)"
```

---

## Phase 4: Test Specs Documentation

### Task 9: Add Package Update Test Specs

**Files:**
- Modify: `docs/tests/unit/uts_pkg_test-specs.md`

**Interfaces:**
- Produces: UTS_PKG_000xx test specs for PackageUpdateAction

- [ ] **Step 1: Add test specs for package update**

Append to `docs/tests/unit/uts_pkg_test-specs.md`:

```markdown
---

## UTS_PKG_00026: Update package via path

**ID:** UTS_PKG_00026
**Traces-To:** SWR_PKG_0013
**Title:** Update package via path
**Type:** Unit
**Priority:** High
**Description:**
Test that package can be updated via --path argument.
**Pre-conditions:**
- Package exists at specified path
- Valid JSON provided
**Test Steps:**
1. Call PackageUpdateAction with --path
2. Verify attributes updated
**Expected Result:**
Package updated successfully.
**Verification Criteria:**
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_PKG_00027: Update package via GUID with type validation

**ID:** UTS_PKG_00027
**Traces-To:** SWR_PKG_0013
**Title:** Update package via GUID with type validation
**Type:** Unit
**Priority:** High
**Description:**
Test that package can be updated via --guid with type validation.
**Pre-conditions:**
- Package exists with given GUID
**Test Steps:**
1. Call PackageUpdateAction with --guid
2. Verify metaClass validation
3. Verify attributes updated
**Expected Result:**
Package updated, type validated.
**Verification Criteria:**
- findElementByGUID called
- metaClass checked equals "Package"
- setName called with correct value
**Last Changed:** 2026-07-10

---

## UTS_PKG_00028: Update package GUID wrong type raises error

**ID:** UTS_PKG_00028
**Traces-To:** SWR_PKG_0013
**Title:** Update package GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong element type via --guid raises CliExecutionError.
**Pre-conditions:**
- GUID resolves to non-package element (Class)
**Test Steps:**
1. Call PackageUpdateAction with --guid for Class
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError with type mismatch message.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to a Package"
- Error contains "found Class"
**Last Changed:** 2026-07-10

---

## UTS_PKG_00029: Update package partial update

**ID:** UTS_PKG_00029
**Traces-To:** SWR_PKG_0013
**Title:** Update package partial update
**Type:** Unit
**Priority:** High
**Description:**
Test that partial update only modifies specified fields.
**Pre-conditions:**
- Package exists
**Test Steps:**
1. Call PackageUpdateAction with only tags field
2. Verify only setPropertyValue called
3. Verify other setters not called
**Expected Result:**
Only specified field updated.
**Verification Criteria:**
- setPropertyValue called for tags
- setDescription not called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_PKG_00030: Update package skips unknown fields

**ID:** UTS_PKG_00030
**Traces-To:** SWR_PKG_0013
**Title:** Update package skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown fields are skipped with warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call PackageUpdateAction with unknown field
2. Verify warning logged
3. Verify known field still applied
**Expected Result:**
Unknown fields skipped, known fields applied.
**Verification Criteria:**
- Logger.warning called with unknown field name
- Known attribute still applied
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit test specs**

```bash
git add docs/tests/unit/uts_pkg_test-specs.md
git commit -m "docs: Add unit test specs for package update (UTS_PKG_00026-00030)"
```

### Task 10: Add Class Update Test Specs

**Files:**
- Modify: `docs/tests/unit/uts_cls_test-specs.md`

**Interfaces:**
- Produces: UTS_CLS_000xx test specs for ClassUpdateAction

- [ ] **Step 1: Add test specs for class update**

Append to `docs/tests/unit/uts_cls_test-specs.md` after existing specs:

```markdown
---

## UTS_CLS_00030: Update class via path

**ID:** UTS_CLS_00030
**Traces-To:** SWR_CLS_00014
**Title:** Update class via path
**Type:** Unit
**Priority:** High
**Description:**
Test that class can be updated via --path argument.
**Pre-conditions:**
- Class exists at specified path
- Valid JSON provided
**Test Steps:**
1. Call ClassUpdateAction with --path
2. Verify attributes updated
**Expected Result:**
Class updated successfully.
**Verification Criteria:**
- setDescription called with correct value
- Logger shows INFO message
**Last Changed:** 2026-07-10

---

## UTS_CLS_00031: Update class via GUID with type validation

**ID:** UTS_CLS_00031
**Traces-To:** SWR_CLS_00014
**Title:** Update class via GUID with type validation
**Type:** Unit
**Priority:** High
**Description:**
Test that class can be updated via --guid with type validation.
**Pre-conditions:**
- Class exists with given GUID
**Test Steps:**
1. Call ClassUpdateAction with --guid
2. Verify metaClass validation
3. Verify attributes updated
**Expected Result:**
Class updated, type validated.
**Verification Criteria:**
- findElementByGUID called
- metaClass checked equals "Class"
- setIsAbstract called with correct value
**Last Changed:** 2026-07-10

---

## UTS_CLS_00032: Update class GUID wrong type raises error

**ID:** UTS_CLS_00032
**Traces-To:** SWR_CLS_00014
**Title:** Update class GUID wrong type raises error
**Type:** Unit
**Priority:** High
**Description:**
Test that wrong element type via --guid raises CliExecutionError.
**Pre-conditions:**
- GUID resolves to non-class element (Package)
**Test Steps:**
1. Call ClassUpdateAction with --guid for Package
2. Verify CliExecutionError raised
**Expected Result:**
CliExecutionError with type mismatch message.
**Verification Criteria:**
- CliExecutionError raised
- Error contains "does not resolve to a Class"
- Error contains "found Package"
**Last Changed:** 2026-07-10

---

## UTS_CLS_00033: Update class boolean flags

**ID:** UTS_CLS_00033
**Traces-To:** SWR_CLS_00014
**Title:** Update class boolean flags
**Type:** Unit
**Priority:** High
**Description:**
Test updating boolean flags isAbstract, isFinal, isActive.
**Pre-conditions:**
- Class exists
**Test Steps:**
1. Call ClassUpdateAction with boolean flags
2. Verify setIsAbstract, setIsFinal, setIsActive called
**Expected Result:**
Boolean flags updated correctly.
**Verification Criteria:**
- setIsAbstract(1) called for true
- setIsFinal(0) called for false
- setIsActive(1) called for true
**Last Changed:** 2026-07-10

---

## UTS_CLS_00034: Update class partial update

**ID:** UTS_CLS_00034
**Traces-To:** SWR_CLS_00014
**Title:** Update class partial update
**Type:** Unit
**Priority:** High
**Description:**
Test that partial update only modifies specified fields.
**Pre-conditions:**
- Class exists
**Test Steps:**
1. Call ClassUpdateAction with only isAbstract field
2. Verify only setIsAbstract called
3. Verify other setters not called
**Expected Result:**
Only specified field updated.
**Verification Criteria:**
- setIsAbstract called
- setDescription not called
- setName not called
**Last Changed:** 2026-07-10

---

## UTS_CLS_00035: Update class skips unknown fields

**ID:** UTS_CLS_00035
**Traces-To:** SWR_CLS_00014
**Title:** Update class skips unknown fields
**Type:** Unit
**Priority:** Medium
**Description:**
Test that unknown fields are skipped with warning.
**Pre-conditions:**
- JSON contains unknown fields
**Test Steps:**
1. Call ClassUpdateAction with unknown field
2. Verify warning logged
3. Verify known field still applied
**Expected Result:**
Unknown fields skipped, known fields applied.
**Verification Criteria:**
- Logger.warning called with unknown field name
- Known attribute still applied
**Last Changed:** 2026-07-10
```

- [ ] **Step 2: Commit test specs**

```bash
git add docs/tests/unit/uts_cls_test-specs.md
git commit -m "docs: Add unit test specs for class update (UTS_CLS_00030-00035)"
```

---

## Phase 5: User Guide Documentation

### Task 11: Update Package User Guide

**Files:**
- Modify: `docs/user_guide/working_with_packages.rst`

**Interfaces:**
- Produces: Updated user guide with update subcommand documentation

- [ ] **Step 1: Add update subcommand documentation**

Add to `docs/user_guide/working_with_packages.rst` after the list section:

```rst
Updating Packages
-----------------

The ``package update`` command modifies attributes of an existing package.

**Usage:**

.. code-block:: bash

   rhapsody-cli package update --path <package-path> [attributes]
   rhapsody-cli package update --guid <guid> [attributes]

**Arguments:**

- ``--path <package-path>`` - Full path to package (including name)
- ``--guid <guid>`` - Package GUID (alternative to --path)
- ``--input <json-file>`` - External JSON file
- ``attributes`` - Inline JSON with fields to update (optional)

**JSON Fields:**

- ``name`` - Package name
- ``description`` - Package description
- ``display_name`` - Display name
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Object with tag key-value pairs
- ``properties`` - Object with property key-value pairs

**Examples:**

.. code-block:: bash

   # Update description via path
   rhapsody-cli package update --path Sensors/TempSensors '{"description":"Updated description"}'

   # Update tags via GUID
   rhapsody-cli package update --guid 12345678-1234-1234-1234-123456789abc '{"tags":{"version":"2.0"}}'

   # Update from file
   rhapsody-cli package update --path Sensors/TempSensors --input update.json

**Partial Update:**

Only specified fields are modified. Unknown fields are skipped with a warning.
```

- [ ] **Step 2: Commit user guide**

```bash
git add docs/user_guide/working_with_packages.rst
git commit -m "docs: Add package update subcommand to user guide"
```

### Task 12: Update Class User Guide

**Files:**
- Modify: `docs/user_guide/working_with_classes.rst`

**Interfaces:**
- Produces: Updated user guide with update subcommand documentation

- [ ] **Step 1: Add update subcommand documentation**

Add to `docs/user_guide/working_with_classes.rst` after the link section:

```rst
Updating Classes
----------------

The ``class update`` command modifies attributes of an existing class.

**Usage:**

.. code-block:: bash

   rhapsody-cli class update --path <class-path> [attributes]
   rhapsody-cli class update --guid <guid> [attributes]

**Arguments:**

- ``--path <class-path>`` - Full path to class (including name)
- ``--guid <guid>`` - Class GUID (alternative to --path)
- ``--input <json-file>`` - External JSON file
- ``attributes`` - Inline JSON with fields to update (optional)

**JSON Fields:**

- ``name`` - Class name
- ``description`` - Class description
- ``isAbstract`` - Boolean flag for abstract class
- ``isFinal`` - Boolean flag for final class
- ``isActive`` - Boolean flag for active class
- ``stereotypes`` - Array of stereotype names
- ``tags`` - Object with tag key-value pairs

**Examples:**

.. code-block:: bash

   # Update description via path
   rhapsody-cli class update --path Sensors/TemperatureSensor '{"description":"Updated description"}'

   # Set abstract flag via GUID
   rhapsody-cli class update --guid 12345678-1234-1234-1234-123456789abc '{"isAbstract":true}'

   # Update multiple fields
   rhapsody-cli class update --path Sensors/TemperatureSensor '{"isAbstract":true,"isFinal":false}'

**Partial Update:**

Only specified fields are modified. Unknown fields are skipped with a warning.

**Note:** For modifying operations, attributes, or superclasses, use the dedicated operation, attribute, and link commands.
```

- [ ] **Step 2: Commit user guide**

```bash
git add docs/user_guide/working_with_classes.rst
git commit -m "docs: Add class update subcommand to user guide"
```

---

## Phase 6: Final Verification

### Task 13: Run Full Test Suite and Quality Gates

**Files:**
- All modified files

**Interfaces:**
- Consumes: All implemented code
- Produces: Verified working state

- [ ] **Step 1: Run full test suite**

```bash
pytest tests/unit -v
```

Expected: All tests pass (including new PackageUpdateAction and ClassUpdateAction tests)

- [ ] **Step 2: Run ruff check**

```bash
ruff check src/ tests/
```

Expected: No errors

- [ ] **Step 3: Run black check**

```bash
black --check src/ tests/
```

Expected: No formatting issues

- [ ] **Step 4: Run mypy**

```bash
mypy src/
```

Expected: No type errors in modified files (may have pre-existing issues in other files)

- [ ] **Step 5: Verify CLI help**

```bash
python -m rhapsody_cli.cli --help
python -m rhapsody_cli.cli package --help
python -m rhapsody_cli.cli class --help
```

Expected: Help text shows update subcommands for package and class

- [ ] **Step 6: Final commit if needed**

If any files were modified during verification:

```bash
git add -A
git commit -m "chore: Final cleanup for package/class update commands"
```

---

## Summary

**Completed:**
- Package update command (SWR_PKG_0013): 5 subcommands total
- Class update command (SWR_CLS_00014): 6 subcommands total
- Tests passing: PackageUpdateAction (7 tests), ClassUpdateAction (8 tests)
- Quality gates: ruff, black, pytest
- Documentation: Requirements, test specs, user guides

**Next Plan:** Operation and Attribute Commands (Plan 2)
**Final Plan:** Port Command + Element Command Removal (Plan 3)