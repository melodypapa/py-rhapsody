# Group Model Classes into Domain Subpackages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the 13 flat `model_*.py` modules currently sitting directly in `src/rhapsody_cli/models/elements/` into domain subpackages (`diagrams/`, `graphics/`, `variables/`, `values/`, `statemachine/`, `activity/`, `interactions/`, `requirements/`, `templates/`, `common/`) so the package mirrors the existing `classifiers/`, `containment/`, `relations/` layout, with every import across `src/` and `tests/` updated and the full quality gate staying green.

**Architecture:** Pure package re-org. No class logic changes. Each flat module is `git mv`-ed into a new subpackage directory that mirrors the Rhapsody Java API domain grouping; the subpackage gains an `__init__.py` re-exporting its classes (mirroring the existing `classifiers/__init__.py` pattern); `elements/__init__.py` is updated to import the new subpackages; every absolute import `rhapsody_cli.models.elements.model_X` anywhere in `src/`/`tests/` is rewritten to `rhapsody_cli.models.elements.<subpkg>.model_X`. Registration side-effects (`register_wrapper` calls) remain intact because the modules are still imported via `elements/__init__.py`.

**Tech Stack:** Python 3.8+, git, pytest, ruff, black, mypy.

## Global Constraints

- TDD is mandatory — write/adjust tests before implementation; coverage target 80% min, 90%+ preferred. (Carried verbatim from project rules.)
- Do NOT use `from __future__ import annotations` — it is forbidden. Use string-quoted forward refs or `TYPE_CHECKING` imports.
- All constants use `SCREAMING_SNAKE_CASE`.
- `mypy` runs in strict mode; all functions need return type annotations.
- `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest` is the full quality gate.
- All changes go on a feature branch (e.g. `refactor/group-model-subpackages`); never commit directly to `main`.
- Commits are human-authored only; no AI co-author trailers.
- The wrapper registry must stay populated: `elements/__init__.py` must continue to import every moved module (directly or via its subpackage `__init__`) so `register_wrapper` fires when `rhapsody_cli` is imported.

---

## File Structure (Target Tree)

```
src/rhapsody_cli/models/elements/
├── __init__.py                     # updated imports (see below)
├── classifiers/                    # (already a subpackage — untouched)
├── containment/                    # (already a subpackage — untouched)
├── relations/                      # (already a subpackage — untouched)
├── diagrams/                       # NEW
│   ├── __init__.py
│   ├── model_diagrams.py           # (moved) RPDiagram
│   └── model_diagram_types.py      # (moved) RP*Diagram
├── graphics/                       # NEW
│   ├── __init__.py
│   └── model_graphics.py           # (moved) RPGraphElement, RPConnector, RPLink, ...
├── variables/                      # NEW
│   ├── __init__.py
│   └── model_variables.py          # (moved) RPVariable, RPAttribute, RPTag, RPArgument
├── values/                         # NEW
│   ├── __init__.py
│   └── model_values.py             # (moved) RPValueSpecification, RPInstanceSpecification, ...
├── statemachine/                   # NEW
│   ├── __init__.py
│   └── model_statemachine.py       # (moved) RPStateVertex, RPState
├── activity/                       # NEW
│   ├── __init__.py
│   ├── model_activity.py           # (moved) RPFlow, RPFlowItem, RPFlowchart, RPObjectNode, RPSwimlane
│   └── model_actions.py            # (moved) RPAction, RPAcceptEventAction, RPSendAction, ...
├── interactions/                   # NEW
│   ├── __init__.py
│   └── model_interactions.py       # (moved) RPMessage, RPTransition, RPEvent, ...
├── requirements/                   # NEW
│   ├── __init__.py
│   └── model_requirements.py       # (moved) RPAnnotation, RPRequirement
├── templates/                      # NEW
│   ├── __init__.py
│   └── model_templates.py          # (moved) RPTemplateInstantiation, ...
└── common/                         # NEW (catch-all helpers)
    ├── __init__.py
    ├── model_misc.py               # (moved) RPComment, RPConstraint, RPEnumerationLiteral
    └── model_other_model.py        # (moved) RPClassifierRole, RPSysMLPort, RPType
```

