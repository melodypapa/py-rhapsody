# Audit & Reorganize Core Wrappers Against the Rhapsody Java API — Design

## Problem

The 2026-07-06 design established `rhapsody_cli`'s wrapping pattern and an
initial set of 12 concrete wrapper classes (`RPClass`, `RPClassifier`,
`RPActor`, `RPUseCase`, `RPAttribute`, `RPOperation`, `RPProject`,
`RPPackage`, `RPRequirement`, `RPStatechart`, `RPDiagram`, `RPInstance`),
each intended to mirror the corresponding `IRPxxx` interface from
`com.telelogic.rhapsody.core` (documented in the Rhapsody Java API at
`C:\LegacyApp\Rhapsody_902_64bit\Doc\java_api`).

Comparing the current implementation against the actual java_api docs
reveals the class hierarchy has drifted from the real Java interface
hierarchy. Six of the twelve wrappers extend `RPUnit` directly, but their
Java counterparts extend an intermediate interface:

```
IRPModelElement
 └─ IRPUnit
      ├─ IRPPackage       → IRPProject
      ├─ IRPClassifier    → IRPClass    → IRPStatechart
      │                   → IRPActor
      │                   → IRPUseCase
      │                   → IRPInterfaceItem → IRPOperation
      ├─ IRPVariable      → IRPAttribute
      ├─ IRPAnnotation    → IRPRequirement
      ├─ IRPRelation      → IRPInstance
      └─ IRPDiagram
```

Four intermediate interfaces (`IRPVariable`, `IRPInterfaceItem`,
`IRPAnnotation`, `IRPRelation`) have no wrapper today, so their methods are
either missing or incorrectly duplicated onto the leaf classes. Getting
this foundation right matters because every future wrapper (state
machine, SysML structure, diagrams, relationships — later sub-projects)
will build on the same base classes; hierarchy bugs here would propagate
outward.

This is the first of several planned sub-projects auditing/expanding
`rhapsody_cli`'s coverage of the Java API. Later sub-projects (tracked
separately, not part of this spec) will add: State Machine elements
(`IRPState`, `IRPTransition`, ...), SysML structural elements (`IRPPort`,
`IRPComponent`, ...), diagram-specific types (`IRPActivityDiagram`,
`IRPSequenceDiagram`, ...), and relationship types (`IRPAssociation`,
`IRPDependency`, ...).

## Goal

1. **Fix the hierarchy**: introduce wrapper classes for the four missing
   intermediate interfaces (`RPVariable`, `RPInterfaceItem`,
   `RPAnnotation`, `RPRelation`) and re-parent the six affected leaf
   wrappers to extend them, matching the Java API exactly.
2. **Full method parity**: bring all 12 existing wrappers (plus the 4 new
   intermediate ones) to full parity with every method declared on their
   corresponding Java interface — not just the methods currently
   implemented.
3. **Reorganize for maintainability**: split the flat `elements/` folder
   into logical subpackages, in preparation for the much larger set of
   classes later sub-projects will add.

## Non-Goals (this sub-project)

- State Machine, SysML structure, diagram-detail, and relationship
  interfaces beyond `IRPDiagram`/`IRPRelation`/`IRPInstance` themselves —
  these are separate future sub-projects.
- Automated HTML-doc parsing tooling — interfaces are reviewed manually
  against the java_api docs for this pass.
- Changes to `RPModelElement`/`RPUnit`/`RPCollection` in `_core.py` beyond
  what's needed to support correct subclassing (they stay in `_core.py`).

## Architecture

### Package reorganization

`src/rhapsody_cli/models/elements/` is split into subpackages by
inheritance family. Each subpackage has an `__init__.py` re-exporting its
wrapper classes (for `register_wrapper` side effects); the top-level
`elements/__init__.py` imports each subpackage.

