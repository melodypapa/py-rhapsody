# Rhapsody Java API Reference (for Python Wrapper Development)

> **Purpose**: This document records the mapping between the IBM Rhapsody Java API
> (`com.telelogic.rhapsody.core`) and the Python wrapper in `rhapsody_cli`.
> Read this before implementing or testing new model wrappers.

---

## 1. Architecture Overview

The Rhapsody COM API mirrors the Java API `com.telelogic.rhapsody.core.*`.
Every `IRP*` Java interface becomes an `RP*` Python class.

| Layer | Java | Python |
|-------|------|--------|
| Interface prefix | `IRP*` | `RP*` |
| Namespace | `com.telelogic.rhapsody.core` | `rhapsody_cli.models.elements.*` |
| Method style | `camelCase()` | `snake_case()` |
| Collections | `IRPCollection` | `RPCollection` |
| Application | `IRPApplication` | `RhapsodyApplication` |

---

## 2. Interface → Class Mapping

All 97 registered wrappers (see `docs/java_api.md` below for full list).

### 2.1 Base Hierarchy

```
IRPModelElement  ──> RPModelElement       (models/core.py)
  └── IRPUnit    ──> RPUnit               (models/core.py)
       ├── IRPClassifier   ──> RPClassifier   (classifiers/model_classifier.py)
       │    ├── IRPClass                ──> RPClass
       │    ├── IRActor                 ──> RPActor
       │    ├── IRPUseCase              ──> RPUseCase
       │    ├── IRPStatechart           ──> RPStatechart
       │    ├── IRPInterfaceItem        ──> RPInterfaceItem
       │    │    └── IRPOperation       ──> RPOperation
       │    ├── IRPException            ──> RPException
       │    └── IRPStereotype           ──> RPStereotype
       ├── IRPPackage        ──> RPPackage     (containment/model_package.py)
       │    ├── IRPProject   ──> RPProject     (containment/model_project.py)
       │    └── IRPProfile   ──> RPProfile     (containment/model_profile.py)
       ├── IRPComponent      ──> RPComponent   (containment/model_component.py)
       ├── IRPCollaboration  ──> RPCollaboration
       ├── IRPDiagram        ──> RPDiagram
       ├── IRPRelation       ──> RPRelation
       │    └── IRPInstance  ──> RPInstance
       │         ├── IRPAssociationRole  ──> RPAssociationRole
       │         └── IRPPort             ──> RPPort
       ├── IRPStateVertex    ──> RPStateVertex
       │    └── IRPState     ──> RPState
       ├── IRPVariable       ──> RPVariable
       │    ├── IRPAttribute ──> RPAttribute
       │    ├── IRPTag       ──> RPTag
       │    └── IRPArgument  ──> RPArgument
       ├── IRPInstanceSlot / IRPValueSpecification etc.
       ├── IRPAnnotation     ──> RPAnnotation
       │    └── IRPRequirement ──> RPRequirement
       ├── IRPTemplateParameter / IRPTemplateInstantiation
       └── IRPGraphElement / IRPGraphEdge / IRPGraphNode etc.
```

### 2.2 Registration Pattern

Each wrapper class registers itself at module level:

```python
AbstractRPModelElement.register_wrapper("MetaClass", RPMyClass)
```

The string `"MetaClass"` must match what `com_obj.getMetaClass()` returns.

---

## 3. Method Naming Convention

Java API methods map to Python as follows:

| Java | Python | Example |
|------|--------|---------|
| `getX()` | `get_x()` | `getName()` → `get_name()` |
| `setX(val)` | `set_x(val)` | `setName("foo")` → `set_name("foo")` |
| `isX()` | `get_is_x()` | `isModified()` → `get_is_modified()` |
| `addX(...)` | `add_x(...)` | `addClass(...)` → `add_class(...)` |
| `findX(...)` | `find_x(...)` | `findClass(...)` → `find_class(...)` |
| `deleteX(...)` | `delete_x(...)` | `deleteClass(...)` → `delete_class(...)` |
| Boolean returns: Java `int` (0/1) → Python `int` | `get_is_abstract()` returns `int` |

### 3.1 Internal COM Call Patterns

There are **three** patterns for calling COM, chosen by method signature:

**Pattern A — No-arg getters** (most common):
```python
def get_name(self) -> str:
    return self._get_method_or_property(self._com, "getName", "name")
```

**Pattern B — Single-arg setters**:
```python
def set_name(self, value: str) -> None:
    self._set_method_or_property(self._com, "setName", "name", value)
```

**Pattern C — Parameterized methods / multi-arg methods**:
```python
def add_class(self, name: str) -> "RPClass":
    result = self.call_com(lambda: self._com.addClass(name))
    return AbstractRPModelElement.wrap(result)
```

**Pattern D — Methods returning collections**:
```python
def get_classes(self) -> RPCollection:
    return RPCollection(self.call_com(lambda: self._com.getClasses()))
```

**Pattern E — Unwrapping arguments then wrapping results**:
```python
def add_dependency_to(self, target: "RPModelElement") -> "RPDependency":
    result = self.call_com(lambda: self._com.addDependencyTo(target._com))
    return AbstractRPModelElement.wrap(result)
```

---

## 4. Testing Patterns

### 4.1 Fake COM Objects

Use `make_fake_element(meta_class, **method_returns)` from `tests/unit/models/fakes.py`:

```python
from tests.unit.models.fakes import make_fake_element

# Fake that returns "Widget" from getName()
fake = make_fake_element("Class", getName="Widget")

# Fake with multiple methods
fake = make_fake_element("Class",
    getName="MyClass",
    getGUID="abc-123",
    getIsAbstract=1,
)
```

**Key rule**: The keyword argument name is the **Java camelCase method name**, not the Python snake_case name.

### 4.2 Fake Collections

```python
from tests.unit.models.fakes import make_fake_collection

items = [make_fake_element("Class"), make_fake_element("Class")]
coll = make_fake_collection(items)
# coll.getCount() → len(items)
# coll.getItem(1) → items[0]  (1-based!)
```

### 4.3 Property Fallback Testing

Some COM Prog IDs expose properties instead of methods:

```python
from unittest.mock import MagicMock

fake = MagicMock(spec=["name"])
fake.name = "PropertyStyleName"
element = RPModelElement(fake)
assert element.get_name() == "PropertyStyleName"
```

### 4.4 COM Error Simulation

```python
from tests.unit.models.fakes import make_com_error

fake = make_fake_element("Class", getName="ok")
fake.getName.side_effect = make_com_error("boom")

with pytest.raises(RhapsodyRuntimeException, match="boom"):
    element.get_name()
```

### 4.5 Assertion Patterns

```python
# Assert COM method was called
fake.setName.assert_called_once_with("NewName")

# Assert COM method was called with unwrapped element
fake.addDependencyTo.assert_called_once_with(target._com)

# Assert result is wrapped correctly
result = element.add_class("Foo")
assert isinstance(result, RPClass)

# Assert returned collection contains wrapped elements
coll = element.get_classes()
assert all(isinstance(item, RPModelElement) for item in coll)
```

### 4.6 Complete Test Example

```python
def test_my_class_get_name(self):
    fake = make_fake_element("Class", getName="Widget")
    element = RPModelElement(fake)
    assert element.get_name() == "Widget"
    fake.getName.assert_called_once_with()

def test_my_class_set_name(self):
    fake = make_fake_element("Class")
    element = RPModelElement(fake)
    element.set_name("NewName")
    fake.setName.assert_called_once_with("NewName")

def test_my_class_add_superclass(self):
    parent_fake = make_fake_element("Class")
    fake = make_fake_element("Class", addSuperclass=parent_fake)
    element = RPClass(fake)
    parent = RPClass(parent_fake)
    result = element.add_superclass(parent)
    fake.addSuperclass.assert_called_once_with(parent_fake)
    assert isinstance(result, RPClass)
```

---

## 5. Complete Java API Method Reference

### 5.1 IRPModelElement (in `RPModelElement`)

**Getters** (all use `_get_method_or_property` pattern):