### `elements/__init__.py` target content

```python
"""Concrete Rhapsody element wrappers, registered with ``AbstractRPModelElement.wrap()``."""

from rhapsody_cli.models.elements import classifiers as classifiers  # noqa: F401
from rhapsody_cli.models.elements import common as common  # noqa: F401
from rhapsody_cli.models.elements import containment as containment  # noqa: F401
from rhapsody_cli.models.elements import diagrams as diagrams  # noqa: F401
from rhapsody_cli.models.elements import graphics as graphics  # noqa: F401
from rhapsody_cli.models.elements import interactions as interactions  # noqa: F401
from rhapsody_cli.models.elements import relations as relations  # noqa: F401
from rhapsody_cli.models.elements import requirements as requirements  # noqa: F401
from rhapsody_cli.models.elements import statemachine as statemachine  # noqa: F401
from rhapsody_cli.models.elements import activity as activity  # noqa: F401
from rhapsody_cli.models.elements import templates as templates  # noqa: F401
from rhapsody_cli.models.elements import values as values  # noqa: F401
from rhapsody_cli.models.elements import variables as variables  # noqa: F401
```

### Reusable import-rewrite command

For each moved module, rewrite every absolute reference `rhapsody_cli.models.elements.model_X` → `rhapsody_cli.models.elements.<subpkg>.model_X` across `src/` and `tests/`. Use this deterministic Python one-liner (Windows-safe; no GNU sed required):

```bash
python -c "import pathlib,re; old='rhapsody_cli.models.elements.MODEL'; new='rhapsody_cli.models.elements.SUBPKG.MODEL'; pat=re.compile(re.escape(old)); [ (p.write_text(pat.sub(new,p.read_text(encoding='utf-8'),0),encoding='utf-8'),print('updated',p)) for p in list(pathlib.Path('src').rglob('*.py'))+list(pathlib.Path('tests').rglob('*.py')) if pat.search(p.read_text(encoding='utf-8')) ]"
```

Replace `MODEL` with the module basename (e.g. `model_graphics`) and `SUBPKG` with the target subpackage (e.g. `graphics`). Run from repo root.

### Green-state rule (important)

When moving a subpackage, rewrite **outgoing** imports *inside the moved files* only for modules that are **already** in a subpackage (`classifiers`, `containment`, `relations`, or an earlier-moved subpackage). For outgoing imports to a flat module that has **not yet been moved**, leave the reference at its old path `rhapsody_cli.models.elements.model_Y` — it still resolves because that file has not moved yet. That module's own task will update the reference. This keeps the tree importable after every task.

Order tasks so `common/` is moved **last** (it is referenced widely as a flat module by many files); every earlier task leaves `elements.model_misc` / `elements.model_other_model` valid until the final task.

---

## Task 1: Move `diagrams` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_diagrams.py` → `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`
- Move: `src/rhapsody_cli/models/elements/model_diagram_types.py` → `src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py`
- Create: `src/rhapsody_cli/models/elements/diagrams/__init__.py`

**Interfaces:**
- Consumes: `RPClassifier` (classifiers), `RPCollaboration` (containment), `RPStatechart` (classifiers), `RPGraphElement`/`RPGraphNode` (graphics — not yet moved; keep old path), `RPFlowchart` (activity — not yet moved; keep old path)
- Produces: `RPDiagram`, `RP*Diagram` classes at `rhapsody_cli.models.elements.diagrams`

- [ ] **Step 1: git mv the two modules**

```bash
git mv src/rhapsody_cli/models/elements/model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git mv src/rhapsody_cli/models/elements/model_diagram_types.py src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py
```

