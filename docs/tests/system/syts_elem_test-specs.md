# System Test Specifications - Model Element Wrappers

**Category:** ELEM
**Prefix:** SYTS
**Test Type:** System
**Last Validated:** 2026-07-07

---

## SYTS_ELEM_00001: End-to-End Create Package, Class, Attribute, Operation, and Save

**ID:** SYTS_ELEM_00001
**Traces-To:** SWR_ELEM_00001, SWR_ELEM_00002, SWR_ELEM_00003, SWR_ELEM_00004, SWR_ELEM_00006, SWR_ELEM_00007
**Title:** Build a model graph end-to-end and persist via save
**Type:** System
**Priority:** High
**Description:**
This test verifies the end-to-end model manipulation flow: starting from a wrapped fake
Project, add a Package, add a Class to the package, add an Attribute and an Operation to
the class, and finally call `save()` on the project. Each creation method must return the
correctly wrapped new element, and the underlying fake COM `add*` calls must be invoked
with the right arguments.
**Pre-conditions:**
- A fake `IRPProject` COM object whose `addPackage(name)` returns a fake `IRPPackage`,
  whose `getMetaClass()` returns "Project", and whose `save()` records a call.
- The fake `IRPPackage` whose `addClass(name)` returns a fake `IRPClass`
  (`getMetaClass()` == "Class").
- The fake `IRPClass` whose `addAttribute(name)` returns a fake `IRPAttribute`
  ("Attribute") and `addOperation(name)` returns a fake `IRPOperation` ("Operation").
- The `rhapsody_cli.models.elements` package imported so the wrapper registry is
  populated.
**Test Steps:**
1. Wrap the fake project COM object via `wrap()`; assert an `RPProject` is returned.
2. Call `project.addPackage("Domain")` and assert an `RPPackage` is returned whose
   `getName()` returns "Domain".
3. Call `package.addClass("Vehicle")` and assert an `RPClass` is returned.
4. Call `class_.addAttribute("speed")` and assert an `RPAttribute` is returned.
5. Call `class_.addOperation("start")` and assert an `RPOperation` is returned.
6. Call `project.save()` and assert the fake project's `save` was invoked exactly once.
7. Inspect the fake COM call recorder to confirm each `add*` received the expected name
   argument.
**Expected Result:**
- Each `add*` returns a wrapper of the correct subclass (RPPackage, RPClass, RPAttribute,
  RPOperation).
- `getName()` on each new element returns the name passed to the `add*` call.
- `project.save()` delegates to the fake COM `save` exactly once.
- The fake COM call recorder shows the correct argument strings for every creation call.
**Verification Criteria:**
- Pass if all isinstance and getName assertions hold, `save` is called once, and the call
  recorder shows the right arguments.
- Fail if any `add*` returns the wrong wrapper type, the name is lost, or `save` is not
  invoked.
**Last Changed:** 2026-07-07

---

## SYTS_ELEM_00002: Diagram Operations End-to-End

**ID:** SYTS_ELEM_00002
**Traces-To:** SWR_ELEM_00008
**Title:** RPDiagram addTextBox, closeDiagram, getCustomViews, and getCorrespondingGraphicElements
**Type:** System
**Priority:** Medium
**Description:**
This test verifies end-to-end diagram operations through the `RPDiagram` wrapper: adding a
text box with positional arguments, closing the diagram, retrieving custom views as an
`RPCollection`, and retrieving the graphic elements corresponding to a model element.
**Pre-conditions:**
- A fake `IRPDiagram` COM object (meta class "ActivityDiagram") whose `addTextBox(text,
  x, y, w, h)` returns a fake text-box element, whose `getCustomViews()` returns a fake
  `IRPCollection` of two views, and whose
  `getCorrespondingGraphicElements(modelElement)` accepts a COM object and returns a fake
  `IRPCollection`.
- The fake diagram records `closeDiagram()` calls.
- The wrapper registry populated.
**Test Steps:**
1. Wrap the fake diagram COM object and assert an `RPDiagram` is returned.
2. Call `diagram.addTextBox("Note", 10, 20, 100, 50)` and assert a wrapped element is
   returned.
3. Call `diagram.getCustomViews()` and assert an `RPCollection` of length 2 is returned.
4. Wrap a fake model element and pass it to
   `diagram.getCorrespondingGraphicElements(model_element)`; assert an `RPCollection` is
   returned.
5. Call `diagram.closeDiagram()` and assert the fake's `closeDiagram` was called once.
6. Inspect the fake call recorder to confirm `addTextBox` received the positional
   arguments in order.