| Java Method | Python Method | Returns |
|-------------|---------------|---------|
| `getName()` | `get_name()` | `str` |
| `getMetaClass()` | `get_meta_class()` | `str` |
| `getGUID()` | `get_guid()` | `str` |
| `getDisplayName()` | `get_display_name()` | `str` |
| `getDisplayNameRTF()` | `get_display_name_rtf()` | `str` |
| `getDescription()` | `get_description()` | `str` |
| `getDescriptionHTML()` | `get_description_html()` | `str` |
| `getDescriptionPlainText()` | `get_description_plain_text()` | `str` |
| `getDescriptionRTF()` | `get_description_rtf()` | `str` |
| `getFullPathName()` | `get_full_path_name()` | `str` |
| `getFullPathNameIn(IRPPackage)` | `get_full_path_name_in(pkg)` | `str` |
| `getOwner()` | `get_owner()` | `RPModelElement` |
| `getProject()` | `get_project()` | `RPProject` |
| `getNestedElements()` | `get_nested_elements()` | `RPCollection` |
| `getNestedElementsRecursive()` | `get_nested_elements_recursive()` | `RPCollection` |
| `getNestedElementsByMetaClass(str)` | `get_nested_elements_by_meta_class(mc)` | `RPCollection` |
| `hasNestedElements()` | `has_nested_elements()` | `int` |
| `getAllTags()` | `get_all_tags()` | `RPCollection` |
| `getLocalTags()` | `get_local_tags()` | `RPCollection` |
| `getAnnotations()` | `get_annotations()` | `RPCollection` |
| `getAssociationClasses()` | `get_association_classes()` | `RPCollection` |
| `getConstraints()` | `get_constraints()` | `RPCollection` |
| `getConstraintsByHim()` | `get_constraints_by_him()` | `RPCollection` |
| `getControlledFiles()` | `get_controlled_files()` | `RPCollection` |
| `getDependencies()` | `get_dependencies()` | `RPCollection` |
| `getOwnedDependencies()` | `get_owned_dependencies()` | `RPCollection` |
| `getHyperLinks()` | `get_hyper_links()` | `RPCollection` |
| `getStereotypes()` | `get_stereotypes()` | `RPCollection` |
| `getRedefines()` | `get_redefines()` | `RPCollection` |
| `getReferences()` | `get_references()` | `RPCollection` |
| `getRemoteDependencies()` | `get_remote_dependencies()` | `RPCollection` |
| `getOverriddenProperties()` | `get_overridden_properties()` | `RPCollection` |
| `getOverriddenPropertiesByPattern(str)` | `get_overridden_properties_by_pattern(p)` | `RPCollection` |
| `getTemplateParameters()` | `get_template_parameters()` | `RPCollection` |
| `getMainDiagram()` | `get_main_diagram()` | `RPDiagram` |
| `getIconFileName()` | `get_icon_file_name()` | `str` |
| `getOverlayIconFileName()` | `get_overlay_icon_file_name()` | `str` |
| `getInterfaceName()` | `get_interface_name()` | `str` |
| `getIsExternal()` | `get_is_external()` | `int` |
| `getIsUnresolved()` | `get_is_unresolved()` | `int` |
| `getIsShowDisplayName()` | `get_is_show_display_name()` | `int` |
| `getDecorationStyle()` | `get_decoration_style()` | `int` |
| `getErrorMessage()` | `get_error_message()` | `str` |
| `getToolTipHTML()` | `get_tool_tip_html()` | `str` |
| `getNewTermStereotype()` | `get_new_term_stereotype()` | `RPStereotype` |
| `getOfTemplate()` | `get_of_template()` | `RPTemplateInstantiation` |
| `getSaveUnit()` | `get_save_unit()` | `RPUnit` |
| `getTi()` | `get_ti()` | `RPTemplateInstantiation` |
| `getUserDefinedMetaClass()` | `get_user_defined_meta_class()` | `str` |
| `getRmmUrl()` | `get_rmm_url()` | `str` |
| `getRequirementTraceabilityHandle()` | `get_requirement_traceability_handle()` | `str` |
| `getBinaryID()` | `get_binary_id()` | `str` |
| `getRemoteURI()` | `get_remote_uri()` | `str` |
| `getTag(str)` | `get_tag(name)` | `RPTag` |
| `getPropertyValue(str)` | `get_property_value(name)` | `str` |
| `getPropertyValueExplicit(str)` | `get_property_value_explicit(name)` | `str` |
| `getPropertyValueConditional(str)` | `get_property_value_conditional(name)` | `str` |
| `getPropertyValueConditionalExplicit(str)` | `get_property_value_conditional_explicit(name)` | `str` |

**Setters** (all use `_set_method_or_property` pattern):

| Java Method | Python Method |
|-------------|---------------|
| `setName(str)` | `set_name(value)` |
| `setGUID(str)` | `set_guid(value)` |
| `setDescription(str)` | `set_description(value)` |
| `setDescriptionHTML(str)` | `set_description_html(value)` |
| `setDescriptionRTF(str)` | `set_description_rtf(value)` |
| `setDisplayName(str)` | `set_display_name(value)` |
| `setDisplayNameRTF(str)` | `set_display_name_rtf(value)` |
| `setDecorationStyle(int)` | `set_decoration_style(value)` |
| `setIsShowDisplayName(int)` | `set_is_show_display_name(value)` |
| `setMainDiagram(IRPDiagram)` | `set_main_diagram(value)` |
| `setOfTemplate(IRPTemplateInstantiation)` | `set_of_template(value)` |
| `setOwner(IRPModelElement)` | `set_owner(value)` |
| `setPropertyValue(str, str)` | `set_property_value(name, value)` |
| `setRequirementTraceabilityHandle(str)` | `set_requirement_traceability_handle(value)` |
| `setTi(IRPTemplateInstantiation)` | `set_ti(value)` |

**Action methods** (use `call_com` directly):

| Java Method | Python Method |
|-------------|---------------|
| `deleteFromProject()` | `delete_from_project()` |
| `addNewAggr(IRPModelElement)` | `add_new_aggr(element)` |
| `addAssociation(IRPModelElement)` | `add_association(element)` |
| `addDependency(IRPModelElement)` | `add_dependency(element)` |
| `addDependencyTo(IRPModelElement)` | `add_dependency_to(target)` |
| `addDependencyBetween(IRPModelElement, IRPModelElement)` | `add_dependency_between(e1, e2)` |
| `addLinkToElement(IRPModelElement)` | `add_link_to_element(target)` |
| `addRemoteDependencyTo(IRPModelElement)` | `add_remote_dependency_to(target)` |
| `addStereotype(RPStereotype)` | `add_stereotype(stereotype)` |
| `addSpecificStereotype(IRPStereotype, str)` | `add_specific_stereotype(stereotype, mc)` |
| `removeStereotype(IRPStereotype)` | `remove_stereotype(stereotype)` |
| `addProperty(IRPGraphicalProperty)` | `add_property(prop)` |
| `removeProperty(IRPGraphicalProperty)` | `remove_property(prop)` |
| `addRedefines(IRPModelElement)` | `add_redefines(element)` |
| `removeRedefines(IRPModelElement)` | `remove_redefines(element)` |
| `deleteDependency(IRPDependency)` | `delete_dependency(dep)` |
| `changeTo(str)` | `change_to(meta_class)` |
| `clone()` | `clone()` |
| `becomeTemplateInstantiationOf(IRPTemplateParameter)` | `become_template_instantiation_of(param)` |
| `synchronizeTemplateInstantiation()` | `synchronize_template_instantiation()` |
| `setTagValue(str, str)` | `set_tag_value(tag_name, value)` |
| `setTagElementValue(str, IRPModelElement)` | `set_tag_element_value(tag_name, element)` |
| `setTagContextValue(str, str)` | `set_tag_context_value(tag_name, context)` |
| `setDescriptionAndHyperlinks(str)` | `set_description_and_hyperlinks(value)` |
| `openFeaturesDialog()` | `open_features_dialog()` |
| `highLightElement()` | `high_light_element()` |
| `locateInBrowser()` | `locate_in_browser()` |
| `findNestedElement(str)` | `find_nested_element(name)` |
| `findNestedElementRecursive(str)` | `find_nested_element_recursive(name)` |
| `findElementsByFullName(str)` | `find_elements_by_full_name(name)` |
| `getIsOfMetaClass(str)` | `get_is_of_meta_class(mc)` |
| `setString(int, str)` | `set_string(index, value)` |
| `setInteger(int, int)` | `set_integer(index, value)` |
| `setModelElement(int, IRPModelElement)` | `set_model_element(index, element)` |
| `addItem(IRPModelElement)` | `add_item(element)` |
| `addGraphicalItem(IRPGraphicalProperty)` | `add_graphical_item(item)` |
| `setLanguage(int)` | `set_language(lang)` |
| `setSize(int)` | `set_size(size)` |

