# Acceptance Test Specifications - Model Element Wrappers

**Category:** ELEM
**Prefix:** ATS
**Test Type:** Acceptance
**Last Validated:** 2026-07-07

---

## ATS_ELEM_00001: Build a Model Hierarchy (Package -> Class -> Attribute/Operation)

**ID:** ATS_ELEM_00001
**Traces-To:** SWR_ELEM_00001, SWR_ELEM_00002, SWR_ELEM_00003, SWR_ELEM_00004, SWR_ELEM_00006, SWR_ELEM_00007, SWR_ELEM_00013
**Title:** Construct a package, add a class, and add an attribute and operation to it
**Type:** Acceptance
**Priority:** High
**Description:**
As a model author, I want to build a model from scratch by adding a package, then a class
inside it, then an attribute and an operation on the class, so that I can script the
creation of structured UML/SysML models.
**Acceptance Criteria:**
- Given an open `RPProject`, When I call `project.addPackage("Domain")`, Then an
  `RPPackage` named `"Domain"` is returned and appears in `project.getPackages()`.
- Given the new `RPPackage`, When I call `package.addClass("Vehicle")`, Then an `RPClass`
  named `"Vehicle"` is returned (meta class `"Class"`).
- Given the new `RPClass`, When I call `cls.addAttribute("speed")` and
  `cls.addOperation("start()")`, Then an `RPAttribute` and an `RPOperation` are returned,
  and `cls.getAttributes()` and `cls.getOperations()` each contain the new element.
- Given `rhapsody_cli.models.elements` has been imported, When I call `wrap()` on each
  newly created element, Then the correct wrapper class (`RPPackage`, `RPClass`,
  `RPAttribute`, `RPOperation`) is returned (registration on import works).
**Verification Criteria:**
Open a fixture project, call `addPackage("Domain")`, then `addClass("Vehicle")`, then
`addAttribute("speed")` and `addOperation("start()")`. Assert each returned object's
`getName()` and `getMetaClass()` match expectations. Assert
`"speed" in [a.getName() for a in cls.getAttributes()]` and
`"start()" in [o.getName() for o in cls.getOperations()]`. Call `project.save()` and
reopen the project to confirm the hierarchy persists.
**Last Changed:** 2026-07-07

---

## ATS_ELEM_00002: Manage Generalization Between Classifiers

**ID:** ATS_ELEM_00002
**Traces-To:** SWR_ELEM_00003, SWR_ELEM_00004
**Title:** Add a generalization (inheritance) from one class to a base class
**Type:** Acceptance
**Priority:** High
**Description:**
As a model author, I want to make one class inherit from another, so that I can express
UML generalization relationships in the model.
**Acceptance Criteria:**
- Given two `RPClass` instances `derived` and `base` in the same package, When I call
  `derived.addGeneralization(base)`, Then a generalization relationship is created in the
  model from `derived` to `base` and no exception is raised.
- Given the same two classes, When I call `derived.addSuperclass(base)`, Then `base`
  becomes a superclass of `derived` (the relationship is reflected when querying
  inheritance-related collections on `derived`).
- Given the `addGeneralization` method, When I pass a non-`RPClassifier` argument, Then
  the behavior matches the underlying COM call's contract (the wrapper delegates the
  argument's `_com` attribute, so passing an `RPClassifier` is the supported path).
**Verification Criteria:**
In a fixture project, create `class Animal` and `class Dog`, then call
`Dog.addSuperclass(Animal)` and `Dog.addGeneralization(Animal)` (on separate fixtures if
needed to avoid double-add). Open the project in the Rhapsody GUI and confirm the
inheritance arrow is drawn between `Dog` and `Animal`. Programmatically, query the
generalization-related collection on `Dog` and confirm an entry referencing `Animal`
exists. No `pywintypes.com_error` should leak; any failure must surface as
`RhapsodyRuntimeException`.
**Last Changed:** 2026-07-07

---

## ATS_ELEM_00003: Query Operations and Attributes of a Class

**ID:** ATS_ELEM_00003
**Traces-To:** SWR_ELEM_00003, SWR_ELEM_00006, SWR_ELEM_00007
**Title:** Read bodies, abstract/static/virtual flags, and attribute properties
**Type:** Acceptance
**Priority:** High
**Description:**
As a test engineer, I want to query the body, abstract/static/virtual flags of an
operation and the multiplicity/visibility/default value of an attribute, so that I can
write assertions about the structure of existing model elements.
**Acceptance Criteria:**
- Given an `RPOperation` with a defined body, When I call `op.getBody()`, Then the
  operation's body text is returned as a string; and `op.getIsAbstract()`,
  `op.getIsStatic()`, and `op.getIsVirtual()` each return a boolean.
- Given an `RPOperation`, When I call `op.getReturns()`, Then the return type element is
  returned (wrapped) or `None`/empty when no return type is set.
- Given an `RPAttribute`, When I call `attr.getMultiplicity()`, `attr.getVisibility()`,
  and `attr.getDefaultValue()`, Then the corresponding string values are returned; and
  after `setMultiplicity("1..*")`, `setVisibility("private")`, and
  `setDefaultValue("0")`, the next getters return the new values.
- Given an `RPAttribute`, When I call `attr.setIsStatic(True)`, Then
  `attr.getIsStatic()` subsequently returns `True` (bool-to-int translation succeeds).
**Verification Criteria:**
On a fixture class, add an operation `start()` with a body, set it abstract/static/virtual
via the GUI (or via a setup script), then assert each `getIs*()` returns the expected
boolean. Add an attribute `count`, call `setMultiplicity("0..1")`,
`setVisibility("protected")`, `setDefaultValue("0")`, `setIsStatic(True)`, then assert
each getter returns the just-set value. Confirm `getBody()` returns a non-empty string
for an operation whose body has been populated.
**Last Changed:** 2026-07-07

