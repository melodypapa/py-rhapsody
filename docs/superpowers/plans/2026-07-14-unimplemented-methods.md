# Unimplemented Methods Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement 73 unimplemented methods across 4 model files, following Patterns A-G (see AGENTS.md).

**Context:** Codebase audit revealed 73 methods marked `[ ] impl` across `core.py`, `model_package.py`, `model_project.py`, and `model_actor.py`. These are COM API wrappers that need implementation.

## Global Constraints

- All implementations follow COM Wrapping Rules (AGENTS.md)
- All methods use snake_case naming
- Unit tests required for each method
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- Commit after each task with conventional commit format
- Import via subpackage `__init__.py` re-exports

---

## Summary Table

| File | Class | Methods | Category |
|------|-------|---------|----------|
| `core.py` | `RPCollection` | 8 | Collection utilities |
| `model_package.py` | `RPPackage` | 24 | Package-level operations |
| `model_project.py` | `RPProject` | 41 | Project-level operations |
| `model_actor.py` | `RPActor` | 1 | Actor-specific |
| **Total** | | **73** | |

---

## Task 1: RPCollection Utility Methods (8 methods)

**File:** `src/rhapsody_cli/models/core.py`

**Methods:**
1. `addGraphicalItem` → `add_graphical_item(item)`
2. `toList` → `to_list()`
3. `setSize` → `set_size(size)`
4. `remove` → `remove(index)`
5. `setString` → `set_string(index, value)`
6. `setModelElement` → `set_model_element(index, element)`
7. `empty` → `empty()`
8. `setInteger` → `set_integer(index, value)`

**Implementation Notes:**
- All methods are simple COM pass-throughs (Pattern A or F)
- `addGraphicalItem` returns `None` (void)
- `toList` returns `list` (Python list from COM collection)
- `setSize`, `remove`, `empty` return `None` (void)
- `setString`, `setModelElement`, `setInteger` return `None` (void)

**Steps:**

- [ ] **Step 1:** Implement `add_graphical_item(item: RPModelElement) -> None` using Pattern F
- [ ] **Step 2:** Implement `to_list() -> list` using Pattern A (returns `list(self)`)
- [ ] **Step 3:** Implement `set_size(size: int) -> None` using Pattern F
- [ ] **Step 4:** Implement `remove(index: int) -> None` using Pattern F
- [ ] **Step 5:** Implement `set_string(index: int, value: str) -> None` using Pattern F
- [ ] **Step 6:** Implement `set_model_element(index: int, element: RPModelElement) -> None` using Pattern F
- [ ] **Step 7:** Implement `empty() -> None` using Pattern F
- [ ] **Step 8:** Implement `set_integer(index: int, value: int) -> None` using Pattern F
- [ ] **Step 9:** Write unit tests for all 8 methods in `tests/unit/models/test_core.py`
- [ ] **Step 10:** Update checklist markers to `[x] impl`, `[x] docstring`, `[x] unit test`
- [ ] **Step 11:** Run quality gate
- [ ] **Step 12:** Commit: `feat(models): implement RPCollection utility methods (8 methods)`

---

## Task 2: RPPackage Flow Methods (6 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_package.py`

**Methods:**
1. `addFlowItems` → `add_flow_items(name: str) -> RPFlowItem`
2. `addFlows` → `add_flows(name: str) -> RPFlow`
3. `deleteFlowItems` → `delete_flow_items(flow_item: RPFlowItem) -> None`
4. `deleteFlows` → `delete_flows(flow: RPFlow) -> None`
5. `getFlowItems` → `get_flow_items() -> RPCollection`
6. `getFlows` → `get_flows() -> RPCollection`

**Implementation Notes:**
- Pattern E for adders (wrap returned COM object)
- Pattern F for deleters (void)
- Pattern C for getters (return RPCollection)

**Steps:**