- [ ] **Step 2: Create `diagrams/__init__.py`** with re-exports (mirror existing subpackage pattern)

```python
"""Diagrams package — wrappers for IRPDiagram and its subtypes."""

from rhapsody_cli.models.elements.diagrams.model_diagram_types import (  # noqa: F401
    RPActivityDiagram,
    RPCollaborationDiagram,
    RPComponentDiagram,
    RPDeploymentDiagram,
    RPObjectModelDiagram,
    RPPanelDiagram,
    RPSequenceDiagram,
    RPStatechartDiagram,
    RPStructureDiagram,
    RPTimingDiagram,
    RPUseCaseDiagram,
)
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram  # noqa: F401

__all__ = [
    "RPDiagram",
    "RPActivityDiagram",
    "RPCollaborationDiagram",
    "RPComponentDiagram",
    "RPDeploymentDiagram",
    "RPObjectModelDiagram",
    "RPPanelDiagram",
    "RPSequenceDiagram",
    "RPStatechartDiagram",
    "RPStructureDiagram",
    "RPTimingDiagram",
    "RPUseCaseDiagram",
]
```

- [ ] **Step 3: Rewrite references TO these modules across src + tests**

```bash
python -c "import pathlib,re; old='rhapsody_cli.models.elements.model_diagrams'; new='rhapsody_cli.models.elements.diagrams.model_diagrams'; pat=re.compile(re.escape(old)); [ (p.write_text(pat.sub(new,p.read_text(encoding='utf-8'),0),encoding='utf-8'),print('updated',p)) for p in list(pathlib.Path('src').rglob('*.py'))+list(pathlib.Path('tests').rglob('*.py')) if pat.search(p.read_text(encoding='utf-8')) ]"
python -c "import pathlib,re; old='rhapsody_cli.models.elements.model_diagram_types'; new='rhapsody_cli.models.elements.diagrams.model_diagram_types'; pat=re.compile(re.escape(old)); [ (p.write_text(pat.sub(new,p.read_text(encoding='utf-8'),0),encoding='utf-8'),print('updated',p)) for p in list(pathlib.Path('src').rglob('*.py'))+list(pathlib.Path('tests').rglob('*.py')) if pat.search(p.read_text(encoding='utf-8')) ]"
```

- [ ] **Step 4: Update `elements/__init__.py`** — replace the two lines:
`from rhapsody_cli.models.elements import model_diagram_types as diagram_types  # noqa: F401`
`from rhapsody_cli.models.elements import model_diagrams as diagrams  # noqa: F401`
with:
`from rhapsody_cli.models.elements import diagrams as diagrams  # noqa: F401`

- [ ] **Step 5: Run targeted tests**

```bash
pytest tests/unit/models/elements/test_diagram.py -v
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: move diagram model modules into diagrams/ subpackage"
```

---

## Task 2: Move `graphics` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_graphics.py` → `src/rhapsody_cli/models/elements/graphics/model_graphics.py`
- Create: `src/rhapsody_cli/models/elements/graphics/__init__.py`

**Interfaces:**
- Consumes: `RPClassifier` (classifiers), `RPDiagram` (now `diagrams`), `RPMessage` (interactions — not yet moved), `RPStateVertex` (statemachine — not yet moved), `RPState` (statemachine — not yet moved), `RPFlow`/`RPSwimlane` (activity — not yet moved), `RPInstance`/`RPPort`/`RPRelation` (relations), `RPCollaboration` (containment), `RPSysMLPort`/`RPLink`/`RPClassifierRole` (common — not yet moved)
- Produces: `RPGraphElement`, `RPConnector`, `RPLink`, `RPGraphNode`, `RPGraphEdge`, `RPPin`, `RPMatrixView`, `RPTableView`, `RPTableLayout`, `RPMatrixLayout`, `RPImageMap`, `RPMessagePoint`, `RPConditionMark`, `RPGraphicalProperty` at `...graphics`

