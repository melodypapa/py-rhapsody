# Variables Subpackage Integration Tests Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add integration tests for all remaining untested methods of `RPVariable`, `RPAttribute` (complete partial coverage), `RPTag`, `RPArgument`. Flip in-source `[ ] integration test` markers to `[x]` as work completes.

**Architecture:** Extends `tests/integration/models/elements/variables/test_model_attribute.py` for `RPAttribute`/`RPVariable`; creates new test files for `RPTag` (`test_model_tag.py`) and `RPArgument` (`test_model_argument.py`).

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid.uuid4().hex[:8]`.

## Scope Analysis (from source inspection)

`src/rhapsody_cli/models/elements/variables/model_variables.py` defines 33 total checklist rows across 4 classes:

| Class | Total rows | Already `[x] integration test` | Remaining (this plan) |
|-------|-----------:|--------------------------------:|-----------------------:|
| `RPVariable` (base) | 10 | 2 (`get_default_value`, `set_default_value`) | 8 |
| `RPAttribute` | 12 | 0 | 12 |
| `RPTag` | 9 | 0 | 9 |
| `RPArgument` | 2 | 0 | 2 |
| **Total** | **33** | **2** | **31** |

Existing `tests/integration/models/elements/variables/test_model_attribute.py` covers:
- `add_attribute`/`get_attributes` (these belong to `RPClass`, out of scope here — do not re-flip)
- `set_type_declaration`/`get_declaration` — present as an `xfail` test (`test_attribute_type_roundtrip`), because `Rhapsody2.Application.1` does not persist `typeDeclaration` (silent no-op). This row remains `[ ]` in-source; this plan does **not** flip it, but adds new coverage for the *working* declaration path (`set_declaration`/`get_declaration` directly, without going through `set_type_declaration`).
- `set_default_value`/`get_default_value` — passing, already flipped `[x]`.

**Untested method list (31, exactly matching remaining `[ ]` markers in source):**

- `RPVariable`: `add_element_default_value`, `add_string_default_value`, `get_declaration`, `get_type`, `get_value_specifications`, `set_declaration`, `set_type`, `set_type_declaration`
- `RPAttribute`: `get_is_constant`, `get_is_ordered`, `get_is_reference`, `get_is_static`, `get_multiplicity`, `get_visibility`, `set_is_constant`, `set_is_ordered`, `set_is_reference`, `set_is_static`, `set_multiplicity`, `set_visibility`
- `RPTag`: `get_base`, `get_from_profile`, `get_multiplicity`, `get_tag_meta_class`, `get_value`, `set_multiplicity`, `set_tag_context_value` (inherited from `RPModelElement`, but tracked as an `RPTag` row in this file), `set_tag_meta_class`, `set_value`
- `RPArgument`: `get_argument_direction`, `set_argument_direction`

## Creation Chains Discovered

- **`RPAttribute`**: `RPClass.add_attribute(name) -> RPAttribute` (already used in existing tests).
- **`RPArgument`**: `RPClass.add_operation(name) -> RPOperation` (subclass of `RPInterfaceItem`), then `RPOperation.add_argument(name) -> RPArgument` (`src/rhapsody_cli/models/elements/classifiers/model_interface_item.py:30`).
- **`RPTag`**: no dedicated factory method exists on `model_variables.py`. The established chain (via `RPModelElement` in `core.py`) is:
  1. `element.add_property(property_key, property_type, property_value)` (`core.py:383`) — creates a new property/tag on the element.
  2. `element.get_tag(name) -> RPModelElement` (`core.py:1281`), which the wrapper factory (`AbstractRPModelElement.wrap`) resolves to `RPTag` when the underlying COM object's meta-type is `Tag` (see `register_wrapper("Tag", RPTag)` at `model_variables.py:424`).
  - Use `test_class.add_property(tag_name, "String", "initial")` then `tag = test_class.get_tag(tag_name)`; assert `isinstance(tag, RPTag)`.
  - If this chain does not yield a real `IRPTag` COM object in the live environment (e.g. returns a generic property object instead), fall back to `xfail` with a clear reason, following the established pattern in `test_model_attribute.py` and `test_model_operation.py`.

## Global Constraints

- Windows-only runtime (requires Windows + a running Rhapsody instance)
- All test classes use `@pytest.mark.integration`
- All tests consume the `test_project: RPProject` fixture
- Use `_unique(prefix)` with `uuid.uuid4().hex[:8]`
- Always `try/finally` cleanup via `element.delete_from_project()` (delete the top-level owning class, not the sub-element, unless the sub-element supports its own `delete_from_project()`)
- Assert both `isinstance()` and read-back values
- Flip `[ ] integration test` to `[x]` per task in `model_variables.py` — only for rows actually covered by a **passing** (non-`xfail`) test
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- Import via subpackage `__init__.py` re-exports (`from rhapsody_cli.models.elements.variables import RPAttribute, RPTag, RPArgument`)

---

## Tasks

### Task 1: `RPVariable` — type management (`get_type`/`set_type`, `get_declaration`/`set_declaration`, `set_type_declaration`)

**Files:**
- Modify: `tests/integration/models/elements/variables/test_model_attribute.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_type`, `set_type`, `get_declaration`, `set_declaration`, `set_type_declaration`

- [ ] **Step 1: Write the new integration tests**

```python
def test_attribute_type_via_existing_classifier(self, test_project: RPProject) -> None:
    pkg_name = self._unique("TypeRefPkg")
    class_name = self._unique("TypeRefCls")
    type_class_name = self._unique("TypeRefType")
    attr_name = self._unique("typedAttr2")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    type_class = pkg.add_class(type_class_name)
    try:
        attr = test_class.add_attribute(attr_name)
        attr.set_type(type_class)
        resolved_type = attr.get_type()
        assert resolved_type is not None
        assert resolved_type.get_name() == type_class_name
    finally:
        test_class.delete_from_project()
        type_class.delete_from_project()