---

## ATS_ELEM_00004: Manipulate Diagrams and Instance Graphic Elements

**ID:** ATS_ELEM_00004
**Traces-To:** SWR_ELEM_00008, SWR_ELEM_00009
**Title:** Close a diagram, add a text box, and query instance links and attributes
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a test engineer, I want to manipulate diagrams (close, add text boxes, find graphic
elements for a model element) and query instance-level attributes and links, so that I
can script diagram layout and inspect object-level relationships.
**Acceptance Criteria:**
- Given an `RPDiagram` (e.g., an activity or class diagram), When I call
  `diagram.closeDiagram()`, Then the diagram is closed in the GUI without error.
- Given an `RPDiagram`, When I call
  `diagram.addTextBox("Note", 100, 100, 200, 50)`, Then a wrapped text box element is
  returned and the text box appears on the diagram.
- Given an `RPDiagram` and a model element `elem` that has a presentation on the diagram,
  When I call `diagram.getCorrespondingGraphicElements(elem)`, Then an `RPCollection` of
  graphic elements is returned (possibly empty if none exist, but no exception).
- Given an `RPInstance`, When I call `inst.getAttributeValue("Name")` and
  `inst.setAttributeValue("Name", "value")`, Then the value can be round-tripped; and
  `inst.getInLinks()` and `inst.getOutLinks()` each return an `RPCollection`.
**Verification Criteria:**
Open a fixture project containing a class diagram, obtain the `RPDiagram`, add a text box
with known coordinates, and confirm via `getCorrespondingGraphicElements` (or the GUI)
that a graphic element now exists. Call `closeDiagram()` and confirm the diagram window
closes. On an `RPInstance` representing an object linkable to others, set and get an
attribute value to confirm round-trip, and assert `getInLinks()` and `getOutLinks()` each
return an `RPCollection` (length may be 0 in a sparse fixture but the call must succeed).
**Last Changed:** 2026-07-07

---

## ATS_ELEM_00005: Manage Statecharts and Their Nodes

**ID:** ATS_ELEM_00005
**Traces-To:** SWR_ELEM_00011, SWR_ELEM_00003
**Title:** Add a statechart to a classifier, add nodes, and delete a state
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a model author, I want to add a statechart to a class, add state nodes to it, and
delete a state, so that I can script the construction of behavioral state machines.
**Acceptance Criteria:**
- Given an `RPClassifier` (e.g., an `RPClass`), When I call `cls.addStatechart()`, Then a
  wrapped `RPStatechart` is returned and registered with meta class `"Statechart"`.
- Given the new `RPStatechart`, When I call
  `chart.addNewNodeByType("State", 10, 10, 120, 60)`, Then a wrapped state node is
  returned and appears on the statechart.
- Given the `RPStatechart` and a previously added state node, When I call
  `chart.deleteState(state)`, Then the state is removed from the statechart without error.
- Given the `RPStatechart`, When I call `chart.createGraphics()` and
  `chart.closeDiagram()`, Then both calls succeed (no exception).
**Verification Criteria:**
In a fixture project, create a class `Controller`, call `addStatechart()` to get a chart,
then `addNewNodeByType("State", 10, 10, 120, 60)` to add a state. Assert the returned
node is non-`None` and wraps a COM object. Call `deleteState(node)` on that node and
assert no exception is raised; confirm via the GUI (or by re-querying the chart's
elements) that the state is gone. Call `createGraphics()` and `closeDiagram()` and assert
neither raises.
**Last Changed:** 2026-07-07

---

## ATS_ELEM_00006: Manage Requirements, Use Cases, and Actors

**ID:** ATS_ELEM_00006
**Traces-To:** SWR_ELEM_00005, SWR_ELEM_00010, SWR_ELEM_00012
**Title:** Read/write requirement IDs, manage use case extension points, and configure actors
**Type:** Acceptance
**Priority:** Medium
**Description:**
As a model author, I want to set and query requirement IDs, manage use case extension
points and describing diagrams, and toggle actor behavior override, so that I can script
traceability and use-case/actor configuration.
**Acceptance Criteria:**
- Given an `RPRequirement`, When I call `req.setRequirementID("REQ-001")`, Then
  `req.getRequirementID()` subsequently returns `"REQ-001"`.
- Given an `RPUseCase`, When I call `uc.addExtensionPoint("main success")`, Then the
  extension point is added; and `uc.getExtensionPoints()`, `uc.getEntryPoints()`, and
  `uc.getDescribingDiagrams()` each return an `RPCollection` (possibly empty, but no
  exception).
- Given an `RPActor`, When I call `actor.setIsBehaviorOverriden(True)`, Then
  `actor.getIsBehaviorOverriden()` subsequently returns `True` (bool-to-int translation
  succeeds).
- Given an `RPActor` and an `RPModelElement` event, When I call
  `actor.addEventReceptionWithEvent("onClick", event)`, Then a wrapped reception is
  returned.
**Verification Criteria:**
On a fixture project, locate (or create) an `RPRequirement`, call `setRequirementID`
with a known string, and assert the getter returns that exact string. On an `RPUseCase`,
add an extension point and assert the three collection-returning methods each yield an
`RPCollection` instance without raising. On an `RPActor`, toggle
`setIsBehaviorOverriden(True)` and assert `getIsBehaviorOverriden()` returns `True`, then
toggle back to `False` and assert it returns `False`. If a fixture event element is
available, call `addEventReceptionWithEvent` and assert the returned object is a wrapped
reception element.
**Last Changed:** 2026-07-07

---
