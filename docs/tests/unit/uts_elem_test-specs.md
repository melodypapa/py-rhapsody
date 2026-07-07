# Unit Test Specifications - Model Element Wrappers

**Category:** ELEM
**Prefix:** UTS
**Test Type:** Unit
**Last Validated:** 2026-07-07

---

## UTS_ELEM_00001: RPProject Extends RPPackage

**ID:** UTS_ELEM_00001
**Traces-To:** SWR_ELEM_00001
**Title:** RPProject is a subclass of RPPackage and registers itself for meta class "Project"
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RPProject` extends `RPPackage` and is registered in `_WRAPPER_REGISTRY` under the meta class `"Project"` at import time of `rhapsody_cli.models.elements.containment`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported so the registry is populated.
- Access to `_WRAPPER_REGISTRY` from `rhapsody_cli.models._core`.
**Test Steps:**
1. Import `rhapsody_cli.models.elements.containment` and `rhapsody_cli.models._core` (for the registry).
2. Assert `issubclass(RPProject, RPPackage)`.
3. Assert `_WRAPPER_REGISTRY["Project"] is RPProject`.
**Expected Result:**
`RPProject` is a subclass of `RPPackage`, and the registry maps `"Project"` to `RPProject`.
**Verification Criteria:**
Pass if both assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00002: RPProject addPackage/close/becomeActiveProject/findComponent/getPackages

**ID:** UTS_ELEM_00002
**Traces-To:** SWR_ELEM_00001
**Title:** RPProject methods delegate to COM and wrap returned elements
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `addPackage(name)` returns a wrapped `RPPackage`, `close()` and `becomeActiveProject()` return `None`, `findComponent(name)` returns a wrapped element, and `getPackages()` returns an `RPCollection`.
**Pre-conditions:**
- A fake project COM object built via `tests.fakes.make_fake_element("Project")` configured with `addPackage.return_value = make_fake_element("Package")`, `findComponent.return_value = make_fake_element("Component")`, and `getPackages.return_value = make_fake_collection([make_fake_element("Package")])`.
- An `RPProject` constructed with that fake object.
**Test Steps:**
1. Construct `proj = RPProject(fake)`.
2. Call `proj.addPackage("P1")` and assert the result is an `RPPackage` whose `_com` is the fake package returned by COM.
3. Call `proj.close()` and assert it returns `None`; assert `fake.close` was called once.
4. Call `proj.becomeActiveProject()` and assert it returns `None`; assert `fake.becomeActiveProject` was called once.
5. Call `proj.findComponent("C1")` and assert the result is a wrapped `RPModelElement` whose `_com` is the fake component.
6. Call `proj.getPackages()` and assert the result is an `RPCollection`.
**Expected Result:**
All methods delegate correctly. `addPackage` returns a wrapped `RPPackage`; `findComponent` returns a wrapped element; `getPackages` returns an `RPCollection`; `close`/`becomeActiveProject` return `None`.
**Verification Criteria:**
Pass if all type/`_com` assertions hold and `fake.addPackage.call_args == call("P1")`, `fake.findComponent.call_args == call("C1")`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00003: RPPackage Extends RPUnit and Registers for "Package"

**ID:** UTS_ELEM_00003
**Traces-To:** SWR_ELEM_00002
**Title:** RPPackage is a subclass of RPUnit registered under meta class "Package"
**Type:** Unit
**Priority:** High
**Description:**
Verifies the inheritance and registration contract for `RPPackage`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPPackage` and `RPUnit` and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPPackage, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Package"] is RPPackage`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if `RPPackage` subclasses `RPUnit` and the registry maps `"Package"` to `RPPackage`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00004: RPPackage Creation Methods Return Wrapped Elements

