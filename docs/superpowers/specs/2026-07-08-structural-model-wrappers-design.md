# Structural Model Wrappers — Iteration 1 Design

## Problem

The 2026-07-06 and 2026-07-07 designs established `rhapsody_cli`'s wrapping
pattern and an initial set of 12 concrete wrapper classes, then fixed the
class hierarchy to mirror `com.telelogic.rhapsody.core` (documented in
`docs/java_api/`). The current wrappers cover the most commonly used
metaclasses, but coverage of the Java API is incomplete in two ways:

1. **Missing methods on existing wrappers.** `RPModelElement`, `RPUnit`,
   `RPPackage`, `RPProject`, `RPClassifier`, `RPClass`, `RPRelation`, and
   `RPInstance` implement only a subset of the methods declared on their
   Java counterparts. Navigation (`getOwner`, `getOwningProject`), stereotype
   management (`getStereotypes`, `addStereotype`), dependency management
   (`getDependencies`, `addDependencyTo`), property access (`getProperty`,
   `setPropertyValue`), and many factory methods (`addInterface`,
   `addEnumeration`, `addSignal`) are absent.

2. **Missing wrappers for structural interfaces that exist in the Java API.**
   `IRPStereotype`, `IRPTag`, `IRPProfile`, `IRPEnumerationLiteral`,
   `IRPAssociationClass`, `IRPAssociationRole`, `IRPGeneralization`,
   `IRPDependency`, `IRPHyperLink`, `IRPComment`, `IRPConstraint`,
   `IRPComponent`, `IRPConfiguration`, `IRPModule`, `IRPNode`,
   `IRPCollaboration`, and `IRPComponentInstance` all have no Python wrapper.

The long-term goal is full parity between the Python wrapper layer and the
Rhapsody Java API. That goal is too large for a single iteration, so it is
decomposed into iterations by layer. This spec covers **Iteration 1: the
structural layer** (classifiers, relations, containment). Subsequent
iterations will handle diagrams, behavioral elements, graphical elements,
search, OSLC, and other subsystems, each in its own spec.

### Interfaces confirmed to exist in the Java API

Several interfaces assumed to exist (`IRPInterface`, `IRPEnumeration`,
`IRPDataType`, `IRPSignal`, `IRPException`) do **not** exist as separate
interfaces in this Rhapsody Java API version (verified by globbing
`docs/java_api/com/telelogic/rhapsody/core/IRP*.html`). The structural
interfaces that do exist and are in scope for Iteration 1 are listed in the
Goal section below. Where those metaclasses exist in the COM API, they are
represented via the generic `IRPClassifier`/`IRPModelElement` interfaces with
a different `getMetaClass()` string — the Python wrappers mirror the Java
interface structure, not the COM metaclass names.

## Goal

Complete the structural layer of the model wrapper to full Java API parity.

### Existing wrappers to complete (full method parity)

- `RPModelElement` (`IRPModelElement`) — base for all model elements
- `RPUnit` (`IRPUnit`) — base for saveable elements
- `RPClassifier` (`IRPClassifier`) — base for classifiable elements
- `RPClass` (`IRPClass`) — class elements
- `RPRelation` (`IRPRelation`) — base for relationships
- `RPInstance` (`IRPInstance`) — instance elements
- `RPPackage` (`IRPPackage`) — package containers
- `RPProject` (`IRPProject`) — top-level project containers

### New wrappers to add

| Python class | Java interface | Extends (Python) |
|---|---|---|
| `RPGeneralization` | `IRPGeneralization` | `RPModelElement` |
| `RPDependency` | `IRPDependency` | `RPModelElement` |
| `RPHyperLink` | `IRPHyperLink` | `RPDependency` |
| `RPEnumerationLiteral` | `IRPEnumerationLiteral` | `RPModelElement` |
| `RPComment` | `IRPComment` | `RPModelElement` |
| `RPConstraint` | `IRPConstraint` | `RPModelElement` |
| `RPTag` | `IRPTag` | `RPVariable` |
| `RPStereotype` | `IRPStereotype` | `RPClassifier` |
| `RPAssociationClass` | `IRPAssociationClass` | `RPClass` |
| `RPAssociationRole` | `IRPAssociationRole` | `RPInstance` |
| `RPProfile` | `IRPProfile` | `RPPackage` |
| `RPComponent` | `IRPComponent` | `RPUnit` |
| `RPConfiguration` | `IRPConfiguration` | (parent confirmed from docs at implementation time) |
| `RPModule` | `IRPModule` | `RPInstance` |
| `RPNode` | `IRPNode` | (parent confirmed from docs at implementation time) |
| `RPCollaboration` | `IRPCollaboration` | (parent confirmed from docs at implementation time) |
| `RPComponentInstance` | `IRPComponentInstance` | `RPInstance` |

### Out of scope (deferred to later iterations)

