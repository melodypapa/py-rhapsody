# Graphics Subpackage Integration Tests Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add integration tests for ALL methods (currently zero coverage, 190 methods — the largest coverage gap in the codebase) of `RPConditionMark`, `RPConnector`, `RPGraphElement`, `RPGraphicalProperty`, `RPImageMap`, `RPLink`, `RPMatrixLayout`, `RPMatrixView`, `RPMessagePoint`, `RPTableLayout`, `RPTableView`, `RPPin`, `RPGraphEdge`, `RPGraphNode`. Flip in-source `[ ] integration test` markers to `[x]` as work completes.

**Architecture:** New test files under `tests/integration/models/elements/graphics/`, split by class group, using shared `rhapsody_app`/`test_project` fixtures and diagram/element creation helpers built on `RPPackage.add_statechart_diagram`/`add_new_aggr`, `RPDiagram.add_new_node_by_type`/`add_new_edge_by_type`, and `RPFlow.add_activity_parameter`.

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid.uuid4().hex[:8]`.

## Scope Verification (190/190 methods accounted for)

`RPConditionMark` has zero own methods (pure `RPMessage` subclass, no checklist rows) — it contributes 0 of the 190 rows. The 190 untested integration-test rows are distributed as:

| Class | Row count | Tasks |
|---|---|---|
| RPConnector | 16 | Task 1 |
| RPGraphElement | 22 | Tasks 2–3 |
| RPGraphicalProperty | 3 | Task 4 |
| RPImageMap | 7 | Task 5 (flagged — see below) |
| RPLink | 19 | Tasks 6–7 |
| RPMatrixLayout | 14 | Task 8 |
| RPMatrixView | 19 | Tasks 9–10 |
| RPMessagePoint | 5 | Task 11 |
| RPTableLayout | 50 | Tasks 12–15 |
| RPTableView | 17 | Tasks 16–17 |
| RPPin | 6 | Task 18 |
| RPGraphEdge | 5 | Task 19 |
| RPGraphNode | 7 | Task 19 |
| **Total** | **190** | |

### Flagged: `RPImageMap` creation path

`RPImageMap` (7 methods) — **Creation path now available:** `RhapsodyApplication.create_new_collection() -> RPCollection` creates an empty collection, then `diagram.get_pictures_with_image_map(file_name, collection)` populates it with `IRPImageMap` objects. The wrapper bug (0-arg signature) has been fixed in Tasks 1-2 of the xfail-improvements plan. Task for RPImageMap should: (1) create a diagram with at least one graph element, (2) call `app.create_new_collection()`, (3) call `diagram.get_pictures_with_image_map("test.emf", collection)`, (4) iterate `collection` to get `RPImageMap` objects, (5) exercise all 7 getter methods. Use real assertions, not xfail.

---

## Global Constraints

- Windows-only runtime (requires Windows + a running Rhapsody instance)
- All test classes use `@pytest.mark.integration`
- All tests consume the `test_project: RPProject` fixture
- Use `_unique(prefix)` with `uuid.uuid4().hex[:8]` (see `tests/integration/models/elements/classifiers/test_model_actor.py` for the canonical pattern)
- Always `try/finally` cleanup using the correct delete/remove method verified from source (`element.delete_from_project()` for model elements/units; `diagram.remove_graph_elements(RPCollection)` for pure graphics-only elements that have no `delete_from_project`)
- Assert both `isinstance()` and read-back values
- Flip `[ ] integration test` to `[x]` per task in `model_graphics.py`
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- Import via subpackage `__init__.py` re-exports (`from rhapsody_cli.models.elements.graphics import RPConnector, ...`)
- Metaclass/type-string arguments passed to `add_new_node_by_type`, `add_new_edge_by_type`, and `add_new_aggr` (e.g. `"Junction"`, `"TableLayout"`, `"Instance"`) are inferred from the registered wrapper names in `model_graphics.py` (`register_wrapper("TableLayout", RPTableLayout)` etc.) and from Rhapsody metaclass conventions used elsewhere in the codebase. **These have not been executed against a live Rhapsody instance.** Each task's Step 2 (run against live Rhapsody) is where these are validated; if a specific type string is rejected by COM, adjust it to the correct Rhapsody metaclass name (consult the Rhapsody API reference or the IDE's "New" context menu for the exact string) and re-run.

---

## Shared Test Helper (create once, reuse across all tasks)

- [ ] **Step 0: Add a shared conftest helper module for graphics fixtures**

**Files:**
- Create: `tests/integration/models/elements/graphics/conftest.py`

```python
"""Shared fixtures/helpers for graphics subpackage integration tests."""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers.model_statechart import RPStatechart
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.diagrams.model_diagrams import RPStatechartDiagram


def unique(prefix: str = "Test") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def gfx_package(test_project: RPProject) -> RPPackage:
    pkg = test_project.add_package(unique("GfxPkg"))
    assert pkg is not None and isinstance(pkg, RPPackage)
    return pkg


@pytest.fixture
def gfx_statechart_diagram(gfx_package: RPPackage) -> RPStatechartDiagram:
    """A statechart diagram to host connectors/graph nodes/edges for graphics tests."""
    diagram = gfx_package.add_statechart_diagram(unique("SD"))
    assert diagram is not None
    return diagram
```

- [ ] **Step 1: Verify the helper imports resolve**

Run: `python -c "import tests.integration.models.elements.graphics.conftest"` (from repo root, with `PYTHONPATH` including `tests/`) — or simply proceed to Task 1, since pytest will surface import errors immediately.

---

### Task 1: RPConnector — full checklist

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_connector.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py` (flip checklist boxes only)

