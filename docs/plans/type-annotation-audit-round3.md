# Type Annotation Audit — Round 3: All Remaining Wrapper Classes

After rounds 1-2 (RPModelElement + 9 imported classes), ~75 wrapper classes remain unchecked. This plan covers them all.

## Method

Same as rounds 1-2:
1. Open Java API HTML doc for the interface (e.g., `IRPClass.html`)
2. Compare each method's Python signature against the Java declaration
3. Fix return types: `IRP*` → specific Python wrapper (e.g., `IRPClassifier` → `RPClassifier`)
4. Fix param types: drop `Any`, use specific wrappers
5. Add `cast()` returns where `wrap()` returns `RPModelElement`
6. Add `TYPE_CHECKING` imports for wrapper types used only in annotations
7. Run `ruff check` + `black --check` + `mypy` on changed files + `pytest tests/unit/`

## Subpackages Order (fewest methods first)

### 1. `classifiers/` — 3 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| `RPException` | `RPModelElement` | 0 | IRPException — empty interface |
| **`RPUseCase`** | `RPClassifier` | 2 | IRPUseCase |
| **`RPActor`** | `RPClassifier` | 2 | IRPActor |
| **`RPInterfaceItem`** | `RPClassifier` | 2 | IRPInterfaceItem |
| **`RPOperation`** | `RPInterfaceItem` | 8 | IRPOperation |
| **`RPStatechart`** | `RPClass` | 10 | IRPStatechart |
| **`RPClass`** | `RPClassifier` | 14 | IRPClass |
| **`RPClassifier`** | `RPUnit` | 18 | IRPClassifier |

RPException is a no-op (0 direct methods, empty interface). Skip it.

### 2. `common/` — 3 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPEnumerationLiteral`** | `RPModelElement` | 0 | IRPEnumerationLiteral |
| **`RPComment`** | `RPModelElement` | 2 | IRPComment |
| **`RPConstraint`** | `RPModelElement` | 2 | IRPConstraint |
| **`RPClassifierRole`** | `RPModelElement` | 4 | IRPClassifierRole |
| **`RPSysMLPort`** | `RPInstance` | 2 | IRPSysMLPort |
| **`RPType`** | `RPClassifier` | 2 | IRPType |

RPEnumerationLiteral has 0 direct methods. Skip it.

### 3. `values/` — 3 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPInstanceSlot`** | `RPModelElement` | 4 | IRPInstanceSlot |
| **`RPInstanceSpecification`** | `RPModelElement` | 2 | IRPInstanceSpecification |
| `RPValueSpecification` | `RPModelElement` | 0 | IRPValueSpecification — empty interface |
| `RPInstanceValue` | `RPValueSpecification` | 0 | IRPInstanceValue — empty interface |
| `RPLiteralSpecification` | `RPValueSpecification` | 0 | IRPLiteralSpecification — empty interface |

RPValueSpecification, RPInstanceValue, RPLiteralSpecification have 0 direct methods. Skip them.

### 4. `requirements/` — 2 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPAnnotation`** | `RPUnit` | 6 | IRPAnnotation |
| **`RPRequirement`** | `RPAnnotation` | 4 | IRPRequirement |

### 5. `variables/` — 1 class with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| RPVariable | `RPUnit` | 10 | IRPVariable — already checked implicitly in round 2 (RPTag file) |
| **`RPAttribute`** | `RPVariable` | 11 | IRPAttribute |
| **`RPArgument`** | `RPVariable` | 2 | IRPArgument |

RPVariable has been partially checked (same file as RPTag, round 2). RPAttribute and RPArgument need full review.

### 6. `statemachine/` — 2 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPStateVertex`** | `RPModelElement` | 2 | IRPStateVertex |
| **`RPState`** | `RPStateVertex` | 14 | IRPState |

### 7. `relations/` — 4 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPInstance`** | `RPRelation` | 6 | IRPInstance |
| **`RPPort`** | `RPInstance` | 6 | IRPPort |
| **`RPGeneralization`** | `RPModelElement` | 6 | IRPGeneralization |
| **`RPHyperLink`** | `RPDependency` | 2 | IRPHyperLink |
| `RPAssociationRole` | `RPInstance` | 2 | IRPAssociationRole |

### 8. `diagrams/` — diagram types

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| RPDiagram | `RPUnit` | 20 | IRPDiagram — already partially checked in round 2 |