- [ ] **Step 1:** Implement `add_flow_items(name: str) -> RPFlowItem` using Pattern E
- [ ] **Step 2:** Implement `add_flows(name: str) -> RPFlow` using Pattern E
- [ ] **Step 3:** Implement `delete_flow_items(flow_item: RPFlowItem) -> None` using Pattern F
- [ ] **Step 4:** Implement `delete_flows(flow: RPFlow) -> None` using Pattern F
- [ ] **Step 5:** Implement `get_flow_items() -> RPCollection` using Pattern C
- [ ] **Step 6:** Implement `get_flows() -> RPCollection` using Pattern C
- [ ] **Step 7:** Write unit tests in `tests/unit/models/elements/test_package.py`
- [ ] **Step 8:** Update checklist markers
- [ ] **Step 9:** Run quality gate
- [ ] **Step 10:** Commit: `feat(models): implement RPPackage flow methods (6 methods)`

---

## Task 3: RPPackage Remote Requirements Methods (7 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_package.py`

**Methods:**
1. `getRemoteRequirementsPopulateMode` → `get_remote_requirements_populate_mode() -> int`
2. `getRootInstanceSpecifications` → `get_root_instance_specifications() -> RPCollection`
3. `loginToRemoteArtifactServer` → `login_to_remote_artifact_server(server_url: str, username: str, password: str) -> None`
4. `populateRemoteRequirements` → `populate_remote_requirements() -> None`
5. `reCalculateEventsBaseId` → `recalculate_events_base_id() -> None`
6. `setRemoteRequirementsPopulateMode` → `set_remote_requirements_populate_mode(mode: int) -> None`
7. `updateContainedDiagramsOnServer` → `update_contained_diagrams_on_server() -> None`

**Implementation Notes:**
- Remote requirements methods require Rhapsody Model Manager integration
- Pattern A for getters (return primitive)
- Pattern C for getters returning collections
- Pattern F for void methods
- Pattern D for setters

**Steps:**

- [ ] **Step 1:** Implement `get_remote_requirements_populate_mode() -> int` using Pattern A
- [ ] **Step 2:** Implement `get_root_instance_specifications() -> RPCollection` using Pattern C
- [ ] **Step 3:** Implement `login_to_remote_artifact_server(server_url, username, password) -> None` using Pattern F (multi-arg setter)
- [ ] **Step 4:** Implement `populate_remote_requirements() -> None` using Pattern F
- [ ] **Step 5:** Implement `recalculate_events_base_id() -> None` using Pattern F
- [ ] **Step 6:** Implement `set_remote_requirements_populate_mode(mode: int) -> None` using Pattern D
- [ ] **Step 7:** Implement `update_contained_diagrams_on_server() -> None` using Pattern F
- [ ] **Step 8:** Write unit tests
- [ ] **Step 9:** Update checklist markers
- [ ] **Step 10:** Run quality gate
- [ ] **Step 11:** Commit: `feat(models): implement RPPackage remote requirements methods (7 methods)`

---

## Task 4: RPPackage SysML Methods (2 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_package.py`

**Methods:**
1. `addImplicitObject` → `add_implicit_object(name: str) -> RPInstance`
2. `addLinkBetweenSYSMLPorts` → `add_link_between_sysml_ports(port1: RPSysMLPort, port2: RPSysMLPort) -> RPLink`

**Implementation Notes:**
- SysML-specific methods
- Pattern E for adders
- Multi-arg adder for `addLinkBetweenSYSMLPorts`

**Steps:**

- [ ] **Step 1:** Implement `add_implicit_object(name: str) -> RPInstance` using Pattern E
- [ ] **Step 2:** Implement `add_link_between_sysml_ports(port1, port2) -> RPLink` using Pattern E (multi-arg)
- [ ] **Step 3:** Write unit tests
- [ ] **Step 4:** Update checklist markers
- [ ] **Step 5:** Run quality gate
- [ ] **Step 6:** Commit: `feat(models): implement RPPackage SysML methods (2 methods)`

---

## Task 5: RPPackage Misc Methods (9 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_package.py`

**Methods:**
1. `getAllNestedElements` → `get_all_nested_elements() -> RPCollection`
2. `getEventsBaseId` → `get_events_base_id() -> str`
3. `getNamespace` → `get_namespace() -> str`
4. `getSavedInSeperateDirectory` → `get_saved_in_separate_directory() -> int`
5. `getUserDefinedStereotypes` → `get_user_defined_stereotypes() -> RPCollection`
6. `setSavedInSeperateDirectory` → `set_saved_in_separate_directory(value: int) -> None`
7. `updateContainedMatricesOnServer` → `update_contained_matrices_on_server() -> None`
8. `updateContainedTablesOnServer` → `update_contained_tables_on_server() -> None`
9. `getEventsBaseId` (if not covered in Task 3)