```

For remaining methods, follow the same pattern:
- `test_attribute_declaration_direct_set` — **implemented** in `tests/integration/models/elements/variables/test_model_attribute.py` (see `docs/superpowers/plans/2026-07-15-fix-operation-setter-and-attribute-declaration-tests.md`). Confirmed the direct `set_declaration`/`get_declaration` path works independently of the known `set_type_declaration` type-reuse behavior.
- `test_attribute_set_type_declaration_reuses_existing_type` — mark `@pytest.mark.xfail` with the same reason string already used in `test_attribute_type_roundtrip` (do not duplicate the existing xfail test; only add this if there is a distinct scenario, e.g. verifying `set_type_declaration` reuses a matching existing type by name — otherwise skip and rely on the existing xfail test to represent this row).

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_attribute.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `get_type`, `set_type`, `get_declaration`, `set_declaration` to `[x] integration test`. Leave `set_type_declaration` as `[ ]` if it remains xfailed (unresolved COM quirk); document this explicitly in a code comment if left unflipped.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_attribute.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPVariable type management"
```

---

### Task 2: `RPVariable` — default value specifications

**Files:**
- Modify: `tests/integration/models/elements/variables/test_model_attribute.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `add_element_default_value`, `add_string_default_value`, `get_value_specifications`

- [ ] **Step 1: Write the new integration tests**

```python
def test_add_string_default_value_and_read_specifications(self, test_project: RPProject) -> None:
    pkg_name = self._unique("MultiDefPkg")
    class_name = self._unique("MultiDefCls")
    attr_name = self._unique("multiAttr")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        attr = test_class.add_attribute(attr_name)
        attr.set_multiplicity("0..*")
        spec = attr.add_string_default_value("firstValue")
        assert spec is not None
        specs = list(attr.get_value_specifications())
        assert len(specs) >= 1
    finally:
        test_class.delete_from_project()
```

For remaining methods, follow the same pattern:
- `test_add_element_default_value` — create a second class instance/object to use as `new_default_val` (an `RPModelElement`), call `attr.add_element_default_value(other_element)`, and assert the returned wrapped `RPInstanceValue` is not `None` and appears (indirectly) via `get_value_specifications()`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_attribute.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `add_element_default_value`, `add_string_default_value`, `get_value_specifications`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_attribute.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPVariable default value specifications"
```

---

### Task 3: `RPAttribute` — constant/ordered/reference/static flags