**ID:** UTS_ELEM_00004
**Traces-To:** SWR_ELEM_00002
**Title:** RPPackage.addClass/addNestedPackage/addActor/addGlobalFunction wrap their results
**Type:** Unit
**Priority:** High
**Description:**
Verifies that the four `addX` creation methods on `RPPackage` call the corresponding COM method with the supplied name and return the result wrapped via `wrap()`.
**Pre-conditions:**
- A fake package COM object built via `make_fake_element("Package")` with each `addClass`/`addNestedPackage`/`addActor`/`addGlobalFunction` returning a distinct fake element built via `make_fake_element` with the appropriate meta class.
**Test Steps:**
1. Construct `pkg = RPPackage(fake)`.
2. Call `pkg.addClass("C")`, `pkg.addNestedPackage("P")`, `pkg.addActor("A")`, `pkg.addGlobalFunction("F")`.
3. Inspect the type and `_com` of each result; inspect the COM call args.
**Expected Result:**
Each result is a wrapped `RPModelElement` (or subclass) whose `_com` is the corresponding fake element returned by COM. Each COM method was called once with the supplied name.
**Verification Criteria:**
Pass if each result `_com` matches the configured fake and the COM call args match the supplied names.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00005: RPClassifier Extends RPUnit

**ID:** UTS_ELEM_00005
**Traces-To:** SWR_ELEM_00003
**Title:** RPClassifier is a subclass of RPUnit
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `RPClassifier` extends `RPUnit` so that all `RPUnit` save/file operations are inherited by Class/Actor/UseCase.
**Pre-conditions:**
- Imports available.
**Test Steps:**
1. Import `RPClassifier` and `RPUnit`.
2. Assert `issubclass(RPClassifier, RPUnit)`.
**Expected Result:**
`RPClassifier` is a subclass of `RPUnit`.
**Verification Criteria:**
Pass if the subclass relationship holds.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00006: RPClassifier addAttribute/addOperation/getAttributes/getOperations/addStatechart

**ID:** UTS_ELEM_00006
**Traces-To:** SWR_ELEM_00003
**Title:** RPClassifier accessor/creation methods delegate to COM and wrap results
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `addAttribute(name)` and `addOperation(name)` return wrapped elements; `getAttributes()` and `getOperations()` return `RPCollection`; `addStatechart()` returns a wrapped statechart.
**Pre-conditions:**
- A fake classifier COM object via `make_fake_element("Classifier")` configured so that `addAttribute` returns `make_fake_element("Attribute")`, `addOperation` returns `make_fake_element("Operation")`, `addStatechart` returns `make_fake_element("Statechart")`, `getAttributes` returns `make_fake_collection([make_fake_element("Attribute")])`, and `getOperations` returns `make_fake_collection([make_fake_element("Operation")])`.
**Test Steps:**
1. Construct `clf = RPClassifier(fake)`.
2. Call `clf.addAttribute("a")` and assert the result is a wrapped element.
3. Call `clf.addOperation("o")` and assert the result is a wrapped element.
4. Call `clf.getAttributes()` and assert the result is an `RPCollection` with `len == 1`.
5. Call `clf.getOperations()` and assert the result is an `RPCollection` with `len == 1`.
6. Call `clf.addStatechart()` and assert the result is a wrapped element.
**Expected Result:**
All methods delegate correctly and wrap their results; collection-returning methods return `RPCollection` instances.
**Verification Criteria:**
Pass if all type/`_com`/length assertions hold and the COM methods are called with the supplied names.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00007: RPClassifier addGeneralization Unwraps the Base Classifier

**ID:** UTS_ELEM_00007
**Traces-To:** SWR_ELEM_00003
**Title:** RPClassifier.addGeneralization delegates the base classifier's _com to COM
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `addGeneralization(base_classifier)` accepts an `RPClassifier` and passes its `_com` (not the wrapper itself) to the underlying COM `addGeneralization`.
**Pre-conditions:**
- A fake classifier COM object `fake_clf` (the derived classifier).
- A fake base classifier COM object `fake_base` and `base = RPClassifier(fake_base)`.
**Test Steps:**
1. Construct `clf = RPClassifier(fake_clf)`.
2. Call `clf.addGeneralization(base)`.
3. Inspect `fake_clf.addGeneralization` call args.
**Expected Result:**
`fake_clf.addGeneralization` was called once with `fake_base` (the unwrapped `_com`), not the `RPClassifier` wrapper.
**Verification Criteria:**
Pass if `fake_clf.addGeneralization.call_args == call(fake_base)`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00008: RPClass Extends RPClassifier and Registers for "Class"

