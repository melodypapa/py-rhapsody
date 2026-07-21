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

### Problem Discovered

During round 3 completion, a critical design issue was discovered in methods that can return "not found" results:

```python
# Current implementation (PROBLEMATIC):
def find_nested_element(self, name: str, meta_class: str) -> RPModelElement:
    """Returns the wrapped matching model element."""
    return AbstractRPModelElement.wrap(AbstractRPModelElement.call_com(...))
    # Returns RPModelElement(None) if not found
    # BUT: Users must access private _com to check if it's null!
```

**The issue:** When COM returns `None` (element not found), we wrap it as `RPModelElement(None)`. But `_com` is a private implementation detail. Users have no public way to know if the returned element is valid or null.

### Current Workaround (Broken)

```python
# Users forced to do this (accessing private implementation):
element = package.find_nested_element("Foo", "Class")
if element._com is None:  # ❌ Private implementation detail!
    print("Not found")
```

### Solution: Use Optional[SpecificType]

**Recommended approach:** Return `Optional[SpecificType]` for any method that can return "not found". Since `AbstractRPModelElement.wrap()` dispatches COM objects to their specific wrapper classes (not just `RPModelElement`), search methods can return specific types:

```python
# CORRECT implementation:
def find_nested_element(self, name: str, meta_class: str) -> Optional["RPModelElement"]:
    """Returns the wrapped matching model element, or None if not found."""
    com_result = AbstractRPModelElement.call_com(lambda: self._com.findNestedElement(name, meta_class))
    if com_result is None:
        return None  # Explicit None
    return AbstractRPModelElement.wrap(com_result)
    # Returns specific wrapper (RPClass, RPPackage, etc.) or None
```

**Why this is better:**
1. ✅ **Pythonic**: Follows standard Python None handling patterns
2. ✅ **Type-safe**: Mypy enforces `if element is None` checks
3. ✅ **No private access**: Users never see `_com`
4. ✅ **Specific types**: Can return `RPClass`, `RPPackage`, etc., not just `RPModelElement`

### Methods Affected (Future Fix)

Search methods that should return `Optional`:
- `find_nested_element()` → `Optional[RPModelElement]`
- `find_nested_element_recursive()` → `Optional[RPModelElement]`
- `find_elements_by_full_name()` → `RPCollection` (already iterable, no None needed)
- Any similar "search" method in child classes

### Methods Unaffected

Methods that **always** return a valid element (or raise exception):
- `get_name()`, `get_meta_class()`, etc. → Stay as `str`, `RPModelElement`, etc.
- `add_*()` methods → Always return newly created element or raise
- Factory methods → Always return valid wrapper

### Implementation Strategy

**Phase 2 (post-round3):**
1. Identify all "search" methods that can return "not found"
2. Change return type from `RPModelElement` → `Optional[RPModelElement]`
3. Update `wrap()` logic: return `None` directly instead of `RPModelElement(None)`
4. Update all callers to handle `Optional` with `if element is None:` checks
5. Update tests to verify both found and not-found cases

### Example Usage After Fix

```python
# Clean, Pythonic code:
element = package.find_nested_element("Foo", "Class")
if element is None:
    print("Element not found")
else:
    print(f"Found: {element.get_name()}")

# With type checking:
found_element: Optional[RPModelElement] = package.find_nested_element("Foo", "Class")
if found_element is not None:
    name = found_element.get_name()  # Type checker knows it's valid here
```

---