**Files:**
- Modify: `tests/integration/models/elements/variables/test_model_attribute.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_is_constant`, `set_is_constant`, `get_is_ordered`, `set_is_ordered`, `get_is_reference`, `set_is_reference`, `get_is_static`, `set_is_static`

- [ ] **Step 1: Write the new integration tests**

```python
def test_attribute_is_constant_roundtrip(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ConstPkg")
    class_name = self._unique("ConstCls")
    attr_name = self._unique("constAttr")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        attr = test_class.add_attribute(attr_name)
        assert attr.get_is_constant() == 0
        attr.set_is_constant(True)
        assert attr.get_is_constant() == 1
        attr.set_is_constant(False)
        assert attr.get_is_constant() == 0
    finally:
        test_class.delete_from_project()
```

For remaining methods, follow the same pattern (each as its own test method, or grouped as `test_attribute_is_ordered_roundtrip`, `test_attribute_is_reference_roundtrip`, `test_attribute_is_static_roundtrip`), wrapping in `@pytest.mark.xfail` (following the `test_model_operation.py` pattern for `set_is_static`/`set_is_virtual`/`set_is_abstract`) only if the live `Rhapsody2.Application.1` COM object raises `AttributeError` for `setIsStatic`/`setIsOrdered`/`setIsReference` — verify at runtime before deciding.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_attribute.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `getIsConstant`, `setIsConstant`, `getIsOrdered`, `setIsOrdered`, `getIsReference`, `setIsReference`, `get_is_static`, `set_is_static` rows — only flip rows backed by passing (non-xfail) tests.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_attribute.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPAttribute constant/ordered/reference/static flags"
```

---

### Task 4: `RPAttribute` — multiplicity & visibility

**Files:**
- Modify: `tests/integration/models/elements/variables/test_model_attribute.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_multiplicity`, `set_multiplicity`, `get_visibility`, `set_visibility`

- [ ] **Step 1: Write the new integration tests**

```python
def test_attribute_multiplicity_roundtrip(self, test_project: RPProject) -> None:
    pkg_name = self._unique("MultPkg")
    class_name = self._unique("MultCls")
    attr_name = self._unique("multAttr")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        attr = test_class.add_attribute(attr_name)
        attr.set_multiplicity("0..*")
        assert attr.get_multiplicity() == "0..*"
    finally:
        test_class.delete_from_project()
```

For remaining methods, follow the same pattern:
- `test_attribute_visibility_roundtrip` — `attr.set_visibility("private")`; assert `attr.get_visibility() == "private"`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_attribute.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `get_multiplicity`, `set_multiplicity`, `get_visibility`, `set_visibility` (`RPAttribute` rows).

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_attribute.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPAttribute multiplicity and visibility"
```

---

### Task 5: `RPTag` — creation, value & metadata

**Files:**
- Create: `tests/integration/models/elements/variables/test_model_tag.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_value`, `set_value`, `get_tag_meta_class`, `set_tag_meta_class`, `get_base`, `get_from_profile`

- [ ] **Step 1: Write the new integration test file**

```python
import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.variables import RPTag


@pytest.mark.integration
class TestRPTagIntegration:
    """Integration tests for RPTag with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    @staticmethod
    def _create_class_with_tag(pkg: RPPackage, class_name: str, tag_name: str) -> "tuple[RPClass, RPTag]":
        test_class = pkg.add_class(class_name)
        test_class.add_property(tag_name, "String", "initialValue")
        tag = test_class.get_tag(tag_name)
        assert tag is not None
        assert isinstance(tag, RPTag)
        return test_class, tag

    def test_tag_value_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TagValPkg")
        class_name = self._unique("TagValCls")
        tag_name = self._unique("myTag")
        pkg = self._create_package(test_project, pkg_name)
        test_class, tag = self._create_class_with_tag(pkg, class_name, tag_name)
        try:
            assert tag.get_value() == "initialValue"
            tag.set_value("updatedValue")
            assert tag.get_value() == "updatedValue"
        finally:
            test_class.delete_from_project()
```

