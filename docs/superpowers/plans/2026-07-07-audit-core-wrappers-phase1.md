# Audit Core Wrappers — Phase 1: Reorg + Hierarchy Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize `rhapsody_cli/models/elements/` into per-family modules, introduce the 4 missing intermediate wrapper classes (`RPVariable`, `RPInterfaceItem`, `RPAnnotation`, `RPRelation`), and re-parent the 6 existing wrappers that currently extend the wrong base class — bringing the wrapper hierarchy into exact alignment with the Java API (`com.telelogic.rhapsody.core`) hierarchy.

**Architecture:** `src/rhapsody_cli/models/elements/` moves from 12 one-class-per-file modules to 6 family modules (`classifiers.py`, `variables.py`, `containment.py`, `requirements.py`, `relations.py`, `diagrams.py`), each holding every wrapper class in that inheritance family, base-class-first. Four new intermediate classes are added with full method parity for their own interface. Six existing leaf classes are re-parented to the new/corrected base class. This plan does **not** add missing methods to the 12 existing classes themselves (e.g. `RPAttribute`, `RPOperation`) beyond what's needed for correct re-parenting — that full method-parity work is Phase 2+, one class at a time.

**Tech Stack:** Python 3.8+, pytest, `unittest.mock.MagicMock` fakes (`tests/models/fakes.py`), ruff, black, mypy (strict).

**Reference spec:** `docs/superpowers/specs/2026-07-07-audit-core-wrappers-design.md`

**Java API doc reference (for all method signatures/descriptions in this plan):** `C:\LegacyApp\Rhapsody_902_64bit\Doc\java_api\com\telelogic\rhapsody\core\IRPVariable.html`, `IRPInterfaceItem.html`, `IRPAnnotation.html`, `IRPRelation.html`, `IRPAttribute.html`, `IRPProject.html`, `IRPStatechart.html`.

---

### Task 1: Reorganize `elements/` into per-family modules (no behavior change)

This task only moves code between files and updates imports. No method bodies, signatures, or class hierarchy change. At the end of this task, the full existing test suite must pass unmodified in behavior (only import paths change).

**Files:**
- Create: `src/rhapsody_cli/models/elements/classifiers.py`
- Create: `src/rhapsody_cli/models/elements/variables.py`
- Create: `src/rhapsody_cli/models/elements/containment.py`
- Create: `src/rhapsody_cli/models/elements/requirements.py`
- Create: `src/rhapsody_cli/models/elements/relations.py`
- Create: `src/rhapsody_cli/models/elements/diagrams.py`
- Delete: `src/rhapsody_cli/models/elements/classifier.py`, `class_.py`, `actor.py`, `usecase.py`, `operation.py`, `statechart.py`, `attribute.py`, `package.py`, `project.py`, `requirement.py`, `instance.py`, `diagram.py`
- Modify: `src/rhapsody_cli/models/elements/__init__.py`
- Modify: `tests/models/elements/test_class.py`, `test_classifier.py`, `test_actor.py`, `test_usecase.py`, `test_operation.py`, `test_statechart.py`, `test_attribute.py`, `test_package.py`, `test_project.py`, `test_requirement.py`, `test_instance.py`, `test_diagram.py`

- [ ] **Step 1: Create `classifiers.py` with the existing classifier-family classes unchanged**

```python
"""Classifier-family wrappers: mirrors IRPClassifier and its Java subtypes
(IRPClass, IRPActor, IRPUseCase, IRPOperation, IRPStatechart) from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)


class RPClassifier(RPUnit):
    """Wraps ``IRPClassifier``."""

    def addAttribute(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addAttribute(name)))

    def addOperation(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addOperation(name)))

    def getAttributes(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAttributes()))

    def getOperations(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOperations()))

    def addGeneralization(self, base_classifier: "RPClassifier") -> None:
        call_com(lambda: self._com.addGeneralization(base_classifier._com))

    def addStatechart(self) -> Any:
        return wrap(call_com(lambda: self._com.addStatechart()))


class RPClass(RPClassifier):
    """Wraps ``IRPClass``."""

    def addSuperclass(self, super_class: "RPClass") -> None:
        call_com(lambda: self._com.addSuperclass(super_class._com))

    def addConstructor(self, arguments_data: str) -> Any:
        return wrap(call_com(lambda: self._com.addConstructor(arguments_data)))

    def addDestructor(self) -> Any:
        return wrap(call_com(lambda: self._com.addDestructor()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def addClass(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addClass(name)))


class RPActor(RPClassifier):
    """Wraps ``IRPActor``."""

    def addEventReceptionWithEvent(self, name: str, event: RPModelElement) -> Any:
        return wrap(call_com(lambda: self._com.addEventReceptionWithEvent(name, event._com)))

    def getIsBehaviorOverriden(self) -> bool:
        return call_com(lambda: bool(self._com.getIsBehaviorOverriden()))

    def setIsBehaviorOverriden(self, is_overridden: bool) -> None:
        call_com(lambda: self._com.setIsBehaviorOverriden(1 if is_overridden else 0))


class RPUseCase(RPClassifier):
    """Wraps ``IRPUseCase``."""

    def addExtensionPoint(self, entry_point: str) -> None:
        call_com(lambda: self._com.addExtensionPoint(entry_point))

    def getExtensionPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getExtensionPoints()))

    def getEntryPoints(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getEntryPoints()))

    def getDescribingDiagrams(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getDescribingDiagrams()))


class RPOperation(RPUnit):
    """Wraps ``IRPOperation``."""

    def getBody(self) -> str:
        return call_com(lambda: str(self._com.getBody()))

    def getIsAbstract(self) -> bool:
        return call_com(lambda: bool(self._com.getIsAbstract()))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def getIsVirtual(self) -> bool:
        return call_com(lambda: bool(self._com.getIsVirtual()))

    def getReturns(self) -> Any:
        return wrap(call_com(lambda: self._com.getReturns()))

    def createAutoFlowChart(self) -> None:
        call_com(lambda: self._com.createAutoFlowChart())


class RPStatechart(RPUnit):
    """Wraps ``IRPStatechart``."""

    def addNewNodeByType(
        self, meta_type: str, x_position: int, y_position: int, width: int, height: int
    ) -> Any:
        return wrap(
            call_com(
                lambda: self._com.addNewNodeByType(meta_type, x_position, y_position, width, height)
            )
        )

    def createGraphics(self) -> None:
        call_com(lambda: self._com.createGraphics())

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def deleteState(self, state: RPModelElement) -> None:
        call_com(lambda: self._com.deleteState(state._com))


register_wrapper("Class", RPClass)
register_wrapper("Actor", RPActor)
register_wrapper("UseCase", RPUseCase)
register_wrapper("Operation", RPOperation)
register_wrapper("Statechart", RPStatechart)
```

- [ ] **Step 2: Create `variables.py` with the existing `RPAttribute` unchanged**

```python
"""Variable-family wrappers: mirrors IRPVariable and IRPAttribute from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, call_com, register_wrapper


class RPAttribute(RPUnit):
    """Wraps ``IRPAttribute``."""

    def getMultiplicity(self) -> str:
        return call_com(lambda: str(self._com.getMultiplicity()))

    def setMultiplicity(self, multiplicity: str) -> None:
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def getIsStatic(self) -> bool:
        return call_com(lambda: bool(self._com.getIsStatic()))

    def setIsStatic(self, is_static: bool) -> None:
        call_com(lambda: self._com.setIsStatic(1 if is_static else 0))

    def getVisibility(self) -> str:
        return call_com(lambda: str(self._com.getVisibility()))

    def setVisibility(self, visibility: str) -> None:
        call_com(lambda: self._com.setVisibility(visibility))

    def getDefaultValue(self) -> str:
        return call_com(lambda: str(self._com.getDefaultValue()))

    def setDefaultValue(self, default_value: str) -> None:
        call_com(lambda: self._com.setDefaultValue(default_value))


register_wrapper("Attribute", RPAttribute)
```