All 10 diagram type subclasses in `model_diagram_types.py` have 0 direct methods each (they only inherit from RPDiagram or each other). Skip all of them.

### 9. `activity/` — 5 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPFlow`** | `RPModelElement` | 12 | IRPFlow |
| **`RPFlowItem`** | `RPClassifier` | 2 | IRPFlowItem |
| **`RPFlowchart`** | `RPStatechart` | 2 | IRPFlowchart |
| **`RPObjectNode`** | `RPState` | 4 | IRPObjectNode |
| **`RPSwimlane`** | `RPModelElement` | 2 | IRPSwimlane |

### 10. `activity/` — action classes

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPAction`** | `RPModelElement` | 4 | IRPAction |
| `RPAcceptEventAction` | `RPState` | 0 | IRPAcceptEventAction |
| `RPAcceptTimeEvent` | `RPState` | 0 | IRPAcceptTimeEvent |
| **`RPCallOperation`** | `RPState` | 4 | IRPCallOperation |
| `RPActionBlock` | `RPMessage` | 0 | IRPActionBlock |
| `RPContextSpecification` | `RPValueSpecification` | 0 | IRPContextSpecification |
| **`RPSendAction`** | `RPAction` | 2 | IRPSendAction |

### 11. `interactions/` — 9 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPMessage`** | `RPModelElement` | 12 | IRPMessage |
| **`RPTransition`** | `RPModelElement` | 8 | IRPTransition |
| **`RPEvent`** | `RPInterfaceItem` | 2 | IRPEvent |
| **`RPTrigger`** | `RPModelElement` | 2 | IRPTrigger |
| **`RPGuard`** | `RPModelElement` | 2 | IRPGuard |
| **`RPExecutionOccurrence`** | `RPModelElement` | 0 | IRPExecutionOccurrence |
| **`RPInteractionOccurrence`** | `RPModelElement` | 4 | IRPInteractionOccurrence |
| **`RPInteractionOperand`** | `RPCollaboration` | 0 | IRPInteractionOperand |
| **`RPInteractionOperator`** | `RPModelElement` | 0 | IRPInteractionOperator |
| **`RPDestructionEvent`** | `RPMessage` | 0 | IRPDestructionEvent |
| **`RPEventReception`** | `RPInterfaceItem` | 0 | IRPEventReception |

### 12. `containment/` — 7 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPPackage`** | `RPUnit` | ~40 | IRPPackage — LARGE |
| **`RPComponent`** | `RPUnit` | 14 | IRPComponent |
| **`RPConfiguration`** | `RPUnit` | 14 | IRPConfiguration |
| **`RPCollaboration`** | `RPUnit` | 14 | IRPCollaboration |
| **`RPNode`** | `RPUnit` | 6 | IRPNode |
| **`RPComponentInstance`** | `RPInstance` | 2 | IRPComponentInstance |
| **`RPProfile`** | `RPPackage` | 0 | IRPProfile — shared from RPPackage |
| `RPModule` | `RPInstance` | 0 | IRPModule — empty/basic |

RPProfile and RPModule have 0 direct methods. Skip them.

### 13. `graphics/` — 10 classes with methods

| Class | Parent | Direct methods | Interface |
|-------|--------|---------------|-----------|
| **`RPGraphElement`** | `RPModelElement` | 10 | IRPGraphElement |
| **`RPGraphicalProperty`** | `RPModelElement` | 0 | IRPGraphicalProperty |
| **`RPGraphEdge`** | `RPGraphElement` | 0 | IRPGraphEdge |
| **`RPGraphNode`** | `RPGraphElement` | 0 | IRPGraphNode |
| **`RPPin`** | `RPConnector` | 2 | IRPPin |
| **`RPConnector`** | `RPStateVertex` | 2 | IRPConnector |
| **`RPImageMap`** | `RPModelElement` | 2 | IRPImageMap |
| **`RPConditionMark`** | `RPMessage` | 0 | IRPConditionMark |
| **`RPMatrixLayout`** | `RPUnit` | 4 | IRPMatrixLayout |
| **`RPMatrixView`** | `RPUnit` | 2 | IRPMatrixView |
| **`RPTableLayout`** | `RPUnit` | 8 | IRPTableLayout |
| **`RPTableView`** | `RPUnit` | 2 | IRPTableView |
| **`RPMessagePoint`** | `RPModelElement` | 0 | IRPMessagePoint |

