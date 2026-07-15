# Support Package Integration Tests Completion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add integration tests for as many of the 169 currently-untested methods across `src/rhapsody_cli/models/support/` (codegen, files, IDE tool wrappers) as have a discoverable, real object-creation path through the existing public API; explicitly document the remainder as blocked pending new factory methods.

**Architecture:** New `tests/integration/models/support/` test package mirroring `tests/integration/models/elements/`, with one test file per source file (`test_model_codegen.py`, `test_model_files.py`, `test_model_ide.py`), using shared `rhapsody_app`/`test_project` fixtures. Since this package wraps tool/IDE/codegen APIs rather than model elements, several classes may require a live file-system artifact (e.g. a real generated code file) or may be unreachable without further factory-method work — these are called out explicitly per task rather than silently skipped.

**Tech Stack:** pytest, pywin32 (win32com), live Rhapsody COM API, `uuid.uuid4().hex[:8]`.

## Research summary (read this before executing tasks)

Unlike the other 14 support/elements subpackages, **every single class in `src/rhapsody_cli/models/support/` was found to have zero discoverable public creation path** in the current codebase. This was verified as follows:

1. **`RhapsodyApplication` (`src/rhapsody_cli/application.py`) is a partial wrapper, not a full `IRPApplication` mirror.** It implements only `open_project`, `create_new_project`, `get_projects`, `get_is_hidden_ui`/`set_hidden_ui`, `get_version`, `get_build_no`, `get_rhapsody_dir`, `get_omroot`. Unlike `model_project.py` (which maintains an exhaustive method-parity checklist against `IRPProject`), `application.py` has no such checklist — but a full-repo grep for every one of the 17 support-package class names (`RPCodeGenerator`, `RPSearchManager`, `RPSelection`, `RPRhapsodyServer`, `RPDiagSynthAPI`, `RPRoundTrip`, `RPAXViewCtrl`, `RPExternalIDERegistry`, `RPInternalOEMPlugin`, `RPPlugInWindow`, `RPProgressBar`, `RPowListListener`, `RPowPaneMgr`, `RPowTextListener`, `RPASCIIFile`, `RPControlledFile`, `RPFile`, `RPFileFragment`) outside of `models/support/*.py` itself returned **zero matches**. No getter/factory anywhere in the codebase returns any of these types.
2. **`model_project.py`'s own checklist confirms the gap for `RPProgressBar`:** line 57 reads `# [ ] getNewProgressBar  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test` — the underlying `IRPProject::getNewProgressBar()` COM method is not merely untested, it is **not implemented at all** in `RPProject`. This is concrete evidence that the factory method needed to construct `RPProgressBar` does not exist yet anywhere in the wrapper.
3. **`model_project.py` confirms no code-generation trigger exists:** `RPProject.get_code_generated_files()` (`model_project.py:564`) wraps `IRPProject::getCodeGeneratedFiles()`, a pure getter that only returns non-empty results *after* code generation has actually run for the project. A full-repo grep for `generateCode`/`generate_code` found **no method anywhere** (in `RPProject`, `RPComponent`, or `RPConfiguration`) that triggers code generation. Without that trigger, `get_code_generated_files()` will always return an empty collection in a freshly-created test project, so it cannot be used to obtain a real `RPFile` instance.
4. **`RPModelElement.get_controlled_files()` (`src/rhapsody_cli/models/core.py:686`) exists**, but a grep for `add_controlled_file`/`addControlledFile` found no method anywhere that associates a controlled file with an element. Without a way to create the association, `get_controlled_files()` will return an empty collection for any freshly-created test element, so it cannot be used to obtain a real `RPControlledFile` instance.
5. **None of the 17 classes in `models/support/` are registered via `AbstractRPModelElement.register_wrapper(...)`** (grep for `register_wrapper` in `models/support/*.py` returned zero matches). Even if a COM object of one of these types were returned by some other, already-implemented method via the generic `AbstractRPModelElement.wrap()` dispatch, it would not be dispatched to the correct wrapper class today — reinforcing that these classes are presently unreachable stubs, exactly as their module docstrings ("auto-generated stubs") state.
6. Several classes (`RPBaseExternalCodeGeneratorTool` and its subclasses `RPCodeGenSimplifiersRegistry`/`RPExternalCodeGeneratorInvoker`, `RPExternalCheckRegistry`, `RPExternalIDERegistry`, `RPInternalOEMPlugin`, `RPowListListener`, `RPowTextListener`) are **plugin/callback interfaces** implemented by external tools and invoked *by* Rhapsody (not obtained *from* Rhapsody via a getter). These require an entirely different test strategy (e.g. registering a Python-side COM server as a Rhapsody plugin) that is out of scope for a getter-based integration test and is not addressed by this plan.