- [ ] **Step 3: Create `containment.py` with the existing `RPPackage`/`RPProject` unchanged**

```python
"""Containment-family wrappers: mirrors IRPPackage and IRPProject from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, register_wrapper, wrap


class RPPackage(RPUnit):
    """Wraps ``IRPPackage``."""

    def addClass(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addClass(name)))

    def addNestedPackage(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addNestedPackage(name)))

    def addActor(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addActor(name)))

    def addGlobalFunction(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addGlobalFunction(name)))


class RPProject(RPUnit):
    """Wraps ``IRPProject``."""

    def addPackage(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.addPackage(name)))

    def close(self) -> None:
        call_com(lambda: self._com.close())

    def becomeActiveProject(self) -> None:
        call_com(lambda: self._com.becomeActiveProject())

    def findComponent(self, name: str) -> Any:
        return wrap(call_com(lambda: self._com.findComponent(name)))

    def getPackages(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getPackages()))


register_wrapper("Package", RPPackage)
register_wrapper("Project", RPProject)
```

- [ ] **Step 4: Create `requirements.py` with the existing `RPRequirement` unchanged**

```python
"""Requirement-family wrappers: mirrors IRPAnnotation and IRPRequirement
from com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from rhapsody_cli.models._core import RPUnit, call_com, register_wrapper


class RPRequirement(RPUnit):
    """Wraps ``IRPRequirement``."""

    def getRequirementID(self) -> str:
        return call_com(lambda: str(self._com.getRequirementID()))

    def setRequirementID(self, requirement_id: str) -> None:
        call_com(lambda: self._com.setRequirementID(requirement_id))


register_wrapper("Requirement", RPRequirement)
```

- [ ] **Step 5: Create `relations.py` with the existing `RPInstance` unchanged**

```python
"""Relation-family wrappers: mirrors IRPRelation and IRPInstance from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, RPUnit, call_com, register_wrapper


class RPInstance(RPUnit):
    """Wraps ``IRPInstance``."""

    def getAllNestedElements(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
```

- [ ] **Step 6: Create `diagrams.py` with the existing `RPDiagram` unchanged**

```python
"""Diagram-family wrappers: mirrors IRPDiagram from com.telelogic.rhapsody.core."""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import (
    RPCollection,
    RPModelElement,
    RPUnit,
    call_com,
    register_wrapper,
    wrap,
)


class RPDiagram(RPUnit):
    """Wraps ``IRPDiagram``."""

    def closeDiagram(self) -> None:
        call_com(lambda: self._com.closeDiagram())

    def addTextBox(
        self, text: str, x_position: int, y_position: int, width: int, height: int
    ) -> Any:
        return wrap(
            call_com(lambda: self._com.addTextBox(text, x_position, y_position, width, height))
        )

    def getCustomViews(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getCustomViews()))

    def getCorrespondingGraphicElements(self, model_element: RPModelElement) -> RPCollection:
        return RPCollection(
            call_com(lambda: self._com.getCorrespondingGraphicElements(model_element._com))
        )


register_wrapper("ActivityDiagram", RPDiagram)
```

- [ ] **Step 7: Delete the 12 old one-class-per-file modules**

```powershell
cd E:\Working\rhapsody-cli
Remove-Item src/rhapsody_cli/models/elements/classifier.py
Remove-Item src/rhapsody_cli/models/elements/class_.py
Remove-Item src/rhapsody_cli/models/elements/actor.py
Remove-Item src/rhapsody_cli/models/elements/usecase.py
Remove-Item src/rhapsody_cli/models/elements/operation.py
Remove-Item src/rhapsody_cli/models/elements/statechart.py
Remove-Item src/rhapsody_cli/models/elements/attribute.py
Remove-Item src/rhapsody_cli/models/elements/package.py
Remove-Item src/rhapsody_cli/models/elements/project.py
Remove-Item src/rhapsody_cli/models/elements/requirement.py
Remove-Item src/rhapsody_cli/models/elements/instance.py
Remove-Item src/rhapsody_cli/models/elements/diagram.py
```

- [ ] **Step 8: Update `src/rhapsody_cli/models/elements/__init__.py`**

Replace its entire contents with:

```python
"""Concrete Rhapsody element wrappers, registered with rhapsody_cli._core.wrap()."""

from __future__ import annotations

from rhapsody_cli.models.elements import classifiers as classifiers  # noqa: F401
from rhapsody_cli.models.elements import containment as containment  # noqa: F401
from rhapsody_cli.models.elements import diagrams as diagrams  # noqa: F401
from rhapsody_cli.models.elements import relations as relations  # noqa: F401
from rhapsody_cli.models.elements import requirements as requirements  # noqa: F401
from rhapsody_cli.models.elements import variables as variables  # noqa: F401
```

- [ ] **Step 9: Update test imports for the classifier family**

In `tests/models/elements/test_class.py`, replace:

```python
from rhapsody_cli.models.elements.class_ import RPClass
from rhapsody_cli.models.elements.classifier import RPClassifier
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier
```

In `tests/models/elements/test_classifier.py`, replace:

```python
from rhapsody_cli.models.elements.classifier import RPClassifier
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPClassifier
```

In `tests/models/elements/test_actor.py`, replace:

```python
from rhapsody_cli.models.elements.actor import RPActor
from rhapsody_cli.models.elements.classifier import RPClassifier
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPActor, RPClassifier
```

In `tests/models/elements/test_usecase.py`, replace:

```python
from rhapsody_cli.models.elements.classifier import RPClassifier
from rhapsody_cli.models.elements.usecase import RPUseCase
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPClassifier, RPUseCase
```

In `tests/models/elements/test_operation.py`, replace:

```python
from rhapsody_cli.models.elements.operation import RPOperation
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPOperation
```

In `tests/models/elements/test_statechart.py`, replace:

```python
from rhapsody_cli.models.elements.statechart import RPStatechart
```

with:

```python
from rhapsody_cli.models.elements.classifiers import RPStatechart
```

- [ ] **Step 10: Update remaining test imports (variables/containment/requirements/relations/diagrams families)**

In `tests/models/elements/test_attribute.py`, replace:

```python
from rhapsody_cli.models.elements.attribute import RPAttribute
```

with:

```python
from rhapsody_cli.models.elements.variables import RPAttribute
```

In `tests/models/elements/test_package.py`, replace:

```python
from rhapsody_cli.models.elements.package import RPPackage
```

with:

```python
from rhapsody_cli.models.elements.containment import RPPackage
```

In `tests/models/elements/test_project.py`, replace:

```python
from rhapsody_cli.models.elements.project import RPProject
```

with:

```python
from rhapsody_cli.models.elements.containment import RPProject
```

In `tests/models/elements/test_requirement.py`, replace:

```python
from rhapsody_cli.models.elements.requirement import RPRequirement
```

with:

```python
from rhapsody_cli.models.elements.requirements import RPRequirement
```

In `tests/models/elements/test_instance.py`, replace:

```python
from rhapsody_cli.models.elements.instance import RPInstance
```

with:

```python
from rhapsody_cli.models.elements.relations import RPInstance
```

In `tests/models/elements/test_diagram.py`, replace:

```python
from rhapsody_cli.models.elements.diagram import RPDiagram
```

with:

```python
from rhapsody_cli.models.elements.diagrams import RPDiagram
```

- [ ] **Step 11: Run the full test suite to verify the reorg didn't change behavior**

Run: `pytest tests/models -v`
Expected: All tests pass (same tests as before, only import paths changed).