Many graphics classes have 0 methods (RPGraphEdge, RPGraphNode, RPGraphicalProperty, RPConditionMark, RPMessagePoint). Skip them. The main ones are RPGraphElement, RPTableLayout, RPMatrixLayout, RPTableView, RPMatrixView, RPImageMap, RPConnector, RPPin.

### 14. `containment/` — RPProject re-audit

RPProject was "partially checked" in round 2. It has ~55 methods and needs a full systematic review. The round 2 audit found it has many `Any` params and potential signature mismatches. This is the largest single file.

## Recommended Execution Order

Work from smallest to largest for quick wins:

1. **common/** — 5 classes (Comment, Constraint, ClassifierRole, SysMLPort, Type)
2. **classifiers/small** — 4 classes (UseCase, Actor, InterfaceItem, Operation)
3. **variables/** — 2 classes (RPAttribute, RPArgument)
4. **statemachine/** — 2 classes (RPStateVertex, RPState)
5. **requirements/** — 2 classes (RPAnnotation, RPRequirement)
6. **relations/** — 5 classes (RPInstance, RPPort, RPGeneralization, RPHyperLink, RPAssociationRole)
7. **values/** — 1 class (RPInstanceSlot, RPInstanceSpecification)
8. **graphics/small** — 5 classes (RPImageMap, RPConnector, RPPin, RPMatrixLayout/View, RPTableView)
9. **activity/** — 5 classes (Flow, FlowItem, Flowchart, ObjectNode, Swimlane)
10. **activity/actions** — 3 classes (RPAction, RPCallOperation, RPSendAction)
11. **interactions/** — 5 classes (Message, Transition, Event, Trigger, Guard, InteractionOccurrence)
12. **classifiers/large** — 2 classes (RPClassifier, RPClass, RPStatechart)
13. **graphics/large** — 2 classes (RPGraphElement, RPTableLayout)
14. **containment/large** — 4 classes (RPPackage, RPComponent, RPConfiguration, RPCollaboration, RPNode, RPComponentInstance)
15. **containment/rpproject** — RPProject full re-audit

## Quality Gate After Each Subpackage

```bash
ruff check src/rhapsody_cli/models/elements/<subpackage>/
black --check src/rhapsody_cli/models/elements/<subpackage>/
mypy src/rhapsody_cli/models/elements/<subpackage>/
pytest tests/unit/ -q
```

## Known Pre-existing Issues (don't fix)

- `core.py` has ~16 `Incompatible return value type` errors from round 1 changes — these require test file fixes
- Test files across `tests/unit/` have `RPModelElement` → expected specific type errors — these are downstream of the source changes and will be cleaned separately
- Don't touch `docs/` or `tests/` unless a test directly fails because of a source change

---

## Design Decision: Optional Return Types for Search Methods

### Background: Java API Behavior

From `docs/java_api/com/telelogic/rhapsody/core/IRPModelElement.html`:

```
findNestedElement(String name, String metaClass)
  Returns: the model element that was specified
  Note: the element is always returned as an object of type IRPModelElement
```

**Key observation from Java docs:**
- Return type is `IRPModelElement` (non-null in Java signature)
- But in reality, COM/Java returns `null` when element not found
- Java allows null returns even though type signature shows non-null
- Users in Java must check `if (element == null)` to handle not-found case

### Current Python Implementation (WRONG)

Our current code attempts to match Java's non-Optional return type:

```python
def find_nested_element(self, name: str, meta_class: str) -> RPModelElement:
    """Returns the wrapped matching model element."""
    return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(...))
    # When COM returns None, we do: return RPModelElement(None)
    # Problem: Type annotation says "always RPModelElement"
    # But we're returning a wrapper with _com = None inside!
```

**The problem:**
- ❌ Type annotation promises `RPModelElement` (never None)
- ❌ But actual runtime: returns `RPModelElement(None)` when not found
- ❌ No public way to check if it's valid (must access private `_com`)
- ❌ Type checker thinks element is always usable

```python
# This type-checks as OK (type checker sees RPModelElement)
element = package.find_nested_element("NonExistent", "Class")
# But at runtime, element._com is None - accessing methods will crash!
name = element.get_name()  # ❌ Crash at runtime, but type checker didn't warn
```

### Solution: Add Optional to Match Runtime Behavior

**Core insight:** Even though Java API docs show `IRPModelElement` (non-null), the actual runtime behavior allows null. Python's `Optional` is the correct way to represent this truthfully.

```python
# CORRECT Python implementation:
def find_nested_element(self, name: str, meta_class: str) -> Optional["RPModelElement"]:
    """Returns the wrapped matching model element, or None if not found.
    
    Matches Java behavior where findNestedElement can return null when
    element not found, even though Java API signature shows IRPModelElement.
    """
    com_result = AbstractRPModelElement.call_com(lambda: self._com.findNestedElement(name, meta_class))
    if com_result is None:
        return None  # Explicit None - truthful to actual behavior
    return AbstractRPModelElement.wrap(com_result)
    # Returns specific wrapper (RPClass, RPPackage, etc.) or None
```

**Why this is correct:**
1. ✅ **Java API truthfulness**: Java API signature lies (says non-null, returns null). Python's Optional tells the truth.
2. ✅ **Type-safe**: Mypy ENFORCES `if element is None:` checks before using
3. ✅ **No private access**: Users never need to check `element._com`
4. ✅ **Specific types**: Returns `RPClass`, `RPPackage`, etc., not just `RPModelElement`
5. ✅ **Matches child class returns**: `wrap()` returns specific subclass, not base class

### How to Check Java API Docs

When auditing return types, follow this pattern:

```
STEP 1: Check Java API signature
  find_nested_element() -> IRPModelElement (appears non-null)

STEP 2: Read documentation/usage examples
  "Returns the model element that was specified"
  Search for: "null", "not found", "returns null", "no result"

STEP 3: Check COM behavior
  Does this method search/look up elements? (find, get_by_name, etc.)
  → YES → Can return null/None when not found → MUST be Optional

  Does this method create/return a new element? (add_*, create_*, etc.)
  → NO: Never Optional (always returns element or raises exception)

STEP 4: Add Optional to Python signature
  Java signature: IRPModelElement findNestedElement(...)
  Python signature: Optional[RPModelElement] find_nested_element(...)
  Implementation: return None if com_obj is None, else wrap(com_obj)
```

### Methods Affected (Phase 2 Implementation)

**Search/lookup methods that should return `Optional`:**
- `find_nested_element()` → `Optional[RPModelElement]`
- `find_nested_element_recursive()` → `Optional[RPModelElement]`
- `find_elements_by_full_name()` → Returns `RPCollection` (already handles empty)
- Any method with "find", "get_by_*", "lookup" pattern
- Check Java docs for each to confirm "can return null" behavior

**Methods that should STAY non-Optional:**
- `get_name()`, `get_meta_class()`, `get_guid()` → Always return value or throw
- `add_*()` methods → Always return newly created element or throw
- `get_all_*()` methods → Return collections (empty if none found)
- Constructor methods → Return new element or throw

### Implementation Strategy (Phase 2)

```
Phase 2: Optional Return Type Implementation

1. Audit all methods against Java API docs
   - Identify which can legitimately return "not found"/null
   - Mark as Optional[SpecificType] in signature
   
2. Update find_nested_element() and similar search methods
   - Change: -> RPModelElement to -> Optional[RPModelElement]
   - Update implementation to return None directly (not wrap None)
   
3. Update all callers
   - Anywhere find_nested_element() is called, add None checks
   - Type checker will enforce this (mypy will error if skipped)
   
4. Update tests
   - Test both "found" and "not found" cases
   - Verify Optional behavior matches expectations
   
5. Quality gate
   - mypy strict mode must pass
   - All tests pass
   - No accessing private _com attribute
```

### Example: Before vs After

**BEFORE (Current - Type Unsafe):**
```python
# Type annotation says never None, but actual return can be None!
element = package.find_nested_element("Foo", "Class")
# Type checker thinks element is always valid
name = element.get_name()  # ❌ CRASH if not found, but no type error
```

**AFTER (Phase 2 - Type Safe):**
```python
# Type annotation matches actual behavior
element = package.find_nested_element("Foo", "Class")
if element is None:  # ✅ Type checker REQUIRES this check
    print("Not found")
else:
    name = element.get_name()  # ✅ Type checker knows it's safe here
```

### Key Principle

> **When Java API docs show non-null but code can return null, Python's `Optional` is MORE TRUTHFUL than Java's signature.**

The Java API docs were written before nullable annotations existed. Python's `Optional` corrects this by explicitly encoding the actual runtime behavior.

---
