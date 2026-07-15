# Diagrams Subpackage Integration Tests Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add integration tests for all remaining untested `RPDiagram` methods (diagram lifecycle, graphic element creation, views, pictures) and creation/isinstance tests for the 10 remaining diagram-type subclasses in `model_diagram_types.py`. Flip in-source `[ ] integration test` markers to `[x]` as work completes.

**Architecture:** Extends `tests/integration/models/elements/diagrams/test_model_diagrams.py` for `RPDiagram`; creates new `tests/integration/models/elements/diagrams/test_model_diagram_types.py` for the subclasses.

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid.uuid4().hex[:8]`.

## Scope Verification (Step 1 findings)

- `model_diagrams.py` — `RPDiagram` has **33** checklist rows, **all currently `[ ] integration test`** (4 of them — `add_text_box`, `get_custom_views`, `close_diagram`, `get_corresponding_graphic_elements` — already have unit tests but zero integration coverage).
- `model_diagram_types.py` — 11 subclasses:
  - `RPCollaborationDiagram` — own method: `get_logical_collaboration` (1 checklist row)
  - `RPComponentDiagram` — pure `pass`, no own methods, inherits `RPDiagram` only
  - `RPDeploymentDiagram` — pure `pass`, no own methods
  - `RPObjectModelDiagram` — pure `pass`, no own methods (already has a creation test in existing `test_model_diagrams.py`)
  - `RPPanelDiagram` — pure `pass`, no own methods
  - `RPSequenceDiagram` — own methods: `get_logical_collaboration`, `get_related_use_cases` (2 checklist rows)
  - `RPStatechartDiagram` — own methods: `add_and_line`, `create_graphics`, `get_statechart` (3 checklist rows)
  - `RPStructureDiagram` — pure `pass`, no own methods. **Try the generic factory:** `pkg.add_new_aggr("StructureDiagram", name)` or `cls.add_new_aggr("StructureDiagram", name)` — if Rhapsody accepts this meta-type, the creation test passes. If it rejects it, keep the xfail with the documented reason. `IRPUnit.getStructureDiagrams()` exists as a getter, confirming the meta-type is valid for retrieval.
  - `RPUseCaseDiagram` — pure `pass`, no own methods
  - `RPTimingDiagram` (extends `RPSequenceDiagram`) — own methods: `get_is_elaborated`, `set_is_elaborated` (2 checklist rows)
  - `RPActivityDiagram` (extends `RPStatechartDiagram`) — own methods: `decompose_swimlane`, `get_flowchart` (2 checklist rows)
- Existing `tests/integration/models/elements/diagrams/test_model_diagrams.py` covers only: creation via `pkg.add_object_model_diagram`, `get_name()`, and an `isinstance(diagram, RPDiagram)` check. None of `RPDiagram`'s own 33 methods are exercised.
- `RPPackage` (in `src/rhapsody_cli/models/elements/containment/model_package.py`) exposes the factory methods needed to instantiate each diagram subtype directly:
  - `add_activity_diagram`, `add_sequence_diagram`, `add_use_case_diagram`, `add_collaboration_diagram`, `add_component_diagram`, `add_deployment_diagram`, `add_object_model_diagram`, `add_statechart_diagram`, `add_timing_diagram`, `add_panel_diagram`
  - No `add_structure_diagram` (see limitation above).

## Global Constraints

- Windows-only runtime (requires Windows + a running Rhapsody instance)
- All test classes use `@pytest.mark.integration`
- All tests consume the `test_project: RPProject` fixture
- Use `_unique(prefix)` with `uuid.uuid4().hex[:8]`
- Always `try/finally` cleanup via `diagram.delete_from_project()`. For tests that call `open_diagram()`/`open_diagram_view()`, call `diagram.close_diagram()` before `delete_from_project()` in the `finally` block to avoid leaving the diagram in an open UI state.
- Assert both `isinstance()` and read-back values
- Flip `[ ] integration test` to `[x]` per task in the relevant `model_*.py` file
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- Import via subpackage `__init__.py` re-exports (`from rhapsody_cli.models.elements.diagrams import RPDiagram, ...`)

---

## Tasks

### Task 1: RPDiagram lifecycle (open/close/populate/is_open)

**Files:**
- Modify: `tests/integration/models/elements/diagrams/test_model_diagrams.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (flip checklist boxes only)

