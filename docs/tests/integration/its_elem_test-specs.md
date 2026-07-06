# Integration Test Specifications - Model Element Wrappers

**Category:** ELEM
**Prefix:** ITS
**Test Type:** Integration
**Last Validated:** 2026-07-07

---

## ITS_ELEM_00001: Project → Package → Class → Attribute creation chain

**ID:** ITS_ELEM_00001
**Traces-To:** SWR_ELEM_00001, SWR_ELEM_00002, SWR_ELEM_00003, SWR_ELEM_00004, SWR_ELEM_00007
**Title:** Chained addPackage().addClass().addAttribute() returns properly wrapped elements at each level
**Type:** Integration
**Priority:** High
**Description:**
Verifies the integration of the model-construction chain across `RPProject.addPackage`,
`RPPackage.addClass`, `RPClassifier.addAttribute`, and the `wrap()` factory. Each `addX(name)`
call returns a wrapped new element whose `_com` is the raw COM object returned by the underlying
`addX` COM call, and that element is immediately usable for the next chained call.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported (registry populated).
- A mock COM project whose `getMetaClass()` returns `"Project"` and whose `addPackage("Pkg")`
  returns a mock COM package.
- The mock COM package's `getMetaClass()` returns `"Package"` and its `addClass("Cls")` returns a
  mock COM class.
- The mock COM class's `getMetaClass()` returns `"Class"` and its `addAttribute("Attr")` returns a
  mock COM attribute whose `getMetaClass()` returns `"Attribute"`.
**Test Steps:**
1. `project = wrap(mock_com_project)`; assert `isinstance(project, RPProject)`.
2. `pkg = project.addPackage("Pkg")`; assert `isinstance(pkg, RPPackage)` and
   `pkg._com is mock_com_package`.
3. `cls = pkg.addClass("Cls")`; assert `isinstance(cls, RPClass)` and `cls._com is mock_com_class`.
4. `attr = cls.addAttribute("Attr")`; assert `isinstance(attr, RPAttribute)` and
   `attr._com is mock_com_attribute`.
5. Assert the underlying COM `addPackage`, `addClass`, `addAttribute` were each called exactly
   once with the corresponding name argument.
**Expected Result:**
The full chain returns correctly typed wrappers at every level; each wrapper's `_com` matches the
raw COM object returned by the preceding `addX` call; the COM layer receives the expected name
arguments.
**Verification Criteria:**
- All four `isinstance` checks pass.
- Each `result._com` is the corresponding mock returned by the prior COM call.
- COM spy call counts are each exactly 1 with the right name argument.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00002: Generalization between two RPClassifier instances

**ID:** ITS_ELEM_00002
**Traces-To:** SWR_ELEM_00003, SWR_ELEM_00004
**Title:** addGeneralization(base) delegates the base classifier's _com to the underlying COM call
**Type:** Integration
**Priority:** High
**Description:**
Verifies that `RPClassifier.addGeneralization` correctly unwraps its `RPClassifier` argument and
passes the raw COM object (`base._com`) to the underlying `addGeneralization` COM method. This
confirms the wrapper-to-wrapper integration pattern: callers pass wrappers, the framework
delegates COM objects.
**Pre-conditions:**
- Two mock COM class objects `derived_com` and `base_com`, both reporting `getMetaClass() ==
  "Class"`.
- `derived_com.addGeneralization(base_com)` is a spy returning a mock generalization element.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `derived = wrap(derived_com)`; `base = wrap(base_com)`.
2. `gen = derived.addGeneralization(base)`.
3. Assert `derived_com.addGeneralization` was called exactly once with `base_com` (the raw COM
   object, NOT the wrapper).
4. Assert the returned `gen` is wrapped (an `RPModelElement` subclass) and its `_com` is the mock
   returned by the COM call.
**Expected Result:**
The wrapper correctly bridges two `RPClassifier` instances: the base wrapper is unwrapped to its
`_com` before the COM call; the resulting generalization is wrapped for the caller.
**Verification Criteria:**
- `derived_com.addGeneralization.call_args` is `(base_com,)` (raw COM, not wrapper).
- The return value is a wrapped `RPModelElement` subclass instance.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00003: Nested element navigation via getPackages and class operations