- All diagram types (`IRPSequenceDiagram`, `IRPUseCaseDiagram`,
  `IRPComponentDiagram`, `IRPCollaborationDiagram`, `IRPDeploymentDiagram`,
  `IRPObjectModelDiagram`, `IRPStructureDiagram`, `IRPTimingDiagram`,
  `IRPPanelDiagram`, `IRPActivityDiagram`, `IRPStatechartDiagram`) — diagrams
  iteration, which also covers `IRPGraphElement`/`IRPGraphNode`/`IRPGraphEdge`/
  `IRPGraphicalProperty`.
- All behavioral elements (`IRPState`, `IRPStateVertex`, `IRPTransition`,
  `IRPTrigger`, `IRPEvent`, `IRPEventReception`, `IRPGuard`, `IRPAction`,
  `IRPActionBlock`, `IRPConnector`, `IRPPin`, activity/flow elements) —
  behavioral iteration.
- Graphical elements, table/matrix views, search manager, OSLC full
  integration, plugins, code generation, external integrators.
- Runtime metaclass-string discovery — small follow-up task to confirm
  `register_wrapper` strings match the COM API's actual `getMetaClass()`
  return values.

## Architecture

### Inheritance hierarchy (Python, after Iteration 1)

```
RPModelElement                  (IRPModelElement)
├── RPUnit                      (IRPUnit)
│   ├── RPPackage               (IRPPackage)
│   │   └── RPProfile           (IRPProfile)
│   ├── RPProject               (IRPProject)
│   ├── RPComponent             (IRPComponent)
│   ├── RPClassifier            (IRPClassifier)
│   │   ├── RPClass             (IRPClass)
│   │   │   └── RPAssociationClass  (IRPAssociationClass)
│   │   └── RPStereotype        (IRPStereotype)
│   ├── RPRelation              (IRPRelation)
│   │   └── RPInstance          (IRPInstance)
│   │       ├── RPModule        (IRPModule)
│   │       ├── RPComponentInstance (IRPComponentInstance)
│   │       └── RPAssociationRole   (IRPAssociationRole)
│   └── RPConfiguration         (IRPConfiguration — exact parent TBD)
├── RPEnumerationLiteral        (IRPEnumerationLiteral)
├── RPComment                   (IRPComment)
├── RPConstraint                (IRPConstraint)
├── RPGeneralization            (IRPGeneralization)
├── RPDependency                (IRPDependency)
│   └── RPHyperLink             (IRPHyperLink)
├── RPVariable                  (IRPVariable — already exists)
│   └── RPTag                   (IRPTag)
├── RPAttribute                 (IRPAttribute — already exists)
├── RPAnnotation                (IRPAnnotation — already exists)
│   └── RPRequirement           (IRPRequirement — already exists)
├── RPDiagram                   (IRPDiagram — already exists)
└── RPNode, RPCollaboration     (parents TBD from docs)
```

Java's `IRPInstance extends IRPRelation, IRPUnit, IRPModelElement` looks like
multiple inheritance, but it is linear (`IRPRelation extends IRPUnit extends
IRPModelElement`). Python's single-inheritance chain mirrors this cleanly; no
MRO complications are expected.

### File layout refactor (hybrid split)

The current `models/elements/` is a flat directory of category files. Two of
them — `classifiers.py` and `relations.py` — will grow significantly. The
hybrid approach: split those two (and `containment.py`) into packages, leave
the smaller category files alone.

#### Target layout

```
src/rhapsody_cli/models/
├── __init__.py
├── _core.py
├── application.py
└── elements/
    ├── __init__.py
    ├── classifiers/                        ← package (was classifiers.py)
    │   ├── __init__.py
    │   ├── model_classifier.py             ← RPClassifier (base)
    │   ├── model_class.py                  ← RPClass
    │   ├── model_actor.py                  ← RPActor
    │   ├── model_usecase.py                ← RPUseCase
    │   ├── model_operation.py              ← RPOperation
    │   ├── model_interface_item.py         ← RPInterfaceItem
    │   ├── model_statechart.py             ← RPStatechart
    │   ├── model_stereotype.py             ← RPStereotype (new)
    │   └── model_association_class.py      ← RPAssociationClass (new)
    ├── containment/                        ← package (was containment.py)
    │   ├── __init__.py
    │   ├── model_package.py                ← RPPackage
    │   ├── model_project.py                ← RPProject
    │   ├── model_profile.py                ← RPProfile (new)
    │   ├── model_component.py              ← RPComponent (new)
    │   ├── model_configuration.py          ← RPConfiguration (new)
    │   ├── model_node.py                   ← RPNode (new)
    │   ├── model_module.py                 ← RPModule (new)
    │   ├── model_collaboration.py          ← RPCollaboration (new)
    │   └── model_component_instance.py     ← RPComponentInstance (new)
    ├── relations/                          ← package (was relations.py)
    │   ├── __init__.py
    │   ├── model_relation.py               ← RPRelation (base)
    │   ├── model_instance.py               ← RPInstance
    │   ├── model_generalization.py         ← RPGeneralization (new)
    │   ├── model_dependency.py             ← RPDependency (new)
    │   ├── model_hyperlink.py              ← RPHyperLink (new)
    │   └── model_association_role.py       ← RPAssociationRole (new)
    ├── diagrams.py                         ← unchanged (small, multiple classes)
    ├── requirements.py                     ← unchanged (small, multiple classes)
    ├── misc.py                             ← new: RPComment, RPConstraint, RPEnumerationLiteral
    └── variables.py                        ← grows: add RPTag
```

