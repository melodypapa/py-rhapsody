# Classifiers Subpackage Integration Tests Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add integration tests for all remaining untested methods across the 12 classifier wrapper classes in `src/rhapsody_cli/models/elements/classifiers/`, and create dedicated test files for `RPAssociationClass`, `RPClassifier`, `RPInterfaceItem` which currently have zero coverage. Flip in-source `[ ] integration test` checklist markers to `[x]` as work completes.

**Architecture:** Extends existing test files under `tests/integration/models/elements/classifiers/` and adds new ones for uncovered classes, using the shared `rhapsody_app`/`test_project` fixtures.

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid.uuid4().hex[:8]` for unique names.

## Global Constraints

- Windows-only runtime (COM automation requires Windows + a running Rhapsody instance)
- All test classes use `@pytest.mark.integration`
- All tests consume the `test_project: RPProject` fixture (session-scoped)
- Use `_unique(prefix)` with `uuid.uuid4().hex[:8]` for unique element names
- Always use `try/finally` for cleanup — never rely solely on fixture teardown
- Assert both `isinstance()` return types and read-back values
- After each task's tests pass, flip `[ ] integration test` to `[x] integration test` in the relevant `model_*.py` file for every method that task covers
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit` (live integration run: `pytest tests/integration -m integration`, requires attached Rhapsody)
- New test files import concrete classes via subpackage `__init__.py` re-exports, e.g. `from rhapsody_cli.models.elements.classifiers import RPClassifier`
- Follow the exact style of `tests/integration/models/elements/classifiers/test_model_class.py`
- `RPEnumeration`, `RPInterface`, `RPSignal` and their creation paths (`RPPackage.add_enumeration`/`add_interface`/`add_signal`) were removed entirely — no `IRPEnumeration`/`IRPInterface`/`IRPSignal` COM interface or `addEnumeration`/`addInterface`/`addSignal` COM method exists anywhere in the Rhapsody Java API (see `docs/superpowers/plans/2026-07-15-remove-fictional-package-methods.md`). Real UML Enumeration/Interface/Signal creation uses `RPPackage.add_type`+`set_kind("Enumeration")`, `add_class`+`add_stereotype("Interface", "Class")`, and `add_event` respectively. `RPException` has no own methods (pure inheritance from `RPModelElement`) and remains out of scope for this plan.

---

## Tasks

### Task 1: RPActor — remaining event reception method

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_actor.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_actor.py` (flip checklist boxes only)

**Methods covered:** `add_event_reception_with_event`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_event_reception_with_event(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ActorEvPkg")
    actor_name = self._unique("EvActor")
    event_name = self._unique("MyEvent")
    reception_name = self._unique("onMyEvent")
    pkg = self._create_package(test_project, pkg_name)
    try:
        actor = pkg.add_actor(actor_name)
        event = pkg.add_event(event_name)
        reception = actor.add_event_reception_with_event(reception_name, event)
        assert reception is not None
        assert reception.get_name() == reception_name
        receptions = [i.get_name() for i in actor.get_interface_items()]
        assert reception_name in receptions
    finally:
        actor.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs).

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_actor.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_actor.py`, change `[ ] integration test` to `[x] integration test` for: `add_event_reception_with_event`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_actor.py src/rhapsody_cli/models/elements/classifiers/model_actor.py
git commit -m "test: add integration tests for RPActor event reception"
```

---

### Task 2: RPAssociationClass — new test file (ends & class flag)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_association_class.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_association_class.py` (flip checklist boxes only)