- [ ] **Step 1: git mv**

```bash
git mv src/rhapsody_cli/models/elements/model_graphics.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
```

- [ ] **Step 2: Create `graphics/__init__.py`** (re-export the public classes listed in `model_graphics.py`)

- [ ] **Step 3: Rewrite outgoing import inside `model_graphics.py` to the already-moved `diagrams` module**

Replace `from rhapsody_cli.models.elements.model_diagrams import RPDiagram` with `from rhapsody_cli.models.elements.diagrams.model_diagrams import RPDiagram`. Leave references to not-yet-moved modules (`model_activity`, `model_interactions`, `model_statemachine`, `model_other_model`) at their old paths.

- [ ] **Step 4: Rewrite references TO `model_graphics` across src + tests** (use the reusable command with `MODEL=model_graphics`, `SUBPKG=graphics`). Note `tests/unit/models/test_integration.py` and `src/rhapsody_cli/models/support/model_codegen.py` reference it.

- [ ] **Step 5: Update `elements/__init__.py`** line `from rhapsody_cli.models.elements import model_graphics as graphics` → `from rhapsody_cli.models.elements import graphics as graphics`

- [ ] **Step 6: Run tests**

```bash
pytest tests/unit/models/elements/test_diagram.py tests/unit/models/test_integration.py -v
```
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "refactor: move graphics model module into graphics/ subpackage"
```

---

## Task 3: Move `variables` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_variables.py` → `src/rhapsody_cli/models/elements/variables/model_variables.py`
- Create: `src/rhapsody_cli/models/elements/variables/__init__.py`

**Interfaces:**
- Consumes: `RPUnit` (core), `RPValues` module (`model_values` — not yet moved; keep old path) for `RPInstanceSlot`/`RPInstanceValue`/`RPLiteralSpecification` used under `TYPE_CHECKING`.
- Produces: `RPVariable`, `RPAttribute`, `RPTag`, `RPArgument` at `...variables`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `variables/__init__.py`** re-exporting `RPVariable, RPAttribute, RPTag, RPArgument`
- [ ] **Step 3: Update `elements/__init__.py`** line → `from rhapsody_cli.models.elements import variables as variables`
- [ ] **Step 4: Rewrite references TO `model_variables`** (consumers include `classifiers/model_classifier.py`, `classifiers/model_interface_item.py`, `model_templates.py`, `tests/unit/models/elements/test_argument.py`, `test_attribute.py`, `test_tag.py`, `test_variable.py`, `tests/unit/models/test_integration.py`)
- [ ] **Step 5: Run tests `pytest tests/unit/models/elements/test_variable.py tests/unit/models/elements/test_attribute.py tests/unit/models/elements/test_tag.py tests/unit/models/elements/test_argument.py -v`** → PASS
- [ ] **Step 6: Commit**

---

## Task 4: Move `values` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_values.py` → `src/rhapsody_cli/models/elements/values/model_values.py`
- Create: `src/rhapsody_cli/models/elements/values/__init__.py`

**Interfaces:**
- Consumes: `RPModelElement` (core), `RPClassifier` (classifiers)
- Produces: `RPValueSpecification`, `RPInstanceSpecification`, `RPInstanceSlot`, `RPInstanceValue`, `RPLiteralSpecification` at `...values`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `values/__init__.py`** re-exporting the five classes
- [ ] **Step 3: Update `elements/__init__.py`** → `from rhapsody_cli.models.elements import values as values`
- [ ] **Step 4: Rewrite references TO `model_values`** (consumers: `model_actions.py`, `model_variables.py`, `classifiers/model_classifier.py` under `TYPE_CHECKING`)
- [ ] **Step 5: Run `pytest tests/unit/models -v -k values`** → PASS
- [ ] **Step 6: Commit**

---