**ID:** UTS_ELEM_00008
**Traces-To:** SWR_ELEM_00004
**Title:** RPClass is a subclass of RPClassifier registered under meta class "Class"
**Type:** Unit
**Priority:** High
**Description:**
Verifies the inheritance chain `RPClass -> RPClassifier -> RPUnit` and the `"Class"` registry entry.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPClass`, `RPClassifier`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPClass, RPClassifier)` and `issubclass(RPClass, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Class"] is RPClass`.
**Expected Result:**
Both subclass relationships hold and the registry maps `"Class"` to `RPClass`.
**Verification Criteria:**
Pass if all three assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00009: RPClass Methods Delegate and Translate Bools

**ID:** UTS_ELEM_00009
**Traces-To:** SWR_ELEM_00004
**Title:** RPClass addSuperclass/addConstructor/addDestructor/getIsAbstract/addClass behave per spec
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `addSuperclass(super_class)` unwraps and forwards `_com`; `addConstructor(arguments_data)` and `addDestructor()` return wrapped elements; `getIsAbstract()` returns a Python `bool`; `addClass(name)` returns a wrapped nested class.
**Pre-conditions:**
- A fake class COM object via `make_fake_element("Class")` configured so `addConstructor` returns `make_fake_element("Operation")`, `addDestructor` returns `make_fake_element("Operation")`, `addClass` returns `make_fake_element("Class")`, and `getIsAbstract` returns `1`.
- A second fake class `fake_super` and `super_class = RPClass(fake_super)`.
**Test Steps:**
1. Construct `cls = RPClass(fake)`.
2. Call `cls.addSuperclass(super_class)` and assert `fake.addSuperclass.call_args == call(fake_super)`.
3. Call `cls.addConstructor("args")` and assert the result is a wrapped element.
4. Call `cls.addDestructor()` and assert the result is a wrapped element.
5. Call `cls.getIsAbstract()` and assert the result is `True` (a `bool`, not an int).
6. Call `cls.addClass("Nested")` and assert the result is a wrapped `RPClass`.
**Expected Result:**
`addSuperclass` forwards the unwrapped `_com`; the `addX` methods wrap their results; `getIsAbstract()` returns a Python `bool`.
**Verification Criteria:**
Pass if all assertions hold, especially `type(cls.getIsAbstract()) is bool` and `cls.getIsAbstract() is True`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00010: RPClass COM Error Translated to RhapsodyRuntimeException

**ID:** UTS_ELEM_00010
**Traces-To:** SWR_ELEM_00004
**Title:** RPClass methods translate com_error raised by the underlying COM into RhapsodyRuntimeException
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that a COM method on `RPClass` (e.g., `addClass`) raises `RhapsodyRuntimeException` (via `call_com`) when the underlying COM object raises a `pywintypes.com_error`.
**Pre-conditions:**
- A fake class COM object via `make_fake_element("Class")` with `addClass.side_effect = tests.fakes.make_com_error("dup name")`.
**Test Steps:**
1. Construct `cls = RPClass(fake)`.
2. Call `cls.addClass("Dup")` inside `assertRaises(RhapsodyRuntimeException)`.
3. Inspect the exception message.
**Expected Result:**
`RhapsodyRuntimeException` is raised; its message contains `"dup name"`.
**Verification Criteria:**
Pass if the exception is `RhapsodyRuntimeException` and `"dup name"` is in `str(exc)`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00011: RPActor Extends RPClassifier and Registers for "Actor"