**Implementation Notes:**
- Pattern A for getters returning primitives
- Pattern C for getters returning collections
- Pattern D for setters
- Pattern F for void methods

**Steps:**

- [ ] **Step 1:** Implement `get_all_nested_elements() -> RPCollection` using Pattern C
- [ ] **Step 2:** Implement `get_events_base_id() -> str` using Pattern A
- [ ] **Step 3:** Implement `get_namespace() -> str` using Pattern A
- [ ] **Step 4:** Implement `get_saved_in_separate_directory() -> int` using Pattern A
- [ ] **Step 5:** Implement `get_user_defined_stereotypes() -> RPCollection` using Pattern C
- [ ] **Step 6:** Implement `set_saved_in_separate_directory(value: int) -> None` using Pattern D
- [ ] **Step 7:** Implement `update_contained_matrices_on_server() -> None` using Pattern F
- [ ] **Step 8:** Implement `update_contained_tables_on_server() -> None` using Pattern F
- [ ] **Step 9:** Write unit tests
- [ ] **Step 10:** Update checklist markers
- [ ] **Step 11:** Run quality gate
- [ ] **Step 12:** Commit: `feat(models): implement RPPackage misc methods (9 methods)`

---

## Task 6: RPProject Gateway/Report Methods (3 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `gatewayExportToXML` → `gateway_export_to_xml(file_path: str) -> None`
2. `gatewayExportToXML2` → `gateway_export_to_xml2(file_path: str, options: str) -> None`
3. `generateReport` → `generate_report(template_path: str, output_path: str) -> None`

**Implementation Notes:**
- Gateway methods for IBM Rational Publishing Engine integration
- Pattern F for void methods

**Steps:**

- [ ] **Step 1:** Implement `gateway_export_to_xml(file_path: str) -> None` using Pattern F
- [ ] **Step 2:** Implement `gateway_export_to_xml2(file_path: str, options: str) -> None` using Pattern F (multi-arg)
- [ ] **Step 3:** Implement `generate_report(template_path: str, output_path: str) -> None` using Pattern F (multi-arg)
- [ ] **Step 4:** Write unit tests
- [ ] **Step 5:** Update checklist markers
- [ ] **Step 6:** Run quality gate
- [ ] **Step 7:** Commit: `feat(models): implement RPProject gateway/report methods (3 methods)`

---

## Task 7: RPProject Custom Views Methods (7 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `addCustomViewOnBrowser` → `add_custom_view_on_browser(view: RPCustomView) -> None`
2. `addCustomViewOnDiagram` → `add_custom_view_on_diagram(view: RPCustomView) -> None`
3. `applyBrowserCustomViewsOnDiagrams` → `apply_browser_custom_views_on_diagrams() -> None`
4. `getActiveCustomViewsOnBrowser` → `get_active_custom_views_on_browser() -> RPCollection`
5. `getActiveCustomViewsOnDiagram` → `get_active_custom_views_on_diagram() -> RPCollection`
6. `removeCustomViewOnBrowser` → `remove_custom_view_on_browser(view: RPCustomView) -> None`
7. `removeCustomViewOnDiagram` → `remove_custom_view_on_diagram(view: RPCustomView) -> None`

**Implementation Notes:**
- Custom views for Rhapsody browser/diagram filtering
- Pattern F for adders/removers (void)
- Pattern C for getters (return RPCollection)

**Steps:**

- [ ] **Step 1:** Implement all 7 methods following Patterns C and F
- [ ] **Step 2:** Write unit tests
- [ ] **Step 3:** Update checklist markers
- [ ] **Step 4:** Run quality gate
- [ ] **Step 5:** Commit: `feat(models): implement RPProject custom views methods (7 methods)`

---