**Expected Result:**
- `addTextBox` returns a wrapped element and forwards all positional arguments to the COM
  method in order.
- `getCustomViews` and `getCorrespondingGraphicElements` return `RPCollection` instances.
- `closeDiagram` delegates to the fake COM method exactly once.
**Verification Criteria:**
- Pass if all return-type assertions hold, the `addTextBox` arguments are forwarded
  correctly, and `closeDiagram` is called once.
- Fail if any method returns the wrong type, arguments are reordered, or `closeDiagram`
  is not invoked.
**Last Changed:** 2026-07-07

---

## SYTS_ELEM_00003: Statechart Operations End-to-End

**ID:** SYTS_ELEM_00003
**Traces-To:** SWR_ELEM_00003, SWR_ELEM_00011
**Title:** Add statechart to classifier, add node, create graphics, close, delete state
**Type:** System
**Priority:** Medium
**Description:**
This test verifies end-to-end statechart operations: adding a statechart to a classifier,
adding a new node by type with positional coordinates, creating graphics, closing the
diagram, and deleting a state by passing a wrapped `RPModelElement`.
**Pre-conditions:**
- A fake `IRPClassifier` ("Class") whose `addStatechart()` returns a fake `IRPStatechart`
  ("Statechart").
- The fake statechart whose `addNewNodeByType(meta_type, x, y, w, h)` returns a fake node
  element, and which records `createGraphics()`, `closeDiagram()`, and
  `deleteState(state)` calls (the last receiving a COM object).
- The wrapper registry populated.
**Test Steps:**
1. Wrap the fake classifier and call `classifier.addStatechart()`; assert an
   `RPStatechart` is returned.
2. Call `statechart.addNewNodeByType("State", 5, 10, 80, 40)` and assert a wrapped node
   is returned.
3. Call `statechart.createGraphics()` and assert the fake's `createGraphics` was called
   once.
4. Wrap a fake state element and call `statechart.deleteState(state)`; assert the fake's
   `deleteState` received the state's underlying COM object (not the wrapper).
5. Call `statechart.closeDiagram()` and assert it was called once.
**Expected Result:**
- `addStatechart` returns an `RPStatechart`.
- `addNewNodeByType` returns a wrapped node and forwards all positional arguments.
- `deleteState` delegates the wrapped element's `_com` (raw COM object) to the fake.
- `createGraphics` and `closeDiagram` each delegate exactly once.
**Verification Criteria:**
- Pass if all return types are correct, positional arguments are forwarded, and
  `deleteState` receives the raw COM object (not the wrapper).
- Fail if `deleteState` receives a wrapper instance instead of the COM object, or if any
  method fails to delegate.
**Last Changed:** 2026-07-07

---

## SYTS_ELEM_00004: Actor and UseCase Operations End-to-End

**ID:** SYTS_ELEM_00004
**Traces-To:** SWR_ELEM_00005, SWR_ELEM_00012
**Title:** RPActor event reception and bool translation; RPUseCase extension points
**Type:** System
**Priority:** Medium
**Description:**
This test verifies end-to-end operations on `RPActor` and `RPUseCase` wrappers: an actor's
`addEventReceptionWithEvent` accepting a wrapped event element, the actor's bool
getter/setter with 1/0 translation, and a use case's extension-point and collection
methods.
**Pre-conditions:**
- A fake `IRPActor` ("Actor") whose `addEventReceptionWithEvent(name, event)` returns a
  fake reception, and which records `getIsBehaviorOverriden()` and
  `setIsBehaviorOverriden(int)` calls.
- A fake `IRPUseCase` ("UseCase") whose `addExtensionPoint(ep)` records the string, and
  whose `getExtensionPoints()`, `getEntryPoints()`, and `getDescribingDiagrams()` each
  return a fake `IRPCollection`.
- The wrapper registry populated.
**Test Steps:**
1. Wrap the fake actor and call `actor.addEventReceptionWithEvent("recv", event)` where
   `event` is a wrapped `RPModelElement`; assert a wrapped reception is returned.
2. Confirm the fake's `addEventReceptionWithEvent` received the event's underlying COM
   object as the second argument.
3. Call `actor.setIsBehaviorOverriden(True)` and assert the fake received integer 1.
4. Call `actor.getIsBehaviorOverriden()` and assert it returns a bool.
5. Wrap the fake use case and call `usecase.addExtensionPoint("EP1")`; assert the fake
   received "EP1".
6. Call `getExtensionPoints()`, `getEntryPoints()`, and `getDescribingDiagrams()` and
   assert each returns an `RPCollection`.