For remaining methods, follow the same pattern:
- `test_tag_meta_class_roundtrip` — `tag.set_tag_meta_class("Class")`; assert `tag.get_tag_meta_class() == "Class"`.
- `test_tag_get_base` — assert `tag.get_base()` returns the owning `RPModelElement` (or the tag's base classifier, per the live COM object semantics — verify at runtime) and is not `None`.
- `test_tag_get_from_profile` — assert `tag.get_from_profile()` returns a string (empty string is acceptable for a locally-created, non-profile tag; assert `isinstance(..., str)`).
- If `add_property`/`get_tag` does not yield a real `IRPTag` object (e.g. `isinstance(tag, RPTag)` fails), mark the whole test class or affected tests `xfail` with a clear reason and document the actual creation chain discovered, so a future task can correct it.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_tag.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `getValue`, `setValue`, `getTagMetaClass`, `setTagMetaClass`, `getBase`, `getFromProfile` (`RPTag` rows) — only for passing tests.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_tag.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPTag value and metadata"
```

---

### Task 6: `RPTag` — multiplicity & tag context value

**Files:**
- Modify: `tests/integration/models/elements/variables/test_model_tag.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_multiplicity`, `set_multiplicity`, `set_tag_context_value`

- [ ] **Step 1: Write the new integration tests**

```python
def test_tag_multiplicity_roundtrip(self, test_project: RPProject) -> None:
    pkg_name = self._unique("TagMultPkg")
    class_name = self._unique("TagMultCls")
    tag_name = self._unique("multTag")
    pkg = self._create_package(test_project, pkg_name)
    test_class, tag = self._create_class_with_tag(pkg, class_name, tag_name)
    try:
        tag.set_multiplicity("0..*")
        assert tag.get_multiplicity() == "0..*"
    finally:
        test_class.delete_from_project()
```

For the remaining method, follow the same pattern:
- `test_tag_set_context_value` — call `tag.set_tag_context_value(tag, RPCollection(...), RPCollection(...))` per the `IRPModelElement::setTagContextValue` signature in `core.py:1670`; construct minimal empty/singleton `RPCollection` arguments as accepted by the live COM API (inspect `core.py:1670` docstring for exact parameter semantics before writing assertions). If the live COM object rejects the call signature (`AttributeError`/`com_error`), mark `xfail` with a reason describing the discovered COM behavior, and leave the checklist row unflipped.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_tag.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `getMultiplicity`, `setMultiplicity` (`RPTag` rows) and `set_tag_context_value` only if the test passes (non-xfail).

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_tag.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPTag multiplicity and context value"
```

---

### Task 7: `RPArgument` — argument direction

**Files:**
- Create: `tests/integration/models/elements/variables/test_model_argument.py`
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py` (flip checklist boxes only)

**Methods covered:** `get_argument_direction`, `set_argument_direction`

- [ ] **Step 1: Write the new integration test file**

```python
import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.variables import RPArgument


@pytest.mark.integration
class TestRPArgumentIntegration:
    """Integration tests for RPArgument with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_argument_direction_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ArgPkg")
        class_name = self._unique("ArgCls")
        op_name = self._unique("argOp")
        arg_name = self._unique("argParam")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            arg = op.add_argument(arg_name)
            assert arg is not None
            assert isinstance(arg, RPArgument)
            arg.set_argument_direction("out")
            assert arg.get_argument_direction() == "out"
        finally:
            test_class.delete_from_project()
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/variables/test_model_argument.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/variables/model_variables.py`, flip `get_argument_direction`, `set_argument_direction` (`RPArgument` rows).

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/variables/test_model_argument.py src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: add integration tests for RPArgument direction"
```

---

### Task 8: Full Subpackage Verification

**Files:** none modified (verification only)

- [ ] **Step 1: Run the full variables integration suite**

Run: `pytest tests/integration/models/elements/variables/ -m integration -v`

- [ ] **Step 2: Confirm checklist completeness**

Grep the source file for any remaining `[ ] integration test` rows and confirm each unflipped row has a documented reason (COM quirk, `xfail`) in the corresponding test file:

Run: `grep -n "\[ \] integration test" src/rhapsody_cli/models/elements/variables/model_variables.py`

- [ ] **Step 3: Run full quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 4: Commit final state (if any cleanup changes were made)**

```bash
git add tests/integration/models/elements/variables/ src/rhapsody_cli/models/elements/variables/model_variables.py
git commit -m "test: complete integration test coverage for variables subpackage"
```