### 5.2 IRPUnit (in `RPUnit`)

| Java Method | Python Method |
|-------------|---------------|
| `save()` | `save()` |
| `load()` | `load()` |
| `unload()` | `unload()` |
| `getFilename()` / `setFilename(str)` | `get_filename()` / `set_filename(value)` |
| `isReadOnly()` / `setReadOnly(int)` | `is_read_only()` / `set_read_only(value)` |
| `getLanguage()` / `setLanguage(int)` | `get_language()` / `set_language(value)` |
| `getCMHeader()` / `setCMHeader(str)` | `get_cm_header()` / `set_cm_header(value)` |
| `getCMState()` | `get_cm_state()` |
| `getCurrentDirectory()` | `get_current_directory()` |
| `getAddToModelMode()` | `get_add_to_model_mode()` |
| `getIncludeInNextLoad()` / `setIncludeInNextLoad(int)` | `get_include_in_next_load()` / `set_include_in_next_load(value)` |
| `getIsStub()` | `get_is_stub()` |
| `getLastModifiedTime()` | `get_last_modified_time()` |
| `getNestedSaveUnits()` | `get_nested_save_units()` |
| `getNestedSaveUnitsCount()` | `get_nested_save_units_count()` |
| `getStructureDiagrams()` | `get_structure_diagrams()` |
| `getUnitPath()` / `setUnitPath(str)` | `get_unit_path()` / `set_unit_path(value)` |
| `isReferenceUnit()` | `is_reference_unit()` |
| `isSeparateSaveUnit()` / `setSeparateSaveUnit(int)` | `is_separate_save_unit()` / `set_separate_save_unit(value)` |
| `copyToAnotherProject(IRPProject, str)` | `copy_to_another_project(project, name)` |
| `referenceToAnotherProject(IRPProject, str)` | `reference_to_another_project(project, name)` |
| `moveToAnotherProjectLeaveAReference(IRPProject, str)` | `move_to_another_project_leave_a_reference(project, name)` |

### 5.3 IRPClassifier (in `RPClassifier`)

| Java Method | Python Method |
|-------------|---------------|
| `addAttribute(str)` | `add_attribute(name)` → `RPAttribute` |
| `addOperation(str)` | `add_operation(name)` → `RPOperation` |
| `addGeneralization()` | `add_generalization()` → `RPGeneralization` |
| `addStatechart(str)` | `add_statechart(name)` → `RPStatechart` |
| `addActivityDiagram(str)` | `add_activity_diagram(name)` → `RPFlowchart` |
| `addFlowItems(str)` | `add_flow_items(name)` → `RPFlowItem` |
| `addFlows(str)` | `add_flows(name)` → `RPFlow` |
| `addRelation(IRPClassifier)` | `add_relation(classifier)` → `RPRelation` |
| `addRelationTo(IRPClassifier, str)` | `add_relation_to(classifier, name)` → `RPRelation` |
| `addUnidirectionalRelation(IRPClassifier)` | `add_unidirectional_relation(classifier)` → `RPRelation` |
| `addUnidirectionalRelationTo(IRPClassifier, str)` | `add_unidirectional_relation_to(classifier, name)` → `RPRelation` |
| `addNewAggr(IRPModelElement, str)` | `add_new_aggr(element, name)` → `RPPort` |
| `deleteAttribute(IRPAttribute)` | `delete_attribute(attr)` |
| `deleteOperation(IRPOperation)` | `delete_operation(op)` |
| `deleteGeneralization(IRPGeneralization)` | `delete_generalization(gen)` |
| `deleteFlowItems(IRPFlowItem)` | `delete_flow_items(item)` |
| `deleteFlows(IRPFlow)` | `delete_flows(flow)` |
| `deleteRelation(IRPRelation)` | `delete_relation(relation)` |
| `findAttribute(str)` | `find_attribute(name)` → `RPAttribute` |
| `findBaseClassifier()` | `find_base_classifier()` → `RPClassifier` |
| `findDerivedClassifier()` | `find_derived_classifier()` → `RPClassifier` |
| `findGeneralization(IRPClassifier)` | `find_generalization(classifier)` → `RPGeneralization` |
| `findInterfaceItem(IRPInterfaceItem)` | `find_interface_item(item)` → `RPInterfaceItem` |
| `findNestedClassifier(str)` | `find_nested_classifier(name)` → `RPClassifier` |
| `findNestedClassifierRecursive(str)` | `find_nested_classifier_recursive(name)` → `RPClassifier` |
| `findRelation(IRPClassifier)` | `find_relation(classifier)` → `RPRelation` |
| `findTrigger(str)` | `find_trigger(name)` → `RPTrigger` |

### 5.4 IRPClass (in `RPClass`)

| Java Method | Python Method |
|-------------|---------------|
| `addSuperclass(IRPClass)` | `add_superclass(superclass)` → `RPGeneralization` |
| `addConstructor()` | `add_constructor()` → `RPOperation` |
| `addDestructor()` | `add_destructor()` → `RPOperation` |
| `addClass(str)` | `add_class(name)` → `RPClass` |
| `addEventReception(str)` | `add_event_reception(name)` → `RPOperation` |
| `addEventReceptionWithEvent(str, str, str)` | `add_event_reception_with_event(name, event, pkg)` → `RPOperation` |
| `addLink(str, IRPModelElement, int)` | `add_link(name, target, style)` → `RPRelation` |
| `addLinkToPartViaPort(str, IRPModelElement, IRPPort, int)` | `add_link_to_part_via_port(name, target, port, style)` → `RPRelation` |
| `addReception(str)` | `add_reception(name)` → `RPOperation` |
| `addTriggeredOperation(str, str)` | `add_triggered_operation(name, trigger)` → `RPOperation` |
| `addType(str)` | `add_type(name)` → `RPType` |
| `deleteClass(IRPClass)` | `delete_class(cls)` |
| `deleteConstructor(IRPOperation)` | `delete_constructor(op)` |
| `deleteDestructor(IRPOperation)` | `delete_destructor(op)` |
| `deleteEventReception(IRPOperation)` | `delete_event_reception(op)` |
| `deleteReception(IRPOperation)` | `delete_reception(op)` |
| `deleteSuperclass(IRPClass)` | `delete_superclass(superclass)` |
| `deleteType(IRPType)` | `delete_type(tp)` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |

### 5.5 IRPPackage (in `RPPackage`)