**Expected Result:**
- `addEventReceptionWithEvent` returns a wrapped reception and forwards the event's raw
  COM object.
- `setIsBehaviorOverriden(True)` -> 1, and `getIsBehaviorOverriden()` returns a bool.
- All three use-case collection methods return `RPCollection` instances.
**Verification Criteria:**
- Pass if all return types are correct, the event COM object is forwarded (not the
  wrapper), and bool translation works.
- Fail if the wrapper is passed instead of the COM object, or if bool translation is
  missing.
**Last Changed:** 2026-07-07

---

## SYTS_ELEM_00005: Requirement and Instance Operations End-to-End

**ID:** SYTS_ELEM_00005
**Traces-To:** SWR_ELEM_00009, SWR_ELEM_00010
**Title:** RPRequirement ID get/set and RPInstance attribute and link collections
**Type:** System
**Priority:** Medium
**Description:**
This test verifies end-to-end operations on `RPRequirement` and `RPInstance` wrappers:
getting and setting the requirement ID, and on an instance retrieving nested elements,
attribute values, and in/out links as `RPCollection`s.
**Pre-conditions:**
- A fake `IRPRequirement` ("Requirement") whose `getRequirementID()` returns "REQ-001"
  and which records `setRequirementID(id)`.
- A fake `IRPInstance` ("Instance") whose `getAllNestedElements()`, `getInLinks()`, and
  `getOutLinks()` each return a fake `IRPCollection`, whose `getAttributeValue(name)`
  returns "value1", and which records `setAttributeValue(name, value)`.
- The wrapper registry populated.
**Test Steps:**
1. Wrap the fake requirement and call `req.getRequirementID()`; assert it returns
   "REQ-001".
2. Call `req.setRequirementID("REQ-002")` and assert the fake received "REQ-002".
3. Wrap the fake instance and call `inst.getAllNestedElements()`; assert an
   `RPCollection` is returned.
4. Call `inst.getAttributeValue("foo")` and assert it returns "value1".
5. Call `inst.setAttributeValue("foo", "bar")` and assert the fake received both
   arguments.
6. Call `inst.getInLinks()` and `inst.getOutLinks()`; assert each returns an
   `RPCollection`.
**Expected Result:**
- Requirement ID get/set delegate correctly with string arguments.
- Instance collection methods return `RPCollection` instances.
- `getAttributeValue` / `setAttributeValue` delegate string arguments correctly.
**Verification Criteria:**
- Pass if all return values and recorded arguments match expectations.
- Fail if any method fails to delegate, or if collection methods return a non-`RPCollection`
  type.
**Last Changed:** 2026-07-07

---

## SYTS_ELEM_00006: Element Module Registration on Import

**ID:** SYTS_ELEM_00006
**Traces-To:** SWR_ELEM_00013, SWR_ELEM_00001, SWR_ELEM_00002, SWR_ELEM_00004
**Title:** Importing elements package populates wrap() registry for all core types
**Type:** System
**Priority:** High
**Description:**
This test verifies that after importing `rhapsody_cli.models.elements`, the `wrap()`
factory's registry is populated for all core element meta classes (Project, Package,
Class, Actor, UseCase, Operation, Attribute, Diagram, Instance, Requirement,
Statechart). A fake COM object with each meta class is wrapped and the correct subclass is
returned.
**Pre-conditions:**
- A set of fake COM objects, each returning one of the core meta class strings from
  `getMetaClass()`.
- A fresh interpreter state where `rhapsody_cli.models.elements` has not yet been
  imported (or the registry is reset and re-populated by import).
**Test Steps:**
1. Import `rhapsody_cli.models.elements` (which transitively imports all element
   modules).
2. For each core meta class string in {"Project", "Package", "Class", "Actor",
   "UseCase", "Operation", "Attribute", "ActivityDiagram", "Instance", "Requirement",
   "Statechart"}, wrap the corresponding fake COM object via `wrap()`.
3. Assert each result is an instance of the expected wrapper subclass (RPProject,
   RPPackage, RPClass, RPActor, RPUseCase, RPOperation, RPAttribute, RPDiagram,
   RPInstance, RPRequirement, RPStatechart).
**Expected Result:**
- After import, every core meta class maps to its dedicated wrapper subclass.
- `wrap()` returns the correct subclass for each fake COM object without raising.
**Verification Criteria:**
- Pass if all isinstance assertions hold for all core meta classes.
- Fail if any meta class is missing from the registry (returns the generic
  `RPModelElement` fallback) or if `wrap()` raises.
**Last Changed:** 2026-07-07