#### Naming convention

- **Per-class files** (one wrapper class per file, in a package):
  `model_<snake_case_metaclass>.py`. The `model_` prefix avoids Python
  reserved words (`model_class.py`, `model_module.py`) and gives a
  consistent, search-friendly name.
- **Category files** (flat modules holding a few small related classes): no
  prefix — `diagrams.py`, `requirements.py`, `variables.py`, `misc.py`.
- **Split rule:** if a category file grows beyond ~5 classes or ~300 lines,
  it becomes a package and its classes move to `model_*.py` files.
  `variables.py` (3 classes after adding `RPTag`) and `misc.py` (3 classes)
  stay flat.
- **File location for TBD-parent wrappers:** `RPConfiguration`, `RPNode`,
  and `RPCollaboration` are placed in `containment/` by default. If the
  implementation-time read of their Java `extends` clause reveals a parent
  that belongs to a different package (e.g., `IRPNode extends IRPInstance`),
  the file moves to that parent's package. The package `__init__.py`
  re-exports are updated accordingly.

#### Re-export rule (backwards compatibility)

Each new package's `__init__.py` re-exports its classes so existing imports
keep working:

- `from rhapsody_cli.models.elements.classifiers import RPClass` — still works
- `from rhapsody_cli.models.elements.containment import RPPackage` — still works
- `from rhapsody_cli.models.elements.relations import RPRelation` — still works
- `from rhapsody_cli.models.elements import RPClass` — still works

The public API is stable across the refactor. The `_com` attribute,
`_WRAPPER_REGISTRY`, and `_get_method_or_property` /
`_set_method_or_property` helpers are internal and may change.

### Base layer completion (`RPModelElement` + `RPUnit`)

These two are the root of the inheritance tree. Every method added here is
inherited by all wrappers below, so they are done first and tested in
isolation.

#### `RPModelElement` (wraps `IRPModelElement`, in `_core.py`)

Currently has: `getName`, `setName`, `getMetaClass`, `getGUID` (plus dunders).

Method categories to add (each method sourced from `IRPModelElement.html`):

1. **Navigation & ownership** — `getOwner()`, `getProject()`,
   `getOwningPackage()`, `getOwningProject()`, `getNestedElements()`,
   `findNestedElement(name, meta_class)`,
   `findNestedElementByMetaClass(name, meta_class)`, `getFullPathName(sep)`,
   `getDisplayName()`, `getToolTipHTML()`, `getAncestors()`,
   `getChildren()`, `getDescendants()`, `isInProject(project)`,
   `getOfTemplate()`, `isATemplate()`, `getTi()`.
2. **Identification & metadata** — `getDescription()`, `setDescription(desc)`,
   `setGUID(guid)`, `clone()`, `changeTo(meta_class)`.
3. **Stereotypes** — `getStereotypes()`, `addStereotype(stereotype)`,
   `setStereotype(stereotype)`, `removeStereotype(stereotype)`,
   `hasStereotype(stereotype)`. Returns/accepts `RPStereotype` wrappers.
4. **Tags & tagged values** — `getTag(name)`, `getLocalTags()`,
   `getAllTags()`, `setTagValue(tag, value)`,
   `setTagElementValue(tag, element)`. Returns/accepts `RPTag` wrappers.
5. **Dependencies** — `getDependencies()`, `addDependencyTo(element)`,
   `addDependencyBetween(source, target)`, `deleteDependency(dependency)`.
   Returns/accepts `RPDependency` wrappers.
6. **Properties (custom properties)** — `getProperty(name)`,
   `getPropertyValue(name)`, `setPropertyValue(name, value)`,
   `addProperty(name, value)`, `removeProperty(name)`, `getProperties()`.
7. **Lifecycle & mutation** — `deleteFromProject()`, `canDelete()`,
   `moveTo(new_owner)`, `highLightElement(color)`, `changeHighLight()`,
   `clearHighlight()`.
8. **Diagrams** — `getMainDiagram()`, `setMainDiagram(diagram)`.
9. **OSLC** — `getOSLCLinks()`, `createOSLCLink(type, uri)`,
   `deleteOSLCLink(link)`. The `OSLCLink` inner class is modeled as a small
   dataclass; `OSLCLink.Types` as an `Enum`. If the COM API does not expose
   OSLC cleanly, methods raise `NotImplementedError` with a TODO.
10. **Other** — `getType()`, `getKeyword()`, `getVersion()`,
    `setVersion(version)`, `getAuthor()`, `setAuthor(author)`,
    `getComment()`, `setComment(comment)`.