| Java Method | Python Method |
|-------------|---------------|
| `addClass(str)` | `add_class(name)` → `RPClass` |
| `addNestedPackage(str)` | `add_nested_package(name)` → `RPPackage` |
| `addActor(str)` | `add_actor(name)` → `RPActor` |
| `addUseCase(str)` | `add_use_case(name)` → `RPUseCase` |
| `addException(str)` | `add_exception(name)` → `RPException` |
| `addInterfaceItem(str, str)` | `add_interface_item(name, mc)` → `RPInterfaceItem` |
| `addEvent(str)` | `add_event(name)` → `RPEvent` |
| `addStatechart(str)` | `add_statechart(name)` → `RPStatechart` |
| `addActivityDiagram(str)` | `add_activity_diagram(name)` → `RPFlowchart` |
| `addSequenceDiagram(str)` | `add_sequence_diagram(name)` → `RPSequenceDiagram` |
| `addCollaborationDiagram(str)` | `add_collaboration_diagram(name)` → `RPCollaborationDiagram` |
| `addComponentDiagram(str)` | `add_component_diagram(name)` → `RPComponentDiagram` |
| `addDeploymentDiagram(str)` | `add_deployment_diagram(name)` → `RPDeploymentDiagram` |
| `addObjectModelDiagram(str)` | `add_object_model_diagram(name)` → `RPObjectModelDiagram` |
| `addPanelDiagram(str)` | `add_panel_diagram(name)` → `RPPanelDiagram` |
| `addTimingDiagram(str)` | `add_timing_diagram(name)` → `RPTimingDiagram` |
| `addUseCaseDiagram(str)` | `add_use_case_diagram(name)` → `RPUseCaseDiagram` |
| `addAssociation(IRPModelElement, IRPModelElement)` | `add_association(e1, e2)` → `RPRelation` |
| `addFlowItems(str)` | `add_flow_items(name)` → `RPFlowItem` |
| `addFlows(str)` | `add_flows(name)` → `RPFlow` |
| `addType(str)` | `add_type(name)` → `RPType` |
| `addGlobalFunction(str)` | `add_global_function(name)` → `RPOperation` |
| `addGlobalObject(str)` | `add_global_object(name)` → `RPClass` |
| `addGlobalVariable(str)` | `add_global_variable(name)` → `RPAttribute` |
| `addNode(str)` | `add_node(name)` → `RPNode` |
| `addModule(str)` | `add_module(name)` → `RPModule` |
| `addImplicitObject(str)` | `add_implicit_object(name)` → `RPClass` |
| `addLink(str, IRPModelElement, IRPModelElement, int)` | `add_link(name, e1, e2, style)` → `RPRelation` |
| `addLinkBetweenSYSMLPorts(str, IRPPort, IRPPort, int)` | `add_link_between_sysml_ports(name, p1, p2, style)` → `RPRelation` |
| `addInstanceSpecification(str, IRPClassifier)` | `add_instance_specification(name, classifier)` → `RPInstanceSpecification` |
| `findClass(str)` | `find_class(name)` → `RPClass` |
| `findActor(str)` | `find_actor(name)` → `RPActor` |
| `findUseCase(str)` | `find_use_case(name)` → `RPUseCase` |
| `findNestedPackage(str)` | `find_nested_package(name)` → `RPPackage` |
| `findNode(str)` | `find_node(name)` → `RPNode` |
| `findType(str)` | `find_type(name)` → `RPType` |
| `findEvent(str)` | `find_event(name)` → `RPEvent` |
| `findGlobalFunction(str)` | `find_global_function(name)` → `RPOperation` |
| `findGlobalObject(str)` | `find_global_object(name)` → `RPClass` |
| `findGlobalVariable(str)` | `find_global_variable(name)` → `RPAttribute` |
| `findAllByName(str, int)` | `find_all_by_name(name, kind)` → `RPCollection` |
| `findUsage(str, int)` | `find_usage(name, kind)` → `RPCollection` |
| `deleteClass(IRPClass)` | `delete_class(cls)` |
| `deletePackage(IRPPackage)` | `delete_package(pkg)` |
| `deleteActor(IRPActor)` | `delete_actor(actor)` |
| `deleteUseCase(IRPUseCase)` | `delete_use_case(uc)` |
| `deleteNode(IRPNode)` | `delete_node(node)` |
| `deleteType(IRPType)` | `delete_type(tp)` |
| `deleteEvent(IRPEvent)` | `delete_event(event)` |
| `deleteGlobalFunction(IRPOperation)` | `delete_global_function(op)` |
| `deleteGlobalObject(IRPClass)` | `delete_global_object(cls)` |
| `deleteGlobalVariable(IRPAttribute)` | `delete_global_variable(attr)` |
| `deleteActivityDiagram(IRPActivityDiagram)` | `delete_activity_diagram(diag)` |
| `deleteSequenceDiagram(IRPSequenceDiagram)` | `delete_sequence_diagram(diag)` |
| `deleteCollaborationDiagram(IRP... )` | `delete_collaboration_diagram(diag)` |
| `deleteComponentDiagram(IRP... )` | `delete_component_diagram(diag)` |
| `deleteDeploymentDiagram(IRP... )` | `delete_deployment_diagram(diag)` |
| `deleteObjectModelDiagram(IRP... )` | `delete_object_model_diagram(diag)` |
| `deletePanelDiagram(IRPPanelDiagram)` | `delete_panel_diagram(diag)` |
| `deleteTimingDiagram(IRPTimingDiagram)` | `delete_timing_diagram(diag)` |
| `deleteUseCaseDiagram(IRPUseCaseDiagram)` | `delete_use_case_diagram(diag)` |
| `deleteFlowItems(IRPFlowItem)` | `delete_flow_items(item)` |
| `deleteFlows(IRPFlow)` | `delete_flows(flow)` |
| `loginToRemoteArtifactServer(str, str, str)` | `login_to_remote_artifact_server(url, user, pwd)` |
| `populateRemoteRequirements(str)` | `populate_remote_requirements(url)` |
| `reCalculateEventsBaseId()` | `recalculate_events_base_id()` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |
| `updateContainedMatricesOnServer()` | `update_contained_matrices_on_server()` |
| `updateContainedTablesOnServer()` | `update_contained_tables_on_server()` |

### 5.6 IRPProject (in `RPProject`)

Inherits all `IRPPackage` methods plus:

| Java Method | Python Method |
|-------------|---------------|
| `addPackage(str)` | `add_package(name)` → `RPPackage` |
| `addComponent(str)` | `add_component(name)` → `RPComponent` |
| `addConfiguration(str)` | `add_configuration(name)` → `RPConfiguration` |
| `addCollaboration(str)` | `add_collaboration(name)` → `RPCollaboration` |
| `addNode(str)` | `add_node(name)` → `RPNode` |
| `addProfile(str)` | `add_profile(name)` → `RPProfile` |
| `close()` | `close()` |
| `saveAs(str)` | `save_as(path)` |
| `saveAsPrevVersion(str)` | `save_as_prev_version(path)` |
| `becomeActiveProject()` | `become_active_project()` |
| `findByName(str)` | `find_by_name(name)` → `RPModelElement` |
| `findByMetaClass(str)` | `find_by_meta_class(mc)` → `RPCollection` |
| `findElementByGUID(str)` | `find_element_by_guid(guid)` → `RPModelElement` |
| `findElementByBinaryID(str)` | `find_element_by_binary_id(id)` → `RPModelElement` |
| `findElementByFileName(str)` | `find_element_by_file_name(name)` → `RPModelElement` |
| `findComponent(str)` | `find_component(name)` → `RPComponent` |
| `findConfiguration(str)` | `find_configuration(name)` → `RPConfiguration` |
| `findCollaboration(str)` | `find_collaboration(name)` → `RPCollaboration` |
| `findNode(str)` | `find_node(name)` → `RPNode` |
| `deleteComponent(IRPComponent)` | `delete_component(component)` |
| `deleteConfiguration(IRPConfiguration)` | `delete_configuration(config)` |
| `deleteCollaboration(IRPCollaboration)` | `delete_collaboration(collab)` |
| `deleteNode(IRPNode)` | `delete_node(node)` |
| `gatewayExportToXML(str, int, str)` | `gateway_export_to_xml(path, opts, filter)` |
| `gatewayExportToXML2(str, int, str, int)` | `gateway_export_to_xml2(path, opts, filter, flag)` |
| `generateReport(str, int)` | `generate_report(template, format)` → `str` |
| `isModifiedRecursive()` | `is_modified_recursive()` → `int` |
| `getRequirementsByID(str)` | `get_requirements_by_id(id)` → `RPCollection` |
| `addCustomViewOnBrowser(str, str)` | `add_custom_view_on_browser(name, query)` |
| `addCustomViewOnDiagram(str, str)` | `add_custom_view_on_diagram(name, query)` |
| `removeCustomViewOnBrowser(str)` | `remove_custom_view_on_browser(name)` |
| `removeCustomViewOnDiagram(str)` | `remove_custom_view_on_diagram(name)` |
| `applyBrowserCustomViewsOnDiagrams()` | `apply_browser_custom_views_on_diagrams()` |
| `setActiveComponent(IRPComponent)` | `set_active_component(component)` |
| `setActiveConfiguration(IRPConfiguration)` | `set_active_configuration(config)` |
| `getActiveConfiguration()` | `get_active_configuration()` → `RPConfiguration` |
| `getActiveComponent()` | `get_active_component()` → `RPComponent` |
| `allowAutoSave(int)` | `allow_auto_save(flag)` |
| `allowNonUniqueNames(int)` | `allow_non_unique_names(flag)` |
| `startTransactionOfNoCGInterest()` | `start_transaction_of_no_cg_interest()` |
| `endTransactionOfNoCGInterest()` | `end_transaction_of_no_cg_interest()` |
| `findElementsWithOSLCLink(str)` | `find_elements_with_oslc_link(url)` → `RPCollection` |
| `findByMetaClassMetaclass(str)` | `find_by_meta_class(mc)` |

### 5.7 IRPRelation (in `RPRelation`)

| Java Method | Python Method |
|-------------|---------------|
| `addQualifier(str, IRPClassifier)` | `add_qualifier(name, classifier)` → `RPAttribute` |
| `removeQualifier(IRPAttribute)` | `remove_qualifier(attr)` |
| `makeUnidirect()` | `make_unidirect()` |
| `setInverse(int)` | `set_inverse(value)` |