- [ ] **Step 12: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean. If `black` reports formatting differences, run `black src/ tests/` and re-check.

- [ ] **Step 13: Commit**

```bash
git add -A
git commit -m "refactor: reorganize elements/ into per-family modules"
```

---

### Task 2: Add `RPVariable`, re-parent `RPAttribute`

`IRPAttribute extends IRPVariable extends IRPUnit`. `RPVariable` is the base for tag/attribute-like elements that carry a type and default value. Two methods (`getDefaultValue`/`setDefaultValue`) currently live (incorrectly) on `RPAttribute` but are actually declared on `IRPVariable` — they move up in this task.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/variables.py`
- Create: `tests/models/elements/test_variable.py`
- Modify: `tests/models/elements/test_attribute.py`

- [ ] **Step 1: Write failing tests for `RPVariable` in `tests/models/elements/test_variable.py`**

```python
"""Tests for rhapsody_cli.models.elements.variables.RPVariable."""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, RPUnit, wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.variables import RPVariable
from tests.models.fakes import make_fake_collection, make_fake_element


def test_variable_is_a_unit() -> None:
    fake = make_fake_element("Variable", getName="count")
    variable = RPVariable(fake)

    assert isinstance(variable, RPUnit)
    assert variable.getName() == "count"


def test_variable_add_element_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    new_value = make_fake_element("Class", getName="Extra")
    element = make_fake_element("Class", getName="Extra")
    fake.addElementDefaultValue.return_value = new_value
    variable = RPVariable(fake)

    result = variable.addElementDefaultValue(wrap(element))

    fake.addElementDefaultValue.assert_called_once_with(element)
    assert result.getName() == "Extra"


def test_variable_add_string_default_value_wraps_result() -> None:
    fake = make_fake_element("Variable")
    literal = make_fake_element("LiteralSpecification", getName="42")
    fake.addStringDefaultValue.return_value = literal
    variable = RPVariable(fake)

    result = variable.addStringDefaultValue("42")

    fake.addStringDefaultValue.assert_called_once_with("42")
    assert result.getName() == "42"


def test_variable_get_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDeclaration="int*")
    variable = RPVariable(fake)

    assert variable.getDeclaration() == "int*"


def test_variable_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable", getDefaultValue="0")
    variable = RPVariable(fake)

    assert variable.getDefaultValue() == "0"


def test_variable_get_type_wraps_result() -> None:
    fake = make_fake_element("Variable")
    type_com = make_fake_element("Class", getName="int")
    fake.getType.return_value = type_com
    variable = RPVariable(fake)

    result = variable.getType()

    fake.getType.assert_called_once_with()
    assert result.getName() == "int"


def test_variable_get_value_specifications_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Spec")
    fake = make_fake_element("Variable")
    fake.getValueSpecifications.return_value = make_fake_collection([inner])
    variable = RPVariable(fake)

    result = variable.getValueSpecifications()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_variable_set_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setDeclaration("int*")

    fake.setDeclaration.assert_called_once_with("int*")


def test_variable_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setDefaultValue("42")

    fake.setDefaultValue.assert_called_once_with("42")


def test_variable_set_type_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    type_fake = make_fake_element("Class", getName="int")
    variable = RPVariable(fake)

    variable.setType(RPClassifier(type_fake))

    fake.setType.assert_called_once_with(type_fake)