**Methods covered:** `get_end1`, `get_end2`, `get_is_class`, `set_is_class`

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPAssociationClass with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPAssociationClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPAssociationClassIntegration:
    """Integration tests for RPAssociationClass with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_association_ends_and_is_class_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AssocPkg")
        class_a_name = self._unique("ClassA")
        class_b_name = self._unique("ClassB")
        link_name = self._unique("LinkCls")
        pkg = self._create_package(test_project, pkg_name)
        class_a = pkg.add_class(class_a_name)
        class_b = pkg.add_class(class_b_name)
        try:
            relation = class_a.add_relation_to(
                class_b, "roleA", "Association", "1", "roleB", "Association", "1", link_name
            )
            assoc_class = pkg.find_nested_element(link_name)
            assert isinstance(assoc_class, RPAssociationClass)
            end1 = assoc_class.get_end1()
            end2 = assoc_class.get_end2()
            assert end1 is not None
            assert end2 is not None
            assert assoc_class.get_is_class() in (0, 1)
            assoc_class.set_is_class(1)
            assert assoc_class.get_is_class() == 1
        finally:
            class_a.delete_from_project()
            class_b.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs).

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_association_class.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_association_class.py`, change `[ ] integration test` to `[x] integration test` for: `get_end1`, `get_end2`, `get_is_class`, `set_is_class`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_association_class.py src/rhapsody_cli/models/elements/classifiers/model_association_class.py
git commit -m "test: add integration tests for RPAssociationClass"
```

---

### Task 3: RPClass — member management (receptions, triggered ops, ctor/dtor/type deletion)

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_class.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_class.py` (flip checklist boxes only)

**Methods covered:** `add_event_reception`, `add_event_reception_with_event`, `add_reception`, `add_triggered_operation`, `delete_class`, `delete_constructor`, `delete_destructor`, `delete_event_reception`, `delete_reception`, `delete_type`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_and_delete_reception(self, test_project: RPProject) -> None:
    pkg_name = self._unique("RecPkg")
    class_name = self._unique("RecCls")
    reception_name = self._unique("onSignal")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        reception = test_class.add_reception(reception_name)
        assert reception is not None
        assert reception.get_name() == reception_name
        items = [i.get_name() for i in test_class.get_interface_items()]
        assert reception_name in items
        test_class.delete_reception(reception)
        items_after = [i.get_name() for i in test_class.get_interface_items()]
        assert reception_name not in items_after
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_triggered_operation` should assert the returned `RPOperation`'s name and presence in `get_operations()`.
- `delete_class`/`delete_type` should create then delete a nested class/type and assert absence from `get_nested_classifiers()`/type list afterward.
- `delete_constructor`/`delete_destructor` should build on the existing `test_constructor_destructor` pattern already in the file, adding explicit deletion and re-query assertions.
- `add_event_reception`/`add_event_reception_with_event`/`delete_event_reception` mirror the reception pattern above but via the legacy event-reception API.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_class.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_class.py`, change `[ ] integration test` to `[x] integration test` for: `add_event_reception`, `add_event_reception_with_event`, `add_reception`, `add_triggered_operation`, `delete_class`, `delete_constructor`, `delete_destructor`, `delete_event_reception`, `delete_reception`, `delete_type`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_class.py src/rhapsody_cli/models/elements/classifiers/model_class.py
git commit -m "test: add integration tests for RPClass member management"
```

---

### Task 4: RPClass — behavioral flags, links & server sync

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_class.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_class.py` (flip checklist boxes only)

**Methods covered:** `add_link`, `add_link_to_part_via_port`, `get_is_active`, `get_is_behavior_overriden`, `get_is_composite`, `get_is_final`, `get_is_reactive`, `set_is_active`, `set_is_behavior_overriden`, `set_is_final`, `update_contained_diagrams_on_server`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_active_flag_roundtrip(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ActPkg")
    class_name = self._unique("ActCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        assert test_class.get_is_active() in (0, 1)
        test_class.set_is_active(1)
        assert test_class.get_is_active() == 1
        test_class.set_is_active(0)
        assert test_class.get_is_active() == 0
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `get_is_composite`, `get_is_final`, `get_is_reactive` are read-only queries: assert the returned value is `0` or `1` on a freshly created class.
- `set_is_behavior_overriden`/`get_is_behavior_overriden` and `set_is_final` follow the roundtrip pattern above.
- `add_link`/`add_link_to_part_via_port` require a composite class with two parts (instances) and an association or ports; create a minimal composite structure via `add_class` nested parts and `add_relation_to`, then assert the returned `RPLink`.
- `update_contained_diagrams_on_server` should be wrapped in `pytest.mark.xfail(reason="requires RMM/DM server connection not available in test environment", strict=False)` since it targets Rhapsody Model Manager.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_class.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_class.py`, change `[ ] integration test` to `[x] integration test` for: `add_link`, `add_link_to_part_via_port`, `get_is_active`, `get_is_behavior_overriden`, `get_is_composite`, `get_is_final`, `get_is_reactive`, `set_is_active`, `set_is_behavior_overriden`, `set_is_final`, `update_contained_diagrams_on_server`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_class.py src/rhapsody_cli/models/elements/classifiers/model_class.py
git commit -m "test: add integration tests for RPClass flags, links and server sync"
```

---

### Task 5: RPClassifier — new test file: attributes, ports & interface items

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_classifier.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_classifier.py` (flip checklist boxes only)

**Methods covered:** `delete_attribute`, `delete_operation`, `find_attribute`, `find_interface_item`, `find_trigger`, `get_attributes_including_bases`, `get_interface_items`, `get_interface_items_including_bases`, `add_port`, `get_ports`, `get_source_artifacts`, `get_sequence_diagrams`, `get_links`

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPClassifier with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPClassifierIntegration:
    """Integration tests for RPClassifier with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_find_attribute_and_delete_attribute(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AttrPkg")
        class_name = self._unique("AttrCls")
        attr_name = self._unique("myAttr")
        pkg = self._create_package(test_project, pkg_name)
        classifier: RPClassifier = pkg.add_class(class_name)
        try:
            attribute = classifier.add_attribute(attr_name)
            found = classifier.find_attribute(attr_name)
            assert found is not None
            assert found.get_name() == attr_name
            classifier.delete_attribute(attribute)
            attrs_after = [a.get_name() for a in classifier.get_attributes()]
            assert attr_name not in attrs_after
        finally:
            classifier.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `delete_operation` mirrors `delete_attribute` using `add_operation`/`get_operations`.
- `find_interface_item` and `get_interface_items`/`get_interface_items_including_bases` use an operation's signature string (e.g. `"myOp()"`).
- `find_trigger` needs a statechart with a triggered operation/event reception; assert the trigger name matches.
- `add_port`/`get_ports` create a port via `add_port(name)` and assert it appears in `get_ports()`.
- `get_source_artifacts`/`get_sequence_diagrams`/`get_links` on a freshly created classifier should return empty `RPCollection` objects (assert `list(...) == []`) since no diagrams/artifacts have been added.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_classifier.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_classifier.py`, change `[ ] integration test` to `[x] integration test` for: `delete_attribute`, `delete_operation`, `find_attribute`, `find_interface_item`, `find_trigger`, `get_attributes_including_bases`, `get_interface_items`, `get_interface_items_including_bases`, `add_port`, `get_ports`, `get_source_artifacts`, `get_sequence_diagrams`, `get_links`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_classifier.py src/rhapsody_cli/models/elements/classifiers/model_classifier.py
git commit -m "test: add integration tests for RPClassifier attributes, ports and interface items"
```

---

### Task 6: RPClassifier — relations & generalization hierarchy

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_classifier.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_classifier.py` (flip checklist boxes only)

**Methods covered:** `add_relation`, `add_relation_to`, `add_unidirectional_relation`, `add_unidirectional_relation_to`, `delete_relation`, `delete_generalization`, `find_relation`, `find_base_classifier`, `find_derived_classifier`, `get_base_classifiers`, `get_derived_classifiers`, `get_relations`, `get_relations_including_bases`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_relation_to_and_find_and_delete(self, test_project: RPProject) -> None:
    pkg_name = self._unique("RelPkg")
    class_a_name = self._unique("ClsA")
    class_b_name = self._unique("ClsB")
    role1 = self._unique("roleA")
    role2 = self._unique("roleB")
    pkg = self._create_package(test_project, pkg_name)
    class_a = pkg.add_class(class_a_name)
    class_b = pkg.add_class(class_b_name)
    try:
        relation = class_a.add_relation_to(class_b, role1, "Association", "1", role2, "Association", "1", "")
        assert relation is not None
        found = class_a.find_relation(relation.get_name())
        assert found is not None
        relations = list(class_a.get_relations())
        assert relation in relations
        class_a.delete_relation(relation)
        relations_after = list(class_a.get_relations())
        assert relation not in relations_after
    finally:
        class_a.delete_from_project()
        class_b.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_relation`/`add_unidirectional_relation`/`add_unidirectional_relation_to` use the name/package-string overloads instead of a classifier reference; verify against `other_class_package_name=pkg_name`.
- `find_base_classifier`/`find_derived_classifier`/`get_base_classifiers`/`get_derived_classifiers` build on `add_generalization` (already covered) with a parent/child pair, then query in both directions.
- `delete_generalization` should call `add_generalization` then `delete_generalization` and assert `get_generalizations()` no longer contains it.
- `get_relations_including_bases` should verify relations from a base class appear when queried on a derived class.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_classifier.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_classifier.py`, change `[ ] integration test` to `[x] integration test` for: `add_relation`, `add_relation_to`, `add_unidirectional_relation`, `add_unidirectional_relation_to`, `delete_relation`, `delete_generalization`, `find_relation`, `find_base_classifier`, `find_derived_classifier`, `get_base_classifiers`, `get_derived_classifiers`, `get_relations`, `get_relations_including_bases`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_classifier.py src/rhapsody_cli/models/elements/classifiers/model_classifier.py
git commit -m "test: add integration tests for RPClassifier relations and generalizations"
```

---

### Task 7: RPClassifier — flows, activity diagrams, nested classifiers & statecharts

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_classifier.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_classifier.py` (flip checklist boxes only)

**Methods covered:** `add_activity_diagram`, `add_flow_items`, `add_flows`, `delete_flow_items`, `delete_flows`, `find_nested_classifier`, `find_nested_classifier_recursive`, `get_activity_diagram`, `get_behavioral_diagrams`, `get_flow_items`, `get_flows`, `get_nested_classifiers`, `get_statechart`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_activity_diagram_and_get_behavioral_diagrams(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ActDiagPkg")
    class_name = self._unique("ActDiagCls")
    pkg = self._create_package(test_project, pkg_name)
    classifier: RPClassifier = pkg.add_class(class_name)
    try:
        activity_diagram = classifier.add_activity_diagram()
        assert activity_diagram is not None
        fetched = classifier.get_activity_diagram()
        assert fetched is not None
        behavioral_diagrams = list(classifier.get_behavioral_diagrams())
        assert len(behavioral_diagrams) >= 1
    finally:
        classifier.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_flow_items`/`get_flow_items`/`delete_flow_items` and `add_flows`/`get_flows`/`delete_flows` follow an add-verify-delete-reverify cycle.
- `find_nested_classifier` vs `find_nested_classifier_recursive`: create a nested class one level deep and two levels deep, asserting the non-recursive method only finds the first-level one while the recursive method finds both.
- `get_nested_classifiers` should assert the created nested class(es) appear in the returned collection.
- `get_statechart` should build on `add_statechart()` (already covered) and verify the getter returns the same statechart.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_classifier.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_classifier.py`, change `[ ] integration test` to `[x] integration test` for: `add_activity_diagram`, `add_flow_items`, `add_flows`, `delete_flow_items`, `delete_flows`, `find_nested_classifier`, `find_nested_classifier_recursive`, `get_activity_diagram`, `get_behavioral_diagrams`, `get_flow_items`, `get_flows`, `get_nested_classifiers`, `get_statechart`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_classifier.py src/rhapsody_cli/models/elements/classifiers/model_classifier.py
git commit -m "test: add integration tests for RPClassifier flows, activity diagrams and nested classifiers"
```

---

### Task 8: RPInterfaceItem — new test file: arguments & signatures

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_interface_item.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_interface_item.py` (flip checklist boxes only)

**Methods covered:** `add_argument`, `add_argument_before_position`, `get_arguments`, `get_signature`, `get_signature_no_arg_names`, `get_signature_no_arg_types`, `match_on_signature`, `set_arguments`

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPInterfaceItem with live Rhapsody COM API.

These tests require a running Rhapsody instance with an open project.
"""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPInterfaceItemIntegration:
    """Integration tests for RPInterfaceItem (via RPOperation) with real Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_add_argument_and_get_arguments(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ArgPkg")
        class_name = self._unique("ArgCls")
        op_name = self._unique("myOp")
        arg_name = self._unique("param")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            operation = test_class.add_operation(op_name)
            argument = operation.add_argument(arg_name)
            assert argument is not None
            assert argument.get_name() == arg_name
            arguments = [a.get_name() for a in operation.get_arguments()]
            assert arg_name in arguments
        finally:
            test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_argument_before_position` should add two arguments and assert ordering via `get_arguments()`.
- `set_arguments` should set an argument signature string (e.g. `"int x, float y"`) and assert `get_arguments()` reflects two arguments.
- `get_signature`/`get_signature_no_arg_names`/`get_signature_no_arg_types` should assert the expected substrings/format after arguments and a return type are set.
- `match_on_signature` should create two operations with identical argument signatures and assert `True`, then a differing one and assert `False`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_interface_item.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_interface_item.py`, change `[ ] integration test` to `[x] integration test` for: `add_argument`, `add_argument_before_position`, `get_arguments`, `get_signature`, `get_signature_no_arg_names`, `get_signature_no_arg_types`, `match_on_signature`, `set_arguments`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_interface_item.py src/rhapsody_cli/models/elements/classifiers/model_interface_item.py
git commit -m "test: add integration tests for RPInterfaceItem arguments and signatures"
```

---

### Task 9: RPOperation — flowchart & descriptive flag getters

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_operation.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_operation.py` (flip checklist boxes only)

**Methods covered:** `create_auto_flow_chart`, `delete_flowchart`, `get_flowchart`, `get_is_cg_derived`, `get_is_const`, `get_is_ctor`, `get_is_dtor`, `get_is_final`, `get_is_inline`, `get_is_trigger`, `get_visibility`, `get_implementation_signature`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_create_and_delete_auto_flow_chart(self, test_project: RPProject) -> None:
    pkg_name = self._unique("FlowPkg")
    class_name = self._unique("FlowCls")
    op_name = self._unique("flowOp")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        op = test_class.add_operation(op_name)
        op.create_auto_flow_chart()
        flowchart = op.get_flowchart()
        assert flowchart is not None
        op.delete_flowchart()
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `get_is_cg_derived`, `get_is_const`, `get_is_ctor`, `get_is_dtor`, `get_is_final`, `get_is_inline`, `get_is_trigger` are read-only flags on a freshly created plain operation: assert each returns `0` (falsy) by default.
- `get_is_ctor`/`get_is_dtor` should additionally be asserted as `1` on operations created via `add_constructor`/`add_destructor` respectively (reusing the `test_constructor_destructor` pattern).
- `get_visibility` should assert an integer in `{0, 1, 2, 3}` for a freshly created operation.
- `get_implementation_signature` should assert a non-empty string is returned.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_operation.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_operation.py`, change `[ ] integration test` to `[x] integration test` for: `create_auto_flow_chart`, `delete_flowchart`, `get_flowchart`, `get_is_cg_derived`, `get_is_const`, `get_is_ctor`, `get_is_dtor`, `get_is_final`, `get_is_inline`, `get_is_trigger`, `get_visibility`, `get_implementation_signature`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_operation.py src/rhapsody_cli/models/elements/classifiers/model_operation.py
git commit -m "test: add integration tests for RPOperation flowchart and flag getters"
```

---

### Task 10: RPOperation — argument deletion, initializer, setters, returns & server sync

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_operation.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_operation.py` (flip checklist boxes only)

**Methods covered:** `delete_argument`, `get_initializer`, `get_returns`, `set_body`, `set_flowchart`, `set_initializer`, `set_is_const`, `set_is_final`, `set_returns`, `set_visibility`, `update_contained_diagrams_on_server`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_set_and_get_body(self, test_project: RPProject) -> None:
    pkg_name = self._unique("BodySetPkg")
    class_name = self._unique("BodySetCls")
    op_name = self._unique("bodyOp")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        op = test_class.add_operation(op_name)
        op.set_body("return 42;")
        assert "42" in op.get_body()
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `delete_argument` should add an argument via `add_argument`, then delete it and assert `get_arguments()` is empty.
- `set_returns`/`get_returns` should create a second class to use as the return type, call `set_returns`, and assert `get_returns()` matches by name.
- `set_visibility`/`set_is_const`/`set_is_final` are `pytest.mark.xfail(strict=False)` candidates if the COM property proves read-only in the live environment (verify empirically; only mark xfail if the roundtrip actually fails).
- `set_initializer`/`get_initializer` and `set_flowchart` follow the standard setter/getter roundtrip pattern (for `set_flowchart`, create a flowchart via `create_auto_flow_chart()`/`get_flowchart()` first, then assign it explicitly).
- `update_contained_diagrams_on_server` should be wrapped in `pytest.mark.xfail(reason="requires RMM/DM server connection not available in test environment", strict=False)`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_operation.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_operation.py`, change `[ ] integration test` to `[x] integration test` for: `delete_argument`, `get_initializer`, `get_returns`, `set_body`, `set_flowchart`, `set_initializer`, `set_is_const`, `set_is_final`, `set_returns`, `set_visibility`, `update_contained_diagrams_on_server`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_operation.py src/rhapsody_cli/models/elements/classifiers/model_operation.py
git commit -m "test: add integration tests for RPOperation argument, initializer and setters"
```

---

### Task 11: RPStatechart — diagram graphics builders

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_statechart.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_statechart.py` (flip checklist boxes only)

**Methods covered:** `add_free_shape_by_type`, `add_image`, `add_new_edge_by_type`, `add_new_edge_for_element`, `add_new_node_by_type`, `add_new_node_for_element`, `add_text_box`, `open_diagram_view`, `add_new_accept_event_action`, `add_new_accept_time_event`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_new_node_by_type(self, test_project: RPProject) -> None:
    pkg_name = self._unique("NodePkg")
    class_name = self._unique("NodeCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        sc = test_class.add_statechart()
        node = sc.add_new_node_by_type("State", 10, 10, 100, 60)
        assert node is not None
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_new_edge_by_type`/`add_new_edge_for_element` require two nodes created via `add_new_node_by_type` first, then an edge between them; assert the returned `RPGraphEdge` is not `None`.
- `add_new_node_for_element` requires an existing model element (e.g. a nested class) to attach graphically.
- `add_free_shape_by_type`, `add_image`, `add_text_box` follow the same node-creation pattern with differing `meta_type`/no meta_type.
- `open_diagram_view` has no return value to assert; simply call it and assert no exception is raised (may need `pytest.mark.xfail(reason="requires interactive Rhapsody GUI session", strict=False)` if it fails headlessly).
- `add_new_accept_event_action`/`add_new_accept_time_event` assert the returned model element is not `None` and has the expected name.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_statechart.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_statechart.py`, change `[ ] integration test` to `[x] integration test` for: `add_free_shape_by_type`, `add_image`, `add_new_edge_by_type`, `add_new_edge_for_element`, `add_new_node_by_type`, `add_new_node_for_element`, `add_text_box`, `open_diagram_view`, `add_new_accept_event_action`, `add_new_accept_time_event`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_statechart.py src/rhapsody_cli/models/elements/classifiers/model_statechart.py
git commit -m "test: add integration tests for RPStatechart diagram graphics builders"
```

---

### Task 12: RPStatechart — diagram lifecycle & pictures

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_statechart.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_statechart.py` (flip checklist boxes only)

**Methods covered:** `close_diagram`, `create_graphics`, `delete_state`, `get_picture`, `get_picture_as`, `get_picture_as_divided_metafiles`, `get_pictures_with_image_map`, `get_statechart_diagram`, `populate_diagram`, `set_show_diagram_frame`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_create_graphics_and_get_statechart_diagram(self, test_project: RPProject) -> None:
    pkg_name = self._unique("GfxPkg")
    class_name = self._unique("GfxCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        sc = test_class.add_statechart()
        sc.create_graphics()
        diagram = sc.get_statechart_diagram()
        assert diagram is not None
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `delete_state` requires a state node added via `add_new_node_by_type("State", ...)`, then delete it and assert it is no longer in `get_elements_in_diagram()`.
- `get_picture`/`get_picture_as`/`get_picture_as_divided_metafiles`/`get_pictures_with_image_map` should assert non-`None`/non-empty results after `create_graphics()`; use formats such as `"BMP"` for `get_picture_as`.
- `populate_diagram`/`set_show_diagram_frame` have no return value — assert no exception raised and (for `set_show_diagram_frame`) that the call completes for both `0` and `1`.
- `close_diagram` should be called after `create_graphics()` and assert no exception is raised.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_statechart.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_statechart.py`, change `[ ] integration test` to `[x] integration test` for: `close_diagram`, `create_graphics`, `delete_state`, `get_picture`, `get_picture_as`, `get_picture_as_divided_metafiles`, `get_pictures_with_image_map`, `get_statechart_diagram`, `populate_diagram`, `set_show_diagram_frame`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_statechart.py src/rhapsody_cli/models/elements/classifiers/model_statechart.py
git commit -m "test: add integration tests for RPStatechart diagram lifecycle and pictures"
```

---

### Task 13: RPStatechart — state/trigger queries & inheritance overrides

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_statechart.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_statechart.py` (flip checklist boxes only)

**Methods covered:** `get_all_triggers`, `get_elements_in_diagram`, `get_graphical_elements`, `get_inherits_from`, `get_is_main_behavior`, `get_is_overridden`, `get_its_class`, `get_root_state`, `override_inheritance`, `set_as_main_behavior`, `unoverride_inheritance`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_get_its_class_and_root_state(self, test_project: RPProject) -> None:
    pkg_name = self._unique("RootPkg")
    class_name = self._unique("RootCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        sc = test_class.add_statechart()
        owning_class = sc.get_its_class()
        assert owning_class is not None
        assert owning_class.get_name() == class_name
        root_state = sc.get_root_state()
        assert root_state is not None
    finally:
        test_class.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `get_all_triggers`/`get_elements_in_diagram`/`get_graphical_elements` on a freshly created statechart should return `RPCollection` objects convertible to a `list` (possibly empty); after `create_graphics()` and a node addition, assert the node appears in `get_elements_in_diagram()`/`get_graphical_elements()`.
- `get_is_main_behavior`/`set_as_main_behavior` follow the roundtrip pattern: assert initial value, set to `1`, assert `1`.
- `get_inherits_from`/`get_is_overridden`/`override_inheritance`/`unoverride_inheritance` require a parent class with a statechart and a child class inheriting from it (`add_superclass`); assert the child's statechart's `get_inherits_from()` returns the parent statechart, call `override_inheritance()` and assert `get_is_overridden() == 1`, then `unoverride_inheritance()` and assert `get_is_overridden() == 0`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_statechart.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_statechart.py`, change `[ ] integration test` to `[x] integration test` for: `get_all_triggers`, `get_elements_in_diagram`, `get_graphical_elements`, `get_inherits_from`, `get_is_main_behavior`, `get_is_overridden`, `get_its_class`, `get_root_state`, `override_inheritance`, `set_as_main_behavior`, `unoverride_inheritance`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_statechart.py src/rhapsody_cli/models/elements/classifiers/model_statechart.py
git commit -m "test: add integration tests for RPStatechart state/trigger queries and inheritance"
```

---

### Task 14: RPStereotype — metaclass management

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_stereotype.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_stereotype.py` (flip checklist boxes only)

**Methods covered:** `add_meta_class`, `get_icon`, `get_is_new_term`, `get_of_meta_class`, `remove_meta_class`, `set_is_new_term`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_and_remove_meta_class(self, test_project: RPProject) -> None:
    pkg_name = self._unique("MetaPkg")
    class_name = self._unique("MetaCls")
    stereo_name = self._unique("MyMetaStereo")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        stereotype = test_class.add_stereotype(stereo_name, "Class")
        stereotype.add_meta_class("Attribute")
        meta_classes = list(stereotype.get_of_meta_class())
        assert "Attribute" in meta_classes or any("Attribute" in str(m) for m in meta_classes)
        stereotype.remove_meta_class("Attribute")
        meta_classes_after = list(stereotype.get_of_meta_class())
        assert "Attribute" not in meta_classes_after
    finally:
        test_class.delete_from_project()
        stereotype.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `get_icon` on a freshly created stereotype should assert a string is returned (possibly empty).
- `get_is_new_term`/`set_is_new_term` follow the standard roundtrip pattern.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_stereotype.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_stereotype.py`, change `[ ] integration test` to `[x] integration test` for: `add_meta_class`, `get_icon`, `get_is_new_term`, `get_of_meta_class`, `remove_meta_class`, `set_is_new_term`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_stereotype.py src/rhapsody_cli/models/elements/classifiers/model_stereotype.py
git commit -m "test: add integration tests for RPStereotype metaclass management"
```

---

### Task 15: RPUseCase — extension & entry point management

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_usecase.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_usecase.py` (flip checklist boxes only)

**Methods covered:** `add_extension_point`, `get_extension_points`, `get_entry_points`, `delete_entry_point`, `delete_extension_point`, `find_entry_point`, `find_extension_point`, `set_is_behavior_overriden`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_find_and_delete_extension_point(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ExtPkg")
    uc_name = self._unique("ExtUc")
    ext_name = self._unique("myExtension")
    pkg = self._create_package(test_project, pkg_name)
    uc = pkg.add_use_case(uc_name)
    try:
        uc.add_extension_point(ext_name)
        found = uc.find_extension_point(ext_name)
        assert found is not None
        extension_points = list(uc.get_extension_points())
        assert any(ext_name in str(e) for e in extension_points)
        uc.delete_extension_point(ext_name)
        extension_points_after = list(uc.get_extension_points())
        assert not any(ext_name in str(e) for e in extension_points_after)
    finally:
        uc.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `get_entry_points`/`delete_entry_point`/`find_entry_point` mirror the extension-point cycle above (entry points are typically populated by Rhapsody's use-case tooling; if the COM API has no direct `addEntryPoint`, assert the getter returns an empty/valid collection and that `find_entry_point` for a non-existent name returns `None`/falsy — document with a comment if entry-point creation is not exposed).
- `set_is_behavior_overriden`/`get_is_behavior_overriden` follow the standard roundtrip pattern (paired with Task 16's `get_is_behavior_overriden` read, or tested together here).

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_usecase.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_usecase.py`, change `[ ] integration test` to `[x] integration test` for: `add_extension_point`, `get_extension_points`, `get_entry_points`, `delete_entry_point`, `delete_extension_point`, `find_entry_point`, `find_extension_point`, `set_is_behavior_overriden`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_usecase.py src/rhapsody_cli/models/elements/classifiers/model_usecase.py
git commit -m "test: add integration tests for RPUseCase extension and entry points"
```

---

### Task 16: RPUseCase — describing diagrams, behavior override & server sync

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_usecase.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_usecase.py` (flip checklist boxes only)

**Methods covered:** `add_describing_diagram`, `get_describing_diagrams`, `get_describing_diagram`, `delete_describing_diagram`, `add_event_reception_with_event`, `get_is_behavior_overriden`, `update_contained_diagrams_on_server`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_get_and_delete_describing_diagram(self, test_project: RPProject) -> None:
    pkg_name = self._unique("DescPkg")
    uc_name = self._unique("DescUc")
    diagram_name = self._unique("DescDiagram")
    pkg = self._create_package(test_project, pkg_name)
    uc = pkg.add_use_case(uc_name)
    try:
        diagram = pkg.add_use_case_diagram(diagram_name)
        uc.add_describing_diagram(diagram)
        diagrams = list(uc.get_describing_diagrams())
        assert diagram in diagrams
        fetched = uc.get_describing_diagram(diagram_name)
        assert fetched is not None
        uc.delete_describing_diagram(diagram)
        diagrams_after = list(uc.get_describing_diagrams())
        assert diagram not in diagrams_after
    finally:
        uc.delete_from_project()
        diagram.delete_from_project()
```

For the remaining methods in this task, follow the same pattern (one test per behavior, or shared test for tightly-coupled getter/setter pairs). Notably:
- `add_event_reception_with_event` requires an event created via `pkg.add_event(name)`; assert the returned reception element is not `None`.
- `get_is_behavior_overriden` should assert a boolean-like `0`/`1` default on a freshly created use case (paired with Task 15's `set_is_behavior_overriden` if not already covered there).
- `update_contained_diagrams_on_server` should be wrapped in `pytest.mark.xfail(reason="requires RMM/DM server connection not available in test environment", strict=False)`.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/classifiers/test_model_usecase.py -m integration -v`
Expected: all new tests PASS (or documented `xfail` for known COM quirks)

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/classifiers/model_usecase.py`, change `[ ] integration test` to `[x] integration test` for: `add_describing_diagram`, `get_describing_diagrams`, `get_describing_diagram`, `delete_describing_diagram`, `add_event_reception_with_event`, `get_is_behavior_overriden`, `update_contained_diagrams_on_server`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_usecase.py src/rhapsody_cli/models/elements/classifiers/model_usecase.py
git commit -m "test: add integration tests for RPUseCase describing diagrams and behavior sync"
```

---

### Task 17: Full Subpackage Verification

**Files:**
- None (verification only)

- [ ] **Step 1: Run the full classifiers integration suite**

Run: `pytest tests/integration/models/elements/classifiers -m integration -v`
Expected: all tests PASS or are documented `xfail` (no unexpected failures/errors)

- [ ] **Step 2: Confirm checklist completeness**

Grep every `model_*.py` file in `src/rhapsody_cli/models/elements/classifiers/` for `integration test` and confirm every row for an implemented (`[x] impl`) method now shows `[x] integration test`.

Run: `grep -rn "\[ \] integration test" src/rhapsody_cli/models/elements/classifiers/`
Expected: no matches remain for implemented methods (any remaining `[ ]` rows must correspond to `[ ] impl` — i.e. not-yet-implemented methods, which are out of scope for this plan).

- [ ] **Step 3: Run full quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
Expected: all pass

- [ ] **Step 4: Final commit (if any cleanup needed)**

```bash
git add tests/integration/models/elements/classifiers/ src/rhapsody_cli/models/elements/classifiers/
git commit -m "test: complete classifiers subpackage integration test coverage"
```