**Methods covered:** `open_diagram`, `close_diagram`, `is_open`, `populate_diagram`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_open_close_and_is_open(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        assert diagram.is_open() == 1
        diagram.close_diagram()
        assert diagram.is_open() == 0
    finally:
        diagram.delete_from_project()
```

For `populate_diagram`, follow the same pattern:

```python
def test_populate_diagram(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls = pkg.add_class(self._unique("PopClass"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.add_new_node_for_element(cls, 0, 0, 100, 60)
        diagram.populate_diagram()
        elements = diagram.get_elements_in_diagram()
        assert cls in list(elements)
    finally:
        diagram.delete_from_project()
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -m integration -v -k "open_close_and_is_open or populate_diagram"`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`, flip `[ ] integration test` to `[x]` for: `openDiagram`, `close_diagram` (already `[x]` unit test; add `[x]` integration test), `isOpen`, `populateDiagram`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git commit -m "test: add integration tests for RPDiagram lifecycle methods"
```

---

### Task 2: RPDiagram graphic element builders

**Files:**
- Modify: `tests/integration/models/elements/diagrams/test_model_diagrams.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (flip checklist boxes only)

**Methods covered:** `add_new_node_by_type`, `add_new_node_for_element`, `add_new_edge_by_type`, `add_new_edge_for_element`, `add_free_shape_by_type`, `add_image`, `add_text_box`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_add_new_node_by_type_and_add_new_edge_by_type(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        node_a = diagram.add_new_node_by_type("Class", 0, 0, 100, 60)
        node_b = diagram.add_new_node_by_type("Class", 200, 0, 100, 60)
        assert node_a is not None
        assert node_b is not None
        edge = diagram.add_new_edge_by_type("Association", node_a, node_b)
        assert edge is not None
    finally:
        diagram.delete_from_project()
```

For remaining methods, follow the same pattern:

```python
def test_add_new_node_for_element(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls = pkg.add_class(self._unique("NodeClass"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        node = diagram.add_new_node_for_element(cls, 0, 0, 100, 60)
        assert node is not None
    finally:
        diagram.delete_from_project()

def test_add_new_edge_for_element(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls_a = pkg.add_class(self._unique("ClsA"))
    cls_b = pkg.add_class(self._unique("ClsB"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.add_new_node_for_element(cls_a, 0, 0, 100, 60)
        diagram.add_new_node_for_element(cls_b, 200, 0, 100, 60)
        assoc = cls_a.add_association(cls_b, self._unique("assoc"))
        edge = diagram.add_new_edge_for_element(assoc)
        assert edge is not None
    finally:
        diagram.delete_from_project()

def test_add_free_shape_by_type(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        shape = diagram.add_free_shape_by_type("Rectangle", 0, 0, 50, 50)
        assert shape is not None
    finally:
        diagram.delete_from_project()

def test_add_image(self, test_project: RPProject, tmp_path) -> None:
    from PIL import Image  # or reuse an existing fixture image under tests/fixtures
    image_path = str(tmp_path / "test_image.bmp")
    Image.new("RGB", (10, 10)).save(image_path)
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        image = diagram.add_image(image_path, 0, 0, 50, 50)
        assert image is not None
    finally:
        diagram.delete_from_project()

def test_add_text_box(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        box = diagram.add_text_box("hello world", 0, 0, 80, 20)
        assert box is not None
    finally:
        diagram.delete_from_project()
```

Note: if `RPClass.add_association` does not exist in the classifiers subpackage, substitute any existing relation-adding method available on `RPClass`/`RPClassifier` (check `model_classifier.py`/`model_class.py` first) or fall back to two nodes plus `add_new_edge_by_type` only, dropping the `add_new_edge_for_element`-specific relation setup and instead reusing an existing model element (e.g. a dependency or generalization) already available in that subpackage's public API.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -m integration -v -k "add_new_node or add_new_edge or add_free_shape or add_image or add_text_box"`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`, flip `[ ] integration test` to `[x]` for: `addNewNodeByType`, `addNewNodeForElement`, `addNewEdgeByType`, `addNewEdgeForElement`, `addFreeShapeByType`, `addImage`, `add_text_box`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git commit -m "test: add integration tests for RPDiagram graphic element builders"
```

---

### Task 3: RPDiagram views

**Files:**
- Modify: `tests/integration/models/elements/diagrams/test_model_diagrams.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (flip checklist boxes only)

**Methods covered:** `create_diagram_view`, `get_diagram_view_of`, `get_diagram_views`, `is_diagram_view`, `open_diagram_view`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_create_diagram_view_and_get_diagram_views(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    view_name = self._unique("View")
    try:
        view = diagram.create_diagram_view(view_name)
        assert view is not None
        views = diagram.get_diagram_views()
        assert len(list(views)) >= 1
    finally:
        diagram.delete_from_project()
```

For remaining methods, follow the same pattern:

```python
def test_get_diagram_view_of_and_is_diagram_view(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    view_name = self._unique("View")
    try:
        diagram.create_diagram_view(view_name)
        found = diagram.get_diagram_view_of(view_name)
        assert found is not None
        assert found.is_diagram_view() == 1
    finally:
        diagram.delete_from_project()

def test_open_diagram_view(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    view_name = self._unique("View")
    try:
        diagram.create_diagram_view(view_name)
        diagram.open_diagram_view(view_name)  # should not raise
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -m integration -v -k "diagram_view"`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`, flip `[ ] integration test` to `[x]` for: `createDiagramView`, `getDiagramViewOf`, `getDiagramViews`, `isDiagramView`, `openDiagramView`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git commit -m "test: add integration tests for RPDiagram view methods"
```

---

### Task 4: RPDiagram picture export & element queries

**Files:**
- Modify: `tests/integration/models/elements/diagrams/test_model_diagrams.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (flip checklist boxes only)

**Methods covered:** `get_picture`, `get_picture_as`, `get_picture_as_divided_metafiles`, `get_picture_ex`, `get_pictures_with_image_map`, `get_elements_in_diagram`, `get_graphical_elements`, `get_corresponding_graphic_elements`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_get_elements_in_diagram_and_get_graphical_elements(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls = pkg.add_class(self._unique("QueryClass"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.add_new_node_for_element(cls, 0, 0, 100, 60)
        elements = diagram.get_elements_in_diagram()
        assert cls in list(elements)
        graphical = diagram.get_graphical_elements()
        assert len(list(graphical)) >= 1
    finally:
        diagram.delete_from_project()
```

For remaining methods, follow the same pattern:

```python
def test_get_corresponding_graphic_elements(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls = pkg.add_class(self._unique("CorrClass"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        node = diagram.add_new_node_for_element(cls, 0, 0, 100, 60)
        found = diagram.get_corresponding_graphic_elements(cls)
        assert node in list(found)
    finally:
        diagram.delete_from_project()

def test_get_picture(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        picture = diagram.get_picture()
        assert picture is not None
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()

def test_get_picture_as(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        picture = diagram.get_picture_as("PNG")
        assert picture is not None
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()

def test_get_picture_ex(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        picture = diagram.get_picture_ex(0, 0, 200, 200)
        assert picture is not None
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()

def test_get_picture_as_divided_metafiles(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        metafiles = diagram.get_picture_as_divided_metafiles()
        assert metafiles is not None
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()

def test_get_pictures_with_image_map(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.open_diagram()
        pictures = diagram.get_pictures_with_image_map()
        assert pictures is not None
    finally:
        diagram.close_diagram()
        diagram.delete_from_project()
```

If any `get_picture*` call raises `RhapsodyRuntimeException` because the diagram must be visually rendered first (COM quirk on headless/CI Rhapsody instances), mark that specific test `@pytest.mark.xfail(reason="requires rendered diagram view in live Rhapsody UI", strict=False)` rather than deleting it.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -m integration -v -k "picture or elements_in_diagram or graphical_elements or corresponding_graphic"`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`, flip `[ ] integration test` to `[x]` for: `getPicture`, `getPictureAs`, `getPictureAsDividedMetafiles`, `getPictureEx`, `getPicturesWithImageMap`, `getElementsInDiagram`, `getGraphicalElements`, `get_corresponding_graphic_elements`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git commit -m "test: add integration tests for RPDiagram picture export and queries"
```

---

### Task 5: RPDiagram frame/ports/relations/misc

**Files:**
- Modify: `tests/integration/models/elements/diagrams/test_model_diagrams.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py` (flip checklist boxes only)

**Methods covered:** `is_show_diagram_frame`, `set_show_diagram_frame`, `rearrange_ports`, `complete_relations`, `update_view_on_server`, `remove_graph_elements`, `get_custom_views`, `set_custom_views`, `get_last_visualization_modified_time`

- [ ] **Step 1: Write the failing/new integration tests**

```python
def test_show_diagram_frame_get_set(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.set_show_diagram_frame(1)
        assert diagram.is_show_diagram_frame() == 1
        diagram.set_show_diagram_frame(0)
        assert diagram.is_show_diagram_frame() == 0
    finally:
        diagram.delete_from_project()
```

For remaining methods, follow the same pattern:

```python
def test_rearrange_ports(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.rearrange_ports()  # should not raise
    finally:
        diagram.delete_from_project()

def test_complete_relations(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.complete_relations()  # should not raise
    finally:
        diagram.delete_from_project()

def test_update_view_on_server(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        diagram.update_view_on_server()  # should not raise
    finally:
        diagram.delete_from_project()

def test_remove_graph_elements(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    cls = pkg.add_class(self._unique("RemClass"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        node = diagram.add_new_node_for_element(cls, 0, 0, 100, 60)
        from rhapsody_cli.models.core import RPCollection

        to_remove = RPCollection([node])  # verify RPCollection accepts a list; else build via get_graphical_elements() filter
        diagram.remove_graph_elements(to_remove)
        remaining = diagram.get_graphical_elements()
        assert node not in list(remaining)
    finally:
        diagram.delete_from_project()

def test_custom_views_get_set(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        views = diagram.get_custom_views()
        diagram.set_custom_views(views)  # round-trip should not raise
    finally:
        diagram.delete_from_project()

def test_get_last_visualization_modified_time(self, test_project: RPProject) -> None:
    pkg = self._create_package(test_project, self._unique("DiagPkg"))
    diagram = pkg.add_object_model_diagram(self._unique("MyDiagram"))
    try:
        modified_time = diagram.get_last_visualization_modified_time()
        assert modified_time is not None
    finally:
        diagram.delete_from_project()
```

Note: verify the exact `RPCollection` construction pattern used elsewhere in the codebase for building a collection from a Python list (check `RPCollection.__init__` in `src/rhapsody_cli/models/core.py`); adjust `test_remove_graph_elements` to match the real constructor signature — it may require going through the underlying COM collection object rather than a raw Python list.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagrams.py -m integration -v -k "show_diagram_frame or rearrange_ports or complete_relations or update_view_on_server or remove_graph_elements or custom_views or last_visualization"`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagrams.py`, flip `[ ] integration test` to `[x]` for: `isShowDiagramFrame`, `setShowDiagramFrame`, `rearrangePorts`, `completeRelations`, `updateViewOnServer`, `removeGraphElements`, `get_custom_views`, `setCustomViews`, `getLastVisualizationModifiedTime`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagrams.py
git commit -m "test: add integration tests for RPDiagram frame, ports, relations and misc methods"
```

---

### Task 6: model_diagram_types.py — creation, isinstance, and subclass-own methods

**Files:**
- Create: `tests/integration/models/elements/diagrams/test_model_diagram_types.py`
- Modify: `src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py` (flip checklist boxes only)

**Methods covered (creation/isinstance for 10 subtypes):** `RPCollaborationDiagram`, `RPComponentDiagram`, `RPDeploymentDiagram`, `RPPanelDiagram`, `RPSequenceDiagram`, `RPStatechartDiagram`, `RPStructureDiagram` (try `add_new_aggr("StructureDiagram", name")` — keep xfail only if Rhapsody rejects the meta-type), `RPUseCaseDiagram`, `RPTimingDiagram`, `RPActivityDiagram`

**Subclass-own methods covered:** `get_logical_collaboration` (`RPCollaborationDiagram`), `get_logical_collaboration`/`get_related_use_cases` (`RPSequenceDiagram`), `add_and_line`/`create_graphics`/`get_statechart` (`RPStatechartDiagram`), `get_is_elaborated`/`set_is_elaborated` (`RPTimingDiagram`), `decompose_swimlane`/`get_flowchart` (`RPActivityDiagram`)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for the diagram-type subclasses in model_diagram_types.py."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.diagrams import (
    RPActivityDiagram,
    RPCollaborationDiagram,
    RPComponentDiagram,
    RPDeploymentDiagram,
    RPPanelDiagram,
    RPSequenceDiagram,
    RPStatechartDiagram,
    RPStructureDiagram,
    RPTimingDiagram,
    RPUseCaseDiagram,
)


@pytest.mark.integration
class TestDiagramTypesIntegration:
    """Integration tests for RPDiagram subclasses with live Rhapsody COM API."""

    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_create_collaboration_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("CollabDiagram")
        diagram = pkg.add_collaboration_diagram(name)
        try:
            assert diagram is not None
            assert isinstance(diagram, RPCollaborationDiagram)
            assert diagram.get_name() == name
            collaboration = diagram.get_logical_collaboration()
            assert collaboration is not None
        finally:
            diagram.delete_from_project()
```

For remaining subtypes, follow the same pattern:

```python
    def test_create_component_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("ComponentDiagram")
        diagram = pkg.add_component_diagram(name)
        try:
            assert isinstance(diagram, RPComponentDiagram)
            assert diagram.get_name() == name
        finally:
            diagram.delete_from_project()

    def test_create_deployment_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("DeploymentDiagram")
        diagram = pkg.add_deployment_diagram(name)
        try:
            assert isinstance(diagram, RPDeploymentDiagram)
            assert diagram.get_name() == name
        finally:
            diagram.delete_from_project()

    def test_create_panel_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("PanelDiagram")
        diagram = pkg.add_panel_diagram(name)
        try:
            assert isinstance(diagram, RPPanelDiagram)
            assert diagram.get_name() == name
        finally:
            diagram.delete_from_project()

    def test_create_sequence_diagram_and_own_methods(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("SeqDiagram")
        diagram = pkg.add_sequence_diagram(name)
        try:
            assert isinstance(diagram, RPSequenceDiagram)
            assert diagram.get_name() == name
            collaboration = diagram.get_logical_collaboration()
            assert collaboration is not None
            use_cases = diagram.get_related_use_cases()
            assert use_cases is not None
        finally:
            diagram.delete_from_project()

    def test_create_statechart_diagram_and_own_methods(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("SCDiagram")
        diagram = pkg.add_statechart_diagram(name)
        try:
            assert isinstance(diagram, RPStatechartDiagram)
            assert diagram.get_name() == name
            diagram.create_graphics()  # should not raise
            statechart = diagram.get_statechart()
            assert statechart is not None
        finally:
            diagram.delete_from_project()

    def test_statechart_add_and_line(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("SCDiagram")
        diagram = pkg.add_statechart_diagram(name)
        try:
            diagram.create_graphics()
            state_node = diagram.add_new_node_by_type("State", 0, 0, 100, 60)
            orthogonal_states = diagram.add_and_line(state_node, 0, 0, 100, 100)
            assert orthogonal_states is not None
        finally:
            diagram.delete_from_project()

    def test_create_structure_diagram(self, test_project: RPProject) -> None:
        from rhapsody_cli.models.elements.classifiers import RPClass

        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        cls = pkg.add_class(self._unique("StructClass"))
        try:
            diagram = cls.add_new_aggr("StructureDiagram", self._unique("StructDgm"))
            assert isinstance(diagram, RPStructureDiagram)
        finally:
            cls.delete_from_project()

    def test_create_use_case_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("UCDiagram")
        diagram = pkg.add_use_case_diagram(name)
        try:
            assert isinstance(diagram, RPUseCaseDiagram)
            assert diagram.get_name() == name
        finally:
            diagram.delete_from_project()

    def test_create_timing_diagram_and_own_methods(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("TimingDiagram")
        diagram = pkg.add_timing_diagram(name)
        try:
            assert isinstance(diagram, RPTimingDiagram)
            assert diagram.get_name() == name
            diagram.set_is_elaborated(1)
            assert diagram.get_is_elaborated() == 1
            diagram.set_is_elaborated(0)
            assert diagram.get_is_elaborated() == 0
        finally:
            diagram.delete_from_project()

    def test_create_activity_diagram_and_own_methods(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("ActDiagram")
        diagram = pkg.add_activity_diagram(name)
        try:
            assert isinstance(diagram, RPActivityDiagram)
            assert diagram.get_name() == name
            flowchart = diagram.get_flowchart()
            assert flowchart is not None
        finally:
            diagram.delete_from_project()

    def test_activity_diagram_decompose_swimlane(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("DiagPkg"))
        name = self._unique("ActDiagram")
        diagram = pkg.add_activity_diagram(name)
        try:
            diagram.create_graphics()
            swimlane = diagram.add_new_node_by_type("Swimlane", 0, 0, 200, 400)
            new_swimlanes = diagram.decompose_swimlane(swimlane)
            assert new_swimlanes is not None
        finally:
            diagram.delete_from_project()
```

Before finalizing `test_statechart_add_and_line` and `test_activity_diagram_decompose_swimlane`, verify the exact metaclass type strings (`"State"`, `"Swimlane"`) accepted by `addNewNodeByType` for statechart/activity diagrams against the live Rhapsody COM API — these are best-effort placeholders and may need adjustment (e.g. `"SimpleState"` vs `"State"`) once run against a real instance. If the COM call fails, capture the actual accepted value from Rhapsody's IDE or API docs and correct the test.

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/diagrams/test_model_diagram_types.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py`, flip `[ ] integration test` to `[x]` for: `getLogicalCollaboration` (both `RPCollaborationDiagram` and `RPSequenceDiagram` checklists), `getRelatedUseCases`, `addAndLine`, `createGraphics`, `getStatechart`, `getIsElaborated`, `setIsElaborated`, `decomposeSwimlane`, `getFlowchart`. Leave `RPStructureDiagram`'s checklist untouched (no own methods to flip) but add an inline comment noting the `xfail` limitation for future follow-up.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/diagrams/test_model_diagram_types.py src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py
git commit -m "test: add integration tests for diagram-type subclasses"
```

---

### Task 7: Full Subpackage Verification

**Files:** None modified — verification only.

- [ ] **Step 1: Run the complete diagrams integration test suite**

Run: `pytest tests/integration/models/elements/diagrams/ -m integration -v`

- [ ] **Step 2: Confirm all checklist boxes are flipped**

Run: `grep -n "\[ \] integration test" src/rhapsody_cli/models/elements/diagrams/model_diagrams.py src/rhapsody_cli/models/elements/diagrams/model_diagram_types.py`

Expect zero remaining unchecked `integration test` rows except the intentionally-documented `RPStructureDiagram` creation gap (which has no own-method checklist rows to begin with).

- [ ] **Step 3: Run the full quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 4: Run the full integration suite once more to confirm no regressions**

Run: `pytest tests/integration/ -m integration -v`

- [ ] **Step 5: Commit** (only if any cleanup edits were needed)

```bash
git add -A
git commit -m "test: complete diagrams subpackage integration test coverage"
```
