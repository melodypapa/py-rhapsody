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

`src/rhapsody_cli/models/elements/` is reorganized into one module per
inheritance family (not one class per file). Each module contains every
wrapper class in that family, ordered base-class-first; the top-level
`elements/__init__.py` imports each module (for `register_wrapper`
side effects).

```
models/
  _core.py                 # RPModelElement, RPUnit, RPCollection (unchanged location)
  elements/
    __init__.py            # imports every module below
    classifiers.py          # RPClassifier(RPUnit), RPClass(RPClassifier),
                             # RPActor(RPClassifier), RPUseCase(RPClassifier),
                             # RPInterfaceItem(RPClassifier) [NEW],
                             # RPOperation(RPInterfaceItem),
                             # RPStatechart(RPClass)
    variables.py             # RPVariable(RPUnit) [NEW], RPAttribute(RPVariable)
    containment.py            # RPPackage(RPUnit), RPProject(RPPackage)
    requirements.py             # RPAnnotation(RPUnit) [NEW], RPRequirement(RPAnnotation)
    relations.py                 # RPRelation(RPUnit) [NEW], RPInstance(RPRelation)
    diagrams.py                   # RPDiagram(RPUnit)
```

Future sub-projects add new classes into these same modules (e.g.
`classifiers.py` gains state-machine-adjacent types) or introduce new
modules (`statemachine.py`, `structure.py`, `relationships.py` for the
broader relationship set beyond `RPRelation`/`RPInstance`). If a module
grows too large to hold in context comfortably, it can be split at that
point — not preemptively.

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
- Docstrings are sourced from the java_api HTML docs: each method's
  docstring is the corresponding method's description text from its
  `IRPxxx.html` page (cleaned of HTML markup), not a freely-invented
  summary. This keeps the Python API's documentation traceable to the
  authoritative Java API reference. Class-level docstrings likewise draw
  from each interface's top-of-page description where one exists.
- Docstrings are written in **Google style** (`Args:`, `Returns:`,
  `Raises:` sections), so that a future Sphinx + `napoleon` + ReadTheDocs
  setup can autodoc them without reformatting. Each method's Java
  parameter/return descriptions (from the java_api docs) are mapped into
  `Args:`/`Returns:` entries; a summary line comes first, matching
  standard Google docstring structure. This formatting convention applies
  retroactively to the existing 12 wrappers' docstrings during this pass,
  not just the new methods being added.

Given the volume (~590 declared methods across the 16 interfaces
involved), implementation is split into multiple phases in the
implementation plan — grouped by interface or small interface clusters —
rather than attempted as one single change.

### Testing

- TDD as usual: write/extend fake COM objects in `tests/fakes.py` and
  failing unit tests before implementing each method.
- Existing tests for the 12 wrappers are updated for new import paths
  (module moves/renames) and extended for new methods/hierarchy. Test
  files remain per-class (e.g. `test_class.py`, `test_actor.py`) even
  though the corresponding implementation classes now share a module —
  test granularity doesn't need to match implementation file grouping.
- New test modules for the 4 new intermediate wrapper classes
  (`RPVariable`, `RPInterfaceItem`, `RPAnnotation`, `RPRelation`).
- `wrap()` registry/dispatch tests extended to cover the new classes.

## Deliverables

- 4 new wrapper classes: `RPVariable`, `RPInterfaceItem`, `RPAnnotation`,
  `RPRelation`.
- 12 existing wrappers corrected (hierarchy + full method parity).
- `elements/` reorganized into 6 modules (one per inheritance family) as
  above.
- All existing tests passing; new tests for new classes/methods.
- `ruff`, `black`, `mypy`, `pytest` all clean.
- All docstrings (existing and new) in Google style, sourced from
  java_api content, ready for a future Sphinx/ReadTheDocs setup (that
  setup itself is not part of this sub-project).

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