#### `RPUnit` (wraps `IRPUnit`, in `_core.py`)

Currently has: `save`, `getFilename`, `setFilename`, `isReadOnly`,
`setReadOnly`, `getNestedElements`.

Method categories to add:

1. **Load/unload** — `load(with_subs)`, `unload()`, `reload()`,
   `reloadIfStatusChanged()`.
2. **Status** — `getStatus()`, `isLoaded()`, `isSeparateSaveUnit()`,
   `setSeparateSaveUnit(flag)`.
3. **Language** — `getLanguage()`, `setLanguage(language)`.
4. **File ops** — `saveAs(filename)`,
   `copyToAnotherProject(target_project, with_subs)`.
5. **Nested units** — `getNestedSaveUnits()`,
   `getNestedSaveUnitsCount()`, `getStructureDiagrams()`.
6. **Add-to-model mode** — `getAddToModelMode()`, `setAddToModelMode(mode)`.
   Mode is an enum-like int; modeled as a module-level `AddToModelMode`
   `IntEnum` in `_core.py` (or a new `_enums.py` if more enums appear).

### Mid-layer completion (`RPClassifier` + `RPClass` + `RPRelation` + `RPInstance`)

Patterns are identical to the base layer; only the method lists differ.

#### `RPClassifier` (wraps `IRPClassifier`, extends `RPUnit`)

Currently has: `addAttribute`, `addOperation`, `getAttributes`, `getOperations`,
`addGeneralization`, `addStatechart`.

Categories to add:
- **Factory methods for child classifiers** — `addClass()`, `addInterface()`
  (if exposed by COM, else `NotImplementedError`), `addActor()`, `addUseCase()`,
  `addSignal()`, `addException()`, `addEnumeration()`, `addAssociation()`,
  `addAssociationClass()`, `addDependency()`, `addNestedPackage()`.
- **Traversal** — `getNestedClassifiers()`, `getGeneralizations()`,
  `getNestedAssociations()`.
- **State/behavior** — `getStatecharts()`, `addActivityDiagram()`,
  `getActivityDiagrams()` (mirror even if the diagram wrappers come later).
- **Class-level flags** — `getIsAbstract()`, `setIsAbstract()`, `getIsLeaf()`,
  `setIsLeaf()`.

Some `add*` methods overlap with `IRPPackage` (both can add classes, actors,
etc.). Java allows this; we mirror both, even at the cost of some
duplication, because parity is the goal.

#### `RPClass` (wraps `IRPClass`, extends `RPClassifier`)

Currently has: `addSuperclass`, `addConstructor`, `addDestructor`,
`getIsAbstract`, `addClass`.

Categories to add:
- **Inheritance** — `getSuperclasses()`, `getSubclasses()`, `removeSuperclass()`.
- **Structural members** — `getNestedClasses()`, `getAssociations()`,
  `getPorts()`, `getInterfaces()`.
- **Constructors/destructors** — `getConstructors()`, `getDestructors()`.
- **Flags** — `setIsAbstract()`, `getIsLeaf()`, `setIsLeaf()`, `getIsActive()`,
  `setIsActive()`, `getIsRoot()`, `setIsRoot()`.
- **Template** — `getTemplateParameters()`, `addTemplateParameter()`,
  `isTemplate()`, `instantiateTemplate()`. Template support may be partial;
  mirror what the Java API exposes.

#### `RPRelation` (wraps `IRPRelation`, extends `RPUnit`)

Currently the most complete wrapper (~30 methods). The implementation pass
here is primarily an audit: enumerate every `IRPRelation` method from the
Java docs, check each against the existing implementation, add any missing
ones. Expected delta is small.

#### `RPInstance` (wraps `IRPInstance`, extends `RPRelation`)

Currently has: `getAllNestedElements`, `getAttributeValue`, `setAttributeValue`,
`getInLinks`, `getOutLinks`.

Categories to add:
- **Instantiation** — `getInstantiatedBy()`, `setInstantiatedBy(operation)`,
  `getListOfInitializerArguments()`,
  `setInitializerArgumentValue(arg_name, arg_value)`, `setExplicit()`,
  `setImplicit()`.
- **Structure** — `addRelationToTheWhole(rel_name)`.
- **Diagrams** — `updateContainedDiagramsOnServer(enforce_update)`
  (Rhapsody Model Manager integration; mirror it, may raise
  `NotImplementedError` if COM does not expose it).

### Containment-layer completion (`RPPackage` + `RPProject` + new wrappers)

#### `RPPackage` (wraps `IRPPackage`, extends `RPUnit`)

Currently has: `addClass`, `addNestedPackage`, `addActor`, `addGlobalFunction`.

Categories to add:
- **Factory methods** — `addUseCase()`, `addInterface()`, `addSignal()`,
  `addException()`, `addEnumeration()`, `addAssociation()`,
  `addAssociationClass()`, `addDependency()`, `addPackage()`,
  `addDiagram()` variants, `addRequirement()`, `addComment()`,
  `addConstraint()`.