**ID:** UTS_ELEM_00011
**Traces-To:** SWR_ELEM_00005
**Title:** RPActor is a subclass of RPClassifier registered under meta class "Actor"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain and registry entry for `RPActor`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPActor`, `RPClassifier`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPActor, RPClassifier)`.
3. Assert `_WRAPPER_REGISTRY["Actor"] is RPActor`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00012: RPActor Methods Translate Bools and Unwrap Event

**ID:** UTS_ELEM_00012
**Traces-To:** SWR_ELEM_00005
**Title:** RPActor addEventReceptionWithEvent/getIsBehaviorOverriden/setIsBehaviorOverriden behave per spec
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `addEventReceptionWithEvent(name, event)` unwraps `event._com` and returns a wrapped reception; `getIsBehaviorOverriden()` returns a Python `bool`; `setIsBehaviorOverriden(True)` calls COM with `1` and `setIsBehaviorOverriden(False)` calls COM with `0`.
**Pre-conditions:**
- A fake actor COM object via `make_fake_element("Actor")` with `addEventReceptionWithEvent.return_value = make_fake_element("EventReception")` and `getIsBehaviorOverriden.return_value = 1`.
- A fake event `fake_evt` and `event = RPModelElement(fake_evt)`.
**Test Steps:**
1. Construct `actor = RPActor(fake)`.
2. Call `actor.addEventReceptionWithEvent("r", event)` and assert the result is a wrapped element; assert `fake.addEventReceptionWithEvent.call_args == call("r", fake_evt)`.
3. Call `actor.getIsBehaviorOverriden()` and assert the result is `True` with `type(...) is bool`.
4. Call `actor.setIsBehaviorOverriden(True)` then `actor.setIsBehaviorOverriden(False)`.
5. Inspect `fake.setIsBehaviorOverriden` call args list.
**Expected Result:**
`addEventReceptionWithEvent` forwards the unwrapped `_com`; `getIsBehaviorOverriden()` returns `True` as a `bool`; `setIsBehaviorOverriden` calls COM with `1` then `0`.
**Verification Criteria:**
Pass if all assertions hold, including the two `setIsBehaviorOverriden` calls using `1` and `0`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00013: RPOperation Extends RPUnit and Registers for "Operation"

**ID:** UTS_ELEM_00013
**Traces-To:** SWR_ELEM_00006
**Title:** RPOperation is a subclass of RPUnit registered under meta class "Operation"
**Type:** Unit
**Priority:** High
**Description:**
Verifies the inheritance chain and registry entry for `RPOperation`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPOperation`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPOperation, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Operation"] is RPOperation`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00014: RPOperation Methods Return Strings, Bools, and Wrapped Elements

**ID:** UTS_ELEM_00014
**Traces-To:** SWR_ELEM_00006
**Title:** RPOperation getBody/getIsAbstract/getIsStatic/getIsVirtual/getReturns/createAutoFlowChart behave per spec
**Type:** Unit
**Priority:** High
**Description:**
Verifies that `getBody()` returns a `str`; `getIsAbstract()`, `getIsStatic()`, `getIsVirtual()` return Python `bool`s; `getReturns()` returns a wrapped element; `createAutoFlowChart()` delegates to COM and returns `None` (or whatever COM returns, untranslated as a wrapper).
**Pre-conditions:**
- A fake operation COM object via `make_fake_element("Operation")` configured with `getBody.return_value = "return x;"`, `getIsAbstract.return_value = 1`, `getIsStatic.return_value = 0`, `getIsVirtual.return_value = 1`, `getReturns.return_value = make_fake_element("Class")`.
**Test Steps:**
1. Construct `op = RPOperation(fake)`.
2. Call `op.getBody()` and assert the result is `"return x;"`.
3. Call `op.getIsAbstract()`, `op.getIsStatic()`, `op.getIsVirtual()` and assert the results are `True`, `False`, `True` respectively, each with `type(...) is bool`.
4. Call `op.getReturns()` and assert the result is a wrapped `RPModelElement` whose `_com` is the configured fake.
5. Call `op.createAutoFlowChart()` and assert `fake.createAutoFlowChart` was called once.
**Expected Result:**
All return-type contracts hold; `getReturns()` returns a wrapped element; `createAutoFlowChart()` delegates to COM.
**Verification Criteria:**
Pass if every assertion holds, especially the bool-type checks.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00015: RPAttribute Extends RPUnit and Registers for "Attribute"