**Original conclusion (superseded):** at plan-authoring time, all 169 methods across the 3 files were documented as BLOCKED — no factory method on `RhapsodyApplication` returned any support-package type. **This is no longer fully true:** the xfail-improvements plan added 8 getter methods to `RhapsodyApplication` that return support-package wrappers. See "Newly Unblocked Classes" below. The remaining classes are still blocked.

## Newly Unblocked Classes (from xfail-improvements plan)

The following 8 classes now have factory methods on `RhapsodyApplication` and can be integration-tested:

| Class | Factory method | Methods unblocked |
|-------|---------------|-------------------|
| `RPSearchManager` | `app.get_search_manager()` | 4 |
| `RPSelection` | `app.get_selection()` | 8 |
| `RPCodeGenSimplifiersRegistry` | `app.get_code_gen_simplifiers_registry()` | 1 |
| `RPDiagSynthAPI` | `app.get_diag_synth_api(client_name)` | 7 |
| `RPExternalCheckRegistry` | `app.get_external_checker_registry()` | 2 |
| `RPExternalIDERegistry` | `app.get_external_ide_registry(client_id)` | 3 |
| `RPExternalRoundtripInvoker` | `app.get_external_roundtrip_invoker()` | 0 (only inherited `get_interface_name`) |
| `RPowPaneMgr` | `app.get_ow_pane_mgr(client_id)` | 4 |

The remaining classes (`RPCodeGenerator`, `RPRhapsodyServer`, `RPFile`, `RPControlledFile`, `RPASCIIFile`, `RPProgressBar`, `RPAXViewCtrl`, `RPInternalOEMPlugin`, `RPJavaPlugins`, `RPPlugInWindow`, `RPBaseExternalCodeGeneratorTool`/`RPExternalCodeGeneratorInvoker`, `RPowListListener`, `RPowTextListener`, `RPRoundTrip`, `RPIntegrator`, etc.) are still blocked — no factory method returns them.

## Global Constraints

- Windows-only runtime (requires Windows + a running Rhapsody instance)
- All test classes use `@pytest.mark.integration`
- Tests consume `rhapsody_app`/`test_project` fixtures from `tests/integration/conftest.py` as needed
- Use `_unique(prefix)` with `uuid.uuid4().hex[:8]`
- Always `try/finally` cleanup where applicable
- Assert both `isinstance()` and read-back values where the class supports it
- Flip `[ ] integration test` to `[x]` per task ONLY for methods actually tested; leave blocked methods' checkboxes untouched and instead add an inline TODO comment above the relevant class referencing this plan doc and the missing factory method
- Quality gate after each task: `ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit`
- Import via `src/rhapsody_cli/models/support/__init__.py` re-exports if present, else deep import

---

## Task 1: Create `tests/integration/models/support/` package scaffolding

**Files:**
- Create: `tests/integration/models/support/__init__.py`

**Feasibility:** N/A (scaffolding only). This prepares the test package location for the day a factory method is added and one of the blocked tasks below becomes actionable; no test files are populated yet since every class in this package is currently blocked (see Research summary above).

- [ ] **Step 1: Create the package directory and `__init__.py`**

Mirror the docstring convention of `tests/integration/models/elements/__init__.py`:

```python
"""Integration tests for support wrapper classes (codegen, files, IDE)."""
```

- [ ] **Step 2: Verify pytest discovers the empty package without error**

Run: `pytest tests/integration/models/support/ -m integration -v --collect-only`