- **Traversal** — `getNestedPackages()`, `getClasses()`, `getActors()`,
  `getUseCases()`, `getInterfaces()`, `getEnumerations()`, `getSignals()`,
  `getExceptions()`, `getAssociations()`, `getDependencies()`,
  `getComponents()`, `getSubSystems()`, `getDiagrams()`, `getRequirements()`,
  `getComments()`, `getConstraints()`.
- **Import/export** — `importFromFile(filename)`, `exportToFile(filename)`
  (if exposed by `IRPPackage`).

#### `RPProject` (wraps `IRPProject`, extends `RPUnit`)

Currently has: `addPackage`, `close`, `becomeActiveProject`, `findComponent`,
`getPackages`, `getRoot`.

Categories to add:
- **Factory methods** — `addClass()`, `addActor()`, `addUseCase()`,
  `addInterface()`, `addEnumeration()`, `addAssociation()`, `addDependency()`,
  `addProfile()`, `addConfiguration()`, `addDiagram()` variants.
- **Traversal** — `getAllElements()`, `getUnits()`, `getComponents()`,
  `getConfigurations()`, `getActiveConfiguration()`, `getProfiles()`,
  `getDiagrams()`.
- **Profile management** — `addProfile()`, `removeProfile()`, `getProfiles()`,
  `applyProfile()`.
- **Configuration management** — `getConfigurations()`,
  `getActiveConfiguration()`, `setActiveConfiguration()`, `addConfiguration()`,
  `removeConfiguration()`.
- **File ops** — `saveAs(filename)`, `importSubProject(filename)`,
  `exportSubProject(filename)`, `importPackage(filename)`.
- **Search** — `findByName(name)`, `findByMetaClass(meta_class)`,
  `findElementByGUID(guid)`. (Full search manager is deferred.)
- **Lifecycle** — `isDirty()`, `setDirty()`.

#### New containment wrappers

| Python class | Java interface | Parent (Python) | Key own methods |
|---|---|---|---|
| `RPProfile` | `IRPProfile` | `RPPackage` | Profile-specific methods (enumerated from `IRPProfile.html` — likely `getStereotypes()`, `getTags()`, `applyToProject()`, `exportProfile()`) |
| `RPComponent` | `IRPComponent` | `RPUnit` | Component-specific methods (enumerated from `IRPComponent.html`) |
| `RPConfiguration` | `IRPConfiguration` | (parent TBD) | Configuration-specific methods (enumerated from `IRPConfiguration.html`) |
| `RPModule` | `IRPModule` | `RPInstance` | Module-specific methods (enumerated from `IRPModule.html`) |
| `RPNode` | `IRPNode` | (parent TBD) | Node-specific methods (enumerated from `IRPNode.html`) |
| `RPCollaboration` | `IRPCollaboration` | (parent TBD) | Collaboration-specific methods (enumerated from `IRPCollaboration.html`) |
| `RPComponentInstance` | `IRPComponentInstance` | `RPInstance` | Component-instance-specific methods |

The parent interfaces of `IRPConfiguration`, `IRPNode`, and `RPCollaboration`
could not be confirmed within the token budget of the initial exploration.
The implementation reads each interface's HTML `extends` clause first and
places the Python class accordingly. If the parent is an interface not yet
wrapped, either wrap it too (if in scope) or use the closest wrapped
ancestor and note the deviation in the implementation log.

### Leaf-level new wrappers

#### Group A — Extends `RPModelElement` directly

##### `RPGeneralization` (wraps `IRPGeneralization`, extends `RPModelElement`)

File: `relations/model_generalization.py`. Own methods:
- `getBaseClass()` → `RPClassifier` — the parent class.
- `setBaseClass(classifier)` — sets the parent class.
- `getDerivedClass()` → `RPClassifier` — the child class.
- `setDerivedClass(classifier)` — sets the child class.
- `getExtensionPoint()` → `str` — the extension point.
- `setExtensionPoint(name)` — sets the extension point.
- `getIsVirtual()` → `int` — 1 if virtual, 0 otherwise.
- `setIsVirtual(flag)` — sets virtuality.
- `getVisibility()` → `str` — visibility string.
- `setVisibility(visibility)` — sets visibility.

Registration: `register_wrapper("Generalization", RPGeneralization)`.

##### `RPDependency` (wraps `IRPDependency`, extends `RPModelElement`)

File: `relations/model_dependency.py`. Own methods:
- `getDependent()` → `RPModelElement` — the source element.
- `setDependent(element)` — sets the source.
- `getDependsOn()` → `RPModelElement` — the target element.
- `setDependsOn(element)` — sets the target.
- `isNeedToMigrate()` → `int` — 1 if an OSLC link not yet migrated.
- `setLinkType(link_type)` — for remote-artifact dependencies, sets link type.
- `setOwnerWithoutChangingDependent(new_owner)` — changes owner without
  altering the dependent.

Registration: `register_wrapper("Dependency", RPDependency)`.

##### `RPHyperLink` (wraps `IRPHyperLink`, extends `RPDependency`)