## Task 8: RPProject CSV Methods (3 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `closeCSVFile` → `close_csv_file() -> None`
2. `openCSVFile` → `open_csv_file(file_path: str, mode: int) -> None`
3. `reloadCSVFile` → `reload_csv_file() -> None`

**Implementation Notes:**
- CSV file handling for requirements import
- Pattern F for void methods

**Steps:**

- [ ] **Step 1:** Implement all 3 methods using Pattern F
- [ ] **Step 2:** Write unit tests
- [ ] **Step 3:** Update checklist markers
- [ ] **Step 4:** Run quality gate
- [ ] **Step 5:** Commit: `feat(models): implement RPProject CSV methods (3 methods)`

---

## Task 9: RPProject Remote/Roundtrip Methods (7 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `applyRoundtripDiffMerge` → `apply_roundtrip_diff_merge() -> None`
2. `enableRhapsodyModelManager` → `enable_rhapsody_model_manager(enabled: int) -> None`
3. `findElementsWithOSLCLink` → `find_elements_with_oslc_link(link: str) -> RPCollection`
4. `getRemoteResourcePackages` → `get_remote_resource_packages() -> RPCollection`
5. `getRoundtripShadowModel` → `get_roundtrip_shadow_model() -> RPModel`
6. `isActivelyManaged` → `is_actively_managed() -> int`
7. `migrateDesignManagerLinks` → `migrate_design_manager_links() -> None`

**Implementation Notes:**
- Model Manager and Design Manager integration methods
- Pattern A for getters returning primitives
- Pattern C for getters returning collections
- Pattern B for getters returning wrapped elements
- Pattern F for void methods

**Steps:**

- [ ] **Step 1:** Implement all 7 methods following Patterns A, B, C, F
- [ ] **Step 2:** Write unit tests
- [ ] **Step 3:** Update checklist markers
- [ ] **Step 4:** Run quality gate
- [ ] **Step 5:** Commit: `feat(models): implement RPProject remote/roundtrip methods (7 methods)`

---

## Task 10: RPProject Rose Import Methods (2 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `importPackageFromRose` → `import_package_from_rose(file_path: str) -> RPPackage`
2. `importProjectFromRose` → `import_project_from_rose(file_path: str) -> None`

**Implementation Notes:**
- Rose model import (legacy)
- Pattern E for adder returning wrapped element
- Pattern F for void method

**Steps:**

- [ ] **Step 1:** Implement `import_package_from_rose(file_path: str) -> RPPackage` using Pattern E
- [ ] **Step 2:** Implement `import_project_from_rose(file_path: str) -> None` using Pattern F
- [ ] **Step 3:** Write unit tests
- [ ] **Step 4:** Update checklist markers
- [ ] **Step 5:** Run quality gate
- [ ] **Step 6:** Commit: `feat(models): implement RPProject Rose import methods (2 methods)`

---

## Task 11: RPProject Events Methods (2 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `checkEventsBaseIdsSolveCollisions` → `check_events_base_ids_solve_collisions() -> int`
2. `recalculateEventsBaseIds` → `recalculate_events_base_ids() -> None`

**Implementation Notes:**
- Event base ID management
- Pattern A for getter returning int
- Pattern F for void method

**Steps:**

- [ ] **Step 1:** Implement `check_events_base_ids_solve_collisions() -> int` using Pattern A
- [ ] **Step 2:** Implement `recalculate_events_base_ids() -> None` using Pattern F
- [ ] **Step 3:** Write unit tests
- [ ] **Step 4:** Update checklist markers
- [ ] **Step 5:** Run quality gate
- [ ] **Step 6:** Commit: `feat(models): implement RPProject events methods (2 methods)`

---

## Task 12: RPProject Misc Methods (19 methods)

**File:** `src/rhapsody_cli/models/elements/containment/model_project.py`