```
models/
  _core.py                 # RPModelElement, RPUnit, RPCollection (unchanged location)
  elements/
    __init__.py            # imports every subpackage below
    classifiers/
      __init__.py
      classifier.py         # RPClassifier(RPUnit)
      class_.py             # RPClass(RPClassifier)
      actor.py               # RPActor(RPClassifier)
      usecase.py             # RPUseCase(RPClassifier)
      interface_item.py      # RPInterfaceItem(RPClassifier)  [NEW]
      operation.py           # RPOperation(RPInterfaceItem)
      statechart.py           # RPStatechart(RPClass)
    variables/
      __init__.py
      variable.py             # RPVariable(RPUnit)  [NEW]
      attribute.py             # RPAttribute(RPVariable)
    containment/
      __init__.py
      package.py               # RPPackage(RPUnit)
      project.py               # RPProject(RPPackage)
    requirements/
      __init__.py
      annotation.py             # RPAnnotation(RPUnit)  [NEW]
      requirement.py             # RPRequirement(RPAnnotation)
    relations/
      __init__.py
      relation.py                 # RPRelation(RPUnit)  [NEW]
      instance.py                  # RPInstance(RPRelation)
    diagrams/
      __init__.py
      diagram.py                   # RPDiagram(RPUnit)
```

Future sub-projects add new files into these same subpackages (e.g.
`classifiers/` gains state-machine-adjacent types) or introduce new ones
(`statemachine/`, `structure/`, `relationships/` for the broader
relationship set beyond `RPRelation`/`RPInstance`).

### Hierarchy corrections

| Wrapper | Current base | Corrected base |
|---|---|---|
| `RPAttribute` | `RPUnit` | `RPVariable` (new) |
| `RPOperation` | `RPUnit` | `RPInterfaceItem` (new) |
| `RPProject` | `RPUnit` | `RPPackage` |
| `RPRequirement` | `RPUnit` | `RPAnnotation` (new) |
| `RPStatechart` | `RPUnit` | `RPClass` |
| `RPInstance` | `RPUnit` | `RPRelation` (new) |

`RPClassifier`, `RPClass`, `RPActor`, `RPUseCase`, `RPPackage`, `RPDiagram`
already extend the correct base (`RPUnit`, `RPClassifier`, or `RPUnit`
respectively) — no change needed there, only method-parity additions.

### Method parity

Each wrapper (existing 12 + 4 new intermediates) is extended so every
method declared on its corresponding Java interface (per the java_api
docs) is implemented, following the existing conventions:

- Method names/signatures mirror Java exactly (`getName()`,
  `setIsStatic(bool)`, etc.).
- COM calls go through `call_com(...)`.
- Property-vs-method COM access differences go through
  `_get_method_or_property`/`_set_method_or_property` where applicable.
- Methods returning `IRPxxx` wrap the result via `wrap()`; methods
  returning `IRPCollection` wrap via `RPCollection`.
- Only methods *declared on that specific interface* are added to that
  wrapper (inherited methods are provided by the corrected base class,
  not duplicated).

Given the volume (~590 declared methods across the 16 interfaces
involved), implementation is split into multiple phases in the
implementation plan — grouped by interface or small interface clusters —
rather than attempted as one single change.

### Testing

- TDD as usual: write/extend fake COM objects in `tests/fakes.py` and
  failing unit tests before implementing each method.
- Existing tests for the 12 wrappers are updated for new import paths
  (subpackage moves) and extended for new methods/hierarchy.
- New test modules for the 4 new intermediate wrapper classes
  (`RPVariable`, `RPInterfaceItem`, `RPAnnotation`, `RPRelation`), mirroring
  the existing per-class test file convention.
- `wrap()` registry/dispatch tests extended to cover the new classes.

## Deliverables

- 4 new wrapper classes: `RPVariable`, `RPInterfaceItem`, `RPAnnotation`,
  `RPRelation`.
- 12 existing wrappers corrected (hierarchy + full method parity).
- `elements/` reorganized into 6 subpackages as above.
- All existing tests passing; new tests for new classes/methods.
- `ruff`, `black`, `mypy`, `pytest` all clean.

## Open Items for Future Sub-Projects (explicitly out of scope here)

- State Machine elements (`IRPState`, `IRPTransition`, `IRPStateVertex`,
  `IRPEvent`, ...).
- SysML structural elements (`IRPPort`, `IRPComponent`,
  `IRPInterfaceItem`'s structural cousins, ...).
- Diagram-specific types beyond the base `IRPDiagram`
  (`IRPActivityDiagram`, `IRPSequenceDiagram`, `IRPObjectModelDiagram`,
  ...).
- Relationship types beyond `IRPRelation`/`IRPInstance`
  (`IRPAssociation`, `IRPDependency`, `IRPLink`, ...).
- Full parity for the remaining ~140+ `IRPxxx` interfaces not addressed
  by this sub-project or the categories above.