## Task 5: Move `statemachine` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_statemachine.py` → `src/rhapsody_cli/models/elements/statemachine/model_statemachine.py`
- Create: `src/rhapsody_cli/models/elements/statemachine/__init__.py`

**Interfaces:**
- Consumes: `RPModelElement` (core), `RPInterfaceItem` (classifiers), `RPSwimlane` (activity — not yet moved; keep old path), `RPConnector`/`RPTransition` (graphics/interactions — not yet moved; keep old path)
- Produces: `RPStateVertex`, `RPState` at `...statemachine`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `statemachine/__init__.py`** re-exporting `RPStateVertex, RPState`
- [ ] **Step 3: Update `elements/__init__.py`** → `from rhapsody_cli.models.elements import statemachine as statemachine`
- [ ] **Step 4: Rewrite references TO `model_statemachine`** (consumers: `model_actions.py`, `model_activity.py`, `model_graphics.py`, `model_interactions.py`, `classifiers/model_statechart.py`)
- [ ] **Step 5: Run `pytest tests/unit/models -v -k state`** → PASS
- [ ] **Step 6: Commit**

---

## Task 6: Move `activity` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_activity.py` → `src/rhapsody_cli/models/elements/activity/model_activity.py`
- Move: `src/rhapsody_cli/models/elements/model_actions.py` → `src/rhapsody_cli/models/elements/activity/model_actions.py`
- Create: `src/rhapsody_cli/models/elements/activity/__init__.py`

**Interfaces:**
- Consumes: `RPClassifier`/`RPStatechart` (classifiers), `RPState` (statemachine — already moved → update import), `RPMessage`/`RPEvent`/`RPRelation` (interactions — not yet moved; keep old), `RPActivityDiagram` (diagrams — already moved → update import), `RPPin` (graphics — not yet moved; keep old), `RPSysMLPort`/`RPInstance`/`RPPort` (common/relations — not yet moved; keep old)
- Produces: `RPFlow`, `RPFlowItem`, `RPFlowchart`, `RPObjectNode`, `RPSwimlane`, `RPAction`, `RPAcceptEventAction`, `RPAcceptTimeEvent`, `RPActionBlock`, `RPCallOperation`, `RPContextSpecification`, `RPSendAction` at `...activity`

- [ ] **Step 1: git mv both modules**
- [ ] **Step 2: Create `activity/__init__.py`** re-exporting the listed classes
- [ ] **Step 3: Inside moved `activity` modules, update outgoing imports already in subpackages**: `model_statemachine` → `statemachine.model_statemachine`, `model_diagram_types` → `diagrams.model_diagram_types`. Leave not-yet-moved (`model_actions` self-ref within activity is fine after move; `model_graphics` keep old; `model_interactions` keep old; `model_other_model` keep old; `relations.*` already subpackage → `relations.model_*`).
- [ ] **Step 4: Update `elements/__init__.py`** lines `model_activity as activity` and `model_actions as actions` → `from rhapsody_cli.models.elements import activity as activity`
- [ ] **Step 5: Rewrite references TO `model_activity` and `model_actions`** across tree (consumers include `classifiers/model_classifier.py`, `model_graphics.py`, `model_interactions.py`, `model_statemachine.py`, `model_diagram_types.py`, `model_diagrams.py` already moved).
- [ ] **Step 6: Run `pytest tests/unit/models -v -k "activity or action"`** → PASS
- [ ] **Step 7: Commit**

---

## Task 7: Move `interactions` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_interactions.py` → `src/rhapsody_cli/models/elements/interactions/model_interactions.py`
- Create: `src/rhapsody_cli/models/elements/interactions/__init__.py`