**Methods:**
1. `addSpellCheckerResult` → `add_spell_checker_result(word: str, suggestion: str) -> None`
2. `cleanUnresolvedElements` → `clean_unresolved_elements() -> None`
3. `endTransactionOfNoCGInterest` → `end_transaction_of_no_cg_interest() -> None`
4. `getDefaultDirectoryScheme` → `get_default_directory_scheme() -> int`
5. `getNewProgressBar` → `get_new_progress_bar() -> RPProgressBar`
6. `getNotifyPluginOnElementsChanged` → `get_notify_plugin_on_elements_changed() -> int`
7. `getRequirementsByID` → `get_requirements_by_id(id: str) -> RPCollection`
8. `remove` → `remove() -> None`
9. `saveAsPrevVersion` → `save_as_prev_version(file_path: str) -> None`
10. `setDefaultDirectoryScheme` → `set_default_directory_scheme(scheme: int) -> None`
11. `setGlobalConfiguration` → `set_global_configuration(config: str) -> None`
12. `setNotifyPluginOnElementsChanged` → `set_notify_plugin_on_elements_changed(enabled: int) -> None`
13. `setObjectExplicit` → `set_object_explicit(obj: RPModelElement) -> None`
14. `setObjectImplicit` → `set_object_implicit(obj: RPModelElement) -> None`
15. `setUseUniqueStereotypeAndRefCache` → `set_use_unique_stereotype_and_ref_cache(enabled: int) -> None`
16. `setWaitDialogWatchdogValue` → `set_wait_dialog_watchdog_value(value: int) -> None`
17. `startTransactionOfNoCGInterest` → `start_transaction_of_no_cg_interest() -> None`
18. `findElementsWithOSLCLink` (covered in Task 9)
19. `getRoundtripShadowModel` (covered in Task 9)

**Implementation Notes:**
- Various utility methods
- Pattern A for getters returning primitives
- Pattern B for getters returning wrapped elements
- Pattern C for getters returning collections
- Pattern D for setters
- Pattern F for void methods

**Steps:**

- [ ] **Step 1:** Implement all methods following Patterns A, B, C, D, F
- [ ] **Step 2:** Write unit tests
- [ ] **Step 3:** Update checklist markers
- [ ] **Step 4:** Run quality gate
- [ ] **Step 5:** Commit: `feat(models): implement RPProject misc methods (19 methods)`

---

## Task 13: RPActor Method (1 method)

**File:** `src/rhapsody_cli/models/elements/classifiers/model_actor.py`

**Methods:**
1. `updateContainedDiagramsOnServer` → `update_contained_diagrams_on_server() -> None`

**Implementation Notes:**
- Same as package-level method (remote requirements)
- Pattern F for void method

**Steps:**

- [ ] **Step 1:** Implement `update_contained_diagrams_on_server() -> None` using Pattern F
- [ ] **Step 2:** Write unit test
- [ ] **Step 3:** Update checklist marker
- [ ] **Step 4:** Run quality gate
- [ ] **Step 5:** Commit: `feat(models): implement RPActor updateContainedDiagramsOnServer`

---

## Task 14: Full Verification

**Steps:**

- [ ] **Step 1:** Verify no `[ ] impl` markers remain
- [ ] **Step 2:** Run full quality gate: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- [ ] **Step 3:** Verify test coverage: `pytest --cov=src/rhapsody_cli/models --cov-report=term-missing`
- [ ] **Step 4:** Create summary commit if needed

---

## Notes

### Intentional NotImplementedError (skip these)

The following methods in `core.py` intentionally raise `NotImplementedError` for Java API parity (no COM API available):

1. `RPModelElement.createOSLCLink` - Rhapsody COM API does not expose this
2. `RPModelElement.deleteOSLCLink` - Rhapsody COM API does not expose this
3. `RPModelElement.getOSLCLinks` - Rhapsody COM API does not expose this

These are **not** part of the 73 unimplemented methods and should be left as-is.

### Pattern Reference

| Pattern | Use Case | Example |
|---------|----------|---------|
| A | Getter returning primitive | `_get_method_or_property(self._com, "getX", "x")` |
| B | Getter returning wrapped element | `AbstractRPModelElement.wrap(call_com(...))` |
| C | Getter returning collection | `RPCollection(call_com(...))` |
| D | Single-arg setter | `_set_method_or_property(self._com, "setX", "x", value)` |
| E | Adder returning wrapped element | `wrap(call_com(lambda: addXxx(name)))` |
| F | Void method | `call_com(lambda: self._com.method(...))` |
| G | Boolean (0/1) | `int(call_com(...))` |