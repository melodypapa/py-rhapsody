# RPInstance Wrapper Registry MetaClass Decision

**Date:** 2026-07-20
**Author:** Investigation via Claude Code
**Status:** Approved

## Overview

This document records the investigation and decision regarding whether `RPInstance` should be registered with metaClass name `"Object"` or `"Instance"` in the wrapper registry.

## Question

Should `RPInstance` be registered as:
- `AbstractRPModelElement.register_wrapper("Object", RPInstance)` (incorrect)
- `AbstractRPModelElement.register_wrapper("Instance", RPInstance)` (correct)

## Investigation Findings

### 1. Current Implementation (Correct)

**Location:** `src/rhapsody_cli/models/elements/relations/model_instance.py:224`

```python
AbstractRPModelElement.register_wrapper("Instance", RPInstance)
```

This registration is **correct** and should **not** be changed.

### 2. Java API Naming Convention

**Source:** `docs/java_api/com/telelogic/rhapsody/core/IRPModelElement.html:1876`

The Java API documentation states:

> For example, for an object of type `IRPStereotype`, the string "Stereotype" will be returned.

**Pattern:** `getMetaClass()` returns the interface name without the "IRP" prefix.

Therefore:
- `IRPInstance` → `"Instance"`
- `IRPStereotype` → `"Stereotype"`
- `IRPClass` → `"Class"`
- etc.

### 3. Java API Interface Hierarchy

**Source:** `docs/java_api/com/telelogic/rhapsody/core/IRPInstance.html:95-102`

```java
public interface IRPInstance extends IRPRelation
```

`IRPInstance` extends `IRPRelation`, not any "Object" interface. There is no "IRPObject" interface in the Rhapsody Java API.

### 4. Existing "Object" Registrations (Unrelated)

The only "Object" registrations in the codebase are for unrelated element types:

```python
# Activity nodes (not instances)
AbstractRPModelElement.register_wrapper("ObjectNode", RPObjectNode)

# Diagrams (not instances)
AbstractRPModelElement.register_wrapper("ObjectModelDiagram", RPObjectModelDiagram)
```

These are separate element types, not related to `IRPInstance`.

## Decision

**DO NOT** add `AbstractRPModelElement.register_wrapper("Object", RPInstance)`.

The current registration with `"Instance"` is correct based on:

1. **Java API convention** — `getMetaClass()` returns interface name without "IRP" prefix
2. **Interface hierarchy** — `IRPInstance` has no relationship to an "Object" interface
3. **Consistency** — All other wrappers follow the same naming pattern
4. **No evidence** — No documentation or code suggests "Object" is used for Instance elements

## Implementation Status

**Status:** ✅ Already correctly implemented

No changes needed. The wrapper registry correctly maps metaClass name `"Instance"` to the `RPInstance` class at `model_instance.py:224`.

## References

- `src/rhapsody_cli/models/elements/relations/model_instance.py` — RPInstance implementation and registration
- `docs/java_api/com/telelogic/rhapsody/core/IRPInstance.html` — Java API documentation
- `docs/java_api/com/telelogic/rhapsody/core/IRPModelElement.html` — getMetaClass() documentation