**ID:** ITS_ELEM_00003
**Traces-To:** SWR_ELEM_00001, SWR_ELEM_00002, SWR_ELEM_00003
**Title:** Navigating getPackages() then getOperations() crosses RPCollection and wrapper boundaries
**Type:** Integration
**Priority:** High
**Description:**
Verifies integration between container-returning navigation methods (`RPProject.getPackages`,
`RPClassifier.getOperations`) and `RPCollection` auto-wrapping. A project's packages must be
returned as an `RPCollection` whose iteration yields `RPPackage` wrappers; navigating further into
a package's class operations must again yield an `RPCollection` of `RPOperation` wrappers.
**Pre-conditions:**
- A mock COM project whose `getMetaClass() == "Project"` and `getPackages()` returns a mock
  `IRPCollection` containing one mock COM package (`getMetaClass() == "Package"`).
- The mock COM package's `getClasses()` returns a mock `IRPCollection` containing one mock COM
  class (`getMetaClass() == "Class"`).
- The mock COM class's `getOperations()` returns a mock `IRPCollection` containing two mock COM
  operations (`getMetaClass() == "Operation"`).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `project = wrap(mock_com_project)`.
2. `pkgs = project.getPackages()`; assert `isinstance(pkgs, RPCollection)` and `len(pkgs) == 1`.
3. `pkg = pkgs[1]`; assert `isinstance(pkg, RPPackage)`.
4. `cls = pkg.getClasses()[1]`; assert `isinstance(cls, RPClass)`.
5. `ops = cls.getOperations()`; assert `isinstance(ops, RPCollection)` and `len(ops) == 2`.
6. Assert every item in `ops` is an `RPOperation`.
**Expected Result:**
Each navigation hop transparently wraps raw COM elements into the correct subclass; collections
and element wrappers compose without manual intervention.
**Verification Criteria:**
- `isinstance` checks at every level pass.
- `len(pkgs) == 1` and `len(ops) == 2`.
- Both items in `ops` are `RPOperation` instances.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00004: RPClass addSuperclass, addConstructor, addDestructor chain

**ID:** ITS_ELEM_00004
**Traces-To:** SWR_ELEM_00004
**Title:** RPClass addSuperclass unwraps the argument; addConstructor/addDestructor wrap their results
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies `RPClass`-specific creation methods integrate correctly with the wrapper layer:
`addSuperclass(super_class)` accepts an `RPClass` and delegates its `_com`;
`addConstructor(arguments_data)` and `addDestructor()` return wrapped new elements.
`getIsAbstract()` returns a Python bool rather than a COM integer.
**Pre-conditions:**
- A mock COM class `child_com` (`getMetaClass() == "Class"`) with spies for `addSuperclass`,
  `addConstructor`, `addDestructor`, and `getIsAbstract`.
- A mock COM class `parent_com` (`getMetaClass() == "Class"`).
- The `addConstructor`/`addDestructor` spies return mock COM elements whose `getMetaClass()` is
  `"Operation"` (constructor/destructor are operations in Rhapsody).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `child = wrap(child_com)`; `parent = wrap(parent_com)`.
2. `child.addSuperclass(parent)`; assert `child_com.addSuperclass` was called with `parent_com`.
3. `ctor = child.addConstructor("void()")`; assert `isinstance(ctor, RPOperation)` (or
   `RPModelElement`) and `ctor._com` is the mock returned by `addConstructor`.
4. `dtor = child.addDestructor()`; assert `dtor._com` is the mock returned by `addDestructor`.
5. Patch `child_com.getIsAbstract` to return `1`; assert `child.getIsAbstract()` is `True`
   (Python bool).
**Expected Result:**
`addSuperclass` unwraps its `RPClass` argument; `addConstructor`/`addDestructor` wrap their
results; `getIsAbstract` translates the COM integer to a Python bool.
**Verification Criteria:**
- `child_com.addSuperclass.call_args == ((parent_com,),)`.
- `ctor._com is mock_com_ctor` and `dtor._com is mock_com_dtor`.
- `child.getIsAbstract() is True` (or `isinstance(..., bool)` and truthy).
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00005: RPActor addEventReceptionWithEvent accepts an RPModelElement event