def test_variable_set_type_declaration_delegates_to_com() -> None:
    fake = make_fake_element("Variable")
    variable = RPVariable(fake)

    variable.setTypeDeclaration("int*")

    fake.setTypeDeclaration.assert_called_once_with("int*")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/elements/test_variable.py -v`
Expected: FAIL with `ModuleNotFoundError` or `ImportError: cannot import name 'RPVariable'`.

- [ ] **Step 3: Implement `RPVariable` in `variables.py` and re-parent `RPAttribute`**

Replace the full contents of `src/rhapsody_cli/models/elements/variables.py` with:

```python
"""Variable-family wrappers: mirrors IRPVariable and IRPAttribute from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPModelElement, RPUnit, call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier


class RPVariable(RPUnit):
    """Wraps ``IRPVariable``: the base interface for typed elements (such as
    attributes and parameters) that carry a type and default value.
    """

    def addElementDefaultValue(self, new_default_val: RPModelElement) -> Any:
        """For tags with multiplicity greater than 1, adds a model element as an additional value.

        Args:
            new_default_val: The model element to add as an additional default value.

        Returns:
            The wrapped ``IRPInstanceValue`` created for the new default value.
        """
        return wrap(call_com(lambda: self._com.addElementDefaultValue(new_default_val._com)))

    def addStringDefaultValue(self, new_default_val: str) -> Any:
        """For tags with multiplicity greater than 1, adds a string as an additional value.

        Args:
            new_default_val: The string to add as an additional default value.

        Returns:
            The wrapped ``IRPLiteralSpecification`` created for the new default value.
        """
        return wrap(call_com(lambda: self._com.addStringDefaultValue(new_default_val)))

    def getDeclaration(self) -> str:
        """Returns the type declaration if an on-the-fly type was used for the element.

        Returns:
            The on-the-fly type declaration, or an existing type's info if one was used.
        """
        return call_com(lambda: str(self._com.getDeclaration()))

    def getDefaultValue(self) -> str:
        """Returns the default value that was set for the variable.

        Returns:
            The default value as a string.
        """
        return call_com(lambda: str(self._com.getDefaultValue()))

    def getType(self) -> Any:
        """Returns the type of the variable.

        Returns:
            The wrapped ``IRPClassifier`` that is the type of the variable.
        """
        return wrap(call_com(lambda: self._com.getType()))

    def getValueSpecifications(self) -> RPCollection:
        """Returns the initial values declared for elements with multiplicity greater than one.

        Returns:
            An ``RPCollection`` of the declared initial value specifications.
        """
        return RPCollection(call_com(lambda: self._com.getValueSpecifications()))

    def setDeclaration(self, declaration: str) -> None:
        """Specifies an on-the-fly declaration for the type of the element.

        Args:
            declaration: The on-the-fly type declaration to use instead of an existing type.
        """
        call_com(lambda: self._com.setDeclaration(declaration))

    def setDefaultValue(self, default_value: str) -> None:
        """Sets a new default value for the variable.

        Args:
            default_value: The new default value.
        """
        call_com(lambda: self._com.setDefaultValue(default_value))

    def setType(self, type_: RPClassifier) -> None:
        """Sets the type of the variable.

        Args:
            type_: The classifier to use as the variable's type.
        """
        call_com(lambda: self._com.setType(type_._com))

    def setTypeDeclaration(self, new_val: str) -> None:
        """Specifies an on-the-fly type declaration, reusing a matching existing type if found.

        Args:
            new_val: The on-the-fly type declaration.
        """
        call_com(lambda: self._com.setTypeDeclaration(new_val))


class RPAttribute(RPVariable):
    """Wraps ``IRPAttribute``."""

    def getMultiplicity(self) -> str:
        """Gets the multiplicity specified for the attribute.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).
        """
        return call_com(lambda: str(self._com.getMultiplicity()))

    def setMultiplicity(self, multiplicity: str) -> None:
        """Specifies the multiplicity for the attribute.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).
        """
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def getIsStatic(self) -> bool:
        """Checks whether the attribute was defined as static.

        Returns:
            ``True`` if the attribute is static, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsStatic()))

    def setIsStatic(self, is_static: bool) -> None:
        """Specifies whether an attribute should be defined as static.

        Args:
            is_static: ``True`` to mark the attribute static, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsStatic(1 if is_static else 0))

    def getVisibility(self) -> str:
        """Gets the visibility specified for the attribute.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).
        """
        return call_com(lambda: str(self._com.getVisibility()))

    def setVisibility(self, visibility: str) -> None:
        """Specifies the visibility of the attribute.

        Args:
            visibility: The visibility string to set (e.g. ``"public"``, ``"private"``).
        """
        call_com(lambda: self._com.setVisibility(visibility))


register_wrapper("Attribute", RPAttribute)
```

- [ ] **Step 4: Remove the now-inherited `getDefaultValue`/`setDefaultValue` tests from `test_attribute.py`**

In `tests/models/elements/test_attribute.py`, delete these two test functions (their behavior is now covered by `test_variable.py`):

```python
def test_attribute_get_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute", getDefaultValue="0")
    attribute = RPAttribute(fake)

    assert attribute.getDefaultValue() == "0"


def test_attribute_set_default_value_delegates_to_com() -> None:
    fake = make_fake_element("Attribute")
    attribute = RPAttribute(fake)

    attribute.setDefaultValue("42")

    fake.setDefaultValue.assert_called_once_with("42")
```

Also update the import line and the base-class assertion test to reflect the new hierarchy. Replace:

```python
from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.variables import RPAttribute
```

with:

```python
from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.variables import RPAttribute, RPVariable
```

and replace:

```python
def test_attribute_is_a_unit() -> None:
    fake = make_fake_element("Attribute", getName="count")
    attribute = RPAttribute(fake)

    assert isinstance(attribute, RPUnit)
    assert attribute.getName() == "count"
```

with:

```python
def test_attribute_is_a_variable() -> None:
    fake = make_fake_element("Attribute", getName="count")
    attribute = RPAttribute(fake)

    assert isinstance(attribute, RPVariable)
    assert attribute.getName() == "count"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_variable.py tests/models/elements/test_attribute.py -v`
Expected: PASS

- [ ] **Step 6: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: add RPVariable, re-parent RPAttribute to extend it"
```

---

### Task 3: Add `RPInterfaceItem`, re-parent `RPOperation`

`IRPOperation extends IRPInterfaceItem extends IRPClassifier`. `RPInterfaceItem` goes in `classifiers.py` alongside the rest of the classifier family.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/classifiers.py`
- Create: `tests/models/elements/test_interface_item.py`
- Modify: `tests/models/elements/test_operation.py`

- [ ] **Step 1: Write failing tests for `RPInterfaceItem` in `tests/models/elements/test_interface_item.py`**

```python
"""Tests for rhapsody_cli.models.elements.classifiers.RPInterfaceItem."""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection
from rhapsody_cli.models.elements.classifiers import RPClassifier, RPInterfaceItem
from tests.models.fakes import make_fake_collection, make_fake_element


def test_interface_item_is_a_classifier() -> None:
    fake = make_fake_element("InterfaceItem", getName="doIt")
    item = RPInterfaceItem(fake)

    assert isinstance(item, RPClassifier)
    assert item.getName() == "doIt"


def test_interface_item_add_argument_wraps_result() -> None:
    fake = make_fake_element("InterfaceItem")
    argument = make_fake_element("Argument", getName="x")
    fake.addArgument.return_value = argument
    item = RPInterfaceItem(fake)

    result = item.addArgument("x")

    fake.addArgument.assert_called_once_with("x")
    assert result.getName() == "x"


def test_interface_item_add_argument_before_position_wraps_result() -> None:
    fake = make_fake_element("InterfaceItem")
    argument = make_fake_element("Argument", getName="y")
    fake.addArgumentBeforePosition.return_value = argument
    item = RPInterfaceItem(fake)

    result = item.addArgumentBeforePosition("y", 1)

    fake.addArgumentBeforePosition.assert_called_once_with("y", 1)
    assert result.getName() == "y"


def test_interface_item_get_arguments_returns_collection() -> None:
    inner = make_fake_element("Argument", getName="x")
    fake = make_fake_element("InterfaceItem")
    fake.getArguments.return_value = make_fake_collection([inner])
    item = RPInterfaceItem(fake)

    result = item.getArguments()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_interface_item_get_signature_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignature="void doIt(int x)")
    item = RPInterfaceItem(fake)

    assert item.getSignature() == "void doIt(int x)"


def test_interface_item_get_signature_no_arg_names_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignatureNoArgNames="void doIt(int)")
    item = RPInterfaceItem(fake)

    assert item.getSignatureNoArgNames() == "void doIt(int)"


def test_interface_item_get_signature_no_arg_types_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", getSignatureNoArgTypes="void doIt(x)")
    item = RPInterfaceItem(fake)

    assert item.getSignatureNoArgTypes() == "void doIt(x)"


def test_interface_item_match_on_signature_delegates_to_com() -> None:
    fake = make_fake_element("InterfaceItem", matchOnSignature=1)
    other = make_fake_element("InterfaceItem")
    item = RPInterfaceItem(fake)

    result = item.matchOnSignature(RPInterfaceItem(other))

    fake.matchOnSignature.assert_called_once_with(other)
    assert result is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/elements/test_interface_item.py -v`
Expected: FAIL with `ImportError: cannot import name 'RPInterfaceItem'`.

- [ ] **Step 3: Add `RPInterfaceItem` to `classifiers.py` and re-parent `RPOperation`**

In `src/rhapsody_cli/models/elements/classifiers.py`, insert the new class directly after `RPUseCase` and before `RPOperation`:

```python
class RPInterfaceItem(RPClassifier):
    """Wraps ``IRPInterfaceItem``: the base interface for operation-like
    elements that carry an argument list and signature (e.g. operations,
    triggers).
    """

    def addArgument(self, new_val: str) -> Any:
        """Adds a new argument to the end of the argument list.

        Args:
            new_val: The name (or name/type expression) of the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.
        """
        return wrap(call_com(lambda: self._com.addArgument(new_val)))

    def addArgumentBeforePosition(self, new_val: str, pos: int) -> Any:
        """Adds a new argument at the specified position in the argument list.

        Args:
            new_val: The name (or name/type expression) of the new argument.
            pos: The 1-based position at which to insert the new argument.

        Returns:
            The wrapped ``IRPArgument`` created.
        """
        return wrap(call_com(lambda: self._com.addArgumentBeforePosition(new_val, pos)))

    def getArguments(self) -> RPCollection:
        """Returns all the arguments for the operation.

        Returns:
            An ``RPCollection`` of ``IRPArgument`` objects.
        """
        return RPCollection(call_com(lambda: self._com.getArguments()))

    def getSignature(self) -> str:
        """Returns the signature of the operation.

        Returns:
            The full signature string, including argument names and types.
        """
        return call_com(lambda: str(self._com.getSignature()))

    def getSignatureNoArgNames(self) -> str:
        """Returns the signature of the operation without the argument names.

        Returns:
            The signature string with argument types but no argument names.
        """
        return call_com(lambda: str(self._com.getSignatureNoArgNames()))

    def getSignatureNoArgTypes(self) -> str:
        """Returns the signature of the operation without the argument types.

        Returns:
            The signature string with argument names but no argument types.
        """
        return call_com(lambda: str(self._com.getSignatureNoArgTypes()))

    def matchOnSignature(self, item: "RPInterfaceItem") -> bool:
        """Compares the signature of this operation with another operation's signature.

        Args:
            item: The other interface item to compare signatures with.

        Returns:
            ``True`` if the signatures match, ``False`` otherwise.
        """
        return bool(call_com(lambda: self._com.matchOnSignature(item._com)))
```

Then change `RPOperation`'s base class from `RPUnit` to `RPInterfaceItem`:

```python
class RPOperation(RPInterfaceItem):
    """Wraps ``IRPOperation``."""
```

(the rest of `RPOperation`'s body is unchanged)

Finally, add `register_wrapper` isn't needed for `RPInterfaceItem` itself (it's an intermediate type, like `RPClassifier`), but double check `register_wrapper("Operation", RPOperation)` at the bottom of the file is untouched.

- [ ] **Step 4: Update `test_operation.py`'s base-class assertion**

In `tests/models/elements/test_operation.py`, replace:

```python
from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.classifiers import RPOperation
```

with:

```python
from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.classifiers import RPInterfaceItem, RPOperation
```

and replace:

```python
def test_operation_is_a_unit() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPUnit)
    assert operation.getName() == "doIt"
```

with:

```python
def test_operation_is_an_interface_item() -> None:
    fake = make_fake_element("Operation", getName="doIt")
    operation = RPOperation(fake)

    assert isinstance(operation, RPInterfaceItem)
    assert operation.getName() == "doIt"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_interface_item.py tests/models/elements/test_operation.py -v`
Expected: PASS

- [ ] **Step 6: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: add RPInterfaceItem, re-parent RPOperation to extend it"
```

---

### Task 4: Add `RPAnnotation`, re-parent `RPRequirement`

`IRPRequirement extends IRPAnnotation extends IRPUnit`.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/requirements.py`
- Create: `tests/models/elements/test_annotation.py`
- Modify: `tests/models/elements/test_requirement.py`

- [ ] **Step 1: Write failing tests for `RPAnnotation` in `tests/models/elements/test_annotation.py`**

```python
"""Tests for rhapsody_cli.models.elements.requirements.RPAnnotation."""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, RPModelElement, RPUnit, wrap
from rhapsody_cli.models.elements.requirements import RPAnnotation
from tests.models.fakes import make_fake_collection, make_fake_element


def test_annotation_is_a_unit() -> None:
    fake = make_fake_element("Annotation", getName="Note1")
    annotation = RPAnnotation(fake)

    assert isinstance(annotation, RPUnit)
    assert annotation.getName() == "Note1"


def test_annotation_add_anchor_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    target = make_fake_element("Class", getName="Widget")
    annotation = RPAnnotation(fake)

    annotation.addAnchor(wrap(target))

    fake.addAnchor.assert_called_once_with(target)


def test_annotation_get_anchored_by_me_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Widget")
    fake = make_fake_element("Annotation")
    fake.getAnchoredByMe.return_value = make_fake_collection([inner])
    annotation = RPAnnotation(fake)

    result = annotation.getAnchoredByMe()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_annotation_get_body_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getBody="Some note text")
    annotation = RPAnnotation(fake)

    assert annotation.getBody() == "Some note text"


def test_annotation_get_specification_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getSpecification="Some spec text")
    annotation = RPAnnotation(fake)

    assert annotation.getSpecification() == "Some spec text"


def test_annotation_get_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", getSpecificationRTF="{\\rtf1}")
    annotation = RPAnnotation(fake)

    assert annotation.getSpecificationRTF() == "{\\rtf1}"


def test_annotation_is_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation", isSpecificationRTF=1)
    annotation = RPAnnotation(fake)

    assert annotation.isSpecificationRTF() is True


def test_annotation_remove_anchor_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    target = make_fake_element("Class", getName="Widget")
    annotation = RPAnnotation(fake)

    annotation.removeAnchor(wrap(target))

    fake.removeAnchor.assert_called_once_with(target)


def test_annotation_set_body_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setBody("New note text")

    fake.setBody.assert_called_once_with("New note text")


def test_annotation_set_specification_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setSpecification("New spec text")

    fake.setSpecification.assert_called_once_with("New spec text")


def test_annotation_set_specification_rtf_delegates_to_com() -> None:
    fake = make_fake_element("Annotation")
    annotation = RPAnnotation(fake)

    annotation.setSpecificationRTF("{\\rtf1 new}")

    fake.setSpecificationRTF.assert_called_once_with("{\\rtf1 new}")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/elements/test_annotation.py -v`
Expected: FAIL with `ImportError: cannot import name 'RPAnnotation'`.

- [ ] **Step 3: Implement `RPAnnotation` in `requirements.py` and re-parent `RPRequirement`**

Replace the full contents of `src/rhapsody_cli/models/elements/requirements.py` with:

```python
"""Requirement-family wrappers: mirrors IRPAnnotation and IRPRequirement
from com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, RPModelElement, RPUnit, call_com, register_wrapper


