# Model Classes Full Sweep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement all unchecked methods (483 `NotImplementedError` stubs + ~427 methods not yet created), add `register_wrapper` for all ~64 unregistered classes, and create 4 missing wrapper classes (Interface, Signal, Exception, Enumeration).

**Actual counts (verified 2026-07-13):**
- 483 `raise NotImplementedError` stubs across 10 files
- 910 unchecked checklist items across 29 files (includes ~427 methods that need to be created from scratch, mainly in containment files)
- 96 total RP* classes, 32 registered, ~64 unregistered

**Architecture:** Each model class wraps a Rhapsody COM interface. Methods delegate to COM via `call_com()`, `_get_method_or_property()`, or `_set_method_or_property()`. Registration maps metaclass strings to Python wrappers at import time.

**Tech Stack:** Python, win32com, pywintypes, pytest

## Global Constraints

- All COM calls → `call_com(lambda: self._com.methodName(...))` (translates `com_error` → `RhapsodyRuntimeException`)
- No-arg getters → `_get_method_or_property(self._com, "getX", "x")`
- Single-arg setters → `_set_method_or_property(self._com, "setX", "x", value)`
- Return wrapped element → `AbstractRPModelElement.wrap(self.call_com(...))` or specific wrapper constructor
- Return collection → `RPCollection(self.call_com(...))`
- All tests use `make_fake_element` / `make_fake_collection` from `tests/unit/models/fakes.py`
- TDD: write failing test first, then implement
- After each task: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`
  - Note: On Windows, `black --check src/ tests/` is slow; run on changed files only
- **Circular import avoidance:** `register_wrapper` calls at module level can trigger circular imports. Each module that registers must ensure its imports use `TYPE_CHECKING` guards for any module that imports it back. The `__init__.py` of each subpackage must import submodules in the correct order.
- **Requirements convention waived:** This is a mechanical refactoring (implementing COM delegation stubs). SW requirement IDs (SWR_MODEL_*) and test case IDs (UTS_MODEL_*) are not required for this plan. Class docstring requirement ID comments are also waived.
- **Checklist update:** After implementing each method, update its checklist entry from `[ ]` to `[x]` for impl, docstring, and test.

---
## Repetitive Method Implementation Pattern

Every unchecked method follows exactly ONE of these patterns. The task steps show 2-3 representative examples per class; the remaining methods use the identical pattern with different method names.

### Pattern A: No-arg getter returning primitive

```python
# Checklist entry: [ ] getXxx
def get_xxx(self) -> str:
    return self._get_method_or_property(self._com, "getXxx", "xxx")
```

Test:
```python
def test_thing_get_xxx() -> None:
    fake = make_fake_element("MetaClass", getXxx="expected")
    obj = RPThing(fake)
    assert obj.get_xxx() == "expected"
    fake.getXxx.assert_called_once_with()
```

### Pattern B: No-arg getter returning wrapped element

```python
def get_xxx(self) -> "RPOther":
    return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.getXxx()))
```

Test:
```python
def test_thing_get_xxx_wraps_result() -> None:
    fake = make_fake_element("MetaClass")
    result = make_fake_element("OtherMeta", getName="Foo")
    fake.getXxx.return_value = result
    obj = RPThing(fake)
    wrapped = obj.get_xxx()
    assert wrapped.get_name() == "Foo"
    fake.getXxx.assert_called_once_with()
```

### Pattern C: No-arg getter returning collection

```python
def get_xxx(self) -> "RPCollection":
    return RPCollection(self.call_com(lambda: self._com.getXxx()))
```

Test:
```python
def test_thing_get_xxx_returns_collection() -> None:
    from rhapsody_cli.models.core import RPCollection
    fake = make_fake_element("MetaClass")
    el1 = make_fake_element("SomeMeta", getName="A")
    fake.getXxx.return_value = make_fake_collection([el1])
    obj = RPThing(fake)
    result = obj.get_xxx()
    assert isinstance(result, RPCollection)
```

### Pattern D: Single-arg setter

```python
def set_xxx(self, value: str) -> None:
    self._set_method_or_property(self._com, "setXxx", "xxx", value)
```

Test:
```python
def test_thing_set_xxx_delegates() -> None:
    fake = make_fake_element("MetaClass")
    obj = RPThing(fake)
    obj.set_xxx("val")
    fake.setXxx.assert_called_once_with("val")
```

### Pattern E: Multi-arg method returning wrapped element

```python
def add_xxx(self, name: str, type_: str) -> "RPOther":
    return AbstractRPModelElement.wrap(
        self.call_com(lambda: self._com.addXxx(name, type_))
    )
```

### Pattern F: Multi-arg void method

```python
def delete_xxx(self, target: "RPOther") -> None:
    self.call_com(lambda: self._com.deleteXxx(target._com))
```

### Pattern G: Boolean check returning int (Rhapsody uses 0/1)

```python
def is_xxx(self) -> int:
    return int(self.call_com(lambda: self._com.isXxx()))
```

Test:
```python
def test_thing_is_xxx() -> None:
    fake = make_fake_element("MetaClass", isXxx=True)
    obj = RPThing(fake)
    assert obj.is_xxx() == 1
```

---
## Task Dependency Order

1. Task 0: 4 missing wrapper classes (Interface, Signal, Exception, Enumeration)
2. Task 1: Statemachine (RPStateVertex, RPState) — 55 stubs
3. Task 2: Interactions (11 classes) — 82 stubs
4. Task 3: Common - other (RPClassifierRole, RPSysMLPort, RPType) — 50 stubs
5. Task 4: Values (5 classes) — 15 stubs
6. Task 5: Templates (3 classes) — 10 stubs
7. Task 6: Variables - remaining unchecked (RPVariable, RPTag) — 14 checklist items
8. Task 7: Activity - actions (7 classes) — 22 stubs
9. Task 8: Activity - flowchart (5 classes) — 46 stubs
10. Task 9: Classifiers - remaining unchecked (6 classes) — ~64 checklist items
11. Task 10: Relations - remaining unchecked (5 classes) — ~25 checklist items
12. Task 11: Containment - Package + Project — 153 checklist items (methods need to be created from scratch, no stubs exist)
13. Task 12: Containment - Component + Collaboration + Configuration + Node + ComponentInstance — 137 checklist items (methods need to be created from scratch)
14. Task 13: Diagrams - types (11 subclasses) + RPDiagram — 39 checklist items
15. Task 14: Requirements - RPAnnotation (registration only, 0 methods)
16. Task 15: Graphics (14 classes) — 190 stubs
17. Task 16: Common - misc (RPEnumerationLiteral, RPConstraint) — 3 checklist items
18. Task 17: Registration sweep — safety net (most done by Tasks 0-16)
19. Task 18: Update convenience methods to use wrap() properly
20. Task 19: Final Quality Gate

**Note:** Tasks 11-12 are the largest scope (290 checklist items total) because containment files have checklist items but no method stubs — methods must be created from scratch. Consider splitting these into smaller sub-tasks if needed.

---
### Task 0: Create 4 Missing Wrapper Classes (Interface, Signal, Exception, Enumeration)

**Files:**
- Create: `src/rhapsody_cli/models/elements/classifiers/model_interface.py`
- Create: `src/rhapsody_cli/models/elements/classifiers/model_signal.py`
- Create: `src/rhapsody_cli/models/elements/classifiers/model_exception.py`
- Create: `src/rhapsody_cli/models/elements/classifiers/model_enumeration.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/__init__.py`

**Interfaces:**
- Consumes: `AbstractRPModelElement.wrap()` — the 4 new classes must be registered so `wrap()` returns typed wrappers instead of generic `RPModelElement`
- Produces: `RPInterface("Interface")`, `RPSignal("Signal")`, `RPException("Exception")`, `RPEnumeration("Enumeration")` registered wrappers usable by `RPPackage.add_interface()`, `add_signal()`, `add_exception()`, `add_enumeration()`

**Note:** The Rhapsody COM API metaclass strings for these are unknown from the codebase. We infer from the pattern (`addInterface()`, `addSignal()`, `addException()`, `addEnumeration()` on `IRPPackage`) that the metaclass strings used by `getMetaClass()` are `"Interface"`, `"Signal"`, `"Exception"`, `"Enumeration"`. These will be confirmed in the registration test.

- [ ] **Step 1: Write failing tests for all 4 new classes**

Create `tests/unit/models/elements/test_interface.py`:
```python
"""Tests for rhapsody_cli.models.elements.classifiers.model_interface.RPInterface."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPInterface
from tests.unit.models.fakes import make_fake_element


def test_interface_is_model_element() -> None:
    fake = make_fake_element("Interface", getName="IFoo")
    iface = RPInterface(fake)
    assert isinstance(iface, RPModelElement)
    assert iface.get_name() == "IFoo"


def test_interface_is_registered() -> None:
    fake = make_fake_element("Interface", getName="IFoo")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPInterface)
```

Create `tests/unit/models/elements/test_signal.py`:
```python
"""Tests for rhapsody_cli.models.elements.classifiers.model_signal.RPSignal."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPSignal
from tests.unit.models.fakes import make_fake_element


def test_signal_is_model_element() -> None:
    fake = make_fake_element("Signal", getName="Sig1")
    sig = RPSignal(fake)
    assert isinstance(sig, RPModelElement)
    assert sig.get_name() == "Sig1"


def test_signal_is_registered() -> None:
    fake = make_fake_element("Signal", getName="Sig1")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPSignal)
```

Create `tests/unit/models/elements/test_exception.py`:
```python
"""Tests for rhapsody_cli.models.elements.classifiers.model_exception.RPException."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPException
from tests.unit.models.fakes import make_fake_element


def test_exception_is_model_element() -> None:
    fake = make_fake_element("Exception", getName="Exc1")
    exc = RPException(fake)
    assert isinstance(exc, RPModelElement)
    assert exc.get_name() == "Exc1"


def test_exception_is_registered() -> None:
    fake = make_fake_element("Exception", getName="Exc1")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPException)
```

Create `tests/unit/models/elements/test_enumeration.py`:
```python
"""Tests for rhapsody_cli.models.elements.classifiers.model_enumeration.RPEnumeration."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPEnumeration
from tests.unit.models.fakes import make_fake_element


def test_enumeration_is_model_element() -> None:
    fake = make_fake_element("Enumeration", getName="Color")
    enum = RPEnumeration(fake)
    assert isinstance(enum, RPModelElement)
    assert enum.get_name() == "Color"


def test_enumeration_is_registered() -> None:
    fake = make_fake_element("Enumeration", getName="Color")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPEnumeration)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_interface.py tests/unit/models/elements/test_signal.py tests/unit/models/elements/test_exception.py tests/unit/models/elements/test_enumeration.py -v`

Expected: FAIL — 8 tests fail with `ImportError` (modules not found) or `ModuleNotFoundError`

- [ ] **Step 3: Create the 4 files**

Create `src/rhapsody_cli/models/elements/classifiers/model_interface.py`:
```python
"""Interface model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPInterface(RPModelElement):
    """Wraps ``IRPInterface``."""


AbstractRPModelElement.register_wrapper("Interface", RPInterface)
```

Create `src/rhapsody_cli/models/elements/classifiers/model_signal.py`:
```python
"""Signal model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPSignal(RPModelElement):
    """Wraps ``IRPSignal``."""


AbstractRPModelElement.register_wrapper("Signal", RPSignal)
```

Create `src/rhapsody_cli/models/elements/classifiers/model_exception.py`:
```python
"""Exception model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPException(RPModelElement):
    """Wraps ``IRPException``."""


AbstractRPModelElement.register_wrapper("Exception", RPException)
```

Create `src/rhapsody_cli/models/elements/classifiers/model_enumeration.py`:
```python
"""Enumeration model-element wrapper."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement


class RPEnumeration(RPModelElement):
    """Wraps ``IRPEnumeration``."""


AbstractRPModelElement.register_wrapper("Enumeration", RPEnumeration)
```

- [ ] **Step 4: Update classifiers `__init__.py` to export and register the 4 new classes**

Modify `src/rhapsody_cli/models/elements/classifiers/__init__.py`:
```python
from rhapsody_cli.models.elements.classifiers.model_actor import RPActor
from rhapsody_cli.models.elements.classifiers.model_association_class import RPAssociationClass
from rhapsody_cli.models.elements.classifiers.model_class import RPClass
from rhapsody_cli.models.elements.classifiers.model_classifier import RPClassifier
from rhapsody_cli.models.elements.classifiers.model_enumeration import RPEnumeration
from rhapsody_cli.models.elements.classifiers.model_exception import RPException
from rhapsody_cli.models.elements.classifiers.model_interface import RPInterface
from rhapsody_cli.models.elements.classifiers.model_interface_item import RPInterfaceItem
from rhapsody_cli.models.elements.classifiers.model_operation import RPOperation
from rhapsody_cli.models.elements.classifiers.model_signal import RPSignal
from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
from rhapsody_cli.models.elements.classifiers.model_stereotype import RPStereotype
from rhapsody_cli.models.elements.classifiers.model_usecase import RPUseCase

__all__ = [
    "RPActor",
    "RPAssociationClass",
    "RPClass",
    "RPClassifier",
    "RPEnumeration",
    "RPException",
    "RPInterface",
    "RPInterfaceItem",
    "RPOperation",
    "RPSignal",
    "RPStatechart",
    "RPStereotype",
    "RPUseCase",
]
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/models/elements/test_interface.py tests/unit/models/elements/test_signal.py tests/unit/models/elements/test_exception.py tests/unit/models/elements/test_enumeration.py -v`

Expected: 8 PASS

- [ ] **Step 6: Run quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

Expected: All pass

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/classifiers/model_interface.py \
       src/rhapsody_cli/models/elements/classifiers/model_signal.py \
       src/rhapsody_cli/models/elements/classifiers/model_exception.py \
       src/rhapsody_cli/models/elements/classifiers/model_enumeration.py \
       src/rhapsody_cli/models/elements/classifiers/__init__.py \
       tests/unit/models/elements/test_interface.py \
       tests/unit/models/elements/test_signal.py \
       tests/unit/models/elements/test_exception.py \
       tests/unit/models/elements/test_enumeration.py
git commit -m "feat: add Interface, Signal, Exception, Enumeration wrapper classes"
```

---

### Task 1: Statemachine — RPStateVertex + RPState (55 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/statemachine/model_statemachine.py`
- Create: `tests/unit/models/elements/test_statemachine.py`

**Registration packages needed:** `"StateVertex"`, `"State"`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_statemachine.py` with the following test functions. Each method gets a test (either a delegation test or a return-value test). Below are representative tests; ALL 55 listed methods in the checklist get similar tests.

For `RPStateVertex` (7 methods):
```python
"""Tests for rhapsody_cli.elements.statemachine.RPStateVertex and RPState."""

