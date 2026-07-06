# rhapsody_cli: Python COM API for IBM Rhapsody — Design

## Problem

IBM Rhapsody exposes automation via a Windows COM API (backed by the same
`com.telelogic.rhapsody.core` interfaces documented in the Rhapsody Java API).
There is currently no Python package for accessing Rhapsody programmatically.
Engineers who already know the Rhapsody Java API (`IRPApplication`,
`IRPProject`, `IRPClass`, etc.) should be able to use an equivalent Python API
with minimal relearning.

## Goal

Provide `rhapsody_cli`, a Pythonic object-oriented wrapper around the Rhapsody
COM API that:

- Mirrors the Java API's class hierarchy and method names/signatures exactly
  (`getName()`, `setName()`, `getOperations()`, `addClass()`, etc.), so
  existing Rhapsody Java API knowledge and documentation transfer directly.
- Supports both read (navigation/inspection) and write (creation,
  modification, save, code generation) operations from v1.
- Establishes one consistent, generic architecture for wrapping any
  `IRPxxx` COM interface, fully implemented for a core set of ~15-20 common
  element types, with the remaining ~140+ Rhapsody element types addable
  later using the same mechanical pattern (new wrapper class + registry
  entry) without further architectural work.
- Is testable without a licensed Rhapsody installation, via mocked COM
  objects.

## Non-Goals (v1)

- Wrapping all ~160+ `IRPxxx` interfaces individually (only the core set
  below; others fall back to a generic wrapper — see "Wrapping Pattern").
- Design Manager / DOORS integration (`loginToDesignManager*`,
  `openProjectFromDesignManager*`) — these are deprecated in the Java API
  itself (removed in Rhapsody 8.4) and are out of scope.
- Cross-platform support — Rhapsody COM is Windows-only; this library
  targets Windows with `pywin32`.
- A GUI or CLI tool — this is a library only.

## Architecture

### Package name

Importable package: `rhapsody_cli` (distinct from the repo name `rhapsody-cli`).

### Connection layer (`rhapsody_cli/application.py`)

`RhapsodyApplication` wraps the top-level `IRPApplication` COM object
(not an `IRPModelElement`, so it is modeled separately from the element
hierarchy).

- `RhapsodyApplication.attach()` — attaches to an already-running Rhapsody
  instance via `win32com.client.GetActiveObject("Rhapsody.Application")`.
  Raises `RhapsodyConnectionError` if no instance is running.
- `RhapsodyApplication.launch()` — starts a new Rhapsody instance via
  `win32com.client.Dispatch("Rhapsody.Application")`.
- `RhapsodyApplication.connect(prefer_attach: bool = True)` — convenience
  entry point: tries `attach()` first (if `prefer_attach`), falls back to
  `launch()` on failure. This is the primary way most users will start.
- No global singleton: each `RhapsodyApplication` instance wraps one COM
  object independently, so multiple simultaneous Rhapsody instances/models
  can be managed side by side in the same process.
- Exposes Java-mirrored methods: `openProject(filename)`,
  `activeProject()`, `getProjects()`, `quit()`, etc.

### Wrapping pattern (`rhapsody_cli/_core.py`)

- Every wrapper class stores exactly one attribute, `_com`, holding the
  raw COM object it wraps. All method calls delegate to `self._com`.
- A central factory function `wrap(com_obj)` inspects the underlying
  Rhapsody element's runtime type and returns the correct Python wrapper
  instance (e.g., a COM object representing an `IRPClass` is wrapped as
  `RPClass`).
- Type resolution is driven by a registry dict mapping Rhapsody type names
  to wrapper classes, e.g. `{"Class": RPClass, "Package": RPPackage, ...}`.
  Adding support for a new Rhapsody element type is purely mechanical:
  define one wrapper class + one registry entry — no changes to `wrap()`
  itself.
- Any COM object whose type is not yet in the registry is wrapped as a
  generic `RPModelElement` (or `RPUnit`, if it exposes unit-like behavior)
  instead of raising an error. This guarantees `wrap()` never crashes on
  an unmapped type and lets navigation code keep working even for element
  types that don't yet have a dedicated wrapper class.
- `IRPCollection` results are wrapped as `RPCollection`, which implements
  `__len__`, `__getitem__`, and `__iter__` over the underlying collection
  (each item auto-wrapped via `wrap()`), in addition to mirrored Java
  methods (`getCount()`, `getItem(index)`, `addItem(element)`, etc.).

### Class hierarchy

Mirrors the Java API interface hierarchy:

```
RPModelElement            (wraps IRPModelElement — base for all model elements)
 └─ RPUnit                (wraps IRPUnit — elements that can be saved as files)
     ├─ RPProject         (wraps IRPProject)
     ├─ RPPackage         (wraps IRPPackage)
     ├─ RPClassifier      (wraps IRPClassifier)
     │    ├─ RPClass      (wraps IRPClass)
     │    ├─ RPActor      (wraps IRPActor)
     │    └─ RPUseCase    (wraps IRPUseCase)
     ├─ RPAttribute       (wraps IRPAttribute)
     ├─ RPOperation       (wraps IRPOperation)
     ├─ RPStatechart      (wraps IRPStatechart)
     ├─ RPRequirement     (wraps IRPRequirement)
     ├─ RPInstance        (wraps IRPInstance — model objects/instances)
     └─ RPDiagram         (wraps IRPDiagram, base for diagram types)

RPApplication              (wraps IRPApplication — top-level, not an IRPModelElement)
RPCollection               (wraps IRPCollection — iterable/indexable container)
```

Initial concrete wrapper set (~15-20 types): `RPApplication`, `RPProject`,
`RPPackage`, `RPClassifier`, `RPClass`, `RPActor`, `RPUseCase`,
`RPAttribute`, `RPOperation`, `RPInstance`, `RPStatechart`,
`RPRequirement`, `RPDiagram`, `RPModelElement`, `RPUnit`, `RPCollection`.

All other Rhapsody element types (e.g., `IRPStateVertex`, `IRPTransition`,
`IRPPort`, `IRPComponent`, and 140+ others) are addressed later by adding
wrapper classes following the identical pattern; they are not blocked by
this design.

### Method naming convention

Method names and signatures mirror the Java API exactly:

- `getName()` / `setName(name)` — not Pythonic `.name` properties.
- `getOperations()`, `getAttributes()`, `getPackage()` — navigation
  getters return wrapped elements or `RPCollection`.
- Creation methods mirror Java: `addClass(name)`, `addNewAggr(metaType,
  name)`, `addAttribute(...)`, `addOperation(...)`, etc.
- Java `String`/`int`/`boolean` parameters and returns map to native
  Python `str`/`int`/`bool`. Java `IRPXxx` return values are auto-wrapped
  via `wrap()`. Java `IRPCollection` returns become `RPCollection`.

### Write support (v1)

v1 includes both read and write operations:

- Creation methods (`addClass`, `addNewAggr`, `addAttribute`,
  `addOperation`, etc.) following Java signatures.
- Property setters (`setName`, etc.).
- Persistence: `save()` / `saveAll()` on `RPProject`/`RPUnit`.
- Code generation triggers (e.g., `generateCode()` equivalents on
  `RPClass`/configuration-related wrappers), passed through to COM.

### Error handling (`rhapsody_cli/exceptions.py`)

- `RhapsodyConnectionError` — raised when `attach()`/`connect()` cannot
  find or start a Rhapsody instance.
- `RhapsodyRuntimeException` — mirrors the Java API's exception of the
  same name. Raised by wrapper methods when the underlying COM call
  raises `pywintypes.com_error`; the original message/HRESULT is
  preserved in the exception for diagnostics.
- All wrapper method calls funnel COM errors through a shared helper that
  performs this translation consistently, so callers never see raw
  `pywintypes.com_error`.

### Testing strategy

- Pure `unittest.mock.MagicMock`-based fake COM objects — no real
  Rhapsody installation or license required; tests run anywhere/CI.
- `tests/fakes.py` provides helpers to build fake COM object graphs
  (e.g., a fake project containing fake packages containing fake classes)
  with configurable type names, so `wrap()`'s dispatch logic can be
  exercised for both known and unknown/unmapped types.
- Coverage focuses on: `wrap()` dispatch and fallback behavior,
  `RPCollection` iteration/indexing, method delegation and naming
  fidelity for each core wrapper class, and COM-error-to-
  `RhapsodyRuntimeException` translation.

### Package layout

```
rhapsody_cli/
  __init__.py
  application.py      # RhapsodyApplication: connect/launch/attach
  _core.py            # wrap() factory, registry, RPModelElement, RPUnit, RPCollection
  elements/
    project.py         # RPProject
    package.py         # RPPackage
    classifier.py       # RPClassifier
    class_.py           # RPClass
    attribute.py        # RPAttribute
    operation.py        # RPOperation
    actor.py             # RPActor
    usecase.py           # RPUseCase
    instance.py          # RPInstance
    statechart.py        # RPStatechart
    requirement.py       # RPRequirement
    diagram.py           # RPDiagram
  exceptions.py        # RhapsodyConnectionError, RhapsodyRuntimeException
tests/
  fakes.py
  test_application.py
  test_wrap.py
  test_class.py
  test_project.py
  test_collection.py
  ...
```

## Dependencies

- `pywin32` (`win32com.client`) — Windows COM automation.
- Python 3.9+ (matches repo's stated "Python 3" support).

## Open Items for Future Iterations (explicitly out of scope for v1 plan)

- Expanding wrapper coverage beyond the core ~15-20 types to the full
  ~160+ `IRPxxx` interface set, following the established registry
  pattern.
- Packaging/publishing to PyPI.
- Higher-level convenience helpers (e.g., batch code-gen across multiple
  projects) built on top of the core wrappers.