class RPAnnotation(RPUnit):
    """Wraps ``IRPAnnotation``: the base interface for free-text annotation
    elements (such as requirements and notes) that can be anchored to other
    model elements.
    """

    def addAnchor(self, target: RPModelElement) -> None:
        """Adds an anchor from the annotation to the specified model element.

        Args:
            target: The model element to anchor this annotation to.
        """
        call_com(lambda: self._com.addAnchor(target._com))

    def getAnchoredByMe(self) -> RPCollection:
        """Gets the list of model elements that are anchored to the annotation.

        Returns:
            An ``RPCollection`` of the anchored model elements.
        """
        return RPCollection(call_com(lambda: self._com.getAnchoredByMe()))

    def getBody(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's body text.
        """
        return call_com(lambda: str(self._com.getBody()))

    def getSpecification(self) -> str:
        """Gets the text of the specification for the annotation.

        Returns:
            The annotation's specification text.
        """
        return call_com(lambda: str(self._com.getSpecification()))

    def getSpecificationRTF(self) -> str:
        """Returns the specification of the annotation in RTF format.

        Returns:
            The RTF-formatted specification string.
        """
        return call_com(lambda: str(self._com.getSpecificationRTF()))

    def isSpecificationRTF(self) -> bool:
        """Checks whether the specification is in RTF format.

        Returns:
            ``True`` if the specification is RTF-formatted, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.isSpecificationRTF()))

    def removeAnchor(self, target: RPModelElement) -> None:
        """Removes the anchor to the specified model element.

        Args:
            target: The model element to remove the anchor from.
        """
        call_com(lambda: self._com.removeAnchor(target._com))

    def setBody(self, body: str) -> None:
        """Adds a specification to the annotation.

        Args:
            body: The body text to set for the annotation.
        """
        call_com(lambda: self._com.setBody(body))

    def setSpecification(self, specification: str) -> None:
        """Adds a specification to the annotation.

        Args:
            specification: The specification text to set for the annotation.
        """
        call_com(lambda: self._com.setSpecification(specification))

    def setSpecificationRTF(self, specification_rtf: str) -> None:
        """Specifies the RTF string to use for the annotation's specification.

        Args:
            specification_rtf: The RTF-formatted specification string.
        """
        call_com(lambda: self._com.setSpecificationRTF(specification_rtf))


class RPRequirement(RPAnnotation):
    """Wraps ``IRPRequirement``."""

    def getRequirementID(self) -> str:
        return call_com(lambda: str(self._com.getRequirementID()))

    def setRequirementID(self, requirement_id: str) -> None:
        call_com(lambda: self._com.setRequirementID(requirement_id))


register_wrapper("Requirement", RPRequirement)
```

- [ ] **Step 4: Update `test_requirement.py`'s base-class assertion**

In `tests/models/elements/test_requirement.py`, replace:

```python
from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.requirements import RPRequirement
```

with:

```python
from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.requirements import RPAnnotation, RPRequirement
```

and replace:

```python
def test_requirement_is_a_unit() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")
    requirement = RPRequirement(fake)

    assert isinstance(requirement, RPUnit)
    assert requirement.getName() == "REQ-1"
```

with:

```python
def test_requirement_is_an_annotation() -> None:
    fake = make_fake_element("Requirement", getName="REQ-1")
    requirement = RPRequirement(fake)

    assert isinstance(requirement, RPAnnotation)
    assert requirement.getName() == "REQ-1"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_annotation.py tests/models/elements/test_requirement.py -v`
Expected: PASS

- [ ] **Step 6: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: add RPAnnotation, re-parent RPRequirement to extend it"
```

---