**ID:** ITS_ELEM_00005
**Traces-To:** SWR_ELEM_00005, SWR_ELEM_00003
**Title:** RPActor.addEventReceptionWithEvent unwraps the event RPModelElement and wraps the reception
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies `RPActor.addEventReceptionWithEvent(name, event)`. The `event` argument is an
`RPModelElement` wrapper; the method must delegate `event._com` to the underlying COM call and
return a wrapped reception. Also confirms `setIsBehaviorOverriden(True)` translates to integer `1`
on the COM side.
**Pre-conditions:**
- A mock COM actor `actor_com` (`getMetaClass() == "Actor"`) with spies for
  `addEventReceptionWithEvent`, `getIsBehaviorOverriden`, and `setIsBehaviorOverriden`.
- A mock COM event `event_com` (`getMetaClass()` unmapped, e.g., `"Event"`).
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `actor = wrap(actor_com)`; `event = wrap(event_com)`.
2. `reception = actor.addEventReceptionWithEvent("recv", event)`.
3. Assert `actor_com.addEventReceptionWithEvent` was called with `("recv", event_com)` (raw COM
   for the event argument).
4. Assert `reception._com` is the mock returned by the COM spy.
5. `actor.setIsBehaviorOverriden(True)`; assert the COM spy received `1`.
6. Patch `actor_com.getIsBehaviorOverriden` to return `0`; assert
   `actor.getIsBehaviorOverriden()` is `False`.
**Expected Result:**
The actor wrapper correctly unwraps the event argument and wraps the reception result; boolean
overrides translate to/from COM integers.
**Verification Criteria:**
- `actor_com.addEventReceptionWithEvent.call_args` matches `("recv", event_com)`.
- `reception._com is mock_com_reception`.
- `actor_com.setIsBehaviorOverriden` last call arg is `1`.
- `actor.getIsBehaviorOverriden() is False`.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00006: RPInstance navigation across nested elements and links

**ID:** ITS_ELEM_00006
**Traces-To:** SWR_ELEM_00009, SWR_CORE_00003
**Title:** RPInstance getAllNestedElements/getInLinks/getOutLinks return RPCollections of wrapped items
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies that `RPInstance`'s collection-returning navigation methods integrate with `RPCollection`
auto-wrapping. Each of `getAllNestedElements()`, `getInLinks()`, and `getOutLinks()` must return
an `RPCollection` whose iteration yields wrapped `RPModelElement` subclasses rather than raw COM
objects. Also confirms `getAttributeValue`/`setAttributeValue` round-trip strings through COM.
**Pre-conditions:**
- A mock COM instance `inst_com` (`getMetaClass() == "Instance"`) with spies for
  `getAllNestedElements`, `getInLinks`, `getOutLinks`, `getAttributeValue`, `setAttributeValue`.
- Each collection spy returns a mock `IRPCollection` with 2 items, each item a mock COM element
  reporting `getMetaClass() == "Instance"` (or any registered type).
- `inst_com.getAttributeValue("color")` returns `"red"`.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `inst = wrap(inst_com)`.
2. `nested = inst.getAllNestedElements()`; assert `isinstance(nested, RPCollection)` and
   `len(nested) == 2`.
3. Assert every item in `nested` is an `RPModelElement` subclass instance.
4. `in_links = inst.getInLinks()`; `out_links = inst.getOutLinks()`; assert both are
   `RPCollection` instances with length 2.
5. `assert inst.getAttributeValue("color") == "red"`.
6. `inst.setAttributeValue("color", "blue")`; assert the COM spy received `("color", "blue")`.
**Expected Result:**
All collection-returning methods produce `RPCollection` wrappers with auto-wrapped items; string
attribute access round-trips correctly through COM.
**Verification Criteria:**
- `isinstance(nested, RPCollection)`, `isinstance(in_links, RPCollection)`,
  `isinstance(out_links, RPCollection)`.
- All iterated items are `RPModelElement` subclass instances.
- `inst_com.setAttributeValue.call_args == (("color", "blue"),)`.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00007: RPUseCase extension point add and retrieve round-trip