File: `relations/model_hyperlink.py`. Own methods: enumerated from
`IRPHyperLink.html` during implementation (small method set; likely includes
`getURL()`, `setURL()` or similar — confirmed at implementation time).

Registration: `register_wrapper("HyperLink", RPHyperLink)`.

##### `RPEnumerationLiteral` (wraps `IRPEnumerationLiteral`, extends `RPModelElement`)

File: `misc.py`. Own methods:
- `getValue()` → `str` — the literal's value.
- `setValue(value)` — sets the value.

Registration: `register_wrapper("EnumerationLiteral", RPEnumerationLiteral)`.

##### `RPComment` (wraps `IRPComment`, extends `RPModelElement`)

File: `misc.py`. Own methods: enumerated from `IRPComment.html` during
implementation. Distinct from `IRPAnnotation` (both exist in the Java API).

Registration: `register_wrapper("Comment", RPComment)`.

##### `RPConstraint` (wraps `IRPConstraint`, extends `RPModelElement`)

File: `misc.py`. Own methods: enumerated from `IRPConstraint.html` during
implementation. Likely includes `getConstraint()`, `setConstraint()`,
`getLanguage()`.

Registration: `register_wrapper("Constraint", RPConstraint)`.

#### Group B — Extends `RPVariable` / `RPClassifier` / `RPClass` / `RPInstance`

##### `RPTag` (wraps `IRPTag`, extends `RPVariable`)

File: `variables.py` (grows from 2 to 3 classes). Own methods:
- `getBase()` → `RPTag` — the base tag this local copy is based on.
- `getFromProfile()` → `RPProfile` — the profile where the tag was defined.
- `getMultiplicity()` → `str` — multiplicity string.
- `setMultiplicity(multiplicity)` — sets multiplicity.
- `getTagMetaClass()` → `str` — the metaclass this tag applies to.
- `setTagMetaClass(meta_class)` — sets the applicable metaclass.
- `getValue()` → `str` — the tag's value.
- `setValue(value)` — sets the value.
- `setTagContextValue(elements, multiplicities)` — sets the value to a
  specific instance of another model element. Takes two `RPCollection` args.

Registration: `register_wrapper("Tag", RPTag)`.

##### `RPStereotype` (wraps `IRPStereotype`, extends `RPClassifier`)

File: `classifiers/model_stereotype.py`. Own methods:
- `addMetaClass(meta_class)` — adds a metaclass to the list this stereotype
  can be applied to.
- `removeMetaClass(meta_class)` — removes a metaclass from the list.
- `getOfMetaClass()` → `str` — comma-separated metaclass names.
- `getIcon()` → `str` — full path to the stereotype's image file.
- `getIsNewTerm()` → `int` — 1 if "new term" stereotype, 0 otherwise.
- `setIsNewTerm(flag)` — toggles "new term" status.

Registration: `register_wrapper("Stereotype", RPStereotype)`.

Because `RPStereotype` extends `RPClassifier`, it inherits `addAttribute`,
`addOperation`, `getAttributes`, `getOperations`, etc. — stereotypes in
Rhapsody can themselves have attributes and operations. This is faithful to
the Java API.

##### `RPAssociationClass` (wraps `IRPAssociationClass`, extends `RPClass`)

File: `classifiers/model_association_class.py`. Own methods:
- `getEnd1()` → `RPRelation` — the first end of the association.
- `getEnd2()` → `RPRelation` — the second end.
- `getIsClass()` → `int` — 1 if association class, 0 if association element.
- `setIsClass(flag)` — toggles between association class and association
  element.

Registration: `register_wrapper("AssociationClass", RPAssociationClass)`.

##### `RPAssociationRole` (wraps `IRPAssociationRole`, extends `RPInstance`)

File: `relations/model_association_role.py`. Own methods: enumerated from
`IRPAssociationRole.html` during implementation. Likely includes
role-specific navigation methods.

Registration: `register_wrapper("AssociationRole", RPAssociationRole)`.

### Registration string convention

All `register_wrapper` calls use best-effort metaclass strings matching the
Rhapsody metaclass name (the part of the Java interface name after `IRP`):
`Generalization`, `Dependency`, `HyperLink`, `EnumerationLiteral`, `Comment`,
`Constraint`, `Tag`, `Stereotype`, `AssociationClass`, `AssociationRole`,
`Profile`, `Component`, `Configuration`, `Module`, `Node`, `Collaboration`,
`ComponentInstance`. If runtime discovery (deferred) shows different strings,
registrations are updated. For now, unmapped metaclasses fall back to
`RPModelElement` in `wrap()`, so a mismatch is non-blocking.

## Cross-Cutting Conventions

### Java API docs as docstrings (applies to all methods)

Every method on every wrapper (existing methods backfilled + new methods)
carries a Python docstring copied from the corresponding Java API
documentation in `docs/java_api/`.