**Methods covered:** `createDefaultTransition`, `getConnectorType`, `getDerivedInEdges`, `getDerivedOutEdge`, `getItsSwimlane`, `getOfState`, `isConditionConnector`, `isDiagramConnector`, `isForkConnector`, `isHistoryConnector`, `isJoinConnector`, `isJunctionConnector`, `isStubConnector`, `isTerminationConnector`, `setItsSwimlane`, `setOfState` (16)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPConnector with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPConnector


@pytest.mark.integration
class TestRPConnectorIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_junction_connector_type_and_predicates(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("ConnPkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            connector = diagram.add_new_node_by_type("Junction", 10, 10, 40, 40)
            assert connector is not None
            assert isinstance(connector, RPConnector)
            assert connector.get_connector_type() == "Junction"
            assert connector.is_junction_connector() == 1
            assert connector.is_condition_connector() == 0
            assert connector.is_fork_connector() == 0
            assert connector.is_join_connector() == 0
            assert connector.is_history_connector() == 0
            assert connector.is_stub_connector() == 0
            assert connector.is_termination_connector() == 0
            assert connector.is_diagram_connector() == 0
        finally:
            diagram.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_fork_connector: diagram.add_new_node_by_type("Fork", ...) -> is_fork_connector() == 1
    # - test_join_connector: diagram.add_new_node_by_type("Join", ...) -> is_join_connector() == 1
    # - test_history_connector: diagram.add_new_node_by_type("History", ...) -> is_history_connector() == 1;
    #   set_of_state(state)/get_of_state() roundtrip using a state added via
    #   diagram.add_new_node_by_type("State", ...)
    # - test_condition_connector: diagram.add_new_node_by_type("Condition", ...) -> is_condition_connector() == 1
    # - test_stub_connector (EnterExit point): diagram.add_new_node_by_type("EnterExit", ...) ->
    #   is_stub_connector() == 1
    # - test_termination_connector: diagram.add_new_node_by_type("Termination", ...) ->
    #   is_termination_connector() == 1
    # - test_create_default_transition: connector.create_default_transition(state) -> isinstance RPTransition
    # - test_get_derived_in_edges / get_derived_out_edge: add transitions into/out of the connector via
    #   diagram.add_new_edge_by_type("Transition", source, connector) then inspect
    #   connector.get_derived_in_edges()/get_derived_out_edge()
    # - test_swimlane_roundtrip: set_its_swimlane(swimlane)/get_its_swimlane() using a swimlane added to
    #   an activity diagram's flowchart (RPFlowchart.add_new_node_by_type("Swimlane", ...))
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_connector.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

In `src/rhapsody_cli/models/elements/graphics/model_graphics.py`, flip all 16 `RPConnector` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_connector.py tests/integration/models/elements/graphics/conftest.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPConnector"
```

---

### Task 2: RPGraphElement — properties & graphical-property system (Part A)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_graph_element.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `addProperty`, `applyDefaultFormat`, `getAllGraphicalProperties`, `getAllProperties`, `getAssociatedImage`, `getDiagram`, `getGraphicalParent`, `getGraphicalProperty`, `getGraphicalPropertyOfText`, `getImageLayout`, `getInterfaceName` (11)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPGraphElement (via RPGraphNode instances) with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPGraphElement, RPGraphicalProperty


@pytest.mark.integration
class TestRPGraphElementIntegrationPartA:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_add_property_and_get_graphical_property(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("GEPkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            node = diagram.add_new_node_by_type("State", 10, 10, 80, 40)
            assert isinstance(node, RPGraphElement)
            key = self._unique("Key")
            node.add_property(key, "String", "hello")
            props = list(node.get_all_graphical_properties())
            assert any(isinstance(p, RPGraphicalProperty) for p in props)
            interface_name = node.get_interface_name()
            assert isinstance(interface_name, str)
            diagram_ref = node.get_diagram()
            assert diagram_ref == diagram
        finally:
            diagram.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_apply_default_format: node.apply_default_format() -> no exception raised
    # - test_get_all_properties: node.get_all_properties() -> RPCollection, contains added property
    # - test_get_associated_image / get_image_layout / get_selected_image (Task 3 counterpart setters):
    #   read-only getters here just assert type/None-or-str without raising
    # - test_get_graphical_parent: nest a node inside another graphical container (e.g. a state within
    #   a composite state) and assert get_graphical_parent() returns the container's graph element
    # - test_get_graphical_property_of_text: node.get_graphical_property_of_text("Name", "Color") or
    #   similar text-target property key, asserting a string or None is returned without raising
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_graph_element.py -m integration -v -k PartA`

- [ ] **Step 3: Flip checklist boxes**

Flip the 11 listed `RPGraphElement` rows above in `model_graphics.py`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_graph_element.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPGraphElement (part A)"
```

---

### Task 3: RPGraphElement — property values & image association (Part B)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_graph_element.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getLocalProperties`, `getModelObject`, `getPropertyValue`, `getSelectedImage`, `removeProperty`, `setAssociatedImage`, `setGraphicalProperty`, `setGraphicalPropertyOfText`, `setImageLayout`, `setPropertyValue`, `setSelectedImage` (11)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPGraphElementIntegrationPartB:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_property_value_roundtrip_and_removal(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("GEPkgB"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            node = diagram.add_new_node_by_type("State", 10, 10, 80, 40)
            key = self._unique("Key")
            node.add_property(key, "String", "v1")
            node.set_property_value(key, "v2")
            assert node.get_property_value(key) == "v2"
            node.remove_property(key)
            local_props = list(node.get_local_properties())
            assert key not in [p.get_key() for p in local_props]
        finally:
            diagram.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_model_object: node.get_model_object() returns the underlying wrapped RPState
    # - test_set_graphical_property / set_graphical_property_of_text: set then read back via
    #   get_graphical_property / get_graphical_property_of_text
    # - test_set_associated_image / get_selected_image / set_selected_image: use a real image file
    #   path under a temp directory (Rhapsody requires an existing file on disk); assert no exception
    #   and (where the API allows) a read-back match
    # - test_set_image_layout: valid layout constants (see IRPGraphElement.ImageLayout in the Rhapsody
    #   API reference, e.g. "Stretch", "Center") — verify exact accepted strings live
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_graph_element.py -m integration -v -k PartB`

- [ ] **Step 3: Flip checklist boxes**

Flip the 11 listed `RPGraphElement` rows above in `model_graphics.py`.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_graph_element.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPGraphElement (part B)"
```

---

### Task 4: RPGraphicalProperty

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_graphical_property.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getInterfaceName`, `getKey`, `getValue` (3)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPGraphicalProperty with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPProject
from rhapsody_cli.models.elements.graphics import RPGraphicalProperty


@pytest.mark.integration
class TestRPGraphicalPropertyIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_key_and_value_roundtrip(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("GPPkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            node = diagram.add_new_node_by_type("State", 10, 10, 80, 40)
            key = self._unique("Key")
            node.add_property(key, "String", "value1")
            props = [p for p in node.get_all_graphical_properties() if isinstance(p, RPGraphicalProperty)]
            match = next((p for p in props if p.get_key() == key), None)
            assert match is not None
            assert match.get_value() == "value1"
            assert isinstance(match.get_interface_name(), str)
        finally:
            diagram.delete_from_project()

    # For remaining methods: getInterfaceName is exercised above; no further methods remain.
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_graphical_property.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

Flip all 3 `RPGraphicalProperty` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_graphical_property.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPGraphicalProperty"
```

---

### Task 5: RPImageMap (flagged — limited creation path)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_image_map.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getInterfaceName`, `getIsGUID`, `getName`, `getPictureFileName`, `getPoints`, `getShape`, `getTarget` (7)

**Note:** A creation path is now available via the xfail-improvements plan: `RhapsodyApplication.create_new_collection()` produces an empty `RPCollection`, and `RPDiagram.get_pictures_with_image_map(file_name, collection)` (now correctly taking `(firstFileName, diagrammap)`) populates that collection with `IRPImageMap` objects. The test below should use real assertions, not `xfail`.

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPImageMap with live Rhapsody COM API."""

import uuid
from pathlib import Path

import pytest

from rhapsody_cli.models.elements.containment import RPProject
from rhapsody_cli.models.elements.graphics import RPImageMap


@pytest.mark.integration
class TestRPImageMapIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_image_map_attributes_via_diagram_picture(self, rhapsody_app, test_project: RPProject, tmp_path: Path) -> None:
        pkg = test_project.add_package(self._unique("IMPkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            image_path = tmp_path / "test_image.bmp"
            # Minimal 1x1 BMP header+pixel so Rhapsody accepts the file as a valid image.
            image_path.write_bytes(
                bytes.fromhex(
                    "424d3a000000000000003600000028000000010000000100000001001800"
                    "0000000004000000c40e0000c40e00000000000000000000ff0000"
                )
            )
            diagram.add_image(str(image_path), 10, 10, 50, 50)
            collection = rhapsody_app.create_new_collection()
            diagram.get_pictures_with_image_map("test_image.emf", collection)
            maps = list(collection)
            assert maps, "Expected at least one IRPImageMap after inserting an image"
            image_map = maps[0]
            assert isinstance(image_map, RPImageMap)
            assert isinstance(image_map.get_name(), str)
            assert isinstance(image_map.get_shape(), str)
            assert isinstance(image_map.get_points(), str)
            assert isinstance(image_map.get_target(), str)
            assert isinstance(image_map.get_picture_file_name(), str)
            assert image_map.get_is_guid() in (0, 1)
            assert isinstance(image_map.get_interface_name(), str)
        finally:
            diagram.delete_from_project()
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_image_map.py -m integration -v`

Confirm that the test passes against live Rhapsody: the diagram must contain at least one graph element (e.g. the inserted image) so that `get_pictures_with_image_map` populates the collection with `IRPImageMap` objects.

- [ ] **Step 3: Flip checklist boxes**

Flip all 7 `RPImageMap` rows once the task's test passes against live Rhapsody.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_image_map.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPImageMap"
```

---

### Task 6: RPLink — endpoints & instantiation (Part A)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_link.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getEnd1Multiplicity`, `getEnd1Name`, `getEnd2Multiplicity`, `getEnd2Name`, `getFrom`, `getFromElement`, `getFromPort`, `getFromSysMLPort`, `getInstantiates`, `getOther` (10)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPLink with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPLink


@pytest.mark.integration
class TestRPLinkIntegrationPartA:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def _build_link(self, test_project: RPProject):
        pkg = self._create_package(test_project, self._unique("LinkPkg"))
        owner_class = pkg.add_class(self._unique("OwnerCls"))
        part_class = pkg.add_class(self._unique("PartCls"))
        assoc = pkg.add_association(self._unique("Assoc"))
        # Parts ("Instance" metaclass) are generic model-element children of the owner class.
        part1 = owner_class.add_new_aggr("Instance", self._unique("p1"))
        part2 = owner_class.add_new_aggr("Instance", self._unique("p2"))
        part1.set_type(part_class)
        part2.set_type(part_class)
        link = owner_class.add_link(part1, part2, assoc, None, None)
        return pkg, owner_class, link

    def test_link_endpoints(self, test_project: RPProject) -> None:
        pkg, owner_class, link = self._build_link(test_project)
        try:
            assert isinstance(link, RPLink)
            assert isinstance(link.get_from(), object)
            assert link.get_from() is not None
            assert isinstance(link.get_end1_name(), str)
            assert isinstance(link.get_end2_name(), str)
        finally:
            owner_class.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_end1_multiplicity / get_end2_multiplicity: read multiplicity strings from the
    #   association ends (e.g. "1", "0..*") set via assoc end configuration if needed
    # - test_get_from_element / get_from_port / get_from_sys_ml_port: exercise on a link built via
    #   RPSysMLPort.add_link(...) when SysML ports are involved, else assert None is returned gracefully
    #   for a plain part-to-part link
    # - test_get_instantiates: link.get_instantiates() -> wrapped classifier/type of the "from" part
    # - test_get_other: link.get_other(part1) -> returns part2 (the "other" end of the link)
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_link.py -m integration -v -k PartA`

- [ ] **Step 3: Flip checklist boxes**

Flip the 10 listed `RPLink` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_link.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPLink (part A)"
```

---

### Task 7: RPLink — remaining getters & setters (Part B)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_link.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getTo`, `getToElement`, `getToPort`, `getToSysMLPort`, `setEnd1Multiplicity`, `setEnd1Name`, `setEnd2Multiplicity`, `setEnd2Name`, `setInstantiates` (9)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPLinkIntegrationPartB:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_end_name_roundtrip(self, test_project: RPProject) -> None:
        pkg, owner_class, link = TestRPLinkIntegrationPartA()._build_link(test_project)
        try:
            new_end1 = self._unique("end1")
            new_end2 = self._unique("end2")
            link.set_end1_name(new_end1)
            link.set_end2_name(new_end2)
            assert link.get_end1_name() == new_end1
            assert link.get_end2_name() == new_end2
            assert link.get_to() is not None
        finally:
            owner_class.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_to_element / get_to_port / get_to_sys_ml_port: mirror the "from" variants in Task 6
    # - test_set_end1_multiplicity / set_end2_multiplicity: set then read back via get_end1_multiplicity
    #   / get_end2_multiplicity
    # - test_set_instantiates: link.set_instantiates(classifier) then get_instantiates() roundtrip
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_link.py -m integration -v -k PartB`

- [ ] **Step 3: Flip checklist boxes**

Flip the 9 listed `RPLink` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_link.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPLink (part B)"
```

---

### Task 8: RPMatrixLayout — full checklist

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_matrix_layout.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getCellElementTypes`, `getFromElementTypes`, `getFromElementTypesQueryToUse`, `getFromElementTypesUseQueryOrElementsList`, `getToElementTypes`, `getToElementTypesQueryToUse`, `getToElementTypesUseQueryOrElementsList`, `setCellElementTypes`, `setFromElementTypes`, `setFromElementTypesQueryToUse`, `setFromElementTypesUseQueryOrElementsList`, `setToElementTypes`, `setToElementTypesQueryToUse`, `setToElementTypesUseQueryOrElementsList` (14)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPMatrixLayout with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.core import RPCollection
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPMatrixLayout, RPTableLayout


@pytest.mark.integration
class TestRPMatrixLayoutIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_element_types_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("MLPkg"))
        try:
            matrix = pkg.add_new_aggr("MatrixLayout", self._unique("Matrix"))
            assert isinstance(matrix, RPMatrixLayout)
            from_types = matrix.get_from_element_types()
            assert isinstance(from_types, RPCollection)
            to_types = matrix.get_to_element_types()
            assert isinstance(to_types, RPCollection)
            cell_types = matrix.get_cell_element_types()
            assert isinstance(cell_types, RPCollection)
            assert matrix.get_from_element_types_use_query_or_elements_list() in (0, 1)
            assert matrix.get_to_element_types_use_query_or_elements_list() in (0, 1)
        finally:
            matrix.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_set_cell_element_types / set_from_element_types / set_to_element_types: build a
    #   RPCollection of metaclass-name strings (or model elements, per COM contract — verify live)
    #   and roundtrip via the matching getter
    # - test_from_element_types_query_to_use roundtrip: create an RPTableLayout via
    #   pkg.add_new_aggr("TableLayout", name) as query, matrix.set_from_element_types_query_to_use(query),
    #   assert matrix.get_from_element_types_query_to_use() == query
    # - test_to_element_types_query_to_use roundtrip: mirror the above for "to" element types
    # - test_use_query_or_elements_list setters: set_from_element_types_use_query_or_elements_list(1)
    #   (QUERY) / (0) (ELEMENTS_LIST) then assert matching getter reflects it
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_matrix_layout.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

Flip all 14 `RPMatrixLayout` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_matrix_layout.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPMatrixLayout"
```

---

### Task 9: RPMatrixView — cells & content (Part A)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_matrix_view.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getCellElements`, `getCellString`, `getColumnCount`, `getContent`, `getFromScope`, `getHTMLContent`, `getImageCollection`, `getItsMatrixLayout`, `getRowCount`, `getToScope` (10)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPMatrixView with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPMatrixLayout, RPMatrixView


@pytest.mark.integration
class TestRPMatrixViewIntegrationPartA:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def _build_matrix_view(self, test_project: RPProject):
        pkg = self._create_package(test_project, self._unique("MVPkg"))
        layout = pkg.add_new_aggr("MatrixLayout", self._unique("Layout"))
        view = pkg.add_new_aggr("MatrixView", self._unique("View"))
        view.set_its_matrix_layout(layout)
        return pkg, layout, view

    def test_row_and_column_counts(self, test_project: RPProject) -> None:
        pkg, layout, view = self._build_matrix_view(test_project)
        try:
            assert isinstance(view, RPMatrixView)
            assert isinstance(layout, RPMatrixLayout)
            assert view.get_its_matrix_layout() == layout
            assert view.get_row_count() >= 0
            assert view.get_column_count() >= 0
        finally:
            view.delete_from_project()
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_cell_elements / get_cell_string: after populating the matrix layout's from/to/cell
    #   element types (Task 8), call view.get_cell_elements(0, 0) / view.get_cell_string(0, 0)
    # - test_get_content: view.get_content("HTML") or another ContentFormat constant
    # - test_get_html_content: view.get_html_content() -> str
    # - test_get_image_collection: view.get_image_collection() -> RPCollection
    # - test_get_from_scope / get_to_scope: view.get_from_scope() / get_to_scope() -> wrapped scope
    #   element or None
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_matrix_view.py -m integration -v -k PartA`

- [ ] **Step 3: Flip checklist boxes**

Flip the 10 listed `RPMatrixView` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_matrix_view.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPMatrixView (part A)"
```

---

### Task 10: RPMatrixView — scope, descendants & view management (Part B)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_matrix_view.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `setFromScope`, `setItsMatrixLayout`, `setToScope`, `updateViewOnServer`, `getIncludeDescendantsFromScope`, `getIncludeDescendantsToScope`, `open`, `setIncludeDescendantsFromScope`, `setIncludeDescendantsToScope` (9)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPMatrixViewIntegrationPartB:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_scope_and_descendants_roundtrip(self, test_project: RPProject) -> None:
        pkg, layout, view = TestRPMatrixViewIntegrationPartA()._build_matrix_view(test_project)
        try:
            pkg2 = pkg.add_nested_package(self._unique("ScopePkg"))
            view.set_from_scope(pkg2)
            assert view.get_from_scope() == pkg2
            view.set_to_scope(pkg2)
            assert view.get_to_scope() == pkg2
            view.set_include_descendants_from_scope(1)
            assert view.get_include_descendants_from_scope() == 1
            view.set_include_descendants_to_scope(1)
            assert view.get_include_descendants_to_scope() == 1
        finally:
            view.delete_from_project()
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_set_its_matrix_layout: swap to a second RPMatrixLayout and confirm get_its_matrix_layout()
    #   reflects the new association
    # - test_update_view_on_server: view.update_view_on_server() -> no exception raised
    # - test_open: view.open() -> no exception raised (opens the view window in the IDE)
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_matrix_view.py -m integration -v -k PartB`

- [ ] **Step 3: Flip checklist boxes**

Flip the 9 listed `RPMatrixView` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_matrix_view.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPMatrixView (part B)"
```

---

### Task 11: RPMessagePoint — full checklist

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_message_point.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getClassifierRole`, `getInteractionOccurrence`, `getInteractionOperator`, `getMessage`, `getType` (5)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPMessagePoint with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPMessagePoint


@pytest.mark.integration
class TestRPMessagePointIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_message_points_from_sequence_diagram(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("MPPkg"))
        try:
            diagram = pkg.add_sequence_diagram(self._unique("SeqD"))
            collaboration = diagram.get_owner()  # RPCollaboration backing the sequence diagram
            role1 = diagram.add_new_node_by_type("ClassifierRole", 10, 10, 60, 100)
            role2 = diagram.add_new_node_by_type("ClassifierRole", 200, 10, 60, 100)
            diagram.add_new_edge_by_type("Message", role1, role2)
            message_points = list(collaboration.get_message_points())
            assert message_points, "Expected at least one IRPMessagePoint after adding a message"
            point = message_points[0]
            assert isinstance(point, RPMessagePoint)
            assert isinstance(point.get_type(), str)
            assert point.get_classifier_role() in (role1, role2, None)
            assert point.get_message() is not None
        finally:
            diagram.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_interaction_occurrence: build a message point on a message inside an interaction
    #   occurrence (CombinedFragment "ref") and assert isinstance of the wrapped occurrence
    # - test_get_interaction_operator: build a message point inside a CombinedFragment (e.g. "alt")
    #   and assert isinstance of the wrapped operator
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_message_point.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

Flip all 5 `RPMessagePoint` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_message_point.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPMessagePoint"
```

---

### Task 12: RPTableLayout — columns & basic query attributes (Part A)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_table_layout.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `addColumn`, `addColumnEx`, `getCollapseFirstColumn`, `getColumnContext`, `getColumnDefaultWidth`, `getColumnImplementationAllowNew`, `getColumnImplementationAllowSelect`, `getColumnImplementationCellType`, `getColumnImplementationDisplayProperty`, `getColumnImplementationGetterCode`, `getColumnImplementationImports`, `getColumnImplementationPickerCode`, `getColumnImplementationSetterCode` (13)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPTableLayout with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPTableLayout


@pytest.mark.integration
class TestRPTableLayoutIntegrationPartA:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_add_column_and_read_attributes(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("TLPkg"))
        try:
            layout = pkg.add_new_aggr("TableLayout", self._unique("Layout"))
            assert isinstance(layout, RPTableLayout)
            column_name = self._unique("Col")
            layout.add_column(column_name, "String")
            columns = list(layout.get_columns())
            assert any(True for _ in columns)  # column collection is populated
            assert layout.get_collapse_first_column() in (0, 1)
            assert layout.get_column_default_width(column_name) >= 0
        finally:
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_add_column_ex: layout.add_column_ex(name, type_, position) and verify ordering via
    #   get_columns()
    # - test_get_column_context: layout.get_column_context(column_name) -> str
    # - test_get_column_implementation_* (AllowNew/AllowSelect/CellType/DisplayProperty/GetterCode/
    #   Imports/PickerCode/SetterCode): each reads back the corresponding attribute set in Task 13's
    #   setter tests, or asserts a sane default (empty string / 0) on a freshly added column
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_layout.py -m integration -v -k PartA`

- [ ] **Step 3: Flip checklist boxes**

Flip the 13 listed `RPTableLayout` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_layout.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableLayout (part A)"
```

---

### Task 13: RPTableLayout — column/type getters & query results (Part B)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_table_layout.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getColumnName`, `getColumnProperty`, `getColumnType`, `getColumns`, `getElementTypes`, `getFromElementTypes`, `getFromElementTypesQueryToUse`, `getFromElementTypesUseQueryOrElementsList`, `getRelationTable`, `getResultList`, `getToElementTypes`, `getToElementTypesQueryToUse`, `getToElementTypesUseQueryOrElementsList` (13)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPTableLayoutIntegrationPartB:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_column_name_and_type(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("TLPkgB"))
        try:
            layout = pkg.add_new_aggr("TableLayout", self._unique("Layout"))
            column_name = self._unique("Col")
            layout.add_column(column_name, "String")
            columns = list(layout.get_columns())
            assert columns
            first_col_name = layout.get_column_name(0)
            assert isinstance(first_col_name, str)
            assert isinstance(layout.get_column_type(0), str)
            assert isinstance(layout.get_element_types(), object)
            assert isinstance(layout.get_from_element_types(), object)
            assert isinstance(layout.get_to_element_types(), object)
            assert layout.get_relation_table() in (0, 1)
            result_list = list(layout.get_result_list())
            assert isinstance(result_list, list)
        finally:
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_column_property: layout.get_column_property(0, "SomeKey") -> str or None
    # - test_get_from/to_element_types_query_to_use: build a second RPTableLayout used as a sub-query
    #   via set_from_element_types_query_to_use (Task 15) and read it back here
    # - test_get_from/to_element_types_use_query_or_elements_list: assert the QueryOrElementsList
    #   constant (0 or 1) matches whatever Task 15 sets
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_layout.py -m integration -v -k PartB`

- [ ] **Step 3: Flip checklist boxes**

Flip the 13 listed `RPTableLayout` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_layout.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableLayout (part B)"
```

---

### Task 14: RPTableLayout — column removal & implementation setters (Part C)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_table_layout.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `removeColumn`, `setCollapseFirstColumn`, `setColumnContext`, `setColumnDefaultWidth`, `setColumnImplementationAllowNew`, `setColumnImplementationAllowSelect`, `setColumnImplementationCellType`, `setColumnImplementationDisplayProperty`, `setColumnImplementationGetterCode`, `setColumnImplementationImports`, `setColumnImplementationPickerCode`, `setColumnImplementationSetterCode`, `setColumnName` (13)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPTableLayoutIntegrationPartC:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_set_column_name_and_remove_column(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("TLPkgC"))
        try:
            layout = pkg.add_new_aggr("TableLayout", self._unique("Layout"))
            column_name = self._unique("Col")
            layout.add_column(column_name, "String")
            renamed = self._unique("ColRenamed")
            layout.set_column_name(0, renamed)
            assert layout.get_column_name(0) == renamed
            layout.set_collapse_first_column(1)
            assert layout.get_collapse_first_column() == 1
            layout.set_column_default_width(0, 150)
            assert layout.get_column_default_width(0) == 150
            layout.remove_column(0)
            assert len(list(layout.get_columns())) == 0
        finally:
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_set_column_context: layout.set_column_context(0, "SomeContext") -> get_column_context
    #   roundtrip (Task 12/13 getter)
    # - test_set_column_implementation_* (AllowNew/AllowSelect/CellType/DisplayProperty/GetterCode/
    #   Imports/PickerCode/SetterCode): set each attribute on a freshly-added column, then verify via
    #   the matching Task 12 getter (add these assertions to the Part A test file, or re-fetch the
    #   layout here and assert directly)
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_layout.py -m integration -v -k PartC`

- [ ] **Step 3: Flip checklist boxes**

Flip the 13 listed `RPTableLayout` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_layout.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableLayout (part C)"
```

---

### Task 15: RPTableLayout — element-type/query setters & column count (Part D)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_table_layout.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `setColumnProperty`, `setColumnType`, `setElementTypes`, `setFromElementTypes`, `setFromElementTypesQueryToUse`, `setFromElementTypesUseQueryOrElementsList`, `setRelationTable`, `setToElementTypes`, `setToElementTypesQueryToUse`, `setToElementTypesUseQueryOrElementsList`, `getColumnCount` (11)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPTableLayoutIntegrationPartD:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_column_count_and_relation_table_flag(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("TLPkgD"))
        try:
            layout = pkg.add_new_aggr("TableLayout", self._unique("Layout"))
            layout.add_column(self._unique("Col1"), "String")
            layout.add_column(self._unique("Col2"), "String")
            assert layout.get_column_count() == 2
            layout.set_column_type(0, "Integer")
            layout.set_relation_table(1)
            assert layout.get_relation_table() == 1
        finally:
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_set_column_property: layout.set_column_property(0, "SomeKey", "SomeValue") -> read back
    #   via get_column_property (Task 13 getter)
    # - test_set_element_types / set_from_element_types / set_to_element_types: build an RPCollection
    #   of metaclass-name strings and roundtrip via the matching Task 13 getters
    # - test_set_from/to_element_types_query_to_use: build a second RPTableLayout as a sub-query,
    #   set via setter, verify via Task 13's getter
    # - test_set_from/to_element_types_use_query_or_elements_list: set 0/1 and verify via Task 13's
    #   getter
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_layout.py -m integration -v -k PartD`

- [ ] **Step 3: Flip checklist boxes**

Flip the 11 listed `RPTableLayout` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_layout.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableLayout (part D)"
```

---

### Task 16: RPTableView — cells, content & layout linkage (Part A)

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_table_view.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getCellElements`, `getCellString`, `getColumnCount`, `getContent`, `getHTMLContent`, `getImageCollection`, `getItsTableLayout`, `getRowCount`, `getScope` (9)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPTableView with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPTableLayout, RPTableView


@pytest.mark.integration
class TestRPTableViewIntegrationPartA:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def _build_table_view(self, test_project: RPProject):
        pkg = self._create_package(test_project, self._unique("TVPkg"))
        layout = pkg.add_new_aggr("TableLayout", self._unique("Layout"))
        view = pkg.add_new_aggr("TableView", self._unique("View"))
        view.set_its_table_layout(layout)
        return pkg, layout, view

    def test_row_column_counts_and_layout_link(self, test_project: RPProject) -> None:
        pkg, layout, view = self._build_table_view(test_project)
        try:
            assert isinstance(view, RPTableView)
            assert isinstance(layout, RPTableLayout)
            assert view.get_its_table_layout() == layout
            assert view.get_row_count() >= 0
            assert view.get_column_count() >= 0
        finally:
            view.delete_from_project()
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_cell_elements / get_cell_string: after adding rows/columns to the layout, verify cell
    #   content via view.get_cell_elements(0, 0) / view.get_cell_string(0, 0)
    # - test_get_content: view.get_content("HTML") or another ContentFormat constant
    # - test_get_html_content: view.get_html_content() -> str
    # - test_get_image_collection: view.get_image_collection() -> RPCollection
    # - test_get_scope: view.get_scope() -> wrapped scope element or None
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_view.py -m integration -v -k PartA`

- [ ] **Step 3: Flip checklist boxes**

Flip the 9 listed `RPTableView` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_view.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableView (part A)"
```

---

### Task 17: RPTableView — scope, descendants & view management (Part B)

**Files:**
- Modify: `tests/integration/models/elements/graphics/test_model_table_view.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getUseOwnerScope`, `setItsTableLayout`, `setScope`, `setUseOwnerScope`, `updateViewOnServer`, `getIncludeDescendants`, `open`, `setIncludeDescendants` (8)

- [ ] **Step 1: Write the failing/new integration tests**

```python
class TestRPTableViewIntegrationPartB:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_scope_and_descendants_roundtrip(self, test_project: RPProject) -> None:
        pkg, layout, view = TestRPTableViewIntegrationPartA()._build_table_view(test_project)
        try:
            pkg2 = pkg.add_nested_package(self._unique("ScopePkg"))
            view.set_scope(pkg2)
            assert view.get_scope() == pkg2
            view.set_use_owner_scope(1)
            assert view.get_use_owner_scope() == 1
            view.set_include_descendants(1)
            assert view.get_include_descendants() == 1
        finally:
            view.delete_from_project()
            layout.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_set_its_table_layout: swap to a second RPTableLayout and confirm get_its_table_layout()
    #   reflects the new association
    # - test_update_view_on_server: view.update_view_on_server() -> no exception raised
    # - test_open: view.open() -> no exception raised (opens the view window in the IDE)
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_table_view.py -m integration -v -k PartB`

- [ ] **Step 3: Flip checklist boxes**

Flip the 8 listed `RPTableView` rows above.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_table_view.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPTableView (part B)"
```

---

### Task 18: RPPin — full checklist

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_pin.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:** `getIsParameter`, `getPinDirection`, `getPinType`, `setIsParameter`, `setPinDirection`, `setPinType` (6)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPPin with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.classifiers import RPClass
from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPPin


@pytest.mark.integration
class TestRPPinIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_pin_direction_and_type_roundtrip(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("PinPkg"))
        try:
            flowchart_pkg = pkg.add_activity_diagram(self._unique("Flow"))
            flow = flowchart_pkg.get_owner()  # RPFlow backing the activity diagram
            pin = flow.add_activity_parameter(self._unique("Param"))
            assert isinstance(pin, RPPin)
            assert pin.get_pin_direction() in ("In", "Out", "InOut", "")
            pin.set_pin_direction("In")
            assert pin.get_pin_direction() == "In"
            pin_class = pkg.add_class(self._unique("PinType"))
            pin.set_pin_type(pin_class)
            assert pin.get_pin_type() == pin_class
        finally:
            flowchart_pkg.delete_from_project()

    # For remaining methods, follow the same pattern:
    # - test_get_is_parameter / set_is_parameter: roundtrip 0/1
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_pin.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

Flip all 6 `RPPin` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_pin.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPPin"
```

---

### Task 19: RPGraphEdge & RPGraphNode — full checklists

**Files:**
- Create: `tests/integration/models/elements/graphics/test_model_graph_edge_node.py`
- Modify: `src/rhapsody_cli/models/elements/graphics/model_graphics.py`

**Methods covered:**
- `RPGraphEdge`: `embedFlow`, `embedNewFlow`, `getContainingArrow`, `getSource`, `getTarget` (5)
- `RPGraphNode`: `bringToFront`, `getIsPanelWidget`, `getPanelWidgetInstancePath`, `hideAllPorts`, `sendToBack`, `setPanelWidgetInstancePath`, `showAllPorts` (7)

- [ ] **Step 1: Write the failing/new integration tests**

```python
"""Integration tests for RPGraphEdge and RPGraphNode with live Rhapsody COM API."""

import uuid

import pytest

from rhapsody_cli.models.elements.containment import RPPackage, RPProject
from rhapsody_cli.models.elements.graphics import RPGraphEdge, RPGraphNode


@pytest.mark.integration
class TestRPGraphNodeIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _create_package(project: RPProject, name: str) -> RPPackage:
        pkg = project.add_package(name)
        assert pkg is not None and isinstance(pkg, RPPackage)
        return pkg

    def test_bring_to_front_and_send_to_back(self, test_project: RPProject) -> None:
        pkg = self._create_package(test_project, self._unique("NodePkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            node = diagram.add_new_node_by_type("State", 10, 10, 80, 40)
            assert isinstance(node, RPGraphNode)
            node.bring_to_front()
            node.send_to_back()
            node.hide_all_ports()
            node.show_all_ports()
            assert node.get_is_panel_widget() in (0, 1)
        finally:
            diagram.delete_from_project()

    # For remaining RPGraphNode methods, follow the same pattern:
    # - test_panel_widget_instance_path: build a node in a panel diagram
    #   (pkg.add_panel_diagram(name)), call get_panel_widget_instance_path() /
    #   set_panel_widget_instance_path("SomePath") roundtrip


@pytest.mark.integration
class TestRPGraphEdgeIntegration:
    @staticmethod
    def _unique(prefix: str = "Test") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    def test_get_source_and_target(self, test_project: RPProject) -> None:
        pkg = test_project.add_package(self._unique("EdgePkg"))
        try:
            diagram = pkg.add_statechart_diagram(self._unique("SD"))
            state1 = diagram.add_new_node_by_type("State", 10, 10, 80, 40)
            state2 = diagram.add_new_node_by_type("State", 200, 10, 80, 40)
            edge = diagram.add_new_edge_by_type("Transition", state1, state2)
            assert isinstance(edge, RPGraphEdge)
            assert edge.get_source() == state1
            assert edge.get_target() == state2
        finally:
            diagram.delete_from_project()

    # For remaining RPGraphEdge methods, follow the same pattern:
    # - test_get_containing_arrow: build a nested edge scenario (e.g. an edge routed within a
    #   composite arrow/connector group) and assert isinstance of the wrapped containing arrow
    # - test_embed_flow / embed_new_flow: on an activity-diagram edge (control/object flow), call
    #   edge.embed_new_flow() and assert the edge now returns itself/a valid flow wrapper per the
    #   documented "Returns self" unit-test behavior (see test_model_graphics.py
    #   TestRPGraphEdgeTask15.test_embed_new_flow_returns_self for the expected contract)
```

- [ ] **Step 2: Run the new tests against live Rhapsody**

Run: `pytest tests/integration/models/elements/graphics/test_model_graph_edge_node.py -m integration -v`

- [ ] **Step 3: Flip checklist boxes**

Flip all 5 `RPGraphEdge` rows and all 7 `RPGraphNode` rows.

- [ ] **Step 4: Run quality gate**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 5: Commit**

```bash
git add tests/integration/models/elements/graphics/test_model_graph_edge_node.py src/rhapsody_cli/models/elements/graphics/model_graphics.py
git commit -m "test: add integration tests for RPGraphEdge and RPGraphNode"
```

---

### Task 20: Full Subpackage Verification

**Files:** none (verification only)

- [ ] **Step 1: Confirm zero remaining `[ ] integration test` rows in the graphics subpackage**

Run:
```bash
grep -c "\[ \] integration test" src/rhapsody_cli/models/elements/graphics/model_graphics.py
```
Expected output: `0`.

- [ ] **Step 2: Run the entire graphics integration suite together**

Run: `pytest tests/integration/models/elements/graphics/ -m integration -v`

- [ ] **Step 3: Run the full quality gate one final time**

Run: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`

- [ ] **Step 4: Run the full integration suite (not just graphics) to check for regressions**

Run: `pytest tests/integration/ -m integration -v`

- [ ] **Step 5: Final commit (if any cleanup remains)**

```bash
git add -A
git commit -m "test: complete integration test coverage for graphics subpackage (190/190 methods)"
```