**ID:** ITS_ELEM_00007
**Traces-To:** SWR_ELEM_00012, SWR_ELEM_00003
**Title:** RPUseCase.addExtensionPoint then getExtensionPoints round-trips via RPCollection
**Type:** Integration
**Priority:** Medium
**Description:**
Verifies `RPUseCase.addExtensionPoint(entry_point)` and `getExtensionPoints()` integration: the
string argument flows to the underlying COM call, and the returned `RPCollection` of extension
points auto-wraps its items. Confirms `RPUseCase` inherits `RPClassifier` behavior while adding
use-case-specific navigation.
**Pre-conditions:**
- A mock COM use case `uc_com` (`getMetaClass() == "UseCase"`) with spies for
  `addExtensionPoint` and `getExtensionPoints`.
- `addExtensionPoint("main")` returns a mock COM extension point whose `getMetaClass()` is
  unmapped (so it falls back to `RPModelElement`).
- `getExtensionPoints()` returns a mock `IRPCollection` of 1 such mock element.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `uc = wrap(uc_com)`; assert `isinstance(uc, RPUseCase)` and `isinstance(uc, RPClassifier)`.
2. `ep = uc.addExtensionPoint("main")`; assert `uc_com.addExtensionPoint` was called with
   `"main"` and `ep._com` is the mock returned.
3. `eps = uc.getExtensionPoints()`; assert `isinstance(eps, RPCollection)` and `len(eps) == 1`.
4. Assert `eps[1]._com is mock_extension_point`.
**Expected Result:**
`addExtensionPoint` round-trips the string and wraps the result; `getExtensionPoints` returns an
`RPCollection` whose single item is the previously added extension point.
**Verification Criteria:**
- `isinstance(uc, RPUseCase)` and `isinstance(uc, RPClassifier)` (inheritance).
- `uc_com.addExtensionPoint.call_args == (("main",),)`.
- `len(eps) == 1` and `eps[1]._com is mock_extension_point`.
**Last Changed:** 2026-07-07

---

## ITS_ELEM_00008: RPStatechart addNewNodeByType returns wrapped node and integrates with deleteState

**ID:** ITS_ELEM_00008
**Traces-To:** SWR_ELEM_00011, SWR_ELEM_00003
**Title:** RPStatechart.addNewNodeByType wraps the new node; deleteState accepts an RPModelElement
**Type:** Integration
**Priority:** Low
**Description:**
Verifies `RPStatechart` integration with the wrapper layer: `addNewNodeByType(meta_type, x, y, w, h)`
returns a wrapped node, and `deleteState(state)` accepts an `RPModelElement` and delegates its
`_com` to the underlying COM call. Also confirms `createGraphics()` and `closeDiagram()` are
callable delegations.
**Pre-conditions:**
- A mock COM statechart `sc_com` (`getMetaClass() == "Statechart"`) with spies for
  `addNewNodeByType`, `deleteState`, `createGraphics`, `closeDiagram`.
- `addNewNodeByType("State", 10, 20, 30, 40)` returns a mock COM node whose `getMetaClass()` is
  unmapped.
- A mock COM state `state_com` whose `getMetaClass()` is unmapped.
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. `sc = wrap(sc_com)`; assert `isinstance(sc, RPStatechart)`.
2. `node = sc.addNewNodeByType("State", 10, 20, 30, 40)`; assert `node._com is mock_node`.
3. Assert `sc_com.addNewNodeByType` was called with `("State", 10, 20, 30, 40)`.
4. `state = wrap(state_com)`; `sc.deleteState(state)`; assert `sc_com.deleteState` was called
   with `state_com` (raw COM, not the wrapper).
5. `sc.createGraphics()`; `sc.closeDiagram()`; assert both COM spies were called once.
**Expected Result:**
The statechart wrapper creates and wraps nodes, unwraps state arguments for deletion, and
delegates graphics operations through `call_com`.
**Verification Criteria:**
- `node._com is mock_node`.
- `sc_com.addNewNodeByType.call_args == (("State", 10, 20, 30, 40),)`.
- `sc_com.deleteState.call_args == ((state_com,),)`.
- `sc_com.createGraphics.call_count == 1` and `sc_com.closeDiagram.call_count == 1`.
**Last Changed:** 2026-07-07

---