### Task 5: Add `RPRelation`, re-parent `RPInstance`

`IRPInstance extends IRPRelation extends IRPUnit`. `RPRelation` has 31 declared methods; several return currently-unmapped types (`IRPAssociationClass`, `IRPClass`) which will simply be wrapped as generic `RPModelElement` by `wrap()` until later sub-projects add dedicated wrappers — this is expected and matches the existing fallback design.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/relations.py`
- Create: `tests/models/elements/test_relation.py`
- Modify: `tests/models/elements/test_instance.py`

- [ ] **Step 1: Write failing tests for `RPRelation` in `tests/models/elements/test_relation.py`**

```python
"""Tests for rhapsody_cli.models.elements.relations.RPRelation."""

from __future__ import annotations

from rhapsody_cli.models._core import RPCollection, RPModelElement, RPUnit, wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier
from rhapsody_cli.models.elements.relations import RPRelation
from tests.models.fakes import make_fake_collection, make_fake_element


def test_relation_is_a_unit() -> None:
    fake = make_fake_element("Relation", getName="assoc1")
    relation = RPRelation(fake)

    assert isinstance(relation, RPUnit)
    assert relation.getName() == "assoc1"


def test_relation_add_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    qualifier = make_fake_element("Class", getName="Key")
    relation = RPRelation(fake)

    relation.addQualifier(wrap(qualifier))

    fake.addQualifier.assert_called_once_with(qualifier)


def test_relation_get_association_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    assoc_class = make_fake_element("AssociationClass", getName="LinkClass")
    fake.getAssociationClass.return_value = assoc_class
    relation = RPRelation(fake)

    result = relation.getAssociationClass()

    fake.getAssociationClass.assert_called_once_with()
    assert result.getName() == "LinkClass"


def test_relation_get_inverse_wraps_result() -> None:
    fake = make_fake_element("Relation")
    inverse = make_fake_element("Relation", getName="inverseAssoc")
    fake.getInverse.return_value = inverse
    relation = RPRelation(fake)

    result = relation.getInverse()

    fake.getInverse.assert_called_once_with()
    assert result.getName() == "inverseAssoc"


def test_relation_get_is_navigable_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getIsNavigable=1)
    relation = RPRelation(fake)

    assert relation.getIsNavigable() is True


def test_relation_get_is_symmetric_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getIsSymmetric=0)
    relation = RPRelation(fake)

    assert relation.getIsSymmetric() is False


def test_relation_get_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getMultiplicity="0..*")
    relation = RPRelation(fake)

    assert relation.getMultiplicity() == "0..*"


def test_relation_get_object_as_object_type_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Widget")
    fake.getObjectAsObjectType.return_value = klass
    relation = RPRelation(fake)

    result = relation.getObjectAsObjectType()

    fake.getObjectAsObjectType.assert_called_once_with()
    assert result.getName() == "Widget"


def test_relation_get_of_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Widget")
    fake.getOfClass.return_value = klass
    relation = RPRelation(fake)

    result = relation.getOfClass()

    fake.getOfClass.assert_called_once_with()
    assert result.getName() == "Widget"


def test_relation_get_other_class_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="Other")
    fake.getOtherClass.return_value = klass
    relation = RPRelation(fake)

    result = relation.getOtherClass()

    fake.getOtherClass.assert_called_once_with()
    assert result.getName() == "Other"


def test_relation_get_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getQualifier="key")
    relation = RPRelation(fake)

    assert relation.getQualifier() == "key"


def test_relation_get_qualifiers_returns_collection() -> None:
    inner = make_fake_element("Class", getName="Key")
    fake = make_fake_element("Relation")
    fake.getQualifiers.return_value = make_fake_collection([inner])
    relation = RPRelation(fake)

    result = relation.getQualifiers()

    assert isinstance(result, RPCollection)
    assert len(result) == 1


def test_relation_get_qualifier_type_wraps_result() -> None:
    fake = make_fake_element("Relation")
    klass = make_fake_element("Class", getName="KeyType")
    fake.getQualifierType.return_value = klass
    relation = RPRelation(fake)

    result = relation.getQualifierType()

    fake.getQualifierType.assert_called_once_with()
    assert result.getName() == "KeyType"


def test_relation_get_relation_label_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationLabel="owns")
    relation = RPRelation(fake)

    assert relation.getRelationLabel() == "owns"


def test_relation_get_relation_link_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationLinkName="Ownership")
    relation = RPRelation(fake)

    assert relation.getRelationLinkName() == "Ownership"


def test_relation_get_relation_role_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationRoleName="owner")
    relation = RPRelation(fake)

    assert relation.getRelationRoleName() == "owner"


def test_relation_get_relation_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getRelationType="Association")
    relation = RPRelation(fake)

    assert relation.getRelationType() == "Association"


def test_relation_get_visibility_delegates_to_com() -> None:
    fake = make_fake_element("Relation", getVisibility="public")
    relation = RPRelation(fake)

    assert relation.getVisibility() == "public"


def test_relation_is_typeless_object_delegates_to_com() -> None:
    fake = make_fake_element("Relation", isTypelessObject=1)
    relation = RPRelation(fake)

    assert relation.isTypelessObject() is True


def test_relation_make_unidirect_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.makeUnidirect()

    fake.makeUnidirect.assert_called_once_with()


def test_relation_remove_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    qualifier = make_fake_element("Class", getName="Key")
    relation = RPRelation(fake)

    relation.removeQualifier(wrap(qualifier))

    fake.removeQualifier.assert_called_once_with(qualifier)


def test_relation_set_inverse_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setInverse("owner", "Association")

    fake.setInverse.assert_called_once_with("owner", "Association")


def test_relation_set_is_navigable_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setIsNavigable(True)

    fake.setIsNavigable.assert_called_once_with(1)


def test_relation_set_multiplicity_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setMultiplicity("0..*")

    fake.setMultiplicity.assert_called_once_with("0..*")


def test_relation_set_of_class_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="Widget")
    relation = RPRelation(fake)

    relation.setOfClass(RPClassifier(klass_fake))

    fake.setOfClass.assert_called_once_with(klass_fake)


def test_relation_set_other_class_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="Other")
    relation = RPRelation(fake)

    relation.setOtherClass(RPClassifier(klass_fake))

    fake.setOtherClass.assert_called_once_with(klass_fake)


def test_relation_set_qualifier_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setQualifier("key")

    fake.setQualifier.assert_called_once_with("key")


def test_relation_set_qualifier_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    klass_fake = make_fake_element("Class", getName="KeyType")
    relation = RPRelation(fake)

    relation.setQualifierType(wrap(klass_fake))

    fake.setQualifierType.assert_called_once_with(klass_fake)


def test_relation_set_relation_label_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setRelationLabel("owns")

    fake.setRelationLabel.assert_called_once_with("owns")


def test_relation_set_relation_link_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setRelationLinkName("Ownership")

    fake.setRelationLinkName.assert_called_once_with("Ownership")


def test_relation_set_relation_role_name_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setRelationRoleName("owner")

    fake.setRelationRoleName.assert_called_once_with("owner")


def test_relation_set_relation_type_delegates_to_com() -> None:
    fake = make_fake_element("Relation")
    relation = RPRelation(fake)

    relation.setRelationType("Association")

    fake.setRelationType.assert_called_once_with("Association")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/elements/test_relation.py -v`
Expected: FAIL with `ImportError: cannot import name 'RPRelation'`.

- [ ] **Step 3: Implement `RPRelation` in `relations.py` and re-parent `RPInstance`**

Replace the full contents of `src/rhapsody_cli/models/elements/relations.py` with:

```python
"""Relation-family wrappers: mirrors IRPRelation and IRPInstance from
com.telelogic.rhapsody.core.
"""

