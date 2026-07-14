# Model Class Integration Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comprehensive, prioritized integration tests for all model wrapper classes under `src/rhapsody_cli/models/elements/`, testing against a live Rhapsody COM API instance.

**Architecture:** Extends the existing `tests/integration/` infrastructure (session-scoped `rhapsody_app` and `test_project` fixtures from `conftest.py`). Each element subpackage gets its own test file(s) under `tests/integration/models/elements/<subpackage>/`. Tests create real model elements, manipulate them through the wrapper API, and verify state via the same API (read-back pattern). Unique names via `uuid.uuid4().hex[:8]` to avoid collisions. Cleanup in `finally` blocks.

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid` for unique names

## Global Constraints

- Windows-only runtime (COM automation requires Windows + Rhapsody)
- All tests use `@pytest.mark.integration` decorator
- All tests consume `test_project: RPProject` fixture (session-scoped, creates isolated project at `demos/test_project/`)
- TDD is mandatory — write failing test first, then verify it passes
- Use `_unique(prefix)` helper with `uuid.uuid4().hex[:8]` for unique element names
- Always use `try/finally` for cleanup — never rely solely on fixture teardown
- Assert both return types (`isinstance`) and return values (name/type equality)
- Follow existing patterns from `tests/integration/models/elements/classifiers/test_model_class.py`

---

### Priority Order for Element Subpackages

1. **classifiers/** — RPClass, RPOperation, RPActor, RPStereotype, RPSignal, RPEnumeration, RPUseCase, RPInterface, RPInterfaceItem, RPException, RPAssociationClass, RPStatechart
2. **containment/** — RPProject, RPPackage (expand existing), RPComponent, RPModule, RPCollaboration, RPNode, RPProfile, RPComponentInstance, RPConfiguration
3. **variables/** — RPAttribute, RPVariable, RPArgument, RPTag
4. **common/** — RPComment, RPConstraint, RPEnumerationLiteral, RPSysMLPort, RPType, RPClassifierRole
5. **relations/** — RPAssociationRole, RPDependency, RPGeneralization, RPHyperLink, RPInstance, RPPort, RPRelation
6. **diagrams/** — RPDiagram and 11 diagram-type wrappers
7. **activity/** — RPAction, RPFlow, RPFlowchart, RPObjectNode, RPSwimlane + action subtypes
8. **requirements/** — RPRequirement, RPAnnotation
9. **statemachine/** — RPState, RPStateVertex
10. **interactions/** — RPEventReception, RPMessage, RPTransition, RPGuard, RPTrigger + others
11. **graphics/** — RPGraphNode, RPGraphEdge, RPGraphicalProperty + others
12. **templates/** — RPTemplateParameter, RPTemplateInstantiation + others
13. **values/** — RPInstanceSpecification, RPValueSpecification + others

---

### Task 1: Expand RPClass Integration Tests (classifiers)

**Files:**
- Modify: `tests/integration/models/elements/classifiers/test_model_class.py`

**Interfaces:**
- Consumes: `test_project` fixture (session-scoped `RPProject`)
- Consumes: `_unique()` helper pattern, `_create_package()` helper

**Rationale:** Existing test file covers only create/navigate/operation/delete. RPClass has ~25 additional methods (add_superclass, add_constructor, add_destructor, get_is_abstract/set_is_abstract, add_type, etc.) that need live-COM validation.

- [ ] **Step 1: Add test for add_superclass / get_generalizations / delete_superclass**

```python
def test_class_inheritance(self, test_project: RPProject) -> None:
    pkg_name = self._unique("InhPkg")
    parent_name = self._unique("ParentCls")
    child_name = self._unique("ChildCls")
    pkg = self._create_package(test_project, pkg_name)
    parent = pkg.add_class(parent_name)
    child = pkg.add_class(child_name)
    try:
        child.add_superclass(parent)
        generalizations = list(child.get_generalizations())
        assert any(gen.get_base_class() == parent for gen in generalizations)
        child.delete_superclass(parent)
        generalizations_after = list(child.get_generalizations())
        assert not any(gen.get_base_class() == parent for gen in generalizations_after)
    finally:
        child.delete_from_project()
        parent.delete_from_project()