Expect zero tests collected, zero errors.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/models/support/__init__.py
git commit -m "test: scaffold tests/integration/models/support package"
```

---

## Task 2: `RPBaseExternalCodeGeneratorTool` / `RPCodeGenSimplifiersRegistry` / `RPExternalCodeGeneratorInvoker` — Document blocked coverage

**Methods in scope (5 total):** `RPBaseExternalCodeGeneratorTool.advance_code_gen_progress_bar`, `should_abort_code_generation`, `write_code_gen_message`; `RPCodeGenSimplifiersRegistry.notify_simplification_done`; `RPExternalCodeGeneratorInvoker.notify_generation_done`.

**Feasibility:** BLOCKED. These three classes form a plugin-callback family: `IRPBaseExternalCodeGeneratorTool` is the base interface for an *external* code-generation tool that Rhapsody calls back into during code generation; `RPCodeGenSimplifiersRegistry` and `RPExternalCodeGeneratorInvoker` are its two concrete registries. No getter anywhere in the codebase returns any of these three types (full-repo grep outside `model_codegen.py` returned zero hits), and there is no code-generation trigger in the wrapper (see Research summary point 3) that would cause Rhapsody to invoke such a callback in the first place. These are not "gettable" objects — they are meant to be *implemented* by external tooling and registered with Rhapsody, which is a fundamentally different (COM server registration) test strategy, out of scope here.

**Required follow-up (out of scope for this plan):** No factory method can make these instantiable in the "get an existing object" sense used elsewhere in this codebase. Enabling integration coverage would require building a Python-side COM server implementing `IRPBaseExternalCodeGeneratorTool`/subinterfaces and registering it as an external code generator tool with Rhapsody — a substantially larger, separate initiative (COM server registration, not a simple wrapper factory method).

- [ ] **Step 1: Add TODO comments**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPBaseExternalCodeGeneratorTool`, `RPCodeGenSimplifiersRegistry`, and `RPExternalCodeGeneratorInvoker`, add:

```python
# TODO(integration-tests): blocked — this is a plugin/callback interface with no
# getter-based creation path; would require registering a COM server as an
# external code generator tool. See
# docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 2.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPBaseExternalCodeGeneratorTool family integration tests as blocked"
```

---

## Task 3: `RPCodeGenerator` — Document blocked coverage

**Methods in scope (2 total):** `get_code_annotations`, `get_generated_file_names`.

**Feasibility:** BLOCKED. `IRPCodeGenerator` represents the actual code generator for a component/configuration. A full-repo grep for `RPCodeGenerator` outside `model_codegen.py` returned zero hits — no `RPComponent`/`RPConfiguration` method returns one.

**Required follow-up (out of scope for this plan):** A method such as `RPComponent.get_code_generator() -> RPCodeGenerator` (wrapping the real `IRPComponent::getCodeGenerator()`/similar COM accessor, name to be confirmed against the Rhapsody COM API reference when implementing) would need to be added to `src/rhapsody_cli/models/elements/containment/model_component.py`.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPCodeGenerator`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RPComponent.get_code_generator() -> RPCodeGenerator.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 3.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPCodeGenerator integration tests as blocked pending factory method"
```

---

## Task 4: `RPDiagSynthAPI` — Document blocked coverage

**Methods in scope (7 total):** `add_instance`, `add_synth_sd_to_model2`, `create_sd2`, `receive_message`, `remove_synth_sd_to_model2`, `s_d_add_condition_mark`, `send_message`.

**Feasibility:** BLOCKED. `IRPDiagSynthAPI` is the sequence-diagram-synthesis API, normally exposed on the application object. A full-repo grep for `RPDiagSynthAPI` outside `model_codegen.py` returned zero hits.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_diag_synth_api() -> RPDiagSynthAPI` would need to be added to `src/rhapsody_cli/application.py`, mirroring the (currently unwrapped) `IRPApplication` accessor for this interface.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPDiagSynthAPI`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.get_diag_synth_api() -> RPDiagSynthAPI.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 4.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPDiagSynthAPI integration tests as blocked pending factory method"
```

---

## Task 5: `RPExternalCheckRegistry` — Document blocked coverage

**Methods in scope (2 total):** `append_failed_elements_comments`, `set_failed_elements_comments`.

**Feasibility:** BLOCKED. `IRPExternalCheckRegistry` is a callback interface implemented by external "model checker" plugins (Rhapsody calls into it to report failed-check comments); it is not obtained via a getter. A full-repo grep for `RPExternalCheckRegistry` outside `model_codegen.py` returned zero hits.

**Required follow-up (out of scope for this plan):** Same plugin-registration caveat as Task 2 — this is a callback interface implemented by external check tooling, not obtainable through a simple factory method. Enabling coverage would require registering a Python-side COM server as an external model-check tool with Rhapsody.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPExternalCheckRegistry`, add:

```python
# TODO(integration-tests): blocked — this is a plugin/callback interface implemented
# by external model-check tools; no getter-based creation path exists.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 5.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPExternalCheckRegistry integration tests as blocked"
```

---

## Task 6: `RPRhapsodyServer` — Document blocked coverage

**Methods in scope (4 total):** `get_application`, `get_hidden_application`, `get_uninitialized_application`, `initialize_application`.

**Feasibility:** BLOCKED. `IRPRhapsodyServer` is the top-level automation server object that itself produces `IRPApplication` instances (i.e. it sits *above* `RhapsodyApplication` in the object hierarchy, not below it). A full-repo grep for `RPRhapsodyServer` outside `model_codegen.py` returned zero hits — nothing in this codebase constructs an `IRPRhapsodyServer` COM object; `RhapsodyApplication.connect()`/`_attach()`/`_launch()` go directly to `IRPApplication` via `win32com.client.GetActiveObject("Rhapsody2.Application.1")` / `Dispatch(...)`, bypassing any server object.

**Required follow-up (out of scope for this plan):** A new top-level entry point, e.g. `RhapsodyServer.connect() -> RPRhapsodyServer` wrapping a distinct COM ProgID for the Rhapsody automation server (to be identified from the Rhapsody COM API reference), would need to be added — likely as a sibling class to `RhapsodyApplication` in a new or existing module, since `RhapsodyApplication` currently has no path to obtain a server-level object.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPRhapsodyServer`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need a new top-level entry point (e.g. RhapsodyServer.connect()) distinct
# from RhapsodyApplication.connect(), wrapping the IRPRhapsodyServer COM ProgID.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 6.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPRhapsodyServer integration tests as blocked pending factory method"
```

---

## Task 7: `RPRoundTrip` — Document blocked coverage

**Methods in scope (1 total):** `roundtrip_file`.

**Feasibility:** BLOCKED. `IRPRoundTrip` performs roundtrip (reverse-engineering) of externally-edited files back into the model. A full-repo grep for `RPRoundTrip` outside `model_codegen.py` returned zero hits.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_round_trip() -> RPRoundTrip` (or a per-project accessor on `RPProject`) would need to be added, wrapping the corresponding `IRPApplication`/`IRPProject` accessor.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPRoundTrip`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.get_round_trip() -> RPRoundTrip.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 7.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPRoundTrip integration tests as blocked pending factory method"
```

---

## Task 8: `RPSearchManager` / `RPSearchQuery` / `RPSearchResult` — Document blocked coverage

**Methods in scope (76 total):** `RPSearchManager.create_search_query`, `search`, `search_and_show_results`, `search_async` (4); `RPSearchQuery` — all 68 non-`get_interface_name` methods (`add_diagram_to_views_list` through `set_views_to_search`, per the checklist at `model_codegen.py:485-553`); `RPSearchResult.get_matched_field`, `get_matched_fields`, `get_matched_object`, `get_name` (4).

**Feasibility:** BLOCKED. All three classes form one dependency chain: `RPSearchQuery` is only constructible via `RPSearchManager.create_search_query()`, and `RPSearchResult` instances are only produced inside the `RPCollection` returned by `RPSearchManager.search()`. Since `RPSearchManager` itself has no creation path (full-repo grep for `RPSearchManager` outside `model_codegen.py` returned zero hits — no method on `RhapsodyApplication` or any model element returns one), all three classes are blocked together.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_search_manager() -> RPSearchManager` would need to be added to `src/rhapsody_cli/application.py`, wrapping the real `IRPApplication` search-manager accessor. Once that single method exists, `RPSearchQuery` (via `create_search_query()`) and `RPSearchResult` (via `search()` on a populated model) both become testable without further factory work.

- [ ] **Step 1: Add TODO comments**