**Interfaces:**
- Consumes: `RPInterfaceItem`/`RPStatechart` (classifiers), `RPCollaboration` (containment), `RPAction` (activity — already moved → update), `RPSequenceDiagram` (diagrams — already moved → update), `RPState`/`RPStateVertex` (statemachine — already moved → update), `RPAssociationRole`/`RPPort` (relations — already subpackage → update), `RPSysMLPort`/`RPType` (common — not yet moved; keep old)
- Produces: `RPEvent`, `RPEventReception`, `RPExecutionOccurrence`, `RPGuard`, `RPInteractionOccurrence`, `RPInteractionOperand`, `RPInteractionOperator`, `RPMessage`, `RPTransition`, `RPTrigger`, `RPDestructionEvent` at `...interactions`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `interactions/__init__.py`** re-exporting the listed classes
- [ ] **Step 3: Update outgoing imports inside the moved file to already-moved subpackages: `model_actions`→`activity.model_actions`, `model_diagram_types`→`diagrams.model_diagram_types`, `model_statemachine`→`statemachine.model_statemachine`, `relations.model_*` stay (already subpackage). Keep `model_other_model` old (common not yet moved).
- [ ] **Step 4: Update `elements/__init__.py`** → `from rhapsody_cli.models.elements import interactions as interactions`
- [ ] **Step 5: Rewrite references TO `model_interactions`** across tree (consumers: `classifiers/model_actor.py`, `classifiers/model_class.py`, `model_actions.py`, `model_graphics.py`, `model_statemachine.py`, `model_other_model.py`)
- [ ] **Step 6: Run `pytest tests/unit/models -v -k interaction`** → PASS
- [ ] **Step 7: Commit**

---

## Task 8: Move `requirements` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_requirements.py` → `src/rhapsody_cli/models/elements/requirements/model_requirements.py`
- Create: `src/rhapsody_cli/models/elements/requirements/__init__.py`

**Interfaces:** Consumes `RPUnit` (core). Produces `RPAnnotation`, `RPRequirement` at `...requirements`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `requirements/__init__.py`** re-exporting `RPAnnotation, RPRequirement`
- [ ] **Step 3: Update `elements/__init__.py`** → `from rhapsody_cli.models.elements import requirements as requirements`
- [ ] **Step 4: Rewrite references TO `model_requirements`** (consumers: `tests/unit/models/elements/test_annotation.py`, `test_requirement.py`)
- [ ] **Step 5: Run `pytest tests/unit/models/elements/test_annotation.py tests/unit/models/elements/test_requirement.py -v`** → PASS
- [ ] **Step 6: Commit**

---