from __future__ import annotations

from typing import Any

from rhapsody_cli.models._core import RPCollection, RPModelElement, RPUnit, call_com, register_wrapper, wrap
from rhapsody_cli.models.elements.classifiers import RPClassifier


class RPRelation(RPUnit):
    """Wraps ``IRPRelation``: the base interface for relationships between
    classifiers (such as associations, and the instance links derived from
    them).
    """

    def addQualifier(self, p_val: RPModelElement) -> None:
        """Adds a qualifier to the association.

        Args:
            p_val: The model element to add as a qualifier.
        """
        call_com(lambda: self._com.addQualifier(p_val._com))

    def getAssociationClass(self) -> Any:
        """Returns the association class linked to this relation, if any.

        Returns:
            The wrapped ``IRPAssociationClass``, or an empty wrapper if none exists.
        """
        return wrap(call_com(lambda: self._com.getAssociationClass()))

    def getInverse(self) -> "RPRelation":
        """Gets the inverse relation for this (bidirectional) relation.

        Returns:
            The wrapped ``IRPRelation`` representing the inverse direction.
        """
        return wrap(call_com(lambda: self._com.getInverse()))

    def getIsNavigable(self) -> bool:
        """Checks whether the relation is navigable.

        Returns:
            ``True`` if the relation is navigable, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsNavigable()))

    def getIsSymmetric(self) -> bool:
        """Checks whether the relation is symmetric.

        Returns:
            ``True`` if the relation is symmetric, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.getIsSymmetric()))

    def getMultiplicity(self) -> str:
        """Gets the multiplicity of the relation.

        Returns:
            The multiplicity string (e.g. ``"1"``, ``"0..*"``).
        """
        return call_com(lambda: str(self._com.getMultiplicity()))

    def getObjectAsObjectType(self) -> Any:
        """Gets the object's class, treated as the object's type.

        Returns:
            The wrapped ``IRPClass``.
        """
        return wrap(call_com(lambda: self._com.getObjectAsObjectType()))

    def getOfClass(self) -> Any:
        """Gets the classifier that owns this relation.

        Returns:
            The wrapped ``IRPClassifier``.
        """
        return wrap(call_com(lambda: self._com.getOfClass()))

    def getOtherClass(self) -> Any:
        """Gets the class that this class is related to via this relation.

        Returns:
            The wrapped ``IRPClassifier`` on the other end of the relation.
        """
        return wrap(call_com(lambda: self._com.getOtherClass()))

    def getQualifier(self) -> str:
        """Gets the qualifier text for the association.

        Returns:
            The qualifier string.
        """
        return call_com(lambda: str(self._com.getQualifier()))

    def getQualifiers(self) -> RPCollection:
        """Gets the collection of qualifier model elements for the association.

        Returns:
            An ``RPCollection`` of qualifier model elements.
        """
        return RPCollection(call_com(lambda: self._com.getQualifiers()))

    def getQualifierType(self) -> Any:
        """For associations that use qualifiers, returns the type of the qualifier.

        Returns:
            The wrapped ``IRPClassifier`` used as the qualifier's type.
        """
        return wrap(call_com(lambda: self._com.getQualifierType()))

    def getRelationLabel(self) -> str:
        """Gets the label of the relation.

        Returns:
            The relation label string.
        """
        return call_com(lambda: str(self._com.getRelationLabel()))

    def getRelationLinkName(self) -> str:
        """Gets the link name of the relation.

        Returns:
            The relation link name string.
        """
        return call_com(lambda: str(self._com.getRelationLinkName()))

    def getRelationRoleName(self) -> str:
        """Gets the role name of the relation.

        Returns:
            The relation role name string.
        """
        return call_com(lambda: str(self._com.getRelationRoleName()))

    def getRelationType(self) -> str:
        """Gets the type of the relation.

        Returns:
            The relation type string (e.g. ``"Association"``).
        """
        return call_com(lambda: str(self._com.getRelationType()))

    def getVisibility(self) -> str:
        """Gets the visibility of the relation.

        Returns:
            The visibility string (e.g. ``"public"``, ``"private"``).
        """
        return call_com(lambda: str(self._com.getVisibility()))

    def isTypelessObject(self) -> bool:
        """Checks whether the object at the other end of the relation has no type.

        Returns:
            ``True`` if the related object is typeless, ``False`` otherwise.
        """
        return call_com(lambda: bool(self._com.isTypelessObject()))

    def makeUnidirect(self) -> None:
        """Makes the relation unidirectional."""
        call_com(lambda: self._com.makeUnidirect())

    def removeQualifier(self, p_val: RPModelElement) -> None:
        """Removes a qualifier from the association.

        Args:
            p_val: The model element to remove from the qualifiers.
        """
        call_com(lambda: self._com.removeQualifier(p_val._com))

    def setInverse(self, role_name: str, link_type: str) -> None:
        """Sets the inverse role name and link type for the relation.

        Args:
            role_name: The role name to use for the inverse relation.
            link_type: The link type to use for the inverse relation.
        """
        call_com(lambda: self._com.setInverse(role_name, link_type))

    def setIsNavigable(self, is_navigable: bool) -> None:
        """Sets whether the relation is navigable.

        Args:
            is_navigable: ``True`` to make the relation navigable, ``False`` otherwise.
        """
        call_com(lambda: self._com.setIsNavigable(1 if is_navigable else 0))

    def setMultiplicity(self, multiplicity: str) -> None:
        """Sets the multiplicity of the relation.

        Args:
            multiplicity: The multiplicity string to set (e.g. ``"1"``, ``"0..*"``).
        """
        call_com(lambda: self._com.setMultiplicity(multiplicity))

    def setOfClass(self, of_class: RPClassifier) -> None:
        """Sets the classifier that owns this relation.

        Args:
            of_class: The classifier to set as the owner of this relation.
        """
        call_com(lambda: self._com.setOfClass(of_class._com))

    def setOtherClass(self, other_class: RPClassifier) -> None:
        """Sets the class that this class is related to via this relation.

        Args:
            other_class: The classifier to set on the other end of the relation.
        """
        call_com(lambda: self._com.setOtherClass(other_class._com))

    def setQualifier(self, qualifier: str) -> None:
        """Sets the qualifier text for the association.

        Args:
            qualifier: The qualifier string to set.
        """
        call_com(lambda: self._com.setQualifier(qualifier))

    def setQualifierType(self, p_val: RPModelElement) -> None:
        """Sets the type to use for the qualifier for the association.

        Args:
            p_val: The classifier to use as the qualifier's type.
        """
        call_com(lambda: self._com.setQualifierType(p_val._com))

    def setRelationLabel(self, relation_label: str) -> None:
        """Sets the label of the relation.

        Args:
            relation_label: The label string to set.
        """
        call_com(lambda: self._com.setRelationLabel(relation_label))

    def setRelationLinkName(self, relation_link_name: str) -> None:
        """Sets the link name of the relation.

        Args:
            relation_link_name: The link name string to set.
        """
        call_com(lambda: self._com.setRelationLinkName(relation_link_name))

    def setRelationRoleName(self, relation_role_name: str) -> None:
        """Sets the role name of the relation.

        Args:
            relation_role_name: The role name string to set.
        """
        call_com(lambda: self._com.setRelationRoleName(relation_role_name))

    def setRelationType(self, relation_type: str) -> None:
        """Sets the type of the relation.

        Args:
            relation_type: The relation type string to set (e.g. ``"Association"``).
        """
        call_com(lambda: self._com.setRelationType(relation_type))