import pytest
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.statemachine import RPState, RPStateVertex
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPStateVertex:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("StateVertex", getName="SV1")
        sv = RPStateVertex(fake)
        assert isinstance(sv, RPModelElement)
        assert sv.get_name() == "SV1"

    def test_add_flow_delegates_and_wraps(self) -> None:
        fake = make_fake_element("StateVertex")
        to = make_fake_element("StateVertex", getName="Target")
        result = make_fake_element("Transition", getName="Flow1")
        fake.addFlow.return_value = result
        sv = RPStateVertex(fake)
        wrapped = sv.add_flow("ControlFlow", RPStateVertex(to))
        assert wrapped.get_name() == "Flow1"
        fake.addFlow.assert_called_once_with("ControlFlow", to)

    def test_add_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("StateVertex")
        to = make_fake_element("StateVertex", getName="Target")
        result = make_fake_element("Transition", getName="T1")
        fake.addTransition.return_value = result
        sv = RPStateVertex(fake)
        wrapped = sv.add_transition(RPStateVertex(to))
        assert wrapped.get_name() == "T1"
        fake.addTransition.assert_called_once_with(to)

    def test_delete_transition_delegates(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteTransition.return_value = None
        sv = RPStateVertex(fake)
        sv.delete_transition(RPModelElement(trans))
        fake.deleteTransition.assert_called_once_with(trans)

    def test_get_in_transitions_returns_collection(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.getInTransitions.return_value = make_fake_collection([trans])
        sv = RPStateVertex(fake)
        result = sv.get_in_transitions()
        assert isinstance(result, RPCollection)
        fake.getInTransitions.assert_called_once_with()

    def test_get_out_transitions_returns_collection(self) -> None:
        fake = make_fake_element("StateVertex")
        trans = make_fake_element("Transition", getName="T1")
        fake.getOutTransitions.return_value = make_fake_collection([trans])
        sv = RPStateVertex(fake)
        result = sv.get_out_transitions()
        assert isinstance(result, RPCollection)
        fake.getOutTransitions.assert_called_once_with()

    def test_get_parent_wraps_result(self) -> None:
        fake = make_fake_element("StateVertex")
        parent = make_fake_element("State", getName="Parent")
        fake.getParent.return_value = parent
        sv = RPStateVertex(fake)
        result = sv.get_parent()
        assert isinstance(result, RPState)
        assert result.get_name() == "Parent"
        fake.getParent.assert_called_once_with()

    def test_set_parent_delegates(self) -> None:
        fake = make_fake_element("StateVertex")
        parent = make_fake_element("State", getName="Parent")
        fake.setParent.return_value = None
        sv = RPStateVertex(fake)
        sv.set_parent(RPState(parent))
        fake.setParent.assert_called_once_with(parent)

    def test_is_registered(self) -> None:
        fake = make_fake_element("StateVertex", getName="SV1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPStateVertex)
```

For `RPState` (48 methods — representative tests):
```python
class TestRPState:
    def test_is_state_vertex(self) -> None:
        fake = make_fake_element("State", getName="S1")
        s = RPState(fake)
        assert isinstance(s, RPStateVertex)

    def test_add_activity_final_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Final")
        fake.addActivityFinal.return_value = result
        s = RPState(fake)
        wrapped = s.add_activity_final()
        assert wrapped.get_name() == "Final"
        fake.addActivityFinal.assert_called_once_with()

    def test_add_connector_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Connector", getName="Fork1")
        fake.addConnector.return_value = result
        s = RPState(fake)
        wrapped = s.add_connector("Fork")
        assert isinstance(wrapped, RPModelElement)
        fake.addConnector.assert_called_once_with("Fork")

    def test_add_internal_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        trigger = make_fake_element("Operation", getName="ev")
        result = make_fake_element("Transition", getName="T1")
        fake.addInternalTransition.return_value = result
        s = RPState(fake)
        wrapped = s.add_internal_transition(RPModelElement(trigger))
        assert wrapped.get_name() == "T1"
        fake.addInternalTransition.assert_called_once_with(trigger)

    def test_add_state_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Sub")
        fake.addState.return_value = result
        s = RPState(fake)
        wrapped = s.add_state("Sub")
        assert wrapped.get_name() == "Sub"
        fake.addState.assert_called_once_with("Sub")

    def test_add_static_reaction_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        trigger = make_fake_element("Operation", getName="ev")
        result = make_fake_element("Transition", getName="T1")
        fake.addStaticReaction.return_value = result
        s = RPState(fake)
        wrapped = s.add_static_reaction(RPModelElement(trigger))
        assert wrapped.get_name() == "T1"
        fake.addStaticReaction.assert_called_once_with(trigger)

    def test_add_termination_state_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("State", getName="Term")
        fake.addTerminationState.return_value = result
        s = RPState(fake)
        wrapped = s.add_termination_state()
        assert wrapped.get_name() == "Term"
        fake.addTerminationState.assert_called_once_with()

    def test_create_default_transition_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        from_ = make_fake_element("State", getName="Root")
        result = make_fake_element("Transition", getName="DT1")
        fake.createDefaultTransition.return_value = result
        s = RPState(fake)
        wrapped = s.create_default_transition(RPState(from_))
        assert wrapped.get_name() == "DT1"
        fake.createDefaultTransition.assert_called_once_with(from_)

    def test_create_sub_statechart_delegates_and_wraps(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Statechart", getName="Sub")
        fake.createSubStatechart.return_value = result
        s = RPState(fake)
        wrapped = s.create_sub_statechart()
        assert wrapped.get_name() == "Sub"
        fake.createSubStatechart.assert_called_once_with()

    def test_delete_connector_delegates(self) -> None:
        fake = make_fake_element("State")
        conn = make_fake_element("Connector", getName="C1")
        fake.deleteConnector.return_value = None
        s = RPState(fake)
        s.delete_connector(RPModelElement(conn))
        fake.deleteConnector.assert_called_once_with(conn)

    def test_delete_internal_transition_delegates(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteInternalTransition.return_value = None
        s = RPState(fake)
        s.delete_internal_transition(RPModelElement(trans))
        fake.deleteInternalTransition.assert_called_once_with(trans)

    def test_delete_static_reaction_delegates(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.deleteStaticReaction.return_value = None
        s = RPState(fake)
        s.delete_static_reaction(RPModelElement(trans))
        fake.deleteStaticReaction.assert_called_once_with(trans)

    def test_get_default_transition_wraps_result(self) -> None:
        fake = make_fake_element("State")
        result = make_fake_element("Transition", getName="DT1")
        fake.getDefaultTransition.return_value = result
        s = RPState(fake)
        wrapped = s.get_default_transition()
        assert wrapped.get_name() == "DT1"
        fake.getDefaultTransition.assert_called_once_with()

    def test_get_entry_action_returns_string(self) -> None:
        fake = make_fake_element("State", getEntryAction="entry()")
        s = RPState(fake)
        assert s.get_entry_action() == "entry()"
        fake.getEntryAction.assert_called_once_with()

    def test_get_exit_action_returns_string(self) -> None:
        fake = make_fake_element("State", getExitAction="exit()")
        s = RPState(fake)
        assert s.get_exit_action() == "exit()"
        fake.getExitAction.assert_called_once_with()

    def test_get_full_name_in_statechart_returns_string(self) -> None:
        fake = make_fake_element("State", getFullNameInStatechart="ROOT.On.Idle")
        s = RPState(fake)
        assert s.get_full_name_in_statechart() == "ROOT.On.Idle"
        fake.getFullNameInStatechart.assert_called_once_with()

    def test_get_inherits_from_wraps_result(self) -> None:
        fake = make_fake_element("State")
        parent = make_fake_element("State", getName="Parent")
        fake.getInheritsFrom.return_value = parent
        s = RPState(fake)
        wrapped = s.get_inherits_from()
        assert isinstance(wrapped, RPState)
        assert wrapped.get_name() == "Parent"
        fake.getInheritsFrom.assert_called_once_with()

    def test_get_internal_transitions_returns_collection(self) -> None:
        fake = make_fake_element("State")
        trans = make_fake_element("Transition", getName="T1")
        fake.getInternalTransitions.return_value = make_fake_collection([trans])
        s = RPState(fake)
        result = s.get_internal_transitions()
        assert isinstance(result, RPCollection)
        fake.getInternalTransitions.assert_called_once_with()

    def test_get_is_overridden_returns_int(self) -> None:
        fake = make_fake_element("State", getIsOverridden=1)
        s = RPState(fake)
        assert s.get_is_overridden() == 1
        fake.getIsOverridden.assert_called_once_with()

    def test_get_is_reference_activity_returns_int(self) -> None:
        fake = make_fake_element("State", getIsReferenceActivity=0)
        s = RPState(fake)
        assert s.get_is_reference_activity() == 0
        fake.getIsReferenceActivity.assert_called_once_with()

    def test_get_its_statechart_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sc = make_fake_element("Statechart", getName="SC1")
        fake.getItsStatechart.return_value = sc
        s = RPState(fake)
        wrapped = s.get_its_statechart()
        assert wrapped.get_name() == "SC1"
        fake.getItsStatechart.assert_called_once_with()

    def test_get_its_swimlane_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sw = make_fake_element("Swimlane", getName="Lane1")
        fake.getItsSwimlane.return_value = sw
        s = RPState(fake)
        wrapped = s.get_its_swimlane()
        assert wrapped.get_name() == "Lane1"
        fake.getItsSwimlane.assert_called_once_with()

    def test_get_logical_states_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getLogicalStates.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_logical_states()
        assert isinstance(result, RPCollection)
        fake.getLogicalStates.assert_called_once_with()

    def test_get_nested_statechart_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sc = make_fake_element("Statechart", getName="Sub")
        fake.getNestedStatechart.return_value = sc
        s = RPState(fake)
        wrapped = s.get_nested_statechart()
        assert wrapped.get_name() == "Sub"
        fake.getNestedStatechart.assert_called_once_with()

    def test_get_reference_to_activity_wraps_result(self) -> None:
        fake = make_fake_element("State")
        act = make_fake_element("Class", getName="Act1")
        fake.getReferenceToActivity.return_value = act
        s = RPState(fake)
        wrapped = s.get_reference_to_activity()
        assert wrapped.get_name() == "Act1"
        fake.getReferenceToActivity.assert_called_once_with()

    def test_get_send_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        sa = make_fake_element("SendAction", getName="SA1")
        fake.getSendAction.return_value = sa
        s = RPState(fake)
        wrapped = s.get_send_action()
        assert wrapped.get_name() == "SA1"
        fake.getSendAction.assert_called_once_with()

    def test_get_state_type_returns_string(self) -> None:
        fake = make_fake_element("State", getStateType="And")
        s = RPState(fake)
        assert s.get_state_type() == "And"
        fake.getStateType.assert_called_once_with()

    def test_get_static_reactions_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sr = make_fake_element("Transition", getName="SR1")
        fake.getStaticReactions.return_value = make_fake_collection([sr])
        s = RPState(fake)
        result = s.get_static_reactions()
        assert isinstance(result, RPCollection)
        fake.getStaticReactions.assert_called_once_with()

    def test_get_sub_state_vertices_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getSubStateVertices.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_sub_state_vertices()
        assert isinstance(result, RPCollection)
        fake.getSubStateVertices.assert_called_once_with()

    def test_get_sub_states_returns_collection(self) -> None:
        fake = make_fake_element("State")
        sub = make_fake_element("State", getName="S1")
        fake.getSubStates.return_value = make_fake_collection([sub])
        s = RPState(fake)
        result = s.get_sub_states()
        assert isinstance(result, RPCollection)
        fake.getSubStates.assert_called_once_with()

    def test_get_the_entry_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        action = make_fake_element("Action", getName="entryAct")
        fake.getTheEntryAction.return_value = action
        s = RPState(fake)
        wrapped = s.get_the_entry_action()
        assert wrapped.get_name() == "entryAct"
        fake.getTheEntryAction.assert_called_once_with()

    def test_get_the_exit_action_wraps_result(self) -> None:
        fake = make_fake_element("State")
        action = make_fake_element("Action", getName="exitAct")
        fake.getTheExitAction.return_value = action
        s = RPState(fake)
        wrapped = s.get_the_exit_action()
        assert wrapped.get_name() == "exitAct"
        fake.getTheExitAction.assert_called_once_with()

    def test_is_and_returns_int(self) -> None:
        fake = make_fake_element("State", isAnd=True)
        s = RPState(fake)
        assert s.is_and() == 1
        fake.isAnd.assert_called_once_with()

    def test_is_compound_returns_int(self) -> None:
        fake = make_fake_element("State", isCompound=True)
        s = RPState(fake)
        assert s.is_compound() == 1

    def test_is_leaf_returns_int(self) -> None:
        fake = make_fake_element("State", isLeaf=True)
        s = RPState(fake)
        assert s.is_leaf() == 1

    def test_is_root_returns_int(self) -> None:
        fake = make_fake_element("State", isRoot=True)
        s = RPState(fake)
        assert s.is_root() == 1

    def test_is_send_action_state_returns_int(self) -> None:
        fake = make_fake_element("State", isSendActionState=True)
        s = RPState(fake)
        assert s.is_send_action_state() == 1

    def test_override_inheritance_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.overrideInheritance.return_value = None
        s = RPState(fake)
        s.override_inheritance()
        fake.overrideInheritance.assert_called_once_with()

    def test_reset_entry_action_inheritance_wraps_self(self) -> None:
        fake = make_fake_element("State")
        fake.resetEntryActionInheritance.return_value = fake
        s = RPState(fake)
        result = s.reset_entry_action_inheritance()
        assert isinstance(result, RPState)
        fake.resetEntryActionInheritance.assert_called_once_with()

    def test_reset_exit_action_inheritance_wraps_self(self) -> None:
        fake = make_fake_element("State")
        fake.resetExitActionInheritance.return_value = fake
        s = RPState(fake)
        result = s.reset_exit_action_inheritance()
        assert isinstance(result, RPState)
        fake.resetExitActionInheritance.assert_called_once_with()

    def test_set_entry_action_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setEntryAction.return_value = None
        s = RPState(fake)
        s.set_entry_action("entry()")
        fake.setEntryAction.assert_called_once_with("entry()")

    def test_set_exit_action_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setExitAction.return_value = None
        s = RPState(fake)
        s.set_exit_action("exit()")
        fake.setExitAction.assert_called_once_with("exit()")

    def test_set_internal_transition_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setInternalTransition.return_value = None
        s = RPState(fake)
        s.set_internal_transition("ev", "[g]", "act")
        fake.setInternalTransition.assert_called_once_with("ev", "[g]", "act")

    def test_set_its_swimlane_delegates(self) -> None:
        fake = make_fake_element("State")
        sw = make_fake_element("Swimlane", getName="L1")
        fake.setItsSwimlane.return_value = None
        s = RPState(fake)
        s.set_its_swimlane(RPModelElement(sw))
        fake.setItsSwimlane.assert_called_once_with(sw)

    def test_set_reference_to_activity_delegates(self) -> None:
        fake = make_fake_element("State")
        act = make_fake_element("Class", getName="Act1")
        fake.setReferenceToActivity.return_value = None
        s = RPState(fake)
        s.set_reference_to_activity(RPModelElement(act))
        fake.setReferenceToActivity.assert_called_once_with(act)

    def test_set_state_type_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setStateType.return_value = None
        s = RPState(fake)
        s.set_state_type("And")
        fake.setStateType.assert_called_once_with("And")

    def test_set_static_reaction_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.setStaticReaction.return_value = None
        s = RPState(fake)
        s.set_static_reaction("ev", "[g]", "act")
        fake.setStaticReaction.assert_called_once_with("ev", "[g]", "act")

    def test_unoverride_inheritance_delegates(self) -> None:
        fake = make_fake_element("State")
        fake.unoverrideInheritance.return_value = None
        s = RPState(fake)
        s.unoverride_inheritance()
        fake.unoverrideInheritance.assert_called_once_with()

    def test_is_registered(self) -> None:
        fake = make_fake_element("State", getName="S1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPState)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_statemachine.py -v`

Expected: FAIL — all tests raise `NotImplementedError` or `ImportError` (if test file doesn't exist yet)

- [ ] **Step 3: Implement all 55 methods + register_wrapper**

Replace every `raise NotImplementedError` in `src/rhapsody_cli/models/elements/statemachine/model_statemachine.py` with the appropriate implementation from Patterns A-G above, and add the following at module level:

**Circular import note:** The statemachine module already uses `TYPE_CHECKING` guards for imports from interactions, activity, graphics, and classifiers. The `register_wrapper` calls at the bottom of the file run at import time but only reference `RPStateVertex` and `RPState` (defined in this same file), so no circular import is triggered. However, ensure that `AbstractRPModelElement` is imported at the top of the file (add it to the existing `from rhapsody_cli.models.core import RPModelElement` line).

For `RPStateVertex`, replace each `raise NotImplementedError` with:
- `add_flow` → Pattern E
- `add_transition` → Pattern E
- `delete_transition` → Pattern F
- `get_in_transitions` → Pattern C
- `get_out_transitions` → Pattern C
- `get_parent` → Pattern B (wrap as `RPState(…)`)
- `set_parent` → Pattern D (multi-arg: Pattern F)

For `RPState`, replace each `raise NotImplementedError` with:
- `add_activity_final` → Pattern E (wrap result in `RPState`)
- `add_connector` → Pattern E (wrap result in `wrap()` generic)
- `add_internal_transition` → Pattern E
- `add_state` → Pattern E (wrap result in `RPState`)
- `add_static_reaction` → Pattern E
- `add_termination_state` → Pattern E (wrap result in `RPState`)
- `create_default_transition` → Pattern E
- `create_nested_statechart` → **skip** (deprecated method, not in checklist; if present, leave as `raise NotImplementedError`)
- `create_sub_statechart` → Pattern B (note: method name in COM is `createSubStatechart`)
- `delete_connector` → Pattern F
- `delete_internal_transition` → Pattern F
- `delete_static_reaction` → Pattern F
- `get_default_transition` → Pattern B
- `get_entry_action` → Pattern A
- `get_exit_action` → Pattern A
- `get_full_name_in_statechart` → Pattern A
- `get_inherits_from` → Pattern B (wrap as `RPState`)
- `get_internal_transitions` → Pattern C
- `get_is_overridden` → Pattern A (return int)
- `get_is_reference_activity` → Pattern A (return int)
- `get_its_statechart` → Pattern B
- `get_its_swimlane` → Pattern B
- `get_logical_states` → Pattern C
- `get_nested_statechart` → Pattern B
- `get_reference_to_activity` → Pattern B
- `get_send_action` → Pattern B
- `get_state_type` → Pattern A
- `get_static_reactions` → Pattern C
- `get_sub_state_vertices` → Pattern C
- `get_sub_states` → Pattern C
- `get_the_entry_action` → Pattern B
- `get_the_exit_action` → Pattern B
- `is_and` → Pattern G
- `is_compound` → Pattern G
- `is_leaf` → Pattern G
- `is_root` → Pattern G
- `is_send_action_state` → Pattern G
- `override_inheritance` → Pattern F
- `reset_entry_action_inheritance` → Pattern B (self-wrapping)
- `reset_exit_action_inheritance` → Pattern B (self-wrapping)
- `set_entry_action` → Pattern D
- `set_exit_action` → Pattern D
- `set_internal_transition` → Pattern F (3 args)
- `set_its_swimlane` → Pattern F
- `set_reference_to_activity` → Pattern F
- `set_state_type` → Pattern D
- `set_static_reaction` → Pattern F (3 args)
- `unoverride_inheritance` → Pattern F

Add at module level (bottom of file):
```python
AbstractRPModelElement.register_wrapper("StateVertex", RPStateVertex)
AbstractRPModelElement.register_wrapper("State", RPState)
```

- [ ] **Step 4: Add RPState and RPStateVertex to statemachine `__init__.py` and `__all__`**

Read the file first, then add the exports.

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/models/elements/test_statemachine.py -v`

Expected: 59 PASS (9 RPStateVertex tests + 50 RPState tests)

- [ ] **Step 6: Run quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/statemachine/model_statemachine.py \
       src/rhapsody_cli/models/elements/statemachine/__init__.py \
       tests/unit/models/elements/test_statemachine.py
git commit -m "feat(statemachine): implement RPStateVertex and RPState methods + register_wrapper"
```

---

### Task 2: Interactions — 11 classes, 82 methods (RPMessage, RPEvent, RPTransition, etc.)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/interactions/model_interactions.py`
- Create: `tests/unit/models/elements/test_interactions.py`

**Registration packages needed:** `"Message"`, `"Event"`, `"Transition"`, `"Trigger"`, `"Guard"`, `"DestructionEvent"`, `"ExecutionOccurrence"`, `"EventReception"`, `"InteractionOccurrence"`, `"InteractionOperand"`, `"InteractionOperator"`

**Methods to implement (82 total, following Patterns A-G):**

`RPMessage` (20 methods): `addActualArgument`, `addArgumentValue`, `getActualArguments`, `getArgs`, `getAssignment`, `getInteractionOccurrence`, `getIsAssign`, `getIsBasic`, `getIsBroadcast`, `getIsFound`, `getIsLost`, `getIsReply`, `getIsTimeout`, `getItsInteractionOperator`, `getKind`, `getOperation`, `getSequenceNumber`, `getTimeout`, `setAssignment`, `setKind`

`RPEvent` (14 methods): `addFlow`, `getFlows`, `getIsSystem`, `getIsTime`, `getIsTriggered`, `getOperation`, `getRcvEventReception`, `getRcvOperation`, `getSendEventReception`, `getSendOperation`, `setIsSystem`, `setIsTime`, `setIsTriggered`, `setOperation`

`RPTransition` (8 methods): `addArgumentValue`, `getArgVals`, `getEvent`, `getGuard`, `getItsTrigger`, `getTarget`, `getTrigger`, `setEvent`

`RPTrigger` (5 methods): `getEvent`, `getEventReception`, `getItsClass`, `setEvent`, `setEventReception`

`RPGuard` (3 methods): `getConstraint`, `getSpecification`, `setSpecification`

`RPDestructionEvent` (3 methods): `getMessage`, `getOperation`, `setOperation`

`RPExecutionOccurrence` (5 methods): `getDuration`, `getEndMessage`, `getItsMessage`, `getStartMessage`, `getTime`

`RPEventReception` (6 methods): `addArgumentValue`, `getArgVals`, `getEvent`, `setEvent`, `addFlow`, `getFlows`

`RPInteractionOccurrence` (8 methods): `addActualArgument`, `getActualArguments`, `getReferencedDiagram`, `setReferencedDiagram`, `getInteractionOperand`, `getGate`, `getMessage`, `getMessages`

`RPInteractionOperand` (4 methods): `addInteractionOperator`, `getGuard`, `getInteractionOperators`, `getMessages`

`RPInteractionOperator` (6 methods): `addInteractionOperand`, `getInteractionOperands`, `getOperator`, `getOperands`, `setOperator`, `getMessages`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_interactions.py` with tests for all 11 classes following the same patterns as Task 1. Each method gets a delegation test. Representative example:

```python
"""Tests for rhapsody_cli.elements.interactions.* classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.interactions import (
    RPDestructionEvent,
    RPEvent,
    RPEventReception,
    RPExecutionOccurrence,
    RPGuard,
    RPInteractionOccurrence,
    RPInteractionOperand,
    RPInteractionOperator,
    RPMessage,
    RPTransition,
    RPTrigger,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPMessage:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Message", getName="Msg1")
        msg = RPMessage(fake)
        assert isinstance(msg, RPModelElement)
        assert msg.get_name() == "Msg1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Message", getName="Msg1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPMessage)

    def test_add_actual_argument_delegates(self) -> None:
        fake = make_fake_element("Message")
        val = make_fake_element("ValueSpecification", getName="v1")
        fake.addActualArgument.return_value = None
        msg = RPMessage(fake)
        msg.add_actual_argument(RPModelElement(val))
        fake.addActualArgument.assert_called_once_with(val)

    def test_add_argument_value_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.addArgumentValue.return_value = None
        msg = RPMessage(fake)
        msg.add_argument_value("x", "5")
        fake.addArgumentValue.assert_called_once_with("x", "5")

    def test_get_actual_arguments_returns_collection(self) -> None:
        fake = make_fake_element("Message")
        val = make_fake_element("ValueSpecification", getName="v1")
        fake.getActualArguments.return_value = make_fake_collection([val])
        msg = RPMessage(fake)
        result = msg.get_actual_arguments()
        assert isinstance(result, RPCollection)
        fake.getActualArguments.assert_called_once_with()

    # ... remaining methods follow same patterns
    def test_get_args_returns_string(self) -> None:
        fake = make_fake_element("Message", getArgs="x=5")
        msg = RPMessage(fake)
        assert msg.get_args() == "x=5"
        fake.getArgs.assert_called_once_with()

    def test_get_assignment_returns_string(self) -> None:
        fake = make_fake_element("Message", getAssignment="result")
        msg = RPMessage(fake)
        assert msg.get_assignment() == "result"
        fake.getAssignment.assert_called_once_with()

    def test_get_interaction_occurrence_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        io = make_fake_element("InteractionOccurrence", getName="IO1")
        fake.getInteractionOccurrence.return_value = io
        msg = RPMessage(fake)
        wrapped = msg.get_interaction_occurrence()
        assert wrapped.get_name() == "IO1"
        fake.getInteractionOccurrence.assert_called_once_with()

    def test_get_is_assign_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsAssign=True)
        msg = RPMessage(fake)
        assert msg.get_is_assign() == 1

    def test_get_is_basic_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsBasic=True)
        msg = RPMessage(fake)
        assert msg.get_is_basic() == 1

    def test_get_is_broadcast_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsBroadcast=True)
        msg = RPMessage(fake)
        assert msg.get_is_broadcast() == 1

    def test_get_is_found_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsFound=True)
        msg = RPMessage(fake)
        assert msg.get_is_found() == 1

    def test_get_is_lost_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsLost=True)
        msg = RPMessage(fake)
        assert msg.get_is_lost() == 1

    def test_get_is_reply_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsReply=True)
        msg = RPMessage(fake)
        assert msg.get_is_reply() == 1

    def test_get_is_timeout_returns_int(self) -> None:
        fake = make_fake_element("Message", getIsTimeout=True)
        msg = RPMessage(fake)
        assert msg.get_is_timeout() == 1

    def test_get_its_interaction_operator_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        op = make_fake_element("InteractionOperator", getName="Alt")
        fake.getItsInteractionOperator.return_value = op
        msg = RPMessage(fake)
        wrapped = msg.get_its_interaction_operator()
        assert wrapped.get_name() == "Alt"
        fake.getItsInteractionOperator.assert_called_once_with()

    def test_get_kind_returns_string(self) -> None:
        fake = make_fake_element("Message", getKind="Asynch")
        msg = RPMessage(fake)
        assert msg.get_kind() == "Asynch"
        fake.getKind.assert_called_once_with()

    def test_get_operation_wraps_result(self) -> None:
        fake = make_fake_element("Message")
        op = make_fake_element("Operation", getName="doThing")
        fake.getOperation.return_value = op
        msg = RPMessage(fake)
        wrapped = msg.get_operation()
        assert wrapped.get_name() == "doThing"
        fake.getOperation.assert_called_once_with()

    def test_get_sequence_number_returns_string(self) -> None:
        fake = make_fake_element("Message", getSequenceNumber="1")
        msg = RPMessage(fake)
        assert msg.get_sequence_number() == "1"
        fake.getSequenceNumber.assert_called_once_with()

    def test_get_timeout_returns_int(self) -> None:
        fake = make_fake_element("Message", getTimeout=42)
        msg = RPMessage(fake)
        assert msg.get_timeout() == 42
        fake.getTimeout.assert_called_once_with()

    def test_set_assignment_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setAssignment.return_value = None
        msg = RPMessage(fake)
        msg.set_assignment("result")
        fake.setAssignment.assert_called_once_with("result")

    def test_set_kind_delegates(self) -> None:
        fake = make_fake_element("Message")
        fake.setKind.return_value = None
        msg = RPMessage(fake)
        msg.set_kind("Asynch")
        fake.setKind.assert_called_once_with("Asynch")
```

Write remaining test classes for `TestRPEvent` (14 methods), `TestRPTransition` (8 methods), `TestRPTrigger` (5 methods), `TestRPGuard` (3 methods), `TestRPDestructionEvent` (3 methods), `TestRPExecutionOccurrence` (5 methods), `TestRPEventReception` (6 methods), `TestRPInteractionOccurrence` (8 methods), `TestRPInteractionOperand` (4 methods), `TestRPInteractionOperator` (6 methods) — all following the same Patterns A-G.

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_interactions.py -v`

Expected: FAIL — all 82+ tests raise `NotImplementedError`

- [ ] **Step 3: Implement all 82 methods + register_wrapper**

Replace every `raise NotImplementedError` in `src/rhapsody_cli/models/elements/interactions/model_interactions.py` using Patterns A-G, and add register_wrapper for all 11 classes at the end of the file.

- [ ] **Step 4: Update interactions `__init__.py` to export all 11 classes**

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/unit/models/elements/test_interactions.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/interactions/model_interactions.py \
       src/rhapsody_cli/models/elements/interactions/__init__.py \
       tests/unit/models/elements/test_interactions.py
git commit -m "feat(interactions): implement 11 interaction classes with register_wrapper"
```

---

### Task 3: Common — Other (RPClassifierRole, RPSysMLPort, RPType) — 57 methods

**Files:**
- Modify: `src/rhapsody_cli/models/elements/common/model_other_model.py`
- Create: `tests/unit/models/elements/test_classifier_role.py`
- Create: `tests/unit/models/elements/test_sysml_port.py`
- Create: `tests/unit/models/elements/test_type.py`

**Registration packages needed:** `"ClassifierRole"`, `"SysMLPort"`, `"Type"`

**Methods to implement:**
- `RPClassifierRole` (7 methods): `getFormalClassifier`, `getFormalInstance`, `getReferencedSequenceDiagram`, `getReferencingClassifierRolesRecursively`, `getRoleType`, `setFormalClassifier`, `setFormalInstance`, `setReferencedSequenceDiagram`
- `RPSysMLPort` (7 methods): `addLink`, `getIsReversed`, `getPortDirection`, `getType`, `setIsReversed`, `setPortDirection`, `setType`
- `RPType` (35 methods): `addEnumerationLiteral`, `deleteEnumerationLiteral`, `getDeclaration`, `getEnumerationLiterals`, `getIsPredefined`, `getIsTypedef`, `getIsTypedefConstant`, `getIsTypedefOrdered`, `getIsTypedefReference`, `getKind`, `getTypedefBaseType`, `getTypedefMultiplicity`, `isArray`, `isEnum`, `isEqualTo`, `isImplicit`, `isKindEnumeration`, `isKindLanguage`, `isKindStruct`, `isKindTypedef`, `isKindUnion`, `isPointer`, `isPointerToPointer`, `isReference`, `isReferenceToPointer`, `isStruct`, `isTemplate`, `isUnion`, `setDeclaration`, `setIsTypedefConstant`, `setIsTypedefOrdered`, `setIsTypedefReference`, `setKind`, `setTypedefBaseType`, `setTypedefMultiplicity`

**Import notes:** The file already imports `RPModelElement` and uses `TYPE_CHECKING` guards for `RPCollection`, `RPEnumerationLiteral`, `RPPackage`, `RPSequenceDiagram`, `RPLink`, `RPRelation`. Add `AbstractRPModelElement` to the existing `from rhapsody_cli.models.core import RPModelElement` line (final import line becomes `from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement`). The `RPClassifier` and `RPInstance` imports at module top are already present (used as base classes / type hints).

**Registration notes:** Add the following three `register_wrapper` calls at the bottom of `src/rhapsody_cli/models/elements/common/model_other_model.py` (after the `RPType` class definition):

```python
AbstractRPModelElement.register_wrapper("ClassifierRole", RPClassifierRole)
AbstractRPModelElement.register_wrapper("SysMLPort", RPSysMLPort)
AbstractRPModelElement.register_wrapper("Type", RPType)
```

**`__init__.py` note:** `src/rhapsody_cli/models/elements/common/__init__.py` already imports and exports `RPClassifierRole`, `RPSysMLPort`, `RPType` — no change needed there. Step 4 below becomes a verification step only.

- [ ] **Step 1: Write failing tests**

Create three test files. Representative tests below — each remaining method follows the same Pattern as the representative shown.

Create `tests/unit/models/elements/test_classifier_role.py`:
```python
"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPClassifierRole."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.common import RPClassifierRole
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.relations import RPInstance
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPClassifierRole:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("ClassifierRole", getName="Lifeline1")
        role = RPClassifierRole(fake)
        assert isinstance(role, RPModelElement)
        assert role.get_name() == "Lifeline1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("ClassifierRole", getName="L1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPClassifierRole)

    def test_get_formal_classifier_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("ClassifierRole")
        clf = make_fake_element("Class", getName="Foo")
        fake.getFormalClassifier.return_value = clf
        role = RPClassifierRole(fake)
        wrapped = role.get_formal_classifier()
        assert wrapped.get_name() == "Foo"
        fake.getFormalClassifier.assert_called_once_with()

    def test_get_formal_instance_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("ClassifierRole")
        inst = make_fake_element("Instance", getName="Inst1")
        fake.getFormalInstance.return_value = inst
        role = RPClassifierRole(fake)
        wrapped = role.get_formal_instance()
        assert wrapped.get_name() == "Inst1"
        fake.getFormalInstance.assert_called_once_with()

    def test_get_referencing_classifier_roles_recursively_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning RPCollection
        fake = make_fake_element("ClassifierRole")
        sub = make_fake_element("ClassifierRole", getName="Sub")
        fake.getReferencingClassifierRolesRecursively.return_value = make_fake_collection([sub])
        role = RPClassifierRole(fake)
        result = role.get_referencing_classifier_roles_recursively()
        assert isinstance(result, RPCollection)
        fake.getReferencingClassifierRolesRecursively.assert_called_once_with()

    def test_get_role_type_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("ClassifierRole", getRoleType="CLASS")
        role = RPClassifierRole(fake)
        assert role.get_role_type() == "CLASS"
        fake.getRoleType.assert_called_once_with()

    def test_set_formal_classifier_delegates(self) -> None:
        # Pattern F — multi-arg void method (single RPClassifier arg)
        fake = make_fake_element("ClassifierRole")
        clf = make_fake_element("Class", getName="Foo")
        fake.setFormalClassifier.return_value = None
        role = RPClassifierRole(fake)
        role.set_formal_classifier(RPClassifier(clf))
        fake.setFormalClassifier.assert_called_once_with(clf)

    def test_set_referenced_sequence_diagram_delegates(self) -> None:
        # Pattern F
        from rhapsody_cli.models.elements.diagrams import RPSequenceDiagram
        fake = make_fake_element("ClassifierRole")
        sd = make_fake_element("SequenceDiagram", getName="SD1")
        fake.setReferencedSequenceDiagram.return_value = None
        role = RPClassifierRole(fake)
        role.set_referenced_sequence_diagram(RPSequenceDiagram(sd))
        fake.setReferencedSequenceDiagram.assert_called_once_with(sd)
```

Create `tests/unit/models/elements/test_sysml_port.py`:
```python
"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPSysMLPort."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.common import RPSysMLPort
from rhapsody_cli.models.elements.classifiers import RPClassifier
from tests.unit.models.fakes import make_fake_element


class TestRPSysMLPort:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("SysMLPort", getName="P1")
        port = RPSysMLPort(fake)
        assert isinstance(port, RPModelElement)
        assert port.get_name() == "P1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("SysMLPort", getName="P1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSysMLPort)

    def test_get_is_reversed_returns_int(self) -> None:
        # Pattern G — boolean check returning int
        fake = make_fake_element("SysMLPort", getIsReversed=True)
        port = RPSysMLPort(fake)
        assert port.get_is_reversed() == 1
        fake.getIsReversed.assert_called_once_with()

    def test_get_port_direction_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("SysMLPort", getPortDirection="InOut")
        port = RPSysMLPort(fake)
        assert port.get_port_direction() == "InOut"
        fake.getPortDirection.assert_called_once_with()

    def test_get_type_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("SysMLPort")
        t = make_fake_element("Class", getName="T1")
        fake.getType.return_value = t
        port = RPSysMLPort(fake)
        wrapped = port.get_type()
        assert wrapped.get_name() == "T1"
        fake.getType.assert_called_once_with()

    def test_set_is_reversed_delegates(self) -> None:
        # Pattern D — single-arg setter (int arg)
        fake = make_fake_element("SysMLPort")
        port = RPSysMLPort(fake)
        port.set_is_reversed(1)
        fake.setIsReversed.assert_called_once_with(1)

    def test_set_port_direction_delegates(self) -> None:
        # Pattern D — single-arg setter (str arg)
        fake = make_fake_element("SysMLPort")
        port = RPSysMLPort(fake)
        port.set_port_direction("Out")
        fake.setPortDirection.assert_called_once_with("Out")

    def test_add_link_delegates_and_wraps(self) -> None:
        # Pattern E — multi-arg method returning wrapped element
        from rhapsody_cli.models.elements.graphics import RPLink
        from rhapsody_cli.models.elements.relations import RPInstance, RPRelation
        from rhapsody_cli.models.elements.containment import RPPackage
        fake = make_fake_element("SysMLPort")
        from_part = make_fake_element("Instance", getName="From")
        to_part = make_fake_element("Instance", getName="To")
        assoc = make_fake_element("Relation", getName="R")
        to_port = make_fake_element("SysMLPort", getName="ToPort")
        new_owner = make_fake_element("Package", getName="Pkg")
        link = make_fake_element("Link", getName="L1")
        fake.addLink.return_value = link
        port = RPSysMLPort(fake)
        wrapped = port.add_link(
            RPInstance(from_part), RPInstance(to_part), RPRelation(assoc),
            RPSysMLPort(to_port), RPPackage(new_owner),
        )
        assert wrapped.get_name() == "L1"
        fake.addLink.assert_called_once_with(from_part, to_part, assoc, to_port, new_owner)
```

Create `tests/unit/models/elements/test_type.py`:
```python
"""Tests for rhapsody_cli.models.elements.common.model_other_model.RPType."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.common import RPType
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPType:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("Type", getName="T1")
        t = RPType(fake)
        assert isinstance(t, RPModelElement)
        assert t.get_name() == "T1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("Type", getName="T1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPType)

    def test_add_enumeration_literal_delegates_and_wraps(self) -> None:
        # Pattern E
        from rhapsody_cli.models.elements.common import RPEnumerationLiteral
        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.addEnumerationLiteral.return_value = lit
        t = RPType(fake)
        wrapped = t.add_enumeration_literal("RED")
        assert wrapped.get_name() == "RED"
        fake.addEnumerationLiteral.assert_called_once_with("RED")

    def test_delete_enumeration_literal_delegates(self) -> None:
        # Pattern F
        from rhapsody_cli.models.elements.common import RPEnumerationLiteral
        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.deleteEnumerationLiteral.return_value = None
        t = RPType(fake)
        t.delete_enumeration_literal(RPEnumerationLiteral(lit))
        fake.deleteEnumerationLiteral.assert_called_once_with(lit)

    def test_get_declaration_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Type", getDeclaration="int x")
        t = RPType(fake)
        assert t.get_declaration() == "int x"
        fake.getDeclaration.assert_called_once_with()

    def test_get_enumeration_literals_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Type")
        lit = make_fake_element("EnumerationLiteral", getName="RED")
        fake.getEnumerationLiterals.return_value = make_fake_collection([lit])
        t = RPType(fake)
        result = t.get_enumeration_literals()
        assert isinstance(result, RPCollection)
        fake.getEnumerationLiterals.assert_called_once_with()

    def test_get_is_predefined_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", getIsPredefined=True)
        t = RPType(fake)
        assert t.get_is_predefined() == 1

    def test_is_array_returns_int(self) -> None:
        # Pattern G — representative for all 16 is_* checks
        fake = make_fake_element("Type", isArray=True)
        t = RPType(fake)
        assert t.is_array() == 1

    def test_is_kind_typedef_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Type", isKindTypedef=True)
        t = RPType(fake)
        assert t.is_kind_typedef() == 1

    def test_set_kind_delegates(self) -> None:
        # Pattern D — representative for set_* str-arg setters
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_kind("Enumeration")
        fake.setKind.assert_called_once_with("Enumeration")

    def test_set_is_typedef_constant_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Type")
        t = RPType(fake)
        t.set_is_typedef_constant(1)
        fake.setIsTypedefConstant.assert_called_once_with(1)

    def test_set_typedef_base_type_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("Type")
        base = make_fake_element("Class", getName="Base")
        t = RPType(fake)
        t.set_typedef_base_type(RPClassifier(base))
        fake.setTypedefBaseType.assert_called_once_with(base)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_classifier_role.py tests/unit/models/elements/test_sysml_port.py tests/unit/models/elements/test_type.py -v`

Expected: FAIL — tests raise `NotImplementedError` for stubbed methods and `AssertionError` for `is_registered` (register_wrapper not yet added)

- [ ] **Step 3: Implement all 57 methods + register_wrapper**

Replace every `raise NotImplementedError` in `src/rhapsody_cli/models/elements/common/model_other_model.py` using Patterns A-G. Method-to-Pattern mapping:

For `RPClassifierRole` (7 methods — 8 list entries; `getFormalInstance` and `setFormalInstance` count separately):
- `get_formal_classifier` → Pattern B (wrap as `RPClassifier`)
- `get_formal_instance` → Pattern B (wrap as `RPInstance`)
- `get_referenced_sequence_diagram` → Pattern B (wrap as `RPSequenceDiagram`)
- `get_referencing_classifier_roles_recursively` → Pattern C
- `get_role_type` → Pattern A (return `str`)
- `set_formal_classifier` → Pattern F (single `RPClassifier` arg → `target._com`)
- `set_formal_instance` → Pattern F (single `RPInstance` arg → `target._com`)
- `set_referenced_sequence_diagram` → Pattern F (single `RPSequenceDiagram` arg → `target._com`)

For `RPSysMLPort` (7 methods):
- `add_link` → Pattern E (5 args; COM signature `addLink(fromPart._com, toPart._com, assoc._com, toPort._com, newOwner._com)`; wrap result as `RPLink`)
- `get_is_reversed` → Pattern G (return `int`)
- `get_port_direction` → Pattern A (return `str`)
- `get_type` → Pattern B (wrap as `RPClassifier`)
- `set_is_reversed` → Pattern D (int arg)
- `set_port_direction` → Pattern D (str arg)
- `set_type` → Pattern F (`RPClassifier` arg → `type_._com`)

For `RPType` (35 methods):
- `add_enumeration_literal` → Pattern E (1 str arg, wrap as `RPEnumerationLiteral`)
- `delete_enumeration_literal` → Pattern F (`RPEnumerationLiteral` arg → `literal._com`)
- `get_declaration` → Pattern A
- `get_enumeration_literals` → Pattern C
- `get_is_predefined`, `get_is_typedef`, `get_is_typedef_constant`, `get_is_typedef_ordered`, `get_is_typedef_reference` → Pattern G (return `int`)
- `get_kind` → Pattern A (return `str`)
- `get_typedef_base_type` → Pattern B (wrap as `RPClassifier`)
- `get_typedef_multiplicity` → Pattern A (return `str`)
- `is_array`, `is_enum`, `is_equal_to`, `is_implicit`, `is_kind_enumeration`, `is_kind_language`, `is_kind_struct`, `is_kind_typedef`, `is_kind_union`, `is_pointer`, `is_pointer_to_pointer`, `is_reference`, `is_reference_to_pointer`, `is_struct`, `is_template`, `is_union` → Pattern G (return `int`) — 16 methods all use identical pattern
- `set_declaration` → Pattern D (str arg)
- `set_is_typedef_constant`, `set_is_typedef_ordered`, `set_is_typedef_reference` → Pattern D (int arg)
- `set_kind` → Pattern D (str arg)
- `set_typedef_base_type` → Pattern F (`RPClassifier` arg → `typedef_base_type._com`)
- `set_typedef_multiplicity` → Pattern D (str arg)

Add at module level (bottom of file):
```python
AbstractRPModelElement.register_wrapper("ClassifierRole", RPClassifierRole)
AbstractRPModelElement.register_wrapper("SysMLPort", RPSysMLPort)
AbstractRPModelElement.register_wrapper("Type", RPType)
```

- [ ] **Step 4: Verify common `__init__.py`** — `RPClassifierRole`, `RPSysMLPort`, `RPType` are already exported (confirmed in `src/rhapsody_cli/models/elements/common/__init__.py`). No edit needed; just verify imports still resolve.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_classifier_role.py tests/unit/models/elements/test_sysml_port.py tests/unit/models/elements/test_type.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/common/model_other_model.py \
       tests/unit/models/elements/test_classifier_role.py \
       tests/unit/models/elements/test_sysml_port.py \
       tests/unit/models/elements/test_type.py
git commit -m "feat(common): implement RPClassifierRole, RPSysMLPort, RPType methods + register_wrapper"
```

---

### Task 4: Values — 5 classes, 15 methods (RPInstanceSlot, RPInstanceSpecification, etc.)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/values/model_values.py`
- Create: `tests/unit/models/elements/test_values.py`

**Registration packages needed:** `"InstanceSlot"`, `"InstanceSpecification"`, `"ValueSpecification"`, `"InstanceValue"`, `"LiteralSpecification"`

**Methods:**
- `RPInstanceSlot` (5): `addElementValue`, `addStringValue`, `getSlotProperty`, `getValues`, `setSlotProperty`
- `RPInstanceSpecification` (6): `addInstanceSlot`, `getClassifier`, `getInstanceSlots`, `isRootInstanceSpecification`, `populateSlots`, `setClassifier`
- `RPValueSpecification` (0): base interface — no methods to implement (the checklist shows `[inherited]` only)
- `RPInstanceValue` (2): `getValue`, `setValue`
- `RPLiteralSpecification` (2): `getValue`, `setValue`

**Import notes:** The file currently imports `from rhapsody_cli.models.core import RPModelElement` and uses `TYPE_CHECKING` for `RPCollection` and `RPClassifier`. Update the runtime import to `from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement`. The `TYPE_CHECKING` block already references `RPClassifier` — keep as-is. The classes `RPInstanceValue` and `RPLiteralSpecification` reference each other via forward-ref string hints (e.g. `"RPInstanceValue"` returned from `RPInstanceSlot.add_element_value`), which already works without runtime imports.

**Registration notes:** Add five `register_wrapper` calls at the bottom of `src/rhapsody_cli/models/elements/values/model_values.py` (after the `RPLiteralSpecification` class):

```python
AbstractRPModelElement.register_wrapper("InstanceSlot", RPInstanceSlot)
AbstractRPModelElement.register_wrapper("InstanceSpecification", RPInstanceSpecification)
AbstractRPModelElement.register_wrapper("ValueSpecification", RPValueSpecification)
AbstractRPModelElement.register_wrapper("InstanceValue", RPInstanceValue)
AbstractRPModelElement.register_wrapper("LiteralSpecification", RPLiteralSpecification)
```

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/values/__init__.py` exports all 5 classes. If not, add the missing imports and `__all__` entries.

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_values.py`:

```python
"""Tests for rhapsody_cli.models.elements.values.model_values classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.values import (
    RPInstanceSlot,
    RPInstanceSpecification,
    RPInstanceValue,
    RPLiteralSpecification,
    RPValueSpecification,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPInstanceSlot:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("InstanceSlot", getName="Slot1")
        slot = RPInstanceSlot(fake)
        assert isinstance(slot, RPModelElement)
        assert slot.get_name() == "Slot1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("InstanceSlot", getName="Slot1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInstanceSlot)

    def test_add_element_value_delegates_and_wraps(self) -> None:
        # Pattern E — single RPModelElement arg, returns RPInstanceValue
        fake = make_fake_element("InstanceSlot")
        val = make_fake_element("Class", getName="Cls1")
        result = make_fake_element("InstanceValue", getName="IV1")
        fake.addElementValue.return_value = result
        slot = RPInstanceSlot(fake)
        wrapped = slot.add_element_value(RPModelElement(val))
        assert wrapped.get_name() == "IV1"
        fake.addElementValue.assert_called_once_with(val)

    def test_add_string_value_delegates_and_wraps(self) -> None:
        # Pattern E — single str arg, returns RPLiteralSpecification
        fake = make_fake_element("InstanceSlot")
        result = make_fake_element("LiteralSpecification", getName="LS1")
        fake.addStringValue.return_value = result
        slot = RPInstanceSlot(fake)
        wrapped = slot.add_string_value("hello")
        assert wrapped.get_name() == "LS1"
        fake.addStringValue.assert_called_once_with("hello")

    def test_get_slot_property_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("InstanceSlot")
        prop = make_fake_element("Attribute", getName="attr1")
        fake.getSlotProperty.return_value = prop
        slot = RPInstanceSlot(fake)
        wrapped = slot.get_slot_property()
        assert wrapped.get_name() == "attr1"
        fake.getSlotProperty.assert_called_once_with()

    def test_get_values_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("InstanceSlot")
        v = make_fake_element("InstanceValue", getName="v1")
        fake.getValues.return_value = make_fake_collection([v])
        slot = RPInstanceSlot(fake)
        result = slot.get_values()
        assert isinstance(result, RPCollection)
        fake.getValues.assert_called_once_with()

    def test_set_slot_property_delegates(self) -> None:
        # Pattern F
        fake = make_fake_element("InstanceSlot")
        prop = make_fake_element("Attribute", getName="attr1")
        fake.setSlotProperty.return_value = None
        slot = RPInstanceSlot(fake)
        slot.set_slot_property(RPModelElement(prop))
        fake.setSlotProperty.assert_called_once_with(prop)


class TestRPInstanceSpecification:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("InstanceSpecification", getName="IS1")
        spec = RPInstanceSpecification(fake)
        assert isinstance(spec, RPModelElement)
        assert spec.get_name() == "IS1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("InstanceSpecification", getName="IS1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInstanceSpecification)

    def test_add_instance_slot_delegates_and_wraps(self) -> None:
        # Pattern E — str + RPModelElement args, returns RPInstanceSlot
        fake = make_fake_element("InstanceSpecification")
        prop = make_fake_element("Attribute", getName="attr1")
        slot = make_fake_element("InstanceSlot", getName="s1")
        fake.addInstanceSlot.return_value = slot
        spec = RPInstanceSpecification(fake)
        wrapped = spec.add_instance_slot("s1", RPModelElement(prop))
        assert wrapped.get_name() == "s1"
        fake.addInstanceSlot.assert_called_once_with("s1", prop)

    def test_get_classifier_wraps_result(self) -> None:
        # Pattern B — wraps as RPClassifier
        fake = make_fake_element("InstanceSpecification")
        clf = make_fake_element("Class", getName="C1")
        fake.getClassifier.return_value = clf
        spec = RPInstanceSpecification(fake)
        wrapped = spec.get_classifier()
        assert wrapped.get_name() == "C1"
        fake.getClassifier.assert_called_once_with()

    def test_get_instance_slots_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("InstanceSpecification")
        s = make_fake_element("InstanceSlot", getName="s1")
        fake.getInstanceSlots.return_value = make_fake_collection([s])
        spec = RPInstanceSpecification(fake)
        result = spec.get_instance_slots()
        assert isinstance(result, RPCollection)
        fake.getInstanceSlots.assert_called_once_with()

    def test_is_root_instance_specification_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("InstanceSpecification", isRootInstanceSpecification=True)
        spec = RPInstanceSpecification(fake)
        assert spec.is_root_instance_specification() == 1

    def test_populate_slots_delegates(self) -> None:
        # Pattern F — no-arg void method
        fake = make_fake_element("InstanceSpecification")
        fake.populateSlots.return_value = None
        spec = RPInstanceSpecification(fake)
        spec.populate_slots()
        fake.populateSlots.assert_called_once_with()

    def test_set_classifier_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("InstanceSpecification")
        clf = make_fake_element("Class", getName="C1")
        fake.setClassifier.return_value = None
        spec = RPInstanceSpecification(fake)
        spec.set_classifier(RPClassifier(clf))
        fake.setClassifier.assert_called_once_with(clf)


class TestRPInstanceValue:
    def test_is_registered(self) -> None:
        fake = make_fake_element("InstanceValue", getName="IV1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPInstanceValue)

    def test_get_value_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("InstanceValue")
        val = make_fake_element("Class", getName="C1")
        fake.getValue.return_value = val
        iv = RPInstanceValue(fake)
        wrapped = iv.get_value()
        assert wrapped.get_name() == "C1"
        fake.getValue.assert_called_once_with()

    def test_set_value_delegates(self) -> None:
        # Pattern F
        fake = make_fake_element("InstanceValue")
        val = make_fake_element("Class", getName="C1")
        fake.setValue.return_value = None
        iv = RPInstanceValue(fake)
        iv.set_value(RPModelElement(val))
        fake.setValue.assert_called_once_with(val)


class TestRPLiteralSpecification:
    def test_is_registered(self) -> None:
        fake = make_fake_element("LiteralSpecification", getName="LS1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPLiteralSpecification)

    def test_get_value_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("LiteralSpecification", getValue="hello")
        ls = RPLiteralSpecification(fake)
        assert ls.get_value() == "hello"
        fake.getValue.assert_called_once_with()

    def test_set_value_delegates(self) -> None:
        # Pattern D — single str arg
        fake = make_fake_element("LiteralSpecification")
        ls = RPLiteralSpecification(fake)
        ls.set_value("hello")
        fake.setValue.assert_called_once_with("hello")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_values.py -v`

Expected: FAIL — `NotImplementedError` from stubs; `is_registered` tests fail (no `register_wrapper` yet)

- [ ] **Step 3: Implement all 15 methods + register_wrapper**

Method-to-Pattern mapping:

For `RPInstanceSlot` (5 methods):
- `add_element_value` → Pattern E (single `RPModelElement` arg → `val._com`; wrap as `RPInstanceValue`)
- `add_string_value` → Pattern E (single str arg; wrap as `RPLiteralSpecification`)
- `get_slot_property` → Pattern B (wrap as `RPModelElement` via `AbstractRPModelElement.wrap(...)`)
- `get_values` → Pattern C
- `set_slot_property` → Pattern F (`RPModelElement` arg → `slot_property._com`)

For `RPInstanceSpecification` (6 methods):
- `add_instance_slot` → Pattern E (str + `RPModelElement` args; wrap as `RPInstanceSlot`)
- `get_classifier` → Pattern B (wrap as `RPClassifier`)
- `get_instance_slots` → Pattern C
- `is_root_instance_specification` → Pattern G (return `int`)
- `populate_slots` → Pattern F (no-arg void method: `self.call_com(lambda: self._com.populateSlots())`)
- `set_classifier` → Pattern F (`RPClassifier` arg → `classifier._com`)

For `RPValueSpecification` (0 methods): no-op — class body remains `pass`. Still needs `register_wrapper("ValueSpecification", RPValueSpecification)` so descendants resolve correctly via the registry fallback chain.

For `RPInstanceValue` (2 methods):
- `get_value` → Pattern B (wrap as `RPModelElement`)
- `set_value` → Pattern F (`RPModelElement` arg → `value._com`)

For `RPLiteralSpecification` (2 methods):
- `get_value` → Pattern A (return `str`; use `_get_method_or_property(self._com, "getValue", "value")`)
- `set_value` → Pattern D (single str arg)

Add at module level (bottom of file):
```python
AbstractRPModelElement.register_wrapper("InstanceSlot", RPInstanceSlot)
AbstractRPModelElement.register_wrapper("InstanceSpecification", RPInstanceSpecification)
AbstractRPModelElement.register_wrapper("ValueSpecification", RPValueSpecification)
AbstractRPModelElement.register_wrapper("InstanceValue", RPInstanceValue)
AbstractRPModelElement.register_wrapper("LiteralSpecification", RPLiteralSpecification)
```

- [ ] **Step 4: Verify/Update values `__init__.py`** — ensure all 5 classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_values.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/values/model_values.py \
       src/rhapsody_cli/models/elements/values/__init__.py \
       tests/unit/models/elements/test_values.py
git commit -m "feat(values): implement 5 value-specification classes + register_wrapper"
```

---

### Task 5: Templates — 3 classes, 10 methods

**Files:**
- Modify: `src/rhapsody_cli/models/elements/templates/model_templates.py`
- Create: `tests/unit/models/elements/test_templates.py`

**Registration packages needed:** `"TemplateInstantiation"`, `"TemplateInstantiationParameter"`, `"TemplateParameter"`

**Methods:**
- `RPTemplateInstantiation` (1): `getTemplateInstantiationParameters`
- `RPTemplateInstantiationParameter` (4): `getArgValue`, `getType`, `setArgValue`, `setType`
- `RPTemplateParameter` (5): `getParameterKind`, `getRepresentative`, `setClassType`, `setParameterKind`, `setRepresentative`

**Import notes:** The templates file imports `RPModelElement` and likely uses `TYPE_CHECKING` for `RPCollection` and `RPClassifier` (verify by reading the file). Update the runtime import to `from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement` (and `RPCollection` if it's a runtime import). The `RPTemplateInstantiationParameter.getType` returns `RPClassifier`; if `RPClassifier` is currently behind `TYPE_CHECKING`, keep it as a forward-ref string hint `"RPClassifier"` — runtime imports of classifiers into templates create a circular dependency.

**Registration notes:** Add three `register_wrapper` calls at the bottom of `src/rhapsody_cli/models/elements/templates/model_templates.py`:

```python
AbstractRPModelElement.register_wrapper("TemplateInstantiation", RPTemplateInstantiation)
AbstractRPModelElement.register_wrapper("TemplateInstantiationParameter", RPTemplateInstantiationParameter)
AbstractRPModelElement.register_wrapper("TemplateParameter", RPTemplateParameter)
```

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/templates/__init__.py` exports all 3 classes. Add imports / `__all__` entries if missing.

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_templates.py`:

```python
"""Tests for rhapsody_cli.models.elements.templates.model_templates classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.templates import (
    RPTemplateInstantiation,
    RPTemplateInstantiationParameter,
    RPTemplateParameter,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPTemplateInstantiation:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateInstantiation", getName="TI1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateInstantiation)

    def test_get_template_instantiation_parameters_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning RPCollection
        fake = make_fake_element("TemplateInstantiation")
        p = make_fake_element("TemplateInstantiationParameter", getName="p1")
        fake.getTemplateInstantiationParameters.return_value = make_fake_collection([p])
        ti = RPTemplateInstantiation(fake)
        result = ti.get_template_instantiation_parameters()
        assert isinstance(result, RPCollection)
        fake.getTemplateInstantiationParameters.assert_called_once_with()


class TestRPTemplateInstantiationParameter:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter", getName="p1")
        param = RPTemplateInstantiationParameter(fake)
        assert isinstance(param, RPModelElement)
        assert param.get_name() == "p1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateInstantiationParameter", getName="p1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateInstantiationParameter)

    def test_get_arg_value_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("TemplateInstantiationParameter", getArgValue="int")
        param = RPTemplateInstantiationParameter(fake)
        assert param.get_arg_value() == "int"
        fake.getArgValue.assert_called_once_with()

    def test_get_type_wraps_result(self) -> None:
        # Pattern B — wraps as RPClassifier
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateInstantiationParameter")
        clf = make_fake_element("Class", getName="C1")
        fake.getType.return_value = clf
        param = RPTemplateInstantiationParameter(fake)
        wrapped = param.get_type()
        assert wrapped.get_name() == "C1"
        fake.getType.assert_called_once_with()

    def test_set_arg_value_delegates(self) -> None:
        # Pattern D — single str arg
        fake = make_fake_element("TemplateInstantiationParameter")
        param = RPTemplateInstantiationParameter(fake)
        param.set_arg_value("int")
        fake.setArgValue.assert_called_once_with("int")

    def test_set_type_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateInstantiationParameter")
        clf = make_fake_element("Class", getName="C1")
        param = RPTemplateInstantiationParameter(fake)
        param.set_type(RPClassifier(clf))
        fake.setType.assert_called_once_with(clf)


class TestRPTemplateParameter:
    def test_is_registered(self) -> None:
        fake = make_fake_element("TemplateParameter", getName="tp1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTemplateParameter)

    def test_get_parameter_kind_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("TemplateParameter", getParameterKind="class")
        tp = RPTemplateParameter(fake)
        assert tp.get_parameter_kind() == "class"
        fake.getParameterKind.assert_called_once_with()

    def test_get_representative_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("TemplateParameter")
        rep = make_fake_element("Class", getName="C1")
        fake.getRepresentative.return_value = rep
        tp = RPTemplateParameter(fake)
        wrapped = tp.get_representative()
        assert wrapped.get_name() == "C1"
        fake.getRepresentative.assert_called_once_with()

    def test_set_parameter_kind_delegates(self) -> None:
        # Pattern D
        fake = make_fake_element("TemplateParameter")
        tp = RPTemplateParameter(fake)
        tp.set_parameter_kind("class")
        fake.setParameterKind.assert_called_once_with("class")

    def test_set_representative_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("TemplateParameter")
        rep = make_fake_element("Class", getName="C1")
        tp = RPTemplateParameter(fake)
        tp.set_representative(RPModelElement(rep))
        fake.setRepresentative.assert_called_once_with(rep)

    def test_set_class_type_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("TemplateParameter")
        clf = make_fake_element("Class", getName="C1")
        tp = RPTemplateParameter(fake)
        tp.set_class_type(RPClassifier(clf))
        fake.setClassType.assert_called_once_with(clf)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_templates.py -v`

Expected: FAIL

- [ ] **Step 3: Implement all 10 methods + register_wrapper**

Method-to-Pattern mapping:

For `RPTemplateInstantiation` (1 method):
- `get_template_instantiation_parameters` → Pattern C

For `RPTemplateInstantiationParameter` (4 methods):
- `get_arg_value` → Pattern A (return `str`)
- `get_type` → Pattern B (wrap as `RPClassifier`)
- `set_arg_value` → Pattern D (str arg)
- `set_type` → Pattern F (`RPClassifier` arg → `type_._com`)

For `RPTemplateParameter` (5 methods):
- `get_parameter_kind` → Pattern A (return `str`)
- `get_representative` → Pattern B (wrap as `RPModelElement`)
- `set_class_type` → Pattern F (`RPClassifier` arg → `class_type._com`)
- `set_parameter_kind` → Pattern D (str arg)
- `set_representative` → Pattern F (`RPModelElement` arg → `representative._com`)

Add at module level (bottom of file):
```python
AbstractRPModelElement.register_wrapper("TemplateInstantiation", RPTemplateInstantiation)
AbstractRPModelElement.register_wrapper("TemplateInstantiationParameter", RPTemplateInstantiationParameter)
AbstractRPModelElement.register_wrapper("TemplateParameter", RPTemplateParameter)
```

- [ ] **Step 4: Verify/Update templates `__init__.py`** — ensure all 3 classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_templates.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/templates/model_templates.py \
       src/rhapsody_cli/models/elements/templates/__init__.py \
       tests/unit/models/elements/test_templates.py
git commit -m "feat(templates): implement 3 template classes + register_wrapper"
```

---

### Task 6: Variables — Remaining (RPVariable, RPTag) — 14 methods

**Files:**
- Modify: `src/rhapsody_cli/models/elements/variables/model_variables.py`
- Create: `tests/unit/models/elements/test_variable.py` (if not exists, else expand)

**Registration packages needed:** `"Variable"`

**Methods:**
- `RPVariable` (6): `getIsConstant`, `getIsOrdered`, `getIsReference`, `setIsConstant`, `setIsOrdered`, `setIsReference`
- `RPTag` (7): `getBase`, `getFromProfile`, `getMultiplicity`, `getTagMetaClass`, `getValue`, `setMultiplicity`, `setTagMetaClass`, `setValue`

**Important clarification (read the source file first):** Inspect `src/rhapsody_cli/models/elements/variables/model_variables.py`. The 6 methods listed under `RPVariable` above are actually defined on `RPAttribute` (a subclass of `RPVariable`) — `RPVariable` itself has all `[x]` checklist items done. The `RPTag` class is also a subclass of `RPVariable` with the 7 unchecked methods (its body is currently `pass`). Implement the 6 methods on `RPAttribute` and the 7 methods on `RPTag`. The class `RPVariable` itself needs only the `register_wrapper("Variable", RPVariable)` call (no method changes).

**Import notes:** The file already imports `AbstractRPModelElement`, `RPCollection`, `RPModelElement`, `RPUnit` from `rhapsody_cli.models.core` at runtime, plus `RPClassifier` from classifiers at runtime, plus `TYPE_CHECKING` guards for `RPInstanceValue` and `RPLiteralSpecification`. No new imports needed.

**Registration notes:** `RPAttribute` is already registered (`register_wrapper("Attribute", RPAttribute)`) and `RPTag` is already registered (`register_wrapper("Tag", RPTag)`). Only **one** new registration call is needed — add it after the `RPVariable` class definition (before `RPAttribute`):

```python
AbstractRPModelElement.register_wrapper("Variable", RPVariable)
```

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/variables/__init__.py` exports `RPVariable`, `RPAttribute`, `RPTag`, `RPArgument` (all 4 classes). Add any missing imports / `__all__` entries.

- [ ] **Step 1: Write failing tests**

Expand `tests/unit/models/elements/test_variable.py` (it already exists). Add (or augment) the following test classes:

```python
"""Tests for rhapsody_cli.models.elements.variables.model_variables classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.variables import RPAttribute, RPTag, RPVariable
from tests.unit.models.fakes import make_fake_element


class TestRPVariable:
    def test_is_registered(self) -> None:
        # Currently fails — register_wrapper("Variable", RPVariable) not yet added
        fake = make_fake_element("Variable", getName="v1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPVariable)


class TestRPAttribute:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Attribute", getName="a1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAttribute)

    def test_get_is_constant_returns_int(self) -> None:
        # Pattern G — boolean check returning int (representative for getIsOrdered, getIsReference)
        fake = make_fake_element("Attribute", getIsConstant=True)
        attr = RPAttribute(fake)
        assert attr.get_is_constant() == 1
        fake.getIsConstant.assert_called_once_with()

    def test_get_is_ordered_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Attribute", getIsOrdered=True)
        attr = RPAttribute(fake)
        assert attr.get_is_ordered() == 1

    def test_get_is_reference_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Attribute", getIsReference=True)
        attr = RPAttribute(fake)
        assert attr.get_is_reference() == 1

    def test_set_is_constant_delegates(self) -> None:
        # Pattern D — int-arg setter (representative for setIsOrdered, setIsReference)
        fake = make_fake_element("Attribute")
        attr = RPAttribute(fake)
        attr.set_is_constant(1)
        fake.setIsConstant.assert_called_once_with(1)

    def test_set_is_ordered_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Attribute")
        attr = RPAttribute(fake)
        attr.set_is_ordered(1)
        fake.setIsOrdered.assert_called_once_with(1)

    def test_set_is_reference_delegates(self) -> None:
        # Pattern D — int-arg setter
        fake = make_fake_element("Attribute")
        attr = RPAttribute(fake)
        attr.set_is_reference(1)
        fake.setIsReference.assert_called_once_with(1)


class TestRPTag:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Tag", getName="t1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTag)

    def test_get_base_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("Tag", getBase="base_val")
        tag = RPTag(fake)
        assert tag.get_base() == "base_val"
        fake.getBase.assert_called_once_with()

    def test_get_from_profile_returns_int(self) -> None:
        # Pattern G — boolean check returning int
        fake = make_fake_element("Tag", getFromProfile=True)
        tag = RPTag(fake)
        assert tag.get_from_profile() == 1

    def test_get_multiplicity_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Tag", getMultiplicity="0..*")
        tag = RPTag(fake)
        assert tag.get_multiplicity() == "0..*"
        fake.getMultiplicity.assert_called_once_with()

    def test_get_tag_meta_class_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Tag", getTagMetaClass="Class")
        tag = RPTag(fake)
        assert tag.get_tag_meta_class() == "Class"
        fake.getTagMetaClass.assert_called_once_with()

    def test_get_value_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Tag", getValue="v1")
        tag = RPTag(fake)
        assert tag.get_value() == "v1"
        fake.getValue.assert_called_once_with()

    def test_set_multiplicity_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Tag")
        tag = RPTag(fake)
        tag.set_multiplicity("0..*")
        fake.setMultiplicity.assert_called_once_with("0..*")

    def test_set_tag_meta_class_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Tag")
        tag = RPTag(fake)
        tag.set_tag_meta_class("Class")
        fake.setTagMetaClass.assert_called_once_with("Class")

    def test_set_value_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Tag")
        tag = RPTag(fake)
        tag.set_value("v1")
        fake.setValue.assert_called_once_with("v1")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_variable.py -v`

Expected: FAIL — `AttributeError` on `RPAttribute.get_is_constant` etc. (methods not yet defined on the `pass`-bodied class), `AssertionError` on `TestRPVariable.test_is_registered`

- [ ] **Step 3: Implement all 13 methods + register_wrapper**

Method-to-Pattern mapping:

For `RPAttribute` (6 methods — these are the "RPVariable remaining" methods from the plan; `RPVariable` itself needs no method changes):
- `get_is_constant` → Pattern G (return `int`)
- `get_is_ordered` → Pattern G (return `int`)
- `get_is_reference` → Pattern G (return `int`)
- `set_is_constant` → Pattern D (int arg)
- `set_is_ordered` → Pattern D (int arg)
- `set_is_reference` → Pattern D (int arg)

For `RPTag` (7 methods — currently `pass` body, all need to be added):
- `get_base` → Pattern A (return `str`)
- `get_from_profile` → Pattern G (return `int`)
- `get_multiplicity` → Pattern A (return `str`)
- `get_tag_meta_class` → Pattern A (return `str`)
- `get_value` → Pattern A (return `str`)
- `set_multiplicity` → Pattern D (str arg)
- `set_tag_meta_class` → Pattern D (str arg)
- `set_value` → Pattern D (str arg)

Add `register_wrapper("Variable", RPVariable)` after the `RPVariable` class definition. The existing `register_wrapper("Attribute", RPAttribute)`, `register_wrapper("Tag", RPTag)`, and `register_wrapper("Argument", RPArgument)` calls are already present and must be preserved.

- [ ] **Step 4: Verify/Update variables `__init__.py`** — ensure `RPVariable`, `RPAttribute`, `RPTag`, `RPArgument` are all exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_variable.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/variables/model_variables.py \
       src/rhapsody_cli/models/elements/variables/__init__.py \
       tests/unit/models/elements/test_variable.py
git commit -m "feat(variables): implement RPAttribute and RPTag methods + register Variable"
```

---

### Task 7: Activity — Actions (7 classes, 22 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/activity/model_actions.py`
- Create: `tests/unit/models/elements/test_actions.py`

**Registration packages needed:** `"AcceptEventAction"`, `"AcceptTimeEvent"`, `"Action"`, `"ActionBlock"`, `"CallOperation"`, `"ContextSpecification"`, `"SendAction"`

**Methods:**
- `RPAcceptEventAction` (2): `getEvent`, `setEvent`
- `RPAcceptTimeEvent` (2): `getDurationTime`, `setDurationTime`
- `RPAction` (2): `getBody`, `setBody`
- `RPCallOperation` (4): `getOperation`, `getTarget`, `setOperation`, `setTarget`
- `RPContextSpecification` (4): `getMultiplicities`, `getValue`, `setMultiplicities`, `setValue`
- `RPSendAction` (8): `addArgumentValue`, `getArgVals`, `getEvent`, `getInvokedOperation`, `getTarget`, `setEvent`, `setInvokedOperation`, `setTarget`

**Import notes:** Read `src/rhapsody_cli/models/elements/activity/model_actions.py` first. The file imports `RPModelElement` from core; update the runtime import to `from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement`. Use `TYPE_CHECKING` guards (or string forward refs) for `RPEvent`, `RPOperation`, `RPInstance` — these live in interactions / classifiers / relations subpackages and would cause circular imports if imported at runtime. `RPCollection` is not needed here (no method returns a collection).

**Registration notes:** Add seven `register_wrapper` calls at the bottom of `src/rhapsody_cli/models/elements/activity/model_actions.py`:

```python
AbstractRPModelElement.register_wrapper("AcceptEventAction", RPAcceptEventAction)
AbstractRPModelElement.register_wrapper("AcceptTimeEvent", RPAcceptTimeEvent)
AbstractRPModelElement.register_wrapper("Action", RPAction)
AbstractRPModelElement.register_wrapper("ActionBlock", RPActionBlock)
AbstractRPModelElement.register_wrapper("CallOperation", RPCallOperation)
AbstractRPModelElement.register_wrapper("ContextSpecification", RPContextSpecification)
AbstractRPModelElement.register_wrapper("SendAction", RPSendAction)
```

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/activity/__init__.py` exports all 7 classes (`RPAcceptEventAction`, `RPAcceptTimeEvent`, `RPAction`, `RPActionBlock`, `RPCallOperation`, `RPContextSpecification`, `RPSendAction`). Add imports / `__all__` entries if missing.

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_actions.py`:

```python
"""Tests for rhapsody_cli.models.elements.activity.model_actions classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.activity import (
    RPAcceptEventAction,
    RPAcceptTimeEvent,
    RPAction,
    RPCallOperation,
    RPContextSpecification,
    RPSendAction,
)
from tests.unit.models.fakes import make_fake_element


class TestRPCallOperation:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("CallOperation", getName="co1")
        co = RPCallOperation(fake)
        assert isinstance(co, RPModelElement)
        assert co.get_name() == "co1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("CallOperation", getName="co1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPCallOperation)

    def test_get_operation_wraps_result(self) -> None:
        # Pattern B — wraps as RPOperation
        fake = make_fake_element("CallOperation")
        op = make_fake_element("Operation", getName="op1")
        fake.getOperation.return_value = op
        co = RPCallOperation(fake)
        wrapped = co.get_operation()
        assert wrapped.get_name() == "op1"
        fake.getOperation.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        # Pattern B — wraps as RPModelElement (target instance)
        fake = make_fake_element("CallOperation")
        target = make_fake_element("Instance", getName="tgt1")
        fake.getTarget.return_value = target
        co = RPCallOperation(fake)
        wrapped = co.get_target()
        assert wrapped.get_name() == "tgt1"
        fake.getTarget.assert_called_once_with()

    def test_set_operation_delegates(self) -> None:
        # Pattern F — RPOperation arg
        from rhapsody_cli.models.elements.classifiers import RPOperation
        fake = make_fake_element("CallOperation")
        op = make_fake_element("Operation", getName="op1")
        co = RPCallOperation(fake)
        co.set_operation(RPOperation(op))
        fake.setOperation.assert_called_once_with(op)

    def test_set_target_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("CallOperation")
        target = make_fake_element("Instance", getName="tgt1")
        co = RPCallOperation(fake)
        co.set_target(RPModelElement(target))
        fake.setTarget.assert_called_once_with(target)


class TestRPSendAction:
    def test_is_model_element(self) -> None:
        fake = make_fake_element("SendAction", getName="sa1")
        sa = RPSendAction(fake)
        assert isinstance(sa, RPModelElement)
        assert sa.get_name() == "sa1"

    def test_is_registered(self) -> None:
        fake = make_fake_element("SendAction", getName="sa1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSendAction)

    def test_add_argument_value_delegates(self) -> None:
        # Pattern F — multi-arg void method (str, str args)
        fake = make_fake_element("SendAction")
        sa = RPSendAction(fake)
        sa.add_argument_value("x", "5")
        fake.addArgumentValue.assert_called_once_with("x", "5")

    def test_get_arg_vals_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("SendAction", getArgVals="x=5")
        sa = RPSendAction(fake)
        assert sa.get_arg_vals() == "x=5"
        fake.getArgVals.assert_called_once_with()

    def test_get_event_wraps_result(self) -> None:
        # Pattern B — wraps as RPEvent
        from rhapsody_cli.models.elements.interactions import RPEvent
        fake = make_fake_element("SendAction")
        ev = make_fake_element("Event", getName="ev1")
        fake.getEvent.return_value = ev
        sa = RPSendAction(fake)
        wrapped = sa.get_event()
        assert wrapped.get_name() == "ev1"
        fake.getEvent.assert_called_once_with()

    def test_get_invoked_operation_wraps_result(self) -> None:
        # Pattern B — wraps as RPOperation
        from rhapsody_cli.models.elements.classifiers import RPOperation
        fake = make_fake_element("SendAction")
        op = make_fake_element("Operation", getName="op1")
        fake.getInvokedOperation.return_value = op
        sa = RPSendAction(fake)
        wrapped = sa.get_invoked_operation()
        assert wrapped.get_name() == "op1"
        fake.getInvokedOperation.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("SendAction")
        target = make_fake_element("Instance", getName="tgt1")
        fake.getTarget.return_value = target
        sa = RPSendAction(fake)
        wrapped = sa.get_target()
        assert wrapped.get_name() == "tgt1"
        fake.getTarget.assert_called_once_with()

    def test_set_event_delegates(self) -> None:
        # Pattern F — RPEvent arg
        from rhapsody_cli.models.elements.interactions import RPEvent
        fake = make_fake_element("SendAction")
        ev = make_fake_element("Event", getName="ev1")
        sa = RPSendAction(fake)
        sa.set_event(RPEvent(ev))
        fake.setEvent.assert_called_once_with(ev)

    def test_set_invoked_operation_delegates(self) -> None:
        # Pattern F — RPOperation arg
        from rhapsody_cli.models.elements.classifiers import RPOperation
        fake = make_fake_element("SendAction")
        op = make_fake_element("Operation", getName="op1")
        sa = RPSendAction(fake)
        sa.set_invoked_operation(RPOperation(op))
        fake.setInvokedOperation.assert_called_once_with(op)

    def test_set_target_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("SendAction")
        target = make_fake_element("Instance", getName="tgt1")
        sa = RPSendAction(fake)
        sa.set_target(RPModelElement(target))
        fake.setTarget.assert_called_once_with(target)


class TestRPAcceptEventAction:
    def test_is_registered(self) -> None:
        fake = make_fake_element("AcceptEventAction", getName="a1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAcceptEventAction)

    def test_get_event_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.interactions import RPEvent
        fake = make_fake_element("AcceptEventAction")
        ev = make_fake_element("Event", getName="ev1")
        fake.getEvent.return_value = ev
        a = RPAcceptEventAction(fake)
        wrapped = a.get_event()
        assert wrapped.get_name() == "ev1"


class TestRPAcceptTimeEvent:
    def test_is_registered(self) -> None:
        fake = make_fake_element("AcceptTimeEvent", getName="at1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAcceptTimeEvent)

    def test_get_duration_time_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("AcceptTimeEvent", getDurationTime="100ms")
        a = RPAcceptTimeEvent(fake)
        assert a.get_duration_time() == "100ms"


class TestRPAction:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Action", getName="act1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPAction)

    def test_get_body_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Action", getBody="body code")
        a = RPAction(fake)
        assert a.get_body() == "body code"

    def test_set_body_delegates(self) -> None:
        # Pattern D
        fake = make_fake_element("Action")
        a = RPAction(fake)
        a.set_body("body code")
        fake.setBody.assert_called_once_with("body code")


class TestRPContextSpecification:
    def test_is_registered(self) -> None:
        fake = make_fake_element("ContextSpecification", getName="cs1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPContextSpecification)

    def test_get_multiplicities_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("ContextSpecification", getMultiplicities="1")
        cs = RPContextSpecification(fake)
        assert cs.get_multiplicities() == "1"

    def test_get_value_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("ContextSpecification")
        val = make_fake_element("Class", getName="v1")
        fake.getValue.return_value = val
        cs = RPContextSpecification(fake)
        wrapped = cs.get_value()
        assert wrapped.get_name() == "v1"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_actions.py -v`

Expected: FAIL

- [ ] **Step 3: Implement all 22 methods + register_wrapper**

Method-to-Pattern mapping:

For `RPAcceptEventAction` (2 methods):
- `get_event` → Pattern B (wrap as `RPEvent`)
- `set_event` → Pattern F (`RPEvent` arg → `event._com`)

For `RPAcceptTimeEvent` (2 methods):
- `get_duration_time` → Pattern A (return `str`)
- `set_duration_time` → Pattern D (str arg)

For `RPAction` (2 methods):
- `get_body` → Pattern A (return `str`)
- `set_body` → Pattern D (str arg)

For `RPCallOperation` (4 methods):
- `get_operation` → Pattern B (wrap as `RPOperation`)
- `get_target` → Pattern B (wrap as `RPModelElement`)
- `set_operation` → Pattern F (`RPOperation` arg → `operation._com`)
- `set_target` → Pattern F (`RPModelElement` arg → `target._com`)

For `RPContextSpecification` (4 methods):
- `get_multiplicities` → Pattern A (return `str`)
- `get_value` → Pattern B (wrap as `RPModelElement`)
- `set_multiplicities` → Pattern D (str arg)
- `set_value` → Pattern F (`RPModelElement` arg → `value._com`)

For `RPSendAction` (8 methods):
- `add_argument_value` → Pattern F (2 str args; `self.call_com(lambda: self._com.addArgumentValue(name, value))`)
- `get_arg_vals` → Pattern A (return `str`)
- `get_event` → Pattern B (wrap as `RPEvent`)
- `get_invoked_operation` → Pattern B (wrap as `RPOperation`)
- `get_target` → Pattern B (wrap as `RPModelElement`)
- `set_event` → Pattern F (`RPEvent` arg → `event._com`)
- `set_invoked_operation` → Pattern F (`RPOperation` arg → `invoked_operation._com`)
- `set_target` → Pattern F (`RPModelElement` arg → `target._com`)

For `RPActionBlock` (0 methods): no-op — class body remains `pass`. Still needs `register_wrapper("ActionBlock", RPActionBlock)`.

Add all seven `register_wrapper` calls (see Registration notes above) at module level (bottom of file).

- [ ] **Step 4: Verify/Update activity `__init__.py`** — ensure all 7 classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_actions.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/activity/model_actions.py \
       src/rhapsody_cli/models/elements/activity/__init__.py \
       tests/unit/models/elements/test_actions.py
git commit -m "feat(activity): implement 7 action classes + register_wrapper"
```

---

### Task 8: Activity — Flowchart (5 classes, 46 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/activity/model_activity.py`
- Create: `tests/unit/models/elements/test_activity.py` (or split into test_flow.py, test_flowchart.py, test_flowitem.py, test_objectnode.py, test_swimlane.py)

**Registration packages needed:** `"Flow"`, `"FlowItem"`, `"Flowchart"`, `"ObjectNode"`, `"Swimlane"`

**Methods:**
- `RPFlow` (17): `addConveyed`, `getConveyed`, `getDirection`, `getEnd1`, `getEnd1Port`, `getEnd1SysMLPort`, `getEnd2`, `getEnd2Port`, `getEnd2SysMLPort`, `removeConveyed`, `setDirection`, `setEnd1`, `setEnd1ViaPort`, `setEnd1ViaSysMLPort`, `setEnd2`, `setEnd2ViaPort`, `setEnd2ViaSysMLPort`
- `RPFlowItem` (3): `addRepresented`, `getRepresented`, `removeRepresented`
- `RPFlowchart` (15): `addAcceptEventAction`, `addAcceptTimeEvent`, `addActivityParameter`, `addCallBehavior`, `addCallOperation`, `addObjectNode`, `addReferenceActivity`, `addSwimlane`, `getFlowchartDiagram`, `getIsAnalysisOnly`, `getItsOwner`, `getSwimlanes`, `setIsAnalysisOnly`, `setItsOwner`
- `RPObjectNode` (7): `addInState`, `getInState`, `getInStateList`, `getRepresents`, `removeInState`, `setInState`, `setRepresents`
- `RPSwimlane` (4): `addSwimlane`, `getContents`, `getRepresents`, `getSwimlanes`, `setRepresents`

**Import notes:** Read `src/rhapsody_cli/models/elements/activity/model_activity.py` first. Update runtime imports to include `AbstractRPModelElement`, `RPCollection` (e.g. `from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement, RPUnit` — keep whatever base classes are already imported). Use `TYPE_CHECKING` guards for cross-package references: `RPAcceptEventAction`, `RPAcceptTimeEvent`, `RPCallOperation`, `RPObjectNode`, `RPSwimlane` (these live in the same `model_actions` / `model_activity` modules), `RPSysMLPort` (common), `RPDiagram` (diagrams), `RPModelElement`/`RPInstance` (relations). Many of these may already be in the `TYPE_CHECKING` block — verify before adding.

**Registration notes:** Add five `register_wrapper` calls at the bottom of `src/rhapsody_cli/models/elements/activity/model_activity.py`:

```python
AbstractRPModelElement.register_wrapper("Flow", RPFlow)
AbstractRPModelElement.register_wrapper("FlowItem", RPFlowItem)
AbstractRPModelElement.register_wrapper("Flowchart", RPFlowchart)
AbstractRPModelElement.register_wrapper("ObjectNode", RPObjectNode)
AbstractRPModelElement.register_wrapper("Swimlane", RPSwimlane)
```

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/activity/__init__.py` exports all 5 classes plus the 7 classes from `model_actions.py` (Task 7). Add imports / `__all__` entries if missing. The `__init__.py` must import `model_actions` and `model_activity` submodules so the `register_wrapper` calls execute.

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_activity.py` (or split per the file list — a single file is simpler for the subagent):

```python
"""Tests for rhapsody_cli.models.elements.activity.model_activity classes."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.activity import (
    RPFlow,
    RPFlowchart,
    RPFlowItem,
    RPObjectNode,
    RPSwimlane,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPFlow:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Flow", getName="f1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlow)

    def test_get_direction_returns_string(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("Flow", getDirection="in")
        flow = RPFlow(fake)
        assert flow.get_direction() == "in"
        fake.getDirection.assert_called_once_with()

    def test_get_end1_wraps_result(self) -> None:
        # Pattern B — representative for getEnd1/2/Port/SysMLPort family
        fake = make_fake_element("Flow")
        end = make_fake_element("Instance", getName="e1")
        fake.getEnd1.return_value = end
        flow = RPFlow(fake)
        wrapped = flow.get_end1()
        assert wrapped.get_name() == "e1"
        fake.getEnd1.assert_called_once_with()

    def test_get_conveyed_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Flow")
        c = make_fake_element("Class", getName="c1")
        fake.getConveyed.return_value = make_fake_collection([c])
        flow = RPFlow(fake)
        result = flow.get_conveyed()
        assert isinstance(result, RPCollection)
        fake.getConveyed.assert_called_once_with()

    def test_add_conveyed_delegates(self) -> None:
        # Pattern F — RPModelElement arg, void
        fake = make_fake_element("Flow")
        c = make_fake_element("Class", getName="c1")
        fake.addConveyed.return_value = None
        flow = RPFlow(fake)
        flow.add_conveyed(RPModelElement(c))
        fake.addConveyed.assert_called_once_with(c)

    def test_remove_conveyed_delegates(self) -> None:
        # Pattern F — RPModelElement arg, void
        fake = make_fake_element("Flow")
        c = make_fake_element("Class", getName="c1")
        fake.removeConveyed.return_value = None
        flow = RPFlow(fake)
        flow.remove_conveyed(RPModelElement(c))
        fake.removeConveyed.assert_called_once_with(c)

    def test_set_direction_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Flow")
        flow = RPFlow(fake)
        flow.set_direction("out")
        fake.setDirection.assert_called_once_with("out")

    def test_set_end1_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("Flow")
        end = make_fake_element("Instance", getName="e1")
        flow = RPFlow(fake)
        flow.set_end1(RPModelElement(end))
        fake.setEnd1.assert_called_once_with(end)

    def test_set_end1_via_port_delegates(self) -> None:
        # Pattern F — 2 RPModelElement args
        fake = make_fake_element("Flow")
        end = make_fake_element("Instance", getName="e1")
        port = make_fake_element("Port", getName="p1")
        flow = RPFlow(fake)
        flow.set_end1_via_port(RPModelElement(end), RPModelElement(port))
        fake.setEnd1ViaPort.assert_called_once_with(end, port)


class TestRPFlowchart:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Flowchart", getName="fc1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlowchart)

    def test_add_swimlane_delegates_and_wraps(self) -> None:
        # Pattern E — str name arg, returns RPSwimlane
        fake = make_fake_element("Flowchart")
        sw = make_fake_element("Swimlane", getName="Lane1")
        fake.addSwimlane.return_value = sw
        fc = RPFlowchart(fake)
        wrapped = fc.add_swimlane("Lane1")
        assert wrapped.get_name() == "Lane1"
        fake.addSwimlane.assert_called_once_with("Lane1")

    def test_add_call_operation_delegates_and_wraps(self) -> None:
        # Pattern E — representative for add*Action / add*Node family
        from rhapsody_cli.models.elements.activity import RPCallOperation
        fake = make_fake_element("Flowchart")
        co = make_fake_element("CallOperation", getName="co1")
        fake.addCallOperation.return_value = co
        fc = RPFlowchart(fake)
        wrapped = fc.add_call_operation("co1")
        assert wrapped.get_name() == "co1"
        fake.addCallOperation.assert_called_once_with("co1")

    def test_add_object_node_delegates_and_wraps(self) -> None:
        # Pattern E
        fake = make_fake_element("Flowchart")
        on = make_fake_element("ObjectNode", getName="on1")
        fake.addObjectNode.return_value = on
        fc = RPFlowchart(fake)
        wrapped = fc.add_object_node("on1")
        assert wrapped.get_name() == "on1"
        fake.addObjectNode.assert_called_once_with("on1")

    def test_get_flowchart_diagram_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.diagrams import RPDiagram
        fake = make_fake_element("Flowchart")
        diag = make_fake_element("ActivityDiagram", getName="d1")
        fake.getFlowchartDiagram.return_value = diag
        fc = RPFlowchart(fake)
        wrapped = fc.get_flowchart_diagram()
        assert wrapped.get_name() == "d1"
        fake.getFlowchartDiagram.assert_called_once_with()

    def test_get_is_analysis_only_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Flowchart", getIsAnalysisOnly=True)
        fc = RPFlowchart(fake)
        assert fc.get_is_analysis_only() == 1

    def test_get_its_owner_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("Flowchart")
        owner = make_fake_element("Class", getName="Owner1")
        fake.getItsOwner.return_value = owner
        fc = RPFlowchart(fake)
        wrapped = fc.get_its_owner()
        assert wrapped.get_name() == "Owner1"
        fake.getItsOwner.assert_called_once_with()

    def test_get_swimlanes_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Flowchart")
        sw = make_fake_element("Swimlane", getName="Lane1")
        fake.getSwimlanes.return_value = make_fake_collection([sw])
        fc = RPFlowchart(fake)
        result = fc.get_swimlanes()
        assert isinstance(result, RPCollection)
        fake.getSwimlanes.assert_called_once_with()

    def test_set_is_analysis_only_delegates(self) -> None:
        # Pattern D — int arg
        fake = make_fake_element("Flowchart")
        fc = RPFlowchart(fake)
        fc.set_is_analysis_only(1)
        fake.setIsAnalysisOnly.assert_called_once_with(1)

    def test_set_its_owner_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("Flowchart")
        owner = make_fake_element("Class", getName="Owner1")
        fc = RPFlowchart(fake)
        fc.set_its_owner(RPModelElement(owner))
        fake.setItsOwner.assert_called_once_with(owner)


class TestRPFlowItem:
    def test_is_registered(self) -> None:
        fake = make_fake_element("FlowItem", getName="fi1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPFlowItem)

    def test_add_represented_delegates(self) -> None:
        # Pattern F
        fake = make_fake_element("FlowItem")
        rep = make_fake_element("Class", getName="rep1")
        fake.addRepresented.return_value = None
        fi = RPFlowItem(fake)
        fi.add_represented(RPModelElement(rep))
        fake.addRepresented.assert_called_once_with(rep)

    def test_get_represented_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("FlowItem")
        rep = make_fake_element("Class", getName="rep1")
        fake.getRepresented.return_value = rep
        fi = RPFlowItem(fake)
        wrapped = fi.get_represented()
        assert wrapped.get_name() == "rep1"


class TestRPObjectNode:
    def test_is_registered(self) -> None:
        fake = make_fake_element("ObjectNode", getName="on1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPObjectNode)

    def test_add_in_state_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("ObjectNode")
        st = make_fake_element("State", getName="s1")
        fake.addInState.return_value = None
        on = RPObjectNode(fake)
        on.add_in_state(RPModelElement(st))
        fake.addInState.assert_called_once_with(st)

    def test_get_represents_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("ObjectNode")
        rep = make_fake_element("Class", getName="rep1")
        fake.getRepresents.return_value = rep
        on = RPObjectNode(fake)
        wrapped = on.get_represents()
        assert wrapped.get_name() == "rep1"


class TestRPSwimlane:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Swimlane", getName="Lane1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSwimlane)

    def test_add_swimlane_delegates_and_wraps(self) -> None:
        # Pattern E — str arg, returns RPSwimlane
        fake = make_fake_element("Swimlane")
        sub = make_fake_element("Swimlane", getName="Sub1")
        fake.addSwimlane.return_value = sub
        sw = RPSwimlane(fake)
        wrapped = sw.add_swimlane("Sub1")
        assert wrapped.get_name() == "Sub1"

    def test_get_swimlanes_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Swimlane")
        sub = make_fake_element("Swimlane", getName="Sub1")
        fake.getSwimlanes.return_value = make_fake_collection([sub])
        sw = RPSwimlane(fake)
        result = sw.get_swimlanes()
        assert isinstance(result, RPCollection)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_activity.py -v`

Expected: FAIL

- [ ] **Step 3: Implement all 46 methods + register_wrapper**

Method-to-Pattern mapping:

For `RPFlow` (17 methods):
- `add_conveyed` → Pattern F (`RPModelElement` arg → `conveyed._com`)
- `get_conveyed` → Pattern C
- `get_direction` → Pattern A (return `str`)
- `get_end1`, `get_end2` → Pattern B (wrap as `RPModelElement`)
- `get_end1_port`, `get_end2_port` → Pattern B (wrap as `RPModelElement` — Rhapsody returns `IRPPort` which is a kind of `IRPInstance`/`IRPModelElement`)
- `get_end1_sysml_port`, `get_end2_sysml_port` → Pattern B (wrap as `RPSysMLPort` if a typed wrapper is desired; `RPModelElement` via `wrap()` is acceptable since the registry will resolve to `RPSysMLPort` if `"SysMLPort"` is the metaclass)
- `remove_conveyed` → Pattern F (`RPModelElement` arg → `conveyed._com`)
- `set_direction` → Pattern D (str arg)
- `set_end1`, `set_end2` → Pattern F (`RPModelElement` arg → `end._com`)
- `set_end1_via_port`, `set_end2_via_port` → Pattern F (2 args: `end._com, port._com`)
- `set_end1_via_sysml_port`, `set_end2_via_sysml_port` → Pattern F (2 args: `end._com, sysml_port._com`)

For `RPFlowItem` (3 methods):
- `add_represented` → Pattern F (`RPModelElement` arg → `represented._com`)
- `get_represented` → Pattern B (wrap as `RPModelElement`)
- `remove_represented` → Pattern F (`RPModelElement` arg → `represented._com`)

For `RPFlowchart` (15 methods):
- `add_accept_event_action` → Pattern E (str name arg; wrap as `RPAcceptEventAction`)
- `add_accept_time_event` → Pattern E (str name arg; wrap as `RPAcceptTimeEvent`)
- `add_activity_parameter` → Pattern E
- `add_call_behavior` → Pattern E
- `add_call_operation` → Pattern E (wrap as `RPCallOperation`)
- `add_object_node` → Pattern E (wrap as `RPObjectNode`)
- `add_reference_activity` → Pattern E
- `add_swimlane` → Pattern E (str name arg; wrap as `RPSwimlane`)
- `get_flowchart_diagram` → Pattern B (wrap as `RPDiagram`)
- `get_is_analysis_only` → Pattern G (return `int`)
- `get_its_owner` → Pattern B (wrap as `RPModelElement`)
- `get_swimlanes` → Pattern C
- `set_is_analysis_only` → Pattern D (int arg)
- `set_its_owner` → Pattern F (`RPModelElement` arg → `owner._com`)

For `RPObjectNode` (7 methods):
- `add_in_state` → Pattern F (`RPModelElement` arg → `state._com`)
- `get_in_state` → Pattern B (wrap as `RPModelElement` — state)
- `get_in_state_list` → Pattern C (collection of states)
- `get_represents` → Pattern B (wrap as `RPModelElement`)
- `remove_in_state` → Pattern F (`RPModelElement` arg → `state._com`)
- `set_in_state` → Pattern F (`RPModelElement` arg → `state._com`)
- `set_represents` → Pattern F (`RPModelElement` arg → `represents._com`)

For `RPSwimlane` (5 methods — note list says 4 but lists 5):
- `add_swimlane` → Pattern E (str name arg; wrap as `RPSwimlane`)
- `get_contents` → Pattern C (collection)
- `get_represents` → Pattern B (wrap as `RPModelElement`)
- `get_swimlanes` → Pattern C
- `set_represents` → Pattern F (`RPModelElement` arg → `represents._com`)

Add all five `register_wrapper` calls (see Registration notes above) at module level (bottom of file).

- [ ] **Step 4: Verify/Update activity `__init__.py`** — ensure all 5 classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_activity.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/activity/model_activity.py \
       src/rhapsody_cli/models/elements/activity/__init__.py \
       tests/unit/models/elements/test_activity.py
git commit -m "feat(activity): implement 5 flowchart classes + register_wrapper"
```

---

### Task 9: Classifiers — Remaining Unchecked (5 classes, ~64 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_operation.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_statechart.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_stereotype.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_usecase.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_association_class.py`
- Modify: `src/rhapsody_cli/models/elements/classifiers/model_interface_item.py`
- Expand existing test files: `test_operation.py`, `test_statechart.py`, `test_stereotype.py`, `test_usecase.py`, `test_association_class.py`

**Registration packages needed:** `"InterfaceItem"` (RPInterfaceItem — class exists, just needs the `register_wrapper` call)

**Methods — RPOperation (20):** `deleteArgument`, `deleteFlowchart`, `getFlowchart`, `getImplementationSignature`, `getInitializer`, `getIsCgDerived`, `getIsConst`, `getIsCtor`, `getIsDtor`, `getIsFinal`, `getIsInline`, `getIsTrigger`, `getVisibility`, `setBody`, `setFlowchart`, `setInitializer`, `setIsConst`, `setIsFinal`, `setVisibility`, `updateContainedDiagramsOnServer`

**Methods — RPStatechart (27):** `addFreeShapeByType`, `addImage`, `addNewEdgeByType`, `addNewEdgeForElement`, `addNewNodeForElement`, `addTextBox`, `openDiagramView`, `addNewAcceptEventAction`, `addNewAcceptTimeEvent`, `getAllTriggers`, `getElementsInDiagram`, `getGraphicalElements`, `getInheritsFrom`, `getIsMainBehavior`, `getIsOverridden`, `getItsClass`, `getPicture`, `getPictureAs`, `getPictureAsDividedMetafiles`, `getPicturesWithImageMap`, `getRootState`, `getStatechartDiagram`, `overrideInheritance`, `populateDiagram`, `setAsMainBehavior`, `setShowDiagramFrame`, `unoverrideInheritance`

**Methods — RPStereotype (6):** `addMetaClass`, `getIcon`, `getIsNewTerm`, `getOfMetaClass`, `removeMetaClass`, `setIsNewTerm`

**Methods — RPUseCase (11):** `addDescribingDiagram`, `addEventReceptionWithEvent`, `deleteDescribingDiagram`, `deleteEntryPoint`, `deleteExtensionPoint`, `findEntryPoint`, `findExtensionPoint`, `getDescribingDiagram`, `getIsBehaviorOverriden`, `setIsBehaviorOverriden`, `updateContainedDiagramsOnServer`

**Methods — RPAssociationClass (4):** `getEnd1`, `getEnd2`, `getIsClass`, `setIsClass`

**Methods — RPInterfaceItem (0):** class exists, only needs `register_wrapper("InterfaceItem", RPInterfaceItem)`.

**Import notes:** Each of the 5 modified files in `src/rhapsody_cli/models/elements/classifiers/` already imports `RPModelElement` (and possibly `RPClassifier` as base). For each file, update the runtime import to include `AbstractRPModelElement`, `RPCollection` if any method needs them. Use `TYPE_CHECKING` guards for cross-classifier references (`RPFlowchart`, `RPState`, `RPDiagram`, `RPGraphElement`, `RPEvent`, `RPStereotype`) — these would create circular imports if imported at runtime. The `classifiers/__init__.py` already imports all 13 classifiers (per Task 0's planned `__init__.py` content), so registration of `RPInterfaceItem` will be picked up automatically once `model_interface_item.py` is imported.

**Registration notes:** Only **one** new `register_wrapper` call is needed across these 5 files. Add it at the bottom of `src/rhapsody_cli/models/elements/classifiers/model_interface_item.py`:

```python
AbstractRPModelElement.register_wrapper("InterfaceItem", RPInterfaceItem)
```

The other 5 classes (`RPOperation`, `RPStatechart`, `RPStereotype`, `RPUseCase`, `RPAssociationClass`) should already have `register_wrapper` calls — verify by reading each file. If any are missing, add the corresponding call (e.g. `AbstractRPModelElement.register_wrapper("Operation", RPOperation)` for `RPOperation`).

- [ ] **Step 1: Write failing tests**

Expand the existing test files (`tests/unit/models/elements/test_operation.py`, `test_statechart.py`, `test_stereotype.py`, `test_usecase.py`, `test_association_class.py`). Representative tests for the two largest classes:

Add to `tests/unit/models/elements/test_operation.py`:
```python
"""Tests for RPOperation — additional methods from Task 9."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPOperation
from tests.unit.models.fakes import make_fake_element


class TestRPOperationTask9:
    def test_get_is_const_returns_int(self) -> None:
        # Pattern G — representative for getIsCgDerived, getIsCtor, getIsDtor,
        # getIsFinal, getIsInline, getIsTrigger
        fake = make_fake_element("Operation", getIsConst=True)
        op = RPOperation(fake)
        assert op.get_is_const() == 1
        fake.getIsConst.assert_called_once_with()

    def test_get_visibility_returns_string(self) -> None:
        # Pattern A — representative for getImplementationSignature, getInitializer
        fake = make_fake_element("Operation", getVisibility="public")
        op = RPOperation(fake)
        assert op.get_visibility() == "public"
        fake.getVisibility.assert_called_once_with()

    def test_get_flowchart_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.activity import RPFlowchart
        fake = make_fake_element("Operation")
        fc = make_fake_element("Flowchart", getName="fc1")
        fake.getFlowchart.return_value = fc
        op = RPOperation(fake)
        wrapped = op.get_flowchart()
        assert wrapped.get_name() == "fc1"
        fake.getFlowchart.assert_called_once_with()

    def test_set_body_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Operation")
        op = RPOperation(fake)
        op.set_body("body code")
        fake.setBody.assert_called_once_with("body code")

    def test_set_is_const_delegates(self) -> None:
        # Pattern D — int arg (representative for setIsFinal)
        fake = make_fake_element("Operation")
        op = RPOperation(fake)
        op.set_is_const(1)
        fake.setIsConst.assert_called_once_with(1)

    def test_set_flowchart_delegates(self) -> None:
        # Pattern F — RPFlowchart arg
        from rhapsody_cli.models.elements.activity import RPFlowchart
        fake = make_fake_element("Operation")
        fc = make_fake_element("Flowchart", getName="fc1")
        op = RPOperation(fake)
        op.set_flowchart(RPFlowchart(fc))
        fake.setFlowchart.assert_called_once_with(fc)

    def test_delete_argument_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        from rhapsody_cli.models.elements.variables import RPArgument
        fake = make_fake_element("Operation")
        arg = make_fake_element("Argument", getName="a1")
        op = RPOperation(fake)
        op.delete_argument(RPArgument(arg))
        fake.deleteArgument.assert_called_once_with(arg)

    def test_update_contained_diagrams_on_server_delegates(self) -> None:
        # Pattern F — no-arg void method
        fake = make_fake_element("Operation")
        op = RPOperation(fake)
        op.update_contained_diagrams_on_server()
        fake.updateContainedDiagramsOnServer.assert_called_once_with()
```

Add to `tests/unit/models/elements/test_statechart.py`:
```python
"""Tests for RPStatechart — additional methods from Task 9."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPStatechart
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPStatechartTask9:
    def test_get_is_main_behavior_returns_int(self) -> None:
        # Pattern G — representative for getIsOverridden
        fake = make_fake_element("Statechart", getIsMainBehavior=True)
        sc = RPStatechart(fake)
        assert sc.get_is_main_behavior() == 1
        fake.getIsMainBehavior.assert_called_once_with()

    def test_get_its_class_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Statechart")
        cls = make_fake_element("Class", getName="C1")
        fake.getItsClass.return_value = cls
        sc = RPStatechart(fake)
        wrapped = sc.get_its_class()
        assert wrapped.get_name() == "C1"
        fake.getItsClass.assert_called_once_with()

    def test_get_root_state_wraps_result(self) -> None:
        # Pattern B — returns RPState
        from rhapsody_cli.models.elements.statemachine import RPState
        fake = make_fake_element("Statechart")
        root = make_fake_element("State", getName="ROOT")
        fake.getRootState.return_value = root
        sc = RPStatechart(fake)
        wrapped = sc.get_root_state()
        assert wrapped.get_name() == "ROOT"
        fake.getRootState.assert_called_once_with()

    def test_get_statechart_diagram_wraps_result(self) -> None:
        # Pattern B — returns RPDiagram
        from rhapsody_cli.models.elements.diagrams import RPDiagram
        fake = make_fake_element("Statechart")
        diag = make_fake_element("StatechartDiagram", getName="d1")
        fake.getStatechartDiagram.return_value = diag
        sc = RPStatechart(fake)
        wrapped = sc.get_statechart_diagram()
        assert wrapped.get_name() == "d1"
        fake.getStatechartDiagram.assert_called_once_with()

    def test_get_all_triggers_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Statechart")
        tr = make_fake_element("Trigger", getName="t1")
        fake.getAllTriggers.return_value = make_fake_collection([tr])
        sc = RPStatechart(fake)
        result = sc.get_all_triggers()
        assert isinstance(result, RPCollection)
        fake.getAllTriggers.assert_called_once_with()

    def test_get_graphical_elements_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Statechart")
        ge = make_fake_element("GraphElement", getName="ge1")
        fake.getGraphicalElements.return_value = make_fake_collection([ge])
        sc = RPStatechart(fake)
        result = sc.get_graphical_elements()
        assert isinstance(result, RPCollection)
        fake.getGraphicalElements.assert_called_once_with()

    def test_add_new_accept_event_action_delegates_and_wraps(self) -> None:
        # Pattern E — representative for addNewAcceptTimeEvent, addNewEdgeByType,
        # addNewNodeForElement, addTextBox, addFreeShapeByType
        from rhapsody_cli.models.elements.activity import RPAcceptEventAction
        fake = make_fake_element("Statechart")
        aea = make_fake_element("AcceptEventAction", getName="a1")
        fake.addNewAcceptEventAction.return_value = aea
        sc = RPStatechart(fake)
        wrapped = sc.add_new_accept_event_action("a1")
        assert wrapped.get_name() == "a1"
        fake.addNewAcceptEventAction.assert_called_once_with("a1")

    def test_set_show_diagram_frame_delegates(self) -> None:
        # Pattern D — int arg
        fake = make_fake_element("Statechart")
        sc = RPStatechart(fake)
        sc.set_show_diagram_frame(1)
        fake.setShowDiagramFrame.assert_called_once_with(1)

    def test_override_inheritance_delegates(self) -> None:
        # Pattern F — no-arg void (representative for unoverrideInheritance, populateDiagram)
        fake = make_fake_element("Statechart")
        sc = RPStatechart(fake)
        sc.override_inheritance()
        fake.overrideInheritance.assert_called_once_with()
```

For `RPStereotype`, `RPUseCase`, `RPAssociationClass` — follow the same test structure (2+ representative tests per class). Examples:
- `RPStereotype.test_add_meta_class_delegates_and_wraps` (Pattern E)
- `RPStereotype.test_get_is_new_term_returns_int` (Pattern G)
- `RPUseCase.test_find_entry_point_wraps_result` (Pattern B — returns wrapped element or None)
- `RPUseCase.test_add_describing_diagram_delegates_and_wraps` (Pattern E)
- `RPAssociationClass.test_get_end1_wraps_result` (Pattern B)
- `RPAssociationClass.test_get_is_class_returns_int` (Pattern G)

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_operation.py tests/unit/models/elements/test_statechart.py tests/unit/models/elements/test_stereotype.py tests/unit/models/elements/test_usecase.py tests/unit/models/elements/test_association_class.py -v`

Expected: FAIL — `NotImplementedError` for stubbed methods

- [ ] **Step 3: Implement all ~64 methods + register_wrapper for RPInterfaceItem**

Method-to-Pattern mapping (representative; full list in `**Methods —**` headers above):

For `RPOperation` (20 methods):
- `delete_argument`, `delete_flowchart` → Pattern F (`RPModelElement` arg → `arg._com`)
- `get_flowchart` → Pattern B (wrap as `RPFlowchart`)
- `get_implementation_signature`, `get_initializer`, `get_visibility` → Pattern A (return `str`)
- `get_is_cg_derived`, `get_is_const`, `get_is_ctor`, `get_is_dtor`, `get_is_final`, `get_is_inline`, `get_is_trigger` → Pattern G (return `int`) — 7 methods, identical pattern
- `set_body`, `set_initializer`, `set_visibility` → Pattern D (str arg)
- `set_flowchart` → Pattern F (`RPFlowchart` arg → `flowchart._com`)
- `set_is_const`, `set_is_final` → Pattern D (int arg)
- `update_contained_diagrams_on_server` → Pattern F (no-arg void)

For `RPStatechart` (27 methods):
- `add_free_shape_by_type`, `add_image`, `add_new_edge_by_type`, `add_new_edge_for_element`, `add_new_node_for_element`, `add_text_box`, `open_diagram_view`, `add_new_accept_event_action`, `add_new_accept_time_event` → Pattern E (varies by signature; see the existing stub for arg count) — 9 methods
- `get_all_triggers`, `get_elements_in_diagram`, `get_graphical_elements`, `get_pictures_with_image_map` → Pattern C — 4 methods
- `get_inherits_from`, `get_its_class`, `get_root_state`, `get_statechart_diagram` → Pattern B — wrap in the appropriate typed wrapper
- `get_is_main_behavior`, `get_is_overridden` → Pattern G (return `int`)
- `get_picture`, `get_picture_as`, `get_picture_as_divided_metafiles` → **special** — these return binary/image data. Pattern A works if the COM call returns bytes; otherwise use `call_com` directly and return the raw object. Verify by reading the existing stub's docstring.
- `override_inheritance`, `populate_diagram`, `set_as_main_behavior`, `unoverride_inheritance` → Pattern F (no-arg void, except `set_as_main_behavior` may take a bool/int arg)
- `set_show_diagram_frame` → Pattern D (int arg)

For `RPStereotype` (6 methods):
- `add_meta_class`, `remove_meta_class` → Pattern F (str arg → COM directly; or `RPModelElement` arg if API takes element)
- `get_icon` → Pattern A or special (returns binary)
- `get_is_new_term` → Pattern G (return `int`)
- `get_of_meta_class` → Pattern C (collection of meta-class strings) — verify by reading the stub
- `set_is_new_term` → Pattern D (int arg)

For `RPUseCase` (11 methods):
- `add_describing_diagram` → Pattern E (wrap as `RPDiagram`)
- `add_event_reception_with_event` → Pattern E (multi-arg; wrap as `RPEventReception`)
- `delete_describing_diagram`, `delete_entry_point`, `delete_extension_point` → Pattern F (`RPModelElement` arg → `target._com`)
- `find_entry_point`, `find_extension_point` → Pattern B (str name arg → `call_com(lambda: self._com.findEntryPoint(name))`; wrap result or return `None` if not found)
- `get_describing_diagram` → Pattern B (wrap as `RPDiagram`)
- `get_is_behavior_overriden` → Pattern G (return `int`)
- `set_is_behavior_overriden` → Pattern D (int arg)
- `update_contained_diagrams_on_server` → Pattern F (no-arg void)

For `RPAssociationClass` (4 methods):
- `get_end1`, `get_end2` → Pattern B (wrap as `RPModelElement` — these are relation ends)
- `get_is_class` → Pattern G (return `int`)
- `set_is_class` → Pattern D (int arg)

For `RPInterfaceItem` (0 methods): no-op — class body remains `pass`. Add `register_wrapper("InterfaceItem", RPInterfaceItem)` at the bottom of `model_interface_item.py`.

- [ ] **Step 4: Verify `classifiers/__init__.py`** — already exports all 13 classes per Task 0. Just verify imports still resolve.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_operation.py tests/unit/models/elements/test_statechart.py tests/unit/models/elements/test_stereotype.py tests/unit/models/elements/test_usecase.py tests/unit/models/elements/test_association_class.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/classifiers/model_operation.py \
       src/rhapsody_cli/models/elements/classifiers/model_statechart.py \
       src/rhapsody_cli/models/elements/classifiers/model_stereotype.py \
       src/rhapsody_cli/models/elements/classifiers/model_usecase.py \
       src/rhapsody_cli/models/elements/classifiers/model_association_class.py \
       src/rhapsody_cli/models/elements/classifiers/model_interface_item.py \
       tests/unit/models/elements/test_operation.py \
       tests/unit/models/elements/test_statechart.py \
       tests/unit/models/elements/test_stereotype.py \
       tests/unit/models/elements/test_usecase.py \
       tests/unit/models/elements/test_association_class.py
git commit -m "feat(classifiers): implement remaining classifier methods + register InterfaceItem"
```

---

### Task 10: Relations — Remaining Unchecked (5 classes, ~25 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/relations/model_relation.py`
- Modify: `src/rhapsody_cli/models/elements/relations/model_dependency.py`
- Modify: `src/rhapsody_cli/models/elements/relations/model_generalization.py`
- Modify: `src/rhapsody_cli/models/elements/relations/model_hyperlink.py`
- Modify: `src/rhapsody_cli/models/elements/relations/model_association_role.py`
- Expand existing test files

**Registration packages needed:** `"Relation"` (for `RPRelation` — class exists, just needs the `register_wrapper` call)

**Methods — RPRelation:** (none unchecked — class exists but not registered)

**Methods — RPDependency (7):** `getDependent`, `getDependsOn`, `isNeedToMigrate`, `setDependent`, `setDependsOn`, `setLinkType`, `setOwnerWithoutChangingDependent`

**Methods — RPGeneralization (10):** `getBaseClass`, `getDerivedClass`, `getExtensionPoint`, `getIsVirtual`, `getVisibility`, `setBaseClass`, `setDerivedClass`, `setExtensionPoint`, `setIsVirtual`, `setVisibility`

**Methods — RPHyperLink (5):** `getTarget`, `getURL`, `setDisplayOption`, `setTarget`, `setURL`

**Methods — RPAssociationRole (3):** `getClassifierRoles`, `getFormalRelations`, `getRoleType`

**Import notes:** Each modified file in `src/rhapsody_cli/models/elements/relations/` already imports `RPModelElement` (or `RPUnit`/`RPInstance` as base). For each file, update the runtime import to include `AbstractRPModelElement`, `RPCollection` if any method needs them. Use `TYPE_CHECKING` guards for `RPClassifier` (classifiers) and `RPModelElement` references — these would create circular imports if imported at runtime.

**Registration notes:** Only **one** new `register_wrapper` call is needed. Add it at the bottom of `src/rhapsody_cli/models/elements/relations/model_relation.py`:

```python
AbstractRPModelElement.register_wrapper("Relation", RPRelation)
```

The other 4 classes (`RPDependency`, `RPGeneralization`, `RPHyperLink`, `RPAssociationRole`) should already have `register_wrapper` calls — verify by reading each file. If any are missing, add the corresponding call (e.g. `AbstractRPModelElement.register_wrapper("Dependency", RPDependency)`).

**`__init__.py` note:** Verify `src/rhapsody_cli/models/elements/relations/__init__.py` exports all relevant classes (`RPRelation`, `RPDependency`, `RPGeneralization`, `RPHyperLink`, `RPAssociationRole`, `RPInstance`, etc.).

- [ ] **Step 1: Write failing tests**

Expand the existing test files (`tests/unit/models/elements/test_dependency.py`, `test_generalization.py`, `test_hyperlink.py`, `test_association_role.py`, `test_relation.py`). Representative tests for the two largest classes:

Add to `tests/unit/models/elements/test_dependency.py`:
```python
"""Tests for RPDependency — methods from Task 10."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.relations import RPDependency
from tests.unit.models.fakes import make_fake_element


class TestRPDependencyTask10:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Dependency", getName="d1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPDependency)

    def test_get_dependent_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("Dependency")
        dep = make_fake_element("Class", getName="Dep1")
        fake.getDependent.return_value = dep
        d = RPDependency(fake)
        wrapped = d.get_dependent()
        assert wrapped.get_name() == "Dep1"
        fake.getDependent.assert_called_once_with()

    def test_get_depends_on_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("Dependency")
        supplier = make_fake_element("Class", getName="Sup1")
        fake.getDependsOn.return_value = supplier
        d = RPDependency(fake)
        wrapped = d.get_depends_on()
        assert wrapped.get_name() == "Sup1"
        fake.getDependsOn.assert_called_once_with()

    def test_is_need_to_migrate_returns_int(self) -> None:
        # Pattern G — boolean check returning int
        fake = make_fake_element("Dependency", isNeedToMigrate=True)
        d = RPDependency(fake)
        assert d.is_need_to_migrate() == 1
        fake.isNeedToMigrate.assert_called_once_with()

    def test_set_dependent_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("Dependency")
        dep = make_fake_element("Class", getName="Dep1")
        d = RPDependency(fake)
        d.set_dependent(RPModelElement(dep))
        fake.setDependent.assert_called_once_with(dep)

    def test_set_depends_on_delegates(self) -> None:
        # Pattern F
        fake = make_fake_element("Dependency")
        supplier = make_fake_element("Class", getName="Sup1")
        d = RPDependency(fake)
        d.set_depends_on(RPModelElement(supplier))
        fake.setDependsOn.assert_called_once_with(supplier)

    def test_set_link_type_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Dependency")
        d = RPDependency(fake)
        d.set_link_type("abstraction")
        fake.setLinkType.assert_called_once_with("abstraction")

    def test_set_owner_without_changing_dependent_delegates(self) -> None:
        # Pattern F — RPModelElement arg
        fake = make_fake_element("Dependency")
        owner = make_fake_element("Package", getName="pkg1")
        d = RPDependency(fake)
        d.set_owner_without_changing_dependent(RPModelElement(owner))
        fake.setOwnerWithoutChangingDependent.assert_called_once_with(owner)
```

Add to `tests/unit/models/elements/test_generalization.py`:
```python
"""Tests for RPGeneralization — methods from Task 10."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.relations import RPGeneralization
from tests.unit.models.fakes import make_fake_element


class TestRPGeneralizationTask10:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Generalization", getName="g1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGeneralization)

    def test_get_base_class_wraps_result(self) -> None:
        # Pattern B — wraps as RPClassifier
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("Generalization")
        base = make_fake_element("Class", getName="Base")
        fake.getBaseClass.return_value = base
        g = RPGeneralization(fake)
        wrapped = g.get_base_class()
        assert wrapped.get_name() == "Base"
        fake.getBaseClass.assert_called_once_with()

    def test_get_derived_class_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("Generalization")
        derived = make_fake_element("Class", getName="Derived")
        fake.getDerivedClass.return_value = derived
        g = RPGeneralization(fake)
        wrapped = g.get_derived_class()
        assert wrapped.get_name() == "Derived"
        fake.getDerivedClass.assert_called_once_with()

    def test_get_extension_point_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("Generalization")
        ep = make_fake_element("ExtensionPoint", getName="ep1")
        fake.getExtensionPoint.return_value = ep
        g = RPGeneralization(fake)
        wrapped = g.get_extension_point()
        assert wrapped.get_name() == "ep1"
        fake.getExtensionPoint.assert_called_once_with()

    def test_get_is_virtual_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("Generalization", getIsVirtual=True)
        g = RPGeneralization(fake)
        assert g.get_is_virtual() == 1
        fake.getIsVirtual.assert_called_once_with()

    def test_get_visibility_returns_string(self) -> None:
        # Pattern A
        fake = make_fake_element("Generalization", getVisibility="public")
        g = RPGeneralization(fake)
        assert g.get_visibility() == "public"
        fake.getVisibility.assert_called_once_with()

    def test_set_base_class_delegates(self) -> None:
        # Pattern F — RPClassifier arg
        from rhapsody_cli.models.elements.classifiers import RPClassifier
        fake = make_fake_element("Generalization")
        base = make_fake_element("Class", getName="Base")
        g = RPGeneralization(fake)
        g.set_base_class(RPClassifier(base))
        fake.setBaseClass.assert_called_once_with(base)

    def test_set_visibility_delegates(self) -> None:
        # Pattern D — str arg
        fake = make_fake_element("Generalization")
        g = RPGeneralization(fake)
        g.set_visibility("private")
        fake.setVisibility.assert_called_once_with("private")

    def test_set_is_virtual_delegates(self) -> None:
        # Pattern D — int arg
        fake = make_fake_element("Generalization")
        g = RPGeneralization(fake)
        g.set_is_virtual(1)
        fake.setIsVirtual.assert_called_once_with(1)
```

For `RPHyperLink`, `RPAssociationRole` — follow the same test structure (2+ representative tests per class).

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_dependency.py tests/unit/models/elements/test_generalization.py tests/unit/models/elements/test_hyperlink.py tests/unit/models/elements/test_association_role.py -v`

Expected: FAIL — `NotImplementedError` for stubbed methods

- [ ] **Step 3: Implement all 25 methods + register_wrapper for RPRelation**

Method-to-Pattern mapping:

For `RPDependency` (7 methods):
- `get_dependent`, `get_depends_on` → Pattern B (wrap as `RPModelElement`)
- `is_need_to_migrate` → Pattern G (return `int`)
- `set_dependent`, `set_depends_on`, `set_owner_without_changing_dependent` → Pattern F (`RPModelElement` arg → `target._com`)
- `set_link_type` → Pattern D (str arg)

For `RPGeneralization` (10 methods):
- `get_base_class`, `get_derived_class` → Pattern B (wrap as `RPClassifier`)
- `get_extension_point` → Pattern B (wrap as `RPModelElement`)
- `get_is_virtual` → Pattern G (return `int`)
- `get_visibility` → Pattern A (return `str`)
- `set_base_class`, `set_derived_class` → Pattern F (`RPClassifier` arg → `target._com`)
- `set_extension_point` → Pattern F (`RPModelElement` arg → `target._com`)
- `set_is_virtual` → Pattern D (int arg)
- `set_visibility` → Pattern D (str arg)

For `RPHyperLink` (5 methods):
- `get_target` → Pattern B (wrap as `RPModelElement`)
- `get_url` → Pattern A (return `str`)
- `set_display_option` → Pattern D (str arg — verify by reading the stub)
- `set_target` → Pattern F (`RPModelElement` arg → `target._com`)
- `set_url` → Pattern D (str arg)

For `RPAssociationRole` (3 methods):
- `get_classifier_roles` → Pattern C (collection of `RPClassifierRole`)
- `get_formal_relations` → Pattern C (collection of `RPRelation`)
- `get_role_type` → Pattern B (wrap as `RPClassifier`)

For `RPRelation` (0 methods): no-op — class body remains as-is. Add `register_wrapper("Relation", RPRelation)` at the bottom of `model_relation.py`.

- [ ] **Step 4: Verify `relations/__init__.py`** — ensure all relation classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_dependency.py tests/unit/models/elements/test_generalization.py tests/unit/models/elements/test_hyperlink.py tests/unit/models/elements/test_association_role.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/relations/model_relation.py \
       src/rhapsody_cli/models/elements/relations/model_dependency.py \
       src/rhapsody_cli/models/elements/relations/model_generalization.py \
       src/rhapsody_cli/models/elements/relations/model_hyperlink.py \
       src/rhapsody_cli/models/elements/relations/model_association_role.py \
       tests/unit/models/elements/test_dependency.py \
       tests/unit/models/elements/test_generalization.py \
       tests/unit/models/elements/test_hyperlink.py \
       tests/unit/models/elements/test_association_role.py
git commit -m "feat(relations): implement remaining relation methods + register Relation"
```

---

### Task 11: Containment — Package + Project (153 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/containment/model_package.py` (~92 unchecked items)
- Modify: `src/rhapsody_cli/models/elements/containment/model_project.py` (~61 unchecked items)
- Expand existing test files: `test_package.py`, `test_project.py`

**Notable methods — RPPackage:** `addEvent`, `addFlowItems`, `addFlows`, `addGlobalObject`, `addGlobalVariable`, `addInstanceSpecification`, `addLink`, `addLinkBetweenSYSMLPorts`, `addModule`, `addNode`, `addSequenceDiagram`, `addStatechart`, `addTimingDiagram`, `addType`, `deleteActor`, `deleteClass`, `deleteEvent`, `deleteNode`, `deleteUseCase`, `findActor`, `findClass`, `findEvent`, `findType`, `findUseCase`, `getEvents`, `getFlows`, `getModules`, `getNodes`, `getTypes`, plus all the remaining `set*`, `add*`, `get*` methods from the checklist.

**Notable methods — RPProject (61):** `gatewayExportToXML`, `gatewayExportToXML2`, `generateReport`, `addComponent`, `addProfile`, `allowAutoSave`, `allowNonUniqueNames`, `findElementByBinaryID`, `findElementByFileName`, `getAllStereotypes`, `getProfiles`, `getRequirementsByID`, `saveAs`, `saveAsPrevVersion`, and all remaining `add*`, `get*`, `set*`, `remove*` methods.

**Critical implementation note:** These methods need to be **CREATED from scratch** — they are NOT `raise NotImplementedError` stubs to replace. The containment files (`model_package.py`, `model_project.py`) have checklist items at the top of each class showing `[ ] methodName` for every unchecked method, but the method bodies do not exist (unlike Tasks 1-10 where stubs exist). You must add the `def` block + implementation following the Pattern rules.

**Import notes:** Both files import `AbstractRPModelElement`, `RPCollection`, `RPModelElement`, `RPUnit` at runtime already (verify by reading the file header). Use `TYPE_CHECKING` guards for any cross-package typed returns (`RPClass`, `RPActor`, `RPUseCase`, `RPEvent`, `RPModule`, `RPNode`, `RPType`, `RPFlow`, `RPDiagram`, `RPComponent`, `RPProfile`, `RPStereotype`, etc.). Many of these may already be in the `TYPE_CHECKING` block — verify before adding. Keep the existing imports intact.

**Registration notes:** `RPPackage` and `RPProject` should already have `register_wrapper("Package", RPPackage)` and `register_wrapper("Project", RPProject)` calls. Verify by reading the file. If missing, add them at the bottom of each respective file.

**Pattern mapping for the 4 method families (this is the core guidance for this task):**
- **`add*` methods** (e.g. `addEvent`, `addModule`, `addNode`, `addType`, `addSequenceDiagram`, `addStatechart`, `addTimingDiagram`, `addInstanceSpecification`, `addLink`, `addLinkBetweenSYSMLPorts`, `addFlowItems`, `addFlows`, `addGlobalObject`, `addGlobalVariable`, `addProfile`, `addComponent`) → **Pattern E** (multi-arg method returning wrapped element). The COM `addXxx(name)` returns the new element which should be wrapped via `AbstractRPModelElement.wrap(self.call_com(lambda: self._com.addXxx(name)))`. For methods taking more than just a name (e.g. `addLinkBetweenSYSMLPorts(fromPart, toPart, ...)`), pass each `RPModelElement` arg as `arg._com`.
- **`delete*` methods** (e.g. `deleteActor`, `deleteClass`, `deleteEvent`, `deleteNode`, `deleteUseCase`) → **Pattern F** (multi-arg void method). Implementation: `self.call_com(lambda: self._com.deleteXxx(target._com))`.
- **`find*` methods** (e.g. `findActor`, `findClass`, `findEvent`, `findType`, `findUseCase`, `findElementByBinaryID`, `findElementByFileName`) → **Pattern B** (return wrapped element or `None`). Implementation: `return AbstractRPModelElement.wrap(self.call_com(lambda: self._com.findXxx(name)))`. If the COM call returns `None` (not found), `wrap(None)` should return `None` — verify this behavior by reading `AbstractRPModelElement.wrap` in `src/rhapsody_cli/models/core.py` (if it doesn't handle `None`, add an early `result = self.call_com(...); return AbstractRPModelElement.wrap(result) if result is not None else None`).
- **`get*` methods returning collections** (e.g. `getEvents`, `getFlows`, `getModules`, `getNodes`, `getTypes`, `getProfiles`, `getAllStereotypes`) → **Pattern C**. Implementation: `return RPCollection(self.call_com(lambda: self._com.getXxxs()))` (or via `_get_method_or_property(self._com, "getXxxs", "xxxs")`).
- **`get*` methods returning primitives** (e.g. `getRequirementsByID`) → **Pattern A** if returning `str`, else inspect the stub.
- **`set*` methods** (single str/int arg) → **Pattern D**.
- **`set*` methods taking `RPModelElement`** → **Pattern F**.
- **`allow*` methods** (e.g. `allowAutoSave`, `allowNonUniqueNames`) → **Pattern F** (single bool/int arg → `self.call_com(lambda: self._com.allowXxx(1 if value else 0))`).
- **`save*` methods** (e.g. `saveAs`, `saveAsPrevVersion`) → **Pattern F** (str path arg → `self.call_com(lambda: self._com.saveAs(path))`).
- **`gateway*` / `generate*` methods** → **Pattern F** (multi-arg void) — verify arg count from the stub's docstring.

- [ ] **Step 1: Write failing tests**

Expand the existing `tests/unit/models/elements/test_package.py` and `test_project.py`. Representative tests below — each remaining method follows the same Pattern as the representative shown.

Add to `tests/unit/models/elements/test_package.py`:
```python
"""Tests for RPPackage — additional methods from Task 11."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment import RPPackage
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPPackageTask11:
    def test_add_event_delegates_and_wraps(self) -> None:
        # Pattern E — add* family (representative for addModule, addNode, addType,
        # addSequenceDiagram, addStatechart, addTimingDiagram, addInstanceSpecification)
        from rhapsody_cli.models.elements.interactions import RPEvent
        fake = make_fake_element("Package")
        ev = make_fake_element("Event", getName="ev1")
        fake.addEvent.return_value = ev
        pkg = RPPackage(fake)
        wrapped = pkg.add_event("ev1")
        assert wrapped.get_name() == "ev1"
        fake.addEvent.assert_called_once_with("ev1")

    def test_add_module_delegates_and_wraps(self) -> None:
        # Pattern E
        fake = make_fake_element("Package")
        mod = make_fake_element("Module", getName="m1")
        fake.addModule.return_value = mod
        pkg = RPPackage(fake)
        wrapped = pkg.add_module("m1")
        assert wrapped.get_name() == "m1"
        fake.addModule.assert_called_once_with("m1")

    def test_add_node_delegates_and_wraps(self) -> None:
        # Pattern E
        fake = make_fake_element("Package")
        node = make_fake_element("Node", getName="n1")
        fake.addNode.return_value = node
        pkg = RPPackage(fake)
        wrapped = pkg.add_node("n1")
        assert wrapped.get_name() == "n1"
        fake.addNode.assert_called_once_with("n1")

    def test_delete_class_delegates(self) -> None:
        # Pattern F — delete* family (representative for deleteActor, deleteEvent,
        # deleteNode, deleteUseCase)
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Package")
        cls = make_fake_element("Class", getName="C1")
        fake.deleteClass.return_value = None
        pkg = RPPackage(fake)
        pkg.delete_class(RPClass(cls))
        fake.deleteClass.assert_called_once_with(cls)

    def test_find_class_wraps_result(self) -> None:
        # Pattern B — find* family (representative for findActor, findEvent,
        # findType, findUseCase). Returns wrapped element or None.
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Package")
        cls = make_fake_element("Class", getName="C1")
        fake.findClass.return_value = cls
        pkg = RPPackage(fake)
        wrapped = pkg.find_class("C1")
        assert wrapped is not None
        assert wrapped.get_name() == "C1"
        fake.findClass.assert_called_once_with("C1")

    def test_find_class_returns_none_when_not_found(self) -> None:
        # Pattern B — None branch
        fake = make_fake_element("Package")
        fake.findClass.return_value = None
        pkg = RPPackage(fake)
        assert pkg.find_class("NoSuchClass") is None

    def test_get_events_returns_collection(self) -> None:
        # Pattern C — get* collection family (representative for getFlows,
        # getModules, getNodes, getTypes)
        fake = make_fake_element("Package")
        ev = make_fake_element("Event", getName="ev1")
        fake.getEvents.return_value = make_fake_collection([ev])
        pkg = RPPackage(fake)
        result = pkg.get_events()
        assert isinstance(result, RPCollection)
        fake.getEvents.assert_called_once_with()

    def test_get_modules_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Package")
        mod = make_fake_element("Module", getName="m1")
        fake.getModules.return_value = make_fake_collection([mod])
        pkg = RPPackage(fake)
        result = pkg.get_modules()
        assert isinstance(result, RPCollection)
        fake.getModules.assert_called_once_with()

    def test_get_types_returns_collection(self) -> None:
        # Pattern C
        from rhapsody_cli.models.elements.common import RPType
        fake = make_fake_element("Package")
        t = make_fake_element("Type", getName="T1")
        fake.getTypes.return_value = make_fake_collection([t])
        pkg = RPPackage(fake)
        result = pkg.get_types()
        assert isinstance(result, RPCollection)
        fake.getTypes.assert_called_once_with()
```

Add to `tests/unit/models/elements/test_project.py`:
```python
"""Tests for RPProject — additional methods from Task 11."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment import RPProject
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPProjectTask11:
    def test_add_component_delegates_and_wraps(self) -> None:
        # Pattern E — add* family (representative for addProfile)
        from rhapsody_cli.models.elements.containment import RPComponent
        fake = make_fake_element("Project")
        comp = make_fake_element("Component", getName="c1")
        fake.addComponent.return_value = comp
        proj = RPProject(fake)
        wrapped = proj.add_component("c1")
        assert wrapped.get_name() == "c1"
        fake.addComponent.assert_called_once_with("c1")

    def test_add_profile_delegates_and_wraps(self) -> None:
        # Pattern E
        fake = make_fake_element("Project")
        prof = make_fake_element("Profile", getName="p1")
        fake.addProfile.return_value = prof
        proj = RPProject(fake)
        wrapped = proj.add_profile("p1")
        assert wrapped.get_name() == "p1"
        fake.addProfile.assert_called_once_with("p1")

    def test_find_element_by_file_name_wraps_result(self) -> None:
        # Pattern B — find* family (representative for findElementByBinaryID)
        fake = make_fake_element("Project")
        el = make_fake_element("Class", getName="C1")
        fake.findElementByFileName.return_value = el
        proj = RPProject(fake)
        wrapped = proj.find_element_by_file_name("C1.cls")
        assert wrapped is not None
        assert wrapped.get_name() == "C1"
        fake.findElementByFileName.assert_called_once_with("C1.cls")

    def test_find_element_by_file_name_returns_none_when_not_found(self) -> None:
        # Pattern B — None branch
        fake = make_fake_element("Project")
        fake.findElementByFileName.return_value = None
        proj = RPProject(fake)
        assert proj.find_element_by_file_name("nope.cls") is None

    def test_get_profiles_returns_collection(self) -> None:
        # Pattern C — get* collection family
        fake = make_fake_element("Project")
        prof = make_fake_element("Profile", getName="p1")
        fake.getProfiles.return_value = make_fake_collection([prof])
        proj = RPProject(fake)
        result = proj.get_profiles()
        assert isinstance(result, RPCollection)
        fake.getProfiles.assert_called_once_with()

    def test_get_all_stereotypes_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Project")
        st = make_fake_element("Stereotype", getName="s1")
        fake.getAllStereotypes.return_value = make_fake_collection([st])
        proj = RPProject(fake)
        result = proj.get_all_stereotypes()
        assert isinstance(result, RPCollection)
        fake.getAllStereotypes.assert_called_once_with()

    def test_allow_auto_save_delegates(self) -> None:
        # Pattern F — bool/int arg (representative for allowNonUniqueNames)
        fake = make_fake_element("Project")
        fake.allowAutoSave.return_value = None
        proj = RPProject(fake)
        proj.allow_auto_save(True)
        fake.allowAutoSave.assert_called_once_with(1)

    def test_save_as_delegates(self) -> None:
        # Pattern F — str path arg (representative for saveAsPrevVersion)
        fake = make_fake_element("Project")
        fake.saveAs.return_value = None
        proj = RPProject(fake)
        proj.save_as("path/to/file.rpy")
        fake.saveAs.assert_called_once_with("path/to/file.rpy")

    def test_generate_report_delegates(self) -> None:
        # Pattern F — multi-arg void (verify arg count from stub)
        fake = make_fake_element("Project")
        fake.generateReport.return_value = None
        proj = RPProject(fake)
        proj.generate_report("template", "out.html")
        fake.generateReport.assert_called_once_with("template", "out.html")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_package.py tests/unit/models/elements/test_project.py -v`

Expected: FAIL — `AttributeError` (methods don't exist yet on the class)

- [ ] **Step 3: Create all 153 methods (RPPackage: 92, RPProject: 61)**

For each unchecked method in the checklist at the top of `RPPackage` and `RPProject`, add the `def` block + implementation. Use the Pattern mapping above. Read the existing implemented methods in `model_package.py` (e.g. `add_class`, `add_actor`, `get_classes`, `get_actors`) as templates — they already demonstrate Pattern E (add + wrap) and Pattern C (get + collection).

Verify `register_wrapper` calls exist at the bottom of both files. If missing, add:
```python
AbstractRPModelElement.register_wrapper("Package", RPPackage)
AbstractRPModelElement.register_wrapper("Project", RPProject)
```

- [ ] **Step 4: Verify `containment/__init__.py`** — ensure `RPPackage`, `RPProject`, `RPComponent`, `RPNode`, etc. are all exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_package.py tests/unit/models/elements/test_project.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/containment/model_package.py \
       src/rhapsody_cli/models/elements/containment/model_project.py \
       src/rhapsody_cli/models/elements/containment/__init__.py \
       tests/unit/models/elements/test_package.py \
       tests/unit/models/elements/test_project.py
git commit -m "feat(containment): implement RPPackage (92) and RPProject (61) methods"
```

---

### Task 12: Containment — Component + Collaboration + Configuration + Node + ComponentInstance (137 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/containment/model_component.py` (~43 unchecked)
- Modify: `src/rhapsody_cli/models/elements/containment/model_collaboration.py` (~39 unchecked)
- Modify: `src/rhapsody_cli/models/elements/containment/model_configuration.py` (~46 unchecked)
- Modify: `src/rhapsody_cli/models/elements/containment/model_node.py` (~6 unchecked)
- Modify: `src/rhapsody_cli/models/elements/containment/model_component_instance.py` (~3 unchecked)
- Expand existing test files

**Critical implementation note (same as Task 11):** These methods need to be **CREATED from scratch** — they are NOT `raise NotImplementedError` stubs. Each containment file has a checklist at the top of the class showing `[ ] methodName` for every unchecked method, but the method bodies do not exist. You must add the `def` block + implementation following the Pattern rules.

**Import notes:** Each file imports `AbstractRPModelElement` and `RPUnit` at runtime (verify by reading each file). For methods that return wrapped elements (Pattern B/E) or collections (Pattern C), add `RPCollection` to the runtime import if not already present. Use `TYPE_CHECKING` guards for cross-package typed returns — verify what's already in the `TYPE_CHECKING` block before adding.

**Registration notes:** All 5 classes should already have `register_wrapper` calls (e.g. `register_wrapper("Component", RPComponent)`, `register_wrapper("Collaboration", RPCollaboration)`, etc.). Verify by reading each file. If any are missing, add the corresponding call at the bottom of the file.

**Pattern mapping (same 4 method families as Task 11):**
- `add*` methods → **Pattern E** (add + wrap)
- `delete*` methods → **Pattern F** (delete via `target._com`)
- `find*` methods → **Pattern B** (return wrapped element or `None` — handle the `None` case explicitly if `wrap()` does not)
- `get*` methods returning collections → **Pattern C**
- `get*` methods returning primitives → **Pattern A**
- `set*` methods (str/int arg) → **Pattern D**
- `set*` methods taking `RPModelElement` → **Pattern F**

- [ ] **Step 1: Write failing tests**

Expand the existing test files (`tests/unit/models/elements/test_component.py`, `test_collaboration.py`, `test_configuration.py`, `test_node.py`, `test_component_instance.py`). Representative tests for the two largest classes:

Add to `tests/unit/models/elements/test_component.py`:
```python
"""Tests for RPComponent — methods from Task 12."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment import RPComponent
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPComponentTask12:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Component", getName="c1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPComponent)

    def test_add_class_delegates_and_wraps(self) -> None:
        # Pattern E — add* family. (Verify the actual method name and signature
        # by reading the checklist at the top of model_component.py — common
        # methods include addClass, addInterface, addRelation, addDiagram, etc.)
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Component")
        cls = make_fake_element("Class", getName="C1")
        fake.addClass.return_value = cls
        comp = RPComponent(fake)
        wrapped = comp.add_class("C1")
        assert wrapped.get_name() == "C1"
        fake.addClass.assert_called_once_with("C1")

    def test_add_node_delegates_and_wraps(self) -> None:
        # Pattern E
        fake = make_fake_element("Component")
        node = make_fake_element("Node", getName="n1")
        fake.addNode.return_value = node
        comp = RPComponent(fake)
        wrapped = comp.add_node("n1")
        assert wrapped.get_name() == "n1"
        fake.addNode.assert_called_once_with("n1")

    def test_get_classes_returns_collection(self) -> None:
        # Pattern C — get* collection family
        fake = make_fake_element("Component")
        cls = make_fake_element("Class", getName="C1")
        fake.getClasses.return_value = make_fake_collection([cls])
        comp = RPComponent(fake)
        result = comp.get_classes()
        assert isinstance(result, RPCollection)
        fake.getClasses.assert_called_once_with()

    def test_find_class_wraps_result(self) -> None:
        # Pattern B — find* family
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Component")
        cls = make_fake_element("Class", getName="C1")
        fake.findClass.return_value = cls
        comp = RPComponent(fake)
        wrapped = comp.find_class("C1")
        assert wrapped is not None
        assert wrapped.get_name() == "C1"

    def test_delete_class_delegates(self) -> None:
        # Pattern F — delete* family
        from rhapsody_cli.models.elements.classifiers import RPClass
        fake = make_fake_element("Component")
        cls = make_fake_element("Class", getName="C1")
        fake.deleteClass.return_value = None
        comp = RPComponent(fake)
        comp.delete_class(RPClass(cls))
        fake.deleteClass.assert_called_once_with(cls)
```

Add to `tests/unit/models/elements/test_collaboration.py`:
```python
"""Tests for RPCollaboration — methods from Task 12."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.containment import RPCollaboration
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPCollaborationTask12:
    def test_is_registered(self) -> None:
        fake = make_fake_element("Collaboration", getName="col1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPCollaboration)

    def test_add_classifier_role_delegates_and_wraps(self) -> None:
        # Pattern E — add* family. (Verify the actual method name by reading
        # the checklist at the top of model_collaboration.py — common methods
        # include addClassifierRole, addDiagram, addMessage, etc.)
        from rhapsody_cli.models.elements.common import RPClassifierRole
        fake = make_fake_element("Collaboration")
        cr = make_fake_element("ClassifierRole", getName="cr1")
        fake.addClassifierRole.return_value = cr
        col = RPCollaboration(fake)
        wrapped = col.add_classifier_role("cr1")
        assert wrapped.get_name() == "cr1"
        fake.addClassifierRole.assert_called_once_with("cr1")

    def test_get_classifier_roles_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("Collaboration")
        cr = make_fake_element("ClassifierRole", getName="cr1")
        fake.getClassifierRoles.return_value = make_fake_collection([cr])
        col = RPCollaboration(fake)
        result = col.get_classifier_roles()
        assert isinstance(result, RPCollection)
        fake.getClassifierRoles.assert_called_once_with()
```

For `RPConfiguration`, `RPNode`, `RPComponentInstance` — follow the same test structure (2+ representative tests per class).

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_component.py tests/unit/models/elements/test_collaboration.py tests/unit/models/elements/test_configuration.py tests/unit/models/elements/test_node.py tests/unit/models/elements/test_component_instance.py -v`

Expected: FAIL — `AttributeError` (methods don't exist yet)

- [ ] **Step 3: Create all 137 methods (RPComponent: 43, RPCollaboration: 39, RPConfiguration: 46, RPNode: 6, RPComponentInstance: 3)**

For each unchecked method in the checklist at the top of each class, add the `def` block + implementation. Use the Pattern mapping above. Read the existing implemented methods in `model_package.py` (from Task 11) as templates for the same method families.

Verify `register_wrapper` calls exist at the bottom of each file.

- [ ] **Step 4: Verify `containment/__init__.py`** — ensure all 5 classes are exported.

- [ ] **Step 5: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_component.py tests/unit/models/elements/test_collaboration.py tests/unit/models/elements/test_configuration.py tests/unit/models/elements/test_node.py tests/unit/models/elements/test_component_instance.py -v`

Expected: ALL PASS

- [ ] **Step 6: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 7: Commit**

```bash
git add src/rhapsody_cli/models/elements/containment/model_component.py \
       src/rhapsody_cli/models/elements/containment/model_collaboration.py \
       src/rhapsody_cli/models/elements/containment/model_configuration.py \
       src/rhapsody_cli/models/elements/containment/model_node.py \
       src/rhapsody_cli/models/elements/containment/model_component_instance.py \
       src/rhapsody_cli/models/elements/containment/__init__.py \
       tests/unit/models/elements/test_component.py \
       tests/unit/models/elements/test_collaboration.py \
       tests/unit/models/elements/test_configuration.py \
       tests/unit/models/elements/test_node.py \
       tests/unit/models/elements/test_component_instance.py
git commit -m "feat(containment): implement 5 containment classes (137 methods)"
```

---

### Task 13: Diagrams — 11 diagram type subclasses + RPDiagram (39 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (29 unchecked methods on `RPDiagram`)
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py` (10 unchecked methods across 11 subclasses)
- Expand: `tests/unit/models/elements/test_diagram.py`
- Create: `tests/unit/models/elements/test_diagram_types.py`

**Import notes:**
- `model_diagrams.py` already imports `AbstractRPModelElement`, `RPCollection`, `RPModelElement`, `RPUnit` at runtime and `RPGraphElement` under `TYPE_CHECKING`. No new runtime imports needed — all 29 `RPDiagram` methods use these.
- `model_diagram_types.py` already imports `RPDiagram` at runtime and `RPCollection`, `RPFlowchart`, `RPStatechart`, `RPCollaboration`, `RPGraphElement`, `RPGraphNode` under `TYPE_CHECKING`. To add `register_wrapper` calls, add `AbstractRPModelElement` to the runtime import from `rhapsody_cli.models.core`.

**Registration notes:**
- `model_diagrams.py` currently has **one** registration: `register_wrapper("ActivityDiagram", RPDiagram)` at the bottom. **Keep this mapping** — existing tests rely on it (`test_diagram_is_registered_for_meta_class_activity_diagram` expects `RPDiagram`).
- Add registrations in `model_diagram_types.py` for the **other 10** diagram types (do NOT re-register `"ActivityDiagram"` there to avoid clobbering the existing `RPDiagram` mapping):
  - `register_wrapper("CollaborationDiagram", RPCollaborationDiagram)`
  - `register_wrapper("ComponentDiagram", RPComponentDiagram)`
  - `register_wrapper("DeploymentDiagram", RPDeploymentDiagram)`
  - `register_wrapper("ObjectModelDiagram", RPObjectModelDiagram)`
  - `register_wrapper("PanelDiagram", RPPanelDiagram)`
  - `register_wrapper("SequenceDiagram", RPSequenceDiagram)`
  - `register_wrapper("StatechartDiagram", RPStatechartDiagram)`
  - `register_wrapper("StructureDiagram", RPStructureDiagram)`
  - `register_wrapper("UseCaseDiagram", RPUseCaseDiagram)`
  - `register_wrapper("TimingDiagram", RPTimingDiagram)`
- The existing `"ActivityDiagram"` → `RPDiagram` registration is intentionally preserved for backward compatibility. (A future task could override this mapping with `RPActivityDiagram` for more specific wrapping — out of scope here.)

**Pattern mapping:**
- `get*` methods returning primitives (str/int) → **Pattern A** (`_get_method_or_property`)
- `get*` methods returning wrapped elements → **Pattern B** (`AbstractRPModelElement.wrap(...)`)
- `get*` methods returning collections → **Pattern C** (`RPCollection(...)`)
- `set*` methods with single str/int arg → **Pattern D** (`_set_method_or_property`)
- `add*`/`create*` methods returning wrapped elements → **Pattern E** (multi-arg, wrap result)
- `open*`/`close*`/`populate*`/`rearrange*`/`remove*`/`complete*`/`update*` void methods → **Pattern F** (`call_com(lambda: ...)`)
- `is*` methods returning 0/1 → **Pattern G** (`int(self.call_com(...))`)
- For parameterized getters like `getDiagramViewOf(name)` and `getPictureAs(format, ...)` → MUST use `call_com` directly (not `_get_method_or_property`, which drops extra args)

**Methods — RPDiagram (29):** `addFreeShapeByType`, `addImage`, `addNewEdgeByType`, `addNewEdgeForElement`, `addNewNodeByType`, `addNewNodeForElement`, `createDiagramView`, `getDiagramViewOf`, `getDiagramViews`, `isDiagramView`, `openDiagramView`, `rearrangePorts`, `setCustomViews`, `updateViewOnServer`, `completeRelations`, `getElementsInDiagram`, `getGraphicalElements`, `getLastVisualizationModifiedTime`, `getPicture`, `getPictureAs`, `getPictureAsDividedMetafiles`, `getPictureEx`, `getPicturesWithImageMap`, `isOpen`, `isShowDiagramFrame`, `openDiagram`, `populateDiagram`, `removeGraphElements`, `setShowDiagramFrame`

**Methods — Diagram types (10):** `RPCollaborationDiagram.get_logical_collaboration` (B), `RPSequenceDiagram.get_logical_collaboration` (B) + `get_related_use_cases` (C), `RPStatechartDiagram.add_and_line` (E) + `create_graphics` (F) + `get_statechart` (B), `RPTimingDiagram.get_is_elaborated` (G) + `set_is_elaborated` (D), `RPActivityDiagram.decompose_swimlane` (E) + `get_flowchart` (B).

- [ ] **Step 1: Write failing tests**

Expand `tests/unit/models/elements/test_diagram.py` with representative tests for `RPDiagram` (at least 3 new tests covering different patterns). Add a new test class for Task 13 methods:
```python
"""Tests for RPDiagram — methods from Task 13 (added to existing test_diagram.py)."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPDiagramTask13:
    def test_open_diagram_delegates_to_com(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("ActivityDiagram")
        fake.openDiagram.return_value = None
        diagram = RPDiagram(fake)
        diagram.open_diagram()
        fake.openDiagram.assert_called_once_with()

    def test_is_open_returns_int(self) -> None:
        # Pattern G — boolean check returning int (0/1)
        fake = make_fake_element("ActivityDiagram")
        fake.isOpen.return_value = 1
        diagram = RPDiagram(fake)
        assert diagram.is_open() == 1
        fake.isOpen.assert_called_once_with()

    def test_get_elements_in_diagram_returns_collection(self) -> None:
        # Pattern C — get* collection
        fake = make_fake_element("ActivityDiagram")
        elem = make_fake_element("Class", getName="Widget")
        fake.getElementsInDiagram.return_value = make_fake_collection([elem])
        diagram = RPDiagram(fake)
        result = diagram.get_elements_in_diagram()
        assert isinstance(result, RPCollection)
        fake.getElementsInDiagram.assert_called_once_with()

    def test_add_new_node_by_type_delegates_and_wraps(self) -> None:
        # Pattern E — multi-arg method returning wrapped element.
        # Verify exact signature by reading the RPDiagram checklist / Java API ref.
        fake = make_fake_element("ActivityDiagram")
        node = make_fake_element("GraphNode", getName="Node1")
        fake.addNewNodeByType.return_value = node
        diagram = RPDiagram(fake)
        wrapped = diagram.add_new_node_by_type("Class", 10, 20, 100, 50)
        assert wrapped.get_name() == "Node1"
        fake.addNewNodeByType.assert_called_once_with("Class", 10, 20, 100, 50)

    def test_set_show_diagram_frame_delegates(self) -> None:
        # Pattern D — single-arg setter (int)
        fake = make_fake_element("ActivityDiagram")
        fake.setShowDiagramFrame.return_value = None
        diagram = RPDiagram(fake)
        diagram.set_show_diagram_frame(1)
        fake.setShowDiagramFrame.assert_called_once_with(1)
```

Create `tests/unit/models/elements/test_diagram_types.py` with registration + method tests for diagram subclasses:
```python
"""Tests for diagram type subclasses from Task 13."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection
from rhapsody_cli.models.elements.diagrams import (
    RPCollaborationDiagram,
    RPComponentDiagram,
    RPDeploymentDiagram,
    RPObjectModelDiagram,
    RPPanelDiagram,
    RPSequenceDiagram,
    RPStatechartDiagram,
    RPStructureDiagram,
    RPUseCaseDiagram,
    RPTimingDiagram,
    RPDiagram,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPDiagramTypeRegistration:
    def test_collaboration_diagram_is_registered(self) -> None:
        fake = make_fake_element("CollaborationDiagram", getName="cd1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPCollaborationDiagram)

    def test_sequence_diagram_is_registered(self) -> None:
        fake = make_fake_element("SequenceDiagram", getName="sd1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPSequenceDiagram)

    def test_statechart_diagram_is_registered(self) -> None:
        fake = make_fake_element("StatechartDiagram", getName="sc1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPStatechartDiagram)

    def test_timing_diagram_is_registered(self) -> None:
        fake = make_fake_element("TimingDiagram", getName="td1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPTimingDiagram)

    def test_activity_diagram_still_maps_to_rpdiagram(self) -> None:
        # Existing mapping preserved — do NOT re-register ActivityDiagram in model_diagram_types.py
        fake = make_fake_element("ActivityDiagram", getName="ad1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPDiagram)


class TestRPSequenceDiagramTask13:
    def test_get_logical_collaboration_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.containment import RPCollaboration
        fake = make_fake_element("SequenceDiagram")
        col = make_fake_element("Collaboration", getName="col1")
        fake.getLogicalCollaboration.return_value = col
        sd = RPSequenceDiagram(fake)
        wrapped = sd.get_logical_collaboration()
        assert isinstance(wrapped, RPCollaboration)
        assert wrapped.get_name() == "col1"

    def test_get_related_use_cases_returns_collection(self) -> None:
        # Pattern C
        fake = make_fake_element("SequenceDiagram")
        uc = make_fake_element("UseCase", getName="UC1")
        fake.getRelatedUseCases.return_value = make_fake_collection([uc])
        sd = RPSequenceDiagram(fake)
        result = sd.get_related_use_cases()
        assert isinstance(result, RPCollection)
        fake.getRelatedUseCases.assert_called_once_with()


class TestRPStatechartDiagramTask13:
    def test_create_graphics_delegates(self) -> None:
        # Pattern F — void method
        fake = make_fake_element("StatechartDiagram")
        fake.createGraphics.return_value = None
        scd = RPStatechartDiagram(fake)
        scd.create_graphics()
        fake.createGraphics.assert_called_once_with()

    def test_get_statechart_wraps_result(self) -> None:
        # Pattern B
        from rhapsody_cli.models.elements.classifiers import RPStatechart
        fake = make_fake_element("StatechartDiagram")
        sc = make_fake_element("Statechart", getName="SC1")
        fake.getStatechart.return_value = sc
        scd = RPStatechartDiagram(fake)
        wrapped = scd.get_statechart()
        assert wrapped.get_name() == "SC1"


class TestRPTimingDiagramTask13:
    def test_get_is_elaborated_returns_int(self) -> None:
        # Pattern G
        fake = make_fake_element("TimingDiagram")
        fake.getIsElaborated.return_value = 1
        td = RPTimingDiagram(fake)
        assert td.get_is_elaborated() == 1

    def test_set_is_elaborated_delegates(self) -> None:
        # Pattern D
        fake = make_fake_element("TimingDiagram")
        fake.setIsElaborated.return_value = None
        td = RPTimingDiagram(fake)
        td.set_is_elaborated(1)
        fake.setIsElaborated.assert_called_once_with(1)
```

For the remaining 7 diagram type subclasses (`RPCollaborationDiagram`, `RPComponentDiagram`, `RPDeploymentDiagram`, `RPObjectModelDiagram`, `RPPanelDiagram`, `RPStructureDiagram`, `RPUseCaseDiagram`) — most have 0 own methods (just `pass`) and only need a registration test each, following the pattern in `TestRPDiagramTypeRegistration`. For `RPCollaborationDiagram.get_logical_collaboration` (Pattern B) and `RPActivityDiagram.decompose_swimlane`/`get_flowchart` — add method tests following the same structure as `TestRPSequenceDiagramTask13`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_diagram.py tests/unit/models/elements/test_diagram_types.py -v`

Expected: FAIL — `AttributeError` (methods don't exist) or `NotImplementedError` (stubs) or `AssertionError` (registration missing)

- [ ] **Step 3: Implement 29 RPDiagram methods in `model_diagrams.py`**

Replace each `raise NotImplementedError` stub (or add the `def` block for the 29 unchecked methods listed in the RPDiagram checklist) using the Pattern mapping above. Reference the 4 already-implemented methods (`close_diagram`, `add_text_box`, `get_custom_views`, `get_corresponding_graphic_elements`) as templates.

- [ ] **Step 4: Implement 10 diagram type subclass methods in `model_diagram_types.py`**

Replace `raise NotImplementedError` stubs:
- `RPCollaborationDiagram.get_logical_collaboration` → Pattern B
- `RPSequenceDiagram.get_logical_collaboration` → Pattern B
- `RPSequenceDiagram.get_related_use_cases` → Pattern C
- `RPStatechartDiagram.add_and_line` → Pattern E (multi-arg, returns `RPCollection`)
- `RPStatechartDiagram.create_graphics` → Pattern F (void)
- `RPStatechartDiagram.get_statechart` → Pattern B
- `RPTimingDiagram.get_is_elaborated` → Pattern G
- `RPTimingDiagram.set_is_elaborated` → Pattern D
- `RPActivityDiagram.decompose_swimlane` → Pattern E (returns `RPCollection`)
- `RPActivityDiagram.get_flowchart` → Pattern B

- [ ] **Step 5: Add 10 `register_wrapper` calls to `model_diagram_types.py`**

Add `AbstractRPModelElement` to the runtime import, then add the 10 registration calls listed in the Registration notes section above (do NOT re-register `"ActivityDiagram"` — it stays mapped to `RPDiagram` in `model_diagrams.py`).

- [ ] **Step 6: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_diagram.py tests/unit/models/elements/test_diagram_types.py -v`

Expected: ALL PASS

- [ ] **Step 7: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 8: Commit**

```bash
git add src/rhapsody_cli/models/elements/diagrams/model_diagrams.py \
       src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py \
       src/rhapsody_cli/models/elements/diagrams/__init__.py \
       tests/unit/models/elements/test_diagram.py \
       tests/unit/models/elements/test_diagram_types.py
git commit -m "feat(diagrams): implement RPDiagram + 11 diagram type subclasses (39 methods)"
```

---

### Task 14: Requirements — RPAnnotation (registration only, 0 methods to implement)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/requirements/model_requirements.py`
- Expand: `tests/unit/models/elements/test_annotation.py`

**Critical note:** `RPAnnotation` already has all 10 checklist items marked `[x]` (implemented + docstring + test). **No methods need to be implemented** — this task is purely a registration task. The only change required is adding one `register_wrapper` call.

**Import notes:** `model_requirements.py` already imports `AbstractRPModelElement`, `RPCollection`, `RPModelElement`, `RPUnit` at runtime. No new imports needed — `AbstractRPModelElement` is already available for `register_wrapper`.

**Registration notes:**
- `RPRequirement` is already registered at the bottom of the file: `register_wrapper("Requirement", RPRequirement)`.
- `RPAnnotation` is **missing** its registration. Add the following line immediately after the `RPAnnotation` class definition (before the `RPRequirement` class):
  ```python
  AbstractRPModelElement.register_wrapper("Annotation", RPAnnotation)
  ```
- This must come BEFORE the `RPRequirement` class definition so that the `Requirement` metaclass can still map to the more specific `RPRequirement` subclass (registrations are processed in order; `RPRequirement` extends `RPAnnotation`, so the `Requirement` registration at the bottom correctly overrides `Annotation` for requirement elements).

- [ ] **Step 1: Write a failing registration test**

Add to `tests/unit/models/elements/test_annotation.py`:
```python
"""Registration test for RPAnnotation — added in Task 14."""

from rhapsody_cli.models.core import AbstractRPModelElement
from rhapsody_cli.models.elements.requirements.model_requirements import RPAnnotation
from tests.unit.models.fakes import make_fake_element


def test_annotation_is_registered_for_meta_class_annotation() -> None:
    # Before Task 14: wrap("Annotation") returns a generic RPModelElement (not RPAnnotation)
    # After Task 14: wrap("Annotation") returns an RPAnnotation instance
    fake = make_fake_element("Annotation", getName="Note1")
    wrapped = AbstractRPModelElement.wrap(fake)
    assert isinstance(wrapped, RPAnnotation)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/models/elements/test_annotation.py::test_annotation_is_registered_for_meta_class_annotation -v`

Expected: FAIL — `AssertionError` (wrapped is a generic `RPModelElement`, not `RPAnnotation`)

- [ ] **Step 3: Add the `register_wrapper` call**

In `src/rhapsody_cli/models/elements/requirements/model_requirements.py`, insert the following line immediately after the `RPAnnotation` class body (after the `set_specification_rtf` method, before `class RPRequirement`):

```python
AbstractRPModelElement.register_wrapper("Annotation", RPAnnotation)
```

- [ ] **Step 4: Run test to verify pass**

Run: `pytest tests/unit/models/elements/test_annotation.py -v`

Expected: ALL PASS (including the new registration test and all existing RPAnnotation method tests)

- [ ] **Step 5: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/elements/requirements/model_requirements.py \
       tests/unit/models/elements/test_annotation.py
git commit -m "feat(requirements): register RPAnnotation wrapper for 'Annotation' metaclass"
```

---

### Task 15: Graphics — 14 classes (~190 methods)

**Files:**
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`
- Create: `tests/unit/models/elements/test_graphics.py`

**Scope warning — consider splitting:** This is the largest task in the plan (~189 stub methods across 14 classes). `RPTableLayout` alone has 49 methods, `RPGraphElement` has 22, `RPLink` has 20, `RPMatrixView` has 19, `RPConnector` has 16, `RPTableView` has 16. If the implementer finds the task unwieldy, split into sub-tasks by class family:
- **15a:** `RPGraphElement` + `RPGraphEdge` + `RPGraphNode` (graph element family, 34 methods)
- **15b:** `RPConnector` + `RPPin` + `RPConditionMark` (connector family, 22 methods)
- **15c:** `RPLink` + `RPImageMap` + `RPGraphicalProperty` + `RPMessagePoint` (link/misc family, 35 methods)
- **15d:** `RPTableLayout` + `RPTableView` + `RPMatrixLayout` + `RPMatrixView` (table/matrix family, 98 methods)

**Import notes:**
- `model_graphics.py` already imports `RPModelElement`, `RPUnit` at runtime; `RPMessage` (from interactions) and `RPStateVertex` (from statemachine) at runtime; and a large `TYPE_CHECKING` block for `RPCollection`, `RPFlow`, `RPSwimlane`, `RPClassifier`, `RPClassifierRole`, `RPSysMLPort`, `RPDiagram`, `RPInteractionOccurrence`, `RPInteractionOperator`, `RPTransition`, `RPInstance`, `RPPort`, `RPRelation`, `RPState`.
- To add `register_wrapper` calls, add `AbstractRPModelElement` to the runtime import from `rhapsody_cli.models.core` (currently only `RPModelElement` and `RPUnit` are imported from there).
- No new `TYPE_CHECKING` imports needed — all cross-package return types are already covered.

**Registration notes:** **None** of the 14 classes are currently registered (no `register_wrapper` calls exist in the file). Add the following 14 calls at the bottom of `model_graphics.py` (after all class definitions):
- `register_wrapper("ConditionMark", RPConditionMark)`
- `register_wrapper("Connector", RPConnector)`
- `register_wrapper("GraphElement", RPGraphElement)`
- `register_wrapper("GraphicalProperty", RPGraphicalProperty)`
- `register_wrapper("ImageMap", RPImageMap)`
- `register_wrapper("Link", RPLink)`
- `register_wrapper("MatrixLayout", RPMatrixLayout)`
- `register_wrapper("MatrixView", RPMatrixView)`
- `register_wrapper("MessagePoint", RPMessagePoint)`
- `register_wrapper("TableLayout", RPTableLayout)`
- `register_wrapper("TableView", RPTableView)`
- `register_wrapper("Pin", RPPin)`
- `register_wrapper("GraphEdge", RPGraphEdge)`
- `register_wrapper("GraphNode", RPGraphNode)`

**Pattern mapping:**
- `get*` methods returning primitives (str/int) → **Pattern A** (`_get_method_or_property`)
- `get*` methods returning wrapped elements (e.g. `get_source`, `get_target`, `get_diagram`, `get_model_object`) → **Pattern B** (`AbstractRPModelElement.wrap(...)`)
- `get*` methods returning collections → **Pattern C** (`RPCollection(...)`)
- `set*` methods with single str/int arg → **Pattern D** (`_set_method_or_property`)
- `add*` methods returning wrapped elements or collections → **Pattern E** (multi-arg, wrap result)
- `remove*`/`open*`/`bring*`/`send*`/`hide*`/`show*`/`apply*`/`embed*` void methods → **Pattern F** (`call_com(lambda: ...)`)
- `is*`/`get*UseQueryOrElementsList`/`getRelationTable` methods returning 0/1 → **Pattern G** (`int(self.call_com(...))`)
- For parameterized getters like `get_graphical_property(name)`, `get_property_value(key)`, `get_column_name(index)`, `get_cell_elements(row, col)` → MUST use `call_com` directly (not `_get_method_or_property`, which drops extra args)
- For multi-arg setters like `set_graphical_property(name, value)`, `set_column_context(index, context)` → MUST use `call_com` directly (not `_set_method_or_property`)

- [ ] **Step 1: Write failing tests**

Create `tests/unit/models/elements/test_graphics.py` with representative tests. Below are tests for `RPGraphElement` (22 methods) and `RPGraphEdge` (5 methods) — the two classes explicitly requested. The other 12 classes follow the same structure (2+ representative tests per class, covering at least one method per Pattern family that the class uses).

```python
"""Tests for graphics package — RPGraphElement, RPGraphEdge, and 12 other classes (Task 15)."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.graphics import (
    RPConditionMark,
    RPConnector,
    RPGraphEdge,
    RPGraphElement,
    RPGraphicalProperty,
    RPGraphNode,
    RPImageMap,
    RPLink,
    RPMatrixLayout,
    RPMatrixView,
    RPMessagePoint,
    RPPin,
    RPTableLayout,
    RPTableView,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPGraphElementTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphElement", getName="ge1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphElement)

    def test_get_interface_name_returns_str(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("GraphElement")
        fake.getInterfaceName.return_value = "IFoo"
        ge = RPGraphElement(fake)
        assert ge.get_interface_name() == "IFoo"
        fake.getInterfaceName.assert_called_once_with()

    def test_get_model_object_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphElement")
        model_obj = make_fake_element("Class", getName="Widget")
        fake.getModelObject.return_value = model_obj
        ge = RPGraphElement(fake)
        wrapped = ge.get_model_object()
        assert wrapped.get_name() == "Widget"
        fake.getModelObject.assert_called_once_with()

    def test_get_all_graphical_properties_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning collection
        fake = make_fake_element("GraphElement")
        prop = make_fake_element("GraphicalProperty", getName="p1")
        fake.getAllGraphicalProperties.return_value = make_fake_collection([prop])
        ge = RPGraphElement(fake)
        result = ge.get_all_graphical_properties()
        assert isinstance(result, RPCollection)
        fake.getAllGraphicalProperties.assert_called_once_with()

    def test_set_associated_image_delegates(self) -> None:
        # Pattern D — single-arg setter (str)
        fake = make_fake_element("GraphElement")
        fake.setAssociatedImage.return_value = None
        ge = RPGraphElement(fake)
        ge.set_associated_image("img.png")
        fake.setAssociatedImage.assert_called_once_with("img.png")

    def test_add_property_delegates(self) -> None:
        # Pattern F — multi-arg void method (3 str args)
        fake = make_fake_element("GraphElement")
        fake.addProperty.return_value = None
        ge = RPGraphElement(fake)
        ge.add_property("key", "type", "value")
        fake.addProperty.assert_called_once_with("key", "type", "value")

    def test_get_graphical_property_uses_call_com_directly(self) -> None:
        # Parameterized getter — must use call_com (not _get_method_or_property)
        fake = make_fake_element("GraphElement")
        prop = make_fake_element("GraphicalProperty", getName="FillColor")
        fake.getGraphicalProperty.return_value = prop
        ge = RPGraphElement(fake)
        wrapped = ge.get_graphical_property("FillColor")
        assert wrapped.get_name() == "FillColor"
        fake.getGraphicalProperty.assert_called_once_with("FillColor")

    def test_remove_property_delegates(self) -> None:
        # Pattern F — single-arg void method (str)
        fake = make_fake_element("GraphElement")
        fake.removeProperty.return_value = None
        ge = RPGraphElement(fake)
        ge.remove_property("key")
        fake.removeProperty.assert_called_once_with("key")


class TestRPGraphEdgeTask15:
    def test_is_registered(self) -> None:
        fake = make_fake_element("GraphEdge", getName="edge1")
        wrapped = AbstractRPModelElement.wrap(fake)
        assert isinstance(wrapped, RPGraphEdge)

    def test_is_graph_element(self) -> None:
        # RPGraphEdge extends RPGraphElement
        fake = make_fake_element("GraphEdge", getName="edge1")
        edge = RPGraphEdge(fake)
        assert isinstance(edge, RPGraphElement)

    def test_get_source_wraps_result(self) -> None:
        # Pattern B — no-arg getter returning wrapped element
        fake = make_fake_element("GraphEdge")
        src = make_fake_element("GraphNode", getName="src")
        fake.getSource.return_value = src
        edge = RPGraphEdge(fake)
        wrapped = edge.get_source()
        assert wrapped.get_name() == "src"
        fake.getSource.assert_called_once_with()

    def test_get_target_wraps_result(self) -> None:
        # Pattern B
        fake = make_fake_element("GraphEdge")
        tgt = make_fake_element("GraphNode", getName="tgt")
        fake.getTarget.return_value = tgt
        edge = RPGraphEdge(fake)
        wrapped = edge.get_target()
        assert wrapped.get_name() == "tgt"
        fake.getTarget.assert_called_once_with()

    def test_embed_new_flow_returns_self(self) -> None:
        # Pattern E — no-arg method returning wrapped element (self)
        fake = make_fake_element("GraphEdge")
        fake.embedNewFlow.return_value = fake  # returns the same edge
        edge = RPGraphEdge(fake)
        result = edge.embed_new_flow()
        fake.embedNewFlow.assert_called_once_with()
        # Result is the graph edge itself (wrapped)
        assert result is not None
```

For the remaining 12 classes (`RPConditionMark`, `RPConnector`, `RPGraphicalProperty`, `RPImageMap`, `RPLink`, `RPMatrixLayout`, `RPMatrixView`, `RPMessagePoint`, `RPTableLayout`, `RPTableView`, `RPPin`, `RPGraphNode`) — add a `TestRP<ClassName>Task15` class with at least: (a) one `test_is_registered` test, (b) one method test per Pattern family that the class uses. Reference the two classes above as the template. Notable examples:
- `RPConnector` — 8 `is*_connector` methods (all Pattern G), 2 `set*` methods taking wrapped elements (Pattern F via `target._com`)
- `RPPin` — `get_pin_type` (Pattern B returning `RPClassifier`), `set_pin_type` (Pattern F)
- `RPGraphNode` — `bring_to_front`/`send_to_back`/`hide_all_ports`/`show_all_ports` (all Pattern F void)
- `RPTableLayout` — `add_column` (Pattern F, 3 str args), `add_column_ex` (Pattern E, returns int), 30+ `get_column_*`/`set_column_*` parameterized methods (use `call_com` directly)

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_graphics.py -v`

Expected: FAIL — `NotImplementedError` (stubs) or `AssertionError` (registration missing)

- [ ] **Step 3: Implement ~189 methods across 14 classes**

Replace each `raise NotImplementedError` stub using the Pattern mapping above. Work class-by-class. For the 4 classes with `pass` bodies that have no own methods (`RPConditionMark`), only add registration — no method implementation needed.

- [ ] **Step 4: Add 14 `register_wrapper` calls**

Add `AbstractRPModelElement` to the runtime import from `rhapsody_cli.models.core`, then add the 14 registration calls listed in the Registration notes section above at the bottom of the file.

- [ ] **Step 5: Verify `graphics/__init__.py`** — all 14 classes are already exported (confirmed). No changes needed.

- [ ] **Step 6: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_graphics.py -v`

Expected: ALL PASS

- [ ] **Step 7: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 8: Commit**

```bash
git add src/rhapsody_cli/models/elements/graphics/model_graphics.py \
       src/rhapsody_cli/models/elements/graphics/__init__.py \
       tests/unit/models/elements/test_graphics.py
git commit -m "feat(graphics): implement 14 graphics classes (~190 methods)"
```

---

### Task 16: Common — Misc Remaining (RPEnumerationLiteral, RPConstraint) — 3 methods

**Files:**
- Modify: `src/rhapsody_cli/models/elements/common/model_misc.py`
- Expand: `tests/unit/models/elements/test_misc.py`

**Critical note:** Both `RPEnumerationLiteral` and `RPConstraint` are **already registered** — `register_wrapper("EnumerationLiteral", RPEnumerationLiteral)` and `register_wrapper("Constraint", RPConstraint)` already exist at the bottom of `model_misc.py`. **No registration changes needed.** This task only implements the 3 unchecked methods (the class bodies are currently `pass`).

**Import notes:** `model_misc.py` imports `AbstractRPModelElement`, `RPModelElement` at runtime. To implement `RPConstraint.get_constraints_by_me` (Pattern C, returns `RPCollection`), add `RPCollection` to the runtime import:
```python
from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
```

**Registration notes:** Already done — no changes. Both classes have working `register_wrapper` calls (verified by existing tests `test_enumeration_literal_is_registered` and `test_constraint_is_registered` in `test_misc.py`).

**Pattern mapping:**
- `RPEnumerationLiteral.get_value()` → **Pattern A** (no-arg getter returning primitive `str`) — use `_get_method_or_property(self._com, "getValue", "value")` wrapped in `str(...)`
- `RPEnumerationLiteral.set_value(value: str)` → **Pattern D** (single-arg setter) — use `_set_method_or_property(self._com, "setValue", "value", value)`
- `RPConstraint.get_constraints_by_me()` → **Pattern C** (no-arg getter returning `RPCollection`) — use `RPCollection(_get_method_or_property(self._com, "getConstraintsByMe", "constraintsByMe"))`

- [ ] **Step 1: Write failing tests**

Expand `tests/unit/models/elements/test_misc.py` with method tests for both classes:
```python
"""Tests for RPEnumerationLiteral and RPConstraint methods — added in Task 16."""

from rhapsody_cli.models.core import RPCollection
from rhapsody_cli.models.elements.common.model_misc import (
    RPConstraint,
    RPEnumerationLiteral,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


class TestRPEnumerationLiteralTask16:
    def test_get_value_returns_str(self) -> None:
        # Pattern A — no-arg getter returning primitive
        fake = make_fake_element("EnumerationLiteral")
        fake.getValue.return_value = "RED"
        literal = RPEnumerationLiteral(fake)
        assert literal.get_value() == "RED"
        fake.getValue.assert_called_once_with()

    def test_set_value_delegates(self) -> None:
        # Pattern D — single-arg setter (str)
        fake = make_fake_element("EnumerationLiteral")
        fake.setValue.return_value = None
        literal = RPEnumerationLiteral(fake)
        literal.set_value("BLUE")
        fake.setValue.assert_called_once_with("BLUE")


class TestRPConstraintTask16:
    def test_get_constraints_by_me_returns_collection(self) -> None:
        # Pattern C — no-arg getter returning RPCollection
        fake = make_fake_element("Constraint")
        inner = make_fake_element("Constraint", getName="InnerConstraint")
        fake.getConstraintsByMe.return_value = make_fake_collection([inner])
        constraint = RPConstraint(fake)
        result = constraint.get_constraints_by_me()
        assert isinstance(result, RPCollection)
        fake.getConstraintsByMe.assert_called_once_with()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/models/elements/test_misc.py::TestRPEnumerationLiteralTask16 tests/unit/models/elements/test_misc.py::TestRPConstraintTask16 -v`

Expected: FAIL — `AttributeError` (methods don't exist yet, since class bodies are `pass`)

- [ ] **Step 3: Implement 3 methods in `model_misc.py`**

Add `RPCollection` to the runtime import, then replace the `pass` body in `RPEnumerationLiteral` with:
```python
def get_value(self) -> str:
    """Returns the value of the enumeration literal.

    Returns:
        The enumeration literal's value as a string.

    Reference:
        com.telelogic.rhapsody.core.IRPEnumerationLiteral::getValue()
    """
    return str(AbstractRPModelElement._get_method_or_property(self._com, "getValue", "value"))

def set_value(self, value: str) -> None:
    """Sets the value of the enumeration literal.

    Args:
        value: The value to set for the enumeration literal.

    Reference:
        com.telelogic.rhapsody.core.IRPEnumerationLiteral::setValue(java.lang.String value)
    """
    AbstractRPModelElement._set_method_or_property(self._com, "setValue", "value", value)
```

Replace the `pass` body in `RPConstraint` with:
```python
def get_constraints_by_me(self) -> RPCollection:
    """Returns the collection of constraints owned by this constraint element.

    Returns:
        An ``RPCollection`` of constraints owned by this element.

    Raises:
        RhapsodyRuntimeException: If the constraints cannot be retrieved.

    Reference:
        com.telelogic.rhapsody.core.IRPConstraint::getConstraintsByMe()
    """
    return RPCollection(AbstractRPModelElement._get_method_or_property(self._com, "getConstraintsByMe", "constraintsByMe"))
```

- [ ] **Step 4: Run tests to verify pass**

Run: `pytest tests/unit/models/elements/test_misc.py -v`

Expected: ALL PASS (including new method tests and existing registration tests)

- [ ] **Step 5: Quality gate**

Run: `ruff check src/ tests/` + `black --check <changed files>` + `pytest tests/unit -x`

- [ ] **Step 6: Commit**

```bash
git add src/rhapsody_cli/models/elements/common/model_misc.py \
       tests/unit/models/elements/test_misc.py
git commit -m "feat(common): implement RPEnumerationLiteral + RPConstraint methods (3 methods)"
```

---

### Task 17: Registration Sweep — Safety Net

**Note:** This is a safety-net task. Most classes will already be registered by Tasks 0-16. This task ensures no class was missed. If all classes are already registered, skip directly to Step 3.

**Files that may still need `register_wrapper`:**
- `activity/model_actions.py` — 7 classes (registered in Task 7)
- `activity/model_activity.py` — 5 classes (registered in Task 8)
- `classifiers/model_classifier.py` — `RPClassifier` (abstract base, may not need registration)
- `classifiers/model_interface_item.py` — `RPInterfaceItem` (registered in Task 9)
- `diagrams/model_diagram_types.py` — 11 classes (registered in Task 13)
- `graphics/model_graphics.py` — 14 classes (registered in Task 15)
- `interactions/model_interactions.py` — 11 classes (registered in Task 2)
- `relations/model_relation.py` — `RPRelation` (registered in Task 10)
- `templates/model_templates.py` — 3 classes (registered in Task 5)
- `values/model_values.py` — 5 classes (registered in Task 4)
- `variables/model_variables.py` — `RPVariable` (registered in Task 6)

**Abstract base classes that do NOT need registration:** `RPModelElement`, `RPUnit`, `RPClassifier`, `RPStateVertex`, `RPVariable` (base), `RPValueSpecification` (base), `RPDiagram` (already registered as "ActivityDiagram"), `RPStatechart` (already registered), `RPClass` (already registered). These are never instantiated directly via `wrap()` — their subclasses are registered instead.

```python
AbstractRPModelElement.register_wrapper("MetaClassName", RPClassName)
```

at the module level (bottom of file, after class definitions). Each registration call must match the metaclass string returned by `getMetaClass()` in the COM API.

---

### Task 18: Update Convenience Methods Using `wrap()`

**Files:**
- `classifiers/model_classifier.py` — `add_port(name)` currently uses bare `wrap()` — it already works generically, but verify it resolves correctly
- `containment/model_package.py` — `add_interface`, `add_signal`, `add_exception`, `add_enumeration` — now that Interface/Signal/Exception/Enumeration wrappers exist, verify `wrap()` resolves them
- All `cast("RPSomeThing", ...)` calls — these are typing-only annotations (`typing.cast` does nothing at runtime). They are used for static type checkers only and do not affect `wrap()` behavior. No change needed.

- [ ] **Step 1: Run the existing tests** to verify all current behavior

Run: `pytest tests/unit/models/elements/test_package.py -v`

Expected: PASS — the `add_interface` test uses `make_fake_element("Classifier", ...)` which will still work (the test creates its own fake, not through `wrap()`)

- [ ] **Step 2: Add integration test** for `wrap()` resolution of the 4 new types

Add to `test_package.py`:
```python
def test_package_add_interface_returns_registered_wrapper() -> None:
    from rhapsody_cli.models.elements.classifiers import RPInterface
    fake = make_fake_element("Package")
    iface = make_fake_element("Interface", getName="IFoo")
    fake.addInterface.return_value = iface
    package = RPPackage(fake)
    result = package.add_interface("IFoo")
    assert isinstance(result, RPInterface)
```

Similarly for `add_signal` → `RPSignal`, `add_exception` → `RPException`, `add_enumeration` → `RPEnumeration`.

- [ ] **Step 3: Quality gate**

- [ ] **Step 4: Commit**

---

### Task 19: Final Quality Gate

- [ ] **Step 1: Run full test suite**

```bash
pytest tests/unit/ -v
```

Expected: ALL PASS (0 failures)

- [ ] **Step 2: Run linters**

```bash
ruff check src/ tests/
black --check src/rhapsody_cli/models/ tests/unit/models/
```

- [ ] **Step 3: Run mypy (if Python < 3.10)**

```bash
mypy src/ tests/
```

- [ ] **Step 4: Fix any issues found**

- [ ] **Step 5: Verify checklist updates**

Spot-check 3-4 model files to ensure:
- All `[ ]` are updated to `[x]` for implemented methods
- All methods have `register_wrapper` if applicable
- All methods have tests

- [ ] **Step 6: Commit final changes**

```bash
git add -A
git commit -m "chore: full model class implementation sweep with register_wrapper"
```