### 5.8 IRPInstance (in `RPInstance`)

| Java Method | Python Method |
|-------------|---------------|
| `addRelationToTheWhole(IRPClassifier)` | `add_relation_to_the_whole(classifier)` → `RPRelation` |
| `getAttributeValue(str)` | `get_attribute_value(name)` → `str` |
| `setAttributeValue(str, str)` | `set_attribute_value(name, value)` |
| `setExplicit(int)` | `set_explicit(flag)` |
| `setImplicit(int)` | `set_implicit(flag)` |
| `setInitializerArgumentValue(str, str)` | `set_initializer_argument_value(name, value)` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |

### 5.9 IRPPort (in `RPPort`)

| Java Method | Python Method |
|-------------|---------------|
| `getIsBehavioral()` / `setIsBehavioral(int)` | `get_is_behavioral()` / `set_is_behavioral(value)` |
| `getIsReversed()` / `setIsReversed(int)` | `get_is_reversed()` / `set_is_reversed(value)` |
| `getPortContract()` / `setPortContract(IRPClassifier)` | `get_port_contract()` / `set_port_contract(classifier)` |
| `getContract()` / `setContract(IRPClassifier)` | `get_contract()` / `set_contract(classifier)` |
| `getProvidedInterfaces()` | `get_provided_interfaces()` → `RPCollection` |
| `addProvidedInterface(IRPInterfaceItem)` | `add_provided_interface(item)` |
| `removeProvidedInterface(IRPInterfaceItem)` | `remove_provided_interface(item)` |
| `getRequiredInterfaces()` | `get_required_interfaces()` → `RPCollection` |
| `addRequiredInterface(IRPInterfaceItem)` | `add_required_interface(item)` |
| `removeRequiredInterface(IRPInterfaceItem)` | `remove_required_interface(item)` |

### 5.10 IRPOperation (in `RPOperation`)

| Java Method | Python Method |
|-------------|---------------|
| `getIsAbstract()` / `setIsAbstract(int)` | `get_is_abstract()` / `set_is_abstract(value)` |
| `getIsStatic()` / `setIsStatic(int)` | `get_is_static()` / `set_is_static(value)` |
| `getIsVirtual()` / `setIsVirtual(int)` | `get_is_virtual()` / `set_is_virtual(value)` |
| `createAutoFlowChart()` | `create_auto_flow_chart()` → `RPFlowchart` |
| `deleteArgument(IRPArgument)` | `delete_argument(arg)` |
| `deleteFlowchart(IRPFlowchart)` | `delete_flowchart(flowchart)` |
| `setIsConst(int)` | `set_is_const(value)` |
| `setIsFinal(int)` | `set_is_final(value)` |
| `setVisibility(int)` | `set_visibility(value)` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |

### 5.11 IRPStatechart (in `RPStatechart`)

| Java Method | Python Method |
|-------------|---------------|
| `addNewNodeByType(str, int, int, int, int, str)` | `add_new_node_by_type(type, x, y, w, h, name)` → `RPGraphNode` |
| `createGraphics()` | `create_graphics()` → `RPGraphNode` |
| `closeDiagram()` | `close_diagram()` |
| `deleteState(IRPStateVertex)` | `delete_state(state)` |
| `addFreeShapeByType(str, int, int, int, int)` | `add_free_shape_by_type(type, x, y, w, h)` → `RPModelElement` |
| `addImage(str, int, int)` | `add_image(path, x, y)` → `RPModelElement` |
| `addNewEdgeByType(str, IRPGraphNode, IRPGraphNode, str)` | `add_new_edge_by_type(type, src, tgt, name)` → `RPGraphEdge` |
| `addNewEdgeForElement(IRPModelElement, IRPModelElement, str)` | `add_new_edge_for_element(src, tgt, name)` → `RPGraphEdge` |
| `addNewNodeForElement(IRPModelElement, str)` | `add_new_node_for_element(element, name)` → `RPGraphNode` |
| `addTextBox(str, int, int, int, int)` | `add_text_box(text, x, y, w, h)` → `RPModelElement` |
| `openDiagramView()` | `open_diagram_view()` |
| `getPictureAs(str, int)` | `get_picture_as(format, max_size)` → `str` |
| `getPictureAsDividedMetafiles(str, int)` | `get_picture_as_divided_metafiles(format, max_size)` → `RPCollection` |
| `getPicturesWithImageMap(str, int, str)` | `get_pictures_with_image_map(format, max_size, map_type)` → `RPCollection` |
| `overrideInheritance()` | `override_inheritance()` |
| `populateDiagram()` | `populate_diagram()` |
| `setAsMainBehavior(int)` | `set_as_main_behaviour(flag)` |
| `setShowDiagramFrame(int)` | `set_show_diagram_frame(flag)` |
| `unoverrideInheritance()` | `unoverride_inheritance()` |

### 5.12 IRPGeneralization (in `RPGeneralization`)

| Java Method | Python Method |
|-------------|---------------|
| `setBaseClass(IRPClassifier)` | `set_base_class(classifier)` |
| `setDerivedClass(IRPClassifier)` | `set_derived_class(classifier)` |
| `setExtensionPoint(str)` | `set_extension_point(value)` |
| `setIsVirtual(int)` | `set_is_virtual(value)` |
| `setVisibility(int)` | `set_visibility(value)` |

### 5.13 IRPDependency (in `RPDependency`)

| Java Method | Python Method |
|-------------|---------------|
| `setDependent(IRPModelElement)` | `set_dependent(element)` |
| `setDependsOn(IRPModelElement)` | `set_depends_on(element)` |
| `setLinkType(int)` | `set_link_type(value)` |
| `setOwnerWithoutChangingDependent(IRPModelElement)` | `set_owner_without_changing_dependent(element)` |
| `isNeedToMigrate()` | `is_need_to_migrate()` → `int` |

### 5.14 IRPHyperLink (in `RPHyperLink`)

| Java Method | Python Method |
|-------------|---------------|
| `setDisplayOption(int)` | `set_display_option(value)` |
| `setTarget(IRPModelElement)` | `set_target(element)` |
| `setURL(str)` | `set_url(value)` |

### 5.15 IRPInterfaceItem (in `RPInterfaceItem`)

| Java Method | Python Method |
|-------------|---------------|
| `addArgument(str)` | `add_argument(name)` → `RPArgument` |
| `addArgumentBeforePosition(IRPArgument, int)` | `add_argument_before_position(arg, pos)` |
| `setArguments(IRPCollection)` | `set_arguments(collection)` |
| `matchOnSignature(IRPInterfaceItem)` | `match_on_signature(item)` → `int` |

### 5.16 IRPStateVertex / IRPState (in `RPStateVertex`, `RPState`)

| Java Method | Python Method |
|-------------|---------------|
| `addState(str)` | `add_state(name)` → `RPState` |
| `addTransition(IRPStateVertex)` | `add_transition(target)` → `RPTransition` |
| `addInternalTransition()` | `add_internal_transition()` → `RPTransition` |
| `addStaticReaction(IRPTrigger)` | `add_static_reaction(trigger)` → `RPTransition` |
| `addActivityFinal()` | `add_activity_final()` → `RPState` |
| `addConnector(int)` | `add_connector(type)` → `IRPConnector` |
| `addFlow(int)` | `add_flow(type)` → `RPFlow` |
| `addTerminationState()` | `add_termination_state()` → `RPState` |
| `createDefaultTransition()` | `create_default_transition()` |
| `createSubStatechart(str)` | `create_sub_statechart(name)` → `RPStatechart` |
| `deleteTransition(IRPTransition)` | `delete_transition(transition)` |
| `deleteInternalTransition(IRPTransition)` | `delete_internal_transition(transition)` |
| `deleteStaticReaction(IRPTransition)` | `delete_static_reaction(transition)` |
| `deleteConnector(IRPConnector)` | `delete_connector(connector)` |
| `overrideInheritance()` | `override_inheritance()` |
| `unoverrideInheritance()` | `unoverride_inheritance()` |
| `setItsSwimlane(IRPSwimlane)` | `set_its_swimlane(swimlane)` |
| `setParent(IRPStateVertex)` | `set_parent(parent)` |
| `setReferenceToActivity(IRPActivity)` | `set_reference_to_activity(activity)` |
| `setInternalTransition(IRPTransition)` | `set_internal_transition(transition)` |
| `setStaticReaction(IRPTransition)` | `set_static_reaction(transition)` |
| `resetEntryActionInheritance()` | `reset_entry_action_inheritance()` |
| `resetExitActionInheritance()` | `reset_exit_action_inheritance()` |

