# Software Requirements - ELEM (Model Element Wrappers)

**Category:** ELEM
**Prefix:** SWR
**Source:** Extracted from code
**Last Validated:** 2026-07-07

---

## SWR_ELEM_00001: RPProject Wrapper

**ID:** SWR_ELEM_00001
**Title: RPProject wraps IRPProject, the top-level container for a Rhapsody model
**Status:** Implemented
**Priority:** High
**Description:**
`RPProject` shall extend `RPUnit` to wrap `IRPProject`. It shall expose Java-mirrored
methods: `addPackage(name)` (returns wrapped new package), `close()`,
`becomeActiveProject()`, `findComponent(name)` (returns wrapped component), and
`getPackages()` (returns `RPCollection`). The wrapper shall register itself for the
meta class `"Project"`.
**Implementation:** src/rhapsody_cli/models/elements/project.py:RPProject
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00002: RPPackage Wrapper

**ID:** SWR_ELEM_00002
**Title: RPPackage wraps IRPPackage, a container for classes, actors, and other elements
**Status:** Implemented
**Priority:** High
**Description:**
`RPPackage` shall extend `RPUnit` to wrap `IRPPackage`. It shall expose Java-mirrored
creation methods that return wrapped new elements: `addClass(name)`,
`addNestedPackage(name)`, `addActor(name)`, and `addGlobalFunction(name)`. The wrapper
shall register itself for the meta class `"Package"`.
**Implementation:** src/rhapsody_cli/models/elements/package.py:RPPackage
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00003: RPClassifier Shared Base

**ID:** SWR_ELEM_00003
**Title: RPClassifier wraps IRPClassifier, the shared base of Class/Actor/UseCase
**Status:** Implemented
**Priority:** High
**Description:**
`RPClassifier` shall extend `RPUnit` to wrap `IRPClassifier`. It shall expose
Java-mirrored methods: `addAttribute(name)` (returns wrapped attribute),
`addOperation(name)` (returns wrapped operation), `getAttributes()` (returns
`RPCollection`), `getOperations()` (returns `RPCollection`),
`addGeneralization(base_classifier)` (accepts an `RPClassifier` and delegates its
`_com`), and `addStatechart()` (returns wrapped statechart).
**Implementation:** src/rhapsody_cli/models/elements/classifier.py:RPClassifier
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00004: RPClass Wrapper

**ID:** SWR_ELEM_00004
**Title: RPClass wraps IRPClass, a UML/SysML class in the Rhapsody model
**Status:** Implemented
**Priority:** High
**Description:**
`RPClass` shall extend `RPClassifier` to wrap `IRPClass`. It shall expose Java-mirrored
methods: `addSuperclass(super_class)` (accepts an `RPClass`), `addConstructor(arguments_data)`
(returns wrapped constructor), `addDestructor()` (returns wrapped destructor),
`getIsAbstract()` (returns bool), and `addClass(name)` (returns wrapped nested class).
The wrapper shall register itself for the meta class `"Class"`.
**Implementation:** src/rhapsody_cli/models/elements/class_.py:RPClass
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00005: RPActor Wrapper

**ID:** SWR_ELEM_00005
**Title: RPActor wraps IRPActor, a UML actor (external role interacting with the system)
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPActor` shall extend `RPClassifier` to wrap `IRPActor`. It shall expose Java-mirrored
methods: `addEventReceptionWithEvent(name, event)` (accepts an `RPModelElement` event,
returns wrapped reception), `getIsBehaviorOverriden()` (returns bool), and
`setIsBehaviorOverriden(is_overridden)` (translates Python bool to 1/0). The wrapper
shall register itself for the meta class `"Actor"`.
**Implementation:** src/rhapsody_cli/models/elements/actor.py:RPActor
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00006: RPOperation Wrapper

**ID:** SWR_ELEM_00006
**Title: RPOperation wraps IRPOperation, a class/package-level operation or function
**Status:** Implemented
**Priority:** High
**Description:**
`RPOperation` shall extend `RPUnit` to wrap `IRPOperation`. It shall expose Java-mirrored
methods: `getBody()` (returns str), `getIsAbstract()` (returns bool), `getIsStatic()`
(returns bool), `getIsVirtual()` (returns bool), `getReturns()` (returns wrapped
element), and `createAutoFlowChart()`. The wrapper shall register itself for the meta
class `"Operation"`.
**Implementation:** src/rhapsody_cli/models/elements/operation.py:RPOperation
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00007: RPAttribute Wrapper

**ID:** SWR_ELEM_00007
**Title: RPAttribute wraps IRPAttribute, a class/package-level attribute or variable
**Status:** Implemented
**Priority:** High
**Description:**
`RPAttribute` shall extend `RPUnit` to wrap `IRPAttribute`. It shall expose Java-mirrored
methods: `getMultiplicity()` / `setMultiplicity(multiplicity)` (str), `getIsStatic()` /
`setIsStatic(is_static)` (bool, translated to 1/0), `getVisibility()` /
`setVisibility(visibility)` (str), and `getDefaultValue()` / `setDefaultValue(default_value)`
(str). The wrapper shall register itself for the meta class `"Attribute"`.
**Implementation:** src/rhapsody_cli/models/elements/attribute.py:RPAttribute
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00008: RPDiagram Wrapper

**ID:** SWR_ELEM_00008
**Title: RPDiagram wraps IRPDiagram, the base interface for all Rhapsody diagram types
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPDiagram` shall extend `RPUnit` to wrap `IRPDiagram`. It shall expose Java-mirrored
methods: `closeDiagram()`, `addTextBox(text, x_position, y_position, width, height)`
(returns wrapped text box), `getCustomViews()` (returns `RPCollection`), and
`getCorrespondingGraphicElements(model_element)` (accepts an `RPModelElement`, returns
`RPCollection`). The wrapper shall register itself for the meta class
`"ActivityDiagram"`.
**Implementation:** src/rhapsody_cli/models/elements/diagram.py:RPDiagram
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00009: RPInstance Wrapper