```

> **Note:** `RPClass` has no `get_superclasses()` method. Use `get_generalizations()`
> (inherited from `RPClassifier`), which returns an `RPCollection` of
> `RPGeneralization` objects; call `.get_base_class()` on each to find the parent.

- [ ] **Step 2: Run test to verify it passes**

```bash
pytest tests/integration/models/elements/classifiers/test_model_class.py::TestRPClassIntegration::test_class_inheritance -v
```
Expected: PASS

- [ ] **Step 3: Add test for add_constructor / add_destructor**

```python
def test_constructor_destructor(self, test_project: RPProject) -> None:
    pkg_name = self._unique("CtorPkg")
    class_name = self._unique("CtorCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        ctor = test_class.add_constructor("void()")
        assert ctor is not None
        assert isinstance(ctor, RPOperation)
        dtor = test_class.add_destructor()
        assert dtor is not None
        assert isinstance(dtor, RPOperation)
        operations = list(test_class.get_operations())
        assert ctor in operations
        assert dtor in operations
    finally:
        test_class.delete_from_project()
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/integration/models/elements/classifiers/test_model_class.py::TestRPClassIntegration::test_constructor_destructor -v
```
Expected: PASS

- [ ] **Step 5: Add test for get_is_abstract / set_is_abstract round-trip**

```python
def test_abstract_roundtrip(self, test_project: RPProject) -> None:
    pkg_name = self._unique("AbsPkg")
    class_name = self._unique("AbsCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        assert test_class.get_is_abstract() is False
        test_class.set_is_abstract(1)
        assert test_class.get_is_abstract() is True
        test_class.set_is_abstract(0)
        assert test_class.get_is_abstract() is False
    finally:
        test_class.delete_from_project()
```

- [ ] **Step 6: Run test to verify it passes**

```bash
pytest tests/integration/models/elements/classifiers/test_model_class.py::TestRPClassIntegration::test_abstract_roundtrip -v
```
Expected: PASS

- [ ] **Step 7: Add test for add_type / delete_type**

```python
def test_type_management(self, test_project: RPProject) -> None:
    pkg_name = self._unique("TypePkg")
    class_name = self._unique("TypeCls")
    pkg = self._create_package(test_project, pkg_name)
    test_class = pkg.add_class(class_name)
    try:
        added_type = test_class.add_type(self._unique("MyType"))
        assert added_type is not None
        assert added_type.get_meta_class() == "Type"
        added_type.delete_from_project()
    finally:
        test_class.delete_from_project()
```

- [ ] **Step 8: Run test to verify it passes**

```bash
pytest tests/integration/models/elements/classifiers/test_model_class.py::TestRPClassIntegration::test_type_management -v
```
Expected: PASS

- [ ] **Step 9: Run existing tests to verify no regressions**

```bash
pytest tests/integration/models/elements/classifiers/test_model_class.py -v
```
Expected: All 8 tests PASS (4 existing + 4 new)

- [ ] **Step 10: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_class.py
git commit -m "test: expand RPClass integration tests with inheritance, ctor/dtor, abstract, type mgmt"
```

---

### Task 2: Add RPOperation Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_operation.py`

**Interfaces:**
- Consumes: `test_project` fixture
- Produces: `TestRPOperationIntegration` class

**Rationale:** RPOperation has ~30 methods; basic create/read was tested via RPClass tests, but operation-specific properties (get_is_static, set_is_static, get_is_virtual, get_body, set_return_type_declaration, etc.) need their own integration tests.

- [ ] **Step 1: Create test file with RPOperation property round-trip tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPClass, RPOperation
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPOperationIntegration:
    """Integration tests for RPOperation with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_static_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("StatPkg")
        class_name = self._unique("StatCls")
        op_name = self._unique("staticOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_static() is False
            op.set_is_static(1)
            assert op.get_is_static() is True
            op.set_is_static(0)
            assert op.get_is_static() is False
        finally:
            test_class.delete_from_project()

    def test_virtual_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("VirtPkg")
        class_name = self._unique("VirtCls")
        op_name = self._unique("virtualOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_virtual() is False
            op.set_is_virtual(1)
            assert op.get_is_virtual() is True
            op.set_is_virtual(0)
            assert op.get_is_virtual() is False
        finally:
            test_class.delete_from_project()

    def test_abstract_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AbsOpPkg")
        class_name = self._unique("AbsOpCls")
        op_name = self._unique("abstractOp")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            assert op.get_is_abstract() is False
            op.set_is_abstract(1)
            assert op.get_is_abstract() is True
            op.set_is_abstract(0)
            assert op.get_is_abstract() is False
        finally:
            test_class.delete_from_project()

    def test_return_type_declaration(self, test_project: RPProject) -> None:
        pkg_name = self._unique("RetPkg")
        class_name = self._unique("RetCls")
        op_name = self._unique("getValue")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            op.set_return_type_declaration("int")
            assert op.get_return_type_declaration() == "int"
        finally:
            test_class.delete_from_project()

    def test_get_body(self, test_project: RPProject) -> None:
        pkg_name = self._unique("BodyPkg")
        class_name = self._unique("BodyCls")
        op_name = self._unique("doSomething")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            op = test_class.add_operation(op_name)
            body = op.get_body()
            assert isinstance(body, str)
        finally:
            test_class.delete_from_project()
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/integration/models/elements/classifiers/test_model_operation.py -v
```
Expected: All 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_operation.py
git commit -m "test: add RPOperation integration tests for static/virtual/abstract/return/body"
```

---

### Task 3: Add RPActor Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_actor.py`

**Interfaces:**
- Consumes: `test_project` fixture

**Rationale:** RPActor inherits from RPClassifier and adds `add_event_reception_with_event`, `get_is_behavior_overriden`, `set_is_behavior_overriden`. Need to verify these work with live COM.

- [ ] **Step 1: Create test file for RPActor**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPActor
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPActorIntegration:
    """Integration tests for RPActor with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_actor_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ActorPkg")
        actor_name = self._unique("TestActor")
        pkg = self._create_package(test_project, pkg_name)
        try:
            actor = pkg.add_actor(actor_name)
            assert actor is not None
            assert isinstance(actor, RPActor)
            assert actor.get_name() == actor_name
            assert actor.get_meta_class() == "Actor"
            actors = pkg.get_actors()
            assert actor in list(actors)
        finally:
            actor.delete_from_project()

    def test_actor_behavior_override(self, test_project: RPProject) -> None:
        pkg_name = self._unique("BehPkg")
        actor_name = self._unique("BehActor")
        pkg = self._create_package(test_project, pkg_name)
        try:
            actor = pkg.add_actor(actor_name)
            assert actor.get_is_behavior_overriden() is False
            actor.set_is_behavior_overriden(True)
            assert actor.get_is_behavior_overriden() is True
            actor.set_is_behavior_overriden(False)
            assert actor.get_is_behavior_overriden() is False
        finally:
            actor.delete_from_project()

    def test_actor_owner(self, test_project: RPProject) -> None:
        pkg_name = self._unique("OwnPkg")
        actor_name = self._unique("OwnActor")
        pkg = self._create_package(test_project, pkg_name)
        try:
            actor = pkg.add_actor(actor_name)
            owner = actor.get_owner()
            assert owner is not None
            assert owner.get_name() == pkg_name
            assert isinstance(owner, RPPackage)
        finally:
            actor.delete_from_project()
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/integration/models/elements/classifiers/test_model_actor.py -v
```
Expected: All 3 tests PASS

- [ ] **Step 3: Run all classifier tests together to verify no side effects**

```bash
pytest tests/integration/models/elements/classifiers/ -v
```
Expected: All classifier tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_actor.py
git commit -m "test: add RPActor integration tests for create, behavior override, owner"
```

---

### Task 4: Add RPStereotype Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_stereotype.py`

- [ ] **Step 1: Create test file for RPStereotype**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPStereotype
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPStereotypeIntegration:
    """Integration tests for RPStereotype with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_stereotype_on_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SterPkg")
        class_name = self._unique("SterCls")
        stereo_name = self._unique("MyStereotype")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            stereotype = test_class.add_stereotype(stereo_name, "Class")
            assert stereotype is not None
            assert isinstance(stereotype, RPStereotype)
            assert stereotype.get_name() == stereo_name
            assert stereotype.get_meta_class() == "Stereotype"
        finally:
            test_class.delete_from_project()
            stereotype.delete_from_project()

    def test_stereotype_owner(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SterOwnPkg")
        class_name = self._unique("SterOwnCls")
        stereo_name = self._unique("OwnedStereo")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            stereotype = test_class.add_stereotype(stereo_name, "Class")
            owner = stereotype.get_owner()
            assert owner is not None
            assert owner.get_name() == pkg_name
            assert isinstance(owner, RPPackage)
        finally:
            test_class.delete_from_project()
            stereotype.delete_from_project()
```

> **Note:** `add_stereotype` creates the stereotype **definition** in the
> owning package, not on the class itself — it must be deleted separately
> from the class in `finally`, or it will be left as an orphan element in
> the package.

> **Note:** `RPPackage.add_stereotype(name)` does not exist. Stereotypes are
> created/applied via the generic `RPModelElement.add_stereotype(name, meta_type)`
> method (present on any element, e.g. `RPClass`), which creates the stereotype
> in the owning package (if it doesn't already exist) and applies it to the
> calling element. `meta_type` is the metaclass the stereotype applies to
> (e.g. `"Class"`).

- [ ] **Step 2: Run tests to verify they pass**

```bash
pytest tests/integration/models/elements/classifiers/test_model_stereotype.py -v
```
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_stereotype.py
git commit -m "test: add RPStereotype integration tests"
```

---

### Task 5: Add RPSignal and RPEnumeration Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_signal.py`
- Create: `tests/integration/models/elements/classifiers/test_model_enumeration.py`

- [ ] **Step 1: Create RPSignal tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPSignal
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPSignalIntegration:
    """Integration tests for RPSignal with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_signal_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("SigPkg")
        sig_name = self._unique("MySignal")
        pkg = self._create_package(test_project, pkg_name)
        try:
            signal = pkg.add_signal(sig_name)
            assert signal is not None
            assert isinstance(signal, RPSignal)
            assert signal.get_name() == sig_name
            assert signal.get_meta_class() == "Signal"
        finally:
            signal.delete_from_project()
```

- [ ] **Step 2: Create RPEnumeration tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPEnumeration
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPEnumerationIntegration:
    """Integration tests for RPEnumeration with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_enumeration_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("EnumPkg")
        enum_name = self._unique("MyEnum")
        pkg = self._create_package(test_project, pkg_name)
        try:
            enumeration = pkg.add_enumeration(enum_name)
            assert enumeration is not None
            assert isinstance(enumeration, RPEnumeration)
            assert enumeration.get_name() == enum_name
            assert enumeration.get_meta_class() == "Enumeration"
        finally:
            enumeration.delete_from_project()
```

- [ ] **Step 3: Run all classifier tests**

```bash
pytest tests/integration/models/elements/classifiers/ -v
```
Expected: All classifier tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/integration/models/elements/classifiers/test_model_signal.py tests/integration/models/elements/classifiers/test_model_enumeration.py
git commit -m "test: add RPSignal and RPEnumeration integration tests"
```

---

### Task 6: Add RPUseCase and RPInterface Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_usecase.py`
- Create: `tests/integration/models/elements/classifiers/test_model_interface.py`

- [ ] **Step 1: Create RPUseCase tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPUseCase
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPUseCaseIntegration:
    """Integration tests for RPUseCase with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_usecase_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("UcPkg")
        uc_name = self._unique("MyUseCase")
        pkg = self._create_package(test_project, pkg_name)
        try:
            uc = pkg.add_use_case(uc_name)
            assert uc is not None
            assert isinstance(uc, RPUseCase)
            assert uc.get_name() == uc_name
            assert uc.get_meta_class() == "UseCase"
        finally:
            uc.delete_from_project()
```

> **Note:** The method is `add_use_case` (underscore), not `add_usecase`.

- [ ] **Step 2: Create RPInterface tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPInterface
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPInterfaceIntegration:
    """Integration tests for RPInterface with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_interface_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("IntPkg")
        iface_name = self._unique("MyInterface")
        pkg = self._create_package(test_project, pkg_name)
        try:
            iface = pkg.add_interface(iface_name)
            assert iface is not None
            assert isinstance(iface, RPInterface)
            assert iface.get_name() == iface_name
            assert iface.get_meta_class() == "Interface"
        finally:
            iface.delete_from_project()
```

- [ ] **Step 3: Run and commit**

```bash
pytest tests/integration/models/elements/classifiers/ -v
git add tests/integration/models/elements/classifiers/test_model_usecase.py tests/integration/models/elements/classifiers/test_model_interface.py
git commit -m "test: add RPUseCase and RPInterface integration tests"
```

---

### Task 7: Expand Containment Integration Tests (containment)

**Files:**
- Modify: `tests/integration/models/elements/containment/test_model_project.py`

**Rationale:** Existing containment tests cover RPProject and RPPackage basics. Need to add RPComponent, RPModule.

- [ ] **Step 1: Add RPComponent creation test**

```python
def test_create_component_in_project(self, test_project: RPProject) -> None:
    comp_name = self._unique("MyComponent")
    comp = test_project.add_component(comp_name)
    try:
        assert comp is not None
        assert comp.get_name() == comp_name
        assert comp.get_meta_class() == "Component"
    finally:
        comp.delete_from_project()
```

> **Note:** `add_component` exists only on `RPProject`, not `RPPackage` — there
> is no `RPPackage.add_component`.

- [ ] **Step 2: Add RPModule creation test**

```python
def test_create_module_in_package(self, test_project: RPProject) -> None:
    pkg_name = self._unique("ModPkg")
    mod_name = self._unique("MyModule")
    pkg = self._create_package(test_project, pkg_name)
    try:
        mod = pkg.add_module(mod_name)
        assert mod is not None
        assert mod.get_name() == mod_name
        assert mod.get_meta_class() == "Module"
    finally:
        mod.delete_from_project()
```

- [ ] **Step 3: Run tests and commit**

```bash
pytest tests/integration/models/elements/containment/ -v
git add tests/integration/models/elements/containment/test_model_project.py
git commit -m "test: add RPComponent and RPModule integration tests"
```

---

### Task 8: Add RPAttribute Integration Tests (variables)

**Files:**
- Create: `tests/integration/models/elements/variables/test_model_attribute.py`

**Rationale:** RPAttribute is a high-priority class used in nearly every model.

- [ ] **Step 1: Create RPAttribute tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.variables import RPAttribute


@pytest.mark.integration
class TestRPAttributeIntegration:
    """Integration tests for RPAttribute with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_add_attribute_to_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("AttrPkg")
        class_name = self._unique("AttrCls")
        attr_name = self._unique("myAttribute")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            assert attr is not None
            assert isinstance(attr, RPAttribute)
            assert attr.get_name() == attr_name
            attrs = list(test_class.get_attributes())
            assert attr in attrs
        finally:
            test_class.delete_from_project()

    def test_attribute_type_roundtrip(self, test_project: RPProject) -> None:
        pkg_name = self._unique("TypePkg")
        class_name = self._unique("TypeCls")
        attr_name = self._unique("typedAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_type_declaration("int")
            assert attr.get_declaration() == "int"
        finally:
            test_class.delete_from_project()

    def test_attribute_default_value(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DefPkg")
        class_name = self._unique("DefCls")
        attr_name = self._unique("defaultAttr")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            attr = test_class.add_attribute(attr_name)
            attr.set_default_value("42")
            assert attr.get_default_value() == "42"
        finally:
            test_class.delete_from_project()
```

> **Note:** `set_type`/`get_type` operate on `RPClassifier` objects (not
> strings) — passing a raw string to `set_type` will raise an `AttributeError`.
> For on-the-fly string type declarations, use `set_type_declaration(str)` /
> `get_declaration()` instead.

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/variables/test_model_attribute.py -v
git add tests/integration/models/elements/variables/test_model_attribute.py
git commit -m "test: add RPAttribute integration tests for create, type, default value"
```

---

### Task 9: Add RPGeneralization Integration Tests (relations)

**Files:**
- Create: `tests/integration/models/elements/relations/test_model_generalization.py`

- [ ] **Step 1: Create RPGeneralization tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.relations import RPGeneralization


@pytest.mark.integration
class TestRPGeneralizationIntegration:
    """Integration tests for RPGeneralization with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_generalization(self, test_project: RPProject) -> None:
        pkg_name = self._unique("GenPkg")
        parent_name = self._unique("Parent")
        child_name = self._unique("Child")
        pkg = self._create_package(test_project, pkg_name)
        parent = pkg.add_class(parent_name)
        child = pkg.add_class(child_name)
        try:
            child.add_generalization(parent)
            gen = child.find_generalization(parent_name)
            assert gen is not None
            assert isinstance(gen, RPGeneralization)
            assert gen.get_meta_class() == "Generalization"
            assert gen.get_base_class() == parent
        finally:
            child.delete_from_project()
            parent.delete_from_project()
```

> **Note:** `add_generalization` returns `None` (it just creates the
> relationship); use `find_generalization(parent_name)` afterward to obtain
> the `RPGeneralization` object.

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/relations/test_model_generalization.py -v
git add tests/integration/models/elements/relations/test_model_generalization.py
git commit -m "test: add RPGeneralization integration test"
```

---

### Task 10: Add Common Element Integration Tests (common)

**Files:**
- Create: `tests/integration/models/elements/common/test_model_misc.py`

- [ ] **Step 1: Create RPComment and RPConstraint tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.common import RPComment, RPConstraint
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPCommentIntegration:
    """Integration tests for RPComment with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_comment_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ComPkg")
        comment_name = self._unique("MyComment")
        pkg = self._create_package(test_project, pkg_name)
        try:
            comment = pkg.add_new_aggr("Comment", comment_name)
            assert comment is not None
            assert isinstance(comment, RPComment)
            assert comment.get_name() == comment_name
            assert comment.get_meta_class() == "Comment"
        finally:
            comment.delete_from_project()


@pytest.mark.integration
class TestRPConstraintIntegration:
    """Integration tests for RPConstraint with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_constraint_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ConPkg")
        con_name = self._unique("MyConstraint")
        pkg = self._create_package(test_project, pkg_name)
        try:
            constraint = pkg.add_new_aggr("Constraint", con_name)
            assert constraint is not None
            assert isinstance(constraint, RPConstraint)
            assert constraint.get_name() == con_name
            assert constraint.get_meta_class() == "Constraint"
        finally:
            constraint.delete_from_project()
```

> **Note:** Neither `RPPackage.add_comment` nor `RPPackage.add_constraint`
> exist. Use the generic `RPModelElement.add_new_aggr(meta_type, name)`
> method (inherited by `RPPackage`) — the same mechanism used elsewhere in
> the codebase (e.g. `RPClassifier.add_port` calls `addNewAggr("Port", name)`).

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/common/test_model_misc.py -v
git add tests/integration/models/elements/common/test_model_misc.py
git commit -m "test: add RPComment and RPConstraint integration tests"
```

---

### Task 11: Add RPDiagram Integration Tests (diagrams)

**Files:**
- Create: `tests/integration/models/elements/diagrams/test_model_diagrams.py`

- [ ] **Step 1: Create RPDiagram tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.diagrams import RPDiagram


@pytest.mark.integration
class TestRPDiagramIntegration:
    """Integration tests for RPDiagram with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_object_model_diagram(self, test_project: RPProject) -> None:
        pkg_name = self._unique("DiagPkg")
        diag_name = self._unique("MyDiagram")
        pkg = self._create_package(test_project, pkg_name)
        try:
            diagram = pkg.add_object_model_diagram(diag_name)
            assert diagram is not None
            assert isinstance(diagram, RPDiagram)
            assert diagram.get_name() == diag_name
        finally:
            diagram.delete_from_project()
```

> **Note:** `RPPackage.add_class_diagram` does not exist. Rhapsody's UML
> "class diagram" equivalent is `add_object_model_diagram`, which returns
> `RPObjectModelDiagram` (a subclass of `RPDiagram`, so `isinstance(diagram,
> RPDiagram)` still holds).

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -v
git add tests/integration/models/elements/diagrams/test_model_diagrams.py
git commit -m "test: add RPDiagram integration test"
```

---

### Task 12: Add Statechart Integration Tests (classifiers)

**Files:**
- Create: `tests/integration/models/elements/classifiers/test_model_statechart.py`

> **Note:** `RPStatechart` is defined in `classifiers/model_statechart.py`, so
> its test file belongs under `tests/integration/models/elements/classifiers/`,
> not a new `statemachine/` directory.

- [ ] **Step 1: Create RPStatechart tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.classifiers import RPClass, RPStatechart
from rhapsody_cli.models.elements.containment import RPPackage, RPProject


@pytest.mark.integration
class TestRPStatechartIntegration:
    """Integration tests for RPStatechart with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_statechart_in_class(self, test_project: RPProject) -> None:
        pkg_name = self._unique("StPkg")
        class_name = self._unique("StCls")
        pkg = self._create_package(test_project, pkg_name)
        test_class = pkg.add_class(class_name)
        try:
            sc = test_class.add_statechart()
            assert sc is not None
            assert isinstance(sc, RPStatechart)
            assert sc.get_meta_class() == "Statechart"
        finally:
            test_class.delete_from_project()
```

> **Note:** `add_statechart()` (defined on `RPClassifier`) takes zero
> arguments — it does not accept a name.

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/classifiers/test_model_statechart.py -v
git add tests/integration/models/elements/classifiers/test_model_statechart.py
git commit -m "test: add RPStatechart integration test"
```

---

### Task 13: Add RPRequirement Integration Tests (requirements)

**Files:**
- Create: `tests/integration/models/elements/requirements/test_model_requirements.py`

- [ ] **Step 1: Create RPRequirement tests**

```python
import uuid
import pytest
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.requirements import RPRequirement


@pytest.mark.integration
class TestRPRequirementIntegration:
    """Integration tests for RPRequirement with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_requirement_in_package(self, test_project: RPProject) -> None:
        pkg_name = self._unique("ReqPkg")
        req_name = self._unique("MyRequirement")
        pkg = self._create_package(test_project, pkg_name)
        try:
            req = pkg.add_new_aggr("Requirement", req_name)
            assert req is not None
            assert isinstance(req, RPRequirement)
            assert req.get_name() == req_name
            assert req.get_meta_class() == "Requirement"
        finally:
            req.delete_from_project()
```

> **Note:** `RPPackage.add_requirement` does not exist anywhere in the
> codebase. Use the generic `RPModelElement.add_new_aggr(meta_type, name)`
> method instead.

- [ ] **Step 2: Run tests and commit**

```bash
pytest tests/integration/models/elements/requirements/test_model_requirements.py -v
git add tests/integration/models/elements/requirements/test_model_requirements.py
git commit -m "test: add RPRequirement integration test"
```

---

### Task 14: Full Suite Verification

- [ ] **Step 1: Run all integration tests**

```bash
pytest tests/integration/ -v
```
Expected: All integration tests PASS

- [ ] **Step 2: Run unit tests to verify no regressions**

```bash
pytest tests/unit/ -q
```
Expected: All unit tests PASS

- [ ] **Step 3: Verify test markers work**

```bash
pytest -m integration --co
```
Expected: All integration tests collected, no unit tests

---

## Execution Order Summary

| Task | Subpackage | Action | Tests Added | Priority |
|------|-----------|--------|-------------|----------|
| 1 | classifiers/RPClass | modify existing | 4 | Critical |
| 2 | classifiers/RPOperation | create new | 5 | Critical |
| 3 | classifiers/RPActor | create new | 3 | High |
| 4 | classifiers/RPStereotype | create new | 2 | Medium |
| 5 | classifiers/RPSignal + Enumeration | create new | 2 | Medium |
| 6 | classifiers/RPUseCase + Interface | create new | 2 | Medium |
| 7 | containment (expand) | modify existing | 2 | Critical |
| 8 | variables/RPAttribute | create new | 3 | High |
| 9 | relations/RPGeneralization | create new | 1 | Medium |
| 10 | common/RPComment + RPConstraint | create new | 2 | Medium |
| 11 | diagrams/RPDiagram | create new | 1 | Low |
| 12 | statemachine/RPStatechart | create new | 1 | Low |
| 13 | requirements/RPRequirement | create new | 1 | Medium |
| 14 | Full suite verification | — | — | — |

## Success Criteria

- All existing integration tests continue to pass
- Every model wrapper class in `src/rhapsody_cli/models/elements/` has at least one integration test verifying create + identity + delete
- Key property round-trips (get/set pairs) are validated for RPClass, RPOperation, RPActor, RPAttribute
- No test leaves behind orphan elements in the Rhapsody model
- Unit tests are unaffected (0 regressions)