### 5.17 IRPTransition / IRPTrigger / IRPMessage (in interactions)

| Java Method | Python Method |
|-------------|---------------|
| `addSourceExecutionOccurrence(IRPExecutionOccurrence)` | `add_source_execution_occurrence(occ)` |
| `addTargetExecutionOccurrence(IRPExecutionOccurrence)` | `add_target_execution_occurrence(occ)` |
| `isDefaultTransition()` | `is_default_transition()` → `int` |
| `isOperation(IRPOperation)` | `is_operation(op)` → `int` |
| `isStaticReaction()` | `is_static_reaction()` → `int` |
| `isTimeout()` | `is_timeout()` → `int` |
| `itsCompoundSource()` | `its_compound_source()` → `int` |
| `overrideInheritance()` | `override_inheritance()` |
| `unoverrideInheritance()` | `unoverride_inheritance()` |
| `reroute(IRPStateVertex, int)` | `reroute(target, kind)` |
| `resetLabelInheritance()` | `reset_label_inheritance()` |
| `setItsAction(IRPAction)` | `set_its_action(action)` |
| `setItsGuard(IRPGuard)` | `set_its_guard(guard)` |
| `setItsLabel(str)` | `set_its_label(label)` |
| `setItsTrigger(IRPTrigger)` | `set_its_trigger(trigger)` |
| `setActualParameterList(IRPCollection)` | `set_actual_parameter_list(params)` |

### 5.18 IRPVariable / IRPAttribute / IRPTag / IRPArgument

| Java Method | Python Method |
|-------------|---------------|
| `addElementDefaultValue(IRPModelElement)` | `add_element_default_value(element)` → `RPInstanceValue` |
| `addStringDefaultValue(str)` | `add_string_default_value(value)` → `RPLiteralSpecification` |
| `getDeclaration()` / `setDeclaration(str)` | `get_declaration()` / `set_declaration(value)` |
| `getDefaultValue()` / `setDefaultValue(str)` | `get_default_value()` / `set_default_value(value)` |
| `getType()` / `setType(IRPClassifier)` | `get_type()` / `set_type(classifier)` |
| `setTypeDeclaration(str)` | `set_type_declaration(value)` |
| `getValueSpecifications()` | `get_value_specifications()` → `RPCollection` |
| *Attribute:* `getMultiplicity()` / `setMultiplicity(str)` | `get_multiplicity()` / `set_multiplicity(value)` |
| *Attribute:* `getIsStatic()` / `setIsStatic(int)` | `get_is_static()` / `set_is_static(value)` |
| *Attribute:* `getVisibility()` / `setVisibility(int)` | `get_visibility()` / `set_visibility(value)` |
| *Argument:* `getArgumentDirection()` / `setArgumentDirection(int)` | `get_argument_direction()` / `set_argument_direction(value)` |

### 5.19 IRPDiagram (in `RPDiagram`)

| Java Method | Python Method |
|-------------|---------------|
| `addFreeShapeByType(str, int, int, int, int)` | `add_free_shape_by_type(type, x, y, w, h)` |
| `addImage(str, int, int)` | `add_image(path, x, y)` |
| `addNewEdgeByType(str, IRPGraphNode, IRPGraphNode, str)` | `add_new_edge_by_type(type, src, tgt, name)` |
| `addNewEdgeForElement(IRPModelElement, IRPModelElement, str)` | `add_new_edge_for_element(src, tgt, name)` |
| `addNewNodeByType(str, int, int, int, int, str)` | `add_new_node_by_type(type, x, y, w, h, name)` |
| `addNewNodeForElement(IRPModelElement, str)` | `add_new_node_for_element(element, name)` |
| `addTextBox(str, int, int, int, int)` | `add_text_box(text, x, y, w, h)` |
| `closeDiagram()` | `close_diagram()` |
| `completeRelations(IRPModelElement)` | `complete_relations(element)` |
| `createDiagramView(IRPModelElement)` | `create_diagram_view(element)` |
| `getCorrespondingGraphicElements(IRPModelElement)` | `get_corresponding_graphic_elements(element)` → `RPCollection` |
| `getDiagramViewOf(IRPModelElement)` | `get_diagram_view_of(element)` |
| `getDiagramViews()` | `get_diagram_views()` → `RPCollection` |
| `getElementsInDiagram()` | `get_elements_in_diagram()` → `RPCollection` |
| `getGraphicalElements()` | `get_graphical_elements()` → `RPCollection` |
| `getPicture(str, int, int)` | `get_picture(format, width, height)` → `str` |
| `getPictureAs(str, int)` | `get_picture_as(format, max_size)` → `str` |
| `getPictureAsDividedMetafiles(str, int)` | `get_picture_as_divided_metafiles(format, max_size)` → `RPCollection` |
| `getPictureEx(...)` | `get_picture_ex(...)` → `str` |
| `getPicturesWithImageMap(str, int, str)` | `get_pictures_with_image_map(format, max_size, map_type)` → `RPCollection` |
| `isDiagramView()` | `is_diagram_view()` → `int` |
| `isOpen()` | `is_open()` → `int` |
| `isShowDiagramFrame()` | `is_show_diagram_frame()` → `int` |
| `openDiagram()` | `open_diagram()` |
| `openDiagramView()` | `open_diagram_view()` |
| `populateDiagram()` | `populate_diagram()` |
| `rearrangePorts()` | `rearrange_ports()` |
| `removeGraphElements(IRPCollection)` | `remove_graph_elements(elements)` |
| `setCustomViews(str)` | `set_custom_views(views)` |
| `setShowDiagramFrame(int)` | `set_show_diagram_frame(flag)` |
| `updateViewOnServer()` | `update_view_on_server()` |

### 5.20 IRPComponent (in `RPComponent`)

| Java Method | Python Method |
|-------------|---------------|
| `addConfiguration(str)` | `add_configuration(name)` → `RPConfiguration` |
| `addFile(str)` | `add_file(name)` → `RPFile` |
| `addFolder(str)` | `add_folder(name)` |
| `addNestedComponent(str)` | `add_nested_component(name)` → `RPComponent` |
| `addScopeElement(IRPModelElement)` | `add_scope_element(element)` |
| `addScopeElementWithoutAggregates(IRPModelElement)` | `add_scope_element_without_aggregates(element)` |
| `addToScope()` | `add_to_scope()` |
| `allElementsInScope()` | `all_elements_in_scope()` → `RPCollection` |
| `deleteConfiguration(IRPConfiguration)` | `delete_configuration(config)` |
| `deleteFile(IRPFile)` | `delete_file(file)` |
| `findConfiguration(str)` | `find_configuration(name)` → `RPConfiguration` |
| `getConfigurations()` | `get_configurations()` → `RPCollection` |
| `getFile(str)` | `get_file(name)` → `RPFile` |
| `getFiles()` | `get_files()` → `RPCollection` |
| `getNestedComponents()` | `get_nested_components()` → `RPCollection` |
| `getPanelDiagrams()` | `get_panel_diagrams()` → `RPCollection` |
| `getPossibleVariants()` | `get_possible_variants()` → `RPCollection` |
| `getScopeBySelectedElements()` | `get_scope_by_selected_elements()` → `RPCollection` |
| `getScopeElements()` | `get_scope_elements()` → `RPCollection` |
| `getScopeElementsByCategory(int)` | `get_scope_elements_by_category(category)` → `RPCollection` |
| `getVariationPoints()` | `get_variation_points()` → `RPCollection` |
| `isDirectoryPerModelComponent()` | `is_directory_per_model_component()` → `int` |
| `removeScopeElement(IRPModelElement)` | `remove_scope_element(element)` |
| `setScopeBySelectedElements()` | `set_scope_by_selected_elements()` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |

### 5.21 IRPConfiguration (in `RPConfiguration`)