**ID:** UTS_ELEM_00015
**Traces-To:** SWR_ELEM_00007
**Title:** RPAttribute is a subclass of RPUnit registered under meta class "Attribute"
**Type:** Unit
**Priority:** High
**Description:**
Verifies the inheritance chain and registry entry for `RPAttribute`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPAttribute`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPAttribute, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Attribute"] is RPAttribute`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00016: RPAttribute Getters/Setters Round-Trip and Translate Bools

**ID:** UTS_ELEM_00016
**Traces-To:** SWR_ELEM_00007
**Title:** RPAttribute multiplicity/isStatic/visibility/defaultValue getters and setters behave per spec
**Type:** Unit
**Priority:** High
**Description:**
Verifies the str getters/setters for `Multiplicity`/`Visibility`/`DefaultValue` forward verbatim, and the bool `isStatic` getter returns a Python `bool` while the setter translates `True`/`False` to `1`/`0`.
**Pre-conditions:**
- A fake attribute COM object via `make_fake_element("Attribute")` configured with `getMultiplicity.return_value = "1"`, `getIsStatic.return_value = 1`, `getVisibility.return_value = "public"`, `getDefaultValue.return_value = "0"`.
**Test Steps:**
1. Construct `attr = RPAttribute(fake)`.
2. Assert `attr.getMultiplicity() == "1"`; call `attr.setMultiplicity("0..1")` and assert `fake.setMultiplicity.call_args == call("0..1")`.
3. Assert `attr.getIsStatic() is True` and `type(...) is bool`; call `attr.setIsStatic(False)` and assert `fake.setIsStatic.call_args == call(0)`.
4. Assert `attr.getVisibility() == "public"`; call `attr.setVisibility("private")` and assert the call arg.
5. Assert `attr.getDefaultValue() == "0"`; call `attr.setDefaultValue("1")` and assert the call arg.
**Expected Result:**
Str getters return the configured strings; str setters forward verbatim; `getIsStatic()` returns a Python `bool`; `setIsStatic(False)` calls COM with `0`.
**Verification Criteria:**
Pass if all assertions hold, especially `setIsStatic(False)` calling COM with the integer `0`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00017: RPDiagram Extends RPUnit and Registers for "ActivityDiagram"

**ID:** UTS_ELEM_00017
**Traces-To:** SWR_ELEM_00008
**Title:** RPDiagram is a subclass of RPUnit registered under meta class "ActivityDiagram"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain and registry entry for `RPDiagram` (note: registered for the meta class `"ActivityDiagram"`).
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPDiagram`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPDiagram, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["ActivityDiagram"] is RPDiagram`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold, with the registry key being exactly `"ActivityDiagram"`.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00018: RPDiagram Methods Delegate and Return Collections