**ID:** SWR_ELEM_00009
**Title: RPInstance wraps IRPInstance, an instance/object in the Rhapsody model
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPInstance` shall extend `RPUnit` to wrap `IRPInstance`. It shall expose Java-mirrored
methods: `getAllNestedElements()` (returns `RPCollection`), `getAttributeValue(attribute_name)`
(returns str), `setAttributeValue(attribute_name, attribute_value)` (str args),
`getInLinks()` (returns `RPCollection`), and `getOutLinks()` (returns `RPCollection`).
The wrapper shall register itself for the meta class `"Instance"`.
**Implementation:** src/rhapsody_cli/models/elements/instance.py:RPInstance
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00010: RPRequirement Wrapper

**ID:** SWR_ELEM_00010
**Title: RPRequirement wraps IRPRequirement, a traceable requirement in the model
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPRequirement` shall extend `RPUnit` to wrap `IRPRequirement`. It shall expose
Java-mirrored methods: `getRequirementID()` (returns str) and
`setRequirementID(requirement_id)` (str). The wrapper shall register itself for the
meta class `"Requirement"`.
**Implementation:** src/rhapsody_cli/models/elements/requirement.py:RPRequirement
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00011: RPStatechart Wrapper

**ID:** SWR_ELEM_00011
**Title: RPStatechart wraps IRPStatechart, a class's behavioral state machine
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPStatechart` shall extend `RPUnit` to wrap `IRPStatechart`. It shall expose
Java-mirrored methods: `addNewNodeByType(meta_type, x_position, y_position, width, height)`
(returns wrapped node), `createGraphics()`, `closeDiagram()`, and `deleteState(state)`
(accepts an `RPModelElement`). The wrapper shall register itself for the meta class
`"Statechart"`.
**Implementation:** src/rhapsody_cli/models/elements/statechart.py:RPStatechart
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00012: RPUseCase Wrapper

**ID:** SWR_ELEM_00012
**Title: RPUseCase wraps IRPUseCase, a UML use case
**Status:** Implemented
**Priority:** Medium
**Description:**
`RPUseCase` shall extend `RPClassifier` to wrap `IRPUseCase`. It shall expose
Java-mirrored methods: `addExtensionPoint(entry_point)` (str),
`getExtensionPoints()` (returns `RPCollection`), `getEntryPoints()` (returns
`RPCollection`), and `getDescribingDiagrams()` (returns `RPCollection`). The wrapper
shall register itself for the meta class `"UseCase"`.
**Implementation:** src/rhapsody_cli/models/elements/usecase.py:RPUseCase
**Last Changed:** 2026-07-07

---

## SWR_ELEM_00013: Element Module Registration on Import

**ID:** SWR_ELEM_00013
**Title: Importing rhapsody_cli.models.elements registers all core element wrappers
**Status:** Implemented
**Priority:** High
**Description:**
The `rhapsody_cli.models.elements` package `__init__.py` shall import all concrete
element wrapper modules (actor, attribute, class_, classifier, diagram, instance,
operation, package, project, requirement, statechart, usecase). Each module shall call
`register_wrapper` at import time so that, after importing the package, the `wrap()`
factory is populated for all core element types.
**Implementation:** src/rhapsody_cli/models/elements/__init__.py
**Last Changed:** 2026-07-07