| Java Method | Python Method |
|-------------|---------------|
| `addInitialInstance(IRPInstanceSpecification)` | `add_initial_instance(spec)` |
| `deleteInitialInstance(IRPInstanceSpecification)` | `delete_initial_instance(spec)` |
| `getInitialInstances()` | `get_initial_instances()` → `RPCollection` |
| `getItsComponent()` / `setItsComponent(IRPComponent)` | `get_its_component()` / `set_its_component(component)` |
| `getInstrumentationScope()` | `get_instrumentation_scope()` |
| `getAllElementsInInstrumentationScope()` | `get_all_elements_in_instrumentation_scope()` |
| `setAllElementsInInstrumentationScope(int)` | `set_all_elements_in_instrumentation_scope(value)` |
| `addToInstrumentationScope(IRPModelElement)` | `add_to_instrumentation_scope(element)` |
| `removeFromInstrumentationScope(IRPModelElement)` | `remove_from_instrumentation_scope(element)` |
| `addPackageToInstrumentationScope(IRPPackage)` | `add_package_to_instrumentation_scope(pkg)` |
| `removePackageFromInstrumentationScope(IRPPackage)` | `remove_package_from_instrumentation_scope(pkg)` |
| `getInstrumentationType()` / `setInstrumentationType(int)` | `get_instrumentation_type()` / `set_instrumentation_type(value)` |
| `getScopeType()` / `setScopeType(int)` | `get_scope_type()` / `set_scope_type(value)` |
| `getStatechartImplementation()` / `setStatechartImplementation(int)` | `get_statechart_implementation()` / `set_statechart_implementation(value)` |
| `getTimeModel()` / `setTimeModel(int)` | `get_time_model()` / `set_time_model(value)` |
| `getGenerateCodeForActors()` / `setGenerateCodeForActors(int)` | `get_generate_code_for_actors()` / `set_generate_code_for_actors(value)` |
| `needsCodeGeneration()` | `needs_code_generation()` → `int` |

### 5.22 IRPCollaboration (in `RPCollaboration`)

| Java Method | Python Method |
|-------------|---------------|
| `addActionBlock(str)` | `add_action_block(name)` → `RPActionBlock` |
| `addClassifierRole(IRPClassifier)` | `add_classifier_role(classifier)` → `RPClassifierRole` |
| `addClassifierRoleByName(str)` | `add_classifier_role_by_name(name)` |
| `addClassifierRoleForInstance(IRPInstanceSpecification)` | `add_classifier_role_for_instance(spec)` |
| `addMessage(IRPMessage, IRPMessage, str)` | `add_message(from_msg, to_msg, name)` → `RPMessage` |
| `addFoundMessage(IRPModelElement, str)` | `add_found_message(target, name)` → `RPMessage` |
| `addLostMessage(IRPMessage, str)` | `add_lost_message(source, name)` → `RPMessage` |
| `addReplyMessage(IRPMessage, str)` | `add_reply_message(to_msg, name)` → `RPMessage` |
| `addDestructionEvent(IRPClassifierRole)` | `add_destruction_event(role)` → `RPDestructionEvent` |
| `addCancelledTimeout(IRPModelElement, str, float, str)` | `add_cancelled_timeout(target, name, duration, time_unit)` |
| `addStateInvariant(IRPClassifierRole, str)` | `add_state_invariant(role, state)` |
| `addConditionMark(IRPClassifierRole)` | `add_condition_mark(role)` → `RPConditionMark` |
| `addInteractionOccurrence(IRPCollaboration)` | `add_interaction_occurrence(collab)` → `RPInteractionOccurrence` |
| `addInteractionOperator(int)` | `add_interaction_operator(op_type)` → `RPInteractionOperator` |
| `addDataFlow(IRPModelElement, IRPModelElement, str, str)` | `add_data_flow(from, to, value, param)` |
| `addDurationConstraint(IRPModelElement, float, float)` | `add_duration_constraint(element, min, max)` |
| `addDurationObservation(IRPModelElement, str)` | `add_duration_observation(element, name)` |
| `addTimeConstraint(IRPModelElement, float, float)` | `add_time_constraint(element, min, max)` |
| `addTimeInterval(IRPModelElement, float)` | `add_time_interval(element, value)` |
| `addTimeObservation(IRPModelElement, str)` | `add_time_observation(element, name)` |
| `addTimeout(IRPModelElement, str, float, str)` | `add_timeout(target, name, duration, unit)` |
| `addCtor(IRPClassifierRole)` | `add_ctor(role)` |
| `addDtor(IRPClassifierRole)` | `add_dtor(role)` |
| `addSystemBorder()` | `add_system_border()` |
| `generateSequence(str)` | `generate_sequence(path)` |
| `getMessages()` | `get_messages()` → `RPCollection` |
| `getClassifierRoles()` | `get_classifier_roles()` → `RPCollection` |
| `getInteractionOccurrences()` | `get_interaction_occurrences()` → `RPCollection` |
| `getInteractionOperators()` | `get_interaction_operators()` → `RPCollection` |
| `getExecutionOccurrences()` | `get_execution_occurrences()` → `RPCollection` |
| `getMessagePoints()` | `get_message_points()` → `RPCollection` |
| `getActivationMode()` | `get_activation_mode()` → `int` |
| `getActivator()` | `get_activator()` → `RPClassifierRole` |
| `getAssociations()` | `get_associations()` → `RPCollection` |
| `getClassifier()` | `get_classifier()` → `RPClassifier` |
| `getConcurrentGroup()` | `get_concurrent_group()` → `int` |
| `getMode()` | `get_mode()` → `int` |
| `getPredecessor()` | `get_predecessor()` → `RPClassifierRole` |
| `getSuccessor()` | `get_successor()` → `RPClassifierRole` |

### 5.23 IRPUseCase (in `RPUseCase`)

| Java Method | Python Method |
|-------------|---------------|
| `addExtensionPoint(str)` | `add_extension_point(name)` → `RPModelElement` |
| `addDescribingDiagram(IRPSequenceDiagram)` | `add_describing_diagram(diagram)` |
| `deleteDescribingDiagram(IRPSequenceDiagram)` | `delete_describing_diagram(diagram)` |
| `deleteEntryPoint(str)` | `delete_entry_point(name)` |
| `deleteExtensionPoint(str)` | `delete_extension_point(name)` |
| `findEntryPoint(str)` | `find_entry_point(name)` → `RPModelElement` |
| `findExtensionPoint(str)` | `find_extension_point(name)` → `RPModelElement` |
| `getDescribingDiagram(str)` | `get_describing_diagram(name)` → `RPSequenceDiagram` |
| `setIsBehaviorOverriden(int)` | `set_is_behavior_overriden(value)` |
| `updateContainedDiagramsOnServer()` | `update_contained_diagrams_on_server()` |

### 5.24 IRPAnnotation / IRPRequirement

| Java Method | Python Method |
|-------------|---------------|
| `addAnchor(IRPModelElement)` | `add_anchor(element)` |
| `removeAnchor(IRPModelElement)` | `remove_anchor(element)` |
| *Requirement:* `getRequirementID()` / `setRequirementID(str)` | `get_requirement_id()` / `set_requirement_id(value)` |

### 5.25 IRPStereotype (in `RPStereotype`)

| Java Method | Python Method |
|-------------|---------------|
| `addMetaClass(str)` | `add_meta_class(mc)` |
| `removeMetaClass(str)` | `remove_meta_class(mc)` |
| `setIsNewTerm(int)` | `set_is_new_term(value)` |

### 5.26 IRPType / IRPClassifierRole / IRPSysMLPort

| Java Method | Python Method |
|-------------|---------------|
| `addEnumerationLiteral(str)` | `add_enumeration_literal(name)` → `RPEnumerationLiteral` |
| `deleteEnumerationLiteral(IRPEnumerationLiteral)` | `delete_enumeration_literal(literal)` |
| `getEnumerationLiterals()` | `get_enumeration_literals()` → `RPCollection` |
| `getReferencedSequenceDiagram()` / `setReferencedSequenceDiagram(IRPSequenceDiagram)` | `get_referenced_sequence_diagram()` / `set_referenced_sequence_diagram(diagram)` |
| `getReferencingClassifierRolesRecursively()` | `get_referencing_classifier_roles_recursively()` → `RPCollection` |
| `isArray()` | `is_array()` → `int` |
| `isEnum()` | `is_enum()` → `int` |
| `isStruct()` | `is_struct()` → `int` |
| `isUnion()` | `is_union()` → `int` |
| `isPointer()` | `is_pointer()` → `int` |
| `isPointerToPointer()` | `is_pointer_to_pointer()` → `int` |
| `isReference()` | `is_reference()` → `int` |
| `isReferenceToPointer()` | `is_reference_to_pointer()` → `int` |
| `isTemplate()` | `is_template()` → `int` |
| `isEqualTo(IRPType)` | `is_equal_to(tp)` → `int` |
| `isImplicit()` | `is_implicit()` → `int` |
| `isKindEnumeration()` | `is_kind_enumeration()` → `int` |
| `isKindLanguage()` | `is_kind_language()` → `int` |
| `isKindStruct()` | `is_kind_struct()` → `int` |
| `isKindTypedef()` | `is_kind_typedef()` → `int` |
| `isKindUnion()` | `is_kind_union()` → `int` |