**ID:** UTS_ELEM_00018
**Traces-To:** SWR_ELEM_00008
**Title:** RPDiagram closeDiagram/addTextBox/getCustomViews/getCorrespondingGraphicElements behave per spec
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `closeDiagram()` returns `None`; `addTextBox(text, x, y, w, h)` forwards all five args and returns a wrapped element; `getCustomViews()` returns an `RPCollection`; `getCorrespondingGraphicElements(model_element)` unwraps the element's `_com` and returns an `RPCollection`.
**Pre-conditions:**
- A fake diagram COM object via `make_fake_element("ActivityDiagram")` configured with `addTextBox.return_value = make_fake_element("GraphicObject")`, `getCustomViews.return_value = make_fake_collection([make_fake_element("GraphicObject")])`, `getCorrespondingGraphicElements.return_value = make_fake_collection([])`.
- A fake model element `fake_el` and `el = RPModelElement(fake_el)`.
**Test Steps:**
1. Construct `diag = RPDiagram(fake)`.
2. Call `diag.closeDiagram()` and assert it returns `None`.
3. Call `diag.addTextBox("hi", 10, 20, 100, 50)` and assert the result is a wrapped element; assert `fake.addTextBox.call_args == call("hi", 10, 20, 100, 50)`.
4. Call `diag.getCustomViews()` and assert the result is an `RPCollection`.
5. Call `diag.getCorrespondingGraphicElements(el)` and assert the result is an `RPCollection`; assert `fake.getCorrespondingGraphicElements.call_args == call(fake_el)`.
**Expected Result:**
All methods delegate correctly; collection-returning methods return `RPCollection`; `getCorrespondingGraphicElements` unwraps the supplied element.
**Verification Criteria:**
Pass if all type/call-args assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00019: RPInstance Extends RPRelation and Registers for "Instance"

**ID:** UTS_ELEM_00019
**Traces-To:** SWR_ELEM_00009
**Title:** RPInstance is a subclass of RPRelation registered under meta class "Instance"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain and registry entry for `RPInstance`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPInstance`, `RPRelation`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPInstance, RPRelation)`.
3. Assert `_WRAPPER_REGISTRY["Instance"] is RPInstance`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00020: RPInstance Methods Return Strings and Collections

**ID:** UTS_ELEM_00020
**Traces-To:** SWR_ELEM_00009
**Title:** RPInstance getAllNestedElements/getAttributeValue/setAttributeValue/getInLinks/getOutLinks behave per spec
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `getAllNestedElements()`, `getInLinks()`, `getOutLinks()` return `RPCollection`; `getAttributeValue(name)` returns a `str`; `setAttributeValue(name, value)` forwards both string args.
**Pre-conditions:**
- A fake instance COM object via `make_fake_element("Instance")` configured with `getAllNestedElements.return_value = make_fake_collection([make_fake_element("Class")])`, `getInLinks.return_value = make_fake_collection([])`, `getOutLinks.return_value = make_fake_collection([])`, `getAttributeValue.return_value = "v1"`.
**Test Steps:**
1. Construct `inst = RPInstance(fake)`.
2. Call `inst.getAllNestedElements()` and assert it is an `RPCollection` with `len == 1`.
3. Call `inst.getAttributeValue("kind")` and assert it returns `"v1"`.
4. Call `inst.setAttributeValue("kind", "v2")` and assert `fake.setAttributeValue.call_args == call("kind", "v2")`.
5. Call `inst.getInLinks()` and `inst.getOutLinks()` and assert both return `RPCollection`.
**Expected Result:**
All collection-returning methods return `RPCollection`; `getAttributeValue` returns a string; `setAttributeValue` forwards both args verbatim.
**Verification Criteria:**
Pass if all type/value/call-args assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00021: RPRequirement Extends RPUnit and Registers for "Requirement"

**ID:** UTS_ELEM_00021
**Traces-To:** SWR_ELEM_00010
**Title:** RPRequirement is a subclass of RPUnit registered under meta class "Requirement"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain and registry entry for `RPRequirement`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPRequirement`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPRequirement, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Requirement"] is RPRequirement`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00022: RPRequirement getRequirementID/setRequirementID Round-Trip

**ID:** UTS_ELEM_00022
**Traces-To:** SWR_ELEM_00010
**Title:** RPRequirement getRequirementID returns str and setRequirementID forwards verbatim
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `getRequirementID()` returns a `str` (via `str(...)` of the COM result) and `setRequirementID(requirement_id)` forwards the supplied string to COM.
**Pre-conditions:**
- A fake requirement COM object via `make_fake_element("Requirement")` with `getRequirementID.return_value = "REQ-001"`.
**Test Steps:**
1. Construct `req = RPRequirement(fake)`.
2. Call `req.getRequirementID()` and assert it returns `"REQ-001"`.
3. Call `req.setRequirementID("REQ-002")` and assert `fake.setRequirementID.call_args == call("REQ-002")`.
**Expected Result:**
`getRequirementID()` returns `"REQ-001"`; `setRequirementID` forwards `"REQ-002"` verbatim.
**Verification Criteria:**
Pass if both assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00023: RPStatechart Extends RPUnit and Registers for "Statechart"