In `src/rhapsody_cli/models/support/model_codegen.py`, above `RPSearchManager`, `RPSearchQuery`, and `RPSearchResult`, add (adjust wording per class):

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need RhapsodyApplication.get_search_manager() -> RPSearchManager; RPSearchQuery
# and RPSearchResult are only reachable through that manager (create_search_query()/search()).
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 8.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_codegen.py
git commit -m "docs: flag RPSearchManager/RPSearchQuery/RPSearchResult integration tests as blocked"
```

---

## Task 9: `RPExternalRoundtripInvoker` / `RPIntegrator` / `RPJavaPlugins` — No additional methods in scope

**Methods in scope (0 total, out of the 169 tracked).** These three classes (`RPExternalRoundtripInvoker` in `model_codegen.py`, `RPIntegrator` in `model_codegen.py`, `RPJavaPlugins` in `model_ide.py`) each declare only the inherited `get_interface_name` method in their checklist, with no additional own methods — so they contribute zero rows to the 169-method total this plan tracks. `get_interface_name` behavior is inherited from `RPModelElement` and is exercised generically wherever any `RPModelElement` subclass is integration-tested elsewhere; it does not need dedicated per-subclass integration coverage here.

**Feasibility:** BLOCKED for object creation (same evidence as other classes — zero hits in a full-repo grep outside `models/support/`), but since there are zero class-specific methods to cover, no TODO/test action is required for these three classes beyond noting them here for completeness in the self-review tally.

- [ ] **Step 1: No code changes required.** This task exists purely to document that these three classes are fully accounted for (with zero methods) in the self-review tally below.

---

## Task 10: `RPASCIIFile` — Document blocked coverage

**Methods in scope (4 total):** `close`, `get_interface_name` (explicitly re-checklisted with its own docstring/unit-test/integration-test columns for this class), `open`, `write`.

**Feasibility:** BLOCKED. `IRPASCIIFile` represents a plain-text file handle for reading/writing arbitrary ASCII files from Rhapsody automation. A full-repo grep for `RPASCIIFile` outside `model_files.py` returned zero hits — no method anywhere constructs one.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_ascii_file() -> RPASCIIFile` (or a similarly-named factory, matching whatever accessor the real `IRPApplication` exposes for ASCII file handles — to be confirmed against the Rhapsody COM API reference) would need to be added to `src/rhapsody_cli/application.py`.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_files.py`, above `RPASCIIFile`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.get_ascii_file() -> RPASCIIFile.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 10.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py
git commit -m "docs: flag RPASCIIFile integration tests as blocked pending factory method"
```

---

## Task 11: `RPControlledFile` — Document blocked coverage

**Methods in scope (3 total):** `get_full_path_file_name`, `open`, `set_target`.

**Feasibility:** BLOCKED. `RPModelElement.get_controlled_files()` (`src/rhapsody_cli/models/core.py:686`) exists and would, in principle, return a `RPCollection` of `RPControlledFile` for any model element — but a full-repo grep for `add_controlled_file`/`addControlledFile` found no method anywhere that associates a controlled file with a model element. Without that association step, `get_controlled_files()` always returns an empty collection for a freshly-created test element (see Research summary point 4), so no real `RPControlledFile` instance can be obtained today.

**Required follow-up (out of scope for this plan):** A method such as `RPModelElement.add_controlled_file(filename: str) -> RPControlledFile` (wrapping the corresponding `IRPModelElement` COM method used to register a controlled file) would need to be added to `src/rhapsody_cli/models/core.py`.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_files.py`, above `RPControlledFile`, add:

```python
# TODO(integration-tests): blocked — RPModelElement.get_controlled_files() exists but
# nothing in the codebase can create/associate a controlled file with an element yet
# (no add_controlled_file()). Would need e.g.
# RPModelElement.add_controlled_file(filename) -> RPControlledFile.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 11.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py
git commit -m "docs: flag RPControlledFile integration tests as blocked pending factory method"
```

---

## Task 12: `RPFile` — Document blocked coverage

**Methods in scope (15 total):** `add_element`, `add_model_element`, `add_package_to_scope`, `add_text_element`, `add_to_scope`, `get_elements`, `get_file_fragments`, `get_file_type`, `get_files`, `get_imp_name`, `get_path`, `get_spec_name`, `is_empty`, `set_file_type`, `set_path`.

**Feasibility:** BLOCKED. `RPProject.get_code_generated_files()` (`model_project.py:564`) exists and returns an `RPCollection` that would contain `RPFile` instances — but only *after* code generation has actually run against the project. A full-repo grep for `generateCode`/`generate_code` found no method anywhere (on `RPProject`, `RPComponent`, or `RPConfiguration`) that triggers code generation (see Research summary point 3). Without that trigger, `get_code_generated_files()` returns an empty collection for a freshly-created test project, so no real `RPFile` instance can be obtained today.

**Required follow-up (out of scope for this plan):** A method such as `RPProject.generate_code(component: "RPComponent") -> None` (or a similar accessor on `RPComponent`/`RPConfiguration`, wrapping the real `IRPProject::generateCode()`/`IRPComponent::generateCode()` COM method — name to be confirmed against the Rhapsody COM API reference) would need to be added, after which `get_code_generated_files()` could be exercised for real.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_files.py`, above `RPFile`, add:

```python
# TODO(integration-tests): blocked — RPProject.get_code_generated_files() exists but
# nothing in the codebase can trigger code generation yet (no generate_code()).
# Would need e.g. RPProject.generate_code(component) -> None (or an equivalent on
# RPComponent/RPConfiguration) before this getter returns anything non-empty.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 12.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py
git commit -m "docs: flag RPFile integration tests as blocked pending code-generation trigger"
```

---

## Task 13: `RPFileFragment` — Document blocked coverage

**Methods in scope (5 total):** `get_fragment_element`, `get_fragment_text`, `get_fragment_type`, `move_fragment_in_owner`, `set_fragment_text`.

**Feasibility:** BLOCKED. `RPFile.get_file_fragments()` is the only path to an `RPFileFragment` instance, and `RPFile` itself is blocked (Task 12). This class is therefore blocked transitively.

**Required follow-up (out of scope for this plan):** Same as Task 12 — once a code-generation trigger exists and produces real `RPFile` instances, `get_file_fragments()` becomes exercisable without any additional factory work specific to `RPFileFragment`.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_files.py`, above `RPFileFragment`, add:

```python
# TODO(integration-tests): blocked (transitively) — only reachable via
# RPFile.get_file_fragments(), and RPFile itself has no creation path yet
# (see Task 12). See docs/superpowers/plans/2026-07-14-integration-tests-support.md
# Task 13.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_files.py
git commit -m "docs: flag RPFileFragment integration tests as blocked (depends on RPFile)"
```

---

## Task 14: `RPAXViewCtrl` — Document blocked coverage

**Methods in scope (2 total):** `do_command`, `execute_command`.

**Feasibility:** BLOCKED. `IRPAXViewCtrl` is an ActiveX view-control wrapper for embedding Rhapsody views in host applications. A full-repo grep for `RPAXViewCtrl` outside `model_ide.py` returned zero hits.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_ax_view_ctrl() -> RPAXViewCtrl` would need to be added to `src/rhapsody_cli/application.py`.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPAXViewCtrl`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.get_ax_view_ctrl() -> RPAXViewCtrl.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 14.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPAXViewCtrl integration tests as blocked pending factory method"
```

---

## Task 15: `RPExternalIDERegistry` — Document blocked coverage

**Methods in scope (3 total):** `progress_task_asynch_callback`, `progress_task_asynch_eliminate`, `send_ide_text_message`.

**Feasibility:** BLOCKED. `IRPExternalIDERegistry` is a callback interface implemented by external IDE integrations (Rhapsody calls into it), not obtained via a getter. A full-repo grep for `RPExternalIDERegistry` outside `model_ide.py` returned zero hits.

**Required follow-up (out of scope for this plan):** Same plugin-registration caveat as Task 2/5 — this would require registering a Python-side COM server as an external IDE integration with Rhapsody, a substantially larger separate initiative rather than a simple factory method.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPExternalIDERegistry`, add:

```python
# TODO(integration-tests): blocked — this is a plugin/callback interface implemented
# by external IDE integrations; no getter-based creation path exists.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 15.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPExternalIDERegistry integration tests as blocked"
```

---

## Task 16: `RPInternalOEMPlugin` — Document blocked coverage

**Methods in scope (14 total):** `active_project_about_to_change`, `active_project_has_changed`, `on_menu_item_select`, `on_menu_item_select_with_parameters`, `rhap_plugin_animation_stopped`, `rhp_plugin_animation_started`, `rhp_plugin_cleanup`, `rhp_plugin_do_command`, `rhp_plugin_final_cleanup`, `rhp_plugin_init`, `rhp_plugin_invoke_item`, `rhp_plugin_on_ide_build_done`, `rhp_plugin_set_application`, `rhp_saving_project`.

**Feasibility:** BLOCKED. `IRPInternalOEMPlugin` is the base plugin interface that Rhapsody calls into for OEM/internal plugins (lifecycle hooks like init/cleanup, menu selection, build-done notifications). It is implemented by plugin authors and registered with Rhapsody, not obtained via a getter. A full-repo grep for `RPInternalOEMPlugin` outside `model_ide.py` returned zero hits.

**Required follow-up (out of scope for this plan):** Same plugin-registration caveat as Task 2/5/15 — would require a full plugin registration mechanism (COM server implementing `IRPInternalOEMPlugin`, registered with Rhapsody's plugin manager), which is a substantially larger separate initiative.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPInternalOEMPlugin`, add:

```python
# TODO(integration-tests): blocked — this is a plugin lifecycle interface implemented
# by OEM/internal plugins and invoked by Rhapsody; no getter-based creation path exists.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 16.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPInternalOEMPlugin integration tests as blocked"
```

---

## Task 17: `RPPlugInWindow` — Document blocked coverage

**Methods in scope (8 total):** `destroy_window`, `get_docking`, `get_pos_string`, `get_window_handle`, `set_docking`, `set_pos_string`, `set_title`, `show_window`.

**Feasibility:** BLOCKED. `IRPPlugInWindow` represents a dockable custom window hosted inside Rhapsody's UI, created by a plugin. A full-repo grep for `RPPlugInWindow` outside `model_ide.py` returned zero hits.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.add_plug_in_window(title: str) -> RPPlugInWindow` would need to be added to `src/rhapsody_cli/application.py`, wrapping the real `IRPApplication` accessor for creating a plugin window.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPPlugInWindow`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.add_plug_in_window(title) -> RPPlugInWindow.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 17.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPPlugInWindow integration tests as blocked pending factory method"
```

---

## Task 18: `RPProgressBar` — Document blocked coverage

**Methods in scope (2 total):** `reset`, `tick`.

**Feasibility:** BLOCKED, with direct evidence. `src/rhapsody_cli/models/elements/containment/model_project.py:57` lists `# [ ] getNewProgressBar  [ ] impl  [ ] docstring  [ ] unit test  [ ] integration test` in `RPProject`'s own method-parity checklist — the underlying `IRPProject::getNewProgressBar()` COM method is confirmed **not implemented at all** in this wrapper (not merely untested). This is the single factory method that would construct an `RPProgressBar`.

**Required follow-up (out of scope for this plan):** Implement `RPProject.get_new_progress_bar() -> RPProgressBar` in `src/rhapsody_cli/models/elements/containment/model_project.py`, wrapping `IRPProject::getNewProgressBar()`, following the "Adding a New Element Wrapper" / method-implementation conventions in `AGENTS.md`. This is a self-contained, low-risk addition (a single no-arg getter) and would be a good first candidate for a follow-up PR that unblocks this task.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPProgressBar`, add:

```python
# TODO(integration-tests): blocked — IRPProject::getNewProgressBar() is not yet
# implemented (see model_project.py's own checklist, "getNewProgressBar" row).
# Implementing RPProject.get_new_progress_bar() -> RPProgressBar would unblock this.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 18.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPProgressBar integration tests as blocked pending getNewProgressBar"
```

---

## Task 19: `RPSelection` — Document blocked coverage

**Methods in scope (8 total):** `can_copy`, `can_cut`, `can_delete`, `can_paste`, `copy_selected`, `cut_selected`, `delete_selected`, `paste_selected`.

**Feasibility:** BLOCKED. `IRPSelection` provides cut/copy/paste/delete for the currently-selected graphic element on a diagram — it depends on live UI selection state. A full-repo grep for `RPSelection` outside `model_ide.py` returned zero hits.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_selection() -> RPSelection` would need to be added to `src/rhapsody_cli/application.py`, wrapping the real `IRPApplication` selection accessor. Note that even once implemented, tests would additionally need a way to programmatically select a graphic element on an open diagram before this class becomes meaningfully testable — worth flagging in that follow-up work.

- [ ] **Step 1: Add TODO comment**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPSelection`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need e.g. RhapsodyApplication.get_selection() -> RPSelection, plus a way to
# programmatically select a graphic element on an open diagram.
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 19.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPSelection integration tests as blocked pending factory method"
```

---

## Task 20: `RPowListListener` / `RPowPaneMgr` / `RPowTextListener` — Document blocked coverage