### 5.27 Graphics (IRPGraphElement, IRPGraphEdge, IRPGraphNode, etc.)

| Java Method | Python Method |
|-------------|---------------|
| `addProperty(IRPGraphicalProperty)` | `add_property(prop)` |
| `applyDefaultFormat()` | `apply_default_format()` |
| `getAllGraphicalProperties()` | `get_all_graphical_properties()` → `RPCollection` |
| `getAllProperties()` | `get_all_properties()` → `RPCollection` |
| `getAssociatedImage()` / `setAssociatedImage(str)` | `get_associated_image()` / `set_associated_image(path)` |
| `getDiagram()` | `get_diagram()` → `RPDiagram` |
| `getGraphicalParent()` | `get_graphical_parent()` → `RPGraphElement` |
| `getGraphicalProperty(str)` | `get_graphical_property(name)` → `RPGraphicalProperty` |
| `getGraphicalPropertyOfText(int)` | `get_graphical_property_of_text(text_index)` |
| `getImageLayout()` / `setImageLayout(int)` | `get_image_layout()` / `set_image_layout(layout)` |
| `getLocalProperties()` | `get_local_properties()` → `RPCollection` |
| `getModelObject()` | `get_model_object()` → `RPModelElement` |
| `getPropertyValue(str)` | `get_property_value(name)` → `str` |
| `getSelectedImage()` / `setSelectedImage(str)` | `get_selected_image()` / `set_selected_image(path)` |
| `removeProperty(IRPGraphicalProperty)` | `remove_property(prop)` |
| `setPropertyValue(str, str)` | `set_property_value(name, value)` |
| `setGraphicalProperty(IRPGraphicalProperty)` | `set_graphical_property(prop)` |
| `setGraphicalPropertyOfText(int, IRPGraphicalProperty)` | `set_graphical_property_of_text(index, prop)` |

### 5.28 Template Parameters

| Java Method | Python Method |
|-------------|---------------|
| `setClassType(IRPClassifier)` | `set_class_type(classifier)` |

### 5.29 Values (IRPInstanceSlot, IRPValueSpecification, etc.)

| Java Method | Python Method |
|-------------|---------------|
| `addElementValue(IRPModelElement)` | `add_element_value(element)` |
| `addInstanceSlot(IRPInstanceSlot)` | `add_instance_slot(slot)` |
| `addStringValue(str)` | `add_string_value(value)` |
| `getClassifier()` / `setClassifier(IRPClassifier)` | `get_classifier()` / `set_classifier(classifier)` |
| `getInstanceSlots()` | `get_instance_slots()` → `RPCollection` |
| `getSlotProperty()` / `setSlotProperty(IRPAttribute)` | `get_slot_property()` / `set_slot_property(attr)` |
| `getValue()` / `setValue(str)` | `get_value()` / `set_value(value)` |
| `getValues()` | `get_values()` → `RPCollection` |
| `isRootInstanceSpecification()` | `is_root_instance_specification()` → `int` |
| `populateSlots()` | `populate_slots()` |

---

## 6. Application API (IRPApplication)

Used in `src/rhapsody_cli/application.py`, not `models/`. Not typically mocked in unit tests.

| Java Method | Python Method |
|-------------|---------------|
| `activeProject` | `active_project` (property) |
| `addToModel(IRPUnit, str, int)` | `add_to_model(unit, path, mode)` |
| `addToModelEx(IRPUnit, str, int)` | `add_to_model_ex(unit, path, mode)` |
| `bringWindowToTop()` | `bring_window_to_top()` |
| `checkModel(IRPProject, int)` | `check_model(project, mode)` |
| `closeAllProjects()` | `close_all_projects()` |
| `createNewCollection()` | `create_new_collection()` → `RPCollection` |
| `createNewProject(str, str)` | `create_new_project(path, name)` → `RPProject` |
| `getActiveProject()` | `get_active_project()` → `RPProject` |
| `getBuildNo()` | `get_build_no()` → `str` |
| `getCodeGenSimplifiersRegistry()` | `get_code_gen_simplifiers_registry()` |
| `getDiagSynthAPI()` | `get_diag_synth_api()` |
| `getExternalCheckerRegistry()` | `get_external_checker_registry()` |
| `getExternalIDERegistry()` | `get_external_ide_registry()` |
| `getExternalRoundtripInvoker()` | `get_external_roundtrip_invoker()` |
| `getOMROOT()` | `get_omroot()` |
| `getOWPaneMgr()` | `get_ow_pane_mgr()` |
| `getRhapsodyDir()` | `get_rhapsody_dir()` → `str` |
| `getSearchManager()` | `get_search_manager()` |
| `getSelection()` | `get_selection()` |
| `getVersion()` | `get_version()` → `str` |
| `openProject(str)` | `open_project(path)` → `RPProject` |
| `quit()` | `quit()` |
| `regenerate(IRPComponent)` | `regenerate(component)` |
| `saveAll()` | `save_all()` |
| `setLog(IRPASCIIFile)` | `set_log(file)` |
| `generate(IRPComponent, int)` | `generate(component, mode)` |
| `generateElements(IRPCollection)` | `generate_elements(elements)` |
| `generateEntireProject(IRPProject, int)` | `generate_entire_project(project, mode)` |

---

## 7. Guidelines for Adding a New Wrapper

### 7.1 Implementation Steps

1. **Create model file**: `src/rhapsody_cli/models/elements/<subpackage>/model_<class>.py`
2. **Subclass the appropriate base** (check hierarchy in section 2.1)
3. **Register wrapper** at module level:
   ```python
   AbstractRPModelElement.register_wrapper("MetaClass", RPMyClass)
   ```
4. **Add import** in subpackage's `__init__.py`
5. **Implement methods** using one of the 5 COM call patterns from section 3.1
6. **Add docstring** to each method with Java API reference:
   ```python
   def add_superclass(self, superclass: "RPClass") -> "RPGeneralization":
       """Add a superclass to this class.
       
       Reference: com.telelogic.rhapsody.core.IRPClass::addSuperclass(IRPClass superClass)
       """
   ```

### 7.2 Testing Steps

1. **Create test file**: `tests/unit/models/<subpackage>/test_model_<class>.py`
2. **Import fakes**: `from tests.unit.models.fakes import make_fake_element, make_fake_collection`
3. **Write tests** following patterns from section 4
4. **Test each method**:
   - Getter: mock return value, assert Python wrapper returns it
   - Setter: call setter, assert COM method called with correct arg
   - Element-returning: mock COM return, assert wrapped result
   - Collection-returning: mock collection, assert `RPCollection` behavior
   - Error path: mock COM error, assert `RhapsodyRuntimeException`
5. **Test wrapper registration**: verify `wrap()` dispatches to the correct class
6. **Test inheritance hierarchy**: verify `isinstance()` checks work

---

## 8. Quick Reference: COM Call Patterns

```python
# 1. No-arg getter → _get_method_or_property
def get_name(self) -> str:
    return self._get_method_or_property(self._com, "getName", "name")

# 2. Single-arg setter → _set_method_or_property
def set_name(self, value: str) -> None:
    self._set_method_or_property(self._com, "setName", "name", value)

# 3. Parameterized method → call_com directly
def find_class(self, name: str) -> "RPClass":
    result = self.call_com(lambda: self._com.findClass(name))
    return AbstractRPModelElement.wrap(result)

# 4. Collection return → RPCollection wrapper
def get_classes(self) -> RPCollection:
    return RPCollection(self.call_com(lambda: self._com.getClasses()))

# 5. Element argument (unwrap → call → wrap result)
def add_dependency_to(self, target: "RPModelElement") -> "RPDependency":
    result = self.call_com(lambda: self._com.addDependencyTo(target._com))
    return AbstractRPModelElement.wrap(result)

# 6. Boolean/int return (no special treatment)
def is_modified(self) -> int:
    return self._get_method_or_property(self._com, "isModified", "modified")
```