**Sourcing:** For each method, read its row in the interface's HTML
method-summary table (or the method-detail section) and extract the
description text, `@param` descriptions, and `@return` description. Convert
HTML formatting to plain text with minimal reStructuredText-style markup:
backticks around code terms (e.g. ``IRPCollection``), no raw HTML.

**Format (Google-style, matching existing `getNestedElements` docstring):**

```python
def getOwner(self) -> "RPModelElement":
    """Returns the owner of the model element.

    Returns:
        The ``IRPModelElement`` that owns this element, wrapped in its
        matching Python wrapper class.
    """
    return wrap(call_com(lambda: self._com.getOwner()))
```

**Rules:**
1. Every public method gets a docstring. No exceptions.
2. The first line is the Java API description, verbatim where possible.
3. `Args:` section lists each parameter with its Java description and Python type.
4. `Returns:` section describes the return value and Python type. For methods
   returning wrappers, note the wrapper class.
5. `Raises:` section lists `RhapsodyRuntimeException` for COM-failure paths
   and `NotImplementedError` for methods the COM Prog ID does not expose.
6. Module-level docstrings on each `model_*.py` file copy the Java
   interface's class-level Javadoc as the module summary, plus a note like
   "Wraps ``com.telelogic.rhapsody.core.IRPClass``."
7. Class docstrings copy the Java interface's class-level Javadoc verbatim.
8. Existing methods without docstrings get backfilled in this iteration.
9. **Deprecated methods:** methods marked as `@deprecated` in the Java API
   docs (see `docs/java_api/deprecated-list.html`) are skipped — not
   implemented, not docstring'd, not tested. The checklist comment marks
   them as `deprecated - skipped` so the audit trail shows they were
   intentionally omitted, not forgotten.

### Implementation patterns (consistent with existing)

- **Reads:** `_get_method_or_property(self._com, "getX", "x")` — prefers
  Java-style method, falls back to property.
- **Writes:** `_set_method_or_property(self._com, "setX", "x", value)`.
- **Returns a single element:** `wrap(call_com(lambda: self._com.getOwner()))`
  — the existing `wrap()` factory dispatches to the right subclass.
- **Returns a collection:** `RPCollection(call_com(lambda: ...))`.
- **Accepts a wrapper param:** `call_com(lambda: self._com.addStereotype(stereotype._com))`
  — unwrap to `._com` inline.
- **Accepts a string/int param:** pass through directly.
- **Returns a primitive:** `str(...)` or `int(...)` cast.

### Error handling

1. All COM calls go through `call_com(lambda: ...)`.
2. Method/property dispatch via `_get_method_or_property` /
   `_set_method_or_property`.
3. Methods the COM Prog ID does not expose are still defined (for parity) but
   raise `NotImplementedError` with a message like:
   `"Rhapsody2.Application.1 does not expose <methodName> on <metaclass>;
   method is defined for Java API parity only."` Discovered during
   implementation by probing the COM object's `hasattr`.
4. Return wrapping: single elements → `wrap(call_com(...))`; collections →
   `RPCollection(call_com(...))`; primitives → cast.
5. Parameter unwrapping: wrapper params → `arg._com` inline.
6. Exceptions: `RhapsodyRuntimeException` for COM failures (automatic via
   `call_com`); `NotImplementedError` for un-exposed methods.

### Type annotations

- Do NOT use `from __future__ import annotations` (forbidden per
  `docs/CODE_GUIDELINES.md`). Use string-quoted forward refs (e.g.
  `"RPCollection"`) or `TYPE_CHECKING` imports.
- mypy runs in strict mode; all functions need return type annotations.
- Use `# type: ignore[attr-defined]` sparingly for `win32com`/`pywintypes`.

### Coverage tracking

Each `model_*.py` file starts with a header comment listing every Java API
method on the wrapped interface(s), with three checkboxes per method:

```python
# IRPClass method parity checklist:
# [x] addSuperclass          [x] impl  [x] docstring  [x] test
# [x] addConstructor         [x] impl  [x] docstring  [x] test
# [ ] addAssociation         [ ] impl  [ ] docstring  [ ] test
# ...
```

A method counts as done only when all three boxes are checked.

## Implementation Plan (Approach A — Hierarchy-First, Bottom-Up)

1. **Step 0 — Refactor.** Create the `classifiers/`, `relations/`,
   `containment/` packages with `__init__.py` re-exports. Move existing
   classes from the flat files into `model_*.py` files. Delete the old flat
   files. Run tests — they must pass before proceeding. No new methods, pure
   move.
2. **Step 1 — Base layer.** Complete `RPModelElement` and `RPUnit` in
   `_core.py`. Enumerate every method from `IRPModelElement.html` and
   `IRPUnit.html`, implement each with a docstring sourced from the Java
   docs, add one test per method to `test_core.py`. Grow `fakes.py` as needed.
3. **Step 2 — Mid layer.** Complete `RPClassifier`, `RPClass`, `RPRelation`,
   `RPInstance` in their new `model_*.py` files. Enumerate methods from the
   Java docs, implement with docstrings, add tests. `RPRelation` is an audit
   pass; the others get substantial new methods.