class RPInstance(RPRelation):
    """Wraps ``IRPInstance``."""

    def getAllNestedElements(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getAllNestedElements()))

    def getAttributeValue(self, attribute_name: str) -> str:
        return call_com(lambda: str(self._com.getAttributeValue(attribute_name)))

    def setAttributeValue(self, attribute_name: str, attribute_value: str) -> None:
        call_com(lambda: self._com.setAttributeValue(attribute_name, attribute_value))

    def getInLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getInLinks()))

    def getOutLinks(self) -> RPCollection:
        return RPCollection(call_com(lambda: self._com.getOutLinks()))


register_wrapper("Instance", RPInstance)
```

- [ ] **Step 4: Update `test_instance.py`'s base-class assertion**

In `tests/models/elements/test_instance.py`, replace:

```python
from rhapsody_cli.models._core import RPUnit, wrap
from rhapsody_cli.models.elements.relations import RPInstance
```

with:

```python
from rhapsody_cli.models._core import wrap
from rhapsody_cli.models.elements.relations import RPInstance, RPRelation
```

and replace:

```python
def test_instance_is_a_unit() -> None:
    fake = make_fake_element("Instance", getName="driver1")
    instance = RPInstance(fake)

    assert isinstance(instance, RPUnit)
    assert instance.getName() == "driver1"
```

with:

```python
def test_instance_is_a_relation() -> None:
    fake = make_fake_element("Instance", getName="driver1")
    instance = RPInstance(fake)

    assert isinstance(instance, RPRelation)
    assert instance.getName() == "driver1"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_relation.py tests/models/elements/test_instance.py -v`
Expected: PASS

- [ ] **Step 6: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: add RPRelation, re-parent RPInstance to extend it"
```

---

### Task 6: Re-parent `RPProject` to extend `RPPackage`

`IRPProject extends IRPPackage` directly (no new intermediate class needed — `RPPackage` already exists). No method-name conflicts exist between `RPProject`'s and `RPPackage`'s current methods.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/containment.py`
- Modify: `tests/models/elements/test_project.py`

- [ ] **Step 1: Update the failing assertion in `test_project.py` first (TDD: adjust the test to express the corrected hierarchy before changing the implementation)**

In `tests/models/elements/test_project.py`, replace:

```python
from rhapsody_cli.models._core import RPUnit
from rhapsody_cli.models.elements.containment import RPProject
```

with:

```python
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
```

and replace:

```python
def test_project_is_a_unit() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPUnit)
    assert project.getName() == "MyProject"
```

with:

```python
def test_project_is_a_package() -> None:
    fake = make_fake_element("Project", getName="MyProject")
    project = RPProject(fake)

    assert isinstance(project, RPPackage)
    assert project.getName() == "MyProject"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/models/elements/test_project.py::test_project_is_a_package -v`
Expected: FAIL with `AssertionError` (since `RPProject` still extends `RPUnit`, not `RPPackage`).

- [ ] **Step 3: Change `RPProject`'s base class in `containment.py`**

In `src/rhapsody_cli/models/elements/containment.py`, change:

```python
class RPProject(RPUnit):
    """Wraps ``IRPProject``."""
```

to:

```python
class RPProject(RPPackage):
    """Wraps ``IRPProject``."""
```

(the rest of `RPProject`'s body is unchanged; `RPUnit` import in this file remains needed for `RPPackage`'s own base class)

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_project.py -v`
Expected: PASS

- [ ] **Step 5: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "fix: re-parent RPProject to extend RPPackage per IRPProject hierarchy"
```

---

### Task 7: Re-parent `RPStatechart` to extend `RPClass`

`IRPStatechart extends IRPClass` directly (no new intermediate class needed). No method-name conflicts exist between `RPStatechart`'s and `RPClass`'s/`RPClassifier`'s current methods.

**Files:**
- Modify: `src/rhapsody_cli/models/elements/classifiers.py`
- Modify: `tests/models/elements/test_statechart.py`

- [ ] **Step 1: Update the failing assertion in `test_statechart.py` first**

In `tests/models/elements/test_statechart.py`, replace:

```python
from rhapsody_cli.models._core import RPModelElement, RPUnit, wrap
from rhapsody_cli.models.elements.classifiers import RPStatechart
```

with:

```python
from rhapsody_cli.models._core import RPModelElement, wrap
from rhapsody_cli.models.elements.classifiers import RPClass, RPStatechart
```

and replace:

```python
def test_statechart_is_a_unit() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")
    statechart = RPStatechart(fake)

    assert isinstance(statechart, RPUnit)
    assert statechart.getName() == "Behavior"
```

with:

```python
def test_statechart_is_a_class() -> None:
    fake = make_fake_element("Statechart", getName="Behavior")
    statechart = RPStatechart(fake)

    assert isinstance(statechart, RPClass)
    assert statechart.getName() == "Behavior"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/models/elements/test_statechart.py::test_statechart_is_a_class -v`
Expected: FAIL with `AssertionError` (since `RPStatechart` still extends `RPUnit`, not `RPClass`).

- [ ] **Step 3: Change `RPStatechart`'s base class in `classifiers.py`**

In `src/rhapsody_cli/models/elements/classifiers.py`, change:

```python
class RPStatechart(RPUnit):
    """Wraps ``IRPStatechart``."""
```

to:

```python
class RPStatechart(RPClass):
    """Wraps ``IRPStatechart``."""
```

(the rest of `RPStatechart`'s body is unchanged)

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/models/elements/test_statechart.py -v`
Expected: PASS

- [ ] **Step 5: Run lint/format/type checks**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/`
Expected: All clean.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "fix: re-parent RPStatechart to extend RPClass per IRPStatechart hierarchy"
```

---

### Task 8: Final full-suite verification

**Files:** none (verification only)

- [ ] **Step 1: Run the entire test suite**

Run: `pytest -v`
Expected: All tests pass, including `tests/models/test_core.py`, all of `tests/models/elements/`, `tests/test_application.py`, `tests/test_public_api.py`, and the `tests/cli/` suite.

- [ ] **Step 2: Run the full quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest`
Expected: All clean, all tests pass.

- [ ] **Step 3: Verify `wrap()` dispatch still works for every registered meta class**

Run:
```powershell
python -c "
from rhapsody_cli.models._core import _WRAPPER_REGISTRY
for name, cls in sorted(_WRAPPER_REGISTRY.items()):
    print(name, '->', cls.__name__)
"
```
Expected output includes exactly: `Actor -> RPActor`, `Attribute -> RPAttribute`, `Class -> RPClass`, `Instance -> RPInstance`, `Operation -> RPOperation`, `Package -> RPPackage`, `Project -> RPProject`, `Requirement -> RPRequirement`, `Statechart -> RPStatechart`, `UseCase -> RPUseCase`, `ActivityDiagram -> RPDiagram` (11 entries — unchanged from before this plan, since the 4 new intermediate classes are not directly registered).

- [ ] **Step 4: Final commit (if any cleanup was needed) and push**

```bash
git status --short
git add -A
git commit -m "chore: verify full suite green after core wrapper hierarchy audit" --allow-empty
git push -u origin docs/audit-core-wrappers-design
```

---

## Deferred to Phase 2+ (not part of this plan)

- Full method parity for `RPModelElement`/`RPUnit` (118 + 29 declared methods).
- Full method parity for `RPClassifier` (46 methods), `RPPackage` (100 methods), `RPProject` (72 methods) — largest remaining classes.
- Full method parity for `RPAttribute` (add `getIsConstant`/`getIsOrdered`/`getIsReference` + setters), `RPOperation` (32 methods), `RPRequirement` (already fully covered — only 2 methods total), `RPInstance` (13 methods — already fully covered), `RPClass` (29 methods), `RPActor` (4 methods — already fully covered), `RPUseCase` (15 methods), `RPStatechart` (32 methods), `RPDiagram` (33 methods).
- Each will be its own follow-up plan, smallest classes first, using the same TDD process and Google-style/java_api-sourced docstring convention established here.