**ID:** UTS_ELEM_00023
**Traces-To:** SWR_ELEM_00011
**Title:** RPStatechart is a subclass of RPUnit registered under meta class "Statechart"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain and registry entry for `RPStatechart`.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPStatechart`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPStatechart, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["Statechart"] is RPStatechart`.
**Expected Result:**
Both assertions hold.
**Verification Criteria:**
Pass if the subclass and registry assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00024: RPStatechart Methods Delegate and Unwrap State

**ID:** UTS_ELEM_00024
**Traces-To:** SWR_ELEM_00011
**Title:** RPStatechart addNewNodeByType/createGraphics/closeDiagram/deleteState behave per spec
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `addNewNodeByType(meta_type, x, y, w, h)` forwards all five args and returns a wrapped node; `createGraphics()` and `closeDiagram()` delegate to COM; `deleteState(state)` unwraps `state._com` and forwards it.
**Pre-conditions:**
- A fake statechart COM object via `make_fake_element("Statechart")` with `addNewNodeByType.return_value = make_fake_element("State")`.
- A fake state `fake_state` and `state = RPModelElement(fake_state)`.
**Test Steps:**
1. Construct `sc = RPStatechart(fake)`.
2. Call `sc.addNewNodeByType("State", 1, 2, 3, 4)` and assert the result is a wrapped element; assert `fake.addNewNodeByType.call_args == call("State", 1, 2, 3, 4)`.
3. Call `sc.createGraphics()` and assert `fake.createGraphics` was called once.
4. Call `sc.closeDiagram()` and assert `fake.closeDiagram` was called once.
5. Call `sc.deleteState(state)` and assert `fake.deleteState.call_args == call(fake_state)`.
**Expected Result:**
`addNewNodeByType` wraps its result and forwards all five args; `createGraphics`/`closeDiagram` delegate; `deleteState` forwards the unwrapped `_com`.
**Verification Criteria:**
Pass if all type/call-args assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00025: RPUseCase Extends RPClassifier and Registers for "UseCase"

**ID:** UTS_ELEM_00025
**Traces-To:** SWR_ELEM_00012
**Title:** RPUseCase is a subclass of RPClassifier registered under meta class "UseCase"
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies the inheritance chain `RPUseCase -> RPClassifier -> RPUnit` and the `"UseCase"` registry entry.
**Pre-conditions:**
- `rhapsody_cli.models.elements` imported.
**Test Steps:**
1. Import `RPUseCase`, `RPClassifier`, `RPUnit`, and `_WRAPPER_REGISTRY`.
2. Assert `issubclass(RPUseCase, RPClassifier)` and `issubclass(RPUseCase, RPUnit)`.
3. Assert `_WRAPPER_REGISTRY["UseCase"] is RPUseCase`.
**Expected Result:**
Both subclass relationships hold and the registry maps `"UseCase"` to `RPUseCase`.
**Verification Criteria:**
Pass if all three assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00026: RPUseCase Methods Return Collections and Forward Strings