4. **Step 3 — Containment layer.** Complete `RPPackage` and `RPProject`. Add
   `RPProfile`, `RPComponent`, `RPConfiguration`, `RPModule`, `RPNode`,
   `RPCollaboration`, `RPComponentInstance`. Each gets its own `model_*.py`
   file and test file.
5. **Step 4 — Leaf wrappers.** Add `RPGeneralization`, `RPDependency`,
   `RPHyperLink`, `RPEnumerationLiteral`, `RPComment`, `RPConstraint`,
   `RPTag`, `RPStereotype`, `RPAssociationClass`, `RPAssociationRole`. Group
   by inheritance parent for efficient testing.
6. **Step 5 — Integration tests.** Cross-wrapper tests:
   `RPModelElement.getStereotypes()` returns `RPCollection[RPStereotype]`,
   `RPClassifier.addGeneralization()` returns `RPGeneralization`,
   `RPProject.addProfile()` returns `RPProfile`, etc.
7. **Step 6 — Audit.** Run `ruff`, `black`, `mypy --strict`, `pytest`. Fix
   all findings. Verify coverage ≥ 80% (target 90%+). Verify every wrapper
   file has its checklist comment fully checked off.

## Testing Strategy

1. **One test per method.** Each public method gets at least one test
   verifying it calls the right COM method/property with the right args and
   returns/wraps the result correctly.
2. **Fakes in `tests/unit/models/fakes.py`.** `make_fake_element`,
   `make_fake_collection`, `make_com_error` already exist. Grow with helpers
   as needed (`make_fake_owner`, `make_fake_stereotype`, `make_fake_project`),
   but prefer reusing `make_fake_element` with configured attributes.
3. **No real COM in tests.** Tests run on any platform (Windows or not)
   because they use fakes. The `pywintypes` import guard in `_core.py`
   ensures the module imports cleanly on non-Windows.
4. **New test files:** `test_generalization.py`, `test_dependency.py`,
   `test_hyperlink.py`, `test_enumeration_literal.py`, `test_comment.py`,
   `test_constraint.py` (these three may share `test_misc.py`),
   `test_tag.py`, `test_stereotype.py`, `test_association_class.py`,
   `test_association_role.py`, `test_profile.py`, `test_component.py`,
   `test_configuration.py`, `test_module.py`, `test_node.py`,
   `test_collaboration.py`, `test_component_instance.py`.
5. **Integration tests** (Step 5) verify cross-wrapper behavior: factory
   methods return the correct subclass, collections contain wrapped items,
   navigation methods traverse correctly.
6. **Coverage target:** 80% minimum, 90%+ preferred. Enforced in CI.

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| COM Prog ID (`Rhapsody2.Application.1`) does not expose some Java API methods | Methods defined but raise `NotImplementedError` | Acceptable; documented in method docstring under `Raises:`. Rare. |
| Metaclass strings do not match Java interface names (e.g., COM returns `"Hyperlink"` not `"HyperLink"`) | `wrap()` falls back to `RPModelElement` instead of the specific subclass | Best-effort registration now; runtime discovery (deferred) confirms and corrects. Non-blocking — fallback still works. |
| `IRPModelElement.html` / `IRPUnit.html` / `IRPPackage.html` / `IRPProject.html` are large (exceed token limits) | Hard to read in one pass | Implementation reads them in chunks (line-offset ranges) or uses an agent with the Explore subagent type to extract method lists. |
| `IRPConfiguration`, `IRPNode`, `RPCollaboration` parent interfaces unknown | Python class placed under wrong parent | Implementation reads the HTML `extends` clause first, places class accordingly. If parent is an interface not yet wrapped, either wrap it too (if in scope) or use the closest wrapped ancestor and note the deviation. |
| OSLC inner classes (`OSLCLink`, `OSLCLink.Types`) need Python modeling | Adds scope | Model as a small dataclass + `Enum` in `_core.py` or a new `_enums.py`. If the COM API does not expose OSLC cleanly, methods raise `NotImplementedError` with a TODO. |
| Large method count (~100 on `RPModelElement`, ~50+ on others) | Long implementation, risk of shallow tests | Checklist comments track progress; one test per method is the minimum bar; integration tests catch wiring issues. Accept that this iteration is large. |
| Docstring sourcing from HTML is tedious | Slows implementation | Mechanical extraction; an agent can read the HTML method-detail section and emit docstring text. Consistent HTML structure makes this reliable. |

## Success Criteria

- All 8 existing wrappers reach full method parity with their Java
  interfaces (verified by the checklist comment in each file being fully
  checked off).
- All 17 new wrappers are implemented, registered, and tested.
- The hybrid file-layout refactor is complete; all existing import paths
  still work.
- Every public method carries a docstring sourced from the Java API docs.
- `ruff check src/ tests/`, `black --check src/ tests/`,
  `mypy src/ tests/`, and `pytest` all pass.
- Test coverage ≥ 80% (target 90%+).