## Task 9: Move `templates` subpackage

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_templates.py` → `src/rhapsody_cli/models/elements/templates/model_templates.py`
- Create: `src/rhapsody_cli/models/elements/templates/__init__.py`

**Interfaces:** Consumes `RPModelElement` (core), `RPClassifier` (classifiers), `RPVariable` (variables — already moved → update import). Produces `RPTemplateInstantiation`, `RPTemplateInstantiationParameter`, `RPTemplateParameter` at `...templates`

- [ ] **Step 1: git mv**
- [ ] **Step 2: Create `templates/__init__.py`** re-exporting the three classes
- [ ] **Step 3: Update outgoing import `model_variables`→`variables.model_variables` inside moved file
- [ ] **Step 4: Update `elements/__init__.py`** → `from rhapsody_cli.models.elements import templates as templates`
- [ ] **Step 5: Rewrite references TO `model_templates`** (none in tests; only internal) — verify with grep
- [ ] **Step 6: Run `pytest tests/unit/models -v`** → PASS for templates area
- [ ] **Step 7: Commit**

---

## Task 10: Move `common` subpackage (last)

**Files:**
- Move: `src/rhapsody_cli/models/elements/model_misc.py` → `src/rhapsody_cli/models/elements/common/model_misc.py`
- Move: `src/rhapsody_cli/models/elements/model_other_model.py` → `src/rhapsody_cli/models/elements/common/model_other_model.py`
- Create: `src/rhapsody_cli/models/elements/common/__init__.py`

**Interfaces:** Consumes `RPModelElement` (core), `RPClassifier` (classifiers), `RPPackage` (containment), `RPSequenceDiagram` (diagrams — already moved → update), `RPLink`/`RPGraphElement` (graphics — already moved → update), `RPEnumerationLiteral` (misc — same subpackage), `RPRelation` (relations — already subpackage → update). Produces `RPComment`, `RPConstraint`, `RPEnumerationLiteral`, `RPClassifierRole`, `RPSysMLPort`, `RPType` at `...common`

- [ ] **Step 1: git mv both modules**
- [ ] **Step 2: Create `common/__init__.py`** re-exporting the six classes
- [ ] **Step 3: Update outgoing imports inside `model_other_model.py` to already-moved targets: `model_diagram_types`→`diagrams.model_diagram_types`, `model_graphics`→`graphics.model_graphics`, `model_misc`→`common.model_misc`, `relations.model_relation` stays. Inside `model_misc.py` no outgoing element imports.
- [ ] **Step 4: Update `elements/__init__.py`** lines `model_misc as misc` and `model_other_model as other_model` → `from rhapsody_cli.models.elements import common as common`
- [ ] **Step 5: Rewrite references TO `model_misc` and `model_other_model`** across entire tree (these are the most-widely referenced — consumers include `classifiers/model_classifier.py`, `containment/model_*`, `model_graphics.py`, `model_interactions.py`, `model_statemachine.py`, `model_activity.py`, `support/model_codegen.py`, `tests/unit/models/elements/test_misc.py`, `tests/unit/models/test_integration.py`)
- [ ] **Step 6: Run full unit suite**

```bash
pytest tests/unit -v
```
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "refactor: move misc/other-model modules into common/ subpackage"
```

---

## Task 11: Full Quality Gate

**Files:** None new — verification only.

- [ ] **Step 1: Run ruff**

```bash
ruff check src/ tests/
```
Expected: no errors (unused-import `F401` flags are already noqa'd; verify no new ones from stale `as` aliases).

- [ ] **Step 2: Run black**

```bash
black --check src/ tests/
```
Expected: no formatting diffs (run `black src/ tests/` if needed and re-commit).

- [ ] **Step 3: Run mypy** (strict; Python < 3.10 in CI)

```bash
mypy src/ tests/
```
Expected: no type errors.

- [ ] **Step 4: Run full test suite + coverage**

```bash
pytest tests/unit -v --cov=rhapsody_cli
```
Expected: all pass, coverage ≥ 80%.

- [ ] **Step 5: Verify registry still populated** — quick smoke import

```bash
python -c "import rhapsody_cli; from rhapsody_cli.models.core import AbstractRPModelElement; print(len(AbstractRPModelElement._WRAPPER_REGISTRY))"
```
Expected: registry non-empty (same count as before the refactor).

- [ ] **Step 6: Commit any formatting fixes**

```bash
git add -A
git commit -m "style: apply lint/format fixes after model regrouping" || echo "nothing to commit"
```

---

## Self-Review Checklist

1. **Spec coverage:** Every flat `model_*.py` module is assigned a target subpackage (diagrams, graphics, variables, values, statemachine, activity, interactions, requirements, templates, common). No flat `model_*.py` remains in `elements/`.
2. **Placeholder scan:** Each task shows exact `git mv` commands, exact `__init__.py` content template, and an exact reusable rewrite command; no "TBD"/"similar to" placeholders.
3. **Type consistency:** Re-exported class names in each `__init__.py` match the class names defined in the moved modules (verified against the `grep "^class "` listing from the current tree).
4. **Green-state rule:** Ordering (common last) + "leave not-yet-moved outgoing imports at old path" guarantees the tree imports after every task; only the final `pytest tests/unit` must be fully green, with each prior task green for its own touched tests.
5. **Registry:** `elements/__init__.py` continues importing all subpackages, so `register_wrapper` side-effects still fire; Task 11 Step 5 asserts this.