**Methods in scope (8 total):** `RPowListListener.dbl_click_notify`, `set_obj_id` (2); `RPowPaneMgr.add_tab_notify`, `close_tab_notify`, `get_ow_list_listener`, `get_ow_text_listener` (4); `RPowTextListener.dbl_click_notify`, `set_obj_id` (2).

**Feasibility:** BLOCKED. These three classes form one dependency chain: `RPowListListener` and `RPowTextListener` are only obtainable via `RPowPaneMgr.get_ow_list_listener(id)`/`get_ow_text_listener(id)`, and `RPowPaneMgr` itself (the output-window pane manager) has no creation path — a full-repo grep for `RPowPaneMgr`, `RPowListListener`, and `RPowTextListener` outside `model_ide.py` returned zero hits. These are also callback/listener interfaces tied to custom Output Window tabs created by a plugin, similar in nature to Task 16.

**Required follow-up (out of scope for this plan):** A method such as `RhapsodyApplication.get_ow_pane_mgr() -> RPowPaneMgr` would need to be added to `src/rhapsody_cli/application.py`. Even then, `get_ow_list_listener`/`get_ow_text_listener` require a `s_obj_i_d` for a tab that a plugin has already registered via `add_tab_notify` — so full coverage would additionally require a working plugin-registration flow (see Task 16).

- [ ] **Step 1: Add TODO comments**

In `src/rhapsody_cli/models/support/model_ide.py`, above `RPowListListener`, `RPowPaneMgr`, and `RPowTextListener`, add:

```python
# TODO(integration-tests): blocked — no public factory method returns this class yet.
# Would need RhapsodyApplication.get_ow_pane_mgr() -> RPowPaneMgr; RPowListListener and
# RPowTextListener are only reachable through that manager for tabs a plugin has
# already registered (see Task 16 for the related plugin-registration gap).
# See docs/superpowers/plans/2026-07-14-integration-tests-support.md Task 20.
```

- [ ] **Step 2: Commit**

```bash
git add src/rhapsody_cli/models/support/model_ide.py
git commit -m "docs: flag RPowListListener/RPowPaneMgr/RPowTextListener integration tests as blocked"
```

---

## Task 21: Full Package Verification

**Goal:** Confirm every one of the 169 tracked methods across `model_codegen.py` (97), `model_files.py` (27), and `model_ide.py` (45) is accounted for in exactly one task above, and report the final tally.

- [ ] **Step 1: Re-run the method inventory and cross-check against this plan**

```bash
grep -c "integration test" src/rhapsody_cli/models/support/model_codegen.py src/rhapsody_cli/models/support/model_files.py src/rhapsody_cli/models/support/model_ide.py
```

Expect `97`, `27`, and `54` respectively (the `model_ide.py` raw count of 54 includes 9 inherited `get_interface_name` rows that are excluded from the 169-method tracked total, per the Research summary — 54 − 9 = 45).

- [ ] **Step 2: Confirm TODO markers were added for every blocked class**

```bash
grep -rn "TODO(integration-tests)" src/rhapsody_cli/models/support/
```

Expect one TODO block per class covered by Tasks 2–8 and 10–20 (17 classes total; `RPExternalRoundtripInvoker`, `RPIntegrator`, `RPJavaPlugins` from Task 9 intentionally have no TODO since they have zero methods to flag).

- [ ] **Step 3: Run the quality gate**

```bash
ruff check src/ tests/ && black --check src/ tests/ && mypy src/ tests/ && pytest tests/unit
```

- [ ] **Step 4: Report the final tally**

- Methods tested (feasible, integration test written): **0 / 169**
- Methods documented as blocked (TODO comment added, no factory path exists): **169 / 169**
  - `model_codegen.py`: 97 blocked (Tasks 2–9)
  - `model_files.py`: 27 blocked (Tasks 10–13)
  - `model_ide.py`: 45 blocked (Tasks 14–20)
- Classes with zero in-scope methods (no action needed): `RPExternalRoundtripInvoker`, `RPIntegrator`, `RPJavaPlugins` (Task 9)
- Total tasks in this plan: 21 (1 scaffolding + 19 per-class/family documentation tasks + 1 verification)

- [ ] **Step 5: Commit the verification (if any residual changes)**

```bash
git status
# If clean, no commit needed — all prior tasks already committed their changes.
```