**ID:** UTS_ELEM_00026
**Traces-To:** SWR_ELEM_00012
**Title:** RPUseCase addExtensionPoint/getExtensionPoints/getEntryPoints/getDescribingDiagrams behave per spec
**Type:** Unit
**Priority:** Medium
**Description:**
Verifies that `addExtensionPoint(entry_point)` forwards the string arg; `getExtensionPoints()`, `getEntryPoints()`, and `getDescribingDiagrams()` each return an `RPCollection`.
**Pre-conditions:**
- A fake use case COM object via `make_fake_element("UseCase")` configured so that `getExtensionPoints`, `getEntryPoints`, and `getDescribingDiagrams` each return `make_fake_collection([make_fake_element("ExtensionPoint")])`.
**Test Steps:**
1. Construct `uc = RPUseCase(fake)`.
2. Call `uc.addExtensionPoint("EP1")` and assert `fake.addExtensionPoint.call_args == call("EP1")`.
3. Call `uc.getExtensionPoints()` and assert it is an `RPCollection` with `len == 1`.
4. Call `uc.getEntryPoints()` and assert it is an `RPCollection`.
5. Call `uc.getDescribingDiagrams()` and assert it is an `RPCollection`.
**Expected Result:**
`addExtensionPoint` forwards the string; all three getters return `RPCollection` instances.
**Verification Criteria:**
Pass if all call-args and type/length assertions hold.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00027: Importing elements Package Registers All Core Wrappers

**ID:** UTS_ELEM_00027
**Traces-To:** SWR_ELEM_00013
**Title:** Importing rhapsody_cli.models.elements populates the registry for all 13 element types
**Type:** Unit
**Priority:** High
**Description:**
Verifies that after importing the `rhapsody_cli.models.elements` package, `_WRAPPER_REGISTRY` contains entries for all 13 core element types: `Project`, `Package`, `Class`, `Actor`, `Operation`, `Attribute`, `ActivityDiagram` (RPDiagram), `Instance`, `Requirement`, `Statechart`, `UseCase`. (Note: `Classifier` is a shared base and is not itself registered.) Each entry maps to the expected wrapper class.
**Pre-conditions:**
- A fresh interpreter or a forced re-import of `rhapsody_cli.models.elements`.
- Access to `_WRAPPER_REGISTRY`.
**Test Steps:**
1. Import `rhapsody_cli.models.elements`.
2. Read `_WRAPPER_REGISTRY` from `rhapsody_cli.models._core`.
3. Assert the registry contains the keys `"Project"`, `"Package"`, `"Class"`, `"Actor"`, `"Operation"`, `"Attribute"`, `"ActivityDiagram"`, `"Instance"`, `"Requirement"`, `"Statechart"`, `"UseCase"`.
4. Assert each key maps to the expected wrapper class (e.g., `"Project" -> RPProject`, `"Class" -> RPClass`, `"ActivityDiagram" -> RPDiagram`, `"UseCase" -> RPUseCase`).
**Expected Result:**
After import, all core element meta classes are registered to their wrapper classes; no `KeyError` occurs when looking them up.
**Verification Criteria:**
Pass if every expected key is present and maps to the expected wrapper class.
**Last Changed:** 2026-07-07

---

## UTS_ELEM_00028: Element Module Registration is Idempotent on Re-import

**ID:** UTS_ELEM_00028
**Traces-To:** SWR_ELEM_00013
**Title:** Re-importing an element module does not corrupt the registry
**Type:** Unit
**Priority:** Low
**Description:**
Verifies that calling `register_wrapper` again (e.g., via `importlib.reload`) for the same meta class still maps to the same wrapper class without raising or duplicating keys.
**Pre-conditions:**
- `rhapsody_cli.models.elements` already imported.
- Access to `importlib.reload` and `_WRAPPER_REGISTRY`.
**Test Steps:**
1. Snapshot `_WRAPPER_REGISTRY["Class"]`.
2. Call `importlib.reload(rhapsody_cli.models.elements.classifiers)`.
3. Assert `_WRAPPER_REGISTRY["Class"] is RPClass` still holds.
4. Assert the number of keys containing `"Class"` is exactly one.
**Expected Result:**
The registry entry for `"Class"` still maps to `RPClass`; no duplicate keys appear.
**Verification Criteria:**
Pass if the registry entry is unchanged and there is exactly one `"Class"` key.
**Last Changed:** 2026-07-07

---
